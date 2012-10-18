# -*- coding: utf-8 -*-

def valida_historia(historia):
    for operacao in historia.split():
        
        hist={'transacoes':[], 'dados'= [] }
        
        inicio = operacao.find('(')
        fim = operacao.find(')')
        if inicio +1 <= fim or len(operacao[:inicio]) <=0:
            print 'Erro na operacao '+operacao
            return -1
        hist['dados'].append(operacao[inicio:fim])
        hist['transacoes'].append(operacao[:inicio)
    

historias = open('historia.txt','r')
for historia in hitoria.readlines():
    var = valida_historia(historia)
    if var != -1:
        print var    

