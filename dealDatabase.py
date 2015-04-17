#encoding:utf8

'''
Created on 2015��4��16��

@author: b
'''
import re
import os
import shutil

root_path="d:/mysql/";
current_database=""


def createDatabase(databaseName):
    finalDir=root_path+databaseName;
    if os.path.exists(finalDir):
        return 1; #dir exists
    else:
        os.makedirs(finalDir);
        return 0;
        
def dropDatabase(databaseName):
    finalDir=root_path+databaseName;
    if os.path.exists(finalDir):
        shutil.rmtree("D:/mysql/mydata"); #dir exists
        return 0
    else:        
        return 1;        
                                

def dealDatabase(s):
    #deal with database
    pDatabase=re.compile(r'^\s*create\s+database\s+([^\s]+)\s*$');
    match=re.match(pDatabase,s);
    if match:
        databaseName=match.group(1)
        ret=createDatabase(databaseName)
        if ret ==1:
            print "database %s already exists!" % databaseName
        else:
            print "database %s created!" % databaseName
    
    
    pDatabase=re.compile(r'^\s*drop\s+database\s+([^\s]+)\s*$');
    match=re.match(pDatabase,s);
    if match:
        databaseName=match.group(1)
        ret=dropDatabase(databaseName)
        if ret ==1:
            print "database %s does't exists!" % databaseName
        else:
            print "database %s dropped!" % databaseName
    
def createTable(tableName,colDetails):
    table_path=root_path+current_database+"/"+tableName
    if os.path.exists(table_path):
        return 1;
    f = open(table_path, 'w')
    for colDetail in colDetails:
        f.write(','.join(str(i) for i in colDetail) )
        f.write("\n")
    f.close()
    return 0

def dropTable(tableName):
    table_path=root_path+current_database+"/"+tableName
    print table_path
    if os.path.exists(table_path):
        os.remove(table_path)
        return 0
    else:        
        return 1;        
                   
                   
def verifyTabCol(tabCol):
    
    if 100<tabCol[2]:
       
        return 0
    
    return 1
    
def parseCreateTable(s):
    pTable=re.compile(r'^create table ([^()]+)\((.+)\)');
    match=re.match(pTable,s);
    if match:
        tableName,innerString=match.group(1),match.group(2)
        
        colArr=innerString.split(',')
        tabArr=[]
        for a in colArr:
            
            #字段type colName dataLength isNotNull isPrime
            dataLength=10
            isNotNull=0
            isPrime=0
            
            print a
            firstBlank=a.index(' ')
            #print firstBlank
            colName= a[0:firstBlank]
            secondBlank=a.index(' ',firstBlank+1)
            dataType= a[firstBlank+1:secondBlank]
            #先写int和varchar
            typeWrap=re.match(r'(\w+)\((\d+)\)',dataType);
            if typeWrap:
                dataType=typeWrap.group(1)
                dataLength=int(typeWrap.group(2))
                
            dataMap={'int':0,'char':1};
            
            dataType=dataMap[dataType];
            
            remainStr=a[secondBlank+1:].lower()
            
            #print "dataType is %d" % dataType
            
            if "not null" in remainStr:
                isNotNull=1
                
            if "primary key" in remainStr:
                isPrime=1

            tabCol=[colName,dataType,dataLength,isNotNull,isPrime] #tabCol是一个col
            print tabCol
            if verifyTabCol(tabCol)==1: #验证数据完整性
                tabArr.append(tabCol)
            else:
                raise Exception("verifyWrong")
                
        return [tableName]+tabArr 
    else:
        raise Exception("wrong formmat create table sentence")   
    
    
    ret=createTable(tableDetail[0],tableDetail[1:]) 
    if ret ==1:
        print "tablename %s already exists!" % tableDetail[0]
    else:
        print "tablename %s created!" % tableDetail[0]

   
    
if __name__ == "__main__":
    #getVirusStatusContinue()
    s="create table tabname(col1 int(10) not NULL primary key,col2 char(20) not null)"
    current_database="jwos"
    tableDetail=parseCreateTable(s)
    tabName="tabname"
    ret=dropTable(tabName)
    if ret==1:
        print "table %s doesn't exist" % tabName
    else:
        print "table %s dropped " % tabName
    
    