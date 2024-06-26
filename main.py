#Остановился на уроке 18
from tkinter import *
from tkinter import messagebox
import time
import random
 
tk = Tk()
app_running = True

size_canvas_x = 500
size_canvas_y = 500
s_x = s_y = 8  # размер игрового поля
s_y = 8
step_x = size_canvas_x // s_x  # шаг по горизонтали
step_y = size_canvas_y // s_y  # шаг по вертикали
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
delta_menu_x = 4  # размер на форме отведенный для меню
menu_x = step_x * delta_menu_x #250
menu_y = 40 # для надписи какой игрок снизу
ships = s_x // 2  # определяем максимальное кол-во кораблей
ship_len1 = s_x // 5  # длина первого типа корабля
ship_len2 = s_x // 3  # длина второго типа корабля
ship_len3 = s_x // 2  # длина третьего типа корабля
enemy_ships1 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)] # список кораблей для 1 игрока
enemy_ships2 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)] # список кораблей для 2 игрока
list_ids = []  # список объектов canvas
points1 = [[-1 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули для 1 игрока
points2 = [[-1 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули для 2 игрока
boom = [[0 for i in range(s_x)] for i in range(s_y)] #  это список попаданий по кораблям противника
ships_list = []#список кораблей игрока 1 и 2
hod_igrovoe_pole_1 = False # ход игрока 1 если true и 2 если false
computer_vs_human = True # переменная опр. против кого играем!  если True-против компа, false - человека
if computer_vs_human:
    add_to_label = " (Компьютер) "
    add_to_label2 = " (Думает,или прицеливается) "
    hod_igrovoe_pole_1 = False
else:
    add_to_label = ""
    add_to_label2 = ""
    hod_igrovoe_pole_1 = False

# print(enemy_ships1)



def on_closing():
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
        app_running = False
        tk.destroy()



tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Игра Морской Бой")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x+size_canvas_x, size_canvas_y, fill="lightyellow")
canvas.pack()
tk.update()



def draw_table(offset_x=0):
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x+step_x * i, 0, offset_x+step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, step_y * i, offset_x+size_canvas_x, step_y * i)



draw_table()
draw_table(size_canvas_x+ menu_x)

#вывод надписей "Игрок 1" и "Игрок 2"
t0 = Label(tk, text="Игрок 1", font=("helvetica", 16))
t0.place(x = size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y= size_canvas_y + 3)
t1 = Label(tk, text="Игрок 2"+ add_to_label, font=("helvetica", 16))
t1.place(x = size_canvas_x + menu_x + size_canvas_x// 2 - t1.winfo_reqwidth() // 2, y= size_canvas_y + 3)


#выделение цветом активного игрока
t0.configure(bg='red') # выделение красным цветом
t0.configure(bg='#f0f0f0') # выделение фоновым цветом окна

# надпись чей ход
t3 = Label(tk, text="*****", font=("helvetica", 16))
t3.place(x = size_canvas_x + menu_x//2 - t3.winfo_reqwidth() // 2, y = size_canvas_y)


def change_rb():
    global computer_vs_human, add_to_label, add_to_label2
    print(rb_var.get())
    if rb_var.get():
        computer_vs_human = True
        add_to_label = " (Компьютер) "
        add_to_label2 = " (Думает,или прицеливается) "
    else:
        computer_vs_human = False
        add_to_label = ""
        add_to_label2 = ""




rb_var = BooleanVar()
rb1 = Radiobutton(tk, text="Чечик vs Комп", variable=rb_var, value=1, command=change_rb)
rb2 = Radiobutton(tk, text="Чечик vs Чечик", variable=rb_var, value=0, command=change_rb)
rb1.place(x=size_canvas_x+20, y = 140)
rb2.place(x=size_canvas_x+20, y = 160)
if computer_vs_human:
    rb1.select()


def mark_igrok(igrok_mark_1):
    if igrok_mark_1:
        t0.configure(bg='red')
        t0.configure(text='ход игрока № 1'+ add_to_label2) 
        t0.place(x = size_canvas_x//2 - t0.winfo_reqwidth() // 2, y = size_canvas_y+3) 
        t1.configure(bg='#f0f0f0') 
        t1.configure(text='ход игрока № 2'+ add_to_label) 
        t1.place(x = size_canvas_x + menu_x + size_canvas_x// 2 - t1.winfo_reqwidth() // 2, y= size_canvas_y + 3)
        t3.configure(text='ход игрока № 2'+ add_to_label)
        t3.place(x = size_canvas_x + menu_x//2 - t3.winfo_reqwidth() // 2, y = size_canvas_y)        
    else:
        t1.configure(bg='red')
        t0.configure(bg='#f0f0f0')
        t0.configure(text='ход игрока № 1')
        t0.place(x = size_canvas_x//2 - t0.winfo_reqwidth() // 2, y = size_canvas_y+3)
        t1.configure(text='ход игрока № 2'+ add_to_label)
        t1.place(x = size_canvas_x + menu_x + size_canvas_x// 2 - t1.winfo_reqwidth() // 2, y= size_canvas_y + 3)
        t3.configure(text='ход игрока № 1')
        t3.place(x = size_canvas_x + menu_x//2 - t3.winfo_reqwidth() // 2, y = size_canvas_y)
mark_igrok(hod_igrovoe_pole_1) 



def button_show_enemy1():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                color = "red"
                if points1[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)



def button_show_enemy2():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                color = "red"
                if points2[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(size_canvas_x + menu_x + i * step_x, j * step_y, size_canvas_x + menu_x + i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)



def button_begin_again():
    global list_ids
    global points1, points2
    global boom
    global enemy_ships1, enemy_ships2
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_ships_list() #генерируем новый список кораблей
    enemy_ships1 = generate_enemy_ships()  #генерируем списки кораблей для 1 игрока
    enemy_ships2 = generate_enemy_ships()  #генерируем списки кораблей для 2 игрока
    points1 = [[-1 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули (тут мы его обнуляем)
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули (тут мы его обнуляем)    
    boom = [[0 for i in range(s_x)] for i in range(s_y)] #  это список попаданий по кораблям противника(обнуляем его)



b0 = Button(tk, text="Показать корабли Ирока №1", command=button_show_enemy1)
b0.place(x=size_canvas_x + 20, y=30)

b1 = Button(tk, text="Начать заново!", command=button_begin_again)
b1.place(x=size_canvas_x + 20, y=110)

b2 = Button(tk, text="Показать корабли Игрока №2", command=button_show_enemy2)
b2.place(x=size_canvas_x + 20, y=70)



def draw_point(x, y):
    print(enemy_ships1[y][x])
    if enemy_ships1[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3, x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships1[y][x] > 0:
        color = "blue"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                            x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)



def draw_point2(x, y, offset_x = size_canvas_x + menu_x):
    print(enemy_ships2[y][x])
    if enemy_ships2[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(offset_x + x * step_x + step_x // 3, y * step_y + step_y // 3, offset_x + x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships2[y][x] > 0:
        color = "blue"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 10, offset_x + x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      offset_x + x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)



def check_winner(x,y):
    win = False
    if enemy_ships1[y][x] > 0:
        boom[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))
    sum_boom = sum(sum(i) for i in zip(*boom))    
    print('sum_enemy_ships1' , sum_enemy_ships1, 'sum_boom' , sum_boom)
    if sum_enemy_ships1 == sum_boom:
        win = True
    return win



# 2-й варик проверки на победу
def check_winner2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False    
    return win



# проверка победы игрока №2
def check_winner2_player2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False    
    return win



# функция опр., что ходит компьютер
def hod_computer():
    global points1, points2, hod_igrovoe_pole_1
    tk.update() # обновим экран
    time.sleep(1) # задержка, типа комп думает!
    hod_igrovoe_pole_1 = False
    ip_x = random.randint(0, s_x-1) # определяем коор-ты "случайного" клика
    ip_y = random.randint(0, s_y-1) # определяем коор-ты "случайного" клика
    while not points1[ip_y][ip_x] == -1: # определяем коор-ты, чтобы не попали туда, куда уже кликали
        ip_x = random.randint(0, s_x-1)
        ip_y = random.randint(0, s_y-1)
    points1[ip_y][ip_x] = 7 # если кликали записываем тип клика (ЛКМ или ПКМ)        
    draw_point(ip_x, ip_y) #отрисовываем ход на экране
    # проверяем кто победил
    if check_winner2():
        winner = 'Победа Игрока № 2 !!!' + add_to_label
        winner_add = 'Все корабли противника Игрока №1 уничтожены'
        print(winner, winner_add)
        # блокируем нажатия по нашим игровым полям, т.к. победитель определен                
        points1 = [[10 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули
        points2 = [[10 for i in range(s_x)] for i in range(s_y)] 
        id1 = canvas.create_rectangle(step_x*3, step_y*3, size_canvas_x+menu_x+size_canvas_x-step_x*3, size_canvas_y-step_y, fill = "green") #рамка для вывода сообщения о победе
        id2 = canvas.create_rectangle(step_x*3+step_x//2, step_y*3+step_y//2, 
                                        size_canvas_x+menu_x+size_canvas_x-step_x*3 - step_x//2, 
                                        size_canvas_y-step_y- step_y//2, fill = "yellow")                
        list_ids.append(id1)# чтобы после "начать заново" очистить окно
        list_ids.append(id2)# чтобы после "начать заново" очистить окно
        id3 = canvas.create_text(step_x * 10, step_y * 5, text = winner, font = ("Arial", 50), justify = CENTER) # надпись winner в прямоугольнике 
        id4 = canvas.create_text(step_x * 10, step_y * 6, text = winner_add, font = ("Arial", 25), justify = CENTER) # надпись winner_add в прямоугольнике                
        list_ids.append(id3)# чтобы после "начать заново" очистить окно
        list_ids.append(id4)# чтобы после "начать заново" очистить окно
    


def add_to_all(event):
    global points1, points2, hod_igrovoe_pole_1
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ
    # print(_type)
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    # print(mouse_x, mouse_y)
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    print(ip_x, ip_y, "_type:", _type)

    # первое игровое поле
    if ip_x < s_x and ip_y < s_y and hod_igrovoe_pole_1: # условие на то, что кликаем на 1-е игровое поле 
        if points1[ip_y][ip_x] == -1: # проверяем кликали ли мы сюда или нет
            points1[ip_y][ip_x] = _type # если кликали записываем тип клика (ЛКМ или ПКМ)
            hod_igrovoe_pole_1 = False # передаем ход 2-му игроку
            draw_point(ip_x, ip_y) #отрисовываем 
            #if check_winner(ip_x, ip_y): # проверяем победителя
            if check_winner2():
                hod_igrovoe_pole_1 = True
                winner = 'Победа Игрока № 2 !!!'
                winner_add = 'Все корабли противника Игрока №1 уничтожены'
                print(winner, winner_add)
                # блокируем нажатия по нашим игровым полям, т.к. победитель определен                
                points1 = [[10 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули
                points2 = [[10 for i in range(s_x)] for i in range(s_y)] 
                id1 = canvas.create_rectangle(step_x*3, step_y*3, size_canvas_x+menu_x+size_canvas_x-step_x*3, size_canvas_y-step_y, fill = "green") #рамка для вывода сообщения о победе
                id2 = canvas.create_rectangle(step_x*3+step_x//2, step_y*3+step_y//2, 
                                              size_canvas_x+menu_x+size_canvas_x-step_x*3 - step_x//2, 
                                              size_canvas_y-step_y- step_y//2, fill = "yellow")                
                list_ids.append(id1)# чтобы после "начать заново" очистить окно
                list_ids.append(id2)# чтобы после "начать заново" очистить окно
                id3 = canvas.create_text(step_x * 10, step_y * 5, text = winner, font = ("Arial", 50), justify = CENTER) # надпись winner в прямоугольнике 
                id4 = canvas.create_text(step_x * 10, step_y * 6, text = winner_add, font = ("Arial", 25), justify = CENTER) # надпись winner_add в прямоугольнике                
                list_ids.append(id3)# чтобы после "начать заново" очистить окно
                list_ids.append(id4)# чтобы после "начать заново" очистить окно
        print('len list_ids = ', len(list_ids))

    # второе игровое поле
    print(ip_x, ip_y, "_type:", _type)
    # ЕСЛИ игровое поле по х больше размер игрового поля + смещение для меню И должно быть меньше 
    # чем 2 игровых поля + смещение (для невыхода за правую границу) И так же оставляем условие для границ по У (высоте)
    if ip_x >= s_x + delta_menu_x and ip_x <= s_x + s_x + delta_menu_x and ip_y < s_y and not hod_igrovoe_pole_1: # условие на то, что кликаем на 1-е игровое поле
        if points2[ip_y][ip_x - s_x - delta_menu_x] == -1:# проверяем кликали ли мы сюда или нет
            points2[ip_y][ip_x - s_x - delta_menu_x] = _type# если кликали записываем тип клика (ЛКМ или ПКМ)
            hod_igrovoe_pole_1 = True # передаем ход 1-му игроку
            draw_point2(ip_x - s_x - delta_menu_x, ip_y)#отрисовываем 
            #if check_winner(ip_x, ip_y):# проверяем победителя
            if check_winner2_player2():
                hod_igrovoe_pole_1 = False
                winner = 'Победа Игрока № 1 !!!'
                winner_add = 'Все корабли противника Игрока №2 уничтожены'
                print(winner, winner_add)
                # блокируем нажатия по нашим игровым полям, т.к. победитель определен
                points2 = [[10 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули
                points1 = [[10 for i in range(s_x)] for i in range(s_y)] #  это список куда мы кликнули                
                id1 = canvas.create_rectangle(step_x*3, step_y*3, size_canvas_x+menu_x+size_canvas_x-step_x*3, size_canvas_y-step_y, fill = "green") #рамка для вывода сообщения о победе
                id2 = canvas.create_rectangle(step_x*3+step_x//2, step_y*3+step_y//2, 
                                              size_canvas_x+menu_x+size_canvas_x-step_x*3 - step_x//2, 
                                              size_canvas_y-step_y- step_y//2, fill = "yellow")                
                list_ids.append(id1)# чтобы после "начать заново" очистить окно
                list_ids.append(id2)# чтобы после "начать заново" очистить окно                
                id3 = canvas.create_text(step_x * 10, step_y * 5, text = winner, font = ("Arial", 50), justify = CENTER) # надпись winner в прямоугольнике 
                id4 = canvas.create_text(step_x * 10, step_y * 6, text = winner_add, font = ("Arial", 25), justify = CENTER) # надпись winner_add в прямоугольнике                
                list_ids.append(id3)# чтобы после "начать заново" очистить окно
                list_ids.append(id4)# чтобы после "начать заново" очистить окно
            # если играем против компа:
            elif computer_vs_human: 
                mark_igrok(hod_igrovoe_pole_1)
                hod_computer() # функция, что ходит комп                    
        print('len list_ids = ', len(list_ids))
    mark_igrok(hod_igrovoe_pole_1)


canvas.bind_all("<Button-1>", add_to_all)  # ЛКМ
canvas.bind_all("<Button-3>", add_to_all)  # ПКМ



#Ф-я генерирующая спиок кораблей
def generate_ships_list():
    global ships_list
    ships_list = [] # обнуляем список
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))
    # print(ships_list)



def generate_enemy_ships():
    enemy_ships = []
    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0
    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in
                       range(s_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y:
                primerno_y = primerno_y - len

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1:
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

        # print(sum_1_enemy)
        # print(ships_list)
        print(enemy_ships)
    return enemy_ships

generate_ships_list()
enemy_ships1 = generate_enemy_ships()  #генерируем списки кораблей для 1 игрока
enemy_ships2 = generate_enemy_ships()  #генерируем списки кораблей для 2 игрока
print('**********')
print(enemy_ships1)
print(enemy_ships2)
print('**********')



while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
