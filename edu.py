import requests
import datetime
from datetime import date
from flask import Flask
app = Flask(__name__)
dayforcol = 7
login = {}
password = {}
fl = False

d = {'today': [], 'tommorow': [], 'monday':[], 'tuesday':[], 'wednesday':[], 'thursday':[], 'friday':[], 'saturday':[]}
u = {'today': [], 'tommorow': [], 'monday':[], 'tuesday':[], 'wednesday':[], 'thursday':[], 'friday':[], 'saturday':[]}
o = {'today': [], 'tommorow': [], 'monday':[], 'tuesday':[], 'wednesday':[], 'thursday':[], 'friday':[], 'saturday':[]}

import xml.etree.ElementTree as et
from dateutil.relativedelta import relativedelta, MO,WE, TH,TU,SU,FR,SA
now = datetime.datetime.now()
mon = now.month
moth = ""
last_update_id = 0
r = requests.models.Response
ismonth = False
proxies = {
  'http': 'http://85.21.63.48:44063',
  'https': 'http://94.242.58.108:10010',
}
if mon == 1:
    moth = "Январь"
if mon == 2:
    moth = "Феварль"
if mon == 3:
    moth = "Март"
if mon == 4:
    moth = "Апрель"  
if mon == 5:
    moth = "Май"    
if mon == 6:
    moth = "Июнь" 
if mon == 7:
    moth = "Июль"
if mon == 8:
    moth = "Август"
if mon == 9:
    moth = "Сентябрь"  
if mon == 10:
    moth = "Октябрь"     
if mon == 11:
    moth = "Ноябрь"    
if mon == 12:
    moth = "Декабрь"  

urok = []
dz = []
och = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'referer' : 'https://edu.tatar.ru/logon'
    }



#-----------------------------------------------------------------------------------

def auth():
    global r,soup,session


    params = {
          'main_login':login[str(chat_id)],
          'main_password':password[str(chat_id)]
       }  

    session = requests.Session()
    session.get("https://edu.tatar.ru/logon",proxies = proxies)
    session.post("https://edu.tatar.ru/logon",params,headers=headers,proxies = proxies)
    
    return session


#--------------------------------------------------------------------------------------
def findday():
    global monday,tuesday,wednesday,thursday, friday,saturday
    today = date.today()
    monday = (today + relativedelta(weekday=MO(-1))).day 
    tuesday = (today + relativedelta(weekday=TU(-1))).day 
    wednesday = (today + relativedelta(weekday=WE(-1))).day 
    thursday = (today + relativedelta(weekday=TH(-1))).day 
    friday = (today + relativedelta(weekday=FR(-1))).day 
    saturday = (today + relativedelta(weekday=SA(-1))).day 

def collect(dayforcol):
    global session,dz,urok,och
    r = session.get("https://edu.tatar.ru/user/diary.xml",proxies = proxies)
    
    root = et.XML(r.text)
    for elem in root:
        for day1 in elem:
            if(day1.attrib["date"]==str(dayforcol)) and (elem.attrib["month"]==moth):
                for lesson in day1.find("classes"):
                    if lesson.text!=None:
                        
                        urok.append(lesson.text)#УРОК
                    else:
                        urok.append("Нет Урока")
                    
                for task in day1.find("tasks"):
                    
                    if task.text != None and task.text !="  " and task.text !=" " :
                        dz.append(task.text)#Задание   
                    else:
                        dz.append("Нет ДЗ")
                for marks in day1.find("marks"):
                    if marks.text!=None:
                        och.append(marks.text)#Домашка  
                    else:
                        och.append("Нет оценки")
                

