# wumpus_kb.py
# ------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

import utils

falseSymb = '~'

#-------------------------------------------------------------------------------
# Wumpus Propositions
#-------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']

def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)

### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)

proposition_bases_location_fluents = ['OK', 'L']

def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)

def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))

proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']

def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)
def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)
def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)
def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)

proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']

def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)

proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------

#def make_percept_sentence(t, tvec):
def axiom_generator_percept_sentence(t, tvec):
    """
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    conjuncts = ['']*len(tvec)

    # tvec[0]==0 ? (conjuncts[0] = percept_stench_str(t)) : (conjuncts[0] = falseSymb+percept_stench_str(t))
    conjuncts[0] = percept_stench_str(t) if tvec[0] else falseSymb+percept_stench_str(t)
    conjuncts[1] = percept_breeze_str(t) if tvec[1] else falseSymb+percept_breeze_str(t)
    conjuncts[2] = percept_glitter_str(t) if tvec[2] else falseSymb+percept_glitter_str(t)
    conjuncts[3] = percept_bump_str(t) if tvec[3] else falseSymb+percept_bump_str(t)
    conjuncts[4] = percept_scream_str(t) if tvec[4] else falseSymb+percept_scream_str(t)
    # print conjuncts

    for i in range(len(conjuncts)):
        if(i == len(conjuncts)-1):
            axiom_str += conjuncts[i]
        else:
            axiom_str += conjuncts[i] + ' & '

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

#-------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
#-------------------------------------------------------------------------------

def axiom_generator_initial_location_assertions(x, y):
    """
    Assert that there is no Pit and no Wumpus in the location

    x,y := the location
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str = falseSymb + pit_str(x, y) + ' & ' + falseSymb + wumpus_str(x, y)

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Section 7.7 of AIMA, starting on page 265
    # Bx,y <=> Pij | P(i+1)j | P(i-1)j | Pi(j+1) | Pi(j-1) for all valid i and j
    axiom_str = breeze_str(x,y) + ' <=> '

    axiom_str += ' ( ' # overall bracket for RHS to prevent clubbing just the first term with the bidirectional
    testLoc = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)] # should also include same location also as per docs above
    for i in range(len(testLoc)):
        loc = testLoc[i]
        # if the location is valid grid location
        if (loc[0] >= xmin and loc[0] <= xmax and loc[1] >= ymin and loc[1] <= ymax):
            axiom_str += pit_str(loc[0], loc[1]) + ' | '

    # remove the last OR symbol
    if axiom_str[-3 :] == ' | ':
        axiom_str = axiom_str[:-3]
    axiom_str += ' ) ' # overall bracket for RHS to prevent clubbing just the first term with the bidirectional

    # # if none of the grid locations were valid and just the breeze_str_xy <=> gets generated, return empty string ''
    # if axiom_str[-5 :] == ' <=> ':
    #     axiom_str = ''
    
    # print(axiom_str)

    return axiom_str

def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')
    return axioms

def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)

    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Similar to Breeze and Pit
    # axiom_str = wumpus_str(x,y) + ' <=> '
    axiom_str = stench_str(x,y) + ' <=> '

    axiom_str += ' ( ' # overall bracket for RHS to prevent clubbing just the first term with the bidirectional
    testLoc = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)] # should also include same location also as per docs above
    for i in range(len(testLoc)):
        loc = testLoc[i]
        if (loc[0] >= xmin and loc[0] <= xmax and loc[1] >= ymin and loc[1] <= ymax):
            # axiom_str += stench_str(loc[0], loc[1]) + ' | '
            axiom_str += wumpus_str(loc[0], loc[1]) + ' | '

    # remove the last OR symbol
    if axiom_str[-3 :] == ' | ':
        axiom_str = axiom_str[:-3]
    axiom_str += ' ) ' # overall bracket for RHS to prevent clubbing just the first term with the bidirectional        

    # # if none of the grid locations were valid and just the breeze_str_xy <=> gets generated, return empty string ''
    # if axiom_str[-5 :] == ' <=> ':
    #     axiom_str = ''
    
    # print(axiom_str) 

    return axiom_str

def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms

