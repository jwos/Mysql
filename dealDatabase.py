#encoding:utf8

import re
import os
import shutil
import fileinput 

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
    
def createTable(tableName,colDetails,isOnlyPrime):
    table_def_path=root_path+current_database+"/"+tableName
    table_index_path=table_def_path+"_pkr"
    table_status_path=table_def_path+"_stat"
    table_dat_path=table_def_path+"_dat"
    if os.path.exists(table_def_path):
        return 1;
    f = open(table_def_path, 'w')
    for colDetail in colDetails:
        f.write(','.join(str(i) for i in colDetail) )
        f.write("\n")
    f.close()
    
    with open(table_status_path, "w") as f:
        f.write("0")
    #创建table_def_path
    open(table_index_path, "w").close()
    open(table_dat_path, "w").close()
    return 0

def dropTable(tableName):
    table_def_path=root_path+current_database+"/"+tableName
    table_index_path=table_def_path+"_pkr"
    table_status_path=table_def_path+"_stat"
    table_dat_path=table_def_path+"_dat"
    if os.path.exists(table_def_path):
        os.remove(table_def_path)
        os.remove(table_index_path)
        os.remove(table_status_path)
        os.remove(table_dat_path)
        return 0
    else:        
        return 1
                       
                   
def verifyTabCol(tabCol):
    
    if 100<tabCol[2]:
       
        return 0
    
    return 1

def existTable(tableName):
    table_def_path=root_path+current_database+"/"+tableName
    if os.path.exists(table_def_path):
        return True
    else:
        return False  
    
    
def dealTable(s):
    pTable=re.compile(r'^create table ([^()]+)\((.+)\)');
    match=re.match(pTable,s);
    if match:
        tableName,createString=match.group(1),match.group(2)
        
        colArr=createString.split(',')
        tabArr=[]
        isOnlyPrime=0 #很重要，
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
                if isOnlyPrime==0:
                    isOnlyPrime=1
                else:
                    print "duplicate primary keys"
                    return 7
            
            tabCol=[colName,dataType,dataLength,isNotNull,isPrime] #tabCol是一个col
            print tabCol
            if verifyTabCol(tabCol)==1: #验证数据完整性
                tabArr.append(tabCol)
            else:
                raise Exception("verifyWrong")
                    
    
        ret=createTable(tableName,tabArr,isOnlyPrime) 
        if ret ==1:
            print "tablename %s already exists!" % tableName
        else:
            print "tablename %s created!" % tableName

    pDropTable=re.compile(r'^\s*drop\s+table\s+([^\s]+)\s*$');
    match=re.match(pDropTable,s);
    if match:
        tableName=match.group(1)
        ret=dropTable(tableName)
        if ret ==1:
            print "database %s does't exists!" % tableName
        else:
            print "database %s dropped!" % tableName


#判断是否主键是否冲突 冲突为true，不冲突为False
def checkConfilctPrime(tableName,colName,primNum):
    table_index_path=root_path+current_database+"/"+tableName+"_pkr"
    if not os.path.exists(table_index_path):
        return 71
    else:
        primaryKeys=[]
        with open(table_index_path, 'r') as f:
            primaryKeys=f.readlines()   
        print primaryKeys
        print primNum     
        if str(primNum) in primaryKeys:
            return True

        else:
            return False
    
    
    
def verifyTabColValue(tableName,valuesArr):
    table_def_path=root_path+current_database+"/"+tableName
    table_index_path=table_def_path+"_pkr"
    f = open(table_def_path, 'r')
    tableDetails=f.readlines()
    f.close()
    
    primeValue=""
    if len(valuesArr)/2>len(tableDetails):
        return 13
    
    for k,v in enumerate(tableDetails):
        [colName,dataType,dataLength,isNotNull,isPrime]=v.split(',')
        #比较数据类型是否一致
        valuesArr_data_place=int(2*k)
        valuesArr_type_type=valuesArr_data_place+1
        if not int(valuesArr[valuesArr_type_type])==int(dataType):
            print "dataType not matched"
            return 17
        
        if int(dataLength)<= len(valuesArr[ valuesArr_data_place]):
            print "dataLength too long"
            return 18
        
        if int(isPrime)==1:
            primeValue=valuesArr[valuesArr_data_place]
            if  checkConfilctPrime(tableName,colName,primeValue):
                print "duplicate prime"
                return 19   
        
    
    #如果是主键正确就把主键放在这里    
    if primeValue!="":
        with open(table_index_path,'a') as f:
            f.write(primeValue)   
            
    return 0   

#将真正写入文件
def realInsert(tableName,insert_data_and_dataType_arr):
    # 必须加一个delete标记
    table_def_path=root_path+current_database+"/"+tableName
    
    table_status_path=table_def_path+"_stat"
    table_dat_path=table_def_path+"_dat"
    f = open(table_dat_path, 'a')
    s=""
    for k,v in enumerate(insert_data_and_dataType_arr):
        if k%2==0:
            if k!=0:
                s+=('|'+str(v) )
            else:
                s+=str(v)
    
    
    #这是delete标记，删除为1
    s+="|0\n"
    
    print s
 
 
    
    f.write(s)
    f.close()
    
    #修改stat文件的count ++
    for line in fileinput.input(table_status_path, inplace=1): 
        if fileinput.filelineno()==1: 
            print int(line)+1, 
        
    
def Insert(s):
    pInsert=re.compile(r'insert into ([^\s]+) values \((.+)\)');
    match=re.match(pInsert,s);
    if match:
        tableName,insertString=match.group(1),match.group(2)   
        print tableName,"|",insertString
        
        #判断表是否存在
        if not existTable(tableName):
            return 3
        #解析insertString
        valuesArr=[i.strip() for i in insertString.split(", ")]
        print valuesArr
        insert_data_and_dataType_arr=[]
        for value in valuesArr:
            if '\'' in value:
                insert_data_and_dataType_arr.append(value.lstrip("'").rstrip("'"))
                insert_data_and_dataType_arr.append(1)
            else:
                insert_data_and_dataType_arr.append(value)
                insert_data_and_dataType_arr.append(0)
        #print insert_data_and_dataType_arr
        ret=verifyTabColValue(tableName,insert_data_and_dataType_arr)
        if ret==0:
            print "verifyOK ok"
            if realInsert(tableName,insert_data_and_dataType_arr):
                pass 
                
        else:
            print ret
            print "verify not ok"
        
        
    
    
    
        
if __name__ == "__main__":
    current_database="jwos"
    
    #getVirusStatusContinue()
    #createTableStr="create table tabname(col1 int(10) not NULL primary key,col2 char(20) not null)"
    #dealTable(createTableStr)
    #dropTableStr="drop table tabname"
    #dealTable(dropTableStr)
    #s="drop table tabname"
   
    
    s="insert into tabname values (13,  'Champs-Elysees')"
    tableDetail=Insert(s)
    #tabName="tabname"
   
    
    