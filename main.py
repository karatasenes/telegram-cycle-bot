import json, os, glob, threading, random, time, uuid, datetime
from session_coverter import SessionMaker
from tgSendMessage import tgSendMessage
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    app_id = config["app_id"]
    app_hash = config["app_hash"]
    admin_session = config["admin_session"]
    sessionsFolder = config["sessionsFolder"]
    messagesFile = config["messagesFile"]
    messageReplyMin = config["messageReplyMin"]
    messageReplyMax = config["messageReplyMax"]
    dialogMesajAraligi = config["dialogMesajAraligi"]
    multiThread = config["multiThread"]
    waitForNext = config["waitForNext"]
    convertMode = config["convertMode"]
    threadCount = config["threadCount"]
    sameNumberTime = config["sameNumberTime"]
    sameMessageTime = config["sameMessageTime"]
    threadTimeRange = config["threadTimeRange"]
with open(messagesFile, 'r', encoding='utf-8') as k:
    messages = json.load(k)["messages"]
if convertMode:
    while True:
        print("You can write 'ok' for exit.")
        number = input("Input the number for generate session: ")
        if number=="ok":
            print("You can view the created sessions in session folder.")
            break
        SessionMaker(number=number).start()
    exit()

system = {}
system["status"] = "active"
def sistemAktif():
    system["status"] = "active"
    print("System is active!")
def sistemPasif():
    system["status"] = "passive"
    print("System is passive!")


def baslat(acilis,kapanis,status,gelen):
    if acilis.find("24") != -1:
        acilis = acilis.replace("24","00")
    if kapanis.find("24") != -1:
        kapanis = kapanis.replace("24","00")
    c = time.strftime("%H:%M:%S").split(":")
    d = acilis.split(":")
    e = kapanis.split(":")
    f = datetime.timedelta(hours=int(d[0]),minutes=int(d[1]),seconds=int(d[2])) - datetime.timedelta(hours=int(c[0]),minutes=int(c[1]),seconds=int(c[2]))
    g = datetime.timedelta(hours=int(e[0]),minutes=int(e[1]),seconds=int(e[2])) - datetime.timedelta(hours=int(c[0]),minutes=int(c[1]),seconds=int(c[2]))
    if str(f.total_seconds()).find("-") != -1:
        h = 86400.0 + f.total_seconds()
    else:
        h = f.total_seconds()
    if str(g.total_seconds()).find("-") != -1:
        i = 86400.0 + g.total_seconds()
    else:
        i = g.total_seconds()
    threading.Timer(h,sistemAktif).start()
    threading.Timer(i,sistemPasif).start()
    if status == gelen:
        threading.Timer(i,acil).start()
def acil():
    with open('config.json',encoding="utf-8") as f:
        dat = json.load(f)
        if len(dat['saatler']) > 0:
            status = len(dat['saatler'])
            b = 1
            for i in dat['saatler']:
                acilis = str(dat['saatler'][i]['acilis']) + ":00:00"
                kapanis = str(dat['saatler'][i]['kapanis']) + ":00:00"
                baslat(acilis,kapanis,status,b)
                b += 1
acil()
#Hata modları
if len(admin_session) == 0:
    print("Admin session does not exists.")
    exit()

admins = []
sessions = glob.glob("sessions/*.session")
sessions = [x.split("\\")[-1] for x in sessions]
print(sessions)
for i in admin_session:
    if i in sessions:
        admins.append(i)
if len(admins) == 0:
    print("Cant find any admin session or not active.")
    exit()

if os.path.exists(messagesFile) == False:
    print("Message file does not exists.")
    exit()

#Hata modları

print(f"""
Starting..
####################
Session count: {len(sessions) - len(admins)}
Multithread Mode: {'Active' if multiThread else 'Passive'}
Message File: {messagesFile}
Min Reply (Seconds): {messageReplyMin}
Max Reply (Seconds): {messageReplyMax}
####################
{"Multithread mode is active, if you wanna single mode you can turn off the multithread.." if multiThread else ''}
""")



#Multithread
infoMulti = {}
dupSessions = sessions
reg = 0
for k in dupSessions:
    if k in admins:
       del dupSessions[reg]
    reg+=1 
selectedMessages = {}
def selectMessageOver(message):
    if message in selectedMessages:
        del selectedMessages[message]
def selectNumberOver(dup):
    dupSessions.append(dup)
def messageSender(app_id, app_hash, session, message, channel, uid):
    t1 = tgSendMessage(app_id=app_id, app_hash=app_hash, session=session, message=message, channel=channel, uid=uid)
    t1.send()
stop = False
def multiThreadProcess(thread_name):
    while  not stop:
        wait = True
        if system["status"] == "passive":
            continue
        if len(dupSessions) > 0:
            uid = str(uuid.uuid4())
            rnd = random.randint(0, len(dupSessions) - 1)
            infoMulti[dupSessions[rnd]] = dupSessions[rnd].replace(".session", "")
            dup2 = dupSessions[rnd]
            session_now = dupSessions[rnd].replace(".session", "")
            del dupSessions[rnd]
            selectMessage = random.choice(messages)
            adminSes = random.choice(admins).replace('.session', '')
            messageChannel = selectMessage["channel_id"]
            messageRound = random.choice(selectMessage["messages"])["messages"]
            firstMessage = messageRound[0]["message"]
            if firstMessage in selectedMessages:
                print("wait process..")
                wait = False
                continue
            selectedMessages[firstMessage] = "created"
            threading.Timer(sameMessageTime, function=selectMessageOver, args=(firstMessage,)).start()
            threading.Timer(sameNumberTime, function=selectNumberOver, args=(dup2,)).start()
            for i in messageRound:     
                messageMain = i["message"]
                messageReply = i["reply"]
                messageSender(app_id, app_hash, f"{sessionsFolder}/{session_now}", messageMain, messageChannel, uid)
                time.sleep(random.randint(messageReplyMin, messageReplyMax))
                messageSender(app_id=app_id, app_hash=app_hash, session=f"{sessionsFolder}/{adminSes}", message=messageReply, channel=messageChannel, uid=uid)
                time.sleep(random.randint(dialogMesajAraligi[0], dialogMesajAraligi[1]))
        if wait:
            time.sleep(waitForNext)


        
if multiThread:
    thread_name = "tgSes-"
    thread_start = 0
    while thread_start <= threadCount:
        threading.Thread(name=thread_name + str(thread_start), target=multiThreadProcess, args=(thread_name + str(thread_start),)).start()
        time.sleep(random.randint(threadTimeRange[0], threadTimeRange[1]))
        thread_start+=1

#Singlethread       
else:
    thread_name = "Single"
    threading.Thread(name=thread_name, target=multiThreadProcess, args=(thread_name,)).start()