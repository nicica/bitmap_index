from tables import Table
import re
from math import log2
import time

bitmap = {}
tables={}

def create_bitmap_index(values):
    indexes = {}
    d_values = set(item for item in values)
    for val in d_values:
        index_value = 0b0
        for i in range(len(values)):
            if val==values[i]:
                index_value|= (1<< (len(values)-1-i))
        index_value=bin(index_value)
        indexes[val]=index_value
    return indexes

def search_with_index(conditions, logic_op):
    if len(conditions)==0:
        return tables['FactTable']
    results = Table("Results",tables['FactTable'].indexes)
    next_op = 'OR'
    bit_index = 0b0
    logic_op_point = -1

    for cond in conditions:
        if next_op=='OR':
            bit_index |= int(bitmap[cond[0]][cond[1]],2)
        elif next_op=='AND':
            bit_index &= int(bitmap[cond[0]][cond[1]],2)
        logic_op_point+=1
        if logic_op_point<len(logic_op):
            next_op = logic_op[logic_op_point]
    size = len(tables['FactTable'].values[tables['FactTable'].indexes[0]])
    point = 1 << (size-1)
    while point>0:
        if (point & bit_index)!=0:
            result_values = []
            for ind in tables['FactTable'].indexes:
                result_values.append(tables['FactTable'].values[ind][int(size-1 -log2(point))])
            results.put_values_directly(result_values)
        point >>= 1
    return results

def normal_search(conditions, logic_op):
    if len(conditions)==0:
        return tables['FactTable']
    results = Table("Results",tables['FactTable'].indexes)
    logic_op_point = -1
    next_op='OR'
    for cond in conditions:
        if next_op=='OR':
            i=0
            for res in tables['FactTable'].values[cond[0]]:
                if res == cond[1]:
                    put_values = []
                    for indx in tables['FactTable'].indexes:
                        put_values.append(tables['FactTable'].values[indx][i])
                    if put_values[0] not in results.values['ID']:
                        results.put_values_directly(put_values)
                i+=1
        elif next_op=='AND':
            i=0
            new_values_m = []
            for res in results.values[cond[0]]:
                if res == cond[1]:
                    new_values_a = []
                    for indx in results.indexes:
                        new_values_a.append(results.values[indx][i])
                    new_values_m.append(new_values_a)
                i+=1
            results.reset_values()
            for arr in new_values_m:
                results.put_values_directly(arr)
        logic_op_point+=1        
        if logic_op_point<len(logic_op):
            next_op=logic_op[logic_op_point]
    return results

def apply_aggregate_function(results, agg_function):
    if agg_function not in ('min','max','avg','sum','count'):
        return results
    nueve_indexs= []
    pattern = r'^Fact\d+$'
    for indx in results.indexes:
        if re.match(pattern, indx):
            nueve_indexs.append(indx)
    
    results_new=Table(results.name,nueve_indexs)
    for indx in results_new.indexes:
        if agg_function == 'min':
            results_new.values[indx].append(min(results.values[indx]))
        elif agg_function == 'max':
            results_new.values[indx].append(max(results.values[indx]))
        elif agg_function == 'avg':
            results_new.values[indx].append(sum(results.values[indx])/len(results.values[indx]))
        elif agg_function == 'sum':
            results_new.values[indx].append(sum(results.values[indx]))
        elif agg_function == 'count':
            results_v3 = Table("Results",['count'])
            results_v3.values['count'].append(len(results.values[indx]))
            return results_v3
    return results_new


def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    data_no_n = [line.strip() for line in data]
    return data_no_n
    
def parse_schema_row(fact_line):
    key, value = fact_line.split(':')
    value = value.strip()
    value_arr = [item.strip() for item in value.split(', ')]
    return key, value_arr

def parse_data_row(data_line):
    return

def main():
    # Parse schema and data from input files
    fact_table = parse_input_file('files/fact_table2.txt')
    data_table = parse_input_file('files/data_table2.txt')
    #kreiranje tabela
    for line in fact_table:
        if line=='':
            break
        key, indexes = parse_schema_row(line)
        table = Table(key, indexes)
        tables[key]= table
    #popunjavanje tabela
    filling_data = False
    for line in data_table:
        if not filling_data and line in tables:
            table_to_fill = tables[line]
            filling_data = True
        elif filling_data and line!='':
            table_to_fill.put_values(line)
        elif filling_data and line=='':
            filling_data=False
    #kreiranje bitmap indeksa
    pattern = r'^D\d+$'
    for ind in tables['FactTable'].indexes:
        if re.match(pattern, ind):
            bitmap[ind] = create_bitmap_index(tables['FactTable'].values[ind])
    
    query_conditions = []
    query_additional_logic_ops = []

    avabiable_indexes =[]

    
    for id in tables['FactTable'].indexes:
        if re.match(pattern, id):
            avabiable_indexes.append(id)
    
    while True:
        print('Type one of the following indexes to search by (type n for whole table): ')
        for ai in avabiable_indexes:
            print(ai,end=' ')
        print('')
        inp_i = input()
        if inp_i=='n':
            break
        if inp_i not in avabiable_indexes:
            continue
        print("Type the value to which you want to search the column by: ")
        inp_v= input()
        query_conditions.append((inp_i,inp_v))
        while True:
            print('Do you want an additional condition with logic operation AND or OR (type n if you want to start the search immediatly)?')
            logic_op = input()
            if logic_op in ['AND','OR','n']:
                break
        if logic_op=='n':
            while True:
                print('Do you want bitmap(Y) search or normal(N) search?')
                srch = input()
                if srch in ['Y','N']:
                    break
            break
        query_additional_logic_ops.append(logic_op)
    start_time=time.process_time()
    if srch=='Y':
        rezultati = search_with_index(query_conditions,query_additional_logic_ops)
    else:
        rezultati = normal_search(query_conditions,query_additional_logic_ops)
    aggregation = 'none'

    rezultati = apply_aggregate_function(rezultati, aggregation)

    total_search_time = time.process_time()

    rezultati.print_table() 

    

    for cond in query_conditions:
        tabela = Table(cond[0],tables[cond[0]].indexes)
        i=0
        for res in tables[cond[0]].values[cond[0]]: 
            if res == cond[1]:
                put_values = []
                for indx in tables[cond[0]].indexes:
                    put_values.append(tables[cond[0]].values[indx][i])
                tabela.put_values_directly(put_values)
            i+=1
        print('')
        tabela.print_table()
    print('\nTotal search time is: ',str(total_search_time-start_time),'s')


    
    
if __name__ == "__main__":
    main()
