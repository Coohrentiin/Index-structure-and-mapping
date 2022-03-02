import numpy as np
import time 
import memory_profiler
from Trees import Tree, Trie
import copy

class BWT(object):
    def __init__(self,text):

        self.text = text
        self.sa = []
        self.bwt_text = ""
        self.L = []
        self.R = []
        self.suffix_trie = None

    def compute_sufixe_array(self):
        trie = Trie()
        words=[]
        for i in range(len(self.text)):
            words.append(self.text[i:])
        for i,word in enumerate(words):
            trie.insert(word,i)

        def compress_trie(trie):
            for i,(label,child) in enumerate(trie.children):
                compress_trie(child)
                if len(child.children) == 1:
                    ## merge with child
                    clabel, cchild = child.children[0]
                    trie.children[i] = (label+clabel, cchild)
        compress_trie(trie)
        self.suffix_trie = trie

        
        def construct_suffix_array(tree):
            sa=list()
            for (label, child) in tree.children:
                if len(child.children) == 0:
                    sa.append((label,child.label))
                else:
                    sa_child=construct_suffix_array(child)
                    for (label_c,child_c) in sa_child:
                        sa.append((label+label_c,child_c))
            return sa
        self.sa = construct_suffix_array(trie)
        return self.sa
    
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
            if self.suffix_trie == None:
                raise "First compute suffix array"
            n=len(self.text)
            BWT=''
            for i in range(n):
                BWT+=self.text[self.sa[i][1]-1]
            self.bwt_text = BWT
        R = [[i, 0] for i in self.bwt_text]            #R for Right
        L = [i.copy() for i in R]
        L.sort(key=lambda item:item[0]) #L for Left

        #Dict containing index interval of each letter, and a count dict (maybe useless if we destroy intervals a bit at each step)
        intervals = {}
        count = {}
        for i, c in enumerate(L):
            try:
                intervals[c[0]] = intervals[c[0]]+[i]
                count[c[0]] = count[c[0]]+1
            except:
                intervals[c[0]] = [i]
                count[c[0]] = 1

        for i in range(len(R)):
            c = R[i][0]
            t = intervals[c][0]
            R[i][1] = t
            L[t][1] = i
            intervals[c] = intervals[c][1:]
        self.L = L
        self.R = R

        return BWT
    
    def bwt_search(self, x):
        start = 0
        end = len(self.L)-1 #index from 0

        def narrow_start(i: int, c: int, s=0, e=end):
            for j in range(s,e+1):
                if self.L[j][0]==c:
                    return j
            return end
        

        def narrow_end(i: int, c: int, s=0, e=end):
            for j in reversed(range(s,e+1)):
                if self.L[j][0]==c:
                    return j
            return start
        
        def narrow_start_right(i: int, c: int, s=0, e=end):
            for j in range(s,e+1):
                if self.R[j][0]==c:
                    return self.R[j][1]
            return start

        def narrow_end_right(i: int, c: int, s=0, e=end):
            for j in reversed(range(s,e+1)):
                if self.R[j][0]==c:
                    return self.R[j][1]
            return end

        n_start = narrow_start(0, x[-1], s=start, e=end)
        n_end   = narrow_end(0, x[-1], s=start, e=end)
        for i,c in enumerate(x[:-1][::-1]):
            start = narrow_start_right(i, c, s=n_start, e=n_end)
            end   = narrow_end_right(i, c, s=n_start, e=n_end)
            n_start = start
            n_end = end                             
            if start>end:
                return None
        
        result = [self.sa[i] for i in range(start, end+1)]
        result.sort(key = lambda x: x[1])
        # At this step answer are between start and end -> need sa sorted to reconstruct 
        return(result) #send back the possible position found in SA