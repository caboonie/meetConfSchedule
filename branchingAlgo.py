import csv
import os

'''
Helper function to recursively build every possible permutation of a list of elements (classes)
'''
def permutations(classes):
    perms = []
    if len(classes)==0:
        return [[]]

    for activity in classes.copy():
        classes.remove(activity)
        for perm in permutations(classes):
            perms.append([activity]+perm)
        classes.append(activity)
    return perms

'''
For a dictionary of classes {"name":size_limit}, creates a schedule dictionary of format {("name","time"):spots_remaining}
'''
def makeClassSchedule(classes,times):
    classSchedule = {}
    for activity in classes:
        for time in times:
            classSchedule[(activity,time)] = classes[activity]
    return classSchedule

'''
Function to try assigning a student to a permutation of their class schedule, and then recursively attempt solving the rest of the schedule
'''
def scheduleHelper(students, classSchedule, times):
    assignments = {}
    #print("assign",students)
    if len(students)==0:
        return assignments
    student = list(students.keys())[0]
    #try each possible permutations of activities and times
    for perm in permutations(students[student]):
        #print(perm)
        validPerm = True
        for index, activity in enumerate(perm):
            if classSchedule[(activity,times[index])] == 0:
                validPerm = False
                break #not enough slots
            if student not in assignments:
                assignments[student] = {}
            assignments[student][times[index]] = activity
        
            classSchedule[(activity,times[index])] -= 1 #take the available spot
        if not validPerm:
            continue

        classList = students.pop(student) #remove the assigned class
        childAssign = scheduleHelper(students, classSchedule, times)
        #print("child:",childAssign)
        #if the recursive call succeeded, then we have a solution to return
        if childAssign != None:
            assignments.update(childAssign) #merge and return the dictionary
            return assignments

        #otherwise the perm failed, so reset the students preferences and class spots
        students[student] = classList
        for index, activity in enumerate(perm):
            classSchedule[(activity,times[index])] += 1
    return None
            


def load_students(input_filename):
    students = {}
    filepath = os.path.abspath(input_filename)
    with open(filepath, 'rt') as form_responses_csv:
        reader = csv.DictReader(form_responses_csv)
        for row in reader:
            students[(row['Name'],row['Year'])]=[
                        row['First Choice'],
                        row['Second Choice'],
                        row['Third Choice'] ]
    return students


### writing the output csv
def save_assignments(students, output_filename,times):
    with open(output_filename, 'wt') as output_file:
        fieldnames = ["Name","Year","Block 1", "Block 2", "Block 3"]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students: 
            writer.writerow({
                "Name": student[0], 
                "Year": student[1], 
                "Block 1": students[student][times[0]],
                "Block 2": students[student][times[1]],
                "Block 3": students[student][times[2]]
            })

if __name__=='__main__':
    input_filename = "student_prefs.csv"
    times = [9,12,3]
    students = load_students(input_filename) #
    limit = 1
    classes = {}
    for student in students:
        for activity in students[student]:
            classes[activity] = limit
    print(classes)
    assignments = scheduleHelper(students,makeClassSchedule(classes,times),times)
    print(assignments)
    if assignments != None:
        save_assignments(assignments,"meetConfAssignments.csv",times)
    else:
        print("impossible")