import serial, pdb, time, re
import more_itertools
from tkinter import *

print("ready to open")
ser = serial.Serial('COM6')
print("opened")

x_size = 10
y_size = 14

results = []
input = ""

canvas = Canvas(width=500, height=700, bg='white')
canvas.pack(expand=YES, fil=BOTH)
canvas.create_window(1000,1000)
tk = Tk()

def plot_results(results, canvas, tk):
    canvas.delete("all")

    try:
        x_size = len(results)
        y_size = len(results[0])
    except:
        return

    average = average_value(results)
    max_value = max(list(more_itertools.flatten(results)))
    min_value = min(list(more_itertools.flatten(results)))

    for x in range(x_size):
        for y in range(y_size):
            try:
                v = results[x][y] - min_value
            except:
                return
            v = int((v / (max_value-min_value)) * 65535)
            v = "#0000{:04x}0000".format(v)

            x1 = x*50 + 5
            y1 = y*50 + 5
            x2 = x1+40
            y2 = y1+40

            canvas.create_rectangle(x1,y1,x2,y2, width = 2, fill=v)

    tk.update_idletasks()
    tk.update()

def average_value(results):
    return [float(sum(l))/len(l) for l in zip(*results)]

while True:

    try:
        ser_in = ser.read_all() 
        input += ser_in.decode("ascii")
    except:
        continue

    search = re.search("=(.*?)-", input, flags=re.DOTALL)
    if search:
        lines = search.group(0).split("\n")

        for line in lines:
            if ("-" in line or "=" in line or line == ''): continue
            vals = line.split(" ")
            vals = [int(x) for x in vals if x != '']
            results.append(vals)

    if results == []:
        continue
    input = input[search.span()[1]:]
    print("============ IN ")
    print(results)
    plot_results(results, canvas, tk)
    print("============ OUT")
    results = []
    time.sleep(1)

pdb.set_trace()

