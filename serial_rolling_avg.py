import serial, pdb, time
import matplotlib.pyplot as plt

print("ready to open")
ser = serial.Serial('COM5')

samples = []
window = 4
graph_window = 200

ave_graph = []
curr_graph = []
del_graph = []
plt.ion()
plt.figure(1)

while True:
    line = ser.read_all().decode("ascii").split("\r\n")
    if len(line) > 1:
        try:
            current = int(line[1])
        except:
            continue
        samples.append((current))
        if len(samples) > window:
            samples.pop(0)

        total = sum(samples)
        ave = total/window
        delta = ave - current

        curr_graph.append(current)
        ave_graph.append(ave)
        del_graph.append(delta)

        if len(curr_graph) > graph_window:
            curr_graph.pop(0)
            ave_graph.pop(0)
            del_graph.pop(0)
        y_axis = range(0,len(ave_graph))

        print("curr: %d, ave: %d, delta: %d" % (current,ave, delta))

        plt.clf()
        plt.subplot(211)
        plt.title('Rolling average and current value')
        plt.plot(y_axis, curr_graph, 'r', y_axis, ave_graph,'b')

        plt.subplot(212)
        plt.title('Delta between average and current')
        plt.plot(y_axis, del_graph, 'b')
        plt.pause(0.05)

    time.sleep(0.5)

