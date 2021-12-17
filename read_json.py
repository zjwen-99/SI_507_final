import json

cache_file = open('cuisine.json', 'r')
cache_file_contents = cache_file.read()
cache = json.loads(cache_file_contents)

cache_file2 = open('eighber.json', 'r')
cache_file_contents2 = cache_file2.read()
cache2 = json.loads(cache_file_contents2)
#print(cache2)


if __name__=="__main__": 
    
    preference = input('Do you have neighberhood preference? ')
    while True:
            if preference=='no':
                chosen_cuisine=input("what cuisine would you like? ")
                cache_cuisine=cache
                while True:
                    try:
                        resturant_list = cache_cuisine['cuisine'][chosen_cuisine]
                        #print(resturant_list)
                        break
                        
                    except:
                        chosen_cuisine = input("Invalid input, please select another cuisine ")
                
                chosen_rest = list(resturant_list.keys())
                for i in range(len(chosen_rest)):
                    print(str(i) +' ' +chosen_rest[i])
                selected_resturant_index = input("Which one to choose? ")
                selected_resturant = chosen_rest[int(selected_resturant_index)]
                resturant_address = list(resturant_list[selected_resturant])
                print(resturant_address[0])
                break  
                

            elif preference=='yes':
                chosen_neighberhood = input("Which neighberhood would you like to go? ")
                cache_neighber=cache2
                while True:
                    try:
                        resturant_list = cache_neighber['neighber'][chosen_neighberhood]
                        #print(resturant_list)
                        break
                        
                    except:
                        chosen_neighberhood = input("No resturants found for this neighberhood, please reenter another? ")
                
                chosen_rest = list(resturant_list.keys())
                for i in range(len(chosen_rest)):
                    print(str(i) +' ' +chosen_rest[i])
                selected_resturant_index = input("Which one to choose? ")
                selected_resturant = chosen_rest[int(selected_resturant_index)]
                resturant_address = list(resturant_list[selected_resturant])
                print(resturant_address[0])
                break
            else:
                preference=input('format wrong, please renter your preference? ')




