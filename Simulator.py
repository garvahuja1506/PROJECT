import sys

global PC
PC = '0b00000000000000000000000000000000'

# Functions
def decimal_hexa(num):
    if not (0<=num<=0xFFFFFFFF):
        raise ValueError("Decimal number must be within the range of 0 to 4294967295 for 8-digit representation.")
    hexadecimal=hex(num)
    hexadecimal=hexadecimal[2:]
    hexadecimal='0x' + str(hexadecimal.zfill(8))
    return hexadecimal
    
def sign_ext_decimal(binary):
    if binary[0]=='1':
        sign=-1
    else:
        sign=1
    if sign==-1:
        binary = ''.join('1' if char == '0' else '0' for char in binary)
        binary = bin(int(binary, 2) + 1)[2:]
    decimal = int(binary, 2)
    return decimal*sign

def decimal_sign_ext(decimal):
    if decimal<0:
        decimal=abs(decimal)
        binary = bin(decimal ^ ((1<<32)-1))[2:]
    else:
        binary = bin(decimal & ((1<<32)-1))[2:]
    binary=binary.zfill(32)
    if decimal<0:
        binary = bin(int(binary, 2) + 1)[2:]
    return binary

def signed_decimal(binary):
    if binary[0]=='1':
        sign=-1
    else:
        sign=1
    length=len(binary)
    if sign==-1:
        for i in range(length):
            if binary[i]=='1':
                for j in range(i - 1, -1, -1):
                    binary[j] = '1' if binary[j] == '0' else '0'
                break
    decimal = 0
    for i in range(len(binary) - 1, 0, -1):
        if binary[i] == '1':
            decimal += 2 ** (len(binary)-1-i)
    return decimal * sign
    
def decimal_signed(decimal):
    if decimal<0:
        decimal = abs(decimal)
        binary = bin(decimal)[2:].zfill(31)
        binary = '1' + binary
    else:
        binary = bin(decimal)[2:].zfill(31)
        binary = '0' + binary
    return binary

def unsigned_decimal(binary):
    decimal=0
    length=len(binary)

    for i in range(length-1,-1,-1):
        if binary[i] == '1':
            decimal += 2 ** (length-1-i)
    return decimal
            

def decimal_unsigned(decimal):
    binary=bin(decimal)[2:].zfill(32)
    binary='0'+binary
    return binary
def sub(rd, rs1, rs2):
    global PC
    rs1_value = sign_ext_decimal(register_values[rs1][2:])
    rs2_value = sign_ext_decimal(register_values[rs2][2:])
    rd_value = rs1_value - rs2_value
    register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b'+decimal_sign_ext(unsigned_decimal(PC[2:]) + 4)

def add(rd, rs1, rs2):
    global PC
    rs1_value = sign_ext_decimal(register_values[rs1][2:])
    rs2_value = sign_ext_decimal(register_values[rs2][2:])
    rd_value = rs1_value + rs2_value
    register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b'+decimal_sign_ext(unsigned_decimal(PC[2:]) + 4)

def sll(rd, rs1, rs2):
    global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][-5:])
    rd_value = rs1_value << rs2_value
    register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def slt(rd, rs1, rs2):
    global PC
    rs1_value = sign_ext_decimal(register_values[rs1][2:])
    rs2_value = sign_ext_decimal(register_values[rs1][2:])

    if rs1_value < rs2_value:
        rd_value = 1
        register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def sltu(rd, rs1, rs2):
    global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][2:])
    if rs1_value < rs2_value:
        rd_value = 1
    register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:0]) + 4)

