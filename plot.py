import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import time


data = [[1,1], [2,3], [4,4]]
def setup_plot():
    fig, ax = plt.subplots()
    points = ax.scatter([], [], marker='o', s=1)
    return fig, ax, points

# Function to update the plot
def update(frame, points, ax):
    print(f'FRAME {frame}')
    time.sleep(2)
    x_coords = [0 + (20 * frame)]
    y_coords = [360 + (frame * 0.01)]
    ax.set_xlim(0,360)
    ax.set_ylim(0, max(y_coords) + 200)
    points.set_offsets(np.column_stack([x_coords, y_coords]))
    return points

def clear_plot(fig, ax):
    print(f'Clearing Plot')
    ax.cla()
    fig.canvas.draw()  # Optional: Explicitly redraw the figure after clearing

# Define an update function for your real-time data
def plot():
    fig, ax, points = setup_plot()
    ani = animation.FuncAnimation(fig, update, frames=None, fargs=(points, ax), blit=True, interval=200)
    plt.show()



