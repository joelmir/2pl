# -*- coding: utf-8 -*-

historias = []

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

#Lê o arquivo e valida as informações    
for historia in open('historia.txt','r').readlines():
    var = valida_historia(historia)
    if var != -1:
        historias.append(var)
        
if historias:
    print 'História valida! :)\n'
    
for h in historias:
    dados = {}
    for d in h['dados']:
        dados[d] = {'transacao':[], 'tipo',''}
    
    for acao in d['hist']:
        if acao['operacao'] == 'c':
            pass
        
        or (dados[acao['dado']]['tipo'] == 'w' and dados[acao['dado']]['transacao'] == acao['transacao'])  
        
        if acao['operacao'] == 'r':
            if dados[acao['dado']]['tipo'] in ['','r']: 
                dados[acao['dado']]['tipo'] = 'r'
                dados[acao['dado']]['transacao'].append(acao['transacao'])
            else:
                t =  [1 for x in dados[acao['dado']]['transacao'] if x != acao['transacao']]:
                print 'Existe '+str(t)+' transacoes em conflito com a acao '+str(acao)
                return
        
        if acao['operacao'] == 'w':
            if dados[acao['dado']]['tipo']  = '':
                
            
            
    








