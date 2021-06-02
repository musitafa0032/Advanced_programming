class Node:
    def __init__(self,word,word_fre,next_node=None):
        self.word = word
        self.word_fre = word_fre
        self.next_node = next_node

class FreqLinkedList:
    def __init__(self):
        self.head = None


    def addWord(self,word):
        new_node = Node(word,1)
        if self.head is None or self.head.word > new_node.word:
            new_node.next_node = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next_node and current.next_node.word <= new_node.word:
                current = current.next_node
            if new_node.word == current.word:
                current.word_fre += 1
            else:
                current.next_node, new_node.next_node = new_node, current.next_node
                    

    def printList(self):
        node = self.head
        while node:
            print(node.word,node.word_fre)
            node=node.next_node




    def filterWords(self,fre):
        q=self.head
        while q.next_node:
            if q.next_node.word_fre < fre:
                q.next_node = q.next_node.next_node
            else:
                q = q.next_node
        if self.head.word_fre < fre:
            self.head = self.head.next_node
