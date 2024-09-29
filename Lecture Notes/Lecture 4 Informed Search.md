# Heuristic Search
Def: trial-and-error methods; A rule of thumb; approximation algorithm; commonsense rule

domain-specific information:  
- Select most promising path along which to continue seaching  
- `h(n)`: estimates *goodness* of node `n`  
- `h(n)` = **estimated cost** (of distance) of minimal cost path from n **to a goal state**.  
- Estimates how close a state `n` is to a goal using domain-specific information
## Heuristics
- **All domain knowledge** used in search is encoded in the **heuristic function, `h(<node>)`**  
EX: 8-puzzle  - number of tiles out of place  
Better solution: Sum of distances for each tile to its goal position
- `h(n)>=0` for all nodes `n`  
- `h(n)=0` for goal node  
- `h(n)=`$\infty$ for a dead-end (that can't lead to goal)