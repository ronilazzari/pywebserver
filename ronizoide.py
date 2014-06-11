#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''

ronizoide versão 0.1

Servidor web básico feito como atividade da disciplina 
de Redes de Computadores da Faculdade de Engenharia 
Elétrica da Universidade de Uberlândia.

O programa implementa de forma simples o protocolo 
HTTP1.1.

Autor: Roní Gilberto Gonçalves
Número de matrícula: 10921EEL026

'''

# importando o módulo socket para criar os sockets do servidor
from socket import *

# importanto o módulo que fornece informações sobre o tempo de acordo
# com o sistema
#import time

conexao = socket(AF_INET, SOCK_STREAM)

conexao.bind(('', 65000))

conexao.listen(10)


while 1:
	
	client,addr = conexao.accept()
	print 'Conexão estabelecida com ', addr
	client.send('É isso aí, irmão!')
	client.close()
