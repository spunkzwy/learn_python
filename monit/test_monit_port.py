import unittest
from monit_port import *

class Test_monit_port(unittest.TestCase):

    def test_check_tcp(self):
        self.assertEquals(check_tcp('6.9.9.7',80),False)
        self.assertEquals(check_tcp('www.baidu.com',80),True)

    def test_check_udp(self):
        self.assertEquals(check_udp('202.99.96.68',53),True)
        self.assertEquals(check_udp('127.0.0.1',53),False)
if __name__ == '__main__':
    unittest.main()
