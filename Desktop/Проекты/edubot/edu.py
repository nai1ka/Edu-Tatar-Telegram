import requests
import datetime
from datetime import date
import bs4
from flask import Flask
app = Flask(__name__)
dayforcol = 7
import xml.etree.ElementTree as et
from dateutil.relativedelta import relativedelta, MO,WE, TH,TU,SU,FR,SA
now = datetime.datetime.now()
mon = now.month
moth = ""
last_update_id = 0
r = requests.models.Response
ismonth = False
proxies = {
  'http': 'http://194.67.201.106:3128',
  'https': 'http://176.212.127.36:56583',
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
params = {
      'main_login':'4823114196',
      'main_password':'be7l'
   }

#-----------------------------------------------------------------------------------

def auth():
    global r,soup
    with requests.Session() as session:
        session.get("https://edu.tatar.ru/logon",proxies = proxies)
        session.post("https://edu.tatar.ru/logon",params,headers=headers,proxies = proxies)
        r = session.get("https://edu.tatar.ru/user/diary.xml",proxies = proxies)
        return r
    
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
    
    
    global r,dz,urok,och
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
    
    
    
#------------------------------------------------------------------------------------------------


token = "613454940:AAHQ7nZJfQ1GbhYNNUYqE_cCAlUA3sqmaqc"
URL = "https://api.telegram.org/bot"+token+"/"
def get_updates():
    url = URL+ "getupdates"
    r = requests.get(url)
    return r.json()
def get_message():
    data = get_updates()
    last_object = data["result"][-1]
    current_update_id = last_object["update_id"]
    global last_update_id
    if last_update_id!=current_update_id:
        last_update_id = current_update_id
        chat_id = last_object["message"]["chat"]["id"]
        message_text = last_object["message"]["text"]
        message = {
           "chat_id": chat_id,
           "text":message_text
           }
        return message
    return None
def send_message(chat_id,text="",parse_mode=""):
    url = URL + "sendmessage?chat_id={}&text={}&parse_mode={}".format(chat_id,text,parse_mode)
    requests.get(url)
def main():
    global chat_id, projects,islog,message,soup
   
    global y,urok,och,dz,dayforcol
    findday()
    auth()
    
    
    
    @app.route('/')
    def pas():
        return "Hello"  
    
    
    
    while True:
        answer = get_message()
        if answer!= None:
            chat_id = answer["chat_id"]
            text = answer["text"] 
            
            if "/update" in text or "Обновить" in text:
                urok = []
                dz = []
                och = []
                collect(dayforcol)
                send_message(chat_id, "Оценки обновлены. Выберите день недели для получения оценок:"+"\n"+"/monday- понедельник \n /tuesday - вторник \n /wednesday - среда \n /thursday - четверг \n /friday - пятница \n /saturday - суббота")
            
            elif "Понедельник" in text  or "/monday" in text:
                findday()
                dayforcol = monday
                collect(dayforcol)
                i = 0
                send_message(chat_id, "*Понедельник*"+"\n"+"-----------------", parse_mode = "Markdown")
                while i!=7 :
                    send_message(chat_id,"Урок: " +urok[i]+"\n"+"Задание: "+dz[i]+ "\n"+"Оценка: "+ och[i])
                    i+=1
                send_message(chat_id, "-----------------", parse_mode = "Markdown")
            elif "Вторник" in text  or "/tuesday" in text:
                findday()
                dayforcol = tuesday
                collect(dayforcol)
                i = 0
                send_message(chat_id, "*Вторник*"+"\n"+"-----------------", parse_mode = "Markdown")
                while i!=7 :
                    send_message(chat_id,"Урок: " +urok[i]+"\n"+"Задание: "+dz[i]+ "\n"+"Оценка: "+ och[i])
                    i+=1 
                send_message(chat_id, "-----------------", parse_mode = "Markdown")
            elif "Среда" in text  or "/wednesday" in text: #ЭТО
                findday()
                dayforcol = wednesday #ЭТО
                collect(dayforcol)
                i = 0
                send_message(chat_id, "*Среда*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while i!=7 :
                    send_message(chat_id,"Урок: " +urok[i]+"\n"+"Задание: "+dz[i]+ "\n"+"Оценка: "+ och[i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown")
            elif "Четверг" in text  or "/thursday" in text: #ЭТО
                findday()
                dayforcol = thursday #ЭТО
                collect(dayforcol)
                i = 0
                send_message(chat_id, "*Четверг*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while i!=7 :
                    send_message(chat_id,"Урок: " +urok[i]+"\n"+"Задание: "+dz[i]+ "\n"+"Оценка: "+ och[i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown") 
            elif "Пятница" in text  or "/friday" in text: #ЭТО
                findday()
                dayforcol = friday #ЭТО
                collect(dayforcol)
                i = 0
                send_message(chat_id, "*Пятница*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while i!=7 :
                    send_message(chat_id,"Урок: " +urok[i]+"\n"+"Задание: "+dz[i]+ "\n"+"Оценка: "+ och[i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown")
            elif "Суббота" in text  or "/saturday" in text: #ЭТО
                findday()
                dayforcol = saturday #ЭТО
                collect(dayforcol)
                i = 0
                send_message(chat_id, "*Суббота*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                while i!=7 :
                    send_message(chat_id,"Урок: " +urok[i]+"\n"+"Задание: "+dz[i]+ "\n"+"Оценка: "+ och[i])
                    i+=1  
                send_message(chat_id, "-----------------", parse_mode = "Markdown")  
            elif "/help" in text:
                send_message(chat_id,"Выберите день недели для получения оценок:"+"\n"+"/monday- понедельник \n /tuesday - вторник \n /wednesday - среда \n /thursday - четверг \n /friday - пятница \n /saturday - суббота")
            else:
                send_message(chat_id, "К сожалению, у меня нет такой команды. Введите /help для получения списка комманд", )  
        else:
            continue
main()