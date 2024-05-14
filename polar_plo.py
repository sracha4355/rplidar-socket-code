import matplotlib.pyplot as plt
import math

ANG_MAX = 45
ANG_MIN = 315
DIST_MAX = 2000
DIST_MIN = 100
limited = True

file_name = "RP.txt"
all_points = []
try:
    with open(file_name, "r") as file:
        for line in file:
            points = line.strip().split(' ')
            points = [float(j) for j in points]
            points.pop(-1)
            all_points.append(points)
except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

min_dist, max_dist = float('inf'), float('-inf')
x, y = [], []
for angle, distance in all_points:
    min_dist = min(min_dist, distance)
    max_dist = max(max_dist, distance)
    if limited:
        if(((angle < ANG_MAX) or (angle > ANG_MIN)) and (DIST_MIN < distance < DIST_MAX) ):
            x.append(math.radians(angle))
            y.append(distance)
    else:
        x.append(math.radians(angle))
        y.append(distance)
print(f'min: {min_dist} max: {max_dist}')

#scaled_data = [(x - min_dist) / (max_dist - min_dist) for x in y]
polar = False

if polar:
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_ylim(0, 1000)
    points = ax.scatter(x, y, marker='o')
else:
    combined = [[x,y] for x,y in zip(x,y)]
    x = [math.cos(i[0]) * i[1] for i in combined]
    y = [math.sin(i[0]) * i[1] for i in combined]
    plt.scatter(x, y)
    #limit
    plt.ylim(-2000, 2000)
    plt.xlim(-2000, 2000)


plt.show()





