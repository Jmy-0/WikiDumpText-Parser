from distutils.log import error
import time
import datetime
import cProfile
from urllib import parse as urlp
from parse import *
import math
from pyparsing import anyCloseTag
def findAnchor(anchorText, links:dict):
    
    with open("allLinks_lowerURL","r",encoding="UTF-8") as f:
        fReadLine = f.readline
        while(True):
            line = fReadLine()
            
            if not line:
                break
                
            line = line.split("\t\t")
            link = line[0]
            anchor = line[1].replace('\n','')
            
            if anchor == anchorText:
                try:
                    links[link][1]+=1
                except KeyError:
                    links[link] = [-1,1]


    print(links)

def getID(links:dict):
    l = len(links)
    count =0
    maxId = -1
    check = 0
    with open("titles", "r",encoding="UTF-8") as f:
        fReadLine = f.readline
        while(True):
            line = fReadLine()
            if not line:
                break

            parsed = parse('id={}_url=?curid={}_title={}\n', line)
            pTitle = parsed.fixed[2].lower()
            try:
                check = links[pTitle][0]
                links[pTitle][0] = int(parsed.fixed[0])
                maxId = links[pTitle][0]
                if check ==-1:
                    count+=1
            except KeyError:
                continue

            if count == l:
                break
    print(links)
    return maxId

def calcRedirect(links:dict, maxId):
    cp = links.copy()
    count =0
    with open("allRedirect", "r", encoding="UTF-8") as f:
        fReadLine = f.readline
        while(True):
            count++1
            line = fReadLine()
            if not line:
                break
            
            parsed = parse("id:_{}_namespace:_{}_title:_{}\n", line)
            try:
                id = int(parsed.fixed[0])
            except AttributeError:
                print("line")
                print("LINE:"+str(count))
            if id > maxId:
                break
            for i in cp:
                if cp[i][0] == id:
                    title = parsed.fixed[2].lower()
                    if i == title:
                        continue
                    try:
                        links[title][1] += links[i][1]
                    except KeyError:
                        links[title] = [-1,links[i][1]]
                    del links[i]

                    
    print(links)
                    


def tf():
    li = []
    an = []
    with open("allLinks","r",encoding="UTF-8") as f:
        while(True):
            line = f.readline()
            
            if not line:
                break
            if line =='\n' or line.find("<doc") >-1:
                continue
                
            line = line.split("\t\t")
            link = urlp.unquote(line[0]).lower()
            link = link.replace(' ','_')
            anchor = line[1].replace('\n','')
            if link.find('\n') > -1:
                link = link.replace('\n','')
            li.append(link)
            an.append(anchor)
    print("half")
    with open("allLinks_lowerURL","w",encoding="UTF-8") as of:
        for i in range(len(li)):
            of.write(li[i] + "\t\t"+an[i]+"\n")

def calcEntrophy(links:dict):
    sum = 0.0
    n = 0
    lg = math.log2
    for i in links:
        n+=links[i][1]

    for i in links:
        sum -= (links[i][1]/n)* lg(links[i][1]/n)

    print("entrophy: %lf"%(sum))
def main():
    links = dict()
    print("find anchor")
    findAnchor("Blood",links)
    # links["rainbow_trout"]=[1830128,155]
    # links["rainbow"]=[6721504,313]
    # links["rainbow_covenant"]=[40689752,1]
    # links["continuum_(spectrum)"]=[55997534,1]
    # links["rainbow_flag_(lgbt_movement)"]=[62666047,9]
    # links["rainbow_coloring"]=[43112064,1]
    # links["rainbow_colour"]=[2596741,1]
    # links["rainbow_smelt"]=[5625855,1]
    # links["rainbow_jersey"]=[4350728,1]
    # links["rainbow_flag_(gay_movement)"]=[13108211,1]
    # links["rainbow_lorikeet"]=[42936841,3]
    # links["rainbows_in_mythology"]=[1026203,6]
    # links["rainbow_flag_(lgbt)"]=[12813031,6]
    # links["atmospheric_refraction"]=[1784072,1]
    # maxId = 62666047
    # print("getID")
    # maxId = getID(links)
    
    # print("calcRedirect")
    # calcRedirect(links, maxId)
    # li=[]

    # print("del")
    # for i in links:
    #     if links[i][0] == -1:
    #         li.append(i)

    # for i in li:
    #     del links[i]

    # for i in links:
    #     print(i +str(links[i]))
    # print('end')

    # calcEntrophy(links)

timeStart = time.time()

main()
timeEnd = time.time()
sec = timeEnd - timeStart
result_list = str(datetime.timedelta(seconds=sec))
print(result_list)