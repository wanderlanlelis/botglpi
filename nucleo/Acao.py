from nucleo.Log import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Acao:
    def navegadorAbrir(self, endereco):
        try:
            self.driver.get(endereco)
            time.sleep(2)
            Log('Sucesso','Abrir navegador em: '+ endereco)
            return True
        except:
            Log('Erro','Não foi possível acessar o site')
            return False
    def navegadorFechar(self):
        self.driver.close()
    def digitar(self,elemento,texto, log1):
        try:
            WebDriverWait(self.driver, 30 ).until( #mudar para 30
                EC.presence_of_element_located((By.XPATH, elemento))
            )
            self.driver.find_element(By.XPATH,elemento).clear()
            Acao.moverCursor(self,elemento)
            self.driver.find_element(By.XPATH,elemento).send_keys(texto)
            Log('Sucesso',log1)       
            return True       
        except:
            Log('Erro',log1)
            return False
    def clicar(self, elemento, log1, tempoDeEspera = 60):        
        try:
            WebDriverWait(self.driver, tempoDeEspera).until(
                EC.presence_of_element_located((By.XPATH, elemento))
            )
            Acao.moverCursor(self,elemento)
            self.driver.find_element(By.XPATH,elemento).click()
            Log('Sucesso',log1) 
            return True
        except:
            Log('Erro',log1)
            return False 
    def clicarDireito(self, elemento, log1):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, elemento))
            )
            actionChains = ActionChains(self.driver)
            actionChains.context_click(elemento).perform()
            ActionChains.perform()
            Log('Sucesso',log1) 
            return True
        except:
            Log('Erro',log1)
            return False 
    def recuperarValor(self, elemento, tempo, log=True):
        try:
            WebDriverWait(self.driver, tempo).until(
                EC.presence_of_element_located((By.XPATH, elemento))
            )
            resultado =  self.driver.find_element(By.XPATH,elemento).text

            if log:
                Log('Sucesso','Texto encontrado: '+resultado.strip()) 
            return resultado
        except:
            if log:
                Log('Erro','Elemento não encontrado')
            return False 
    def aguardarElemento(self, elemento, tempo):
        Log('Info','Aguardando elemento aparecer') 
        try:
            WebDriverWait(self.driver, tempo).until(
                EC.presence_of_element_located((By.XPATH, elemento))
            )
            Log('Sucesso','Elemento encontrado') 
            return True
        except:
            Log('Erro','Elemento não encontrado')
            return False 
    def aguardarElementoDesaparecer(self, elemento, tempo):
        Log('Info','Aguardando elemento a ser desaparecer')
        try:
            WebDriverWait(self.driver, tempo).until_not(
                EC.presence_of_element_located((By.XPATH, elemento))
            )
            Log('Sucesso','Elemento desapareceu') 
            return True
        except:
            Log('Erro','Elemento não encontrado')
            return False 
    def screenshot(self, elemento,nomeimagem, log1):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, elemento))
            )
            self.driver.find_element(By.XPATH,elemento).screenshot(nomeimagem)
            Log('Sucesso',log1) 
            return True
        except:
            Log('Erro',log1)
            return False 
    def moverCursor(self,elemento):
        hoverable = self.driver.find_element(By.XPATH, elemento)
        ActionChains(self.driver)\
            .move_to_element(hoverable)\
            .perform()