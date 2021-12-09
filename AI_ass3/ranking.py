from z3 import *

l1,l2,l3,l4 = Bool('Lisa Rank 1'),Bool('Lisa Rank 2'),Bool('Lisa Rank 3'),Bool('Lisa Rank 4')
b1,b2,b3,b4 = Bool('Bob Rank 1'),Bool('Bob Rank 2'),Bool('Bob Rank 3'),Bool('Bob Rank 4')
j1,j2,j3,j4 = Bool('Jim Rank 1'),Bool('Jim Rank 2'),Bool('Jim Rank 3'),Bool('Jim Rank 4')
m1,m2,m3,m4 = Bool('Mary Rank 1'),Bool('Mary Rank 2'),Bool('Mary Rank 3'),Bool('Mary Rank 4')

s = Solver()

### Constraints of ranking
s.add(
    # One person can only have one rank
    Sum([If(i,1,0) for i in [l1,l2,l3,l4]]) == 1,
    Sum([If(i,1,0) for i in [b1,b2,b3,b4]]) == 1,
    Sum([If(i,1,0) for i in [j1,j2,j3,j4]]) == 1,
    Sum([If(i,1,0) for i in [m1,m2,m3,m4]]) == 1,

    # One position can only have one person
    Sum([If(i,1,0) for i in [l1,b1,j1,m1]]) == 1,
    Sum([If(i,1,0) for i in [l2,b2,j2,m2]]) == 1,
    Sum([If(i,1,0) for i in [l3,b3,j3,m3]]) == 1,
    Sum([If(i,1,0) for i in [l4,b4,j4,m4]]) == 1,
)

lm,mm = Bool('Lisa is a biology major'), Bool('Mary is a biology major')

## Fact 1
s.add( 
    Not(And(l1,b2)),Not(And(b1,l2)),Not(And(l2,b3)),Not(And(b2,l3)),Not(And(l3,b4)),Not(And(b3,l4))
)

### Fact 2
s.add(
    Implies(lm,Or(
        And(j1,l2),And(j2,l3),And(j3,l4)
    ))
)
s.add(
    Implies(mm,Or(
        And(j1,m2),And(j2,m3),And(j3,m4)
    ))
)

### Fact3
s.add(
    Or(
        And(b1,j2),And(b2,j3),And(b3,j4)
    )
)

### Fact4
s.add(
    Or(
        And(lm,Not(mm)),And(Not(lm),mm)
    )
)

### Fact5
s.add(
    Or(
        l1,m1
    )
)

print(s.check())

model = s.model()
[print(var, '= True') for var in model.decls() if model[var] == True]

# The answer is (Mary,Bob,Jim,Lisa)