def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at least one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    # At least one Wumpus means any one location in the valid range should have a Wumpus.
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            # if ( (x != 1) and (y != 1) ): # Exclude the location 1,1 as it won't have wumpus by definition
            if ( not ( (x == 1) and (y == 1)) ): # Exclude the location 1,1 as it won't have wumpus by definition
                axiom_str += wumpus_str(x,y) + ' | '

    if axiom_str[-3 :] == ' | ':
        axiom_str = axiom_str[:-3]     

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at at most one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    # I feel can be done as: (((W11 XOR W21) XOR W31) XOR W41) XOR ... where XOR is ^ symbol as neen from logic.py file
    # where A XOR B = (A NAND B) AND (A OR B)
    # This however takes tooooooo long to get evaluated. 
    # Similarly, enumerating all conditions like: (~Wij & ~Wij & ~Wij) | (Wij & ~Wij & ~Wij) | (~Wij & Wij & ~Wij) | (~Wij & ~Wij & Wij)
    # viz basically to state that 0 or 1 number of wumpus can be alive also takes toooo long for evaluation

    # Reason for length of the execution when the main connectives are OR conditions is that now it needs to evauate all the clauses to 
    # understand if the entire statement is effectively true or false.
    
    # Therefore following textbook, take all combos of locations and check (~Wij OR ~Wij) AND (~Wij OR ~Wij) AND .... for all combos

    # Trying textbook method first as that is probably more likely to work since it is given.

    # Store all coords as a list
    coords = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            coords.append((x,y))
    
    # extract pairs of coords from the list
    for i in range(len(coords) - 1): # From 0 till end-1
        for j in range(i+1, len(coords)): # From i + 1 till end
            # print ( (coords[i], coords[j]) )
             # Exclude pairs that work with the (1,1) location, as it won't have wumpus by definition
            # if ( ((coords[i][0] != 1) and (coords[i][1] != 1)) or ((coords[j][0] != 1) and (coords[j][1] != 1)) ):
            if ( not ( ((coords[i][0] == 1) and (coords[i][1] == 1)) or ((coords[j][0] == 1) and (coords[j][1] == 1)) ) ):
                axiom_str += ' ( ' + \
                    (falseSymb + wumpus_str(coords[i][0], coords[i][1])) + \
                    ' | ' + \
                    (falseSymb + wumpus_str(coords[j][0], coords[j][1])) + \
                    ' ) ' + \
                    ' & '

    if axiom_str[-3 :] == ' & ':
        axiom_str = axiom_str[:-3]          

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t = 0):
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.

    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            # Allow location if it is current xi, yi location
            if (x == xi and y == yi):
                axiom_str += state_loc_str(x,y,t) + ' & '
            # Else negate it/state other locations are false
            else:
                axiom_str += falseSymb + state_loc_str(x,y,t) + ' & '

    if axiom_str[-3 :] == ' & ':
        axiom_str = axiom_str[:-3]

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_only_one_heading(heading = 'north', t = 0):
    """
    Assert that Agent can only head in one direction at a time.

    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str += state_heading_north_str(t) if heading == 'north' else falseSymb + state_heading_north_str(t)
    axiom_str += ' & '
    axiom_str += state_heading_east_str(t) if heading == 'east' else falseSymb + state_heading_east_str(t)
    axiom_str += ' & '
    axiom_str += state_heading_south_str(t) if heading == 'south' else falseSymb + state_heading_south_str(t)
    axiom_str += ' & '
    axiom_str += state_heading_west_str(t) if heading == 'west' else falseSymb + state_heading_west_str(t)

    # print(axiom_str) 

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_have_arrow_and_wumpus_alive(t = 0):
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    axiom_str += state_have_arrow_str(t) + ' & ' +  state_wumpus_alive_str(t)

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str


def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    #utils.print_not_implemented()
    """
    Generate all of the initial wumpus axioms

    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))

    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())

    return axioms


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------

