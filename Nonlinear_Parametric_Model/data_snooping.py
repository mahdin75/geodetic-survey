#it gets a file then does adjustment...

#error codes:
# {1: error in pick a file}
# {2: error in parse csv}

import Tkinter
import tkMessageBox
from tkFileDialog import askopenfilename
import csv
import numpy
import math
import scipy.stats #for chi2 disturbution

#-------------------GUI Tkinter: create a window-------------------
top = Tkinter.Tk()

#-------------------GUI Tkinter: create a frames(containers)-------------------
frameTop = Tkinter.Frame(top)
frameTop.pack()

frameBottom = Tkinter.Frame(top)
frameBottom.pack(side = Tkinter.BOTTOM)





#show file data 1
def showData1(f):
    stringToPrint=""
    data = csv.reader(f,delimiter=',')
    for row in data:
        rr=''
        i = 0
        for ele in row:
            rr = rr + ele
            if i<2:
                rr = rr + ','
            i = i + 1
        stringToPrint = stringToPrint + rr + '\n'
    TextArea2.delete("1.0",'end-1c')  
    TextArea2.insert(Tkinter.INSERT, stringToPrint)  
    f.close()
       
#select file1
def pickAFile1():
    try:
        filename = askopenfilename()
        f = open(filename,'r')
    except IOError:
        print "error code: 1"
    else:
        showData1(f)

#show file data2
def showData2(f):
    stringToPrint=""
    data = csv.reader(f,delimiter=',')
    for row in data:
        rr=''
        i = 0
        for ele in row:
            rr = rr + ele
            if i<3:
                rr = rr + ','
            i = i + 1
        stringToPrint = stringToPrint + rr + '\n'
    TextArea.delete("1.0",'end-1c')  
    TextArea.insert(Tkinter.INSERT, stringToPrint)  
    f.close()
        
#select file2
def pickAFile2():
    try:
        filename = askopenfilename()
        f = open(filename,'r')
    except IOError:
        print "error code: 1"
    else:
        showData2(f)

#create new window for resualts
def create_window(res):
    #window
    window = Tkinter.Toplevel(top)
    #label
    var3 = Tkinter.StringVar()
    label3 = Tkinter.Label(window, textvariable=var3, width=40,fg='white', bg='#550',  relief= Tkinter.RAISED )
    var3.set("ID,   X,   Y,   R Error")
    label3.pack()
    #textbox and scrollbar
    textRes = Tkinter.Text(window)
    ScrollBar3 = Tkinter.Scrollbar(window)
    ScrollBar3.config(command=textRes.yview)
    textRes.config(yscrollcommand=ScrollBar3.set,height = 10,width= 30)
    ScrollBar3.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
    textRes.pack(fill=Tkinter.BOTH)
    
    textRes.delete("1.0",'end-1c')  
    textRes.insert(Tkinter.INSERT, res)  

#Algorithm to do adjustment
def getDistFromId(id1,id2,coorsData):
    for row in coorsData:
        if row[0] == id1:
            coor1 = [row[1],row[2]]
        if row[0] == id2:
            coor2 = [row[1],row[2]]
    return math.sqrt((float(coor1[0])-float(coor2[0]))**2+(float(coor1[1])-float(coor2[1]))**2);

#function helper for next function
def getIndexInPriorCoord(id,unknown):
    index = -1
    for t in unknown:
        index = index + 1
        if id == t[0]:
            return index
    return -100000 #this have to be here to have one parameter returned

#function to comput each diff
def diffComputer(a,b,c,d):
    return (a-b)/(math.sqrt((a-b)**2+(c-d)**2))

