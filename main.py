import tkinter as tk
from tkinter import ttk, messagebox
from tkVideoPlayer import TkinterVideo
from threading import Thread
from os import listdir, remove, path, mkdir
from random import shuffle, choice, sample
from datetime import datetime
from imageio import get_writer, imread_v2
from PIL import Image, ImageDraw
import moviepy.editor as mp

# start_time = time.time()
# print("Get 0 time: —- %s seconds —-" % (time.time() - start_time))

def block_widgets(state):
    if(state):
        btn_start["state"] = tk.DISABLED
        btn_stop["state"] = tk.NORMAL
        btn_play_pause["state"] = tk.DISABLED
        checkbox_save_as_mp4["state"] = tk.DISABLED
        entry_size["state"] = tk.DISABLED
        entry_timeout["state"] = tk.DISABLED
        entry_skip_steps["state"] = tk.DISABLED
        entry_frames_per_sec["state"] = tk.DISABLED
        checkbox_use_ROM["state"] = tk.DISABLED
        entry_extra_neighbors_to_be_happy_amount["state"] = tk.DISABLED
        text_box_extra_color_preset["state"] = tk.DISABLED
        entry_extra_pict_size["state"] = tk.DISABLED
    else:
        btn_start["state"] = tk.NORMAL
        btn_stop["state"] = tk.DISABLED
        btn_play_pause["state"] = tk.NORMAL
        checkbox_save_as_mp4["state"] = tk.NORMAL
        entry_size["state"] = tk.NORMAL
        entry_timeout["state"] = tk.NORMAL
        entry_skip_steps["state"] = tk.NORMAL
        entry_frames_per_sec["state"] = tk.NORMAL
        checkbox_use_ROM["state"] = tk.NORMAL
        entry_extra_neighbors_to_be_happy_amount["state"] = tk.NORMAL
        text_box_extra_color_preset["state"] = tk.NORMAL
        entry_extra_pict_size["state"] = tk.NORMAL

def gen_canvas():
    size = pow(input_size, 2)
    value_list = []
    for color in input_extra_color_preset_dict.keys():
        dots_size = int(size * input_extra_color_preset_dict[color])
        for i in range(dots_size):
            value_list.append(color)
    while(len(value_list)<size):
        value_list.append("green")
    shuffle(value_list)
    green_list = [cur_index for cur_index in range(len(value_list)) if value_list[cur_index] == "green"]
    unhappy_set = set()
    for i in range(len(value_list)):
        if(value_list[i]=="green"):
            continue
        if(not check_if_happy(i, value_list)):
            unhappy_set.add(i)
    return value_list, green_list, unhappy_set

def get_neighbors(cell_index):
    if(cell_index == 0): #left bottom corner
        neighbors_list = [cell_index + input_size, cell_index + input_size + 1, cell_index + 1]
    elif(cell_index == input_size*input_size-input_size): #left upper corner
        neighbors_list = [cell_index + 1, cell_index - input_size, cell_index - input_size + 1]
    elif(cell_index == input_size*input_size-1): #right upper corner
        neighbors_list = [cell_index - 1, cell_index - input_size - 1, cell_index - input_size]
    elif(cell_index == input_size - 1): #right bottom corner
        neighbors_list = [cell_index + input_size - 1, cell_index + input_size, cell_index - 1]
    elif(cell_index%input_size == 0): #left wall
        neighbors_list = [cell_index + input_size, cell_index + input_size + 1, cell_index + 1, cell_index - input_size, cell_index - input_size + 1]
    elif((cell_index+1)%input_size == 0): #right wall
        neighbors_list = [cell_index + input_size - 1, cell_index + input_size, cell_index - 1, cell_index - input_size - 1, cell_index - input_size]
    elif(cell_index < input_size): #bottom wall
        neighbors_list = [cell_index + input_size - 1, cell_index + input_size, cell_index + input_size + 1, cell_index - 1, cell_index + 1]
    elif(cell_index > input_size*input_size-input_size): #upper wall
        neighbors_list = [cell_index - 1, cell_index + 1, cell_index - input_size - 1, cell_index - input_size, cell_index - input_size + 1]
    else:
        neighbors_list = [cell_index+input_size-1, cell_index+input_size, cell_index+input_size+1, cell_index-1, cell_index+1, cell_index-input_size-1, cell_index-input_size, cell_index-input_size+1]
    return neighbors_list

def check_if_happy(cell_index, index_list):
    same_color_neighbors = 0
    for temp_index in get_neighbors(cell_index):
        if(index_list[temp_index] == index_list[cell_index]):
            same_color_neighbors +=1
    if(same_color_neighbors >= input_extra_neighbors_to_be_happy_amount):
        return True
    else:
        return False

