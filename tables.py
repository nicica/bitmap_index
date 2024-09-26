class Table:
    def __init__(self,name, indexes):
        self.name = name
        self.indexes=indexes
        self.values = {}
        for index in indexes:
            self.values[index] = []
    def reset_values(self):
        self.values = {}
        for index in self.indexes:
            self.values[index] = []
    def put_values(self, line):
        value__arr = [item.strip() for item in line.split(', ')]
        i=0
        for value in self.values:
            self.values[value].append(value__arr[i])
            i+=1
    def put_values_directly(self, value__arr):
        i=0
        for value in self.values:
            self.values[value].append(value__arr[i])
            i+=1
    def print_table(self):
        print(self.name)
        for value in self.values:
            print(value, end='\t')
        print('\n',end='')
        if len(self.values[self.indexes[0]])==0:
            return
        for i in range(len(self.values[self.indexes[0]])):
            for value in self.values:
                print(self.values[value][i],end='\t')
            print('\n',end='')


