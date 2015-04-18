#encoding:utf8

import unittest
from dealDatabase import *

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def testCreateTable(self):
        createTableStr="create table tabname(col1 int(10) not NULL primary key,col2 char(20) not null)"
        dealTable(createTableStr)
        
    def testDropTable(self):
        #dropTableStr="drop table tabname"
        #dealTable(dropTableStr)
        pass
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    current_database="jwos"
    unittest.main()
