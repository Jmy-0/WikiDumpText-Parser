from distutils.log import error
import os
from parse import *
from urllib import parse as urlp
import re
def parsedFileSum(a,b, path,texts):
    
    inputPath = path+"/parsed_"+a+b
    with open(inputPath , 'r',encoding='UTF-8') as f:
        texts.append(f.read())


def getParsed(a,b,r):
    
    path = "./linux"
    folder = "/"
    page = "/wiki_"
    heads = []
    anchors = []
    links = []
    print("folder : "+a+b)
    outputPath = path+folder+a+b+"/parsed_"+a+b
    for i in (range(r)):
        print("page: %d"%(i))
        if(i<10):
            P = path+folder+a+b+page+'0'+str(i)
        else:
            P = path+folder+a+b+page+str(i)
        with open(P , 'r',encoding='UTF-8') as f:
            docs = f.read()
            tt = docs.find('Alternatives Journal')
            if tt > -1:
                print(docs)
    #         docs = docs.replace('\n','').replace('"','').replace('&gt','').replace(' ','_').split('</doc>')

    #     for doc in docs:#한 doc에 대한 파싱
    #         if doc == '':
    #             continue
    #         headAndContent = doc.split('>')
    #         h = headAndContent[0].replace('<doc ','')
    #         content = headAndContent[1]
    #         content=content.split('&lt;');

    #         anchor = []
    #         link = []
    #         for t in content:
    #             temp = parse('a_href={};{}', t)
    #             if temp != None:
    #                 link.append(temp.fixed[0])
    #                 anchor.append(temp.fixed[1])
    #         heads.append(h)
    #         links.append(link)
    #         anchors.append(anchor)

    # with open(outputPath,"w",encoding='UTF-8') as output_fp:
    #     for num in range(len(heads)):
    #         output_fp.write(heads[num]+'\n')
    #         for l in range(len(links[num])):
    #             output_fp.write(links[num][l] + "\t\t" + anchors[num][l]+"\n")
                        
    #         output_fp.write("\n") 

def parseRedirects():
    #insert 명령어 기준으로 split, 파일 개수 및 이름은 이때 나온 리스트의 개수와 같다
    with open("enwiki-latest-redirect.sql","r",encoding="UTF-8") as f:
        allTexts = f.read()
        allLines = allTexts.split("INSERT INTO `redirect` VALUES ")
    count = 0

    for line in allLines:
        fromID = []
        namespace = []
        title = []
        fromIDAppend = fromID.append
        titleAppend = title.append
        namespaceAppend = namespace.append
        parsedLines =line.split("),")
        for parsedLine in parsedLines:
            data = parse("({},{},'{}','{},'{}", parsedLine)
            if not data:
                continue
            if data.fixed[1] !='0':#namespace 0아니면 무시
                continue

            fromIDAppend(data.fixed[0])
            namespaceAppend(data.fixed[1])
            titleAppend(data.fixed[2])
        
        #fromID 와 title만 저장
        with open("./redirects/redirect"+str(count),"w",encoding="UTF-8") as outfile:
            for i in range(len(fromID)):
                outfile.write("id:_"+str(fromID[i])+"_namespace:_"+namespace[i] +"_title:_"+title[i]+"\n")
        count+=1

def mergePagelinks():
    for i in range():
        with open("./pagelinks/pagelinks", "r",encoding="UTF-8") as f:
            f.read()
            
    return    


def mergeRedirect():
    li = []
    for i in range(553):
        with open("./redirects/redirect"+str(i),"r",encoding="UTF-8") as f:
            li.append(f.read())
    
    with open("allRedirect", "w", encoding="UTF-8") as f:
        for i in li:
            f.write(i.replace('\\"','"').replace("\\'","'").replace("\\\\",'\\'))


def parseTitles():
    with open("allLinks_lowerURL","r",encoding="UTF-8") as f:
        inputReadLine = f.readline
        with open("titles", "w", encoding="UTF-8")as of:
            while(True):
                line = inputReadLine()

                if not line:
                    break
                if line.find("<doc") >-1:
                    of.write(line.replace("<doc_",""))

