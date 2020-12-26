from tkinter import *
from PIL import Image, ImageDraw

window = Tk()

def show_image1():
    image = Image.open(addres.get())
    image.show()
def show_image2():
    image = Image.open(addres1.get())
    image.show()

def find_word(line):
    for step in range(1, len(line)):
        for start in range(step):
            if len(set(line[(start or None)::step])) != 1:
                break
        else:
            return line[:step]
    return line

def text_to_bits(text, encoding='utf-16', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))
def text_from_bits(bits, encoding='utf-16', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

word_size=0
def hide_text():
    image = Image.open(addres.get())
    word = text.get()
    binary_word = text_to_bits(word)
    word_size = len(str(binary_word))

    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    k=0
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            if c % 2 == 1 and binary_word[k % word_size] == '0':
                c = c - 1;
            elif c % 2 == 0 and binary_word[k % word_size] == '1':
                c = c + 1;
            k = k + 1
            draw.point((i, j), (a, b, c))
    image.save(addres1.get(), "PNG")

def find_text():
    image1 = Image.open(addres2.get())
    width1 = image1.size[0]
    height1 = image1.size[1]
    pix = image1.load()
    word1 = str('')
    for i in range(int(width1/2)):
        for j in range(height1):
            c = pix[i, j][2]
            c1 = c % 2
            word1 = word1 + str(c1)
    text_word=find_word(text_from_bits(word1))
    lbll.configure(text=text_word)



window.title("Это приложение прячет ваше слово в изображении так, что вы ее не найдете")
window.geometry('130000x500')
lbl = Label(window, text="Введите адрес изображения, в которое нужно спрятать слово(расширение изображения .png). Пример: C:\\Users\\raush\Downloads\\404.png")
lbl.grid(column=0, row=0)
addres = Entry(window, width=45)
addres.grid(column=1, row=0)
lbl1 = Label(window, text="Введите слово")
lbl1.grid(column=0, row=1)
text = Entry(window, width=45)
text.grid(column=1, row=1)
lbl2 = Label(window, text="Введите адрес и название изображения для сохранения. Пример: C:\\Users\\raush\Downloads\\404.png")
lbl2.grid(column=0, row=2)
addres1 = Entry(window, width=45)
addres1.grid(column=1, row=2)
btn = Button(window, text="Спрятать", command=hide_text)
btn.grid(column=1, row=3)
lbl2 = Label(window, text="Введите адрес изображения, в котором хотите найти слово. Пример: C:\\Users\\raush\Downloads\\404.png")
lbl2.grid(column=0, row=4)
addres2 = Entry(window, width=45)
addres2.grid(column=1, row=4)
btn1 = Button(window, text="Найти", command=find_text)
btn1.grid(column=1, row=5)
lblll = Label(window, text="Мы нашли сообщение, котрое спрятали в изображении: ")
lblll.grid(column=0, row=6)
lbll = Label(window, text="")
lbll.grid(column=1, row=6)
btn1 = Button(window, text="Показать исходное изображение", command=show_image1)
btn1.grid(column=0, row=7)
btn1 = Button(window, text="Показать изображение со спрятанным в ней словом", command=show_image2)
btn1.grid(column=1, row=7)

window.mainloop()