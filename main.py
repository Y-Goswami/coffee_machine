import json
import copy
import threading
import time

class Beverage(threading.Thread): 
    
    def __init__(self,beverage_name,beverage_ingredients): 
        threading.Thread.__init__(self)
        self.beverage_name = beverage_name
        self.beverage_ingredients = copy.deepcopy(beverage_ingredients)
    
    def run(self):
        machine(self.beverage_name,self.beverage_ingredients)

def machine(beverage_name,beverage_ingredients):                                                            #machine function
    time.sleep(1)                               
    threadLock.acquire()                                                                                    #locking thread
    #time.sleep(1)
    can_be_prepared = True                                                      
    for ingredient,quantity in beverage_ingredients.items():    
        if ingredient in all_ingredients:                                                                   #checking if ingredient is available in the default list of ingredients
            if all_ingredients[ingredient]<quantity:                                                        #if ingrredient is available, checking for sufficient quantity
                can_be_prepared = False                                     
                print(beverage_name, "cannot be prepared because",ingredient,"is not sufficient") 
                break
        else :
            print(beverage_name, "cannot be prepared because",ingredient,"is not available")
            can_be_prepared = False
            break
    if(can_be_prepared):                                                                                    #all conditions for beverage preparation are fullfilled
        for ingredient,quantity in beverage_ingredients.items():
            all_ingredients[ingredient] = all_ingredients[ingredient] - quantity                            #updating availabe quantity of ingredients
        print(beverage_name,"is prepared")      
    threadLock.release()                                                                                    #releasing thread
    
def refill(all_ingredients):
    for ingredient,quantity in all_ingredients.items():
        if quantity<=5:                                                                                     #assuming refill is necessary below 5ml
            print(ingredient,"is running low; press 1 to refill / any other number to ignore")                    
            choice = int(input())
            if choice == 1:
                all_ingredients[ingredient] = quantity + 200                                                #refilling with 200ml
        
    

input1 = open('test.json',)                                                                                 #taking input from test.json file
input1 = json.load(input1)
outlets = input1['machine']['outlets']['count_n']                                                           #number of outlets to serve drinks simultaneously
all_ingredients = input1['machine']['total_items_quantity']                                                 # all available ingredients
threadLock = threading.Lock()   
threads=[]                                                                                                  #to track all threads                                
threads_to_delete =[]                                                                                       #to delete specific threads after completion

for name in input1['machine']['beverages'] :                    
    thread = Beverage(name,input1['machine']['beverages'][name])                                            #creating threads
    threads.append(thread)                                                                                  #adding them to the tracking 'threads' list

while(threads):                                                                                             #loop will run untill all threads/beverges are covered
    threadcount = 0;                                                                                        #variable to control how many threads can run simultaneously

    for t in threads:                                                                                       #looping through each thread
        t.start()                                                                                           #starting thread for one beverage
        threads_to_delete.append(t)                                                                         #noting whcih thread is started for future references
        threadcount+=1
        if threadcount == outlets:                                                                          #maximum threads running simultaneously = number of outlets
            threadcount = 0
            break
        
    for t in threads_to_delete:                                                                             #looping over running threads
        t.join()                                                                                            #check for thread termination
        threads.remove(t)                                                                                   #removing thread from master tracker 'threads'

    threads_to_delete.clear()                                                                               #clearing helper list 

    refill(all_ingredients)                                                                                 #checking for refill of ingredients after each serve
        