#function for creating design matrix
def getDiff(fr,to,i,known,unknown,dist):
    if i == getIndexInPriorCoord(fr,unknown) or i==getIndexInPriorCoord(to,unknown) or i==len(unknown)+getIndexInPriorCoord(fr,unknown) or i==len(unknown)+getIndexInPriorCoord(to,unknown):
        #diff for each parameter that it is not zero
        coors = known + unknown
        thisCoors = []
        for q in coors:
            if fr == q[0]:
                thisCoors.append([q[0],q[1],q[2]])
            if to == q[0]:
                thisCoors.append([q[0],q[1],q[2]])
        if i<=(len(unknown)-1):
            if unknown[i][0]== thisCoors[0][0]:
                coorForComput =  [[thisCoors[0][1],thisCoors[0][2]],[thisCoors[1][1],thisCoors[1][2]]]
            else:
                coorForComput =  [[thisCoors[1][1],thisCoors[1][2]],[thisCoors[0][1],thisCoors[0][2]]]
            return diffComputer(coorForComput[0][0],coorForComput[1][0],coorForComput[0][1],coorForComput[1][1])
        else:
            if unknown[i-len(unknown)][0]== thisCoors[0][0]:
                coorForComput =  [[thisCoors[0][1],thisCoors[0][2]],[thisCoors[1][1],thisCoors[1][2]]]
            else:
                coorForComput =  [[thisCoors[1][1],thisCoors[1][2]],[thisCoors[0][1],thisCoors[0][2]]]
            return diffComputer(coorForComput[0][1],coorForComput[1][1],coorForComput[0][0],coorForComput[1][0])
          
    else:
         return 0   
    
#w test func
def findMistake(ehat,qehat):
    print qehat
    print ehat
    print '---start to find mistake observations...'
    maxError = numpy.max(numpy.abs(ehat/numpy.sqrt(qehat)))
    print numpy.abs(ehat/numpy.sqrt(qehat))
    zAlphPer2 = scipy.stats.norm.ppf(0.975)
    if maxError > zAlphPer2:
        indexOfMistake = numpy.argmax(numpy.abs(ehat/numpy.sqrt(qehat)))
        print 'Ohh yes there is an error!!!!!!!'
        print 'obs with index('+ str(indexOfMistake) + ') will be clear...'
        return [True,indexOfMistake]
    else:
        return [False,False]