def shilling_sim(skip_steps, cur_value_list, cur_green_list, cur_unhappy_set):
    progress_bar_task_status["maximum"] = skip_steps
    for i in range(skip_steps):
        cur_empty_cell_index = choice(cur_green_list)
        cur_color_cell_index = int(sample(cur_unhappy_set, 1)[0])
        cur_green_list.remove(cur_empty_cell_index)
        cur_green_list.append(cur_color_cell_index)
        cur_value_list[cur_empty_cell_index] = cur_value_list[cur_color_cell_index]
        cur_value_list[cur_color_cell_index] = "green"
        cells_to_check_list = get_neighbors(cur_color_cell_index)
        cells_to_check_list.extend(get_neighbors(cur_empty_cell_index))
        cells_to_check_list.append(cur_empty_cell_index)
        cur_unhappy_set.remove(cur_color_cell_index)
        for cur_cell_to_check in cells_to_check_list:
            if(cur_value_list[cur_cell_to_check]=="green"):
                continue
            if(check_if_happy(cur_cell_to_check, cur_value_list)):
                cur_unhappy_set.discard(cur_cell_to_check)
            else:
                cur_unhappy_set.add(cur_cell_to_check)
        if(len(cur_unhappy_set)==0):
            set_stop_work()
            break
        progress_bar_task_status["value"] +=1
    progress_bar_task_status.stop()
    return cur_value_list, cur_green_list, cur_unhappy_set

def start_prog():
    global input_size
    global input_frames_per_sec
    global input_time_length
    global input_skip_steps
    global input_extra_neighbors_to_be_happy_amount
    global input_extra_color_preset_dict
    global input_extra_pict_size
    global input_check_save_mp4
    global input_extra_check_use_ROM
    try:
        input_size = int(entry_size.get())
        input_frames_per_sec = int(entry_frames_per_sec.get())
        input_time_length = int(entry_timeout.get())
        input_skip_steps = int(entry_skip_steps.get())
        input_extra_neighbors_to_be_happy_amount = int(entry_extra_neighbors_to_be_happy_amount.get())
        block_widgets(True)
        input_extra_color_preset_dict = {}
        for key_and_value in text_box_extra_color_preset.get(1.0, tk.END).split('\n')[:-1]:
            key = key_and_value.split()[0]
            value = float(key_and_value.split()[1])
            input_extra_color_preset_dict[key] = value
        input_extra_pict_size = int(entry_extra_pict_size.get())
        input_check_save_mp4 = bool(check_save_as_mp4.get())
        input_extra_check_use_ROM = bool(check_use_ROM.get())
    except Exception as e:
        tk.messagebox.showerror(title="Incorrect input!", message="One or more parameters were entered incorrectly.\nCheck that it is correct and try again.")
        return
    progress_bar_status["maximum"] = input_frames_per_sec*input_time_length
    if not path.isdir("temp_results"):
        mkdir("temp_results")
    th = Thread(target=gif_start_gen)
    th.setDaemon(True)
    th.start()

