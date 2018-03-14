import math
import random
import matplotlib.pyplot as plt

convex_hull = [] # List of lines that make up convex hull

# Return the value of n
# n minimum value is 2
def read_n() :
    n = int(input())
    while(n < 2) :
        n = int(input())
    return n

# Return list of point
# Point has 2 value, (x,y)
# Value of each point is randomized
def create_points(n, points) :
    i = 0
    while(i < n) :
        x = random.randint(-100,100)
        y = random.randint(-100,100)
        point = (x,y)
        points.append(point)
        i = i + 1
    points.sort()
    return points

# Return determinant of a 3x3 matrix
def determinant(p1, p2, p3) :
    return p1[0]*p2[1] + p3[0]*p1[1] + p2[0]*p3[1] - p3[0]*p2[1] - p2[0]*p1[1] - p1[0]*p3[1]

# Return the furthest point from a given line
def furthest_point(points, p1, pn) :
    # Convert two given points to equation form
    a = pn[1] - p1[1]
    b = p1[0] - pn[0]
    c = ((pn[0] - p1[0]) * p1[1]) - ((pn[1] - p1[1]) * p1[0])
    point = points[0]
    max_distance = abs(a*point[0] + b*point[1] + c) / math.sqrt(pow(a,2) + pow(b,2)) # Assume first element of points is the furthest point
    i = 1
    n = len(points)
    while(i < n) :
        check_point = points[i]
        distance = abs(a*check_point[0] + b*check_point[1] + c) / math.sqrt(pow(a,2) + pow(b,2)) # Checks the distance of other points
        if(distance > max_distance) : # Assumed max distance is less than distance of other points in list
            max_distance = distance
            point = check_point
        i = i + 1
    return point

# Seperates list of point to two different side
# Left and right side is dependent on line's direction
# Line(p1,pn)'s left side is equal to line(pn,p1)'s right side
# To calculate line(p1,pn)'s right side, we use line(pn,p1)'s left side
def seperate_points(points, p1, pn) :
    left = []
    for p3 in points :
        det = determinant(p1,pn,p3)
        if(det > 0) : # Points on the left side of line(p1,pn) have positive determinant value
            left.append(p3)
        # Points that's crossed by line(p1,pn) is ignored, because it wont create convex hull
    return left

# Create conves hull from a given set of points
def create_convex_hull(points, p1, pn) :
    n = len(points)
    if(n == 0) : # Base
        convex = (p1,pn)
        convex_hull.append(convex) # Add line(p1,pn) to list of lines that make up convex hull
    else :
        pmax = furthest_point(points, p1, pn) # Pmax = furthest point from line(p1,pn)
        left = seperate_points(points, p1, pmax) # Determine the left side of line(p1,pmax)
        print("Available outer points<",p1,",",pmax,"> : ", left)
        create_convex_hull(left, p1, pmax) # Recursion until left side of line(p1,pmax) is empty
        left = seperate_points(points, pmax, pn) # Determine the left side of line(pmax,pn)
        print("Available outer points<",pmax,",",pn,"> : ", left)
        create_convex_hull(left, pmax, pn) # Recursion until left side of line(pmax,p1) is empty
    return

# Draw convex hull with matplotlib
def draw_convex_hull(points) :
    x = []
    y = []
    for point in points :
        x.append(point[0])
        y.append(point[1])
    plt.scatter(x,y) # Draw all points in set S
    a = []
    b = []
    for line in convex_hull :
        point1 = line[0]
        point2 = line[1]
        a.append(point1[0])
        a.append(point2[0])
        b.append(point1[1])
        b.append(point2[1])
    plt.plot(a,b) # Draw convex hull
    plt.show()
    return

# Main program
def main() :
    n = read_n() # Read n with minimal value of 2
    points = []; left = []; right = [];
    points = create_points(n,points) # Create randomized points from with absis and coordinate value of -100 to 100
    # Extreme points from a sorted list is always the first element and the last element
    p1 = points[0]
    pn = points[n-1]
    print("Extreme points : ", p1, " and ", pn)
    # Left indicates the left side of line(p1,pn)
    # Right indicates the right side of line(p1,pn)
    # Right side of line(p1,pn) will be calculated with line(pn,p1)'s left side
    left = seperate_points(points, p1, pn)
    create_convex_hull(left, p1, pn)
    right = seperate_points(points, pn, p1)
    create_convex_hull(right, pn, p1)
    # Draw convex hull with matplotlib
    i = 0
    n = len(convex_hull)
    while(i < n) :
        print(convex_hull[i])
        i = i + 1
    draw_convex_hull(points)
    return

main()
