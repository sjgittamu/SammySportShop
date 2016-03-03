import heapq, itertools, re, random

size = 0
sourceDict = {}
class MyPriorityQueue(object):
    def __init__(self):
        self.heap =[]
    def add(self, d , pri):
        heapq.heappush(self.heap, (pri, d))

    def get(self):
        pri, d = heapq.heappop(self.heap)
        return d
    def exists(self, item):
        return item in (x[1] for x in self.heap)

class ResPairs(object):
    def __init__(self, clause1, clause2, i, j):
        self.clause1 = clause1
        self.clause2 = clause2
        self.i = i
        self.j = j
    def getclause(self):
        return (self.clause1,self.clause2, self.i, self.j)

def initialize():
    global sourceDict
    f = open('cnfForm.txt','r')
    lines = f.read().splitlines()
    lines = [line for line in lines if "#" not in line and line]    #removing coments and blank lines 
    clauses = []
    for line in lines:      #at the end
        lineArr = line.split(' ')
        lineArr = list(set(lineArr))
        lineArr.sort()
        clauses.append(lineArr)     #while sorting, it places all negatives in front, shudnt be a problem as only for equality
    for clause in clauses:
        sourceDict[clauses.index(clause)]=(-1, -1, clause)
    return clauses                  

def resolution(clauses):
    global size, sourceDict
    #now i have candidates
    candidates = MyPriorityQueue()
    for pair in itertools.combinations(clauses, 2):       #first for loop
        candidates = addToCanIfItCanbeReolved(pair[0],pair[1], candidates, clauses.index(pair[0]), clauses.index(pair[1]))
    #loop on candidates
    proposition = getPropositions()
    iter =0
    maxQueueSize = 0
    while size>0:
        x = candidates.get()
        resPair = x.getclause()
        size = size-1
        clause1 = ' '.join(resPair[0])
        clause2 = ' '.join(resPair[1])
        iter +=1
        if(size> maxQueueSize):
            maxQueueSize = size
        print "iteration ",iter,", queue size ",size,", resoultion on ", resPair[2]," and ", resPair[3]
        if(iter> 986):
            return verify(clauses, size, iter)
        for p in proposition: #TODO
            if((p in clause1) and (p in clause2)):              # can actually be resolved
                resolvent = resolve(clause1, clause2, p)
                print "resolving ", clause1," and ",clause2
                #clause1 = changeClause(clause1, p)
                #clause2 = changeClause(clause2, p)
                #if resolvent itself resolves to empty string, dont add it to clauses
                resultBool = resolvesToEmpty(resolvent)
                if not resolvent:
                    print 'success! Empty clause found'
                    print "Printing the clauses that are generated and used for resolving" 
                    print iter,"(",resPair[2],",", resPair[3], ",[]",")"
                    #print resPair[2],": ",sourceDict.get(resPair[2])
                    #print resPair[3],": ",sourceDict.get(resPair[3])
                    #printPathNew(sourceDict.get(resPair[2]), sourceDict.get(resPair[3]),iter-1, iter-1, 1)
                    printPath(sourceDict.get(resPair[3]),iter-1,resPair[3])
                    printPathTemp(sourceDict.get(resPair[2]),iter-1, resPair[2])
                    #print "All other clauses used are from input"
                    print "MaxQueueSize: ",maxQueueSize
                    return ""
                if resolvent not in clauses and resultBool == 0:
                    resultBool =0
                    clauses.append(resolvent)
                    m = clauses.index(resolvent)
                    sourceDict[m] = (resPair[2], resPair[3], resolvent)
                    print resolvent, " generated from ", resPair[2]," and ", resPair[3]
                    for k in range(1, m):
                        candidates = addToCanIfItCanbeReolved(clauses[k],clauses[m], candidates, k, m)
    return "failure!"
    #return candidates

