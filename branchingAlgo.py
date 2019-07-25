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
    global num_calls
    assignments = {}
    #print("assign",students)
    if len(students)==0:
        return assignments
    student = list(students.keys())[0]
    #try each possible permutations of activities and times

    num_calls+=1
    for perm in permutations(students[student]):
        #print(perm)
        if student == ('Tal Herman', 'Y2'):
            print(perm)
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
            students[(row['Name'],row['Year'])]=  ["Bhangra" if "Bhangra" in i else i.strip() for i in row['Please tick 3 boxes!'].split(",")]
    return students


### writing the output csv
def save_assignments(students, output_filename,times):
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow("Name,Year,Block 1,Block 2,Block 3")
        for student in students: 
            writer.writerow(student[0]+","+ student[1]+","+   students[student][times[0]]+","+ students[student][times[1]]+","+  students[student][times[2]])

if __name__=='__main__':
    global num_calls
    input_filename = "meetConf2019.csv"
    times = [9,12,3]
    students = load_students(input_filename) #
    limit = 25
    classes = {}
    total_count = {}
    for student in students:
        for activity in students[student]:
            classes[activity] = limit
            if activity in total_count:
                total_count[activity] += 1
            else:
                total_count[activity] = 1
    print(total_count)
    
    #print(classes)
    num_calls = 0
    classSchedule = makeClassSchedule(classes,times)
    
    classSchedule[('Bhangra',9)] = 2
    classSchedule[('Bhangra',3)] = 2
    classSchedule[('Product Management - Guest Lecture by Gil Hirsch',9)] = 0
    classSchedule[('Product Management - Guest Lecture by Gil Hirsch',12)] = 0
    classSchedule[('Product Management - Guest Lecture by Gil Hirsch',9)] = 0
    classSchedule[('Product Management - Guest Lecture by Gil Hirsch',3)] = 30
    classSchedule[('Local Girl Goes Global - Guest Lecture by Idit Harel',3)] = 0
    classSchedule[('Creativity - a taste of thinking beyond',3)] = 0
    classSchedule[('Creativity - a taste of thinking beyond',12)] = 0 
    classSchedule[('Creativity - a taste of thinking beyond',9)] = 30
    assignments = scheduleHelper(students,classSchedule,times)
    print(num_calls)
    print("+++++++++++++++++++=")
    #rint(classSchedule)
    #print([i[0]+","+str(i[1])+": "+str(classSchedule[i]) for i in classSchedule])
    schedule = {}
    

    if assignments != None:
        save_assignments(assignments,"meetConfAssignmentsTest.csv",times)
        for assignment in assignments:
            for activity in assignments[assignment]:
                if (assignments[assignment][activity],activity) in schedule:
                    schedule[(assignments[assignment][activity],activity)] += 1
                else:
                    schedule[(assignments[assignment][activity],activity)] = 1
        print(schedule)

    else:
        print("impossible")