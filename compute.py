import math
import random
import time
import threading
import sys
from datetime import datetime, timedelta

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
    total = 0.0
    for i in range(len(tour) - 1):
        current = locations[tour[i]]
        next_point = locations[tour[(i + 1)]]
        total += computeEuclideanDistance(current, next_point)
    return total

def nearest_neighbor(locations, start = 0):
    n = len(locations)
    unvisited = list(range(n))
    unvisited.remove(start)
    tour = [start]
    current = start

    while unvisited:
        distances = [(computeEuclideanDistance(locations[current], locations[i]), i) for i in unvisited]
        distances.sort()
        closest = distances[0][1]
        tour.append(closest)
        unvisited.remove(closest)
        current = closest

    tour.append(start)
    return tour

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
    print("ComputePossibleSolutions")
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

    if n > 4096:
        sys.exit("Aborting. File exists exists but contains more than 4096 coordinates.")

    now = datetime.now()
    ready_time = (now + timedelta(minutes=5)).strftime("%-I:%M%p").lower()
    
    print(f"There are {n} nodes: Solutions will be available by {ready_time}")
    print()

    total_x = 0
    total_y = 0
    for point in locations:
        total_x += point[0]
        total_y += point[1]
    
    avg_x = total_x / n
    avg_y = total_y / n

    landing_pad = (avg_x, avg_y)

    start = 0
    min_distance = float('inf')

    for i in range(n):
        dist = computeEuclideanDistance(locations[i], landing_pad)
        if dist < min_distance:
            min_distance = dist
            start = i

    tour = nearest_neighbor(locations, start)
    total_dist = total_tour_distance(locations, tour)

    print(f"If you use 1 drone(s), the total route will be {total_dist:.1f} meters")
    print(f"Landing Pad 1 should be at [{int(round(landing_pad[0]))},{int(round(landing_pad[1]))}], "f"serving {n} locations, route is {total_dist:.1f} meters")
    
if __name__ == "__main__":
    main()