def translateAllLinks():
    li = []
    an = []
    liAppend = li.append
    anAppend = an.append
    with open("allLinks","r",encoding="UTF-8") as f:
        readLine = f.readline
        
        while(True):
            line = readLine()
            
            if not line:
                break
            if line =='\n':
                continue
            if line.find("<doc") >-1:
                p = parse("<doc_id={}_url=?curid={}_title={}\n", line)
                nowPageTitle = p.fixed[2]
                continue
                
            line = line.split("\t\t")#url, anchor text분리
            #link = urlp.unquote(line[0]).lower()#url을 title로 변환
            link = urlp.unquote(line[0])
            link = link[:1].upper()+link[1:]
            link = link.replace(' ','_')#다른 파일의 title과 비교하기위해 공백문자를 _로 변환
            link = link.split("#")# #을 포함한 데이터에 대한 처리를 위해 분리

            if link[0] == "":# #으로 시작하는 경우
                #continue# #으로 시작하는 경우 제거
                link[0]=nowPageTitle#그 링크가 존재하는 페이지를 가리키는 링크이므로 현재 페이지의 title로 바꾼다

            anchor = line[1].replace('\n','')
            if link[0].find('\n') > -1:
                link[0] = link[0].replace('\n','')

            liAppend(link[0])
            anAppend(anchor)
    print("half")
    with open("allLinks_","w",encoding="UTF-8") as of:
        for i in range(len(li)):
            of.write(li[i] + "\t\t"+an[i]+"\n")                
               
def findWord():#디버그용
    count =0
    cnf =0
    with open("title_deleteHTMLcode.txt","w",encoding="UTF-8") as outf:
        wr = outf.write
        with open("titles","r",encoding="UTF-8") as f:
            fReadLine = f.readline
            while(True):
                count += 1
                line = fReadLine()
                if not line:
                    break
                line = parse("id={}_url=?curid={}_title={}\n",line)
                title = line.fixed[2].replace("&amp;","&").replace("&quot;",'"')
                wr("id="+line[0]+"_url=?curid="+line[1]+"_title="+title+"\n")


    print("전체 : %d cnf : %d"%(count,cnf))
def parsePagelinks():
    #insert 명령어 기준으로 split, 파일 개수 및 이름은 이때 나온 리스트의 개수와 같다
    count = 0
    fromID = []
    namespace = []
    title = []
    fromNamespace = []
    fromIDAppend = fromID.append
    titleAppend = title.append
    namespaceAppend = namespace.append
    fromNamespaceAppend = fromNamespace.append
    fileNum = 554
    start = 37
    for i in range(start-1,fileNum):
        with open("./pagelinks/pagelinks"+str(i+1)+".txt","r",encoding="UTF-8") as f:
            readLine = f.readline
            while(True):
                line = readLine()
                count+=1
                if not line:
                    break


                line = parse("INSERT INTO `pagelinks` VALUES {});\n", line)
                parsedLines = line.fixed[0].split("),")
            
            
                for parsedLine in parsedLines:
                    data = parse("({},{},'{}',{}", parsedLine)
                    if not data:
                        continue
                    
                    if data.fixed[1] == '0' and data.fixed[3] == '0':
                        fromIDAppend(data.fixed[0])
                        namespaceAppend(data.fixed[1])
                        titleAppend(data.fixed[2])
                        fromNamespaceAppend(data.fixed[3])
        with open("./parsedPagelinks/parsedPagelinks"+str(i+1)+".txt","w",encoding="UTF-8") as outfile:
            for i in range(len(fromID)):
                outfile.write(str(fromID[i])+"\t\t"+title[i]+"\n")
            outfile.close()
        fromID.clear()
        namespace.clear()
        title.clear()
        fromNamespace.clear()

def mergePagelinks():
    start = 1
    end = 238
    size = 4
    count = 0
    li = []
    for i in range(start,end+1):
        with open("./parsedPagelinks/parsedPagelinks"+str(i)+".txt","r",encoding="UTF-8") as f:
            count +=1
            li.append(f.read())

        
        if count % size == 0:
            with open("./pagelinks/merged"+str(int(count / 4))+".txt","w",encoding="UTF-8") as outf:
                for j in li:
                    outf.write(j)
            li.clear()


    with open("./pagelinks/merged"+str(int(count / 4 + 1))+".txt","w",encoding="UTF-8") as outf:
        for j in li:
            outf.write(j)
        li.clear()
def splitPagelinks():
    count = 0
    texts = []
    size = 100
    textsAppend = texts.append
    with open("enwiki-latest-pagelinks.sql","r",encoding="iso8859_1") as f:
        
        while(True):
            count+=1
            line = f.readline()
            if not line:
                break
            
            textsAppend(line)

            if count%size == 0:
                with open("./pagelinks/pagelinks"+str(int(count/size))+".txt","w",encoding="UTF-8") as outfile:
                    for i in texts:
                        outfile.write(i)
                    outfile.close()
                texts.clear()
    with open("./pagelinks/pagelinks"+str(int(count/size)+1)+".txt","w",encoding="UTF-8") as outfile:
        for i in texts:
            outfile.write(i)
        
    texts.clear()

