import numpy as np
import math
import sys

global rsun, dtor, radeg, kmRs
rsun  =  7e10		 # convert to cm, 0.34 V374Peg
dtor  = 0.0174532925  # degrees to radians
radeg = 57.29577951    # radians to degrees
kmRs  = 1.0e5 / rsun # km (/s) divided by rsun (in cm)


#-----------geometry functions ------------------------------------

def SPH2CART(sph_in):
    r = sph_in[0]
    colat = (90. - sph_in[1]) * dtor
    lon = sph_in[2] * dtor
    x = r * np.sin(colat) * np.cos(lon)
    y = r * np.sin(colat) * np.sin(lon)
    z = r * np.cos(colat)
    return [x, y, z]

def CART2SPH(x_in):
# calcuate spherical coords from 3D cartesian
# output lat not colat
    r_out = np.sqrt(x_in[0]**2 + x_in[1]**2 + x_in[2]**2)
    colat = np.arccos(x_in[2] / r_out) * 57.29577951
    lon_out = np.arctan(x_in[1] / x_in[0]) * 57.29577951
    if lon_out < 0:
        if x_in[0] < 0:
            lon_out += 180.
        elif x_in[0] > 0:
            lon_out += 360. 
    elif lon_out > 0.:
	    if x_in[0] < 0:  lon_out += 180. 
    return [r_out, 90. - colat, lon_out]

def rotx(vec, ang):
# Rotate a 3D vector by ang (input in degrees) about the x-axis
    ang *= dtor
    yout = np.cos(ang) * vec[1] - np.sin(ang) * vec[2]
    zout = np.sin(ang) * vec[1] + np.cos(ang) * vec[2]
    return [vec[0], yout, zout]

def roty(vec, ang):
# Rotate a 3D vector by ang (input in degrees) about the y-axis
    ang *= dtor
    xout = np.cos(ang) * vec[0] + np.sin(ang) * vec[2]
    zout =-np.sin(ang) * vec[0] + np.cos(ang) * vec[2]
    return [xout, vec[1], zout]

def rotz(vec, ang):
# Rotate a 3D vector by ang (input in degrees) about the y-axis
	ang *= dtor
	xout = np.cos(ang) * vec[0] - np.sin(ang) * vec[1]
	yout = np.sin(ang) * vec[0] + np.cos(ang) * vec[1]
	return [xout, yout, vec[2]]

# -------------- main function ------------------
'''try:
    Elat      = float(sys.argv[1])
    Elon0     = float(sys.argv[2])
    CMElat    = float(sys.argv[3])
    CMElon    = float(sys.argv[4])
    CMEtilt   = float(sys.argv[5])  # forecat tilt, wrt to N not E
    CMEvel0   = float(sys.argv[6]) * 1e5    # convert to cm/s
    CMEmass   = float(sys.argv[7]) * 1e15   # convert to g
    CMEAW     = float(sys.argv[8]) * dtor  # convert to radians
    CMEA      = float(sys.argv[9])
    CMEB      = float(sys.argv[10])
    vSW       = float(sys.argv[11]) * 1e5   # convert to cm/s
    SWrho0    = float(sys.argv[12]) * 1.67e-24 # in g (just missing expo factor before) 
    Cd        = float(sys.argv[13])
except:
    sys.exit('only '+str(len(sys.argv)-1)+' inputs given, need 14 (Elat Elon0 tGCS t20 CMEv CMEM CMEAW CMEA CMEB vSW SWrho0 )')

invec = [Elat, Elon0, CMElat, CMElon, CMEtilt, CMEvel0, CMEmass, CMEAW, CMEA, CMEB, vSW, SWrho0, Cd]'''
def getAT(invec, rCME):
    
    Elat      = invec[0]
    Elon0     = invec[1]
    CMElat    = invec[2]
    CMElon    = invec[3]
    CMEtilt   = invec[4]
    CMEvel0   = invec[5] * 1e5
    CMEmass   = invec[6] * 1e15
    CMEAW     = invec[7] * dtor
    CMEA      = invec[8]
    CMEB      = invec[9]
    vSW       = invec[10] * 1e5
    SWrho0    = invec[11] * 1.67e-24
    Cd        = invec[12]    

    CdivR = np.tan(CMEAW) / (1. + CMEB + np.tan(CMEAW) * (CMEA + CMEB))

    Erotrate = 360/365./24/60. # deg per min
    # start w/o Earth rot so not considering changes in Elon due to diff in transit time
    Erotrate = 0.
    
    # calculate E rot between C2 and 20 Rs
    #dElon1 = (t20-tGCS) * Erotrate

    #rCME = 20.
    vCME = CMEvel0
    Elon = Elon0
    
    dt = 1
    t  = 0
    # run CME nose to 1 AU
    while rCME <= 213.:
        t += dt
        rCME += vCME*dt*60/7e10 
        CtimesR = CdivR * rCME
        rcent = rCME - (CMEA+CMEB) * CtimesR
        CMEarea = 4*CMEB*CtimesR**2 * (7e10)**2
        SWrho = SWrho0 * (213./rcent)**2
        dV = -Cd * CMEarea * SWrho * (vCME-vSW) * np.abs(vCME-vSW) * dt * 60 / CMEmass
        vCME += dV
        Elon += Erotrate * dt
        #print rCME, vCME/1e5
        #if rCME < 25: print CMEarea, CMEB, CtimesR, rCME
    #print CMEarea
    inCME = False
    prevmin = 9999.
    while not inCME:
        t += dt
        rCME += vCME*dt*60/7e10 
        CtimesR = CdivR * rCME
        rcent = rCME - (CMEA+CMEB) * CtimesR
        CMEarea = 4*CMEB*CtimesR**2 * (7e10)**2
        SWrho = SWrho0 * (213/rcent)**2
        dV = -Cd * CMEarea * SWrho * (vCME-vSW) * np.abs(vCME-vSW) * dt * 60 / CMEmass
        vCME += dV
        Elon += Erotrate * dt

        thetas = np.linspace(-math.pi/2, math.pi/2,1001)
        Epos1 = SPH2CART([213,Elat,Elon])
        temp = rotz(Epos1, -CMElon)
        temp2 = roty(temp, CMElat)
        Epos2 = rotx(temp2, CMEtilt)

        xFR = rcent + CMEA*CtimesR*np.cos(thetas)
        zFR = CtimesR * np.sin(thetas) 
        dists2 = ((Epos2[0] - xFR)**2 + Epos2[1]**2 + (Epos2[2] - zFR)**2) / (CMEB*CtimesR)**2
        CAang = thetas[np.where(dists2 == np.min(dists2))]
        thismin = np.min(dists2)
        #print thismin, rCME, Epos2, Elat, Elon
        if thismin < 1:
            TT = t/60./24.
            #print 'Transit Time:     ', TT
            #print 'Final Velocity:   ', vCME/1e5
            #print 'CME nose dist:    ', rCME
            #print 'Earth longitude:  ', Elon
            #print Elon, rCME, vCME/1e5#,CAang[0]/dtor, np.tan(Epos2[1]/(CMEB*CtimesR))/dtor
            #print CAang[0]/dtor
            inCME = True
            return TT, vCME/1e5         
        elif thismin < prevmin:
            prevmin = thismin
        else:
            return 9999, -9999

#invec = [-2.7,0.,-15.,-45.,35.,800.,1., 80., 0.8, 0.7, 375, 3, 0.8]               
#print getAT(invec, 21.5)
#invec = [0,0.,0.,0.,90.,1200.,5./2, 40., 0.75, 0.35, 440., 6.9, 0.5]               
#print getAT(invec, 20.)
