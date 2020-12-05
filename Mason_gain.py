try:
    import numpy
    from tkinter import *
    import tkinter as tk
    from tkinter import ttk
    import os,sys
    from PIL import ImageTk, Image
    import cv2
    os.startfile('Instruction.docx')
except:
    print('can not run programme in your system. Please run again')
    
def show_sfg():
    x= 500
    y=600
    t= 50
    img= numpy.zeros((y,x+2*t,3),numpy.uint8)
    l= len(dict)
    dict2={}
    i=1
    for node in dict:
        dict2[node]={'col':(numpy.random.randint(100,250),numpy.random.randint(100,200),numpy.random.randint(100,240)),'loc':(t+int((x-t)/l)*i,int(y/2))}
        img= cv2.circle(img,dict2[node]['loc'],4, dict2[node]['col'],4)
        i+=1
    for node in dict2:
         for node2 in dict[node]:
             x0,y0= dict2[node]['loc']
             x1,y1= dict2[node2]['loc']
             if not node== node2:
                 imx= int(abs((x0-x1)/2)) +x0 if x0<x1 else int(abs((x0-x1)/2)) +x1
                 imy= int((x1-x0)/2)
                 imy= imy+2*int(t*(imy/abs(imy)))
                 img= cv2.line(img,(x0,y0),(imx,y0+imy),dict2[node]['col'],2)
                 img= cv2.line(img,(imx,y0+imy),(x1,y1),dict2[node]['col'],2)
             else:
                 img= cv2.line(img,(x0,y0),(x0-7,y0-50),dict2[node]['col'],2)
                 img= cv2.line(img,(x0-7,y0-50),(x0+7,y0-50),dict2[node]['col'],2)
                 img= cv2.line(img,(x0+7,y0-50),(x0,y0),dict2[node]['col'],2)

    cv2.imshow('SFG!!',img)
    
def frwrd_paths(imput,output):
    node= imput
    visited={}
    stack=[imput]
    final=[]
    for i in dict:
        visited[i]=[]
    while True:
        c=0
        for key in dict[node]:
            if key not in stack and key not in visited[node]:
                c=1
                stack.append(key)
                if key== output:
                    final.append(stack)
                    stack=stack[:-1]
                    visited[node].append(output)
                    node= stack[-1]
                else:
                    visited[node].append(key)
                    node=key
            if c==1:
                    break
        if c==0:
            if len(stack)>1:
                stack=stack[:-1]
            else:
                break
            node=stack[-1]
    print('Frwrd paths',final)
    frwrd_values=[]
    c=[value_finder(i) for i in final]
    print('values:',c)
    return final,c

def loop():
    queue= [[i] for i in dict]
    final=[]
    explored=[]
    while queue:
        x= queue[0]
        queue.remove(x)
        i= x[-1]
        neigh= dict[i]
        for j in neigh:
            a=x.copy()
            if j not in x :
                a.append(j)
                queue.append(a)
            if j==x[0]:
                a.append(j)
                final.append(a)
        explored.append(i)
    yeho=[]
    for i in range(len(final)):
        x= final[i]
        b=[]
        for j in range(len(x)-1):
            b.append(str(x[j])+str(x[j+1]))
        b.sort(reverse=False)
        c=''
        for k in b:
            c= str(c)+str(k)
        yeho.append(c)
    duplicate_ind = [idx for idx, val in enumerate(yeho) if val in yeho[:idx]]
    final=[final[i] for i in range(len(final)) if i not in duplicate_ind]
    print('Closed Loops-',final)
    value=[ value_finder(i) for i in final]
    print('Loops values:>>',value)
    return final,value

def delta_k(frwrd,lp):
    dtk={}
    dtk_value={}
    for i in range(0,len(frwrd)):
        x= frwrd[i][:-1]
        d=[]
        for cl in lp:
            if not (any(i in cl for i in x)):
                    d.append(cl)
        dtk[str(i+1)]=d
        dtk_value[str(i+1)]= [value_finder(k) for k in d]
    print('Delta K closed loops:',dtk,'corresponding values>>>', dtk_value)
    deltak= []
    for i in dtk:
        s=0
        ntlpsv= non_touching_lps(dtk[i])
        n3tl= n3ltps(dtk[i])
        n4tl= n4ltps(dtk[i])
        s= delta_from_node(ntlpsv, dtk_value[i], n3tl, n4tl)
        deltak.append(s)
    return dtk, deltak

