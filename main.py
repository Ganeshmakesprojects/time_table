import mysql.connector as mc
import random 
import numpy as np
import matplotlib.pyplot as plt

mydb = mc.connect( user='vamshi', password='{cookies}',host = '127.0.0.1' ,auth_plugin='mysql_native_password', database='db')

mycursor = mydb.cursor()

# mycursor.execute("select batchid, profid from batch, professor where batch.courseid = professor.courseid")

# bp = mycursor.fetchall()

# mycursor.execute("select profid, courseid from professor, course where course.courseid = professor.courseid")

# pc = mycursor.fetchall()

mycursor.execute("select * from batch")

batch = mycursor.fetchall()

mycursor.execute("select * from professor")

prof = mycursor.fetchall()

mycursor.execute("select * from course")

crs = mycursor.fetchall()

mycursor.execute("select * from rooms")

rooms = mycursor.fetchall()

room = [i[0] for i in rooms]

course = {}
crs_name = {}
# Course is a dictionary with courseid as key and hours as value
# crs_name is a dictionary with course_id as key and course_name as value
for i in crs : 
	if i[0] not in course : 
		course[i[0]] = i[2]
		crs_name[i[0]] = i[1]

professor = {}
prof_name = {}
# professor is a dictionary with courseid as key and prof_id as value
# prof_name is a dictionary with prof_id as key and prof_name as value
for i in prof : 
	if i[2] not in prof : 
		professor[i[2]] = i[0]
	prof_name[i[0]] = i[1]

time = [i  for i in range(8,12)]
time += [i  for i in range(13,17)]
day = [i for i in range(1,6)]

dayname = {0:"Monday   ",1:"Tuesday  ",2:"Wednesday",3:"Thursday ",4:"Friday   "}


POPULATION_SIZE = 20


#Chormosome = Time table with tuples containing (batch , prof , day , time , room)

class Timetable(object) :
	def __init__(self, chromosome): 
		self.chromosome = chromosome 
		self.fitness = self.cal_fitness()

	# @classmethod
	def mutated_gene(self) :
		global day , time , room
		return (random.choice(day) , random.choice(time), random.choice(room))

	def crossover(self, par2): 
		''' 
		Perform crossover and produce new offspring 
		'''
		child_chromosome = [] 
		for gp1, gp2 in zip(self.chromosome, par2.chromosome):	 

			# random probability 
			prob = random.random() 

			# if prob is less than 0.45, insert gene 
			# from parent 1 
			if prob < 0.495: 
				child_chromosome.append(gp1) 

			# if prob is between 0.45 and 0.90, insert 
			# gene from parent 2 
			elif prob < 0.99: 
				child_chromosome.append(gp2) 

			# otherwise insert random gene(mutate), 
			# for maintaining diversity 
			else: 
				dt = self.mutated_gene()
				child_chromosome.append((gp1[0] , gp1[1] , gp1[2] , dt[0] , dt[1], dt[2])) 

		return Timetable(child_chromosome) 

	@classmethod
	def create_gnome(self): 
		global batch , professor , course , day , time , room
		ttable = []
		for i in batch :
			#Number of hours in the course
			for j in range(course[i[1]]) :  
				gene = (i[0] , i[1] , professor[i[1]] , random.choice(day),random.choice(time),random.choice(room)) 
				ttable.append(gene)
		return ttable

	def cal_fitness(self):  
		global  day , time
		fitness = 0
		mat = np.zeros(shape = (len(day) , len(time)) , dtype = 'object')
		#Check if two time intervals have doesn't have same batch
		for i in self.chromosome :
			d = day.index(i[3])
			t = time.index(i[4])
			#insert batchid ,  into matrix elements
			if mat[d,t] == 0 :
				mat[d,t] = [[i[0]] , [i[2]], []]
			else : 
				if i[0] in mat[d,t][0] :
					fitness += 1
				else :
					mat[d,t][0].append(i[0])
				if i[2] in mat[d,t][1] :
					fitness += 1
				else :
					mat[d,t][1].append(i[2])
				if i[5] in mat[d,t][2] :
					fitness += 1
				else :
					mat[d,t][2].append(i[5])

		return fitness