def axiom_generator_location_OK(x, y, t):
    """
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    #?? Any additional conditions? ie. should I use stench, breeze percepts to conclude if this spot is safe?
    #?? More Wumpus based checks needed? Just need to look for "alive" wumpus at that location. Fine to go to the location if wumpus is dead

    #?? Also look at other cases so far and see if I need to use a double or single implication anywhere
    #?? Also include the overall generation_... functions so that sentences are created for all states/x/y vals generated by that generation function?
    #?? Exclude (1,1) from the At least one wumpus and at most one wumpus functions? Since wumpus can not be in 1,1 by definition? Even if included, this should not affect the statement


    # no wumpus in that location OR
    # wumpus in that location AND dead
    # AND no pit in that location
    # axiom_str = state_OK_str(x,y,t) + ' <=> ' + \
    #     ' ( ' + \
    #     ' ( ' + falseSymb + wumpus_str(x,y) + ' ) ' + ' | ' + \
    #     ' ( ' + wumpus_str(x,y) + ' & ' + falseSymb + state_wumpus_alive_str(t) +  ' ) ' + \
    #     ' ) ' + \
    #     ' & ' + \
    #     falseSymb + pit_str(x,y)

    # As per textbook (pg. 268)
    axiom_str = state_OK_str(x,y,t) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + falseSymb + wumpus_str(x,y) + ' | ' + ' ( ' + wumpus_str(x,y) + ' & ' + falseSymb + state_wumpus_alive_str(t) + ' ) ' +  ' ) ' + \
        ' & ' + \
        falseSymb + pit_str(x,y) + \
        ' ) '
    # Old version:
        # ' ( ' + \
        # falseSymb + ' ( ' + wumpus_str(x,y) + ' & ' + state_wumpus_alive_str(t) +  ' ) ' + ' & ' + \
        # falseSymb + pit_str(x,y) + \
        # ' ) '

    # print(axiom_str)
     
    return axiom_str

def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')
    return filter(lambda s: s != '', axioms)

#-------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

def axiom_generator_breeze_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # From the testbook. Page 266, relating atemporals with temporals/fluents
    axiom_str = state_loc_str(x,y,t) + ' >> ' + ' ( ' + percept_breeze_str(t) + ' <=> ' + breeze_str(x,y) + ' ) '

    # print(axiom_str)

    return axiom_str

def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return filter(lambda s: s != '', axioms)

def axiom_generator_stench_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # From the testbook. Page 266, relating atemporals with temporals/fluents
    axiom_str = state_loc_str(x,y,t) + ' >> ' + ' ( ' + percept_stench_str(t) + ' <=> ' + stench_str(x,y) + ' ) '

    # print(axiom_str)

    return axiom_str

def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!
def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.
    
    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    # bumpMoveStr = 
    nonMoveActionStr = falseSymb + action_forward_str(t) +  ' | ' + action_grab_str(t)  +  ' | ' + action_shoot_str(t)  + \
        ' | ' + action_wait_str(t)  +  ' | ' + action_turn_left_str(t) +  ' | ' + action_turn_right_str(t)

    # Central Tiles
    if( (x-1 >= xmin) and (x+1 <= xmax) and (y-1 >= ymin) and (y+1 <= ymax) ): # All ranges lie in valid space/limits
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x-1,y,t) + ' & ' + ' ( ' + state_heading_east_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x+1,y,t) + ' & ' + ' ( ' + state_heading_west_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y-1,t) + ' & ' + ' ( ' + state_heading_north_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y+1,t) + ' & ' + ' ( ' + state_heading_south_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '

    # Corner Tiles
    # Lower Left
    elif( (x-1 < xmin) and (y-1 < ymin) ):
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x+1,y,t) + ' & ' + ' ( ' + state_heading_west_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y+1,t) + ' & ' + ' ( ' + state_heading_south_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '
    # Upper Left
    elif( (x-1 < xmin) and (y+1 > ymax) ):
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x+1,y,t) + ' & ' + ' ( ' + state_heading_west_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y-1,t) + ' & ' + ' ( ' + state_heading_north_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '
    # Upper Right
    elif( (x+1 > xmax) and (y+1 > ymax) ):
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x-1,y,t) + ' & ' + ' ( ' + state_heading_east_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y-1,t) + ' & ' + ' ( ' + state_heading_north_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '
    # Lower Right
    elif( (x+1 > xmax) and (y-1 < ymin) ):
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x-1,y,t) + ' & ' + ' ( ' + state_heading_east_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y+1,t) + ' & ' + ' ( ' + state_heading_south_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '

    # Edge Tiles
    # Lower Edge
    elif( (x-1 >= xmin) and (x+1 <= xmax) and (y-1 < ymin) ): # only x lies in the valid space
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x-1,y,t) + ' & ' + ' ( ' + state_heading_east_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x+1,y,t) + ' & ' + ' ( ' + state_heading_west_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y+1,t) + ' & ' + ' ( ' + state_heading_south_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '
    # Upper Edge
    elif( (x-1 >= xmin) and (x+1 <= xmax) and (y+1 > ymax) ): # only x lies in the valid space
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x-1,y,t) + ' & ' + ' ( ' + state_heading_east_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x+1,y,t) + ' & ' + ' ( ' + state_heading_west_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y-1,t) + ' & ' + ' ( ' + state_heading_north_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '
    # Left Edge
    elif( (x-1 < xmin) and (y+1 >= ymin) and (y+1 <= ymax) ): # only y lies in the valid space
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x+1,y,t) + ' & ' + ' ( ' + state_heading_west_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y-1,t) + ' & ' + ' ( ' + state_heading_north_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y+1,t) + ' & ' + ' ( ' + state_heading_south_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '
    # Right Edge
    elif( (x+1 > xmax) and (y+1 >= ymin) and (y+1 <= ymax) ): # only y lies in the valid space
        axiom_str += state_loc_str(x,y,t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_loc_str(x-1,y,t) + ' & ' + ' ( ' + state_heading_east_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y-1,t) + ' & ' + ' ( ' + state_heading_north_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y+1,t) + ' & ' + ' ( ' + state_heading_south_str(t) + ' & ' + action_forward_str(t) + ' ) ' + ' ) ' + ' | ' + \
        ' ( ' + state_loc_str(x,y,t) + ' & ' + ' ( ' + percept_bump_str(t+1) + ' | ' + nonMoveActionStr + ' ) ' + ' ) ' + \
        ' ) '

    # print(axiom_str)

    return axiom_str

def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    #utils.print_not_implemented()
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_at_location_ssa')
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_have_arrow_ssa(t):
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str = state_have_arrow_str(t+1) + ' <=> ' + ' ( ' + state_have_arrow_str(t) + ' & ' + ' ( ' + falseSymb+action_shoot_str(t) + ' ) ' + ' ) '

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

    (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # axiom_str = state_wumpus_alive_str(t+1) + '<=>' + \
    #     ' ( ' + state_wumpus_alive_str(t) +  ' & ' + falseSymb+percept_scream_str(t) + ' ) '
    # t+1 for scream since wumpus will scream in next time step, also, this t+1 should be valid since
    # Location ssa on page 267 Eqn. 7.3 uses Bump_t+1 
    # And s_manual says in previous edition, a combo of wumpus_alive and scream was used. The only reason it was 
    # replaced with more complex arrow related action was because wumpus_alive and scream combo could not be used 
    # for future planning (as it was a timestep too slow), and it could only be used for perception.
    axiom_str = state_wumpus_alive_str(t+1) + ' <=> ' + \
        ' ( ' + state_wumpus_alive_str(t) +  ' & ' + falseSymb+percept_scream_str(t+1) + ' ) '

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

#----------------------------------


def axiom_generator_heading_north_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    # axiom_str += \
    #     state_heading_north_str(t+1) + ' <=> ' + \
    #     ' ( ' + \
    #     ' ( ' + state_heading_north_str(t) + ' & ' + \
    #     ' ( ' + \
    #     falseSymb + action_turn_left_str(t) + ' & ' + falseSymb + action_turn_right_str(t) + ' & ' + \
    #     ' ( ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + action_wait_str(t) + ' | ' + action_forward_str(t) + ' | ' + percept_bump_str(t) + ' ) ' +  ' ) ' + \
    #     ' ) ' + \
    #     ' | '  \
    #     ' ( ' + state_heading_west_str(t) + ' & ' + action_turn_right_str(t) +  ' ) ' + ' | ' + \
    #     ' ( ' + state_heading_east_str(t) + ' & ' + action_turn_left_str(t) +  ' ) ' + \
    #     ' ) '
    axiom_str += \
        state_heading_north_str(t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_heading_north_str(t) + ' & ' + \
        ' ( ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + action_wait_str(t) + ' | ' + action_forward_str(t) + ' | ' + percept_bump_str(t) + ' ) ' +  ' ) ' + \
        ' | '  \
        ' ( ' + state_heading_west_str(t) + ' & ' + action_turn_right_str(t) +  ' ) ' + ' | ' + \
        ' ( ' + state_heading_east_str(t) + ' & ' + action_turn_left_str(t) +  ' ) ' + \
        ' ) '


    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_heading_east_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    axiom_str += \
        state_heading_east_str(t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_heading_east_str(t) + ' & ' + \
        ' ( ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + action_wait_str(t) + ' | ' + action_forward_str(t) + ' | ' + percept_bump_str(t) + ' ) ' +  ' ) ' + \
        ' | '  \
        ' ( ' + state_heading_north_str(t) + ' & ' + action_turn_right_str(t) +  ' ) ' + ' | ' + \
        ' ( ' + state_heading_south_str(t) + ' & ' + action_turn_left_str(t) +  ' ) ' + \
        ' ) '

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_heading_south_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be South at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    axiom_str += \
        state_heading_south_str(t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_heading_south_str(t) + ' & ' + \
        ' ( ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + action_wait_str(t) + ' | ' + action_forward_str(t) + ' | ' + percept_bump_str(t) + ' ) ' +  ' ) ' + \
        ' | '  \
        ' ( ' + state_heading_east_str(t) + ' & ' + action_turn_right_str(t) +  ' ) ' + ' | ' + \
        ' ( ' + state_heading_west_str(t) + ' & ' + action_turn_left_str(t) +  ' ) ' + \
        ' ) '

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_heading_west_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    axiom_str += \
        state_heading_west_str(t+1) + ' <=> ' + \
        ' ( ' + \
        ' ( ' + state_heading_west_str(t) + ' & ' + \
        ' ( ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + action_wait_str(t) + ' | ' + action_forward_str(t) + ' | ' + percept_bump_str(t) + ' ) ' +  ' ) ' + \
        ' | '  \
        ' ( ' + state_heading_south_str(t) + ' & ' + action_turn_right_str(t) +  ' ) ' + ' | ' + \
        ' ( ' + state_heading_north_str(t) + ' & ' + action_turn_left_str(t) +  ' ) ' + \
        ' ) '

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str


def generate_heading_ssa(t):

    #utils.print_not_implemented()
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]

def generate_non_location_ssa(t):
    #utils.print_not_implemented()
    """
    Generate all non-location-based SSAs
    """
    axioms = [] # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_heading_only_north(t):
    """
    Assert that when heading is North, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str += state_heading_north_str(t) + ' <=> ' + \
        '(' + \
        falseSymb + ' ( ' + state_heading_south_str(t) + ' | ' + state_heading_east_str(t) + \
        ' | ' +  state_heading_west_str(t) + ' ) ' + \
        ')'

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_heading_only_east(t):
    """
    Assert that when heading is East, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str += state_heading_east_str(t) + ' <=> ' + \
        '(' + \
        falseSymb + ' ( ' + state_heading_south_str(t) + ' | ' + state_heading_north_str(t) + \
        ' | ' +  state_heading_west_str(t) + ' ) ' + \
        ')'

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_heading_only_south(t):
    """
    Assert that when heading is South, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str += state_heading_south_str(t) + ' <=> ' + \
        '(' + \
        falseSymb + ' ( ' + state_heading_east_str(t) + ' | ' + state_heading_north_str(t) + \
        ' | ' +  state_heading_west_str(t) + ' ) ' + \
        ')'


    # print(axiom_str)
    
    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented() 
    return axiom_str

