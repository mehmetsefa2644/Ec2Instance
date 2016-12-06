////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                     

WELCOME TO THE DOCUMENTATION OF WFSCHED PROGRAM



wfsched is the program, written in Python, that
    

-creates an ec2 instance, and transfers your workflow directory to the
 ec2 instance,
    
-topologically sorts your workflow depending on the dependencies in *.wdf file which you explain your
 dependencies,
    
-brings back the executed files to your ~/Downloads/2016400372BALIK directory.
    
-terminates your instance.



************PYTHON3 AND BOTO3 SHOULD BE DOWNLOADED TO YOUR PC, AND PYTHON3 SHOULD BE ADDED TO YOUR PATH*****************

                                    

++++USAGE++++

                                ./wfsched.py myworkflow [-v]



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
-put your workflow file, including *.wdf file, into the same folder with wfsched.py

    
-pass your workflow file name as argument
        ./wfsched.py <yourworkflowfilename> [-v]

    
- -v can be added to verbosity


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
EXAMPLE WORKFLOW FILE

    

-myworkflow
        
-description.wdf
        
-prog1.py
        
-prog2.py
        
-prog3.py
        
-prog4.py
        
-prog5.py



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    
.WDF FILE EXAMPLE

    
A: prog1.py hello
    
B: prog1.py world
    
C: prog2.py 23 45
    
D: prog3.py
    
E: prog4.py a b c
    
F: prog1.py istanbul
    
G: prog5.py
    
%%
    
A => D
    
B => D
    
D => F
    
B => E
    
C => E
    
C => G
    
E => G