def print_batch_tt(timtable , b) :
	global day , time , dayname , crs_name , professor, prof_name , batch

	mat = np.zeros(shape = (len(day) , len(time)) , dtype = 'object')
	file_name = "batch"+str(b) + ".txt"
	f = open(file_name , "w")
	for i in timtable :
		if i[0] == b :
			d = day.index(i[3])
			t = time.index(i[4])
			mat[d,t] = [i[1] , i[5]]
	print(end = '\t\t')
	for i in time :
		if i < 9 :
			print('0'+str(i) + '-'+ '0' +str(i+1) , end="  ")
		if i == 9 :
			print('0'+str(i) + '-' +str(i+1) , end="  ")
		if i >= 10 :
			print(str(i) + '-'+ str(i+1) , end="  ")
	print(end = "\n\n")
	for i in range(len(day)) : 
		print(dayname[i] , end = "\t")
		for j in range(len(time)) :
			if mat[i][j] == 0 :
				print('enjoy' , end = "  ")
			else :
				print(mat[i,j][0] , mat[i,j][1] , end = "  ")
		print()

	#Write in a file
	f.write('\n\t\t')
	for i in time :
		if i < 9 :
			f.write('0'+str(i) + '-'+ '0' +str(i+1)+"  ")
		if i == 9 :
			f.write('0'+str(i) + '-' +str(i+1) + "  ")
		if i >= 10 :
			f.write(str(i) + '-'+ str(i+1) + "  ")
	#All the time stamps i.e the main columns
	f.write("\n\n")
	for i in range(len(day)) : 
		f.write(dayname[i] + "\t")
		for j in range(len(time)) :
			if mat[i][j] == 0 :
				f.write('enjoy' + "  ")
			else :
				f.write(str(mat[i,j][0])+' ' + str(mat[i,j][1]) + "  ")
		f.write("\n")
	f.close()

	#Append to the file the details of the professor
	f = open(file_name , 'a')
	f.write("\n\nInformation : \n")
	for i in batch :
		if i[0] == b :
			f.write(str(i[1])+ ". " + crs_name[i[1]] + " : " + prof_name[professor[i[1]]]+ "\n")
	f.write("\n")

	f.close()

def main() :
	generation = 1

	found = False
	population = []
	generations = []
	fitness_rec = [] 

	for _ in range(POPULATION_SIZE): 
				gnome = Timetable.create_gnome() 
				population.append(Timetable(gnome))

	while not found: 

		# sort the population in increasing order of fitness score 
		population = sorted(population, key = lambda x:x.fitness) 

		#Chromosome with lowest fitness i.e 0 is preferred.
		if population[0].fitness <= 0: 
			found = True
			break

		# Otherwise generate new offsprings for new generation 
		new_generation = [] 

		#10% of the highest fittest population are taken to next generation
		s = int((20*POPULATION_SIZE)/100) 
		new_generation.extend(population[:s]) 

		# From 50% of fittest population, Individuals 
		# will crossover to produce offspring 
		s = int((80*POPULATION_SIZE)/100) 
		for _ in range(s): 
			parent1 = random.choice(population[:10]) 
			parent2 = random.choice(population[:10]) 
			child = parent1.crossover(parent2) 
			new_generation.append(child) 

		population = new_generation 

		generation += 1
		generations.append(generation)
		fitness_rec.append(population[0].fitness)
		# if generation > 1 :
		# 	break
		print("generation : " , generation)
		print("fitness : " , population[0].fitness)

	
	# print("Generation: {}\nTime table: {}\tFitness: {}".\
	# 	format(generation, 
	# 	population[0].chromosome, 
	# 	population[0].fitness)) 

	best_tt = population[0].chromosome

	b = set(i[0] for i in batch)
	
	for bach in b :
		print("\t\tBATCH : ",bach)
		print()
		print_batch_tt(best_tt , bach)
		print()

	plt.plot(generations, fitness_rec) 
  
	plt.xlabel('Generation') 
	plt.ylabel('Fitness') 
	  
	# giving a title to my graph 
	plt.title('Generation Vs Fitness') 
	  
	plt.show() 

if __name__ == '__main__' :
	main()