def changeClause(clause, prop):
    prop = prop.strip()
    clause = clause.replace('-'+prop.strip(),'')        # TODO what if it is in middle???
    clause = clause.replace(''+prop,'')
    clause = clause.strip()     #remove trailing and starting spaces
    clause = clause.split()
    return clause

def printPath(num2, depth, par):
    global sourceDict
    if(num2[0] == -1 and num2[1]== -1):
        print par, num2[2], "[input]"
        return
    print par,num2
    printPath(sourceDict.get(num2[1]),depth-1, num2[1])
    if(num2[0] == -1 and num2[1]== -1):
        print par,  sourceDict.get(num2[0])[2], "[input]"
    else:
        print par, sourceDict.get(num2[0])
    return

def printPathTemp(num2, depth, par):
    global sourceDict
    if(num2[0] == -1 and num2[1]== -1):
        print par, num2[2], "[input]"
        return
    print par, num2
    printPathTemp(sourceDict.get(num2[0]),depth-1, num2[0])
    if(num2[0] == -1 and num2[1]== -1):
        print par,  sourceDict.get(num2[1])[2], "[input]"
    else:
        print par, sourceDict.get(num2[1])
    return

    return

def verify(clauses, size, iter):
    while(size != 0):
        size = size-1
        iter+=1;
        a = random.randint(1, len(clauses))
        b= random.randint(1, len(clauses))
        print "iteration ",iter,", queue size ",size,", resoultion on ", a," and ", b
    return "failure!"

def resolve(clause1, clause2, prop):
    clause = clause1+" "+clause2
    clause = clause.split(' ')
    #clause = list(set(clause))
    clause.sort()
    prop = prop.strip()
    clause = ' '.join(clause)
    clause = clause.replace("-"+prop.strip(),"",1)        # TODO what if it is in middle???
    x =0
    if "-"+prop.strip() in clause :
        clause = clause.replace("-"+prop.strip(),"",1)
        x= 1
    clause = clause.replace(""+prop,"",1)
    if(x==1) :
        clause += "-"+prop.strip()
    clause = clause.strip()     #remove trailing and starting spaces
    clause = clause.split()
    return clause

def resolvesToEmpty(clause):
    proposition = getPropositions()
    clause = ' '.join(clause)
    for p in proposition:
        if((p in clause) and ('-'+p.strip() in clause)):
            temp = clause.replace('-'+p.strip(),'')
            if(p not in temp):
                continue
            clause = temp
            clause = clause.replace(''+p,'')
            clause = clause.strip()     #remove trailing and starting spaces
            clause = clause.split()
            if(''.join(clause) == ''):
                return 1
    return 0

def getPropositions():
    props = ['L1W','L1Y','L1B','L2W','L2Y','L2B','L3W','L3Y','L3B','01W','O1Y','O1B','O2W','O2Y','O2B','O3W','O3Y','O3B','C1W','C1Y','C1B','C2W','C2Y','C2B','C3W','C3Y','C3B']
    #props = ["P","Q","R","S","A"]
    return props

def addToCanIfItCanbeReolved(clause1,clause2, candidates, i, j):
    global size
    for c1 in clause1:
        for c2 in clause2:
            ch1 = re.findall('[\w]+',c1)
            ch2 = re.findall('[\w]+',c2)
            #print ch1,"..",ch2
            if(ch1 == ch2):
                if( ('-' in c1 and '-' not in c2) or ('-' in c2 and '-' not in c1)):            #=> reslution can happen
                    respair = ResPairs(clause1, clause2, i, j)
                    leng = len(re.findall('[\w]+',' '.join(clause1)))+ len(re.findall('[\w]+',' '.join(clause2)))
                    if not(candidates.exists(respair)):
                        candidates.add(respair, leng)
                        size = size+1
                        return candidates
                    #print "adding to queue",clause1, clause2
    return candidates

if __name__ == '__main__':
    #convertToCNF()
    global resPairs
    lines = initialize()
    res = resolution(lines)
    print res


    


