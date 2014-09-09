#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''

ronizoide versão 0.1

Servidor web básico feito como atividade da disciplina 
de Redes de Computadores da Faculdade de Engenharia 
Elétrica da Universidade de Uberlândia.

O programa implementa parcialmente e de forma simples 
o protocolo HTTP/1.1.

Autor: Roní Gilberto Gonçalves
Número de matrícula: 10921EEL026

'''

# importando o módulo socket para criar os sockets do servidor
from socket import *

# importanto o módulo que fornece informações sobre o tempo 
# de acordo com o sistema. Esta informação será usada no 
# cabeçalho da mensagem HTTP
from time import gmtime, strftime

# importando o arquivo constants.py, que contém algumas 
# constantes úteis e separadas do código original por 
# questão de legibilidade

from constants import *


# @ Função descobre_tipo_conteudo(string)
# 
# Esta função recebe uma string contendo o objeto solicitado
# pelo comando GET retornando o tipo de arquivo desejado de
# acordo com a extensão dele, por exemplo: .htm, .jpg, etc.
#
# @ Argumento recebido: string
# @ Tipo retornado: string 
#
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

# @ Função make_header(TYPE_OF_CONTENT)
# 
# Esta função recebe uma string retornada pela função
# descobre_tipo_conteudo(). Ela retorna o cabeçalho
# da mensagem HTTP para dois tipos de arquivos: html ou 
# jpeg. Essa função não está completa... se ela receber
# um conteúdo diferente de jpeg, o tipo de conteúdo será
# considerado como text/html.
#
# A formatação da data no cabeçalho está de acordo com a
# RFC 2616, seção 14, ítem 18:
#
# http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
#
# Por que fiz essa função com nome em inglês e a anterior
# em português? R: nem mesmo eu sei.
#
# @ Argumento recebido: string
# @ Tipo retornado: string 
#
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

#
# Laço infinito em que o servidor ronizoide ficará
# disponível e aceitará os pedidos de conexão feitos
# por quaisquer clientes, desde que o servidor não
# esteja ocupado com outro cliente.
#
while True:
	
	client,addr = conexao.accept()
	print 'Conexão estabelecida com ', addr

# A mensagem recebida do cliente web não terá mais dois
# que 4096 bytes	
	msg = client.recv(4096)

# A mensagem recebida do cliente é uma string. O método split()
# aplicado a ela cria uma lista chamada msglist
	msglist = msg.split()

# O segundo elemento da lista msglist corresponde ao objeto requerido
# pelo comando GET feito pelo cliente web. Neste programa só vou me
# preocupar com o comando GET. Há outros como POST, OPTION que serão
# ignorados.
# O índice do segundo elemento é 1 porque em Python, assim como em C
# as contagens se iniciam em 0.
	object_path = msglist[1]

# Salvo na variável content_type justamente o valor retornado pela
# função descobre_tipo_conteudo()
	content_type = descobre_tipo_conteudo(msglist[1])

# Variável booleana inicializada com True
	existearquivo = True
	
#
# Ao receber a mensagem do cliente web, o programa verifica se
# o comando é GET. Se o for, procura o objeto solicitado e o 
# envia ao cliente. Se o comando recebido for qualquer outro
# que não o GET, o programa envia a mensagem BAD REQUEST. Não
# é uma boa solução, mas ao menos o programa trata de reponder
# a um comando não suportado por ele. :-\
#
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

# Caso o objeto solicitado pelo cliente web não exista no diretório
# em que o programa procura por arquivos ('diretorio_local/root/')
# o servidor web envia uma mensagem de erro 404 e exibe a página
# específica para isso onde o usuário pode retornar à página
# principal 'index.htm'
		else:
			
			client.send(NOTFOUND_RESPONSE)
			client.send(make_header('text/html'))
			
			arquivo_pedido = open('root/404/404.htm', 'r')
			arquivo_lido = arquivo_pedido.read()
			arquivo_pedido.close()
			
			client.send(arquivo_lido)
			client.send('\r\n')

# Para qualquer comando emitido pelo cliente web diferente do GET,
# o servidor enviará a mensagem BAD REQUEST 
	else:
		client.send(BAD_REQUEST)

# Cada mensagem recebida do cliente web é exibida no console. Não
# há nenhuma razão específica para isso: só para ver o que os na-
# vegadores enviam mesmo
	print msglist

# A lista com cada palavra enviada pelo cliente web é eszaviada
	msglist = []
	
# A conexão TCP é finalizada com o método close()
	client.close()
