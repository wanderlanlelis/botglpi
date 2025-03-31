import time
import os
import json
from datetime import datetime

logs = ''
class Log:
    def __init__(self,tipo, mensagem, local=None) -> None:   
        global logs
        log = (time.asctime()+ " | "+tipo+" | "+mensagem+";")
        print(log)
        logs = log+logs
        
        if mensagem.lower() =="fim":
            self.salvarArquivoLog(logs,local)
            time.sleep(5)

    def salvarArquivoLog(self,log, local = "c"):       
        nomeArquivo = local+":\\campello\\log\\"
        nomeArquivo = nomeArquivo+str(datetime.today().strftime('%Y-%m-%d %H:%M:%S').replace('-','').replace(':','').replace(' ','_'))+".txt"
        f = open(nomeArquivo, "a")
        f.write(log.replace(";","\n"))
        f.close()
        Log('info','log de execução gerado com sucesso')