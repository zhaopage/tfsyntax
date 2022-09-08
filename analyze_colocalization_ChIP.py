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

def computeColocalization(infile, prefix):
    tabFile = prefix + ".tab"
    matFile = prefix + ".mat"

    tfHash   = {}
    colHash  = {}
    tfList   = []
    
    with gzip.open(infile, "rt") as fi:
        for line in fi:
            row = line.rstrip().split("\t")
            tfname = row[3]
            pos    = "|".join(row[:3])
            target = row[7]
            
            if tfname not in tfHash:
                tfHash[tfname] = {}
            #
            if pos not in tfHash[tfname]:
                tfHash[tfname][pos] = {}
            #
            tfHash[tfname][pos][target] = ""
    #
    
    tfList = sorted( list(tfHash.keys()) )
    for tfname in tfList:
        colHash[tfname] = {}
        total = len( tfHash[tfname] )
        for target in tfList:
            count = 0
            for pos in tfHash[tfname]:
                if target in tfHash[tfname][pos]:
                    count = count + 1
            #
            colHash[tfname][target] = "{:.2f}".format(count * 100 /total)
    #

    with open( tabFile, "wt" ) as fo:
        fo.write( "primary\tassociated\tcolocalization_score\n" )
        for tfname in tfList:
            for target in tfList:
                outline = tfname + "\t" + target + "\t" + colHash[tfname][target]
                fo.write( outline + "\n" )
    #

    with open( matFile, "wt" ) as fo:
        fo.write( "TFName\t" + "\t".join( tfList ) + "\n" )
        for tfname in tfList:
            outline = tfname
            for target in tfList:
                if target in colHash[tfname]:
                    outline = outline + "\t" + colHash[tfname][target]
                else:
                    outline = outline + "\t" + "0.0"
            #
            fo.write( outline + "\n" )                    
    #   
#


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description: analyze TF colocalization profile for ChIP-Seq data",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", dest="infile",    type=str,   required=True,  help="The path of annotated summit file")
    parser.add_argument("-o", dest="prefix",    type=str,   required=True,  help="The path of output file")
    
    args=parser.parse_args()
    
    infile   = args.infile
    prefix   = args.prefix
    
    infoLine("Compute TF colocalization")
    computeColocalization(infile, prefix)
    
    infoLine('Done!')
#