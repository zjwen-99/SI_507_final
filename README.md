# SI_507_final
This program is the final project of SI 507, which is scrawling cuisine and restaurants information in New York City from multiple pages of a website. By implementing the interactive command line, users could enter their preference and the program will provide them related options for users, including the names of restaurant and its location for a specific type of cuisine or neighborhood. 

Data source:
https://www.nyc.com/restaurants/

User Instructions:
To get started, user need to run the tree_generation.py file to generate trees in json file. Then, running read_json.py file and user options will be displayed in the command line.

Data Structure:
In the final project, tree is used to store the scrawled data in json file. There are two trees structures used in this project, the first tree is used to store the cuisine data and corresponding restaurants and restaurants’ address. The root node is defined as cuisine, and child nodes of the root is the name of the cuisine. Finally, the child nodes of each restaurant are addresses. Similarly, for the neighborhood side, for the second tree, root is defined as neighborhood, and child nodes of the root are names of neighborhood, and child of the neighborhood is the corresponding restaurant. Finally, restaurants addresses are defined as the leaf.