def xor(rd, rs1, rs2):
    global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][2:])
    
    if (rs1_value == 0 and rs2_value == 0) or (rs1_value == 1 and rs2_value == 1):
        rd_value = 0
    else:
        rd_value = 1
    
    register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def srl(rd, rs1, rs2):
    global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][2:])
    rd_value = rs1_value >> rs2_value
    register_values[rd] =  '0b' + decimal_sign_ext(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def or_func(rd, rs1, rs2):
    global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][2:])
    rd_value = rs1_value | rs2_value
    register_values[rd] = '0b' + decimal_unsigned(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def and_func(rd, rs1, rs2):
    global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][2:])
    rd_value = rs1_value & rs2_value
    register_values[rd] = '0b' + decimal_unsigned(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def R(i):
    global PC
    
    funct3 = i[17:20]
    funct7 = i[:7]
    rs2 = dict_registers[i[7:12]]
    rs1 = dict_registers[i[12:17]]
    rd = dict_registers[i[20:25]]

    if funct7 == '0100000':
        sub(rd, rs1, rs2)

    elif funct3 == '000':
        add(rd, rs1, rs2)
    
    elif funct3 == '001':
        sll(rd, rs1, rs2)

    elif funct3 == '010':
        slt(rd, rs1, rs2)

    elif funct3 == '011':
        sltu(rd, rs1, rs2)
    
    elif funct3 == '100':
        xor(rd, rs1, rs2)
        
    elif funct3 == '101':
        srl(rd, rs1, rs2)

    elif funct3 == '110':
        or_func(rd, rs1, rs2)

    elif funct3 == '111':
        and_func(rd, rs1, rs2)


# Do S Type, B, Type, I Type, J Type : Harshul and Prabhav

'''
START HERE
'''

# I type

def addi(binary, rd, rs):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs][2:])
    imm_value = sign_ext_decimal(binary)
    rd_value = rs1_value + imm_value
    register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def sltiu(rs, imm, rd):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs][2:])
    imm_value = sign_ext_decimal(imm)
    if rs1_value < imm_value:
        rd_value = 1
    else:
        rd_value = 0
    register_values[rd] = '0b' + decimal_sign_ext(rd_value)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)
    
def jalr(rd, rs, imm):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs][2:])
    imm_value = sign_ext_decimal(imm)
    # register_values[rd] = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)
    PC = ('0b' + decimal_unsigned(rs1_value + imm_value))[:-1]  + '0'
    
def lw(rd, rs, imm):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs][2:])
    imm_value = sign_ext_decimal(imm)
    address = rs1_value + imm_value
    register_values[rd] = memory_values[decimal_hexa(address)]
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)
    
def I(i):
    #global PC
    imm = i[:12]
    rs = dict_registers[i[12:17]]
    funct3 = i[17:20]
    rd = dict_registers[i[20:25]]
    
    if i[-7:] == '0000011':
        lw(rd, rs, imm)
    elif i[-7:] == '1100111':
        jalr(rd, rs, imm)
    elif i[-7:] == '0010011':
        if funct3 == '000':
            addi(imm, rd, rs)
        else:
            sltiu(rs, imm, rd)

# B type

def beq(rs1, rs2, imm):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs1][2:])
    rs2_value = sign_ext_decimal(register_values[rs2][2:])
    imm_value = sign_ext_decimal(imm)
    if rs1_value == rs2_value:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + imm_value)
    else:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def bne(rs1, rs2, imm):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs1][2:])
    rs2_value = sign_ext_decimal(register_values[rs2][2:])
    imm_value = sign_ext_decimal(imm)
    if rs1_value != rs2_value:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + imm_value)
    else:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)
        
def blt(rs1, rs2, imm):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs1][2:])
    rs2_value = sign_ext_decimal(register_values[rs2][2:])
    imm_value = sign_ext_decimal(imm)
    if rs1_value < rs2_value:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + imm_value)
    else:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def bge(rs1, rs2, imm):
    #global PC
    rs1_value = sign_ext_decimal(register_values[rs1][2:])
    rs2_value = sign_ext_decimal(register_values[rs2][2:])
    imm_value = sign_ext_decimal(imm)
    if rs1_value >= rs2_value:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + imm_value)
    else:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)

