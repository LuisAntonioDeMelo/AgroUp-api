import json
class Patologia :
    
    def __init__ (self,nome,nome_cientifico,classificador,
                  descricao,sintomas,acuracia,gravidade):
        self.nome = nome
        self.nome_cientifico = nome_cientifico
        self.classificador = classificador
        self.descricao = descricao
        self.sintomas = sintomas
        self.acuracia = acuracia
        #gravidades tera o peso entre 0.1 a 0.5 
        self.gravidade = gravidade
        

#algoritmo para calcular o risco de infecção ira calcular 
# a gravidade de 1 a 5 * pelo resultado da acuracia 
    def risco_de_infeccioso(self):
        return  (self.acuracia * 100)* self.gravidade
    
#regra para risco
    def risco_geral(self):
        value = self.risco_de_infeccioso
        if value >= 4:
            return "Grau Alto de Infecção"
        if value >= 2 and value < 4:
            return "Grau Médio de Infecção" 
        if value < 2:
            return "Grau Baixo de Infecção"
        
#resultado em texto
    def acuracidade(self):
        valor =  self.acuracia*100 #normalizar
        if valor >= 9:
            return "Excelente!"
        elif valor >= 7 and  valor < 9:
            return "Bom!"
        elif valor >= 5 and valor < 7:
            return "Regular!"
        else :
            return "Indefinido! e inválido"
        pass
    