def non_touching_lps(lp):
    temp_lp= lp.copy()
    print('Non touching loops indicated below')
    dict={}
    while temp_lp:
        x= temp_lp[0]
        temp_lp.remove(x)
        print(x,'>>>>>',end='')
        v= value_finder(x)
        print('value>>>',v)                            #xtra
        a=[]
        for j in range(len(temp_lp)):
            if not (any(i in x for i in temp_lp[j])):
                print(temp_lp[j],end='-->')
                a.append(value_finder(temp_lp[j]))
                print(value_finder(temp_lp[j]),end='>>>')  #xtra
        if len(a)>0 :
            dict[v]= a 
        print('')
    print('printing non-touching-loop-dict<<>>',dict)
    return dict
                         
def value_finder(node_l):
    m=1
    c=[]
    for i in range(0,len(node_l)-1):
        m*= dict[node_l[i]][node_l[i+1]]
    return m

def delta_from_node(ntlps_value,lp_value, n3tl, n4tl):
    s=0
    for x in ntlps_value:
        l= ntlps_value[x].copy()
        p=0
        for i in l:
            p+=i
        p=p*x
        s+=p
    s1=0
    for x in lp_value:
        s1+=x
    s= s+1-s1 -n3tl + n4tl
    return s

def n3ltps(lp):
    s=0
    if len(lp)<3:
        return 0
    for i in range(0,len(lp)-2):
        for j in range(i+1,len(lp)-1):
            for k in range(j+1,len(lp)):
                if not( any(p in lp[i] for p in lp[j]) and any(q in lp[j] for q in lp[k])):
                    s+= value_finder(lp[i])*value_finder(lp[j])*value_finder(lp[k])
                    print('3 non_touching_loop_exist',lp[i],'>>',lp[j],'>>',lp[k])
                    print('values:-',value_finder(lp[i]), value_finder(lp[j]), value_finder(lp[k])) #xtra
    return s
def n4ltps(lp):
    s=0
    if len(lp)<4:
        return 0
    for i in range(0,len(lp)-3):
        for j in range(i+1,len(lp)-2):
            for k in range(j+1,len(lp)-1):
                for l in range(k+1, len(lp)):
                    if not any(p in lp[i] for p in lp[j]) and not any(q in lp[j] for q in lp[k]) and not any(r in lp[k] for r in lp[l]):
                        s+= value_finder(lp[i])*value_finder(lp[j])*value_finder(lp[k])*value_finder(lp[l])
                        print('4 non_touching_loop_exist',lp[i],'>>',lp[j],'>>',lp[k],'>>',lp[l])
                        print('values:>>',value_finder(lp[i]),value_finder(lp[j]),value_finder(lp[k]),value_finder(lp[l]))  #xtra
    return s

def main():
    sn= str(sampleEntry4.get())
    en= str(sampleEntry5.get())
    frwrd, frwrd_value =frwrd_paths(sn,en)  
    lp, lp_value =loop()
    dtk, deltak =delta_k(frwrd,lp)
    ntl= non_touching_lps(lp)
    n3tl= n3ltps(lp)
    n4tl= n4ltps(lp)
    dnmtr_delta= delta_from_node(ntl,lp_value, n3tl, n4tl)
    print('/\= ',dnmtr_delta)
    print('/\k=',deltak)
    frwrd_value= numpy.array(frwrd_value)
    deltak= numpy.array(deltak)
    numrtr= numpy.dot(deltak,frwrd_value.T)
    print('TF=',numrtr/dnmtr_delta)
    #show_sfg()
    sampleListBox.delete(0,END)
    sampleListBox.insert(END,numrtr/dnmtr_delta)
    
#dict={'1':{'1':1,'2':3,'3':6},'2':{'1':2,'3':5,'2':8},'3':{'2':7}}
dict={}
#main()
def add_node():
    fr= str(sampleEntry1.get())
    to= str(sampleEntry2.get())
    w= float(sampleEntry3.get())
    if fr not in dict:
        dict[fr]={}
    if to not in dict:
        dict[to]={}
    dict[fr][to]=w

def clear_all():
    dict={}

def open_file():
    try:
        os.startfile('Logic_Img.jpg')
    except:
        print('Plz specify a default open with for file under Properties')
  
