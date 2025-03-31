from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from nucleo.Log import *
from nucleo.Acao import *
import requests
import sys
from shutil import rmtree
import json
from datetime import datetime, timedelta
import getpass
import os

class App():
	def __init__(self, dados) -> None:
		self.glpi_url = 'https://servicedesk.campello.com.br'
		self.logado = False
		self.listadedados = []
		self.parametros = {
			'inserir':['entidade','titulo','descricao'],
			'concluir':['idchamado','descricao', 'tempo'], 
			'adicionaratividade':['idchamado','descricao', 'tempo'], 
			'pesquisar':None
			}

		try:
			for parametro in sys.argv[1:]: self.listadedados.append(parametro)
			if len(self.listadedados)<1: raise
		except: 
			for parametro in dados: self.listadedados.append(parametro)

		listadeajuda = ['help','ajuda','-h','h']
		processosdisponiveis = {'1':'pesquisar','2':'inserir','3':'concluir','4':'adicionaratividade'}
		if self.listadedados[0] in listadeajuda or self.listadedados[2] in listadeajuda: return self.ajuda()
		
		try: 
			processo = processosdisponiveis[self.listadedados[2]]
			self.listadedados[2] = processo
		except: pass

		if not self.verificarParametros(self.listadedados[2]): return None
		Log('info','Iniciando processo: '+ self.listadedados[2])


		processo = "self."+self.listadedados[2]+"()"
		return exec(f"x = {processo}")

	def verificarParametros(self, processo):
		try:
			if processo!='pesquisar' and (len(self.listadedados)-3) != len(self.parametros[processo]):
				Log('erro','quantidade de parametros incorreta')
				Log('info','parametros desejados para essa operação: ' +str(self.parametros[processo]))
				return False
			return True
		except:
			Log('erro','o processo requisitado não existe, digite "ajuda" como parametro para saber mais')
			return False
		
	def ajuda(self):
		print('\n\nLista de comandos:')
		for acao in self.parametros:
			print('\t'+acao+' | parametros: '+ str(self.parametros[acao]))

	def identificarUsuario(self):
		listaUsuarios = {
				'55319999999999':{'usuario':'teste@teste.com.br','senha':'teste'}
				,'5531999999998':{'usuario':'teste1@teste.com.br','senha':'teste'}
			}
	
	def login(self):
		usuario = self.listadedados[0]
		senha   = self.listadedados[1]

		self.iniciarSelenium(headless=True)	
		try:
			Acao.navegadorAbrir(self, self.glpi_url+'/front/ticket.php')
			Acao.digitar(self,'//*[@id="login_name"]',usuario,'digitar usuário: '+usuario)
			Acao.digitar(self, '/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[3]/input',senha,'digitar senha: '+''.join('*' for _ in senha))
			Acao.clicar(self,'/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[6]/button','clicar em login')
		except:
			Log('erro','houve um erro ao realizar login no sistema')
			return False
		return True

	def inserir(self):
		entidade = self.listadedados[3]
		titulo = self.listadedados[4]
		descricao = self.listadedados[5]+'\n[Ticket adicionado via robô: Otto]'

		#print(entidade,titulo,descricao)

		if not self.logado: self.login()
		try:
			Acao.navegadorAbrir(self, self.glpi_url+'/front/ticket.form.php')
			perfilUsuario = Acao.recuperarValor(self,'/html/body/div[2]/header/div/div[2]/div/div[1]/div/a/div/div[1]',5)

			time.sleep(3)
			Acao.clicar(self,'//*[@id="item-main"]/div/div[1]/div/div/span[1]/span[1]/span/span[2]','clicar na seleção de entidade',5)
			time.sleep(1)
			Acao.digitar(self,'/html/body/span/span/span[1]/input',entidade,'digitar entidade')
			time.sleep(2)
			Log('info','pressionar ENTER')
			self.driver.find_element(By.XPATH,'/html/body/span/span/span[1]/input').send_keys(Keys.ENTER)
			time.sleep(5)

			try:
				Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div/div/div/div/form/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/input[2]','clicar no campo de data',5)
				time.sleep(1)
				Acao.clicar(self,'/html/body/div[6]/div[4]/div/button','clicar no botão agora',2)
				time.sleep(1)
				self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/div/div[2]/div/div/div/div/form/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/input[2]').send_keys(Keys.ENTER)
			except:
				pass
		
			# Escolher a categiria
			if perfilUsuario=='Solicitante':
				elemento = '/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[2]/div/div/span[1]/span[1]/span/span[1]'
			else:
				elemento = '/html/body/div[2]/div/div/main/div/div/div[2]/div/div/div/div/form/div[1]/div[2]/div/div[1]/div/div/span/div/div/div/span[1]/span[1]/span/span[2]'
			Acao.clicar(self, elemento,'clicar no menu de seleção',2)
			time.sleep(2)
			Acao.digitar(self,'/html/body/span/span/span[1]/input','robo com falha','digitar caregoria')
			time.sleep(1)
			Log('info','pressionar ENTER')
			self.driver.find_element(By.XPATH,'/html/body/span/span/span[1]/input').send_keys(Keys.ENTER)
			time.sleep(1)


			# Digitar o Titulo
			if perfilUsuario=='Solicitante':
				Acao.digitar(self,'/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[5]/div/input', titulo,'digitar titulo')
				Log('info','pressionar TAB')
				self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[5]/div/input').send_keys(Keys.TAB)
			else:
				Acao.digitar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div/div/div/div/form/div[1]/div[1]/div/div/div/div[2]/span/div/div[2]/div[1]/div/input',titulo,'digitar titulo')
				self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/div/div[2]/div/div/div/div/form/div[1]/div[1]/div/div/div/div[2]/span/div/div[2]/div[1]/div/input').send_keys(Keys.TAB)
			
			
			if perfilUsuario=='Solicitante':
				iframe = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[6]/div/div[1]/div[1]/div[2]/div[1]/iframe")
			else:
				iframe = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/div/div[2]/div/div/div/div/form/div[1]/div[1]/div/div/div/div[2]/span/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/iframe")
			self.driver.switch_to.frame(iframe)
			self.driver.find_element(By.XPATH, '//*[@id="tinymce"]').click()
			Acao.digitar(self,'//*[@id="tinymce"]',descricao,'preencher a descrição')
			self.driver.switch_to.default_content()

			
			# Salvar chamado
			if perfilUsuario=='Solicitante':
				Acao.clicar(self,'/html/body/div[2]/div/div/main/div/form/div/div[4]/button','clciar em enviar mensagem')
			else:
				Log('info','pressionar tecla ENTER')
				self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/div/div[2]/div/div/div/div/form/div[1]/div[1]/div/div/div/div[2]/span/div/div[2]/div[1]/div/input').send_keys(Keys.ENTER)
			
			time.sleep(5)
			url = self.driver.current_url
			numeroChamadoAberto = url[url.find('=')+1:]
			Log('info','[numero do chamado aberto: '+numeroChamadoAberto+']')
			time.sleep(5)
			return '[numero do chamado aberto: '+numeroChamadoAberto+']'
		except:
			Log('erro','não foi possivel registrar o chamado')
			return False

	def pesquisar(self):
		if not self.logado: self.login()
		perfilUsuario = Acao.recuperarValor(self,'/html/body/div[2]/header/div/div[2]/div/div[1]/div/a/div/div[1]',5)
		try:
			if perfilUsuario=='Solicitante': pass
			else:
				Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[1]/div/div/div[3]/span/span[1]/span/span[1]','clicar no menu de seleção')
				Acao.clicar(self, '/html/body/span/span/span[2]/ul/li[5]/ul/li[1]','clicar em atribuido Tecnico')
				Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[1]/div/div/div[4]/div/div[2]/span','clicar em menu de seleção ')
				Acao.clicar(self,'/html/body/span/span/span[2]/ul/li[2]','clicar em "eu" ')
			Acao.clicar(self, '/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[2]/button[1]','clicar em nova regra')
			Acao.clicar(self, '/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[1]/div[2]/div/div[3]/span/span[1]/span','clicar no menu de seleção',5)
			Acao.digitar(self,'/html/body/span/span/span[1]/input','status','digitar a palavra status')
			time.sleep(1)
			Acao.clicar(self, '/html/body/span/span/span[2]/ul/li[2]/ul/li[1]', 'clicar em status',5)

			Acao.clicar(self, '/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[1]/div[2]/div/div[4]/div/div[2]/span/span[1]/span','clicar em menu de seleção')
			Acao.clicar(self, '/html/body/span/span/span[2]/ul/li[7]','clicar em não fechado')	
			Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div[2]/form/div/div/div[2]/button[4]','clicar em pesquisar')
			time.sleep(3)
		except:
			Log('erro','houve um erro ao filtrar os chamados')

		i = 1
		dadosDoChamado = []
		while i!=0:
			if Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[3]',5, False) == False:
				break
			else:
				if perfilUsuario=='Solicitante':
					id = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[1]',2,False) # perfil solicitante
					titulo = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[2]',5, False)
				else:
					id = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[2]',5, False)				
					titulo = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[3]',5, False)
				situacao = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[5]',5, False)
				dataAtualizacao = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[6]',5, False)
				dataAbertura = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[7]',5, False)
				prioridade = Acao.recuperarValor(self,'/html/body/div[2]/div/div/main/div/div[2]/div/form/div/div[2]/table/tbody/tr['+str(i)+']/td[8]',5, False)
				dadosDoChamado.append({'id':id, 'titulo':titulo})
			i = i+1
		return Log('info','resultado: [Nao ha chamados abertos]') if len(dadosDoChamado)==0 else Log('info','resultado: \n'+str(dadosDoChamado))
	
	def adicionaratividade(self):	
		if not self.logado: self.login()

		idchamado = self.listadedados[3]
		descricao = self.listadedados[4]+'\n[Ticket atualizado via robô: Otto]'
		tempo 	  = self.listadedados[5]

		try:
			Acao.navegadorAbrir(self, self.glpi_url+'/front/ticket.form.php?id='+str(idchamado))
			Acao.clicar(self, '/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/button[2]','clicar em responder')
			Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/ul/li[1]/a','clicar em adicionar tarefa')
			
			Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/div/div/div[2]/div/form/div[1]/div[2]/div/div[7]/div/span/span[1]/span/span[1]','clicar em tempo')
			
			Acao.digitar(self,'/html/body/span/span/span[1]/input',tempo,'digitar tempo')
			self.driver.find_element(By.XPATH,'/html/body/span/span/span[1]/input').send_keys(Keys.ENTER)

			Acao.clicar(self,'//*[@id="new-TicketTask-block"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[2]/div/div[4]/div/span/span[1]/span/span[2]','clicar em status da atividade',1)
			Acao.clicar(self,'/html/body/span/span/span[2]/ul/li[3]','clicar em Feito',1)
	
			iframe = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[1]/iframe")
			self.driver.switch_to.frame(iframe)
			self.driver.find_element(By.XPATH, '//*[@id="tinymce"]').click()
			Acao.digitar(self,'//*[@id="tinymce"]',descricao,'preencher a descrição')
			self.driver.switch_to.default_content()



			Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/div/div/div[2]/div/form/div[2]/div/button','clicar em adicionar')
			time.sleep(2)
			Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/span[2]/div/button','clicar em salvar')
			time.sleep(5)
			Log('sucesso','atividade adicionada ao chamado')
			return True
		except:
			Log('erro','não foi possivel adicionar a atividade ao chamado')
			return False

	def concluir(self):
		if not self.logado: self.login()
		try:
			self.adicionaratividade()
			Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/form/div/div[1]/div/div/div[4]/div/span/span[1]/span/span[1]','clicar em status')
			Acao.clicar(self,'/html/body/span/span/span[2]/ul/li[5]','clicar em solucionado')
			time.sleep(2)
			Acao.clicar(self,'/html/body/div[2]/div/div/main/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/span[2]/div/button','clicar em salvar')
			Log('sucesso','Chamado solucionado')
			return '[\nCodigo do chamado: '+self.listadedados[2]+']'
		except:
			Log('erro','Não foi possivel solucionar')
			return False

	def iniciarSelenium(self, proxy=False, headless=False, debuggerAddress=False):
		Log('info','iniciando Selenium')
		from selenium import webdriver
		from selenium.webdriver.chrome.options import Options
		chrome_options = Options()
		
		if headless: 
			#chrome_options.add_argument("--headless")
			chrome_options.add_argument("--headless=new")
		
		if debuggerAddress:
			chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8989")

		chrome_options.add_argument('--blink-settings=imagesEnabled=false')
		chrome_options.add_argument("--start-maximized")
		self.driver = webdriver.Chrome(options=chrome_options)
		#self.driver.set_window_position(-2000,0)
		Log('info','Selenium iniciado com sucesso')

	def ws(self, dados):
		resultado = requests.post('https://central.campello.com.br/emtel/view/ws.php', data=dados).text
		return json.loads(resultado)

try:
	if sys.argv[0]!="ajuda" and len(sys.argv) > 3: dados = sys.argv
	else: raise
except: 
	os.system('cls')
	acao = input("\n\n\nQual ação deseja realizar?\n[0] - ajuda\n[1] - pesquisar\n[2] - inserir\n[3] - concluir\n\n")
	os.system('cls')
	
	dados = []
	# if not acao or acao =='0': dados.append('ajuda')
	if acao and acao !='0': 			
		dados = [input('usuario: '), input('senha: '), acao]
	match(acao):
		case '0': parametros = 'ajuda'
		case '3': parametros = input('codigo do chamado: '), input('descricao: '), input('tempo')
		case '2': parametros = input('empresa: '), input('titulo: '), input('descricao: ')
		case _:  None

	try:
		parametros = list(parametros)
		for iten in parametros: dados.append(iten)
	except: pass
app = App(dados)