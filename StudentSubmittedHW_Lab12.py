########################################
# Faisal Sikder
# University of Miami
# Dept of Computer Science
########################################


import os
import subprocess
import shutil
from TextToPdf import write_simple_pdf
import time

students = [line.strip().split(',') for line in open('Fall2016csc220\\usernames_names.txt')]

#usernames = [line[0] for line in lines]
#print usernames

distadd = "BoxSync\\Box Sync\\"
assignment = "Lab12"
assignmentfiles_A = ["Node.java","PathFinder.java"]
assignmentfiles =["Node.java","PathFinder.java"]
compile_files =  ["Node.java","PathFinder.java"]
compile_files_A = ["Node.java","PathFinder.java"]
disk_main_add = "Fall2016csc220\\"
main_file = "TLab12.java"
main_class = "TLab12"
main_file_A = "TLab12.java"
main_class_A = "TLab12"
actual_point = [15,5,10,5,65,-20];

def check_correct_assignment_submission(distadd,assignment,filelist):
    for assign in assignmentfiles_A:
        #print distadd+"\\"+assignment+"\\src\\"+assignment+"\\"+assign
        if os.path.isfile(distadd+"\\"+assignment+"\\src\\"+assignment+"\\"+assign) is False:
            #print distadd+"\\"+assignment+"\\src\\"+assignment+"\\"+assign       
            return False
    return True


def check_shared_folder(distadd,assignment,assignmentfiles):
    folders =  os.listdir(distadd)
    students.sort()
    missing_student=[]
    incorrect_student = []
    for student in students:
        if "csc220-"+student[0] not in folders:
            missing_student.append(student)
        elif check_correct_assignment_submission(distadd+"csc220-"+student[0],assignment,assignmentfiles) is False:
            incorrect_student.append(student)
 
    file = open(disk_main_add+"Missing-Wrongly-Named-students.txt","w")
    file.write("Username, First Name, Last Name\n");
    file.write("\nFolder Missing\n\n");
    for ms in missing_student:
        file.write(ms[0]+", " +ms[1]+", "+ms[2]+"\n");
    file.write("\nIncorrect Submission\n\n");
    for ms in incorrect_student:
        file.write(ms[0]+", " +ms[1]+", "+ms[2]+"\n");
    file.close()



def copy_assignment_with_name(dist_box, dist_disk):
    folders =  os.listdir(dist_box)
    students.sort()
    copied_student = []
    if not os.path.exists(dist_disk):
        os.makedirs(dist_disk)
        print assignment+" -- Folder created"
    for student in students:
        lab_submit =dist_box+"csc220-"+student[0]+"\\"+assignment
        if os.path.exists(lab_submit):
            shutil.copytree(lab_submit,dist_disk+"\\csc220-"+student[0]+"\\"+assignment);
            copied_student.append(student)
            print "Good -- Copied -- "+student[1]+" "+student[2]+" "+student[0]
        else:
            if not os.path.exists(dist_disk+"\\csc220-"+student[0]):
                os.makedirs(dist_disk+"\\csc220-"+student[0])
            for nfile in assignmentfiles:
                org_loc = find_file(nfile,dist_box+"csc220-"+student[0])
                if org_loc is not None:
                    shutil.copyfile(org_loc, dist_disk+"\\csc220-"+student[0]+"\\"+nfile);
            print "Bad Submission -- Copied -- "+student[1]+" "+student[2]+" "+student[0] + "--------->"
                           
    file = open(dist_disk+"\\wednesday10am.txt","w")
    for ms in copied_student:
        file.write(ms[0].strip()+"\n");
    file.close()    

def copy_assignment_with_name_late(dist_box, dist_disk):
    folders =  os.listdir(dist_box)
    students.sort()
    copied_student = []
    submited_students = [line.strip() for line in open(dist_disk+"\\wednesday10am.txt")]
    #print    submited_students
    for student in students:
        if student[0].strip() not in submited_students:
            lab_submit =dist_box+"csc220-"+student[0]+"\\"+assignment
            if os.path.exists(lab_submit):
                shutil.copytree(lab_submit,dist_disk+"\\csc220-"+student[0]+"\\"+assignment);
                copied_student.append(student)
            else:
                if not os.path.exists(dist_disk+"\\csc220-"+student[0]):
                    os.makedirs(dist_disk+"\\csc220-"+student[0])
                for nfile in assignmentfiles:
                    org_loc = find_file(nfile,dist_box+"csc220-"+student[0])
                    if org_loc is not None:
                        shutil.copyfile(org_loc, dist_disk+"\\csc220-"+student[0]+"\\"+nfile);               
    file = open(dist_disk+"\\thursday10am.txt","w")
    for ms in copied_student:
        file.write(ms[0].strip()+"\n");
    file.close()

