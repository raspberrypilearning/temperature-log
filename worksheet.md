# Temperature Log
n
The system on a chip (SoC) of the Raspberry Pi has a temperature sensor that can be used to measure its temperature from the command line. It can provide information on how much heat the chip has generated during operation and also report on the temperature of the environment. This project's aim is to create a simple script that can run automatically as you boot up your Raspberry Pi, take measurements from the temperature sensor at given intervals, and write them into log files that can be viewed later.

![](images/bcm2835.jpg)

## Finding CPU temperatures with Python

There's a simple terminal command that can be used to find the temperature of the CPU.

### Viewing the temperature

To view the current temperature of your Raspberry Pi, open up a terminal (`ctrl`+`alt`+`t`) and type:

``` bash
`vcgencmd measure_temp`.
```

You should see something like the following output:

``` bash
pi@raspberrypi:~ $ vcgencmd measure_temp
temp=48.3'C
```

### Creating a python script

Any command you use in the teminal can be called from within a python script by using the `os` library.

1. Open up a new Python3 shell by going to `Menu`>`Programming`>`Python 3 (IDLE)`.
1. Now create a new Python script by clicking on `File` > `New File`.
1. If you want to run a shell command using python, the best way to do it is using the `subprocess` module, so your first line should import the `check_output` method from this library.

``` python
from subprocess import check_output
```

1. You can now use `check_output` to run the command you typed into the termial earlier. You type feed in the command as a list, with the 0th item being the command to run, and subsequent items being the arguments passed to the command.

``` python
temp = check_output(["vcgencmd","measure_temp"])
```

1. Save and run the file (`ctrl+s` + `F5`). Then switch over into the python shell and type `temp` to check the variable's value. You should see something that looks like this:

``` python
>>> temp
b"temp=48.3'C\n"
>>> 
```

1. So you can see that the temperature is, in this case, `48.3` celcius. But what's that `b` doing at the start of the string?

1. The `check_output` command returns a datatype called a byte string. This is where each character is represented by a value between 0 and 255 in a large array. To see this as a string, it needs to be decoded. You can decode the `out` variable with an extra line of python.

``` python
temp = temp.decode("UTF-8")
```

1. Now when you query `temp` in the python shell, you should see something like:

``` python
>>> temp
"temp=48.3'C\n"
>>> 
```

### Finding floats with regex
1. Although you now have a string, it would be better to get the actual value out of the string. It's a decimal number, which is called a float in Computer Science. To do this you can use a handy concept called **regular expressions**. Regular expressions, or **regex** look for patterns in strings. In this case we want to find a number, followed by a decimal point, followed by an additional number.

1. First you need to import the `findall` method from the `re` library. Add this line beneath your `subprocess import`

``` python
from re import findall
```

1. You can start by just looking for a number. In regex, the characters `\d` searches for a number.

``` python
temp = findall("\d", temp)
```

1. Querying temp in the shell will now provide something like this:

``` python
>>> temp
['4', '8', '3']
>>> 
```

1. You'll notice that the numbers have been placed in a list. Unfortunately the `4` and the `8` have been split. By adding a `+` to the d, you can search for numbers that are consecutive. Edit the line so it's like this:

``` python
temp = findall("\d+", temp)
```

1. This should give you something like this:

``` python
>>> temp
['48', '3']
>>> 
```

1. The number has still been split around the decimal point though. The line can be edited to include a search for the deimal point though.

``` python
temp = findall("\d+\.", temp)
```

1. Now querying temp in the shell gives this:

``` python
>>> temp
['48.']
>>> 
```

1. So you're missing the number after the decimal place. One more change will give you the actual number.

``` python
temp = findall("\d+\.\d+", temp)
```
1. Now you have:

``` python
>>> temp
['48.3']
>>> 
```
### Getting the actual float.

1. You still have a little problem. You don't actually have the float yet. What you have is something like `['48.3']`, which is actually a string inside a list.

1. As the list has only a single element, you can get the 0th element easily, by adding another line.

``` python
temp = temp[0]
```

1. Then you just need to convert the string to a float.

``` python
temp = float(temp)
```

1. Your entire script should now look like this:

``` python
from subprocess import check_output
from re import findall

temp = check_output(["vcgencmd","measure_temp"])
temp = temp.decode("UTF-8")
temp = findall("\d+\.\d+",temp)
temp = temp[0]
temp = float(temp)
```

1. You could condense this down into fewer lines, if you like:

``` python
from subprocess import check_output
from re import findall

temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
temp = float(findall("\d+\.\d+",temp)[0])
```

1. But you'll definately want to place it all in a function:

