import numpy as np
import os,sys,time,datetime,gzip
import argparse

def infoLine(message,infoType="info"):
    infoType = infoType.upper()
    if len(infoType) < 5:
        infoType=infoType + " "
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    outline = "[" + infoType + " " + str(time) + "] " + message
    print(outline)

    if infoType == "ERROR":
        sys.exit()
#

def computeDensity(infile, outfile):
    smtHash = {}
    tfHash  = {}
    
    with gzip.open(infile, "rt") as fi:
        for line in fi:
            row   = line.rstrip().split("\t")
            smt   = "|".join(row[:3])
            tfname= row[7]
            if smt not in smtHash:
                smtHash[smt] = {}
            #
            smtHash[smt][tfname] = ""
            
            if tfname not in tfHash:
                tfHash[tfname] = {}
            #
            tfHash[tfname][smt] = ""
    #
    
    for smt in smtHash:
        smtHash[smt] = len(smtHash[smt])
    #
    
    with open(outfile, "wt") as fo:
        fo.write( "TFName\tmean\tstd\tinfo\n" )
        for tfname in tfHash:
            vlist = [ smtHash[smt] for smt in tfHash[tfname] ]
            mean  = np.mean(vlist)
            std   = np.std(vlist)
            vlist = [str(k) for k in vlist]
            
            outline= tfname + "\t" + "{:.2f}".format(mean) + "\t" + "{:.2f}".format(std) + "\t" + "|".join(vlist)
            fo.write( outline + "\n" )
    #
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description: analyze TF density profile",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", dest="infile",    type=str,   required=True,  help="The path of annotated summit file")
    parser.add_argument("-o", dest="outfile",   type=str,   required=True,  help="The path of output file")
    
    args=parser.parse_args()
    
    infile   = args.infile
    outfile  = args.outfile
    
    infoLine("Compute TF density")
    computeDensity(infile, outfile)
    
    infoLine('Done!')
#