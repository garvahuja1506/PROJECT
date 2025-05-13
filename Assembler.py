registers = {
    'zero': '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100',
    't0': '00101', 't1': '00110', 't2': '00111', 's0': '01000', 'fp': '01000',
    's1': '01001', 'a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101',
    'a4': '01110', 'a5': '01111', 'a6': '10000', 'a7': '10001', 's2': '10010',
    's3': '10011', 's4': '10100', 's5': '10101', 's6': '10110', 's7': '10111',
    's8': '11000', 's9': '11001', 's10': '11010', 's11': '11011', 't3': '11100',
    't4': '11101', 't5': '11110', 't6': '11111'
}

        # funct7, funct3, opcode
instructionR = {
    "add": ["0000000", "000", "0110011"], 
    "sub": ["0100000", "000", "0110011"],
    "sll": ["0000000", "001", "0110011"],
    "slt": ["0000000", "010", "0110011"],
    "srl": ["0000000", "101", "0110011"],
    "or":  ["0000000", "110", "0110011"],
    "and": ["0000000", "111", "0110011"],
    "xor": ["0000000", "100", "0110011"]
}

instructionI = {
    "lw": ["010", "0000011"],
    "jalr": ["000", "1100111"],
    "addi": ["000", "0010011"]
}

instructionS = {
    "sw": ["010", "0100011"]
}

instructionB = {
    "beq": ["000", "1100011"],
    "bne": ["001", "1100011"],
    "blt": ["100", "1100011"],
    "bge": ["101", "1100011"],
    "bltu": ["011", "1100011"]
}

instructionU = {
    "auipc": "0010111",
    "lui": "0110111"
}

instructionJ = {
    "jal": "1101111"
}

instructionbonus = {
    "mul": "0000001", "rst": "0000000", "halt": "1111111", "rvrs": "0000111"
}

label_dict = {}

# sign extension functions -->
def sign_ext_RISB(n):
    num=n&0xfff
    return format(num,'012b')

def sign_ext_J(n):
    num=n&0xfffff
    return format(num,'020b') 

def sign_ext_B(n):
    num=n&0x1fff
    return format(num,'013b')

def sign_ext_U(n):
    num=n&0xfffff
    return format(num,'020b')

# type instruction -->
def s_type(register):
    imm_part, reg_part = register[1].split('(')
    rs1 = reg_part[:-1]
    imm = sign_ext_RISB(int(imm_part))
    rs2 = registers[register[0]]
    rs1_code = registers[rs1]
    f3, op = instructionS['sw']
    imm_high = imm[:7]
    imm_low = imm[7:]
    return imm_high + rs2 + rs1_code + f3 + imm_low + op

def j_type(register):

    opcode= instructionJ['jal']
    try:
        z=sign_ext_J(int(register[1]))
    except:
        if register[1] in label_dict:
            if (list(label_dict.items())[0][0] == register[1]):
                z = sign_ext_J((label_dict[register[1]]-count+1)*4)
            else:
                z = sign_ext_J((label_dict[register[1]] - count) * 4)

    return (z[0]+z[10:20]+z[9]+z[1:9]+registers[register[0]]+opcode)

def r_type(register: list[str], instruction: str)->str:
    f3 = instructionR[instruction][1]
    f7 = instructionR[instruction][0]
    opcode = instructionR[instruction][2]
    rd, rs1, rs2 = [registers[x] for x in register]
    instr_32_bit = f7+rs2+rs1+f3+rd+opcode
    return instr_32_bit

def i_type(register: list[str], instruction: str)->str:
    f3, opcode = instructionI[instruction]
    if instruction == "lw":
        register[1], temp = register[1].split('(')
        z = sign_ext_RISB(int(register[1]))
        temp = temp[:-1]
        register.append(temp)
        rd, rs1 = registers[register[0]], registers[register[2]]
        imm = z
    else:
        rd, rs1 = registers[register[0]], registers[register[1]]
        imm = sign_ext_RISB(int(register[2]))
    instr_32_bit = imm + rs1 + f3 + rd + opcode
    return instr_32_bit

def b_type(register: list[str], instruction: str)->str:
    # beq rs1,rs2,imm
    f3, opcode = instructionB[instruction]
    rs1, rs2 = registers[register[0]], registers[register[1]]
    if register[2] not in label_dict:
        imm = sign_ext_B(int(register[2]))
        instruct_32_bit = imm[0] + imm[2:8] + rs2 + rs1 + f3 + imm[8:12] + imm[1] + opcode
    else:
        imm = sign_ext_B((int(label_dict[register[2]])-count)*4)
        instruct_32_bit = imm[0] + imm[2:8] + rs2 + rs1 + f3 + imm[8:12] + imm[1] + opcode

    return instruct_32_bit
def bonustype(register: list[str], instruction: str)->str:
    if instruction == "mul":
        rd, rs1, rs2 = [registers[x] for x in register]
        instruct_32_bit = "0"*7 + rs2 + rs1 + "0"*7 + rd + "0"*7
    elif instruction == "rvrs":
        rd, rs1 = [registers[x] for x in register]
        instruct_32_bit = "0"*12 + rs1 + "0"*3 + rd + "0"*7
    else:
        instruct_32_bit = "0"*32
    return instruct_32_bit

def main(filename):
    output = []
    file_name = filename
    with open(f"{filename}.txt", "r") as f:
        lines = f.readlines()

    global count
    count = 0
    for line in lines:
        if ':' in line:
            parts = line.split(':')
            label = parts[0].strip()
            remaining = parts[1].strip()
            label_dict[label] = count
            if remaining:
                count += 1
        else:
            if line:
                count += 1
    
    count = 0
    for line in lines:
        try:
            line = line.strip()
            particular_line = line.split()
            if ":" in particular_line[0]:
                label = particular_line[0][:particular_line[0].index(":")]
                if len(particular_line) > 1:
                    instruction = particular_line[1]
                else:
                    instruction = None

                if len(particular_line) > 2:
                    register = particular_line[2]
                    registerlist = register.split(",")
                else:
                    register = None

                label_dict[label] = count

            else:
                instruction = particular_line[0]

                if len(particular_line) > 1:
                    register = particular_line[1]
                    registerlist = register.split(',')
                else:
                    register = None
                count += 1
            if instruction == None or register == None:
                print(instruction)
                print(register)
                print("Error!!")
            elif instruction in instructionR:
                res = r_type(registerlist, instruction)
            elif instruction in instructionI:
                res = i_type(registerlist, instruction)
            elif instruction in instructionS:
                res = s_type(registerlist)
            elif instruction in instructionB:
                res = b_type(registerlist, instruction)
            elif instruction in instructionJ:
                res = j_type(registerlist)
            elif instruction in instructionbonus:
                res = bonustype(registerlist, instruction)

            else:
                res = "Error"
            print(res)
            output.append(res)
        except:
            print("Error")
            output.append("\n")

        with open("answer.txt", "w") as f:
            for item in output:
                f.write(item+"\n")


main("testcase")