def assignment_checking_comments(filename,comments,create=0):
    if  create == 0:
        file = open(filename,"a+");
    else:
        file = open(filename,"w");
    file.write(comments);
    file.write("\n");
    file.close();

def assignment_checking_rubic(filename,points,status,is_late=False):
    #print str(len(actual_point)) + " " +str(len(points))
    file = open(filename,"a+");
    file.write("Grading Rubric Bellow: \n\n");
    i=0
    for st in status:
        file.write(st+"( "+str(actual_point[i])+"% ) --> "+str(points[i])+"%\n");
        i+=1
    if is_late:
        file.write("Late Penalty ( 50% off ): --> - "+str(sum(points)*.5)+"%\n");
        file.write("Total Points: --> "+str(sum(points)*0.5)+"%\n");
    else:
        file.write("Total Points: --> "+str(sum(points))+"%\n");
    file.write("\n");
    file.close();

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def create_copy_the_file_in_correct_order(stu_lab_loc):
    if not os.path.exists(stu_lab_loc+"\\TA"):
        os.makedirs(stu_lab_loc+"\\TA")
    if not os.path.exists(stu_lab_loc+"\\TA\\"+assignment):
        os.makedirs(stu_lab_loc+"\\TA\\"+assignment)
    if not os.path.exists(stu_lab_loc+"\\TA\\"+assignment+"\\src"):
        os.makedirs(stu_lab_loc+"\\TA\\"+assignment+"\\src")
    if not os.path.exists(stu_lab_loc+"\\TA\\"+assignment+"\\src\\"+assignment.lower()):
        os.makedirs(stu_lab_loc+"\\TA\\"+assignment+"\\src\\"+assignment.lower())

    final_loc = stu_lab_loc+"\\TA\\"+assignment+"\\src\\"+assignment.lower();
    for nfile in assignmentfiles:
        org_loc = find_file(nfile,stu_lab_loc)
        if org_loc is not None:
            shutil.copyfile(org_loc, final_loc+"\\"+nfile);
    return True    

def copy_a_backup_copy(disk_destination):
    if os.path.exists(disk_destination+"_Copy") is False:
            shutil.copytree(disk_destination,disk_destination+"_Copy");

def copy_a_backup_copy_original(disk_destination):
    if os.path.exists(disk_destination+"_Copy_Original") is False:
            shutil.copytree(disk_destination,disk_destination+"_Copy_Original");

def assignment_checking_rubric_all(filename,student = None,points=None, is_late = False):
    
    if  points is None:
        file = open(filename,"w");
        file.write("Last Name, First Name, Lab id, Submitted, Correct Submitted, Does Compile, Does Run, solveMaze() ,Wrong Signeture Penalty, Is Late ,Total Percent");
    else:
        file = open(filename,"a+");
        file.write(student[2]+","+student[1]+","+student[0]+",")
        for pt in points:
            file.write(str(pt)+",")
        if is_late:
            file.write("-"+str(sum(points)*0.5)+",")
            file.write(str(sum(points)*0.5))
        else:
            file.write("-0,")
            file.write(str(sum(points)))
    file.write("\n");
    file.close();

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def check_if_actually_not_submitted(dist_disk_loc):
    for nfile in assignmentfiles:
        org_loc = find_file(nfile,dist_disk_loc)
        if org_loc is not None:
            return False   # found so false 
    return True            # not found any so true
            
def copy_maze_files(dist_disk_loc):
     root_loc = "Java\\EclipseWorkspace\\CSC220Fall2016\\"

     mazes = ["tinyMaze","straight","demoMaze","turn","classic","mediumMaze","bigMaze","unsolvable"]
     for mz in mazes:
          shutil.copyfile(root_loc+mz+".txt", dist_disk_loc+mz+".txt")

     solutions = ["tinyMazeSol","straightSol","demoMazeSol","turnSol","classicSol","mediumMazeSol","bigMazeSol","unsolvableSol"]
     for sl in solutions:
          shutil.copyfile(root_loc+sl+".txt", dist_disk_loc+sl+".txt")

