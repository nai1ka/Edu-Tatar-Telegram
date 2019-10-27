import requests
import traceback
import datetime
from datetime import date
from flask import Flask
import xml.etree.ElementTree as et
from dateutil.relativedelta import relativedelta, MO,WE, TH,TU,SU,FR,SA
app = Flask(__name__)

login = {}
password = {}

token = "974890667:AAGwif71apXIv31QcCXlM88DMlaDLmlg0nY"
URL = "https://api.telegram.org/bot"+token+"/"
now = datetime.datetime.now()
today = date.today()
monday = (today + relativedelta(weekday=MO(-1))).day 
tuesday = (today + relativedelta(weekday=TU(-1))).day 
wednesday = (today + relativedelta(weekday=WE(-1))).day 
thursday = (today + relativedelta(weekday=TH(-1))).day 
friday = (today + relativedelta(weekday=FR(-1))).day 
saturday = (today + relativedelta(weekday=SA(-1))).day

last_update_id=0

now = datetime.datetime.now()
mon = now.month
moth = ""
last_update_id = 0
r = requests.models.Response
ismonth = False
user_login={}
user_password={}
proxies = {
  'https': 'https://91.208.39.70:8080'
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

def auth(login,password,user_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
        'referer' : 'https://edu.tatar.ru/logon'
        }  
    proxy=requests.get("https://api.getproxylist.com/proxy?allowsHttps=1&protocol[]=http&country[]=RU&maxConnectTime=1&lastTested=600").json()
       
    #proxies = {
         #'https': 'https://'+proxy["ip"]+":"+str(proxy["port"])
         #'https': 'https://193.124.205.57:3128'
         #TODO настроить прокси
    #}    
    proxies={
        'https':'socks4://217.168.76.230:33032'
    
    }

    
    print(login[user_id]["login"])
    params = {
          'main_login':str(login[user_id]["login"]),
          'main_password':str(password[user_id]["password"])
       }  
    session = requests.Session()
    session.post("https://edu.tatar.ru/logon",params,headers=headers,proxies=proxies)
    
    return session


#--------------------------------------------------------------------------------------

def collect(login,passwd,user_id,dayforcol):
    r = auth(login,passwd,user_id).get("https://edu.tatar.ru/user/diary.xml")
    #print(r.text)
    if(r.text!="Restricted IP"):
        data = dict.fromkeys(['Lesson', 'Homework', 'Mark'])
        finish_lesson = []
        homework = []
        mark = []     
        root = et.XML(r.text)
        for elem in root:
            for day1 in elem:
                if(day1.attrib["date"]==str(dayforcol)) and (elem.attrib["month"]==moth):
                    for lesson in day1.find("classes"):
                        if lesson.text!=None:
                            
                            finish_lesson.append(lesson.text)#УРОК
                        else:
                            finish_lesson.append("None")
                        
                    for task in day1.find("tasks"):
                        
                        if task.text != None and task.text !="  " and task.text !=" " :
                            homework.append(task.text)#Задание   
                        else:
                            homework.append("Нет ДЗ")
                    for marks in day1.find("marks"):
                        if marks.text!=None:
                            mark.append(marks.text)#Домашка  
                        else:
                            mark.append("Нет оценки")
        data["Lesson"]=finish_lesson
        data["Homewrok"]=homework
        data["Mark"]=mark
        return data
                



def get_updates():
    url = URL+ "getupdates"
    r = requests.get(url)
    
    return r.json()
def get_message():
    global last_update_id
    current_update_id=0
    data = get_updates()
    if len(data["result"])>0:
        last_object = data["result"][-1]
        current_update_id = last_object["update_id"]
    if last_update_id!=current_update_id and "text" in last_object["message"]:
        last_update_id = current_update_id
        chat_id = last_object["message"]["chat"]["id"]

        message_text = last_object["message"]["text"]
        message = {
           "chat_id": chat_id,
           "text":message_text
           }


        return message


def send_message(chat_id,text="",parse_mode=""):
    url = URL + "sendmessage?chat_id={}&text={}&parse_mode={}".format(chat_id,text,parse_mode)
    requests.get(url)
def main():

    input_login=False
    input_passwd=False    
    while True:
        answer = get_message()
        
        if answer!= None:
            chat_id = answer["chat_id"]
            text = answer["text"] 
            if "/start" in text :            
                send_message(chat_id, "Здравствуйте! Я - бот, созданный Наилем Миннемуллиным. Для подробной информации введите /help")
                send_message(chat_id, "Введите логин от вашего дневника.")
                input_login=True
            elif len(text)==10 and input_login==True:
                user_login[chat_id]={"login":text}
                input_login=False
                send_message(chat_id, "Введите Ваш пароль от EduTatar")
                input_passwd=True
            elif input_passwd==True:
                user_password[chat_id]={"password":text}
                send_message(chat_id, "Авторизация прошла успешно. Введите день для получения оценок.")
                input_passwd=False           
            elif "Понедельник" in text  or "/monday" in text:            
                data=collect(user_login,user_password,chat_id,monday)
                send_message(chat_id, "*Понедельник*"+"\n"+"-----------------", parse_mode = "Markdown")
                for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                send_message(chat_id, "-----------------", parse_mode = "Markdown")
            elif "Вторник" in text  or "/tuesday" in text:            
                data=collect(user_login,user_password,chat_id,tuesday)
                send_message(chat_id, "*Вторник*"+"\n"+"-----------------", parse_mode = "Markdown")
                for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                send_message(chat_id, "-----------------", parse_mode = "Markdown")                           
            elif "Среда" in text  or "/wednesday" in text: #ЭТО             
                data=collect(user_login,user_password,chat_id,wednesday)
                send_message(chat_id, "*Среда*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО

                for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                send_message(chat_id, "-----------------", parse_mode = "Markdown")              
            elif "Четверг" in text  or "/thursday" in text: #ЭТО           
                data=collect(user_login,user_password,chat_id,thursday)
                send_message(chat_id, "*Четверг*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                send_message(chat_id, "-----------------", parse_mode = "Markdown")            
            elif "Пятница" in text  or "/friday" in text: #ЭТО               
                data=collect(user_login,user_password,chat_id,friday)
                send_message(chat_id, "*Пятница*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                send_message(chat_id, "-----------------", parse_mode = "Markdown")             
            elif "Суббота" in text  or "/saturday" in text: #ЭТО
                data=collect(user_login,user_password,chat_id,saturday)
                send_message(chat_id, "*Суббота*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])       
                send_message(chat_id, "-----------------", parse_mode = "Markdown") 
            elif "Завтра" in text or "/tommorow" in text:  
                if (datetime.date.today()+datetime.timedelta(days=1)).isoweekday()!=7:
                    data=collect(user_login,user_password,chat_id,(datetime.date.today()+datetime.timedelta(days=1)).day)

                    send_message(chat_id, "*Завтра*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО

                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                    send_message(chat_id, "-----------------", parse_mode = "Markdown") 
                else:
                    send_message(chat_id, "Завтра воскресенье!",parse_mode = "Markdown")
            elif "Сегодня" in text or "/today" in text: 
                data=collect(user_login,user_password,chat_id,(datetime.date.today()).day)
                send_message(chat_id, "*Сегодня*"+"\n"+"-----------------", parse_mode = "Markdown")#ЭТО
                for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            send_message(chat_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                send_message(chat_id, "-----------------", parse_mode = "Markdown") 
            elif "/help" in text:
                send_message(chat_id,"Для обновления журнала используйте /update")
                send_message(chat_id,"Выберите день недели для получения оценок:"+"\n /today - сегодня \n /tommorow - завтра \n /monday - понедельник \n /tuesday - вторник \n /wednesday - среда \n /thursday - четверг \n /friday - пятница \n /saturday - суббота")
            
 
            else:
                send_message(chat_id, "К сожалению, у меня нет такой команды. Введите /help для получения списка комманд", )  
        else:
            continue
main()
