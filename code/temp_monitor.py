from subprocess import check_output
from re import findall
from time import sleep, strftime, time
import matplotlib.pyplot as plt

plt.ion()
x = []
y = []

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

def write_temp(temp):
    with open("cpu_temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))
        
def graph(temp):
    y.append(temp)
    x.append(time())
    plt.clf()
    plt.scatter(x,y)
    plt.plot(x,y)
    plt.draw()    

while True:
    temp = get_temp()
    write_temp(temp)
#    graph(temp)
    sleep(1)

