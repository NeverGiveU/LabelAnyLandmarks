# -*- coding: utf-8 -*-
"""Description
    @Author  : Chopin
    @Time    : 2020/01/09
    @Comment : A tool for landmark annotation.
"""

#### import packages
import tkinter as tk
from tkinter import Menu, filedialog, NW , Entry
import os
import PIL
from PIL import ImageTk
from PIL import Image
import shutil
import json
import numpy as np


#### json parser
def new_json(json_pth):
    pass

def read_json(json_pth):
    pass

def update_json(json_pth, item):
    pass


#### predefine
window = tk.Tk()
#window.iconbitmap("icon.ico")
window.title('Scanme')
window.title("Landmarker")
window.geometry("{}x{}".format(512+256+64, 512+256+64))
window.configure(background='DimGray')
window.resizable(height=False, width=False)


## global variables
window.src_pth = ''
window.des_pth = ''
window.json_fh = None
window.postfixes = ['png', 'jpg', 'jpeg', 'JPEG', 'PNG', 'JPG', 'bmp', 'webp']
window.length  = 0
window.max_count_landmarks = 5
window.count_landmarks = 0
window.cur_landmark_index = 0
window.dft_img_size = 512+256#512
#window.tag_names = ["left_eye", "right_eye", "nose", "left_mouth", "right_mouth"]
window.color = "#00ff00"
#window.colors = ["#ff0000", "#daa520", "#2f4f4f", "#228b22", "#b22222"]
#window.colors_dict = {"left_eye":"#ff0000", "right_eye":"#daa520", "nose":"#2f4f4f", "left_mouth":"#228b22", "right_mouth":"#b22222"}
#window.cur_tag_name = ""
#window.cur_tag_id = -1
window.imgs_list = []
window.cur_img = None
window.raw_img = None
window.count = 0
# img size
window.h = []
window.w = []
window.rh = []
window.rw = []
window.ratio = []
# img landmarks
window.landmarks = {}
window.file_name = ''
window.alert_flag= False
# state
window.state = 0
'''
    0 --for (de)noting landmarks
    1 --select regions
'''
window.rectangle = []
window.second_affine = [0, 0, False]
window.subject_count = 0


#### functions
def _quit():
    window.quit()
    window.destroy()
    exit()

def _reset():
    window.src_pth = ''
    # window.des_pth = ''
    window.length = 0
    window.json_fh = None
    window.cur_tag_name = ""
    window.cur_tag_id = -1
    window.imgs_list = []
    window.cur_img = None
    window.raw_img = None
    window.count = 0
    # img size
    window.h = []
    window.w = []
    window.rh = []
    window.rw = []
    window.ratio = []
    # img landmarks
    window.landmarks = {}
    window.subject_count = 0


