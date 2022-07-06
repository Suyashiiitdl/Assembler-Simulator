#CO Final
import sys
registers = {'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'011','FLAGS':'111'}
opcode = {'add':'10000',
          'sub':'10001',
          'mul':'10110',
          'xor':'11010',
          'or':'11011',
          'and':'11100',
          'ld':'10100',
          'st':'10101',
          'div':'10111',
          'mov':'10011',   # of typeC(mov R1 R2)
          'rs':'11000',
          'ls':'11001',
          'not':'11101',
          'cmp':'11110',
          'jmp':'11111',
          'jlt':'01100',
          'jgt':'01101',
          'je':'01111',
          'hlt':'01010'}


data = []

filled_lines = 0

data = sys.stdin.read().split('\n')
data = [x.split() for x in data if x != '\n' and x != '']
filled_lines = len(data)


"""
for i in range(0,lines):
    n = input().split(' ')
    
    if n == [' ']:
        continue
    data.append(n)
    
    filled_lines+=1
"""


vars ={}
labels ={}
varCount = 0
prog_counter = 0

## variable and lables storing
for i in range(0,filled_lines):
    instruction = data[i]

    if instruction[0] == "var":
        prog_counter -= 1
        varCount += 1

    if instruction[0][-1] == ":":
        if len(instruction) < 2:
        #           print(f"Error: Label instruction is Invalid in line {prog_counter +1 +varCount}")
                    continue
                    
        a = str(instruction[0][:-1])
        labels[a] = str(bin(prog_counter).replace("0b","").rjust(8,"0"))
    prog_counter+=1

for i in range(0,filled_lines):
    instruction = data[i]
    if instruction[0] == "var":
        if len(instruction)==1:
            continue
            #print("ERROR: UNDEFINED VARIABLE")
        else:
            a = str(instruction[1])
            vars[a] = str(bin(prog_counter).replace("0b","").rjust(8,"0"))
            prog_counter+=1

##### Error checking#######

label_rep = []
prog_count = 0
def main(n):
    
    global registers
    global opcode
    global labels
    global vars
    global prog_count
    global filled_lines
    global label_rep
    
    op_name = opcode.keys()
    reg_name = registers.keys()
    var_name = vars.keys()
    lable_name = labels.keys()

    ###Error Checking###

    if (n[0] not in op_name) and (n[0] != 'var') and (n[0][:-1] not in lable_name):
        prog_count +=1
        return(f"Error: INVALID OPCODE INSTRUCTION")


    if (n[0] == 'hlt') and (prog_count !=filled_lines - 1) :
        prog_count +=1
        return(f"Error: Halt instruction in between the program in line {prog_counter}")

    if (prog_count == filled_lines -1) and (n[0] != 'hlt'):
        prog_count +=1
        return("Error: No Halt instruction in the end")


    if (n[0][-1] == ":") and (len(n) < 2):
        prog_count +=1
        return ("Error: Label instruction is Invalid")

    if n[0] == "var" and len(n)==1:
        prog_count +=1
        return("Error: UNDEFINED VARIABLE")
                    
    #Variables
    if (n[0] == "var"):
        if len(n) == 2:
            prog_count += 1
            return
        else:
            prog_count +=1
            return(f"Error: Incorrect Variable Declaration in line {prog_count}")

    #Labels
    lable_name = labels.keys()
    n1 = n[0][:-1]
    if (n1 in lable_name):
        if n1 in label_rep:
            prog_count +=1
            return(f"Error: Label Repetition in line {prog_count}")
        label_rep.append(n1)
        if len(n) < 2:
            prog_count += 1
            return (f"Error: Invalid Lable Declaration in line {prog_count}")
        if n[1] not in op_name:
            prog_count +=1
            return (f"Error: Invalid Lable Instructions in line {prog_count}")
        if len(n)>4:
            prog_count +=1
            return (f"Error: Invalid Lable Instructions in line {prog_count}")
        else:
            prog_count += 1
            return
    
    
    # A_type
    instrA = ['add','sub','mul','xor','or','and']
    if (len(n) == 4) and (n[0] in instrA):
        n1 = n[0]
        n2 = n[1]
        n3 = n[2]
        n4 = n[3]
        
        x1 = opcode.get(n[0])
        if (n1 not in instrA) :
            prog_count += 1
            return(f"Error: INVALID OPCODE in line {prog_count}")
        if (n2 not in reg_name) or (n3 not in reg_name) or (n4 not in reg_name):
            prog_count += 1
            return(f"Error: INVALID REGISTER NAME in line {prog_count}")
            
        x2 = registers.get(n[1])
        x3 = registers.get(n[2])
        x4 = registers.get(n[3])
        a = x1 + '00' + x2 + x3 + x4
        prog_count += 1
        return(a)

    #B_type
    instrB = ['mov','ls','rs']
    if (len(n) == 3) and (n[2][0] == '$') and (n[0] in instrB):
        if (n[1] not in reg_name):
            prog_count += 1
            return(f"Error: INVALID REGISTER NAME in line {prog_count}")
        
        n1 = n[0]
        if n1 == 'mov':
            x1 = '10010'
        else:    
            x1 = opcode.get(n[0])
        x2 = registers.get(n[1])
        x3 = n[2][1:]
            
        a = x3.isdigit()
        if a == False:
            prog_count += 1
            return(f"Error: INVALID VALUE ONLY WHOLE NUMBERS ARE VALID in line {prog_count}")          

        if int(float(x3))>255 or int(float(x3))<0:
            prog_count += 1
            return(f"Error: OVERFLOW FOR IMMEDIATE VALUE in line {prog_count}")
            
        z3 = ""
        y3 = str(bin(int(x3)))[2:]
        length = len(y3)
        for i in range(0,8-length):
            z3 = z3 + '0'
        z3 = z3 + y3
     
        a = x1 + x2 +z3
        prog_count += 1
        return(a)
    if (n[0] in instrB) and(len(n) != 3):
        prog_count +=1
        return ("Error: Invalid Instruction in line {prog_count}")
    if (n[0] in instrB) and (n[2][0] != '$') and (n[0] != 'mov'):
        prog_count +=1
        return ("Error: Invalid Instruction in line {prog_count}")

    

    #D_type
    if (n[0] == 'ld' or n[0] == 'st'):
        
        x1 = opcode.get(n[0])
        x2 = registers.get(n[1])

        if (n[1] not in reg_name):
            prog_count += 1
            return (f"Error: INVALID REGISTER NAME in line {prog_count}")
        
        #var_name = vars.keys()
        if n[2] not in var_name:
            prog_count += 1
            return (f"Error: UNDEFINED VARIABLE in line {prog_count}")
        if len(n) != 3:
            prog_count +=1
            return ("Error: Invalid Instruction in line {prog_count}")
        
        x3 = vars.get(n[2])
        a = x1 + x2 + x3
        prog_count += 1
        return a

    #C_type
    instrC = ['mov','div','not','cmp']
    if n[0] in instrC and n[2][0] != '$':
        if len(n) != 3:
            prog_count +=1
            return ("Error: Invalid Instruction in line {prog_count}")
            
        n1 = n[0]
        x1 = opcode.get(n[0])
        x2 = registers.get(n[1])
        x3 = registers.get(n[2])


        if (n[1] not in reg_name) or ((n[2] not in reg_name)):
            prog_count += 1
            return (f"Error: INVALID REGISTER NAME in line {prog_count}")

        if n1 not in instrC:
            prog_count += 1
            return(f"Error: INVALID OPCODE in line {prog_count}")
            
        a = x1 + '00000' +x2 + x3
        prog_count += 1
        return (a)
        
    #E_type
    instrE = ['jmp','jlt','jgt','je']
    if (n[0] in instrE):
        x1 = opcode.get(n[0])
        x2 = labels.get(n[1])

        if len(n) != 2:
            prog_count +=1
            return ("Error: Invalid Instruction in line {prog_count}")

        lable_name = labels.keys()
        if n[1] not in lable_name:
            prog_count += 1
            return (f"Error: UNDEFINED LABLE in line {prog_count}")

        a = x1 + '000' + x2
        prog_count += 1
        return (a)
    
    #F_type
    if len(n) == 1:
        n1 = n[0]
        if n1 != 'hlt':
            prog_count += 1
            return(f"Error: INVALID OPCODE in line {prog_count}")
            
        a = '01010' + '00000000000'
        prog_count += 1
        return(a)
    else:
        prog_count += 1
        return(f"Error: Invalid Instruction in line {prog_count}")

binary = []

for i in data:
    a = main(i)
    binary.append(a)

for i in binary:
    if i == None:
        continue
    print(i)
    