wtestRes = [False,False]
def computer(wtestRes):
    #get and parse distance data from text box

    data = TextArea2.get("1.0",'end-1c')
    data = data.splitlines()
    distData = []
    m = 0
    #remove mistake Data W Testt
    if wtestRes[0]:
        data.pop(wtestRes[1])
        print 'Number of Data is now: '+str(len(data))

        #update text field
        ff = 0
        str1 = ''
        while 1:
            str1 = str1 + str(data[ff])+'\n'
            ff = ff + 1
            if len(data) <= ff:
                break 
        TextArea2.delete("1.0",'end-1c')
        TextArea2.insert("1.0",str1)

    
    data = csv.reader(data,delimiter=',')
    for row in data:
        m = m+1
        distData.append(map(float,row))
    
    #get and parse 'prior coordinates' and 'fixed coors'
    priorCoorData = []
    priorCoorDataX = []
    priorCoorDataY = []
    fixedCoorData = []
    n = 0
    data = TextArea.get("1.0",'end-1c')
    data = data.splitlines()
    data = csv.reader(data,delimiter=',')
    for row in data:
        if row[3] == '0':
            priorCoorData.append(map(float,row))
            priorCoorDataX.append(float(row[1]))    
            priorCoorDataY.append(float(row[2]))
            n = n + 1
        elif row[3] == '1':
            fixedCoorData.append(map(float,row))
    n = 2*n
    
    #Adjustment Alorithm ( LSQ ) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    A = numpy.zeros((m,n))
    Y = numpy.matrix(distData)
    Y = Y[:,2]
    Yi = numpy.ones((m))
    Yi = Yi.tolist()
    Yi = numpy.matrix([Yi])
    #sigma = 2mm
    Qy = numpy.eye(m)*0.0025
    dx = numpy.ones((n))
    x = numpy.matrix(priorCoorDataX+priorCoorDataY)
    s = 0
    #adjustment loop
    while numpy.linalg.norm(dx)>0.000000000001:
        
        #update Yi
        j = 0
        x = x.tolist()
        x = x[0]
        for row in priorCoorData:  #data is coorData!
            row[1] = x[j]
            row[2] = x[j+(len(x)/2)]
            j = j + 1
        j = 0

        Yi = Yi.tolist()
        Yi = Yi[0]
        for row in distData:
            dist = getDistFromId(row[0],row[1],fixedCoorData+priorCoorData)
            row[2] = dist
            Yi[j] = dist
            j = j + 1

        Yi = numpy.matrix(Yi)
        x = numpy.matrix(x)

        dy = Y - Yi.transpose()

        #update A
        j = 0
        A = A.tolist()
        x = x.tolist()
        x = x[0]
        for row in distData:
            i = 0
            for t in x: 
                A[j][i] = getDiff(row[0],row[1],i,fixedCoorData,priorCoorData,distData)
                i = i + 1
            j = j + 1 
            
        A = numpy.matrix(A)
        x = numpy.matrix(x)
        #compute dx
        dx = numpy.linalg.inv(A.transpose()*numpy.linalg.inv(Qy)*A)*A.transpose()*numpy.linalg.inv(Qy)*dy
        x = x.transpose()  + dx
        x = x.transpose()
        s = s + 1
    ehat = dy
    sigma0hat = (ehat.transpose()*(numpy.linalg.inv(Qy))*ehat)/(m-n)
    #chi2 Test
    df = m - n
    g = df*sigma0hat
    RightChi2test = g/scipy.stats.chi2.ppf(0.025,df)
    LeftChi2test = g/scipy.stats.chi2.ppf(0.975,df)
    
    print str(LeftChi2test[0,0])+'   <   1   <    '+ str(RightChi2test[0,0]) + '     ?!'
    if 1<RightChi2test and LeftChi2test<1:
        print 'test was accepted'
        #print results
        resultsToShow = x.tolist()
        create_window(str(resultsToShow))
    else:
        #w test
        qehat = (numpy.eye(m)-A*(numpy.linalg.inv(A.transpose()*numpy.linalg.inv(Qy)*A)*A.transpose()*numpy.linalg.inv(Qy)))*Qy
        print 'test was denied'
        wtestRes = findMistake(ehat.transpose(),qehat.diagonal())
        #computer(wtestRes)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!here!!!!!
        #recursive function
        computer(wtestRes)
        
    return (sigma0hat,m-n)



#-------------------GUI Tkinter : create Labels-------------------
var1 = Tkinter.StringVar()
var2 = Tkinter.StringVar()
label1 = Tkinter.Label(frameTop, textvariable=var1, width=40, fg='white', bg='#550', relief= Tkinter.RAISED )
label2 = Tkinter.Label(frameBottom, textvariable=var2, width=40,fg='white', bg='#550',  relief= Tkinter.RAISED )
var1.set("ID,   X,   Y,   Fixed Point")
label1.pack()
var2.set("From,   To,   Distance")
label2.pack()

#-------------------GUI Tkinter: create textarea-------------------
TextArea = Tkinter.Text(frameTop)
ScrollBar = Tkinter.Scrollbar(frameTop)
ScrollBar.config(command=TextArea.yview)
TextArea.config(yscrollcommand=ScrollBar.set,height = 10,width= 30)
ScrollBar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
TextArea.pack(fill=Tkinter.BOTH)

#-------------------GUI Tkinter: create a textarea2-------------------
TextArea2 = Tkinter.Text(frameBottom)
ScrollBar2 = Tkinter.Scrollbar(frameBottom)
ScrollBar2.config(command=TextArea2.yview)
TextArea2.config(yscrollcommand=ScrollBar2.set,height = 10,width= 30)
ScrollBar2.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
TextArea2.pack(fill=Tkinter.BOTH)

#-------------------GUI Tkinter: create buttons-------------------
B1 = Tkinter.Button(frameBottom, text ="pick distance file: .csv", command = pickAFile1).pack()
B2 = Tkinter.Button(frameTop, text ="pick coordinates file: .csv", command = pickAFile2).pack()
B3 = Tkinter.Button(frameBottom, text ="compute",bg='purple', command = lambda: computer(wtestRes)).pack()

#-------------------GUI Tkinter: to save UI-------------------
top.mainloop()