``` python
from subprocess import check_output
from re import findall

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)
```

1. So now in the shell you can call the function:

``` python
>>> get_temp()
47.8
>>> 
```

## Writing the data to a CSV file.

Although it's nice that you now have a function to find out the CPU temperature, it would be useful if that data could be stored somewhere. A CSV (comma seperated values) as ideal for this, as it can be used by applications like Excel and Libre Office.

1. You'll want to log the date and time, while getting the CPU temperatures, so you'll some extra libraries for this. Add this to your imports.

``` python
from time import sleep, strftime, time
```

These extra methos let you pause your program (`sleep`), get todays date as a string (`strftime`) and get the exact time in what is known as **UNIX Time** (`time`)


1. To write to a file, you first need to create it. To the end of your file, add the following line:

``` python
with open("cpu_temp.csv", "a") as log:
```

This creates a new file called `cpu_temp.csv` and opens it with the name `log`. It also opens it in *append* mode, so that lines are only written to the end of the file.

1. Now, you'll need to start an infinite loop, that will run until you kill the program (`ctrl`+`c`)

``` python
with open("cpu_temp.csv", "a") as log:
    while True:
```

1. Inside the loop, you can use your `get_temp` function to get the temperature

``` python
with open("cpu_temp.csv", "a") as log:
    while True:
        temp = get_temp()
```

1. Now you want to write both the current data and time, plus the temperature to the csv file.

``` python
with open("cpu_temp.csv", "a") as log:
    while True:
        temp = get_temp()
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))
```

1. That line's a little complicated, so let's break it down a bit:
  - `log.write()` will write what ever string is in the brackets to the csv file.
  - `"{0},{1}\n"` is a string containing two placeholders seperated by a comma, and ending in a newline.
  - `strftime("%Y-%m-%d %H:%M:%S")` is inserted into the first placeholder. It's the current data and time as a string.
  - `str(temp)` is the CPU temperature converted to a string.

1. Lastly you can add a single line to the end of your file to pause the script between writes. Here it's pausing for one second, but you can use any interval that is suitable for you.

``` python
sleep(1)
```

1. The entire script should now look like this:

``` python
from subprocess import check_output
from re import findall
from time import sleep, strftime, time

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

with open("cpu_temp.csv", "a") as log:
    while True:
        temp = get_temp()
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))
        sleep(1)
```

## Live graphing the data

You can produce a graph of CPU temperatures, that will update as it's recorded. For this you'll need the `matplotlib` library. The instructions for installing this are [here]()

1. First of all import the `matplotlib` library where your other imports are.

``` python
import matplotlib.pyplot as plt
```

1. The next three lines can go before you `get_temp()` definition. They'll tell matplotlib that you're intending on doing interactive plotting, and also create the two lists that will hold the data to be plotted.

``` python
plt.ion()
x = []
y = []
```

1. The next lines, are all going into your `while True` loop, before the csv is written, but after the `temp = get_temp()` line. Firstly you add the current temperature to the end of the `y` list, and the time to the end of the `x` list.

``` python
y.append(temp)
x.append(time())
```

1. Then the plot needs to be cleared, and then the points and lines calculated.

``` python
plt.clf()
plt.scatter(x,y)
plt.plot(x,y)
```

1. Lastly the plot can be drawn.

``` python
plt.draw()
```

1. Run your program and you should see the graph being interactivly drawn. Open up some programs such as Minecraft or Mathematica and watch the CPU temperature increase.

## Automating the script

It might be useful to have this script running when the Raspberry Pi starts up. To do this it's best to clean up the script a little, so that you can comment out the lines that draw the graph, with ease. Below is the same script tidied into functions, and with the graph drawing line commented out.

``` python
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
```

1. Automating scripts is simple with `crontab`. Open up a terminal (`ctrl`+`alt`+`t`).
1. Now to edit the crontab you just type:

``` bash
crontab -e
```
1. Scroll to the bottom of the file and add this single line:

``` bash
@reboot python3 /home/pi/temp_monitor.py
```

This assumes you script is called `temp_monitor.py` and is saved in your home directory.

1. Now reboot your Raspberry Pi. Give it a little time to run and then in in a terminal type:

``` bash
cat cpu_temp.csv
```

to see the contents of the csv file.

1. If you want to see a graph, then just uncomment the `graph(temp)` line using IDLE and run the file.

## What next?

- If you want to play around more with matplotlib, you can have a look at the Visualising Sorting with Python lessons, on the Raspberry Pi website.
- Why not have a look at the Getting Started with the Twitter API resource, and have your Raspberry Pi tweet you when the CPU temperature gets too high?

