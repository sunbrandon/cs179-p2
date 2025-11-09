import math
import random
import time
import threading
import sys

def read_locations(filename):
    locations = []

    try:

        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) != 2:
                        sys.exit(f"Aborting. File expected 2 coordinates, got {len(parts)}")
                    else:
                        x = float(parts[0])
                        y = float(parts[1])
                        locations.append((x, y))
        
        return locations
    
    except Exception as error: 
        sys.exit("Aborting. File does not exist")

def computeEuclideanDistance(coord1, coord2):
    return math.sqrt(((coord2[0]-coord1[0])**2) + ((coord2[1]-coord1[1])**2))

def total_tour_distance(locations, tour):
    total = 0
    for i in range(len(tour)):
        current = locations[tour[i]]
        next_point = locations[tour[(i + 1) % len(tour)]]
        total += computeEuclideanDistance(current, next_point)
    return total

def nearest_neighbor(locations, start, bestSoFar=float('inf')):
    n = len(locations)
    unvisited = list(range(n))
    unvisited.remove(start)
    tour = [start]
    current = start
    curr_dist = 0

    while len(unvisited) > 0:
        if len(unvisited) == 1:
            closest = unvisited[0]
            dist_to_closest = computeEuclideanDistance(locations[current], locations[closest])
        else:
            distances = []
            for point in unvisited:
                dist = computeEuclideanDistance(locations[current], locations[point])
                distances.append((dist, point))
            distances.sort()
            
            if random.random() < 0.1:
                closest = distances[1][1]
                dist_to_closest = distances[1][0]
            else:
                closest = distances[0][1]
                dist_to_closest = distances[0][0]
        
        curr_dist += dist_to_closest
        
        if curr_dist >= bestSoFar:
            return None, float('inf')
        
        tour.append(closest)
        unvisited.remove(closest)
        current = closest

    return_dist = computeEuclideanDistance(locations[current], locations[start])
    curr_dist += return_dist
    
    if curr_dist >= bestSoFar:
        return None, float('inf')
    
    return tour, curr_dist

def write_solution(locations, tour, distance, prefix):
    output_filename = f"{prefix}_FormosaSolutions_solution_{int(round(distance))}.txt"
    
    with open(output_filename, 'w') as file:
        for index in tour:
            x, y = locations[index]
            file.write(f"{x} {y}")
            file.write("\n")
        
        start_x, start_y = locations[0]
        file.write(f"{start_x} {start_y}")
    
    print(f"Route written to disk as {output_filename}")
    return output_filename

def main():
    print("ComputeDronePath")
    print()
    
    filename = input("Enter the name of file: ")
    print()

    if not filename:
        print("No filename entered.")
        return
    
    if not filename.lower().endswith('.txt'):
        sys.exit("Aborting. File is not in .txt format")
    
    locations = read_locations(filename)
    
    if locations is None:
        return
    
    n = len(locations)

    if n == 0:
        sys.exit("Aborting. File exists but is empty.")

    if n > 256:
        sys.exit("Aborting. File exists exists but contains more than 265 coordinates.")
    
    print(f"There are {n} nodes, computing route...")
    print("Shortest Route Discovered So Far")

    
if __name__ == "__main__":
    main()