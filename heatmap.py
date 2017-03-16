import matplotlib.pyplot as plt
import numpy as np

a = np.array( [[0, 299, 279, 0, 0, 0, 0, 3, 0, 0], \
[0, 10, 34,   0, 0, 0, 0, 4, 0, 0], \
[0, 297, 282, 0, 0, 0, 0, 4, 0, 0], \
[0, 354, 363, 0, 0, 0, 0, 5, 0, 0], \
[0, 332, 333, 0, 0, 0, 0, 5, 0, 0], \
[0, 203, 204, 0, 0, 0, 0, 4, 0, 0], \
[0, 31, 19,   0, 0, 0, 0, 3, 0, 0], \
[0, 353, 354, 0, 0, 0, 0, 2, 0, 0], \
[0, 254, 264, 0, 0, 0, 0, 3, 0, 0], \
[0, 247, 242, 0, 0, 0, 0, 2, 0, 0], \
[0, 333, 329, 0, 0, 0, 0, 3, 0, 0], \
[0, 214, 221, 0, 0, 0, 0, 4, 0, 0], \
[0, 122, 114, 0, 0, 0, 0, 4, 0, 0], \
[0, 280, 283, 0, 0, 0, 0, 4, 0, 0]] )

plt.imshow(a, cmap='winter', interpolation='nearest')
plt.ylabel('Time')
plt.xlabel('ADC values per pressure-pixel')
plt.title('Pressure pixel ADC readings over time')
plt.rcParams['axes.facecolor']='white'
plt.show()

