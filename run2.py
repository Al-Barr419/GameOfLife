
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()
height = 5
width = 5
gameLength = 2
Propositions = []
#
for i in range(gameLength):
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


for l in range(gameLength):
    for w in range(width):
        for h in range(height):    
            Propositions[l][w].append(AliveProposition(h,w,l))

Tester = AliveProposition("Barb","Barb","Barb")
# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
'''@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"
'''
# Call your variables whatever you want
'''
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")
'''

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

def findNeighbours3(pProp):
    w = pProp.row
    h = pProp.col
    t = pProp.time
    try:
        n1 = Propositions[t][w-1][h]
    except:
        n1 = Tester
    try:
        n2 = Propositions[t][w][h-1]
    except:
        n2 = Tester
    try:
        n3 = Propositions[t][w+1][h]
    except:
        n3 = Tester
    try:
        n4 = Propositions[t][w][h+1]
    except:
        n4 = Tester
    return ((~n1 & n2 & n3 & n4) | (n1 & ~n2 & n3 & n4) | (n1 & n2 & ~n3 & n4) | (n1 & n2 & n3 & ~n4))

#Checks if there are 2 or 3 neighbours.. 
def findNeighbours2V3(pProp):
    #Haivng 2 or 3 neighobours is the same as negation 0,1,4 neibhours. 
    w = pProp.row
    h = pProp.col
    t = pProp.time
    #gather neighbours, and catch if index is out of bounds. 
    try:
        n1 = Propositions[t][w-1][h]
    except:
        n1 = Tester
    try:
        n2 = Propositions[t][w][h-1]
    except:
        n2 = Tester
    try:
        n3 = Propositions[t][w+1][h]
    except:
        n3 = Tester
    try:
        n4 = Propositions[t][w][h+1]
    except:
        n4 = Tester
    return ~((~n1 & ~n2 & ~n3 & ~n4) | (n1 & ~n2 & ~n3 & ~n4) | (~n1 & n2 & ~n3 & ~n4) | (~n1 & ~n2 & n3 & ~n4) | (~n1 & ~n2 & ~n3 & n4) | (n1 & n2 & n3 & n4))

def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
    
    #Add constraint, where neighbours imply the next iteration.  
    E.add_constraint(~Tester)
    for x in range(gameLength-1):
        for y in range(width):
            for z in range(height):    
                A = Propositions[x][y][z]
                E.add_constraint(((A & findNeighbours2V3(A)) >> Propositions[x+1][y][z]))
                E.add_constraint(((~A & findNeighbours3(A)) >> ~Propositions[x+1][y][z]))

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions:ls %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())
    
