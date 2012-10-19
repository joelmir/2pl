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
    print '\nAvaliação sintatica válida! :)\n'
    
def valida_operacao(historico):
    for acao in historico:
        if acao['operacao'] == 'c':
            for k in [k for k in dados.keys() if acao['transacao'] in dados[k]['transacao']]:
                dados[k]['transacao'].del(acao['transacao'])
                
                if not dados[k]['transacao'] or dados[acao['dado']]['tipo'] == 'w':
                    dados[acao['dado']]['tipo'] = ''
                
        if acao['operacao'] == 'r':
            if dados[acao['dado']]['tipo'] in ['','r']: 
                dados[acao['dado']]['tipo'] = 'r'
                dados[acao['dado']]['transacao'].append(acao['transacao'])
            else:
                t =  [ x for x in dados[acao['dado']]['transacao'] if x != acao['transacao'] ]
                if t:
                    print 'Existe '+str(t)+' transacoes em conflito com a acao '+str(acao)
                    return False
        
        if acao['operacao'] == 'w':
            
            if dados[acao['dado']]['tipo']  == '':
                dados[acao['dado']]['tipo']  = 'w'
                dados[acao['dado']]['transacao'].append(acao['transacao'])
                
            
            elif dados[acao['dado']]['tipo']  == 'r':
                t =  [x for x in dados[acao['dado']]['transacao'] if x != acao['transacao']]
                if t:
                    print 'Existe '+str(t)+' transacoes lendo o dado, em conflito com a acao '+str(acao)
                    return False
                else:
                    dados[acao['dado']]['tipo']  = 'w'
                    
            else:
                t =  [x for x in dados[acao['dado']]['transacao'] if x != acao['transacao']]
                if t:
                    print 'A transacao '+t[0]+' contém bloqueio exclusivo ao dado, gerando conflito com a acao '+str(acao)
                    return False
    return True
for h in historias:
    dados = {}
    for d in h['dados']:
        dados[d] = {'transacao':[], 'tipo':''}
    
    if valida_operacao(h['hist']):
        print 'História  válida!\n\n'+str(h['hist'])               