def _src_dir():
    _reset()
    window.src_pth = filedialog.askdirectory()

    # get image paths as lists
    for root, dirs, files in os.walk(window.src_pth):
        for f in files:
            postfix = f.split('.')[-1]
            if postfix in window.postfixes:
                f_name = os.path.join(root, f)
                window.imgs_list.append(f_name)

    window.length = len(window.imgs_list)

    # get the first one and show it
    if window.length > 0:
        pth = window.imgs_list[0]
        # print(window.imgs_list)
        # get file name
        window.file_name = os.path.basename(pth).split('.')[0]
        window.raw_img = window.cur_img = Image.open(pth).convert('RGB')
        # print(window.file_name)
        # print(window.cur_img)
        w, h = window.cur_img.size
        '''
        if w < window.dft_img_size and h < window.dft_img_size:
            window.ratio = 0
            window.h = 0
            window.w = 0
            window.rh = h 
            window.rw = w 
            pass
        else:
        '''
        if True:
            size = max(w, h)
            window.rh.append(h) 
            window.rw.append(w)
            ratio = window.dft_img_size / size 
            h = int(h * ratio)
            w = int(w * ratio)
            window.cur_img = window.cur_img.resize((w, h))
            window.h.append(h)
            window.w.append(w) 
            window.ratio.append(ratio)

        window.cur_img = ImageTk.PhotoImage(window.cur_img)

        img_win.delete("all")
        img_win.create_image(window.dft_img_size//2, window.dft_img_size//2, anchor='center',image=window.cur_img)


def _des_dir():
    window.des_pth = filedialog.askdirectory()
    open_json()

def _debug():
    pass

def local2global(x, y):
    if window.ratio[-1] <= 0:
        x_ = - window.dft_img_size // 2 + window.rw[-1] // 2 + x 
        y_ = - window.dft_img_size // 2 + window.rh[-1] // 2 + y 
    else:
        x_ = - window.dft_img_size // 2 + window.w[-1] // 2 + x 
        y_ = - window.dft_img_size // 2 + window.h[-1] // 2 + y 
        x_ /= window.ratio[-1]
        y_ /= window.ratio[-1]
    dx, dy, rr = window.second_affine 
    x_ = x_+dx 
    y_ = y_+dy 
    return x_, y_

     
def annote(event):
    if window.length > 0 and window.state == 0:
        window.alert_flag = True
        # get coordinates
        # print(event.x, event.y)
        
        try:
            [x_, y_] = window.landmarks[str(window.cur_landmark_index+1)]
            img_win.delete(img_win.landmarks[str(window.cur_landmark_index+1)])
        except:
            pass


        x = event.x
        y = event.y
        # project back to the original image
        """
        if window.ratio[-1] <= 0:
            x_ = - window.dft_img_size // 2 + window.rw[-1] // 2 + x 
            y_ = - window.dft_img_size // 2 + window.rh[-1] // 2 + y 
        else:
            x_ = - window.dft_img_size // 2 + window.w[-1] // 2 + x 
            y_ = - window.dft_img_size // 2 + window.h[-1] // 2 + y 
            x_ /= window.ratio[-1]
            y_ /= window.ratio[-1]
        """
        x_, y_ = local2global(x, y)
        # draw points
        name = str(window.cur_landmark_index+1)
        img_win.landmarks[name] = img_win.create_oval(x-3, y-3, x+3, y+3, fill='#00{}00'.format(get_color(window.cur_landmark_index)), outline="white")
        img_win.notes[name] = img_win.create_text(x-4, y-4, text=name)
        window.landmarks[str(window.cur_landmark_index+1)] = [x_, y_]

        window.cur_landmark_index = min(len(window.landmarks), window.max_count_landmarks-1)
        window.count_landmarks = len(window.landmarks)




def global2local(x, y):
    dx, dy, rr = window.second_affine 
    x -= dx 
    y -= dy 
    if window.ratio[-1] <= 0:
        x = x + window.dft_img_size // 2 - window.rw[-1] // 2
        y = y + window.dft_img_size // 2 - window.rh[-1] // 2
    else:
        x = x * window.ratio[-1] + window.dft_img_size // 2 - window.w[-1] // 2
        y = y * window.ratio[-1] + window.dft_img_size // 2 - window.h[-1] // 2
    return x, y
    

def de_annote(event):
    if window.length > 0 and window.state == 0:
        # _debug(info="你按下了鼠标右键")
        window.alert_flag = True

        x = event.x
        y = event.y
        # project back to the original image
        """
        if window.ratio[-1] <= 0:
            x_ = - window.dft_img_size // 2 + window.rw[-1] // 2 + x 
            y_ = - window.dft_img_size // 2 + window.rh[-1] // 2 + y 
        else:
            x_ = - window.dft_img_size // 2 + window.w[-1] // 2 + x 
            y_ = - window.dft_img_size // 2 + window.h[-1] // 2 + y 
            x_ /= window.ratio[-1]
            y_ /= window.ratio[-1]
        """
        x_, y_ = local2global(x, y)

        distances = [0] * window.count_landmarks
        for landmark in window.landmarks:
            # if landmark == "SIZE":
            #     continue
            x, y = window.landmarks[landmark]
            distances[int(landmark)-1] = int((x_-x)**2+(y-y_)**2)
        # print(window.landmarks)
        index = np.argmin(np.array(distances))
        #print(distances)
        window.cur_landmark_index = index
        img_win.delete(img_win.landmarks[str(window.cur_landmark_index+1)])
        #img_win.delete(img_win.notes[str(window.cur_landmark_index+1)])


def empty():
    window.json_fh = None
    #window.cur_tag_name = ""
    #window.cur_tag_id = -1
    #window.cur_img = None
    # img size
    window.h = []
    window.w = []
    window.rh = []
    window.rw = []
    window.ratio = []
    window.alert_flag = False
    window.rectangle = []
    window.second_affine = [0., 0., False]
    # img landmarks
    window.landmarks = {}

    window.count_landmarks = 0
    window.cur_landmark_index = 0
    window.subject_count = 0

    """
    btn0['fg'] = window.colors[0]
    btn0['bg'] = 'white'
    btn1['fg'] = window.colors[1]
    btn1['bg'] = 'white'
    btn2['fg'] = window.colors[2]
    btn2['bg'] = 'white'
    btn3['fg'] = window.colors[3]
    btn3['bg'] = 'white'
    btn4['fg'] = window.colors[4]
    btn4['bg'] = 'white'
    """


def draw_landmarks():
    # if already exists, display it
    for name in window.landmarks:
        if name == 'SIZE' or name == 'IMAGE':
            continue

        x, y = window.landmarks[name]
        '''
        if window.ratio[-1] <= 0:
            x = x + window.dft_img_size // 2 - window.rw[-1] // 2
            y = y + window.dft_img_size // 2 - window.rh[-1] // 2
        else:
            x = x * window.ratio[-1] + window.dft_img_size // 2 - window.w[-1] // 2
            y = y * window.ratio[-1] + window.dft_img_size // 2 - window.h[-1] // 2
        '''
        x, y = global2local(x, y)
        x, y = int(x), int(y)
        img_win.landmarks[name] = img_win.create_oval(x-3, y-3, x+3, y+3, fill='#00{}00'.format(get_color(int(name)-1)), outline="white")#window.color)
        img_win.notes[name] = img_win.create_text(x-4, y-4, text=name)



def open_json():
    pth = os.path.join(window.des_pth, window.file_name+'-{}.txt'.format(window.subject_count))
    if os.path.exists(pth) is not True:
        pass
    else:
        # read and initialize
        fh = open(pth, 'r', encoding='utf-8')
        line = fh.readline()
        fh.close()
        window.landmarks = json.loads(line)

        if 'SIZE' in window.landmarks:
            del window.landmarks['SIZE']
        if "IMAGE" in window.landmarks:
            del window.landmarks["IMAGE"]
        
        window.count_landmarks = len(window.landmarks)# point to next
        window.cur_landmark_index = min(len(window.landmarks), window.max_count_landmarks-1)
        # print(window.landmarks, window.count_landmarks, window.cur_landmark_index)
        draw_landmarks()
        """
        # if already exists, display it
        for name in window.landmarks:
            #print(name, type(name))
            if name == 'SIZE' or name == 'IMAGE':
                continue

            x, y = window.landmarks[name]
            
            if window.ratio[-1] <= 0:
                x = x + window.dft_img_size // 2 - window.rw[-1] // 2
                y = y + window.dft_img_size // 2 - window.rh[-1] // 2
            else:
                x = x * window.ratio[-1] + window.dft_img_size // 2 - window.w[-1] // 2
                y = y * window.ratio[-1] + window.dft_img_size // 2 - window.h[-1] // 2

            x, y = int(x), int(y)
            img_win.landmarks[name] = img_win.create_oval(x-3, y-3, x+3, y+3, fill='#00{}00'.format(get_color(int(name)-1)), outline="white")#window.color)
            img_win.notes[name] = img_win.create_text(x-4, y-4, text=name)
        """

def get_color(d):
    #print(d)
    d = int(d*255/window.max_count_landmarks)
    s = hex(d)[2:]
    if len(s) == 1:
        s = '0'+s 
    return s


def write_json():
    '''
    landmarks_tmp = {}
    for k in window.landmarks:
        if window.landmarks[k][0] < 0 or window.landmarks[k][1] < 0:
            continue
        else:
            landmarks_tmp[k] = window.landmarks[k]
    '''
    if window.alert_flag:
        window.landmarks["SIZE"] = [window.rh[0], window.rw[0]]
        window.landmarks["IMAGE"] = window.file_name
        json_str = json.dumps(window.landmarks)
        fh = open(os.path.join(window.des_pth, window.file_name) + '-{}.txt'.format(window.subject_count), 'w', encoding='utf-8')
        fh.write(json_str)
        fh.close()
        # print("Successfully Save!")


def show_process():
    p = int(window.count/window.length*80)
    print("Process: |"+">"*p+" "*(80-p)+"| {:.2f}%".format(window.count/window.length*100))


def prev(event):
    if window.state > 0:
        return 
    if window.second_affine[2]:
        go_to_previous_state()
        return  
    write_json()
    empty()
    if window.length == 0:
        return 0
    window.count -= 1
    show_process()
    idx = window.count % window.length
    pth = window.imgs_list[idx]
    # get file name
    window.file_name = os.path.basename(pth).split('.')[0]
    window.raw_img = window.cur_img = Image.open(pth)

    w, h = window.cur_img.size
    '''
    if w < window.dft_img_size and h < window.dft_img_size:
        window.ratio = 0
        window.h = 0
        window.w = 0
        window.rh = h 
        window.rw = w 
        pass
    else:
    '''
    if True:
        size = max(w, h)
        window.rh = [h] 
        window.rw = [w] 
        ratio = window.dft_img_size / size 
        h = int(h * ratio)
        w = int(w * ratio)
        window.cur_img = window.cur_img.resize((w, h))
        window.h = [h]
        window.w = [w] 
        window.ratio = [ratio]
    window.cur_img = ImageTk.PhotoImage(window.cur_img)
    img_win.delete("all")
    img_win.create_image(window.dft_img_size//2, window.dft_img_size//2, anchor='center',image=window.cur_img)
    
    open_json()
    

def next(event):
    if window.state > 0:
        return 
    write_json()
    empty()
    if window.length == 0:
        return 0
    window.count += 1
    show_process()
    idx = window.count % window.length
    # print('%.3f' % (window.count / window.length))
    pth = window.imgs_list[idx]
    # print(pth)
    # get file name
    window.file_name = os.path.basename(pth).split('.')[0]
    # open_json()
    window.raw_img = window.cur_img = Image.open(pth)

    w, h = window.cur_img.size
    '''
    if w < window.dft_img_size and h < window.dft_img_size:
        window.ratio = 0
        window.h = 0
        window.w = 0
        window.rh = h 
        window.rw = w 
        pass
    else:
    '''
    if True:
        size = max(w, h)
        window.rh = [h] 
        window.rw = [w] 
        ratio = window.dft_img_size / size 
        h = int(h * ratio)
        w = int(w * ratio)
        window.cur_img = window.cur_img.resize((w, h))
        window.h = [h]
        window.w = [w] 
        window.ratio = [ratio]
    window.cur_img = ImageTk.PhotoImage(window.cur_img)
    img_win.delete("all")
    img_win.create_image(window.dft_img_size//2, window.dft_img_size//2, anchor='center',image=window.cur_img)

    open_json()


# click space
def state_switch_to_1(event):
    if window.second_affine[2] == False:
        window.state = 1


def click_down_to_draw_rectangle(event):
    if window.state != 1 or window.second_affine[2]:
        return 
    x = event.x 
    y = event.y 
    window.rectangle = [(x,y), (0,0)]


def drag_to_draw_rectangle(event):
    if window.state != 1:
        return 
    x1, y1 = window.rectangle[0]
    x2, y2 = event.x, event.y 
    window.rectangle[1] = (x2, y2)
    try:
        img_win.delete(img_win.rectangle["region"])
    except:
        pass 
    img_win.rectangle["region"] = img_win.create_rectangle(x1, y1, x2, y2, outline="cyan", width=2, dash=True)


def click_down_to_finish_rectangle(event):
    if window.state != 1:
        return 
    # print("We finish drawing.")
    # get th clip
    # 1. Project to image style
    x1, y1 = window.rectangle[0]
    x2, y2 = window.rectangle[1]

    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    x1, y1 = local2global(x1, y1)
    x2, y2 = local2global(x2, y2)

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(window.rw[-1]-1, x2)
    y2 = min(window.rh[-1]-1, y2)

    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    # 2. Crop
    window.cur_img = window.raw_img.crop((x1, y1, x2, y2))

    # 3. Project
    window.second_affine[0] = x1
    window.second_affine[1] = y1 # offset
    w_, h_ = x2-x1+1, y2-y1+1
    window.rh.append(h_)
    window.rw.append(w_)
    s_ = max(w_, h_)
    r = window.dft_img_size / s_ 
    window.second_affine[2] = True
    w_ = w_*r 
    h_ = h_*r
    window.h.append(h_)
    window.w.append(w_)
    window.ratio.append(r)
    window.cur_img = window.cur_img.resize((int(w_), int(h_)))

    window.cur_img = ImageTk.PhotoImage(window.cur_img)
    img_win.delete("all")
    img_win.create_image(window.dft_img_size//2, window.dft_img_size//2, anchor='center',image=window.cur_img)
    draw_landmarks()

    window.state = 0


def click_mouse_left(event):
    if window.state == 0:
        annote(event)
    elif window.state == 1:
        click_down_to_draw_rectangle(event)


def go_to_previous_state():
    window.h.pop()
    window.w.pop()
    window.rh.pop()
    window.rw.pop()
    window.ratio.pop()
    window.cur_img = window.raw_img.resize((int(window.w[0]), int(window.h[0])))
    window.cur_img = ImageTk.PhotoImage(window.cur_img)
    img_win.delete("all")
    img_win.create_image(window.dft_img_size//2, window.dft_img_size//2, anchor='center',image=window.cur_img)
    window.second_affine = [0., 0., False]
    draw_landmarks()
    pass


def update_subject():
    if window.second_affine[2]:
        window.h.pop()
        window.w.pop()
        window.rh.pop()
        window.rw.pop()
        window.ratio.pop()
    window.cur_img = window.raw_img.resize((int(window.w[0]), int(window.h[0])))
    window.cur_img = ImageTk.PhotoImage(window.cur_img)
    img_win.delete("all")
    img_win.create_image(window.dft_img_size//2, window.dft_img_size//2, anchor='center',image=window.cur_img)
    window.second_affine = [0., 0., False]
    # window.count -= 1
    # next(None)
    window.alert_flag = False
    window.rectangle = []
    window.second_affine = [0., 0., False]
    window.landmarks = {}
    window.count_landmarks = 0
    window.cur_landmark_index = 0

    open_json()


def up(eent):
    write_json()
    # print("Up")
    window.subject_count -= 1
    window.subject_count = max(0, window.subject_count)
    update_subject()


def down(event):
    write_json()
    # print("Down", window.subject_count)
    txt_pth = os.path.join(window.des_pth, window.file_name+'-{}.txt'.format(window.subject_count))
    if os.path.exists(txt_pth) is True:
        window.subject_count += 1
    update_subject()


#### details
## menu bar
menubar = Menu(window)
window.config(menu=menubar)
# item 1: file
file_item = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_item)
# option 1: open dir
file_item.add_command(label='打开文件夹', command=_src_dir)

# option 2: save dir
file_item.add_separator()
file_item.add_command(label='打开保存文件夹', command=_des_dir)

# option 3: exit
# file_item.add_separator()
# file_item.add_command(label='退出', command=_quit)
# option 4: debug
# file_item.add_separator()
# file_item.add_command(label='Debug', command=_debug)

## img_window
img_win = tk.Canvas(window, height=window.dft_img_size, width=window.dft_img_size)
img_win.bind("<Button-1>", click_mouse_left)
img_win.bind("<Button-3>", de_annote)
#img_win.bind("<Button-1>", click_down_to_draw_rectangle)
img_win.bind("<B1-Motion>", drag_to_draw_rectangle)
img_win.bind("<ButtonRelease-1>", click_down_to_finish_rectangle)
img_win.name = "Image"
img_win.place(x=32, y=32, anchor=NW)
img_win.landmarks = {}
img_win.notes = {}
img_win.rectangle = {}

## keyboard
window.bind('<KeyPress-Left>', prev)
window.bind('<KeyPress-Right>', next)
window.bind('<KeyPress-Up>', up)
window.bind('<KeyPress-Down>', down)
window.bind('<space>', state_switch_to_1)

## select tag
"""
count = 0
btn0 = tk.Button(window, text=window.tag_names[count], fg=window.colors[count], command=select_tag_0, width=30, bd=0)
btn0.place(x=window.dft_img_size+32+32, y=32+count*32, anchor=NW)
count = 1
btn1 = tk.Button(window, text=window.tag_names[count], fg=window.colors[count], command=select_tag_1, width=30, bd=0)
btn1.place(x=window.dft_img_size+32+32, y=32+count*32, anchor=NW)
count = 2
btn2 = tk.Button(window, text=window.tag_names[count], fg=window.colors[count], command=select_tag_2, width=30, bd=0)
btn2.place(x=window.dft_img_size+32+32, y=32+count*32, anchor=NW)
count = 3
btn3 = tk.Button(window, text=window.tag_names[count], fg=window.colors[count], command=select_tag_3, width=30, bd=0)
btn3.place(x=window.dft_img_size+32+32, y=32+count*32, anchor=NW)
count = 4
btn4 = tk.Button(window, text=window.tag_names[count], fg=window.colors[count], command=select_tag_4, width=30, bd=0)
btn4.place(x=window.dft_img_size+32+32, y=32+count*32, anchor=NW)
"""

#### loop
window.mainloop()
