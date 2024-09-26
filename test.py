import random

with open('files/data_table2.txt','w') as file:
    file.write('FactTable\n')
    rand_values = ['A','B','C']
    rand_values2= ['X','Y']
    rand_values3= ['p1','p2','p3','lri','psi']
    rand_values4= ['b','w','a','l']
    matr = [rand_values,rand_values2,rand_values3,rand_values4]
    for i in range(9000):
        file.write(str(i+1))
        file.write(', ')
        file.write(str(rand_values[random.randint(0,2)]))
        file.write(', ')
        file.write(str(rand_values2[random.randint(0,1)]))
        file.write(', ')
        file.write(str(rand_values3[random.randint(0,4)]))
        file.write(', ')
        file.write(str(rand_values4[random.randint(0,3)]))
        file.write(', ')
        file.write(str(random.randint(1,50)))
        file.write(', ')
        file.write(str(random.randint(-5,10)*11))
        file.write(', ')
        file.write(str(random.randint(1,20)*100))
        file.write(', ')
        file.write(str(random.randint(1,10)*random.randint(6,19)))
        file.write('\n')
    file.write('\n')
    for i in range(4):
        file.write('D')
        file.write(str(i+1))
        file.write('\n')
        for j in range (250):
            file.write(str(matr[i][random.randint(0,len(matr[i])-1)]))
            file.write(', ')
            file.write(str(round(random.random()*5,2)))
            file.write(', ')
            file.write(str(random.randint(-1,1)*round(random.random(),2)))
            file.write('\n')
        file.write('\n')
        
