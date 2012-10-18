# -*- coding: utf-8 -*-

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
    

historias = open('historia.txt','r')
for historia in historias.readlines():
    var = valida_historia(historia)
    if var != -1:
        print var    

