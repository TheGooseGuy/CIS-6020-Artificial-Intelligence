goal-based agents:
1. state
2. goal
3. actions

decide the characteristics of the problem (fully obeservable? determininstic?...)

represent the state:
string (for 8-puzzle exammple)

goal:
def isGoal(state):


actions:
given current state, specify whether actions can be applied, and what state we achieve after the action
represent actions: discrete events that occur at an instant of time

good representation simplify the problem

search in a state space:
to keep track of the connections between states: tree data structure/graph data structure

state space (V,E) V: nodes, E: arcs
each arc has fixed, positive cost.
a goal test is applied to a state to determine if it achieve the goal



state-space search

