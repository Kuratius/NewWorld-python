import numpy as np

#import json
#mostly here so that I can use it to import jsons with monster stats later
from scipy import interpolate




#load attributescaling tables
#there's like a hundred different ways to compute attribute scaling,
#but the easiest is to just load it from the datamined files the way the game likely does
#for those who care: there's a few breakpoints for attribute scaling,  but it is linear in between
#so you can just map the breakpoints and linearly interpolate in between
strscaling = np.loadtxt('datasheets-csv-main/AttributeDefinition/Strength.csv',skiprows=1, usecols=(0,27),delimiter=",")
dexscaling = np.loadtxt('datasheets-csv-main/AttributeDefinition/Dexterity.csv',skiprows=1, usecols=(0,27),delimiter=",")
intscaling = np.loadtxt('datasheets-csv-main/AttributeDefinition/Intelligence.csv',skiprows=1, usecols=(0,26),delimiter=",")
focscaling = np.loadtxt('datasheets-csv-main/AttributeDefinition/focus.csv',skiprows=1, usecols=(0,29),delimiter=",")
healscaling = np.loadtxt('datasheets-csv-main/AttributeDefinition/focus.csv',skiprows=1, usecols=(0,27),delimiter=",")

strdmg=interpolate.interp1d(strscaling[:,0],strscaling[:,1])
dexdmg=interpolate.interp1d(dexscaling[:,0],dexscaling[:,1])
intdmg=interpolate.interp1d(intscaling[:,0],intscaling[:,1])
focdmg=interpolate.interp1d(focscaling[:,0],focscaling[:,1])
focheal=interpolate.interp1d(healscaling[:,0],healscaling[:,1])
statdmgfunctions=[strdmg,dexdmg,intdmg,focdmg]

def dmgstatScaling(stats, weights):
    #expects stats and weights to be vector of length 4
    #can probably work with 5 or 6, but the game doesnt have situations where that would matter yet 
    #(and we dont have dmg scaling tables for con for example)
    #will probably write separate implementation that works for entering multiple stat combinations simultaneously
    #
    assert len(stats)==len(weights)
    for stat in stats:
        assert stat>=5
    dmgsum=0
    for i in range(len(stats)):
        print(i)
        dmgsum+=statdmgfunctions[i](stats[i])*weights[i]
        
    return dmgsum/100
    
    
def gsMultiplier(GS):
    #computes the multiplier to the base damage of a weapon with fixed gs
    if 100<=GS<=500:
        return (1+0.0112)**np.floor((GS-100)/5)
    elif GS>500:
        return (1+0.0112)**80*(1+0.6667*0.0112)**np.floor((GS-500)/5)
    
    
    
def avgCritrate(p):
    #computes average crit rate with bad luck protection
    #assuming a basecritrate from gear of p
    mysum=0
    if p!=0:
        maxHits = int(np.ceil(1/p))
    else: 
        return 0
    for hits in range(1, maxHits + 1):
        def prod(start, end, p):
            product=1
            for m in range(start,end):
                product=product*(1 - (m*p))
            return product
        mysum += (hits) * prod(0, hits, p) * min(hits * p, 1)    # changed (hits * p) to min(hits * p, 1)
    return 1/mysum

#implement simulated version
def simulatecritchance(basecrit,N):
    #simulates the average crit chance using the bad luck protection system
    #mostly here for legacy purposes or if someone doesn't trust the math
    #recommend choosing N>=10000 for good results
    critnumber=0
    crit=basecrit
    for i in range(N):
        randomvalue=np.random.rand()

        if randomvalue<=crit:
            critnumber+=1
            crit=basecrit
        else:
            crit+=basecrit
    return critnumber/N





def armorScaling(armor, AWGS):
    #computes the armorscaling currently used in the game
    #AWGS is the gearscore of the attacker's weapon
    #1.2 isnt the exact number used by the game, it's actually something like 1.200009 or so
    #but the decimals rarely matter
    
    return 1/(1+armor/AWGS**1.2)

def levelscaling(level):
    return (level-1)*0.025


#todo
#def gemScaling(tier,stat)
#def totaldamage
#def mobscaling 
#def healing
