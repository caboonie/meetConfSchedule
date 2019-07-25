import csv
import os

'''
Helper function to recursively build every possible permutation of a list of elements (classes)
'''
def permutations(classes):
    perms = []
    if len(classes)==0:
        return [[]]

    for activity in list(classes):
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

def scheduleHelper(students, classSchedule, times, tops = []):
    global num_calls
    assignments = {}
    #print("assign",students)
    


    if len(students)==0:
        return assignments
    student = list(students.keys())[0]

    #try each possible permutations of activities and times
    if(student in tops):
        print(student)
    num_calls+=1
    if(num_calls%100000==0):
    	print(num_calls)
    for perm in permutations(students[student]):
        #print(student,perm)
        #print("spots",classSchedule)
        validPerm = True
        index = 0
        for activity in perm:
            if classSchedule[(activity,times[index])] == 0:
                validPerm = False
                break #not enough slots
            if student not in assignments:
                assignments[student] = {}
            assignments[student][times[index]] = activity
        
            classSchedule[(activity,times[index])] -= 1 #take the available spot
            index+=1
        if not validPerm:
			for i in range(index):
				classSchedule[(perm[i],times[i])] -= 1
			continue

        classList = students.pop(student) #remove the assigned , save it for later
        
        childAssign = scheduleHelper(students, classSchedule, times, tops)
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
    with open(output_filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow("Name,Year,Block 1,Block 2,Block 3")
        for student in students: 
			print(student[0]+","+ student[1]+","+   students[student][times[0]]+","+ students[student][times[1]]+","+  students[student][times[2]])
			writer.writerow(student[0]+","+ student[1]+","+   students[student][times[0]]+","+ students[student][times[1]]+","+  students[student][times[2]])

if __name__=='__main__':

	global num_calls
	input_filename = "testFile.csv"
	times = [9,12,3]
	students = load_students(input_filename) #
	limit = 40
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

	classSchedule[('Bhangra',9)] = 0
	classSchedule[('Bhangra',3)] = 20
	classSchedule[('Product Management - Guest Lecture by Gil Hirsch',9)] = 0
	classSchedule[('Product Management - Guest Lecture by Gil Hirsch',12)] = 0
	classSchedule[('Product Management - Guest Lecture by Gil Hirsch',9)] = 0
	classSchedule[('Product Management - Guest Lecture by Gil Hirsch',3)] = 30
	classSchedule[('Fruit Shakes - Mustafa',9)] = 0
	classSchedule[('Fruit Shakes - Mustafa',3)] = 0
	classSchedule[('Local Girl Goes Global - Guest Lecture by Idit Harel',3)] = 0
	classSchedule[('Local Girl Goes Global - Guest Lecture by Idit Harel',12)] = 0
	classSchedule[('Creativity - a taste of thinking beyond',3)] = 0
	classSchedule[('Creativity - a taste of thinking beyond',12)] = 0 
	classSchedule[('Creativity - a taste of thinking beyond',9)] = 30
	classSchedule[('Korean 101 - Tasneem',9)] = 0
	#classSchedule[('Beginner Music - Vivian', 12)] = 0

	'''
	x=1
	classSchedule = {("a",1):x,("b",1):x,("c",1):2*x,("d",1):0,("a",2):2*x,("b",2):x,("c",2):0,("d",2):x}
	students = {str(i):["a","b"] for i in range(x)}
	students.update({str(i):["c","b"] for i in range(x,2*x)})
	students.update({str(i):["c","a"] for i in range(2*x,3*x)})
	students.update({str(i):["a","d"] for i in range(3*x,4*x)})
	times = [1,2]
	'''


	assignments = scheduleHelper(students,classSchedule,times)#,list(students.keys())[0:100])
	#print(assignments)

	print(num_calls)
	print("+++++++++++++++++++++")
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

	'''
	classes = {('"Introduction to Spanish language  and Mexican culture - Farah', 12): 12, ('"Introduction to Spanish language  and Mexican culture - Farah', 3): 5, ('Theater Improvisation - Dor and Anna', 12): 12, ('Sushi Workshop - Cat and Jennie', 9): 49, ('Mathematical Card Games - Mindren', 9): 12, ('Songwriting - Dou Dou', 9): 1, ('Fruit Shakes - Mustafa', 12): 22, ('Origami - Emily', 12): 4, ('Movie Production - Max', 12): 22, ('Bhangra', 12): 12, ('Basketball 101 - Yara', 3): 17, ('Origami - Emily', 3): 28, ('Yoga - Alicia', 3): 11, ('Recycling - Boaz', 3): 2, ('Sushi Workshop - Cat and Jennie', 12): 3, ('Movie Production - Max', 9): 28, ('Just Dance - Shoval and Malak', 3): 11, ('"Introduction to Spanish language  and Mexican culture - Farah', 9): 3, ('Tie Dye - Celina and Leen K', 9): 25, ('Japanese 101 - Lour', 3): 5, ('Songwriting - Dou Dou', 12): 6, ('Korean 101 - Tasneem', 3): 23, ('Basketball 101 - Yara', 12): 19, ('Tie Dye - Celina and Leen K', 12): 26, ('Korean 101 - Tasneem', 12): 7, ('Beginner Music - Vivian', 12): 2, ('Recycling - Boaz', 9): 6, ('Theater Improvisation - Dor and Anna', 3): 2, ('Product Management - Guest Lecture by Gil Hirsch', 3): 22, ('Basketball 101 - Yara', 9): 4, ('Yoga - Alicia', 9): 1, ('Songwriting - Dou Dou', 3): 18, ('Beginner Music - Vivian', 9): 1, ('Recycling - Boaz', 12): 9, ('Japanese 101 - Lour', 9): 1, ('Local Girl Goes Global - Guest Lecture by Idit Harel', 9): 5, ('Just Dance - Shoval and Malak', 9): 38, ('Bhangra', 3): 8, ('Which MEET coordinator are you? - Zuly and Vick', 12): 11, ('Theater Improvisation - Dor and Anna', 9): 12, ('Notebook Painting - Rawan', 3): 7, ('Tie Dye - Celina and Leen K', 3): 9, ('Just Dance - Shoval and Malak', 12): 12, ('Creativity - a taste of thinking beyond', 9): 29, ('Notebook Painting - Rawan', 12): 15, ('Beginner Music - Vivian', 3): 12, ('Yoga - Alicia', 12): 17, ('Notebook Painting - Rawan', 9): 19, ('Movie Production - Max', 3): 12, ('Ombre Nail Art - Sophie and Abby', 3): 13, ('Japanese 101 - Lour', 12): 12, ('Mathematical Card Games - Mindren', 12): 8, ('Which MEET coordinator are you? - Zuly and Vick', 3): 29, ('Ombre Nail Art - Sophie and Abby', 12): 3}

	input_filename = "testFile.csv"
	students = set()
	filepath = os.path.abspath(input_filename)
	with open(filepath, 'rt') as form_responses_csv:
	    reader = csv.DictReader(form_responses_csv)
	    for row in reader:
	    	print(row['Name'].lower())
	        students.add(row['Name'].lower())
	#print("cohen' in students)
	print(students)
	students_not = set()
	input_filename = "2019 all students.csv"
	filepath = os.path.abspath(input_filename)
	with open(filepath, 'rt') as form_responses_csv:
	    reader = csv.DictReader(form_responses_csv)
	    for row in reader:
	    	student = (row['first']+" "+row['last']).lower()
	    	if(student not in students):
	    		students_not.add(student)
	print(students_not)


	set(['nir menahem', 'noor ali', 'tal davidson', 'rayan amin',  'sarah alayan', 'george alawi', 'tamar shafrir', 'danyil vaida', 'katrina farah', 'michal tevet', 'layan mabjish', 'natalie moshaiev', 'ariel navarro-sucary', 'rahaf zorba', 'maya gordon', 'bshara marjieh', 'tareq abu salih', 'carmel gross', 'shikma lerner-friedman', 'basel manasrah', 'aya  tabony', 'danielle weiss', 'kareem hijazi', 'mansour abu khadra', 'juna azzam', 'yonatan fingerut', 'diam habib allah', 'marah ali', 'ofir ochayon', 'noam mertsen', 'shir shitrit', 'satti passi', 'william  elias', 'sameeha abbas', 'sumayah takruri', 'maya jaber', 'ward elias', 'fanar khateeb', 'judeh araj', 'mohammad hamdan', 'seraj abu salah', 'shira maybruch', 'naama shalev', 'rawand mukarker', 'natal habil', 'bassel khamaisi', 'tamara hashimeh', 'razi salameh', 'stahv shayo', 'sadeen siaj', 'siwar khateb', 'niv hod tamir', 'jana sayed ahmad', 'shaked ben ami', 'nour  mahmoud ', 'nevi gavrieli', 'eman  khamaisy', 'shiraz marigosian', 'simon  deeb', 'gilad yosef', 'idan zamir', 'ido forshtat', 'carmi assaf-shapira', 'mor yehuda', 'anas abbassi', 'eyal livny', 'osama hijazi', 'shir raviv', 'ward zoabi', 'yiftach banki', 'jawzal  sheikh khalil', 'rommie  egert', 'yousef  michael', 'salwa  khaldi', 'yossef tzeel krupp', 'yoav goldberg', 'wajeeh aweisat', 'mohamed yaghmour', 'yaala oren', 'shay lee isan', 'mohee eldin  bitar', 'lour jean', 'omer ichar', 'yonatan fatal', 'eviatar guter-elazar', 'rami mansour', 'juna hamed', 'ron harel', 'salam abu ahmad', 'barak kuchinsky', 'hamodi hriesh', 'inbar koursh', 'or  ayubi', 'tamer  matar', 'dona khalaily', 'omer sharon gabay', 'hala abdin', 'matvey khoussainov', 'noya shinnar', 'itamar gan sinclair', 'maya daniel', 'wasim risheq', 'maayan zeira', 'adan  abu naaj', 'avishag haetzni', 'nara fleifel', 'tala jahshan', 'wasem saalameh', 'roy berger', 'alice qassabian', 'waseem  lawen', 'noam globerman', 'noam regev', 'vivian  salem', 'wael hashem', 'omer meidan', 'taqwa  zoabi', 'shahar arie', 'leen  khamis', 'uri etzion', 'adriana faddoul', 'mousa bakri', 'tamara kreitler', 'sol diab', 'mai rodrigez'])
	'''
	set(['nir menahem', 'noor ali', 'tal davidson', 'rayan amin',  
		'tamar shafrir',  'michal tevet', 'natalie moshaiev', 
		'maya gordon', 'bshara marjieh', 'tareq abu salih',
		'basel manasrah',  'kareem hijazi', 'mansour abu khadra',
		 'shir shitrit', 'satti passi', 'sameeha abbas', 
		 'maya jaber', 'ward elias', 'fanar khateeb', 
		 'mohammad hamdan', 'shira maybruch', 'bassel khamaisi',
		   'jana sayed ahmad','nour  mahmoud ','gilad yosef',
		       'anas abbassi', 
		       'shir raviv', 
		        'rommie  egert', 'yousef  michael',
		         'yossef tzeel krupp', 'yoav goldberg', 'wajeeh aweisat',
		          'mohamed yaghmour', 
		             'juna hamed', 'salam abu ahmad',
		              'barak kuchinsky', 'hamodi hriesh', 
		                'matvey khoussainov',
		                 'wasim risheq', 'maayan zeira',
		                 'avishag haetzni',
		                 'roy berger', 
		                  'noam globerman',
		                 'vivian  salem', 'wael hashem', 'omer meidan', 'taqwa  zoabi',
		                  'shahar arie',
		                    'tamara kreitler', 'sol diab', 'mai rodrigez'])
