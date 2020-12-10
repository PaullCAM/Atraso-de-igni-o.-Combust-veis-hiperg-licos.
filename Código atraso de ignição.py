# -*- coding: utf-8 -*-
"""
Created on Tue May 19 00:05:37 2020

@author: Paull Cristhiann Acosta Mendoza
"""

from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
#import matplotlib.pyplot as plt

#Definicao de funcoes utilizadas no código

def calculaDif(recorte1, recorte2, recorte3): #Definicao da funcao diferença para determinar o contato da gota no solido
    
  d1 = cv2.absdiff(recorte3, recorte2)
  d2 = cv2.absdiff(recorte2, recorte1)
  imagem = cv2.bitwise_and(d1, d2)
  #s,imagem = cv2.threshold(imagem, 135, 255, cv2.THRESH_BINARY) #Filtro de intensidades.
  
  return imagem

#Criando as variaveis de intensidade média
  
Int_mean = []
Int_mean_2 = []


fps = 246 #fps da gravação
Inicio = 15 #Valor de inicio de movimento para cada gravação. 
Corte_he = 600 #Corte horizontal esquerdo
Corte_hd = 850 #Corte horizontal direito
Dif_corteh = Corte_hd - Corte_he #Pixeis na horizontal da imagem apos corte.
Corte_vs = 0 #Corte vertical superior
Corte_vi = 230 #Corte vertical inferior
Dif_cortev = Corte_vi - Corte_vs #Pixeis na vertical da imagem apos corte.

# Ler o arquivo do teste

mypath='teste python, 21' #Importação da gravação realizada
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = np.empty(len(onlyfiles), dtype=object)


#Primeira etapa do código. Procurar de um valor mínimo de Intensidade média para
#cada frame que irá definir o tempo de contato entre reagentes. 

for n in range(Inicio, len(onlyfiles)): #Looping para leitura das imagens 
    #previamente importadas e armazenadas em uma variavel para poder trabalhar posteriormente
    
    images[n] = cv2.imread(join(mypath,onlyfiles[n]))

#Looping para o calculo das diferencas

N = len(onlyfiles)

Min = 100
Crit_2 = 0

for n in range(Inicio, N-2):
    #Recortes para o teste  e aplicacao da funcao diferenca anteriormente 
    #descrita
    img = images[n]
    most = img
    recorte1 = img[Corte_vs:Corte_vi, Corte_he:Corte_hd] #O corte na imagem influencia no grafico
    #e no codigo ja que o conta gotas reflete luz.
       
    img = images[n+1] 
    recorte2 = img[Corte_vs:Corte_vi, Corte_he:Corte_hd]
   
    img = images[n+2] 
    recorte3 = img[Corte_vs:Corte_vi, Corte_he:Corte_hd]
    
    Dif = calculaDif(recorte1, recorte2, recorte3) #Execução da função diferença
    
    Dif_mean = cv2.mean(cv2.mean(Dif))[0] #Cálculo da intensidade média das diferenças
    print ("Dif mean = ",Dif_mean, n)
    
    Int_mean.append(Dif_mean)
    
    if n != Inicio: #Recurso utilizado para avaliar o mínimo local da gravação
        
        Incr = Int_mean[-1] - Int_mean[-2]
    
        if Incr < 0: #Momento onde a derivada da intensidade média se torna negativa
        
            if Min > Dif_mean:
        
                Min = Dif_mean
                cont = 0
        
            else:
        
                cont = cont + 1
        
                if cont == 1 and Crit_2 == 0:
            
                    Crit_2 = Min
        
        
    #cv2.namedWindow("recorte dif", cv2.WINDOW_NORMAL) #Mostra em tela os recortes de diferenca
    
    #cv2.imshow("recorte dif",Dif)
    #cv2.waitKey(0)
    #cv2.namedWindow("Imagens", cv2.WINDOW_NORMAL)
    #cv2.imshow('Imagens', recorte1)
    #cv2.waitKey(0)
    
min_crit_2 = Int_mean.index(Crit_2) + Inicio    
minimo = min_crit_2
#minimo = Int_mean.index(min(Int_mean)) + Inicio #Critério de mínimo global

#if min_crit_2 > minimo: #Recurso de comparação para os critérios de contato entre reagentes

#    minimo = min_crit_2
#print(minimo)

#Segunda etapa do código. Utilizado para definir o tempo da autoignição da mistura.

graf = 0 #Recurso de parada para o critério 1

for n in range(minimo, N):
    
    images[n] = cv2.imread(join(mypath,onlyfiles[n]))

#for i in range(0, len(onlyfiles)):
    
    #cv2.imshow('Imagens', images[i])
    #cv2.waitKey(0)
  
    img = images[n] 
    recorte = img[Corte_vs:Corte_vi, Corte_he:Corte_hd]
    
    Mean = cv2.mean(cv2.mean(recorte))[0]
    
    Int_mean_2.append(Mean) #Calculo da intensidade media para determinar a maxima posteriormente

    for i in range (0,Dif_cortev, 1): #Varredura das imagens para utilizar o critério cor
        
        for j in range (0,Dif_corteh, 1):
            # bgr
            if recorte[i,j][0] < 120 and recorte[i,j][1] >= 235 and recorte[i,j][2] >= 235 and graf==0:#Critério 1
           
                graf = n
                
maximo = Int_mean_2.index(max(Int_mean_2)) + minimo #Intensidade média máxima da gravação considerando o minimo previamente calculado
#maximo = graf #Critério de cor
#if graf > maximo and graf != 0: #Comparação dos critérios.

#   maximo = graf

Delay_time = (maximo - minimo) / fps * 1000


print("Minimo = ", minimo)
print("Maximo = ", maximo)
print("Delay time = ", Delay_time, "ms")



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    