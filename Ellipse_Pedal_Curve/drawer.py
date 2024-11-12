from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import numpy as np
import math

def drawer(x,qx,ids,ij,rely=95):
    ixy  = np.concatenate((ids,np.concatenate((x[0:x.shape[0]/2],x[x.shape[0]/2:x.shape[0]]),axis=1)),axis=1)
    condition = raw_input('R  or  ABS: ')

    while(1):

        if condition=='ABS':
            #Absolute drawing
            for i in range(ixy.shape[0]):
                #find eig
                fig = plt.figure(1)
                a = np.matrix([[qx[i,i],qx[i,i+ixy.shape[0]]],[qx[i+ixy.shape[0],i],qx[i+ixy.shape[0],i+ixy.shape[0]]]])
                v,w = np.linalg.eig(a)
                v[0:2] = math.sqrt(v[0]),math.sqrt(v[1])

                si = 0.5*math.atan(2*a[0,1]/(a[0,0]-a[1,1]))
                #print si*180/math.pi

                #draw ellipse
                e = Ellipse((ixy[i,1],ixy[i,2]),150*2.45*2*v[0],150*2.45*2*v[1],si*180/math.pi)
                b = plt.subplot(111, aspect='equal')
                e.set_clip_box(b.bbox)
                e.set_alpha(0.3)
                b.add_artist(e)

                #draw pedal
                theta = np.linspace(0, np.pi*2, 50)
                r = 2.45*np.sqrt((a[0,0]*np.cos(theta)**2+a[1,1]*np.sin(theta)**2)+(2*a[0,1]*np.sin(theta)*np.cos(theta)))
                plt.subplot(111, aspect='equal')
                plt.plot(ixy[i,1] + 150*r*np.cos(theta),ixy[i,2]+ 150*r*np.sin(theta),'r')

                #print label
                plt.text(ixy[i,1],ixy[i,2], str(int(ixy[i,0])), style='italic',
                        bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
            break

        elif condition=='R':
            #realtive drawing
            Jacob = np.matrix([[-1,1,0,0],[0,0,-1,1]])
            for rij in ij:
                i = rij[0]
                j = rij[1]

                i = int(np.where(ixy[:,0]==i)[0])
                j = int(np.where(ixy[:,0]==j)[0])

                L = qx.shape[0]/2
                qxR = np.matrix([[qx[i,i],qx[i,j],qx[i,i+L],qx[i,j+L]],
                                 [qx[j,i],qx[j,j],qx[j,i+L],qx[j,j+L]],
                                 [qx[i+L,i],qx[i+L,j],qx[i+L,i+L],qx[i+L,j+L]],
                                 [qx[j+L,i],qx[j+L,j],qx[j+L,i+L],qx[j+L,j+L]]])
                qdx = Jacob*qxR*Jacob.transpose()
               # print qdx

                # find eig
                fig = plt.figure(1)
                a = qdx
                v, w = np.linalg.eig(a)
                v[0:2] = math.sqrt(v[0]), math.sqrt(v[1])

                si = 0.5 * math.atan(2 * a[0, 1] / (a[0, 0] - a[1, 1]))
               # print si * 180 / math.pi

                # draw ellipse
                e = Ellipse(((ixy[i, 1]+ixy[j, 1])/2, (ixy[i, 2]+ixy[j, 2])/2), 150 * 2.45 * 2 * v[0], 150 * 2.45 * 2 * v[1], si * 180 / math.pi)
                b = plt.subplot(111, aspect='equal')
                e.set_clip_box(b.bbox)
                e.set_alpha(0.2)
                b.add_artist(e)

                # draw pedal
                theta = np.linspace(0, np.pi * 2, 50)
                r = 2.45 * np.sqrt(
                    (a[0, 0] * np.cos(theta) ** 2 + a[1, 1] * np.sin(theta) ** 2) + (2 * a[0, 1] * np.sin(theta) * np.cos(theta)))
                plt.subplot(111, aspect='equal')
                plt.plot((ixy[i, 1]+ixy[j, 1])/2 + 150 * r * np.cos(theta), (ixy[i, 2]+ixy[j, 2])/2 + 150 * r * np.sin(theta), 'r')

                plt.subplot(111, aspect='equal')
                plt.plot([ixy[i, 1] , ixy[j, 1]] , [ixy[i, 2] ,ixy[j, 2]] ,'b')

                # print label
                plt.text((ixy[i, 1]+ixy[j, 1])/2, (ixy[i, 2]+ixy[j, 2])/2, str(int(ixy[i, 0]))+' - '+str(int(ixy[j, 0])), style='italic',
                         bbox={'facecolor': 'green', 'alpha': 0.2, 'pad': 6})
            break

    #set BBOX
    bboxx = [ixy[0,1]-90,ixy[0,1]+90]
    bboxy = [ixy[0,2]-90,ixy[0,2]+90]
    plt.xlim(bboxx[0],bboxx[1])
    plt.ylim(bboxy[0],bboxy[1])

    #show resualt
    plt.grid()
    plt.show()



