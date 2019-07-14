import csv
import os

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

def makeClassSchedule(classes,times):
    classSchedule = {}
    for activity in classes:
        for time in times:
            classSchedule[(activity,time)] = classes[activity]
    return classSchedule

def scheduleHelper(students, classSchedule, times):
    assignments = {}
    if len(students)==0:
        return assignments
    student = list(students.keys())[0]
    #try each possible permutations of activities and times
    #print(classSchedule)
    for perm in permutations(students[student]):
        #print(perm)
        validPerm = True
        for index, activity in enumerate(perm):
            if classSchedule[(activity,times[index])] == 0:
                validPerm = False
                break #not enough slots
            if student not in assignments:
                assignments[student] = {}
            assignments[student][activity] = times[index]
        
            classSchedule[(activity,times[index])] -= 1
            #print("post change",(activity,times[index]))
            #print(classSchedule)
        if not validPerm:
            continue
        classList = students.pop(student)
        childAssign = scheduleHelper(students, classSchedule, times)
        if childAssign != None:
            return dict(childAssign, **assignments)
        students[student] = classList
    return None
            
    #for activity in students[student]:
    #        assignments[student][activity] = time


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

students = {"a":["art","dance","fencing"],"b":["art","dance","fencing"],"c":["art","dance","fencing"],"d":["art","dance","fencing"]}
classes = {"art":1,"dance":1,"fencing":1}
times = [9,12,3]


expected = {"a":{"art":9,"dance":12,"fencing":3}}

#print(permutations(["art","dance","fencing"]))
#print(scheduleHelper(students,makeClassSchedule(classes,times),times))

if __name__=='__main__':
    input_filename = "student_preferences.csv"
    students = load_students(input_filename)
    print(scheduleHelper(students,makeClassSchedule(classes,times),times))