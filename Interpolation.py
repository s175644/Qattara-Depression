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

plt.plot(t,Height)
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.show()

#Plotting bomb locations:
L = np.load("Locations.npy")
s=L*Height

plt.plot(t,Height)
plt.plot(t,s, "ro")
plt.xlabel('Distance in [km]')
plt.ylabel('Height in [m]')
plt.show()



