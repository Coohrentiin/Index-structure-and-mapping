import numpy as np
import time 
import memory_profiler
from Trees import Tree, Trie

class BWT(object):
    def __init__(self,text):

        self.text = text
        self.sa = []
        self.bwt_text = ""
        self.L = []
        self.R = []
        return(0)
    
    def compute_sufixe_array(self):
        return(0)
    
    def construct_bwt(self, naive=False):
        if naive:
            n=len(self.text)
            sa=[]
            for i in range(n):
                sa.append(self.text[i:]+self.text[:i])
            sa.sort()
            BWT=''
            for i in range(n):
                BWT+=sa[i][-1]
            self.bwt_text = BWT
        else:
            pass
        return(0)
    
    def bwt_search(self):
        return(0)
    