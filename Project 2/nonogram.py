from typing import List, Set, Tuple
import time
import sys

# Convert text file to row clues and column clues
def parse_nonogram_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    row_clues = []
    col_clues = []
    switch_to_col_clues = False

    for line in lines:
        line = line.strip()
        if line:
            if not switch_to_col_clues:
                row_clues.append([int(x) for x in line.split()])
            else:
                col_clues.append([int(x) for x in line.split()])
        else:
            switch_to_col_clues = True  # Switch after encountering an empty line

    return row_clues, col_clues

# The solver
def solve_nonogram(row_clues: List[List[int]], col_clues: List[List[int]]) -> List[List[bool]]:
    height = len(row_clues)
    width = len(col_clues)
    
    grid = [[None] * width for _ in range(height)]
    
    def get_all_possible_lines(length: int, clues: List[int]) -> Set[Tuple[bool, ...]]:
        def recursive_fill(current: List[bool], pos: int, clue_idx: int, blocks_left: List[int]) -> Set[Tuple[bool, ...]]:
            if clue_idx == len(blocks_left):

                result = current + [False] * (length - len(current))
                return {tuple(result)} if sum(result) == sum(clues) else set()
            
            results = set()
            block = blocks_left[clue_idx]
            
            max_pos = length - sum(blocks_left[clue_idx:]) - (len(blocks_left) - clue_idx - 1)
            for start in range(pos, max_pos + 1):

                if len(current) < start:
                    current.extend([False] * (start - len(current)))
                
                if start > 0 and len(current) >= start and current[start-1]:
                    continue
                
                new_current = current.copy()
                if len(new_current) < start:
                    new_current.extend([False] * (start - len(new_current)))
                
                block_area = new_current[len(new_current):start+block] if len(new_current) < start+block else new_current[start:start+block]
                if any(block_area) and len(block_area) == block:
                    continue
                
                new_current = new_current[:start]
                new_current.extend([True] * block)
                if start + block < length:
                    new_current.append(False)
                    results.update(recursive_fill(new_current, start + block + 1, clue_idx + 1, blocks_left))
                elif clue_idx == len(blocks_left) - 1:
                    results.add(tuple(new_current))
            
            return results
            
        if not clues:
            return {tuple(False for _ in range(length))}
        return recursive_fill([], 0, 0, clues)

    def update_line(line: List[bool], possibilities: Set[Tuple[bool, ...]]) -> bool:
        changed = False
        for i in range(len(line)):
            if line[i] is None:
                values = {p[i] for p in possibilities}
                if len(values) == 1:
                    line[i] = values.pop()
                    changed = True
        return changed

    def get_column(grid: List[List[bool]], col: int) -> List[bool]:
        return [row[col] for row in grid]

    def set_column(grid: List[List[bool]], col: int, values: List[bool]):
        for i, value in enumerate(values):
            grid[i][col] = value

    if any(sum(clue) + len(clue) - 1 > width for clue in row_clues):
        return None
    if any(sum(clue) + len(clue) - 1 > height for clue in col_clues):
        return None

    row_possibilities = {}
    col_possibilities = {}

    changed = True
    while changed:
        changed = False
        
        # Process rows
        for i, row in enumerate(grid):
            if None in row:
                if i not in row_possibilities:
                    row_possibilities[i] = get_all_possible_lines(width, row_clues[i])
                possibilities = {p for p in row_possibilities[i] 
                               if all(v is None or v == p[j] for j, v in enumerate(row))}
                if not possibilities:
                    return None
                row_possibilities[i] = possibilities
                if update_line(row, possibilities):
                    changed = True

        # Process columns
        for j in range(width):
            col = get_column(grid, j)
            if None in col:
                if j not in col_possibilities:
                    col_possibilities[j] = get_all_possible_lines(height, col_clues[j])
                possibilities = {p for p in col_possibilities[j]
                               if all(v is None or v == p[i] for i, v in enumerate(col))}
                if not possibilities:
                    return None  # No solution exists
                col_possibilities[j] = possibilities
                new_col = col.copy()
                if update_line(new_col, possibilities):
                    set_column(grid, j, new_col)
                    changed = True

    if any(None in row for row in grid):
        return None
    
    return grid

def print_nonogram(grid: List[List[bool]]):
    if grid is None:
        print("No solution exists!")
        return
    for row in grid:
        print(''.join('E' if cell else '.' for cell in row))


# Run the solver
def main():
    file_name = sys.argv[1]
    file_path = f"{file_name}"
    
    row_clues, col_clues = parse_nonogram_data(file_path)

    start_time = time.time()
    solution = solve_nonogram(row_clues, col_clues)
    end_time = time.time()

    elapsed_time = end_time - start_time

    if solution:
        print_nonogram(solution)
        print(f"Time taken: {elapsed_time:.4f} seconds")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()