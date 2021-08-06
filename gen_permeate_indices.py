"""
Add the atom indices corresponing to atoms with minimim z-coordinate value
"""

import os
import sys
import numpy as np
import pandas as pd
import re

def adjust_coordinates(filename,outfile):
    
    try:
        print("Opening file...\n ",filename)
        f=open(filename)

    except IOError as e:
        print("Unable to open" + filename +". Please check the file")
   
    #Load coordinates in pandas dataframe
    coord=[]
    box=[] 
    n_atoms=0
    for idx,line in enumerate(f):
        if idx==1:
            n_atoms=int(line.split()[0])
        if idx>=2:
            parts=line.split()
            if len(parts)==6:
                coord.append([parts[0],parts[1],parts[2],float(parts[3]),float(parts[4]), float(parts[5])])
            elif len(parts)==5:
                 coord.append([parts[0],parts[1][0:-5],parts[1][-5:],float(parts[2]),float(parts[3]), float(parts[4])])
            elif len(parts)==3:
                box.append([parts[0],parts[1], parts[2]])

    box_x=float(box[0][0])
    box_y=float(box[0][1])
    print("Box dimensions:",box_x,box_y)
    labels=["resid","atom_type","index","x","y","z"]
    df=pd.DataFrame(coord,columns=labels)
    df.astype({'x': 'float64'}).dtypes
    df.astype({'y': 'float64'}).dtypes 
    df.astype({'z': 'float64'}).dtypes
    pd.set_option('display.max_rows',df.shape[0]+1)

    
    #Find the maximum of polymer atoms

    polymer=df.loc[df['resid'].str.contains("MPD|TMC", case=False)]
    max_polymer=polymer["z"].max()

    sol=df.loc[df['resid'].str.contains("SOL", case=False)]
    feed=sol[sol.z>max_polymer]['index']
    

    
    #Sort the atoms according to the Z-coordinates
    #Save the indices of selected atoms in the index file
    o=open("equil-pacxb-wall.ndx","a+")
    o.write("\n")
    o.write("[ FeedWater ]\n")
    j=0
    for i in feed:
        o.write(i+" ")
        j+=1 
        if j ==15:
           o.write("\n")
           j=0
    f.close()
    o.close()

   
if __name__ == "__main__":
    adjust_coordinates(filename="test.gro", outfile="indices.txt")


