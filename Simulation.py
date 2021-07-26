import numpy as np
import random as rnd

 
class Monke():
  #monke_type specifies the strategy chosen by the monkey: 0 - Always co-operate, 1 - Always defect
                                                          #3 - Tit-for-tat,       2 - Random choice
  def __init__(self, monke_type=2):
    self.id = 0
    self.pos = 0
    self.food = 0
    self.age = 0
    self.monke_type = monke_type
    #stores whether a monke is alive or not, dead monkes can't interact with other monkes
    self.zinda = True 
    #memorylist stores the last interaction with the other monke, 1 for cooperation, 0 for no encounter
    #and -1 if the other monke defected last time
    self.memorylist = []
 
class Tree():
  def __init__(self):
    self.monke1 = -1
    self.monke2 = -1
 
class Environment():
  def __init__(self, n=100, repreq=10, livereq=1, memorycost = 5):
    self.n=n #number of trees = number of fruits
    self.reproductionreq=repreq #fruits reqd to reproduce
    self.livereq=livereq #fruits reqd to stay alive
    self.memorycost = memorycost
    self.monkes = []
    self.trees = self.get_empty_trees()
    self.currpop = [0,0,0,0]
    self.monkesontrees = 0
    self.pop_hist = []
 
  def setup(self, monkes : list):

        self.monkes = monkes
        for i in range(len(monkes)):
            monkes[i].id=i
            self.currpop[monkes[i].monke_type]=self.currpop[monkes[i].monke_type]+1
            self.buildmemory(i)
        return
 
  def buildmemory(self, i):
    #returns an emmpty array containing as many zeroes as the total number of monkes
    self.monkes[i].memorylist = np.zeros(len(self.monkes), dtype = int)
    return
 
  def get_empty_trees(self):
    trees = []
    for i in range(self.n): 
      trees.append(Tree())
    return trees
 
  def choose_rand_pos(self,iter):
    x=np.random.choice(self.n)
    tree=self.trees[x]
    #choose a random empty spot on the trees array for an incoming monke
    #the array of trees must not already be full of monkes, as that would result in an infinite loop
    while tree.monke1!=-1 and tree.monke2!=-1 and self.monkesontrees < 0.1*self.n:
      if iter>50:
        return -1
      x =self.choose_rand_pos(iter+1)
    return x
 
  def populateTree(self, i):
    x=self.monkes[i].pos
    if self.trees[x].monke1==-1:
      self.trees[x].monke1=i
      #print(self.trees[x].monke1)
    else:
      self.trees[x].monke2=i

    return
 
  def assign_rand_pos(self):
    #not all monkes will get assigned to a tree, some will go hungry for the iteration
    for i in range(len(self.monkes)):
        if self.monkes[i].zinda == True:
           if rnd.random() > 0.5:
            x = self.choose_rand_pos(0)
            if x!=-1:
          
              self.monkes[i].pos = x
              self.populateTree(i)
              self.monkesontrees += 1
            else:
              self.monkes[i].pos=-1
           else:
            self.monkes[i].pos=-1
 
  def cooperation_bool_pair(self, monke1, monke2):
    cooperate1=True 
    cooperate2=True
    if monke1.monke_type==0:
      cooperate1 = True
    if monke1.monke_type==1:
      cooperate1 = False
    if monke1.monke_type==2:
      cooperate1 = bool(rnd.getrandbits(1))
    if monke1.monke_type==3:
      if monke1.memorylist[monke2.id]==1:
        cooperate1 = True
      if monke1.memorylist[monke2.id]==-1:
        cooperate1 = False
      if monke1.memorylist[monke2.id]==0:
         if rnd.randint(0,1)==0:
           cooperate1= False
         else:
           cooperate1= True
      if monke2.monke_type==0:
        cooperate2 = True
      if monke2.monke_type==1:
        cooperate2 = False
      if monke2.monke_type == 2:
        cooperate2 = bool(rnd.getrandbits(1))
      if monke2.monke_type==3:
        if monke2.memorylist[monke1.id]==1:
          cooperate2 = True
        if monke2.memorylist[monke1.id]==-1:
          cooperate2 = False
        if monke2.memorylist[monke1.id]==0:
           if rnd.randint(0,1)==0:
             cooperate2= False
           else:
             cooperate2= True
    d=dict()
    d['c1']=cooperate1
    d['c2']=cooperate2
    return d  
 
  def interactions(self):
    for i in range(len(self.trees)):
      if self.trees[i].monke1!=-1 and self.trees[i].monke2!=-1:
        c = self.cooperation_bool_pair(self.monkes[self.trees[i].monke1],self.monkes[self.trees[i].monke2])
        c1=c['c1']
        c2=c['c2']
       
        if c1 and c2:
          self.monkes[self.trees[i].monke1].food+=1
          self.monkes[self.trees[i].monke2].food+=1
        if c1 and not c2:
         self.monkes[self.trees[i].monke2].food+=2
        if c2 and not c1:
          self.monkes[self.trees[i].monke1].food=+2
        if not c1 and not c2:
          self.monkes[self.trees[i].monke1].food=+0.5
          self.monkes[self.trees[i].monke2].food=+0.5
        if self.monkes[self.trees[i].monke1].monke_type==3:
          if c2:
           self.monkes[self.trees[i].monke1].memorylist[self.trees[i].monke2]=1
          else:
           self.monkes[self.trees[i].monke1].memorylist[self.trees[i].monke2]=-1
        if self.monkes[self.trees[i].monke2].monke_type==3:
          if c1:
           self.monkes[self.trees[i].monke2].memorylist[self.trees[i].monke1]=1
          else:
           self.monkes[self.trees[i].monke2].memorylist[self.trees[i].monke1]=-1
      if self.trees[i].monke1==-1 and self.trees[i].monke2!=-1:
       self.monkes[self.trees[i].monke2].food+=2
      if self.trees[i].monke1!=-1 and self.trees[i].monke2==-1:
       self.monkes[self.trees[i].monke1].food+=2
       
 
  def clearTrees(self):
    #after every iteration, every tree will become empty of monkes again
    for i in range(len(self.trees)):
      self.trees[i].monke1 = self.trees[i].monke2 = -1
    return

  def add_to_memory_list(self):
    for i in range(len(self.monkes)):
      self.monkes[i].memorylist=np.append(self.monkes[i].memorylist,0)
 
  def night(self):
    for i in range(len(self.monkes)):
      #for every agent, check it's food and strategy if it has more food
      monke = self.monkes[i]
      #print(self.monkes[i].id)
      if monke.zinda == True:      
        # Increase age
        monke.age+=1
        #print(monke.id)
        #monkes with insufficient food can't survive the iteration
        #adjusting the population matrix accordingly
        #print(monke.food)
        if monke.food<self.livereq:
          monke.zinda = False
          self.currpop[monke.monke_type] -= 1
        else:
          monke.food -= self.livereq
          #mmm... monke
        if monke.food>=self.reproductionreq:
          #a new monke inherits its monke_type from its parent monke
          self.add_to_memory_list()
          self.monkes.append(Monke(monke.monke_type))
          self.monkes[-1].id = sum(self.currpop)
          self.buildmemory(len(self.monkes)-1)
          self.currpop[monke.monke_type] += 1
          monke.food -= self.reproductionreq
 
  def refreshmemory(self):
    for i in range(len(self.monkes)):
      monke = self.monkes[i]
      if monke.monke_type == 3 and monke.zinda == True and monke.age % 30 == 0 and monke.age != 0:
        if monke.food > self.memorycost:
          monke.food -= self.memorycost
        else:
          self.buildmemory(monke)
 
  def iterate(self, numit = 4):
    for i in range(numit):
      self.monkesontrees = 0
      self.assign_rand_pos()
      self.interactions()
      print(self.monkesontrees)
      self.clearTrees()
    self.night()
    self.refreshmemory()  
 
  def run(self, num_iterate):
    for i in range(num_iterate):
      self.iterate()
      self.pop_hist.append(self.currpop)
      print(f'Iteration {i}/{num_iterate}: Population = {self.currpop}')

e = Environment()

monkes = []
for i in range(10):
  monkes.append((Monke(0)))
for i in range(15):
  monkes.append(Monke(1))
for i in range(7):
  monkes.append(Monke(2))
for i in range(10):
  monkes.append(Monke(3))

e.setup(monkes)
e.run(20)
