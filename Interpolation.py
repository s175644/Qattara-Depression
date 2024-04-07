import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as syi

#Contains data about points along the channel
#Columns are latitude, longitude and height
D = np.loadtxt("channel_data.txt")

Distance = []
Distanceh = []
xdata = [0]
R = 6371000
x=0

for i in range(len(D)-1):
    #Converting to radians
    lat1=D[i,0]*np.pi/180
    lat2=D[i+1,0]*np.pi/180
    long1=D[i,1]*np.pi/180
    long2=D[i+1,1]*np.pi/180
    
    #Calculating distance between each point:
    kat1 = 2*R*np.arcsin(np.sqrt(np.sin((lat2-lat1)/2)**2+np.cos(lat1)*np.cos(lat2)*np.sin((long2-long1)/2)**2)) 
    Distance.append(kat1) 
        
    #Calculating distance between each point with the height included:
    # final_dis=np.sqrt(kat1**2+(abs(D[i+1,2]-D[i,2]))**2)
    # Distanceh.append(final_dis)
    
    #x coordinate for the heights
    x += kat1/1000
    xdata.append(x)

Ifunc = syi.interp1d(xdata, D[:,2])
t = np.arange(0,xdata[-1],250/1000)
Height = Ifunc(t)
np.save("Height data.npy", Height)

###Plotting height for question 2:
plt.plot(t,Height)
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Plotting height vs channel length [question 2]")
plt.show()

###Plotting bomb locations for question 3:
L = np.load("Locations3.npy")
CD3 = np.load("ChannelDepth3.npy")
s=L*Height
BL=np.vstack((t,s))
Del=[]

for i in range(len(L)):
    if L[i]==0:
        Del.append(i)

FBL=np.delete(BL, Del, axis=1)

plt.plot(t,Height)
plt.plot(FBL[0,:],FBL[1,:], "ro")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Bomb locations along channel [question 3]")
plt.show()

#Ploting channel depth:
depth3=Height-CD3
plt.plot(t,Height)
plt.plot(t,depth3, "r")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Channel smoothness [question 3]")
plt.show()

###Plotting bomb locations and channel depth for question 4:
#First plotting bomb locations:
L4 = np.load("Locations4.npy")
CD4 = np.load("ChannelDepth4.npy")
print("Number of bombs used, Q4: ", sum(L4))

s4=L4*Height
BL4=np.vstack((t,s4))
Del4=[]

for i in range(len(L4)):
    if L4[i]==0:
        Del4.append(i)

FBL4=np.delete(BL4, Del4, axis=1)

plt.plot(t,Height)
plt.plot(FBL4[0,:],FBL4[1,:], "ro")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Bomb locations along channel [question 4]")
plt.show()

#Ploting channel depth:
depth4=Height-CD4
plt.plot(t,Height)
plt.plot(t,depth4, "r")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Channel smoothness [question 4]")
plt.show()

###Plotting bomb location and channel depth for question 5:
L5 = np.load("Locations5.npy")
CD5 = np.load("ChannelDepth5.npy")
print("Number of bombs used, Q5: ", sum(L5))

s5=L5*Height
BL5=np.vstack((t,s5))
Del5=[]

for i in range(len(L5)):
    if L5[i]==0:
        Del5.append(i)

FBL5=np.delete(BL5, Del5, axis=1)

plt.plot(t,Height)
plt.plot(FBL5[0,:],FBL5[1,:], "ro")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Bomb locations along channel [question 5]")
plt.show()

#Ploting channel depth:
depth5=Height-CD5
plt.plot(t,Height)
plt.plot(t,depth5, "r")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Channel smoothness [question 5]")
plt.show()

###Plotting bomb location and channel depth for question 6:
L6s = np.load("Locations6(50).npy")
#L6e = np.load("Locations6(End30).npy")
CD6s = np.load("ChannelDepth6(50).npy")
#CD6e = np.load("ChannelDepth6(End30).npy")
sta=0
#sta=len(Height)-len(L6s)
p=len(L6s)
#p=len(Height)
print("Number of bombs used, Q6: ", sum(L6s))

s61=L6s[:,0]*Height[sta:p]
s62=L6s[:,1]*Height[sta:p]
#s63=L6s[:,2]*Height[sta:p]
BL61=np.vstack((t[sta:p],s61))
BL62=np.vstack((t[sta:p],s62))
#BL63=np.vstack((t[sta:p],s63))
Del61=[]
Del62=[]
#Del63=[]

for i in range(len(L6s)):
    if L6s[i,0]==0:
        Del61.append(i)

for i in range(len(L6s)):
    if L6s[i,1]==0:
        Del62.append(i)

# for i in range(len(L6s)):
#     if L6s[i,2]==0:
#         Del63.append(i)
        
FBL61=np.delete(BL61, Del61, axis=1)
FBL62=np.delete(BL62, Del62, axis=1)
#FBL63=np.delete(BL63, Del63, axis=1)

plt.plot(t[sta:p],Height[sta:p])
plt.plot(FBL61[0,:],FBL61[1,:], "ro")
plt.plot(FBL62[0,:],FBL62[1,:], "go")
#plt.plot(FBL63[0,:],FBL63[1,:], "mo")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Bomb locations along channel [question 6, first half]")
plt.show()

#Ploting channel depth:
depth6=Height[sta:p]-CD6s
plt.plot(t[sta:p],Height[sta:p])
plt.plot(t[sta:p],depth6, "r")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Channel smoothness [question 6, first half]")
plt.show()


###Plotting bomob location and channel depth for change in yield setting:
L7 = np.load("Locations6NewSet(50).npy")
CD7 = np.load("ChannelDepth6NewSet(50).npy")
p2=len(L7)
print("Number of bombs used, Q6, new settings: ", sum(L7))

s71=L7[:,0]*Height[0:p2]
s72=L7[:,1]*Height[0:p2]
s73=L7[:,2]*Height[0:p2]
BL71=np.vstack((t[0:p2],s71))
BL72=np.vstack((t[0:p2],s72))
BL73=np.vstack((t[0:p2],s73))
Del71=[]
Del72=[]
Del73=[]

for i in range(len(L7)):
    if L7[i,0]==0:
        Del71.append(i)

for i in range(len(L7)):
    if L7[i,1]==0:
        Del72.append(i)

for i in range(len(L7)):
    if L7[i,2]==0:
        Del73.append(i)
        
FBL71=np.delete(BL71, Del71, axis=1)
FBL72=np.delete(BL72, Del72, axis=1)
FBL73=np.delete(BL73, Del73, axis=1)

plt.plot(t[0:p2],Height[0:p2])
plt.plot(FBL71[0,:],FBL71[1,:], "ro")
plt.plot(FBL72[0,:],FBL72[1,:], "go")
plt.plot(FBL73[0,:],FBL73[1,:], "yo")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Bomb locations along channel [New setting, first half]")
plt.show()

#Ploting channel depth:
depth7=Height[0:p2]-CD7
plt.plot(t[0:p2],Height[0:p2])
plt.plot(t[0:p2],depth7, "r")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.title("Channel smoothness [New setting, first half]")
plt.show()