## Creating a Python script to monitor temperature

--- task ---
Open a new Python 3 file by going to **Menu** > **Programming** > **Mu**.
--- /task ---


--- task ---
You can use the GPIO Zero module to find the CPU temperature. First you'll need to import the `CPUTemperature` class:

```python
from gpiozero import CPUTemperature
```

Then you can create a `cpu` object:

```python
cpu = CPUTemperature()
```

--- /task ---

--- task ---
Save and run this program, and then in the shell at the bottom of the Mu window, type `cpu.temperature`.

```python
>>> cpu.temperature
63.783
```
--- /task ---

This is the temperature of the CPU in ℃.