def check_assignment_for_student(dist_disk):
    #global main_class, main_class_A
    new_compile_main = main_class
    #copy_a_backup_copy(dist_disk)
    latestudents = [line.strip() for line in open(dist_disk+'\\thursday10am.txt')]
    folders =  os.listdir(dist_disk)
    students.sort()
    submission_missing=[]
    submission_wrong = []
    submission_status = ["Submitted","Correct Submitted", "Does Compile","Does Run","solveMaze(in,out)","Wrong Method Name Penalty"]
    review_file = assignment.lower()+"_comments.txt"
    rubic_all_file = dist_disk+"\\"+assignment.lower()+"_rubric.csv"
    assignment_checking_rubric_all(rubic_all_file)
    comments = ""
    itri = 0
    for student in students:
        #if itri >=20:
        #    break
        itri +=1
        comments=""
        is_late = student[0] in latestudents
        submission_point = []
        for spt in range(0,len(actual_point)):
            submission_point.append(0)
        stu_lab_folder = "csc220-"+student[0]
        stu_lab_comment = dist_disk+"\\"+stu_lab_folder+"\\"+student[0]+"_"+review_file
        stu_lab_file_loc = dist_disk+"\\"+stu_lab_folder
        is_copy = True
        no_submission = False
        assignment_checking_comments(stu_lab_comment,"",1)
        if stu_lab_folder not in folders or check_if_actually_not_submitted(stu_lab_file_loc):
            submission_missing.append(student)
            if stu_lab_folder not in folders:
                os.makedirs(stu_lab_file_loc)
            assignment_checking_comments(stu_lab_comment,"No asignment Submitted.\n")
            is_copy = False
            no_submission = True
        elif check_correct_assignment_submission(stu_lab_file_loc,assignment,assignmentfiles) is False:
            submission_point[0]=actual_point[0]
            submission_wrong.append(student)
            assignment_checking_comments(stu_lab_comment,"Assignment Submission is Wrong. \n")
            is_copy = create_copy_the_file_in_correct_order(stu_lab_file_loc)
            stu_lab_file_loc = stu_lab_file_loc+"\\TA"
        else:
            submission_point[0]=actual_point[0]  # assignment submitted
            submission_point[1]=actual_point[1]  # assignment submitted correctly
        # now compile and run
        new_compile_main = main_class
        if is_copy:
            source_folder = stu_lab_file_loc+"\\"+assignment+"\\src\\"
            package_folder  = stu_lab_file_loc+"\\"+assignment+"\\src\\"+assignment.lower()
            src_main="Java\\EclipseWorkspace\\CSC220Fall2016\\src\\"+assignment.lower()+"\\"+main_file
            shutil.copyfile(src_main,package_folder+"\\"+main_file)
                       
            #copy all files
            copy_maze_files(source_folder);
            # now compile
            javac_command = package_folder+"\\"+main_file;
            for cname in compile_files:
                javac_command += " "+package_folder+"\\"+cname;
            
            javac_command = "javac "+javac_command
            #print javac_command
            compile = os.popen(javac_command); 
            #print compile.errors
            output = compile.read()
            #print output
            is_compiled = compile.close()
            #print str(is_compiled)+student[0]
            is_second_compile = False
            output = "";
            if is_compiled is not None:
                javac_command = package_folder+"\\"+main_file_A;
                for cname in compile_files_A:
                    javac_command += " "+package_folder+"\\"+cname;
                javac_command = "javac "+javac_command
                #print javac_command
                compile = os.popen(javac_command); 
                output = compile.read()
                is_compiled = compile.close()
                is_second_compile = True
                new_compile_main = main_class_A
                if is_compiled is not None:
                    print "failed to compile second time ----- "+student[0]+student[1]+student[2]
                #else:
                    #print "compile second time"
            #else:
                #print "compile first time"

                 

            output = "-1"
            is_run_successfully = 1
            # now run
            output = ""
            if is_compiled is None:
                print "Now running ..... "+student[0]+student[1]+student[2];
                submission_point[2]=actual_point[2]   # program compiled successfully
                java_run = "java -cp " + source_folder + " " +assignment.lower()+"."+new_compile_main +" "+source_folder
                #print java_run
                run = os.popen(java_run);
                output = run.read();
                is_run_successfully = run.close()
                output = output.strip()
            else:
                assignment_checking_comments(stu_lab_comment,"Program doesn't compile. \n")
                submission_wrong.append(student)

            if is_run_successfully is None:
                submission_point[3] = actual_point[3]  # program run successfully
            elif is_compiled is None:
                assignment_checking_comments(stu_lab_comment,"Program compile and run but has runtime error. \n")
            comments = "";
            if is_compiled is None and is_run_successfully is None:
                #if is_second_compile:
                    #submission_point[-1] = actual_point[-1]
                    #assignment_checking_comments(stu_lab_comment,"Your program doesn't use all the same method and/or veriable names as it is written in the assignment document.\n")
                    #print "---- Compiled with checkout: "+student[0]+student[1]+student[2]
                message = []
                try:
                    message = output[output.index("$$")+2:output.rindex("$$")].split("$$");
                    comments = output[output.rindex("$$")+2:];
                except:                
                    print "---- parsing exception: "+student[0]+student[1]+student[2]
                #print message
                #print comments
                for spt in range(0,len(message)):
                    submission_point[spt+4] = float(message[spt])
                
                assignment_checking_comments(stu_lab_comment,comments+"\n");
                                
        elif no_submission is False:
            assignment_checking_comments(stu_lab_comment,"Your file submission is wrong. Or you haven't submit all files!\n")
        assignment_checking_rubic(stu_lab_comment,submission_point,submission_status,is_late)
        assignment_checking_rubric_all(rubic_all_file,student,submission_point,is_late)
        print student[1]+ student[2] + " done"

    file = open(dist_disk+"\\Double_check_code.txt","w")
    file.write("Username, First Name, Last Name\n");
    for ms in submission_wrong:
        file.write(ms[0]+", " +ms[1]+", "+ms[2]+"\n");
    file.close()