def bltu(rs1, rs2, imm):
    #global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][2:])
    imm_value = sign_ext_decimal(imm)
    if rs1_value < rs2_value:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + imm_value)
    else:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)
    
def bgeu(rs1, rs2, imm):
    #global PC
    rs1_value = unsigned_decimal(register_values[rs1][2:])
    rs2_value = unsigned_decimal(register_values[rs2][2:])
    imm_value = sign_ext_decimal(imm)
    if rs1_value >= rs2_value:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + imm_value)
    else:
        PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)
        
def B(i):
    #global PC
    imm = i[0]+i[24]+i[1:7]+i[20:24]+'0'
    rs2 = dict_registers[i[7:12]]
    rs1 = dict_registers[i[12:17]]
    funct3 = i[17:20]
    
    if funct3 == '000':
        beq(rs1, rs2, imm)
    elif funct3 == '001':
        bne(rs1, rs2, imm)
    elif funct3 == '100':
        blt(rs1, rs2, imm)
    elif funct3 == '101':
        bge(rs1, rs2, imm)
    elif funct3 == '110':
        bltu(rs1, rs2, imm)
    elif funct3 == '111':
        bgeu(rs1, rs2, imm)
# S type
def S(i):
    #global PC
    # funct3 = i[17:20]
    rs2 = dict_registers[i[7:12]]
    rs1 = dict_registers[i[12:17]]
    imm = i[:7] + i[20:25]
    imm = sign_ext_decimal(imm)
    val = unsigned_decimal(register_values[rs1][2:])
   
    mem = val + imm
    memory = decimal_hexa(mem)
    memory_values[memory] = register_values[rs2]
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + 4)
# J type
def J(i):
    #global PC
    rd = dict_registers[i[20:25]]
    imm = i[0] + i[12:20] + i[11] + i[1:11] + '0'
    register_values[rd] = '0b' + decimal_sign_ext(unsigned_decimal(PC[2:]) + 4)
    PC = '0b' + decimal_unsigned(unsigned_decimal(PC[2:]) + sign_ext_decimal(imm))

'''
END HERE
'''


