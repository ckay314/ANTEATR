import numpy as np
from funcANTEATR import getAT

getv = lambda x: 660*np.log10(x)-9475.
getAW = lambda x: 19.8*np.log10(x) - 270.
    
#masses = np.array([0.5,0.6,0.7,0.8,0.9,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,20.,30.,40.,50.])*1e15

#logmasses = np.linspace(14.7, 16.7, 30, endpoint=True)
logmasses = np.linspace(15, 16.7, 30, endpoint=True)
masses =  np.power(10, logmasses)

# invec = [Elat, Elon0, CMElat, CMElon, CMEtilt, CMEvel0 (5), CMEmass, CMEAW, CMEA, CMEB, vSW, SWrho0, Cd]
invec = [0.,0.,0.,0.,90.,500.,1., 30., 0.75, 0.55, 440., 6.9, 1.]
    
counter = 0
for mass in masses:
#for ii in range(1):
    #mass = masses[0]
    invec[5] = getv(mass) 
    invec[6] = mass/1e15
    invec[7] = getAW(mass)
    origvec = invec
    print invec[5], invec[6], invec[7], getAT(invec,20)
    
    # need to calculate width in poloidal dir
    CMEB = invec[9]
    CMEAW = invec[7]*3.14159/180.
    CMEA = invec[8]
    CdivR = np.tan(CMEAW) / (1. + CMEB + np.tan(CMEAW) * (CMEA + CMEB))
    rnose = 213
    CtimesR = CdivR * rnose
    Bdist = CMEB*CtimesR
    maxPang = np.arctan(Bdist/(rnose-(CMEB)*CtimesR))*180/3.14159
    #print mass, maxPang, invec[7], Bdist, CtimesR, CdivR
    
    # CME lat
    #newlats = [maxPang*(i - 1)/10. for i in range(21)]
    newlats = 0.95*np.linspace(-maxPang, maxPang, 21)
    #print newlats
    #print newlats
    #print mass/1e15, newlats
    outstr = ''
    for lat in newlats:
        invec[2] = lat
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '0 ' + outstr
    invec[2] = newlats[10]
    
    # CME lon
    #newlons = [i - 10 for i in range(21)]
    newlons = 0.99*np.linspace(-invec[7], invec[7],21)
    #print newlons
    outstr = ''
    for lon in newlons:
        invec[3] = lon
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '1 ' + outstr
    invec[3] = newlons[10]
    
    # CME vel
    #newvels = [invec[5] + 10*i - 100 for i in range(21)]
    newvels = np.linspace(0.5*invec[5],1.5*invec[5],21)
    outstr = ''
    for vel in newvels:
        invec[5] = vel
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '2 ' + outstr
    invec[5] = newvels[10]
    
    # CME mass
    thismass = invec[6]
    newmass = [(0.05*i + 0.5)*thismass for i in range(21)]
    outstr = ''
    for mass in newmass:
        invec[6] = mass
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '3 ' + outstr
    invec[6] = newmass[10]

    # CME AW
    #newAWs = [invec[7] + i - 10  for i in range(21)]
    newAWs = np.linspace(0.5*invec[7],1.5*invec[7],21)
    outstr = ''
    for AW in newAWs:
        invec[7] = AW
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '4 ' + outstr
    invec[7] = newAWs[10]
    
    # SW v
    newSWvs = [invec[10] + 10*i - 100 for i in range(21)]
    outstr = ''
    for vel in newSWvs:
        invec[10] = vel
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '5 ' + outstr
    invec[10] = newSWvs[10]
    
    # SW rho
    newSWrhos = [invec[11] + 0.5*i - 5 for i in range(21)]
    outstr = ''
    for rho in newSWrhos:
        invec[11] = rho
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '6 ' + outstr
    invec[11] = newSWrhos[10]
    
    # Cd
    newCds = [0.1*i for i in range(21)]
    outstr = ''
    for Cd in newCds:
        invec[12] = Cd
        time, speed = getAT(invec,20)
        outstr = outstr + '{:8.3f}'.format(time) + ' '
    print str(counter) + '7 ' + outstr
    invec[12] = newCds[10]
    
    counter += 1
    
# if you are reading this, yes I got lazy and copy/pasted from terminal 
# instead of saving to a file
    