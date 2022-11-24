# Library Imports
import numpy as np
import json

# Dataset Imports
with open('dataset/dataset.json') as json_data:
    intents = json.load(json_data)

# Question, answer listing 
questions = []
answer = [] 
context = []

for intent in intents['data']:
    if (intent['title'] == "YouTube"):
        for paragrap in intent['paragraphs']:
            context.append(paragrap['context'])
            for qas in paragrap['qas']:
                questions.append(qas['question'].lower())
                if (qas['is_impossible']) :
                    for plau_ans in qas['plausible_answers']:
                        answer.append(plau_ans['text'])
                else : 
                     for ans in qas['answers']:
                        answer.append(ans['text'])

context = context[0]

# Vectorizer
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(questions)

# Transformer
from sklearn.feature_extraction.text import TfidfTransformer
tfidf = TfidfTransformer() #by default applies "l2" normalization
X_tfidf = tfidf.fit_transform(X_vec)

#Creating tkinter GUI
import webbrowser
from tkinter import *
from tkinter import ttk
from sklearn.metrics.pairwise import cosine_similarity

def init():
    ChatBox.config(state=NORMAL)
    ChatBox.insert(END, "Bot: Halo, selamat datang! Ada yang bisa saya bantu? \n\n" )
    ChatBox.config(foreground="#000000", font=("Verdana", 10 ))

def callback():
    webbrowser.open_new(r"https://rifkisagas.github.io/portfolio/")

def goodbye():
    new= Toplevel(root)
    new.geometry("250x120")
    new.title("Terimakasih!")
    new.resizable(width=FALSE, height=FALSE)
    Label(new, text="Sampai nanti!", font=("Verdana",17,'bold')).pack(pady=30)
    ttk.Button(new, text="Ok", command=root.destroy).pack()

def conversation(im):
    global tfidf, X_tfidf
    Y_vec = vectorizer.transform(im)
    Y_tfidf = tfidf.fit_transform(Y_vec)
    cos_sim = np.rad2deg(np.arccos(max(cosine_similarity(Y_tfidf, X_tfidf)[0])))
    if cos_sim > 60 :
        return "Maaf, pengalaman saya kurang banyak untuk menjawab.."
    else:
        return answer[np.argmax(cosine_similarity(Y_tfidf, X_tfidf)[0])]

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    im = [msg]
    EntryBox.delete("0.0",END)

    if msg == "Beritahu saya tentang Youtube":
        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, "Anda: " + msg + '\n\n')
        ChatBox.config(foreground="#000000", font=("Verdana", 10 ))
        res = context
        ChatBox.insert(END, "Bot: " + res + '\n\n')   
        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)

    elif msg != '':
        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, "Anda: " + msg + '\n\n')
        ChatBox.config(foreground="#000000", font=("Verdana", 10 ))
    
        ints = conversation(im)
        res = ints
        
        ChatBox.insert(END, "Bot: " + res + '\n\n')
            
        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)

def view():
    new= Toplevel(root)
    new.geometry("500x600")
    new.title("Frequently Asked Questions")
    new.resizable(width=FALSE, height=FALSE)
    new_ChatBox = Text(new, bd=0, bg="white", height="8", width="50", font="Arial",)
    new_ChatBox.place(x=6,y=6, height=520, width=470)
    new_SendButton = Button(new, font=("Verdana",9,'bold'), text="Tutup", width="12", height=5,
                    bd=0, bg="#BA0001", activebackground="#3c9d9b",fg='#ffffff',
                    command= new.destroy)
    new_SendButton.place(x=440, y=550, height=30, width=50)
    new_scrollbar = Scrollbar(new, command=new_ChatBox.yview, cursor="double_arrow")
    new_ChatBox['yscrollcommand'] = new_scrollbar.set
    new_scrollbar.place(x=478,y=8, height=520)

    # FAQ
    new_ChatBox.config(state=NORMAL)
    # pertanyaan = ['Kapan youtube dibuat?', 'Siapa CEO Youtube?', 
    #              'Berapa Google membayar Youtube pada tahun 2006?', 
    #              'Selain video blogging dan pendidikan, apa saja yang tersedia di Youtube?', 
    #              'Siapa yang menjual Youtube?',]

    pertanyaan = questions
    for i in pertanyaan:
        str_pertanyaan = i 
        new_ChatBox.config(state=NORMAL)
        new_ChatBox.insert(END, "Anda: " + str_pertanyaan + '\n\n')
        new_ChatBox.config(foreground="#000000", font=("Verdana", 10 ))
        im = [i]
        ints = conversation(im)
        res = ints
        new_ChatBox.insert(END, "Bot: " + res + '\n\n')
        new_ChatBox.config(state=DISABLED)
        new_ChatBox.yview(END)

#root window
root = Tk()
root.title("Youtube Company Question Answering (Bahasa Indonesia)")
root.geometry("600x550")
root.resizable(width=FALSE, height=FALSE)

# #inclusion
# bg = PhotoImage(file="bg.png")
# label1 = Label( root, image = bg)
# label1.place(x = 0, y = 0)
# root.wm_attributes('-transparentcolor','black')

#Create Chat window
ChatBox = Text(root, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatBox.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(root, command=ChatBox.yview, cursor="double_arrow")
ChatBox['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(root, font=("Verdana",9,'bold'), text="Kirim", width="12", height=5,
                    bd=0, bg="#00c441", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(root, bd=0, bg="#dddddd",width="80", height="5", font=("Arial",12))


#Create Additional Information window
faqButton = Button(root, font=("Verdana",9,'bold'), text="FAQ", width="12", height=5,
                    bd=0, bg="#C8B88A", activebackground="#3c9d9b",fg='#ffffff',
                    command= view)
# faq_ChatBox.config(state=DISABLED)

#Place all components on the screen
scrollbar.place(x=576,y=6, height=386)
ChatBox.place(x=6,y=6, height=386, width=570)
EntryBox.place(x=6, y=401, height=30, width=520)
SendButton.place(x=540, y=401, height=30, width=50)

#Place additional button
faqButton.place(x=6,y=450, height=80, width=80)
aboutButton = Button(root, font=("Verdana",9,'bold'), text="Tentang\nDeveloper", width="12", height=5,
                    bd=0, bg="#86B049", activebackground="#3c9d9b",fg='#ffffff',
                    command= callback)
aboutButton.place(x=420,y=450, height=80, width=80)

exitButton = Button(root, font=("Verdana",9,'bold'), text="Keluar", width="12", height=5,
                    bd=0, bg="#BA0001", activebackground="#3c9d9b",fg='#ffffff',
                    command= goodbye)
exitButton.place(x=510,y=450, height=80, width=80)
init()
root.mainloop()