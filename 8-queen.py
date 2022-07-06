# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 21:45:37 2022

@author: diren
"""
import random
import time
import pandas as pd


def Yeme_hesapla(tahta): #Tahtaya yerleştirilen vezirlerin birbirlerini
                         #yeme sayısını hesaplayan fonksiyon
    yeme = 0 
    
    for i in range(len(tahta)):
        for j in range(i+1,len(tahta)):
            if(abs(tahta[i]-tahta[j])==abs(i-j) or tahta[j]==tahta[i]):
                yeme = yeme + 1
    return (yeme)

def Tüm_hareketlerde_yeme_hesapla(tahta,index): #İndexi verilen vezirin yerini değiştirince 
                                                #oluşan tüm hareketlerdeki 
                                                #yeme sayısını hesaplayan fonksiyon
    
    yemeler=[]
    temp=tahta.copy()
    
    for i in range(8):
        temp[index] = i
        yemeler.append(Yeme_hesapla(temp))
            
    return yemeler 
  
def En_iyi_komşuyu_hesapla(tahta,index): #Komşu sütunlardaki vezirlerin yer değişimine göre
                                         #en küçük yeme sayılarını hesaplayan fonksiyon
                                         
    en_iyi_komşular = []
    for i in range(8):
        
        en_küçük = min(Tüm_hareketlerde_yeme_hesapla(tahta,i))
        en_iyi_komşular.append(en_küçük)
    
    en_iyi_komşular[index] = 50  #Bu indexteki değeri çok büyük yaptım çünkü 
    return en_iyi_komşular         #algoritmada kendi sütununda arama yapmamalı

    
def Hill_Climb():       #Hill_climb metodu
    
    start_time = time.time()  #Çalışma zamanını başlangıcı
    tahta = []  

    for i in range(8):
        tahta.append(random.randint(0,7))  #tahta dizisine random vezir konumları ataması
        
    toplam_yeme = Yeme_hesapla(tahta)
    
    sütun = random.randint(0,7) #vezirin yeri değiştirilecek ilk indexi random atadım
    random_restart = 0
    eski_toplam_yeme = 0
    yer_değiştirme = 0
    while(toplam_yeme > 0):  #local minimum 0 olana kadar döngüye girecek
        
        
        ana_yemeler = Tüm_hareketlerde_yeme_hesapla(tahta, sütun)
        ana_yemeler_minimum = min(ana_yemeler)
        ana_yemeler_minimum_index = ana_yemeler.index(ana_yemeler_minimum) #tahtanın olası hamleler sonucu
                                                                        #en küçük yeme sayısını ve bu hamlenin olduğu 
                                                                        #indexi tutum
                                                                        
        
        en_küçük_komşu_yemeler = En_iyi_komşuyu_hesapla(tahta, sütun)       #aynı şekilde komşu durumlar için tutuldu
        en_küçük_komşu_yemeler_minimum = min(en_küçük_komşu_yemeler)
        en_küçük_komşu_yemeler_minimum_index = en_küçük_komşu_yemeler.index(en_küçük_komşu_yemeler_minimum)
        
        if(en_küçük_komşu_yemeler_minimum < ana_yemeler_minimum): #komşudaki değişim daha iyiyse o yola gidildi
            komşu_yemeler = Tüm_hareketlerde_yeme_hesapla(tahta,en_küçük_komşu_yemeler_minimum_index)
            komşu_yemeler_minimum = min(komşu_yemeler)
            komşu_yemeler_minimum_index = komşu_yemeler.index(komşu_yemeler_minimum)
            
            sütun = en_küçük_komşu_yemeler_minimum_index
            tahta[sütun] = komşu_yemeler_minimum_index
        
        else: #değilse aynı sütunda değişiklik yaparak devam edildi
            tahta[sütun] = ana_yemeler_minimum_index
      
        
        toplam_yeme = Yeme_hesapla(tahta)
        
        if(toplam_yeme ==eski_toplam_yeme):     #eğer eski durum güncellenemiyorsa local minimuma takıldı demektir
                                                #o yüzden random restart atıldı
            tahta.clear()
            for i in range(8):
                tahta.append(random.randint(0,7))
            
            random_restart +=1
            
        
        else:
            eski_toplam_yeme = Yeme_hesapla(tahta) #değilse güncellendi
            
        yer_değiştirme +=1

    
    Random_restart_sayısı.append(random_restart)
    Yer_değiştirme_sayısı.append(yer_değiştirme)
    İşlem_süresi.append(time.time() - start_time)
    
Random_restart_sayısı = []    
Yer_değiştirme_sayısı = []
İşlem_süresi =[]
    
         
for i in range(15): #15 kez hill climb çağırıldı
    Hill_Climb()   
    
    
print(Random_restart_sayısı)
print(Yer_değiştirme_sayısı)
print(İşlem_süresi)

df = pd.DataFrame({'Random Restart': Random_restart_sayısı, #tablo için pandas dataframe kullandım
        'Yer Değiştirme': Yer_değiştirme_sayısı,
        'İşlem Süresi': İşlem_süresi})
df.loc['ortalama'] = df.mean(numeric_only=True, axis=0)

df
 
