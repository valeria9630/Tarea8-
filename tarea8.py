import threading
import time
import random
import json



def leerJson(ruta):
    with open(ruta) as contenido:
        objeto = json.load(contenido)
        return objeto
        
     
      


"""
ARGS & VARS
"""
ruta ="C:\\Users\\valeria\\Documents\\Programacion2\\preguntas.json"

objeto = leerJson(ruta)
print(objeto)
for o in objeto:
         laps= o.get("laps")
         delay = o.get("delay")
         sleepTime = o.get("sleeptime")


threads = []
waitLocks= {}
ranking=[]
rankLock=threading.Condition();

for lock in range(laps):
    waitLocks[lock]=threading.Condition()


"""
TURTLE
"""
def turtle(laps,delay):
    for counter in range(laps):
        print( threading.currentThread().getName()+"["+str(counter)+"]")
        time.sleep(delay);
        waitLocks[counter].acquire()
        waitLocks[counter].notifyAll()
        waitLocks[counter].release()
    rankLock.acquire()
    ranking.append(threading.currentThread().getName())
    rankLock.release()
    return
"""
HARE
"""
def hare(laps,sleepTime):
    slept=0
    for counter in range(laps):
        print (threading.currentThread().getName()+"["+str(counter)+"]")
        randomDice=random.randint(1, 100)
        if slept == 0 and randomDice > 80 :
            print (threading.currentThread().getName()+"[zzzZZZZ]")
            waitLocks[counter].acquire()
            sleepQuality=waitLocks[counter].wait(sleepTime)
            waitLocks[counter].release()
            slept=1

            if not sleepQuality :
                hareStatus="woken Up"
            else:
                hareStatus="God morning sunshine"
            print (threading.currentThread().getName()+"["+hareStatus+"]")
    rankLock.acquire()
    ranking.append(threading.currentThread().getName())
    rankLock.release()
    return

"""
MAIN LOOPS
"""

ruta ="C:\\Users\\valeria\\Documents\\Programacion2\\preguntas.json"
objeto =leerJson(ruta)
for o in objeto:
    hares = o.get("hares")
    turtles = o.get("turtles")


for i in range(turtles):
    turtleName="turtle"+str(i)
    t = threading.Thread(name=turtleName,target=turtle,args=(laps,delay))
    threads.append(t)
    t.start()

for i in range(hares):
    hareName="hare"+str(i)
    t = threading.Thread(name=hareName,target=hare,args=(laps,sleepTime))
    threads.append(t)
    t.start()

"""Polling"""
for animalThread in threads :
    animalThread.join()

counter=0
print  ("RANKING")
for animal in ranking:
    print ("#",counter,animal)
    counter+=1
    




