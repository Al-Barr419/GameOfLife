
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()

height = 2
width = 2
gameLength = 2
Propositions = []
#
for i in range(gameLength):
    Propositions.append([])


# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@constraint.at_least_one(E)
@proposition(E)
class AliveProposition:

    def __init__(self, height, width, time):
        self.width = width
        self.height = height
        self.time = time
    def __repr__(self):
        return f"A({self.height},{self.width},{self.time})"


for h in range(height):
    for w in range(width):
        for l in range(gameLength):
            Propositions[l].append(AliveProposition(h,w,l))
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
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
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
    print(Propositions)
