# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 08:20:47 2018

@author: Dominik Pfeiffer
Modul zur Erzeugung verschiedener Blenden
"""
import numpy as np
from PIL import Image 

"""
Umrechnen der Array-Koordinaten in Spiegelkoordinaten in Einheiten des Pitches
1 Spiegeleinheit = 10,8mu m
"""
def realxy(j,i):
    if i%2 == 0:
        return(j,i/2)
    else:
        return(j+1/2,i/2)
        
"""
Bestimmen der Iterationsparameter
Maximaler Blendenradius - r (double)
Mittelpunkt - x0,y0 (double)
"""
def abcd(r,x0,y0):
    a = int(max(0,y0-2*r))
    b = int(max(0,y0+2*r))+1
    c = int(max(0,x0-r))
    d = int(max(0,x0+r))+1
    return(a,b,c,d)

"""
Funktion zum Speichern eines Bildes
"""
def save(pic,name):
    pic.save(name)
"""
Einfache Blendensequenzen erzeugen
Minimaler/Maximaler Radius in Spiegeleinheiten - rmin/rmax (float) typische Werte: rmin 85, rmax:170 (*10.8 mum)
Länge der Sequenz - l (int)
Speicherverzeichnis - verz (String)
Nullpunkt - x0,y0 (int) (Default: x0=304,y0=342)
Normal/Negativ - bol (Boolean) (Default=True -> 'Weiße' Blende)
"""
    
def Vollblende(rmin,rmax,l,verz,x0=304,y0=342,bol=True):
    if bol:
        col = 1
        img = Image.new('1',(608,684),'black')
    else:
        col = 0
        img = Image.new('1',(608,684),'white')
    r = np.linspace(rmin,rmax,l)
    pixels = img.load()
    num = range(0,l)
    for k in range(0,l):
        if k <10:
            name = verz+'INPUT_0'+str(num[k])+'.bmp'
        else:
            name = verz+'INPUT_'+str(num[k])+'.bmp'
        a,b,c,d = abcd(r[k],x0,y0)
        print(a,b,c,d)
        for i in range(a,b):
            for j in range(c,d):
                x,y = realxy(j-x0,i-y0)
                z = np.sqrt((x)**2+(y)**2)
                if z <= r[k]:
                    pixels[j,i] = col
        img.save(name)

#rl=np.linspace(45,563,20)
#ou=np.linspace(90,594,20)
#for i in range(0,20):
#    Blende(45,45,1,'RL_r45/'+str(int(rl[i])),rl[i],341)
#    Blende(45,45,1,'OU_r45/'+str(int(ou[i])),304,ou[19-i])


"""
Funktion zum erstellen von segmentiellen Kreisblenden
Anzahl der Segmente (gesamt)- seg (int) (Vielfaches von 2!)
Minimaler/Maximaler Radius in Spiegeleinheiten - rmin/rmax (float) (Default rmin=0)
phi0 - Startpunkt des ersten Sektors (Drehung des Koordinatensystems um phi0 math.pos.)
Füllparameter aktive Segmente - alpha (float: 0-2)
Nullpunkt - x0,y0 (int) (Default: x0=304,y0=342)
"""
def Segmentblende(seg,rmax,rmin=0,phi0=0,alpha=1,x0=304,y0=342):
    img = Image.new('1',(608,684),'black')
    pixels = img.load()
    delta = 2*np.pi/seg
    for s in range(0,seg):
        if s%2 == 0:
            a,b,c,d = abcd(rmax,x0,y0)
            for i in range(a,b):
                for j in range(c,d):
                    x,y = realxy(j-x0,y0-i)
                    z = np.sqrt((x)**2+(y)**2)
                    if y == 0 and x >= 0:
                        phi=0
                    elif y == 0 and x<0:
                        phi = np.pi
                    elif y >= 0:
                        phi = np.arccos(x/z)
                    elif y < 0:
                        phi = np.pi+np.arccos(-x/z)
                    if rmin <= z <= rmax and (s*delta + phi0) <= phi <= ((s+alpha)*delta+ phi0):
                        pixels[j,i] = 1                   
    img.save(str(rmax)+'_'+str(seg)+'_'+str(phi0)+'.bmp')
    # Sereturn(img)
"""
Methoden um eine dunkles Segment in einer Vollblende rotieren zu lassen.
rotate_help basiert dabei auf der Segmentbelden-Methode in leicht abgewandelter Form.
Die Methode rotate ruft diese auf, um die Bilder zu erzeugen.
step (int) - Anzahl der Schritte in der die Fehlstelle um 2pi rotiert
width (float) - Breite der Fehlstelle in rad
rmin/rmax (float) - wie bei Segmentbelden!
"""
def rotate_help(seg,rmax,rmin=0,phi0=0,alpha=1,x0=304,y0=342):
    img = Image.new('1',(608,684),'black')
    pixels = img.load()
    delta = 2*np.pi/seg
    for s in range(0,seg):
        if s%2 == 0:
            a,b,c,d = abcd(rmax,x0,y0)
            for i in range(a,b):
                for j in range(c,d):
                    x,y = realxy(j-x0,y0-i)
                    z = np.sqrt((x)**2+(y)**2)
                    if y == 0 and x >= 0:
                        phi=0
                    elif y == 0 and x<0:
                        phi = np.pi
                    elif y >= 0:
                        phi = np.arccos(x/z)
                    elif y < 0:
                        phi = np.pi+np.arccos(-x/z)
                    if rmin <= z <= rmax and (((s*delta + phi0)  <= phi <= ((s+alpha)*delta+ phi0)) or ((s*delta + phi0)  <= phi+2*np.pi <= ((s+alpha)*delta+ phi0))):
                        pixels[j,i] = 1              
                    # elif rmin <= z <= rmax and (s*delta + phi0)  <= phi+2*np.pi <= ((s+alpha)*delta+ phi0):
                    #     pixels[j,i] = 1                   
    # img.save(str(rmax)+'_'+str(seg)+'.bmp')
    return(img)
    
def rotate(seg=10,step=10,maxangle=2*np.pi,width=1.3,rmin=0,rmax=170):
    # alpha = width/np.pi
    for i in range(0,step):
        phi0 = maxangle/step *i
        img = rotate_help(seg,rmax,rmin,phi0,width)
        save(img,'INPUT3_'+str(i)+'.bmp')
        
"""
Funktion zum erstellen einer Ringblende mit variablen Radien
Minimaler/Maximaler Radius in Spiegeleinheiten - rmin/rmax (float)
Nullpunkt - x0,y0 (int) (Default: x0=304,y0=342)
Radius Punkt - rdot (float:0-rmin) (Default: rdot=0)
Mittelpunkt zeichnen? - dot (Boolean) (Default: dot=False)
"""
def Ringblende(rmin,rmax,x0=304,y0=342,rdot=0,dot=False):
    img = Image.new('1',(608,684),'black')
    pixels = img.load()
    a,b,c,d = abcd(rmax,x0,y0)
    for i in range(a,b):
        for j in range(c,d):
            x,y = realxy(j-x0,y0-i)
            z = np.sqrt((x)**2+(y)**2)
            if  rmin <= z <= rmax:
                pixels[j,i] = 1
            if dot:
                if z <= rdot:
                    pixels[j,i] = 1
    #img.save('test.bmp')#TODO: Korrekte Speicherfunktion
    return(img)#Mit save(pic,name) verwenden!!!
"""
Funktion zum Zeichnen einer Kreisblende an einem Bestimten Mittelpunkt
Bilddatei - im (image)
Radius der Blenden - r (float)
Nullpunkt - x0,y0 (int)
"""    
def circle(im,r,x0,y0):
    pix=im.load()
    a,b,c,d=abcd(r,x0,y0)
    for i in range(a,b):
        for j in range(c,d):
            x,y = realxy(j-x0,i-y0)
            z = np.sqrt((x)**2+(y)**2)
            if z <= r:
                pix[j,i] = 1

"""
Funktion zur Erstellung eines Gitters aus Kreisblenden auf Basis der circle-Funktion
Mittelpunkte - arr (Array) enthält die Mittelpunktstupel des Gitters
Radius der Blenden - r (float)
"""             
def Gitter(arr,r):
    img = Image.new('1',(608,684),'black')
    for i in range(0,len(arr)):
        x0=arr[i,0]
        y0=arr[i,1]
        circle(img,r,x0,y0)
    img.save('test.bmp')#TODO: Korrekte Speicherfunktion        
    