def gif_start_gen():
    global stop_work
    stop_work = False
    total_frame_amount = input_frames_per_sec*input_time_length
    main_value_list, main_green_list, main_unhappy_set = gen_canvas()
    if (not input_extra_check_use_ROM):
        all_frames = []
    for i in range(total_frame_amount):
        image = Image.new(mode="RGBA", size=(input_extra_pict_size, input_extra_pict_size), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle([0, 0, input_extra_pict_size, input_extra_pict_size], fill = (0,0,0))
        if(i!=0):
            main_value_list, main_green_list, main_unhappy_set = shilling_sim(input_skip_steps,main_value_list,main_green_list, main_unhappy_set)
        for cur_pos in range(len(main_value_list)):
            draw.rectangle([cur_pos % input_size * input_extra_pict_size/input_size, int(cur_pos / input_size) * input_extra_pict_size/input_size, (cur_pos % input_size + 1) * input_extra_pict_size/input_size, (int(cur_pos / input_size) + 1) * input_extra_pict_size/input_size], fill=main_value_list[cur_pos])
        progress_bar_status["value"] +=1
        if(not input_extra_check_use_ROM):
            all_frames.append(image)
        else:
            image.save(f"temp_results/pict_{str(i).zfill(8)}.png", "png", save_all=True)
        if (stop_work):
            total_frame_amount = i
            break
    if(not input_extra_check_use_ROM):
        all_frames[0].save('temp_model.gif',format="GIF", save_all=True, append_images=all_frames[1:], optimize=True, loop=0, fps=input_frames_per_sec)
    else:
        with get_writer('temp_model.gif', mode='I', fps=input_frames_per_sec) as writer:
            for frame_number in range(total_frame_amount):
                image = imread_v2(f'temp_results/pict_{str(frame_number).zfill(8)}.png')
                writer.append_data(image)
    gif_load_to_start()
    progress_bar_status.stop()
    if(input_check_save_mp4):
        gif_to_mp4_save()
    clean_dir()
    stop_work = False
    block_widgets(False)

def clean_dir():
    if path.isdir("temp_results"):
        for f in listdir("temp_results/"):
            remove(path.join("temp_results/", f))

def gif_load_to_start():
    videoplayer.load("temp_model.gif")
    videoplayer.place(x=1,y=1, width=500, height=500)

def gif_to_mp4_save():
    clip = mp.VideoFileClip("temp_model.gif")
    time_format = "%H-%M-%S %d.%m.%Y"
    clip.write_videofile(f"Output Model [{datetime.now().strftime(time_format)}].mp4")

def gif_play_pause():
    if videoplayer.is_paused():
        videoplayer.play()
        btn_play_pause["text"] = "Pause"
    else:
        videoplayer.pause()
        btn_play_pause["text"] = "Play"

def gif_ended(event):
    btn_play_pause["text"] = "Play"

def set_stop_work():
    global stop_work
    stop_work = True

def btn_stop_work():
    set_stop_work()
    btn_stop["state"] = tk.DISABLED

def on_closing():
    clean_dir()
    root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Schelling model by raOvOen")
    root.resizable(width=False, height=False)
    window_width = 720
    window_height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

    btn_start = tk.Button(root, text="Start", command=start_prog)
    btn_start.place(x=506, y=3, width=100, height=30)

    btn_stop = tk.Button(root, text="Stop", command=btn_stop_work, state=tk.DISABLED)
    btn_stop.place(x=611, y=3, width=100, height=30)

    check_save_as_mp4 = tk.BooleanVar()
    check_save_as_mp4.set(False)
    checkbox_save_as_mp4 = tk.Checkbutton(root, text="Save as mp4", variable=check_save_as_mp4, offvalue=False, onvalue=True)
    checkbox_save_as_mp4.place(x=610, y=35, width=100, height=30)

    label_main = tk.Label(root, text="[Main options]", justify=tk.LEFT)
    label_main.place(x=505, y=35, height=30)

    label_size = tk.Label(root, text="Size (n amount):", justify=tk.LEFT)
    label_size.place(x=505, y=70, height=30)

    label_video_length = tk.Label(root, text="Video length (sec):", justify=tk.LEFT)
    label_video_length.place(x=505, y=105, height=30)

    label_skip_steps = tk.Label(root, text="Skip (steps):", justify=tk.LEFT)
    label_skip_steps.place(x=505, y=140, height=30)

    label_frames_per_sec = tk.Label(root, text="Frames per sec:", justify=tk.LEFT)
    label_frames_per_sec.place(x=505, y=175, height=30)

    entry_size = tk.Entry(root)
    entry_size.place(x=620, y=70, width=88, height=30)

    entry_timeout = tk.Entry(root)
    entry_timeout.place(x=620, y=105, width=88, height=30)

    entry_skip_steps = tk.Entry(root)
    entry_skip_steps.place(x=620, y=140, width=88, height=30)

    entry_frames_per_sec = tk.Entry(root)
    entry_frames_per_sec.place(x=620, y=175, width=88, height=30)

    label_extra = tk.Label(root, text="[Extra options]", justify=tk.LEFT)
    label_extra.place(x=505, y=225, height=30)

    label_extra_neighbors_to_be_happy_amount = tk.Label(root, text="Neighbors amount:", justify=tk.LEFT)
    label_extra_neighbors_to_be_happy_amount.place(x=505, y=260, height=30)

    label_extra_pict_size = tk.Label(root, text="Picture size (dpi):", justify=tk.LEFT)
    label_extra_pict_size.place(x=505, y=295, height=30)

    label_extra_color_preset = tk.Label(root, text="Color preset:", justify=tk.LEFT)
    label_extra_color_preset.place(x=505, y=325, height=30)

    entry_extra_neighbors_to_be_happy_amount = tk.Entry(root)
    entry_extra_neighbors_to_be_happy_amount.insert(tk.END,5)
    entry_extra_neighbors_to_be_happy_amount.place(x=620, y=260, width=88, height=30)

    entry_extra_pict_size = tk.Entry(root)
    entry_extra_pict_size.insert(tk.END, 500)
    entry_extra_pict_size.place(x=620, y=295, width=88, height=30)

    text_box_extra_color_preset = tk.Text(root, state='normal', height=11, width=25)
    text_box_extra_color_preset.insert(tk.END,"red 0.45\nblue 0.45")
    text_box_extra_color_preset.place(x=505, y=360)

    check_use_ROM = tk.BooleanVar()
    check_use_ROM.set(True) 
    checkbox_use_ROM = tk.Checkbutton(root, text="Use ROM", variable=check_use_ROM, offvalue=False, onvalue=True)
    checkbox_use_ROM.place(x=610, y=225, width=100, height=30)

    videoplayer = TkinterVideo(master=root, scaled=True)
    videoplayer.bind("<<Ended>>", gif_ended)

    btn_play_pause = tk.Button(root, text="Play", command=gif_play_pause, state=tk.DISABLED)
    btn_play_pause.place(x=200, y=510, width=100, height=30)

    progress_bar_status = ttk.Progressbar(root, orient="horizontal", mode="determinate", value=0)
    progress_bar_status.place(x=10, y=511, width=180, height=30)

    progress_bar_task_status = ttk.Progressbar(root, orient="horizontal", mode="determinate", value=0)
    progress_bar_task_status.place(x=310, y=511, width=180, height=30)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()