def matchURLAndTitle():
    #타이틀 먼저 확인해서 변수로 저장
    title = dict()
    count =0
    with open("titles","r",encoding="UTF-8") as tf:
        inputRead = tf.readline
        while(True):
            count +=1
            line = inputRead()
            if not line:
                break

            p = parse("id={}_url=?curid={}_title={}\n",line)
            if p.fixed[2] in title:
                title[p.fixed[2]+"__count:"+str(count)] = p.fixed[0]
            else:
                title[p.fixed[2]] = p.fixed[0]
        tf.close()
    print("title end")
    li = list()
    url = list()
    urlAppend = url.append
    liAppend = li.append
    canNotFoundCount = 0
    with open("allLinks_","r",encoding="UTF-8") as f:
        inputRead = f.readline
        while(True):
            line = inputRead()
            if not line:
                break

            p = line.split("\t\t")
            p[0] = p[0].replace("&amp;nbsp;","_")
            urlAppend(p[0])
            try:
                liAppend(title[p[0]])
            except KeyError:
                liAppend("CanNotFoundTitle")
                canNotFoundCount += 1

        f.close()
        print("entire: %d CanNotFound: %d"%(count,canNotFoundCount))
    print("links end")
    with open("allLinks_ID","w",encoding="UTF-8") as wf:
        for i in range(len(li)):
            wf.write(li[i]+"\t\t"+url[i] +"\n")


def mergeID():
    with open("allLinks_","r",encoding="UTF-8") as inf1:
        readall = inf1.readline
        with open("allLinks_ID", "r", encoding="UTF-8") as inf2:
            with open("id and anchor", "w", encoding="UTF-8") as of:
                readID = inf2.readline
                while(True):
                    line1 = readall()
                    line2 = readID()
                    if not line1:
                        break;

                    li1 = line1.split("\t\t")
                    li2 = line2.split("\t\t")

                    of.write(li2[0]+"\t\t"+li1[1])
def deleteHTMLCode():
    id = list()
    url = list()

    idAppend = id.append
    urlAppend = url.append
    tags = {"</a>","<sub>","</sub>","<ref>","</ref>","<small>","</small>","<span_style=>","</span>","<includeonly>","</includeonly>","<sup>","</sup>"}
    with open("allLinks_ID","r",encoding="UTF-8") as f:
        inputRead = f.readline
        while(True):
            line = inputRead()
            if not line:
                break

            p = line.split("\t\t")
            if p[0] != "CanNotFoundTitle":
                continue
            p[1] = p[1].replace("&amp;","&").replace("&lt;", "<").replace("&gt;",">").replace("&quot;",'"').replace("&nbsp;","_")
            for i in tags:
                p[1] = p[1].replace(i,"")
            p[1] = p[1].replace("&amp;","&").replace("&lt;", "<").replace("&gt;",">").replace("&quot;",'"').replace("&nbsp;","_")
            test = parse("{}<!--{}-->{}", p[1])
            idAppend(p[0])
            if not test:
                urlAppend(p[1][:1].upper()+p[1][1:])
            else:
                urlAppend(test.fixed[0][:1].upper()+test.fixed[0][1:]+test.fixed[1])
        f.close()
    with open("url","w",encoding="UTF-8") as of:
        for i in range(len(id)):
            of.write(id[i]+"\t\t"+url[i])
def matchURLAndTitle2():
    #타이틀 먼저 확인해서 변수로 저장
    title = dict()
    count =0
    with open("title_deleteHTMLcode.txt","r",encoding="UTF-8") as tf:
        inputRead = tf.readline
        while(True):
            
            line = inputRead()
            if not line:
                break

            p = parse("id={}_url=?curid={}_title={}\n",line)
            if p.fixed[2] in title:
                title[p.fixed[2]+"__count:"+str(count)] = p.fixed[0]
            else:
                title[p.fixed[2]] = p.fixed[0]
        tf.close()
    print("title end")
    li = list()
    url = list()
    urlAppend = url.append
    liAppend = li.append
    canNotFoundCount = 0
    with open("url","r",encoding="UTF-8") as f:
        inputRead = f.readline
        while(True):
            line = inputRead()
            if not line:
                break

            p = line.split("\t\t")
            urlAppend(p[1])
            count +=1
            try:
                liAppend(title[p[1]])
            except KeyError:
                liAppend("CanNotFoundTitle")
                canNotFoundCount += 1

        f.close()
        print("all: %d CanNotFound: %d"%(count,canNotFoundCount))
    print("links end")
    with open("allLinks_ID2","w",encoding="UTF-8") as wf:
        for i in range(len(li)):
            wf.write(li[i]+"\t\t"+url[i])
print("start")
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#matchURLAndTitle()
#translateAllLinks()
#deleteHTMLCode()
#matchURLAndTitle2()
#mergeID()
#splitPagelinks()
#parsePagelinks()
#mergeRedirect()
#mergePagelinks()
#getParsed('a','a',43)


with open("./pagelinks/merged3.txt", "r", encoding="iso8859_1") as f:
    while(True):
        line = f.readline()
        if not line:
            break;
        print(line)

print("end")