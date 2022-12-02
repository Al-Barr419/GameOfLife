
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from visualizer import create_visualization

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()


height = 4
width = 4
gameLength = 5
Propositions = []
constraintType = "normal" #normal, reverse, atLeast1, totalSolutions in order for which rules to use. 


for i in range(gameLength+1):
    Propositions.append([])
    for w in range(width):
        Propositions[i].append([])


# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding

@proposition(E)
class AliveProposition:
    def __init__(self, height, width, time):
        self.row = width
        self.col = height
        self.time = time
    def __repr__(self):
        return f"A({self.time},{self.row},{self.col})"


for l in range(gameLength+1):
    for w in range(width):
        for h in range(height):    
            Propositions[l][w].append(AliveProposition(h,w,l))


Tester = AliveProposition("Barb","Barb","Barb")
# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

def findNeighbours3(pProp):
    w = pProp.row
    h = pProp.col
    t = pProp.time
    
    if w == 0:
        n1 = Tester
    else:
        n1 = Propositions[t][w-1][h]
    if h == 0:
        n2 = Tester
    else:
        n2 = Propositions[t][w][h-1]
        
    if w == width-1:
        n3 = Tester
    else:
        n3 = Propositions[t][w+1][h]

    if h == height-1:
        n4 = Tester
    else:
        n4 = Propositions[t][w][h+1]

    return ((~n1 & n2 & n3 & n4) | (n1 & ~n2 & n3 & n4) | (n1 & n2 & ~n3 & n4) | (n1 & n2 & n3 & ~n4))

#Checks if there are 2 or 3 neighbours.. 
def findNeighbours2V3(pProp):
    #Haivng 2 or 3 neighobours is the same as negation 0,1,4 neibhours. 
    w = pProp.row
    h = pProp.col
    t = pProp.time
    #gather neighbours, and catch if index is out of bounds. 
    if w == 0:
        n1 = Tester
    else:
        n1 = Propositions[t][w-1][h]
    if h == 0:
        n2 = Tester
    else:
        n2 = Propositions[t][w][h-1]
    if w == width-1:
        n3 = Tester
    else:
        n3 = Propositions[t][w+1][h]
    if h == height-1:
        n4 = Tester
    else:
        n4 = Propositions[t][w][h+1]
    # The comment out return statement is an alternate equivalent version of the current version we used for testing, 
    # It is equal to ~(0,1, or 4 neibhours), this should be equivalent to (2 or 3 neighbours)  
    # return ~((~n1 & ~n2 & ~n3 & ~n4) | (n1 & ~n2 & ~n3 & ~n4) | (~n1 & n2 & ~n3 & ~n4) | (~n1 & ~n2 & n3 & ~n4) | (~n1 & ~n2 & ~n3 & n4) | (n1 & n2 & n3 & n4))
    return  (n1 & n2 & ~n3 & ~n4)|(n1 & ~n2 & n3 & ~n4)|(n1 & ~n2 & ~n3 & n4)| (~n1 & n2 & ~n3 & n4)|(~n1 & n2 & n3 & ~n4)|(n1 & n2 & ~n3 & ~n4)| (~n1 & ~n2 & n3 & n4)|(~n1 & n2 & n3 & ~n4)|(n1 & ~n2 & n3 & ~n4)| (~n1 & ~n2 & n3 & n4)|(~n1 & n2 & ~n3 & n4)|(n1 & ~n2 & ~n3 & n4)| ((~n1 & n2 & n3 & n4) | (n1 & ~n2 & n3 & n4) | (n1 & n2 & ~n3 & n4) | (n1 & n2 & n3 & ~n4))
def example_theory():
    #Add constraint, where neighbours imply the next iteration.  
    E.add_constraint(~Tester)

    if constraintType == "normal":
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):    
                    A = Propositions[x][y][z]
                    #Constraints Defining the rules of the game
                    E.add_constraint(((~A & findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
        for q in range(width):
            for w in range(height):
                #Stable State Constraints,
                E.add_constraint(Propositions[gameLength-1][q][w]>> Propositions[gameLength][q][w])
                E.add_constraint(~Propositions[gameLength-1][q][w]>> ~Propositions[gameLength][q][w])
        return E

    elif constraintType == "reverse":
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):    
                    #Constraints Defining the rules of the game
                    A = Propositions[x][y][z]
                    E.add_constraint(((~A & findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> Propositions[x+1][y][z]))

        for q in range(width):
            for w in range(height):
                #Constraints For Stable State, 
                E.add_constraint(Propositions[gameLength-1][q][w]>> Propositions[gameLength][q][w])
                E.add_constraint(~Propositions[gameLength-1][q][w]>> ~Propositions[gameLength][q][w])
        return E

    elif constraintType == "atLeast1":
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):    
                    #Constraints Defining the rules of the game
                    A = Propositions[x][y][z]
                    E.add_constraint(((~A & findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
                    
        for q in range(width):
            for w in range(height):
                #Stable State Constraints
                E.add_constraint(Propositions[gameLength-1][q][w]>> Propositions[gameLength][q][w])
                E.add_constraint(~Propositions[gameLength-1][q][w]>> ~Propositions[gameLength][q][w])
        constraint.add_at_least_one(E, Propositions[gameLength-1])
        
        return E

    elif constraintType == "totalSolutions":
        for x in range(gameLength):
            for y in range(width):
                for z in range(height):   
                    #Constraints Defining the rules of the game
                    A = Propositions[x][y][z]
                    E.add_constraint(((~A & findNeighbours3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((~A & ~findNeighbours3(A)) >> ~Propositions[x+1][y][z]))
                    E.add_constraint(((A & findNeighbours2V3(A)) >> Propositions[x+1][y][z]))
                    E.add_constraint(((A & ~findNeighbours2V3(A)) >> ~Propositions[x+1][y][z]))
        return E



if __name__ == "__main__":
    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions:ls %d" % count_solutions(T))
   # print("   Solution: %s" % T.solve())
    create_visualization(T.solve(), Propositions)
    
    #print(E.introspect(T.solve()))
    