def axiom_generator_heading_only_west(t):
    """
    Assert that when heading is West, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str += state_heading_west_str(t) + ' <=> ' + \
        '(' + \
        falseSymb + ' ( ' + state_heading_east_str(t) + ' | ' + state_heading_north_str(t) + \
        ' | ' +  state_heading_south_str(t) + ' ) ' + \
        ')'

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def generate_heading_only_one_direction_axioms(t):
    #utils.print_not_implemented()
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]


def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.
    
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # OLD Implementation with Full and Explicit Clauses
    # axiom_str += \
    # ' ( ' + action_forward_str(t) + ' <=> ' + '(' + falseSymb + ' ( ' + action_climb_str(t) + ' | ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + \
    #     action_turn_left_str(t) + ' | ' + action_turn_right_str(t) + ' | ' + action_wait_str(t) + ' ) ' + ' ) '  + ')'
    # axiom_str += ' & '

    # axiom_str += \
    # ' ( ' + action_climb_str(t) + ' <=> ' + '(' + falseSymb + ' ( ' + action_forward_str(t) + ' | ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + \
    #     action_turn_left_str(t) + ' | ' + action_turn_right_str(t) + ' | ' + action_wait_str(t) + ' ) ' + ' ) ' + ')'
    # axiom_str += ' & '        

    # axiom_str += \
    # ' ( ' + action_grab_str(t) + ' <=> ' + '(' + falseSymb + ' ( ' + action_climb_str(t) + ' | ' + action_forward_str(t) + ' | ' + action_shoot_str(t) + ' | ' + \
    #     action_turn_left_str(t) + ' | ' + action_turn_right_str(t) + ' | ' + action_wait_str(t) + ' ) ' + ' ) ' + ')'
    # axiom_str += ' & '

    # axiom_str += \
    # ' ( ' + action_shoot_str(t) + ' <=> ' + '(' + falseSymb + ' ( ' + action_climb_str(t) + ' | ' + action_grab_str(t) + ' | ' + action_forward_str(t) + ' | ' + \
    #     action_turn_left_str(t) + ' | ' + action_turn_right_str(t) + ' | ' + action_wait_str(t) + ' ) ' + ' ) ' + ')'
    # axiom_str += ' & '  

    # axiom_str += \
    # ' ( ' + action_turn_left_str(t) + ' <=> ' + '(' + falseSymb + ' ( ' + action_climb_str(t) + ' | ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + \
    #     action_forward_str(t) + ' | ' + action_turn_right_str(t) + ' | ' + action_wait_str(t) + ' ) ' + ' ) ' + ')'
    # axiom_str += ' & '

    # axiom_str += \
    # ' ( ' + action_turn_right_str(t) + ' <=> ' + '(' + falseSymb + ' ( ' + action_climb_str(t) + ' | ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + \
    #     action_turn_left_str(t) + ' | ' + action_forward_str(t) + ' | ' + action_wait_str(t) + ' ) ' + ' ) ' + ')'
    # axiom_str += ' & '

    # axiom_str += \
    # ' ( ' + action_wait_str(t) + ' <=> ' + '(' + falseSymb + ' ( ' + action_climb_str(t) + ' | ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + \
    #     action_turn_left_str(t) + ' | ' + action_turn_right_str(t) + ' | ' + action_forward_str(t) + ' ) ' + ' ) ' + ')'

    # Similar to At Most One Wumpus, here also evaluation time is really large if OR conditions are used. So, need to try to encode it in pairs:
    # So, similar to (at_least_one_wumpus)  AND (at_most_one_wumpus) that was done in textbook to make sure the result was exactly_one_wumpus, here also 
    # should do the same.

    def getActStr(act, t):
        if act == 'Forward':
            return action_forward_str(t)
        elif act == 'Grab':
            return action_grab_str(t)
        elif act == 'Shoot':
            return action_shoot_str(t)
        elif act == 'Climb':
            return action_climb_str(t)
        elif act == 'TurnLeft':
            return action_turn_left_str(t)
        elif act == 'TurnRight':
            return action_turn_right_str(t)
        elif act == 'Wait':
            return action_wait_str(t)
        else:
            print(">>> ERROR: ACTION in wumpus_kb.py NOT FOUND")
            return None

    # At least one action:
    axiom_str += '(' + action_forward_str(t) + ' | ' + action_grab_str(t) + ' | ' + action_shoot_str(t) + ' | ' + action_climb_str(t) + \
        ' | ' + action_turn_left_str(t) + ' | ' + action_turn_right_str(t) + ' | ' + action_wait_str(t) + ')' + ' & '

    # At most one action:
    actions = ['Forward', 'Grab', 'Shoot', 'Climb', 'TurnLeft', 'TurnRight', 'Wait']
    actionpairs = []
    for i in range(len(actions)):
        for j in range(i+1, len(actions)-1):
            actionpairs.append( (actions[i], actions[j]) )
    
    for actpair in actionpairs:
        act1 = actpair[0]
        act2 = actpair[1]

        axiom_str += '('
        axiom_str += falseSymb + getActStr(act1, t)
        axiom_str += ' | '
        axiom_str += falseSymb + getActStr(act2, t)
        axiom_str += ')'
        axiom_str += ' & '

    # Delete the last &        
    if axiom_str[-3 :] == ' & ':
        axiom_str = axiom_str[:-3]

    # print(axiom_str)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def generate_mutually_exclusive_axioms(t):
    #utils.print_not_implemented()
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []

    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return filter(lambda s: s != '', axioms)

#-------------------------------------------------------------------------------
