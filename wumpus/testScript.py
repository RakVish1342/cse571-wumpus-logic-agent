import wumpus_kb as kb


print(">> axiom_generator_percept_sentence")
t = 0
tvec = [False, True, False, False, True]
kb.axiom_generator_percept_sentence(t, tvec)
print ("-----")


print (">> axiom_generator_initial_location_assertions")
x = 1
y = 1
kb.axiom_generator_initial_location_assertions(x, y)
print ("-----")

print (">> axiom_generator_pits_and_breezes")
x = 1
y = 1
xmin = 1
xmax = 4
ymin = 1
ymax = 3
kb.axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax)
print ("-----")


#'''
print (">> generate_pit_and_breeze_axioms")
xmin = 1
xmax = 4
ymin = 1
ymax = 3
kb.generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax)
print ("-----")
#'''