def check_wrong_package_name(dist_disk):
    copy_a_backup_copy_original(dist_disk)
    submission_wrong = []
    students.sort()
    for student in students:
        stu_lab_folder = "csc220-"+student[0]
        stu_lab_file_loc = dist_disk+"\\"+stu_lab_folder
        for nfile in assignmentfiles:
            org_loc = find_file(nfile,stu_lab_file_loc)
            if org_loc is not None:
                code_file = open(org_loc, "r")
                whole_code = code_file.read()
                code_file.close()
                if(whole_code.find(assignment.lower()+";")) == -1:
                     submission_wrong.append(student)
                     break
    file = open(dist_disk+"\\wrong_package_name.txt","w")
    file.write("Username, First Name, Last Name\n")
    for ms in submission_wrong:
        file.write(ms[0]+", " +ms[1]+", "+ms[2]+"\n")
        print(ms[0]+", " +ms[1]+", "+ms[2])
    file.close()
    


def submit_grade_in_box(dist_disk,box_add):
    students.sort()
    for student in students:
        review_file = student[0]+"_"+assignment.lower()+"_comments"
        disk_stu_lab_comment = dist_disk+"\\"+"csc220-"+student[0]
        box_stu_lab_comment = box_add+"csc220-"+student[0]
        #make the pdf
        write_simple_pdf(disk_stu_lab_comment,review_file)
        shutil.copyfile(disk_stu_lab_comment+"\\"+review_file+".pdf",box_stu_lab_comment+"\\"+review_file+".pdf")
        print "Copid for "+student[1]+student[2]





def check_everything_together(disk_destination):
    string = "_Graded"
    if os.path.exists(disk_destination+string):
        if raw_input('Allready graded? Do you want to remove previous grade?(y/n) : ').lower()[0] == 'y':
           shutil.rmtree(disk_destination+string)
        else:
            return
    shutil.copytree(disk_destination,disk_destination+string);
    print "Waiting 5 seconds !"
    for i in range(0,6):
        print "%d "%(5-i)
        time.sleep(1)
    check_assignment_for_student(disk_destination+string)

def submit_grade_in_box(dist_disk,box_add):
    students.sort()
    for student in students:
        review_file = student[0]+"_"+assignment.lower()+"_comments"
        disk_stu_lab_comment = dist_disk+"\\"+"csc220-"+student[0]
        box_stu_lab_comment = box_add+"csc220-"+student[0]
        #make the pdf
        write_simple_pdf(disk_stu_lab_comment,review_file)
        shutil.copyfile(disk_stu_lab_comment+"\\"+review_file+".pdf",box_stu_lab_comment+"\\"+review_file+".pdf")
        print "Copid for "+student[1]+student[2]

#check_shared_folder(distadd,assignment,assignmentfiles)

#submited_students = [line.strip() for line in open(disk_main_add+assignment+"\\wednesday10am.txt")]
#print   submited_students


#check_assignment_for_student(disk_main_add+"Test1");
#check_wrong_package_name(disk_main_add+"Test1")
#copy_a_backup_copy(disk_main_add+"Test1");

#check_wrong_package_name(disk_main_add+assignment)    

#check_assignment_for_student(disk_main_add+assignment)



#replace_pivate_with_protected(disk_main_add+assignment)
if raw_input('Working on the assignment: '+assignment+', Do you want to continue? y/n ? ').lower()[0] == 'n':
    print("Exiting Without doing anything..........................")
    exit(1)
#copy_assignment_with_name(distadd, disk_main_add+assignment);
#copy_assignment_with_name_late(distadd, disk_main_add+assignment);
#check_wrong_package_name(disk_main_add+assignment)
#check_everything_together(disk_main_add+assignment);

# -- nfox

#put grade
#submit_grade_in_box(disk_main_add+assignment+"_Graded",distadd);