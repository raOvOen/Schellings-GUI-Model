import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from tkVideoPlayer import TkinterVideo
from matplotlib import pyplot as plt
import random
from celluloid import Camera

def gen_canvas():
    size = pow(int(entry_size.get()),2)
    dots_size = int(size * 0.45)
    value_list = [0 for i in range(size)]
    for i in range(dots_size):
        value_list[i] = 1
        value_list[dots_size+i] = 2
    random.shuffle(value_list)
    return value_list

def shilling_sim(skip_steps, cur_value_list):
    #for i in skip_steps:
    random.shuffle(cur_value_list)
    return cur_value_list

def start_prog():
    gif_start_gen()

def gif_start_gen():
    value_list = gen_canvas()
    fig = plt.figure(figsize=(5, 5), dpi=100)
    camera = Camera(fig)
    for i in range(int(entry_frames_per_sec.get())*int(entry_timeout.get())):
        value_list = shilling_sim(int(entry_skip_steps.get()),value_list)
        for j in range(len(value_list)):
            if value_list[j] == 2:
                cur_color = "red"
            elif value_list[j] == 1:
                cur_color = "blue"
            else:
                cur_color = "green"
            plt.plot(j%int(entry_size.get())+1, int(j/int(entry_size.get()))+1, color=cur_color, marker="s", markersize=100)
        camera.snap()
    animation = camera.animate()
    animation.save('temp_model.gif', writer='pillow', fps=int(entry_frames_per_sec.get()))

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Schelling model by IvanovA.G.")
    root.resizable(width=False, height=False)
    window_width = 1000
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    btn_start = tk.Button(root)
    btn_start["text"] = "Start"
    btn_start.place(x=501, y=0, width=100, height=30)
    btn_start["command"] = start_prog

    label_size = tk.Label(root)
    label_size["text"] = "Size (n amount): "
    label_size["justify"]=tk.LEFT
    label_size.place(x=501, y=70, height=30)

    label_video_length = tk.Label(root)
    label_video_length["text"] = "Video length (sec): "
    label_video_length["justify"]=tk.LEFT
    label_video_length.place(x=501, y=105, height=30)

    label_skip_steps = tk.Label(root)
    label_skip_steps["text"] = "Skip (steps): "
    label_skip_steps["justify"]=tk.LEFT
    label_skip_steps.place(x=501, y=140, height=30)

    label_frames_per_sec = tk.Label(root)
    label_frames_per_sec["text"] = "Frames per sec: "
    label_frames_per_sec["justify"]=tk.LEFT
    label_frames_per_sec.place(x=501, y=175, height=30)

    entry_size = tk.Entry(root)
    entry_size.place(x=600, y=70, width=100, height=30)

    entry_timeout = tk.Entry(root)
    entry_timeout.place(x=600, y=105, width=100, height=30)

    entry_skip_steps = tk.Entry(root)
    entry_skip_steps.place(x=600, y=140, width=100, height=30)

    entry_frames_per_sec = tk.Entry(root)
    entry_frames_per_sec.place(x=600, y=175, width=100, height=30)

    # videoplayer = TkinterVideo(master=root, scaled=True)
    # videoplayer.load("temp_model.gif")
    # #videoplayer.load("VID-20221006-WA0001.mp4")
    # videoplayer.place(x=1,y=1, width=500, height=500)
    # videoplayer.play()  # play the video

    root.mainloop()