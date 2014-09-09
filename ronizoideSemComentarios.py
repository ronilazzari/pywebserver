#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''

ronizoide versao 0.1

Servidor web basico feito como atividade da disciplina 
de Redes de Computadores da Faculdade de Engenharia 
Eletrica da Universidade de Uberlandia.

O programa implementa parcialmente e de forma simples 
o protocolo HTTP/1.1.

Autor: Roni Gilberto Goncalves
Numero de matricula: 10921EEL026

'''

from socket import *
from time import gmtime, strftime
from constants import *

def descobre_tipo_conteudo(string):
	
	tipo_conteudo = []
	auxiliar = ''
	
	for i in range(len(string)):

		auxiliar = string[(len(string) - 1) - i]
		
		if (auxiliar == '.'):
			
			break
		else:
			
			tipo_conteudo.append(auxiliar)
	
	tipo_conteudo.reverse()
	
	return ''.join(tipo_conteudo)

def make_header(TYPE_OF_CONTENT):

	header = ''
	header = ('Connection: ' + CNX + 'Date: ' + strftime("%a, %d %b %Y %X GMT", gmtime()) + '\r\n' + 'Server: ' + SERVERNAME)
	
	if (TYPE_OF_CONTENT == 'JPG' or TYPE_OF_CONTENT == 'jpg'):
		
		header = header + CONTENT_TYPE_JPG + '\r\n'
	else:
		header = header + CONTENT_TYPE_TXT + '\r\n'
		
	return header

conexao = socket(AF_INET, SOCK_STREAM)

conexao.bind(('', 65000))

conexao.listen(10)

while True:
	
	client,addr = conexao.accept()
	print 'Conexao estabelecida com ', addr

	msg = client.recv(4096)

	msglist = msg.split()

	object_path = msglist[1]

	content_type = descobre_tipo_conteudo(msglist[1])

	existearquivo = True

	if msglist[0] == 'GET':
		
		try:
			arquivo_pedido = open(('root' + object_path), 'rb')
		
		except IOError:
			
			existearquivo = False

		if (existearquivo):
		
			client.send(OK_RESPONSE)
			client.send(make_header(content_type))
			arquivo_lido = arquivo_pedido.read()
			arquivo_pedido.close()
			client.send(arquivo_lido)
			client.send('\r\n')

		else:
			
			client.send(NOTFOUND_RESPONSE)
			client.send(make_header('text/html'))
			
			arquivo_pedido = open('root/404/404.htm', 'r')
			arquivo_lido = arquivo_pedido.read()
			arquivo_pedido.close()
			
			client.send(arquivo_lido)
			client.send('\r\n')

	else:
		client.send(BAD_REQUEST)

	print msglist

	msglist = []

	client.close()
