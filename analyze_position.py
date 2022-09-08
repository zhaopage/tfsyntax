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

def analyzeFactorPosition(infile, outfile):
    dataHash = {}
    posHash = {}
    tf2SummitHash = {}
    
    # read data by summit
    with gzip.open(infile, "rt") as fi:
        for line in fi:
            line = line.rstrip()
            row = line.split("\t")
            
            summitPos  = int( 0.5 * (int(row[1]) + int(row[2]) + 1) )
            motif_start= int(row[5]) - summitPos
            motif_end  = int(row[6]) - summitPos
            
            if len(row) >=9 and row[8] == "-":
                motif_start= summitPos - int(row[6])
                motif_end  = summitPos - int(row[5])
            else:
                motif_start= int(row[5]) - summitPos
                motif_end  = int(row[6]) - summitPos
            
            loc = str(motif_start) + "," + str(motif_end)
            factorName = row[7]
            if factorName not in posHash:
                posHash[factorName] = []
                tf2SummitHash[factorName] = {}
            posHash[factorName].append(loc)
            tf2SummitHash[factorName][row[3]] = ""

    # output position
    with open(outfile,"wt") as fo:
        factorlist = list(posHash.keys())
        factorlist.sort()
        for factorName in factorlist:
            fo.write( factorName + "\t" + str( len( tf2SummitHash[factorName] ) ) + "\t" + "|".join( posHash[factorName] ) + "\n" )
#


def computeCoverageByPosition(infile, outfile):
    winSize = 401
    itvHash = {}
    sp = 0 - int(0.5 * winSize)
    ep = int(0.5 * winSize)
    
    
    # read intervals by TFs
    with open(infile, "rt") as fi:
        for line in fi:
            row    = line.rstrip().split("\t")
            tfname = row[0]
            itvHash[tfname] = row[2].split("|")
    #
    
    with open(outfile, "wt") as fo:
        fo.write( "TFName\t" + "\t".join([str(k) for k in range(sp, ep + 1) ]) + "\n")
        
        for tfname in itvHash:
            posHash = {}
            for k in range( sp, ep + 1 ):
                posHash[k] = 0
            #
            for itv in itvHash[tfname]:
                locList = [int(k) for k in itv.split(",")]
                for k in range( locList[0] + 1 , locList[1] + 1 ):
                    if k >= sp and k <= ep:
                        posHash[k] = 1 + posHash[k]
            #
            pctList = [ "{:.2f}".format(posHash[k] * 100 / len(itvHash[tfname])) for k in range(sp, ep + 1) ]
            fo.write(tfname + "\t" + "\t".join(pctList) + "\n")
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description: analyze TF positional profile",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", dest="infile",    type=str,   required=True,  help="The path of annotated summit file")
    parser.add_argument("-o", dest="outprefix", type=str,   required=True,  help="Prefix of output files")
    
    args=parser.parse_args()
    
    infile    = args.infile
    outprefix = args.outprefix
    
    relativePosFile = outprefix + ".relative_position.tab"
    positionPctFile = outprefix + ".coverage_percentage.tab"
    
    infoLine("Compute relative position of each TF binding site")
    analyzeFactorPosition(infile, relativePosFile)
    
    infoLine("Compute TF coverage on each position")
    computeCoverageByPosition(relativePosFile, positionPctFile)
    
    infoLine('Done!')
#