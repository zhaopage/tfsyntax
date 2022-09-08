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



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description: Filter expressed TFs",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", dest="infile",    type=str,   required=True,  help="The path of annotated summit file")
    parser.add_argument("-e", dest="expFile",   type=str,   required=True,  help="The path of expressed TFs")
    parser.add_argument("-o", dest="outfile",   type=str,   required=True,  help="The path of output files")
    
    args=parser.parse_args()
    
    infile = args.infile
    expFile= args.expFile
    outfile= args.outfile
    
    tfHash = {}
    
    infoLine("Reading expressed TFs")
    with open(expFile, "rt") as fi:
        for line in fi:
            line= line.rstrip()
            tfHash[line] = ""
    #
    infoLine("There are " + str(len(tfHash)) + " expressed TFs.")
    
    
    infoLine("Filtering data")
    with gzip.open(infile, "rt") as fi:
        with gzip.open(outfile, "wt") as fo:
            for line in fi:
                row = line.rstrip().split("\t")
                if row[4] == ".":
                    continue
                #
                
                if row[7] in tfHash:
                    fo.write( "\t".join( row[:8] ) + "\n" )
    #
    infoLine("Done!")
#

