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
