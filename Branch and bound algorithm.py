import pandas as pd
import numpy as np

class Node:
    def __init__(self, level, profit, weight, bound, items):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.bound = bound
        self.items = items

def bound(node, capacity, revenues, days):
    if node.weight >= capacity:
        return 0
    profit_bound = node.profit
    j = node.level + 1
    total_weight = node.weight
    
    while j < len(revenues) and total_weight + days[j] <= capacity:
        total_weight += days[j]
        profit_bound += revenues[j]
        j += 1
    
    if j < len(revenues):
        profit_bound += (capacity - total_weight) * (revenues[j] / days[j])
    
    return profit_bound

def branch_and_bound(capacity, revenues, days):
    n = len(revenues)
    nodes = []
    root = Node(level=-1, profit=0, weight=0, bound=0, items=[0] * n)
    root.bound = bound(root, capacity, revenues, days)
    nodes.append(root)
    max_profit = 0
    best_items = []
    
    while nodes:
        current = nodes.pop(0)
        
        if current.level == -1:
            level = 0
        else:
            level = current.level + 1
        
        if level < n:
            left = Node(level=level,
                        profit=current.profit + revenues[level],
                        weight=current.weight + days[level],
                        bound=0,
                        items=current.items[:])
            left.items[level] = 1
            
            if left.weight <= capacity and left.profit > max_profit:
                max_profit = left.profit
                best_items = left.items[:]
            
            left.bound = bound(left, capacity, revenues, days)
            if left.bound > max_profit:
                nodes.append(left)
            
            right = Node(level=level,
                         profit=current.profit,
                         weight=current.weight,
                         bound=0,
                         items=current.items[:])
            right.bound = bound(right, capacity, revenues, days)
            if right.bound > max_profit:
                nodes.append(right)
    
    return max_profit, best_items

def solve_knapsack_from_csv(file_path, capacity_column, profit_column, capacity):

    df = pd.read_csv(file_path)
    
    if capacity_column not in df.columns or profit_column not in df.columns:
        raise ValueError(f"The columns '{capacity_column}' and '{profit_column}' must be present in the CSV file.")
    
    revenues = df[profit_column].tolist()
    days = df[capacity_column].tolist()
    
    max_profit, selected_projects = branch_and_bound(capacity, revenues, days)
    
    selected_project_ids = [df.index[i] + 1 for i, x in enumerate(selected_projects) if x == 1]
    return max_profit, selected_project_ids

if __name__ == "__main__":

    file_path = "C:/Users/DELL/Documents/Optimization/Example.txt"  # Replace with file path
    
    capacity_column = "Days"  
    profit_column = "Revenue"  
    
    total_days = int(input("Enter the total number of available researcher days: ")) 
    
    try:
        max_profit, selected_projects = solve_knapsack_from_csv(file_path, capacity_column, profit_column, total_days)
        print(f"Maximum Profit: {max_profit}")
        print(f"Selected Projects: {', '.join(map(str, selected_projects))}")
    except Exception as e:
        print(f"Error: {e}")