def coll1():
    global urok,och,dz,d
    
    collect(now.day)

    
    for i in dz:
        d["today"].append(i)
    
        u["today"].append(i) 
    
    for i in och:
        o["today"].append(i)
    

    dz = []
    urok = []
    och = []
    collect((datetime.date.today()+datetime.timedelta(days=1)).day)
    for i in dz:
        d["tommorow"].append(i)
        
    
    for i in urok:
                u["tommorow"].append(i)  
    
    for i in och:
        o["tommorow"].append(i)                
    
    dz = []
    urok = []
    och = []    
    collect(monday)
    for i in dz:
        d["monday"].append(i)
    
    for i in urok:
        u["monday"].append(i)  
    
    for i in och:
        o["monday"].append(i)                
   
    dz = []
    urok = []
    och = []    
    collect(wednesday)
    for i in dz:
        d["wednesday"].append(i)
    
    for i in urok:
        u["wednesday"].append(i)    
   
    for i in och:
        o["wednesday"].append(i)                
   
    dz = []
    urok = []
    och = []    
    collect(tuesday)
    for i in dz:
        d["tuesday"].append(i)
    for i in urok:
        u["tuesday"].append(i)  
    for i in och:
        o["tuesday"].append(i)  
    
    dz = []
    urok = []
    och = []    
    collect(thursday)
    for i in dz:
        d["thursday"].append(i)
    for i in urok:
        u["thursday"].append(i) 
    for i in och:
        o["thursday"].append(i)            
        
    dz = []
    urok = []
    och = []    
    collect(friday)
    for i in dz:
        d["friday"].append(i)
    for i in urok:
        u["friday"].append(i)    
    for i in och:
        o["friday"].append(i)                
            
    dz = []
    urok = []
    och = []    
    collect(saturday)
    for i in dz:
        d["saturday"].append(i)
    for i in urok:
        u["saturday"].append(i)  
    for i in och:
        o["saturday"].append(i) 
    

token = "665510128:AAHQ7p3p6w1oqj-aDlhkHjRwBw_clZSkaNM"
URL = "https://api.telegram.org/bot"+token+"/"
def get_updates():
    url = URL+ "getupdates"
    r = requests.get(url)
    
    return r.json()
def get_message():
    global login,fl
    data = get_updates()

    if len(data["result"])>0:
        last_object = data["result"][-1]
        current_update_id = last_object["update_id"]
    
    global last_update_id
    if last_update_id!=current_update_id and "text" in last_object["message"]:
        last_update_id = current_update_id
        chat_id = last_object["message"]["chat"]["id"]

        message_text = last_object["message"]["text"]
        message = {
           "chat_id": chat_id,
           "text":message_text
           }


        return message
    fl = True
    return None


def send_message(chat_id,text="",parse_mode=""):
    url = URL + "sendmessage?chat_id={}&text={}&parse_mode={}".format(chat_id,text,parse_mode)
    requests.get(url)
