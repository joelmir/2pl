# -*- coding: utf-8 -*-
import pdb, random, sys


def valida_historia(historia):
    
    h ={'transacoes':[], 'dados':[], 'hist':[] }
    
    for operacao in historia.split():
        
        inicio = operacao.find('(')
        fim = operacao.find(')')
        op = {}
        
        if not (len(operacao) == 2 and operacao[0] == 'c'):
            if operacao[0] not in ['r','w']:
                print 'Erro na operacao '+operacao+' (Não foi definida o tipo da operacao "read" ou "write" )'
                return -1
            elif inicio +1 >= fim:
                print 'Erro na operacao '+operacao+' (Não contém dados)'
                return -1
            elif len(operacao[1:inicio]) == 0:
                print 'Erro na operacao '+operacao+' (Não contém transação)'
                return -1
        
            h['dados'].append(operacao[inicio+1:fim])
            h['transacoes'].append(operacao[1:inicio])
            
            op['transacao'] = operacao[1:inicio]
            op['dado'] = operacao[inicio+1:fim]
            op['operacao'] = operacao[0]
            
        else:
            op['transacao'] = operacao[1]
            op['operacao'] = operacao[0]
               
        h['hist'].append(op)
        
    h['transacoes'] = list(set(h['transacoes']))
    h['dados'] = list(set(h['dados']))
    return h

    
def commit(acao,dados):
    #pdb.set_trace()
    for k in [k for k in dados.keys() if acao['transacao'] in dados[k]['transacao']]:
        dados[k]['transacao'].remove(acao['transacao'])
                
        if not dados[k]['transacao'] or dados[k]['tipo'] == 'w':
           dados[k]['tipo'] = ''
    #pdb.set_trace()
    return dados

def reorganiza_historia(historico,acao,dados,rodada_bloqueada):
    
    #incrementa a rodada bloqueada
    rodada_bloqueada+=1
    #verifica qual é o momento da história que aconteceu o bloqueio
    
    bloqueio = historico.index(acao)
    
    #elimina a transação história que ainda deve ser processada
    historia_futu = [h for h in historico[bloqueio:] if h['transacao'] != acao['transacao']]
    
    #verifica se ja faz muitas acoes que está bloqueado, pode ser um deadlock
    if rodada_bloqueada >= (len(historico) - bloqueio):
        print 'DeadLock!!!'
        rodada_bloqueada = 0
        
        #elimina a transacao da historia original que já foi processada
        historia_pass = [h for h in historico[:bloqueio] if h['transacao'] != acao['transacao']]
        
        #carrega toda a transacao que deseja reordenar na execução da história...
        transacao = [h for h in historico if h['transacao'] == acao['transacao']]
        
        #reorganiza os dados...
        dados = commit(acao,dados)
    
    #trata como um simples bloqueio    
    else:
        
        print 'Bloqueio!!! (',rodada_bloqueada,')'
        
        #Mantem a história ja executada sem retirar a transação bloqueada
        historia_pass = historico[:bloqueio]
        
        #descobre quais são as operacoes que a transação bloqueada ainda precisa realizar
        transacao = [h for h in historico[bloqueio:] if h['transacao'] == acao['transacao']]
        
    historia_new = []
    
    #gera uma posiçao onde será reordenada a transação cancelada...
    next_position = random.randrange(len(historia_futu))

    #Intercala com as operações restantes
    for idx,h in enumerate(historia_futu):
        historia_new.append(h)
        if idx > next_position:
            if (idx%2 != 0 and transacao):
                historia_new.append(transacao[0])
                transacao.remove(transacao[0])
                
    #caso ainda existe pedaços da transação para executar, então adiciona no final...
    if transacao:
        historia_new.extend(transacao)
        
    
    
    #pdb.set_trace()
    op = valida_operacao(historia_new,dados, rodada_bloqueada)
    
    #valida o restante na nova historia
    historia_pass.extend(op)
    return historia_pass
    
    

def valida_operacao(historico,dados,bloqueio):

    for idx, acao in enumerate(historico):
        if acao['operacao'] == 'c':
            dados = commit(acao,dados)
                
        elif acao['operacao'] == 'r':
            if dados[acao['dado']]['tipo'] in ['','r']: 
                dados[acao['dado']]['tipo'] = 'r'
                dados[acao['dado']]['transacao'].append(acao['transacao'])
            else:
                t =  [ x for x in dados[acao['dado']]['transacao'] if x != acao['transacao'] ]
                if t:
                    print 'Existe '+str(t)+' transacoes em conflito com a acao '+str(acao)
                    return reorganiza_historia(historico,acao,dados,bloqueio)
                    
        
        elif acao['operacao'] == 'w':
            
            if dados[acao['dado']]['tipo']  == '':
                dados[acao['dado']]['tipo']  = 'w'
                dados[acao['dado']]['transacao'].append(acao['transacao'])
                
            
            elif dados[acao['dado']]['tipo']  == 'r':
                t =  [x for x in dados[acao['dado']]['transacao'] if x != acao['transacao']]
                if t:
                    print 'Existe '+str(t)+' transacoes lendo o dado, em conflito com a acao '+str(acao)
                    return reorganiza_historia(historico,acao,dados,bloqueio)
                else:
                    dados[acao['dado']]['tipo']  = 'w'
                    
            else:
                t =  [x for x in dados[acao['dado']]['transacao'] if x != acao['transacao']]
                if t:
                    print 'A transacao '+t[0]+' contém bloqueio exclusivo ao dado, gerando conflito com a acao '+str(acao)
                    return reorganiza_historia(historico,acao,dados,bloqueio)
         
        #Se conseguiu executar uma transação, não tem poossivel deadlook zera o bloqueio
        bloqueio = 0              
    return historico

historias = []


#verifica se possui ou não parametros para gerar uma história ler a existente...
if not sys.argv:
    #Lê o arquivo e valida as informações    
    for historia in open('historia.txt','r').readlines():
        var = valida_historia(historia)
        if var != -1:
            historias.append(var)
else:

    #TODO
    
    
    #Lê o arquibo e gera uma história com as transações...
    historia = []
    for transacao in open('transacoes.txt','r').readlines():
        historia.append(transacao.split())
    
    #cria a nova historia
    historia_new = []
    
    #Se existir historia....
    if historia:
        for transacao in historia:
        
            #gera uma posiçao onde será reordenada a transação cancelada...
            next_position = random.randrange(1,4)
            
            #cria uma cópia da historia...
            historia_old=[]
            historia_old[:] = historia_new[:]
            
            historia_new =[]
            
            #Intercala com as operações restantes na historia já gerada
            for idx,hist in enumerate(historia_old):
                historia_new.append(hist)
                if (idx%next_position != 0 and transacao):
                    historia_new.append(transacao[0])
                    transacao.remove(transacao[0])
            if transacao:
                historia_new.extend(transacao)
    else:
        print 'Opppsssss'
        exit(0)
        
    
    #valida a historia gerada...
    var = valida_historia((' '.join(historia_new)))
    if var != -1:
       historias.append(var)
        
if historias:
    print '\nAvaliação sintatica válida! :)\n'
    

for h in historias:
    dados = {}
    print '\n'
    
    for d in h['dados']:
        dados[d] = {'transacao':[], 'tipo':''}
    
    for contexto in h['hist']:
        print contexto    
    print '\n'
    
    h['hist'] = valida_operacao(h['hist'], dados,0)  
    
    print 'História  válida!'
       
    for contexto in h['hist']:
        print contexto
           








