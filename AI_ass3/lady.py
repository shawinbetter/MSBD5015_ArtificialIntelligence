from z3 import *

#indicates whether a lady in current room.
#e.g. l1 means lady in Room I
l1,l2,l3 = Bool('l1'),Bool('l2'),Bool('l3')
s = Solver()

## Add constraint: Either lady or tiger in a room
s.add(Or(And(l1,Not(l2),Not(l3)),
         And(Not(l1),l2,Not(l3)),
         And(Not(l1),Not(l2),l3)))
 

## Add constraint: At most one of three signs are true
p1 = Not(l1)
p2 = l2
p3 = Not(l2)
s.add(Or(And(Not(p1),Not(p2),Not(p3)),
         And(Not(p1),Not(p2),p3),
         And(Not(p1),p2,Not(p3)),
         And(p1,Not(p2),Not(p3))  
         ))

print(s.check())
print(s.model()) #[l3 = False, l1 = True, l2 = False]

##This is my answer,lady in Room I
s.add(Not(l1))

#Add the negation will lead to unsat
print(s.check())#unsat

