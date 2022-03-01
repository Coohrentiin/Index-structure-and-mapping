import graphviz

class Tree:
    """
    N-ary tree with node and edge labels
    
    Trees can be constructed by adding children via method add_child.
    """
    def __init__(self, label=""):
        self.children = list()
        self.label = label

    def create(self,*args):
        return Tree(*args)
    
    def add_child(self, edge_label=None, label=""):
        """
        Add child
        
        Args:
            edge_label: edge label
            label: label of child node
        Returns:
            new child tree
        """
        self.children.append((edge_label, self.create(label)))
        return self.children[-1][1]

    def _add_to_graphviz(self, dot, index=1):
        """Add edges and nodes to graphviz object"""
        root = index
        dot.node(str(root), str(self.label))
        index += 1
        
        for e, c in self.children:
            child_index = index
            index = c._add_to_graphviz(dot, child_index)
            dot.edge(str(root), str(child_index), label=str(e))
        
        return index
    
    def dot(self, *, graph_attr={'rankdir': 'LR', 'ranksep': '0.4'},
            node_attr={'shape': 'plaintext', 'width': '0.1', 'height': '0.1'},
            edge_attr={'arrowsize': '0.75'}
           ):
        """
        Construct Graphviz Digraph of the tree
        
        Returns: tree as graphviz.Digraph
        """
        
        dot = graphviz.Digraph('Tree')

        dot.graph_attr.update(graph_attr)
        dot.node_attr.update(node_attr)
        dot.edge_attr.update(edge_attr) ## ,lblstyle="above, sloped" ?? with tikz

        self._add_to_graphviz(dot)
        return dot

class Trie (Tree):
    def __init__(self, label=""):
        super().__init__(label)
    
    def create(self, *args):
        return Trie(*args)
        
    def lookup_child(self, edge_label):
        """
        Lookup index of child with edge label, assume sorted children
        """
        
        for c in self.children:
            if c[0] == edge_label:
                return c[1]

        return None
                
    def add_child(self, edge_label, label=""):
        """
        Get child with edge label, keeping edge labels alphabetically sorted
        """
        
        if self.children==[] or self.children[-1][0]<edge_label:
            i = len(self.children)
        else:
            for i, c in enumerate(self.children):
                if c[0] > edge_label:
                    break
                    
        c = self.create(label)
        self.children.insert(i, (edge_label, c))
        return c
    
    def insert( self, x, annotation ):
        """
        Insert string x with annotation
        
        Args:
          x: string
          annotation: typically the word index
        
        This inserts new branches in alphabetical order
        """
        if x == "":
            self.label = annotation
            return

        c = self.lookup_child(x[0])
        if c is None:
            c = self.add_child(x[0])
            c.ol = annotation

        c.insert( x[1:], annotation)