def main():
    global chat_id, projects,islog,message,soup,login
    global y,urok,och,dz,dayforcol
    findday()
    
    
    
    
    @app.route('/')
    def pas():
        return "Hello"  
    while True:
        answer = get_message()
        
        if answer!= None:
            chat_id = answer["chat_id"]
            text = answer["text"] 
            #print(answer)
            if "/update" in text or "Обновить" in text:
                send_message(chat_id, "Загрузка данных. Это может занять некоторое время...")
                coll1()
                send_message(chat_id, "Оценки обновлены. Выберите день недели для получения оценок:"+"\n"+"/monday- понедельник \n /tuesday - вторник \n /wednesday - среда \n /thursday - четверг \n /friday - пятница \n /saturday - суббота")
            
            elif "Понедельник" in text  or "/monday" in text:            
                i = 0
                send_message(chat_id, "*Понедельник*"+"\n"+"-----------------", parse_mode = "Markdown")
                while len(u["monday"])>i:
                    send_message(chat_id,"Урок: " +u["monday"][i]+"\n"+"Задание: "+d["monday"][i]+ "\n"+"Оценка: "+ o["monday"][i])
                    i+=1
                send_message(chat_id, "-----------------", parse_mode = "Markdown")
            elif "Вторник" in text  or "/tuesday" in text:            
                i = 0
                send_message(chat_id, "*Вторник*"+"\n"+"-----------------", parse_mode = "Markdown")
                while len(u["tuesday"])>i:
                    send_message(chat_id,"Урок: " +u["tuesday"][i]+"\n"+"Задание: "+d["tuesday"][i]+ "\n"+"Оценка: "+ o["tuesday"][i])
                    i+=1 
                send_message(chat_id, "-----------------", parse_mode = "Markdown")                           
            elif "Среда" in text  or "/wednesday" in text: #ЭТО             
                i = 0
                send_message(chat_id, "*Среда*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО

                while len(u["wednesday"])>i:
                    send_message(chat_id,"Урок: " +u["wednesday"][i]+"\n"+"Задание: "+d["wednesday"][i]+ "\n"+"Оценка: "+ o["wednesday"][i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown")              
            elif "Четверг" in text  or "/thursday" in text: #ЭТО           
                i = 0
                send_message(chat_id, "*Четверг*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while len(u["thursday"])>i:
                    
                    send_message(chat_id,"Урок: " +u["thursday"][i]+"\n"+"Задание: "+d["thursday"][i]+ "\n"+"Оценка: "+ o["thursday"][i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown")            
            elif "Пятница" in text  or "/friday" in text: #ЭТО               
                i = 0
                send_message(chat_id, "*Пятница*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while len(u["friday"])>i:
                    send_message(chat_id,"Урок: " +u["friday"][i]+"\n"+"Задание: "+d["friday"][i]+ "\n"+"Оценка: "+ o["friday"][i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown")             
            elif "Суббота" in text  or "/saturday" in text: #ЭТО
                i = 0
                send_message(chat_id, "*Суббота*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while len(u["saturday"])>i:
                    send_message(chat_id,"Урок: " +u["saturday"][i]+"\n"+"Задание: "+d["saturday"][i]+ "\n"+"Оценка: "+ o["saturday"][i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown") 
            elif "Завтра" in text or "/tommorow" in text:  
                if (datetime.date.today()+datetime.timedelta(days=1)).isoweekday()!=7:
                    
                    i = 0
                    send_message(chat_id, "*Завтра*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО

                    while len(u["tommorow"])>i:
                        
                        send_message(chat_id,"Урок: " +u["tommorow"][i]+"\n"+"Задание: "+d["tommorow"][i]+ "\n"+"Оценка: "+ o["tommorow"][i])
                        
                        i+=1  
                    send_message(chat_id, "-----------------", parse_mode = "Markdown") 
                else:
                    send_message(chat_id, "Завтра воскресенье!",parse_mode = "Markdown")
            elif "Сегодня" in text or "/today" in text: 
                
                i = 0
                send_message(chat_id, "*Сегодня*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while len(u["today"])>i:
                    send_message(chat_id,"Урок: " +u["today"][i]+"\n"+"Задание: "+d["today"][i]+ "\n"+"Оценка: "+o["today"][i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown") 
            elif "/help" in text:
                send_message(chat_id,"Для обновления журнала используйте /update")
                send_message(chat_id,"Выберите день недели для получения оценок:"+"\n /today - сегодня \n /tommorow - завтра \n /monday - понедельник \n /tuesday - вторник \n /wednesday - среда \n /thursday - четверг \n /friday - пятница \n /saturday - суббота")
            elif "/start" in text :            
                
                send_message(chat_id, "Здравствуйте! Я - бот, созданный Наилем Миннемуллиным. Для подробной информации введите /help")
                send_message(chat_id, "Введите логин от вашего дневника.")
                answer = get_message()
                while answer==None:
                    answer = get_message()

                login.update({str(chat_id):answer["text"]})
                print(login)
                send_message(chat_id, "Введите пароль от дневника")
                answer = get_message()
                while answer==None:
                    answer = get_message()
                password.update({str(chat_id):answer["text"]})
                print(password)
                send_message(chat_id,"Выберите день недели для получения оценок:"+"\n /today - сегодня \n /tommorow - завтра \n /monday - понедельник \n /tuesday - вторник \n /wednesday - среда \n /thursday - четверг \n /friday - пятница \n /saturday - суббота")
                auth()
                coll1()
                
                
                
                
                    
                    


            else:
                send_message(chat_id, "К сожалению, у меня нет такой команды. Введите /help для получения списка комманд", )  
        else:
            continue
while True:
    try:
        main()
    except:
        continue    
