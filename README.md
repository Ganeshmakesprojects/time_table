Input : 
The datavam.sql file creates the required database which contains professors, subjects, number of hours, number of batches etc..

Command : source ./data_vam.sql (./ implies the files should be executed in the same directory.)

Output : 
Based on the number of batches, batch.txt files are created for every batch with necessary professor information given in the batch.txt files

Command : python main.py

main.py takes input from the database and uses genetic algorithms to generate least conflicting time table.

  Genetic algorithms first generates fixed number of random time tables which is called the population. The number of conflicts are 
calculated which is called the fitness of the time table. If the fitness is 0 then the time table obtained has 0 conflicts which is 
optimal. 

  The population is sorted according to its fitness and sorted in ascending order. The top n time tables are taken and cross over is done 
between them. Cross over involves randomly selecting two time tables and mutating i.e. the attributes are interchanged between them and a 
child time table is born. Therefore, a new population is formed and the process is repeated until the least amount of conficts are found.

  The top time table of the final population is considered as the best time table that can be produced.
