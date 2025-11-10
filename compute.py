import math
import random
import time
import threading
import sys
from datetime import datetime, timedelta
import numpy as np
import copy

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

def to_roman(n):
    roman_numerals = ["i", "ii", "iii", 'iv']
    return roman_numerals[n-1]

def kmeans(locations,k):

   locations = np.array(locations)
   #Random Centroids
   clusters = {}
   np.random.seed(37)
   
   #picking INITIAL centroids based on random existing points
   random_indices = np.random.choice(locations.shape[0], k, replace=False)
   centroids = locations[random_indices]

   for i in range(k):
       centroid = centroids[i]
       coordinates = []
       cluster = {
           'centroid' : centroid,
           'coordinates' : []
       }
  
       clusters[i] = cluster

   change = True

   while change:


       for i in range(locations.shape[0]):
               dist = []
              
               curr = locations[i]
              
               for j in range(k):
                   dis = computeEuclideanDistance(curr,clusters[j]['centroid'])
                   dist.append(dis)
               curr_cluster = np.argmin(dist)
               clusters[curr_cluster]['coordinates'].append(curr)


       curr_locations = copy.deepcopy(clusters)
 
       for i in range(k):
               coordinates = np.array(clusters[i]['coordinates'])
               if coordinates.shape[0] > 0:
                   new_center = coordinates.mean(axis =0)
                   clusters[i]['centroid'] = new_center
                  
                   clusters[i]['coordinates'] = []
      
       for i in range(locations.shape[0]):
               dist = []
              
               curr = locations[i]
              
               for j in range(k):
                   dis = computeEuclideanDistance(curr,clusters[j]['centroid'])
                   dist.append(dis)
               curr_cluster = np.argmin(dist)
               clusters[curr_cluster]['coordinates'].append(curr)

       count = 0
       for i in range(k):
            if not np.array_equal(clusters[i]['centroid'], curr_locations[i]['centroid']):
                count += 1


       if count == 0:
           change = False

   return clusters

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

    for k in range(1,5): # 4 experiments of k=1 through k=4.
        clusters = kmeans(locations,k)
        total_dist = 0
        output_list = []
        
        for j in range(k): # each cluster per experiment
            cluster_locations = clusters[j]['coordinates']
            centroid = clusters[j]['centroid']

            if len(cluster_locations) == 0:
                print(f"    {to_roman(j+1)}. Landing Pad {j+1} should be at [{int(round(centroid[0]))},{int(round(centroid[1]))}], "f"serving 0 locations, route is 0.0meters")
                continue
            
            tour = nearest_neighbor(cluster_locations, 0) #start at location 0 in cluster locations, starting node shouldn't matter
            cluster_dist = total_tour_distance(cluster_locations,tour)

            total_dist += cluster_dist

            output = f"    {to_roman(j+1)}. Landing Pad {j+1} should be at [{int(round(centroid[0]))},{int(round(centroid[1]))}], "f"serving {len(cluster_locations)} locations, route is {cluster_dist:.1f} meters"
            output_list.append(output)

        print(f"{k}) If you use {k} drone(s), the total route will be {total_dist:.1f} meters")
        for output in output_list:
            print(output)
        print()
    
if __name__ == "__main__":
    main()