# Body
register_values = {
    'zero':'0b00000000000000000000000000000000', 'ra':'0b00000000000000000000000000000000', 'sp':'0b00000000000000000000000100000000',
    'gp':'0b00000000000000000000000000000000', 'tp':'0b00000000000000000000000000000000', 't0':'0b00000000000000000000000000000000', 
    't1':'0b00000000000000000000000000000000', 't2':'0b00000000000000000000000000000000', 's0':'0b00000000000000000000000000000000', 
    's1':'0b00000000000000000000000000000000', 'a0':'0b00000000000000000000000000000000', 'a1':'0b00000000000000000000000000000000', 
    'a2':'0b00000000000000000000000000000000', 'a3':'0b00000000000000000000000000000000', 'a4':'0b00000000000000000000000000000000', 
    'a5':'0b00000000000000000000000000000000', 'a6':'0b00000000000000000000000000000000', 'a7':'0b00000000000000000000000000000000', 
    's2':'0b00000000000000000000000000000000', 's3':'0b00000000000000000000000000000000', 's4':'0b00000000000000000000000000000000', 
    's5':'0b00000000000000000000000000000000', 's6':'0b00000000000000000000000000000000', 's7':'0b00000000000000000000000000000000', 
    's8':'0b00000000000000000000000000000000', 's9':'0b00000000000000000000000000000000', 's10':'0b00000000000000000000000000000000', 
    's11':'0b00000000000000000000000000000000', 't3':'0b00000000000000000000000000000000', 't4':'0b00000000000000000000000000000000', 
    't5':'0b00000000000000000000000000000000', 't6':'0b00000000000000000000000000000000'
}
memory_values = {
    '0x00010000': '0b00000000000000000000000000000000', '0x00010004': '0b00000000000000000000000000000000', 
    '0x00010008': '0b00000000000000000000000000000000', '0x0001000c': '0b00000000000000000000000000000000', 
    '0x00010010': '0b00000000000000000000000000000000', '0x00010014': '0b00000000000000000000000000000000', 
    '0x00010018': '0b00000000000000000000000000000000', '0x0001001c': '0b00000000000000000000000000000000',
    '0x00010020': '0b00000000000000000000000000000000', '0x00010024': '0b00000000000000000000000000000000', 
    '0x00010028': '0b00000000000000000000000000000000', '0x0001002c': '0b00000000000000000000000000000000', 
    '0x00010030': '0b00000000000000000000000000000000', '0x00010034': '0b00000000000000000000000000000000', 
    '0x00010038': '0b00000000000000000000000000000000', '0x0001003c': '0b00000000000000000000000000000000',
    '0x00010040': '0b00000000000000000000000000000000', '0x00010044': '0b00000000000000000000000000000000', 
    '0x00010048': '0b00000000000000000000000000000000', '0x0001004c': '0b00000000000000000000000000000000', 
    '0x00010050': '0b00000000000000000000000000000000', '0x00010054': '0b00000000000000000000000000000000', 
    '0x00010058': '0b00000000000000000000000000000000', '0x0001005c': '0b00000000000000000000000000000000',
    '0x00010060': '0b00000000000000000000000000000000', '0x00010064': '0b00000000000000000000000000000000', 
    '0x00010068': '0b00000000000000000000000000000000', '0x0001006c': '0b00000000000000000000000000000000', 
    '0x00010070': '0b00000000000000000000000000000000', '0x00010074': '0b00000000000000000000000000000000', 
    '0x00010078': '0b00000000000000000000000000000000', '0x0001007c': '0b00000000000000000000000000000000'
}

dict_registers = {
    '00000':'zero', '00001':'ra', '00010':'sp', '00011':'gp', '00100':'tp', '00101':'t0', '00110':'t1', '00111':'t2', '01000':'s0', 
    '01001':'s1', '01010':'a0', '01011':'a1', '01100':'a2', '01101':'a3', '01110':'a4', '01111':'a5', '10000':'a6', '10001':'a7', 
    '10010':'s2', '10011':'s3', '10100':'s4', '10101':'s5', '10110':'s6', '10111':'s7', '11000':'s8', '11000':'s9', '11010':'s10', 
    '11011':'s11', '11100':'t3', '11101':'t4', '11110':'t5', '11111':'t6'
}

B_OPCODE = '1100011'
J_OPCODE = '1101111'
R_OPCODE = '0110011'
S_OPCODE = '0100011'
I_OPCODE = {'0000011': 'lw', '0010011': 'addi', '0010011': 'sltiu', '1100111': 'jalr'}

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as f:
    input_lines = f.readlines()

halt = "0"*25 + "1100011"




output = []

a=((unsigned_decimal(PC[2:])//4))
data = input_lines[a]
if data != halt:
    data = data[:-1]
b=len(input_lines)

while (data != halt): 

    if data[-7:] == R_OPCODE:
        R(data)
    elif  data[-7:] == B_OPCODE:
        B(data)
    elif data[-7:] == S_OPCODE:
        S(data)
    elif data[-7:] in I_OPCODE.keys():
        I(data)
    elif data[-7:] == J_OPCODE:
        J(data)

# 
    a=((unsigned_decimal(PC[2:])//4))
    data = input_lines[a]
    if data != halt:
        data = data[:-1]
    
output_element = PC
for reg in register_values.keys():
    output_element += ' ' + register_values[reg]
output.append(output_element)

with open(output_file, 'w') as f:

    for i in range(len(output)):
        f.write(output[i])
        f.write(' \n')

    for keys, values in memory_values.items():
        f.write(keys + ':' + values + '\n')