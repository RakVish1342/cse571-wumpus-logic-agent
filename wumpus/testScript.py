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

print (">> axiom_generator_wumpus_and_stench")
x = 1
y = 1
xmin = 1
xmax = 4
ymin = 1
ymax = 3
kb.axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax)
print ("-----")


#'''
print (">> generate_wumpus_and_stench_axioms")
xmin = 1
xmax = 4
ymin = 1
ymax = 3
kb.generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax)
print ("-----")
#'''

#'''
print (">> axiom_generator_at_least_one_wumpus")
xmin = 1
xmax = 4
ymin = 1
ymax = 3
kb.axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax)
print ("-----")
#'''

#'''
print (">> axiom_generator_at_most_one_wumpus")
xmin = 1
xmax = 4
ymin = 1
ymax = 3
kb.axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax)
print ("-----")
#'''

print (">> axiom_generator_only_in_one_location")
t=0
xi = 1
yi = 1
xmin = 1
xmax = 4
ymin = 1
ymax = 3
kb.axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t)
print ("-----")

print (">> axiom_generator_only_one_heading")
t=0
heading = 'north'
kb.axiom_generator_only_one_heading(heading, t)
print ("-----")

print (">> axiom_generator_have_arrow_and_wumpus_alive")
t=0
kb.axiom_generator_have_arrow_and_wumpus_alive(t)
print ("-----")

print (">> axiom_generator_location_OK")
t = 0
x = 1
y = 1
kb.axiom_generator_location_OK(x, y, t)
print ("-----")


print (">> axiom_generator_breeze_percept_and_location_property")
t = 0
x = 1
y = 1
kb.axiom_generator_breeze_percept_and_location_property(x, y, t)
print ("-----")

print (">> axiom_generator_stench_percept_and_location_property")
t = 0
x = 1
y = 1
kb.axiom_generator_stench_percept_and_location_property(x, y, t)
print ("-----")


#ADD location ssa

print (">> axiom_generator_have_arrow_ssa")
t = 0
kb.axiom_generator_have_arrow_ssa(t)
print ("-----")

print (">> axiom_generator_wumpus_alive_ssa")
t = 0
kb.axiom_generator_wumpus_alive_ssa(t)
print ("-----")

print (">> axiom_generator_heading_north_ssa")
t = 0
kb.axiom_generator_heading_north_ssa(t)
print ("-----")

print (">> axiom_generator_heading_east_ssa")
t = 0
kb.axiom_generator_heading_east_ssa(t)
print ("-----")

print (">> axiom_generator_heading_south_ssa")
t = 0
kb.axiom_generator_heading_south_ssa(t)
print ("-----")

print (">> axiom_generator_heading_west_ssa")
t = 0
kb.axiom_generator_heading_west_ssa(t)
print ("-----")