root = Tk()
root.configure(background='black')
root.title("Masons Gain ")

sampleFrame = Canvas(root, bg="black")
img= Image.open('thumbnail.jpg')
img= img.resize((1060,512))
image= ImageTk.PhotoImage(img)

sampleFrame.create_image(0,0,anchor=NW, image=image)
sampleFrame.pack()

sampleLabel0 = Label(sampleFrame, text='                    Transfer Function calculation using Mason Gain Formula', font=('Heveltica', 20, 'normal'), bg='black',fg="red")
sampleLabel0.grid(row=1, column=0, pady="10", padx="5")

sampleLabel1 = Label(sampleFrame, text='write from node', font=('Heveltica', 11, 'normal'), bg='black',fg="white")
sampleLabel1.grid(row=2, column=0, pady="10", padx="5")

sampleLabel2 = Label(sampleFrame, text='write To node', font=('Heveltica', 11, 'normal'),bg='black', fg="white")
sampleLabel2.grid(row=3, column=0, pady="10", padx="5")

sampleLabel3 = Label(sampleFrame, text='write weight', font=('Heveltica', 11, 'normal'), bg="black",fg= 'white')
sampleLabel3.grid(row=4, column=0, pady="10", padx="5")

sampleLabel4 = Label(sampleFrame, text='* Made in time constraint. Report any bug to 107119002@nitt.edu', font=('Heveltica', 10, 'italic'), bg='black',fg="pink")
sampleLabel4.grid(row=10, column=0, pady="10", padx="5")

sampleEntry1 = Entry(sampleFrame, font=('Heveltica', 13, 'normal'))
sampleEntry1.grid(row=2, column=1, columnspan=2, pady="12", padx="5")

sampleEntry2 = Entry(sampleFrame, font=('Heveltica', 13, 'normal'))
sampleEntry2.grid(row=3, column=1, columnspan=2, pady="12", padx="5")

sampleEntry3 = Entry(sampleFrame, font=('Heveltica', 13, 'normal'))
sampleEntry3.grid(row=4, column=1, columnspan=2, pady="12", padx="5")

sampleButton1 = Button(sampleFrame, text="Clear All", relief='ridge', bg="yellow", command=clear_all)
sampleButton1.grid(row=5, column=0, columnspan=2, pady="12", padx="5")

sampleButton2 = Button(sampleFrame, text="ADD Path", relief='ridge', bg="yellow", command=add_node)
sampleButton2.grid(row=5, column=1, columnspan=2, pady="12", padx="5")

sampleButton3 = Button(sampleFrame, text="Calculate TF", relief='ridge', bg="yellow", command=main)
sampleButton3.grid(row=8, column=0, columnspan=2, pady="12", padx="5")

sampleLabel5 = Label(sampleFrame, text='write start node', font=('Heveltica', 11, 'normal'),bg='black', fg="white")
sampleLabel5.grid(row=6, column=0, pady="10", padx="5")

sampleLabel6 = Label(sampleFrame, text='write end node', font=('Heveltica', 11, 'normal'),bg='black', fg="white")
sampleLabel6.grid(row=7, column=0, pady="10", padx="5")

sampleEntry4 = Entry(sampleFrame, font=('Heveltica', 13, 'normal'))
sampleEntry4.grid(row=6, column=1, columnspan=2, pady="12", padx="5")

sampleEntry5 = Entry(sampleFrame, font=('Heveltica', 13, 'normal'))
sampleEntry5.grid(row=7, column=1, columnspan=2, pady="12", padx="5")

sampleListBox = Listbox(sampleFrame, width=20, font=('Heveltica', 12, 'normal'), height=1, bg="cyan")   
sampleListBox.grid(row=8, column=2, columnspan=1, pady="5", padx="5")

sampleButton0 = Button(sampleFrame, text="Click for Logic", relief='ridge', bg="magenta", command=open_file)
sampleButton0.grid(row=9, column=2, columnspan=1, pady="12", padx="5")
sampleListBox.insert(END,'Answer display')

sampleButton34 = Button(sampleFrame, text="Click for SFG", relief='ridge', bg="magenta", command=show_sfg)
sampleButton34.grid(row=9, column=0, columnspan=1, pady="12", padx="5")
root.mainloop()
