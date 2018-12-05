from Parser import *


class CodeWriter:
    def __init__(self):
        self.countJumps = 0
        self.parser = Parser


    def writePush(self, CodeSegment, ValueToPush, filename):
        """switch case according to the CodeSegment"""
        if CodeSegment == "constant":
            return ["@" + str(ValueToPush) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
        elif CodeSegment == "local":
            return ["@LCL\nD=M\n@" + str(ValueToPush) + "\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
        elif CodeSegment == "argument":
            return ["@ARG\nD=M\n@" + str(ValueToPush) + "\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
        elif CodeSegment == "this":
            return ["@THIS\nD=M\n@" + str(ValueToPush) + "\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
        elif CodeSegment == "that":
            return ["@THAT\nD=M\n@" + str(ValueToPush) + "\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
        elif CodeSegment == "pointer":
            if ValueToPush == '0':
                return ["@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
            else:
                return ["@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
        elif CodeSegment == "static":
            return ["@" + filename.split(".")[0] + "." + str(ValueToPush) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]
        elif CodeSegment == "temp":
            return ["@R5\nD=M\n@" + str(ValueToPush) + "\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]




    def writePop(self ,CodeSegment, OffsetIndexToStore,filename):
        """switch case according to the CodeSegment"""
        if CodeSegment == "local":
            return ["@" +str(OffsetIndexToStore)+"\nD=A\n@LCL\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "argument":
            return ["@" +str(OffsetIndexToStore)+"\nD=A\n@ARG\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "this":
            return ["@" +str(OffsetIndexToStore)+"\nD=A\n@THIS\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "that":
            return ["@" +str(OffsetIndexToStore)+"\nD=A\n@THAT\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "pointer":
            if OffsetIndexToStore == '0':
                return ["@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"]
            else:
                return ["@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"]

        elif CodeSegment == "static":
            return ["@SP\nM=M-1\nA=M\nD=M\n@" + filename.split(".")[0] + "." + str(OffsetIndexToStore) + "\nM=D\n"]
        elif CodeSegment == "temp":
            return ["@" + str(OffsetIndexToStore) + "\nD=A\n@R5\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]

    def writeArithmetic(self, CommandType):
        """switch case according to the CodeSegment"""
        if CommandType == "add":
            return self.AddCommand()
        elif CommandType == "neg":
            return self.NegCommand()
        if CommandType == "or":
            return self.OrCommand()
        if CommandType == "sub":
            return self.SubCommand()
        if CommandType == "eq":
            return self.EqualCommand()
        if CommandType == "gt":
            return self.GTCommand()
        if CommandType == "lt":
           return self.LTCommand()
        if CommandType == "and":
            return self.AndCommand()
        if CommandType == "not":
            return self.NotCommand()

    # complete pop and push methods

    """*******Arithmatic methods********"""
    def NegCommand(self):
        return ["@SP\nA=M-1\nM= -M\n"]

    def NotCommand(self):
        return ["@SP\nA=M-1\nM=!M\n"]

    def AddCommand(self):
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M + D\nM=D\n"]
    def AndCommand(self):
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M & D\nM=D\n"]

    def SubCommand(self):
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M - D\nM=D\n"]

    def OrCommand(self):
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M | D\nM=D\n"]

    def EqualCommand(self):
        """if eq is set so we have to generate Jump command in assembly. if the Jump condition is true
        so set M register to be -1 , i.e true. otherwise, set M register to be 0, i.e false"""
        self.countJumps +=  1  # every jump has to reffer to a deferent num of line in instruction, so by increment the countJump
        # field, we actually define differnt jump location for each vm Jump command
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n \
        @Jump" + str(self.countJumps) + "\nD;JEQ\n@SP\nA=M-1\nM=0\n@CONT" + str(self.countJumps) + "\n "
            "0;JMP\n(Jump" + str(self.countJumps) + ")\n@SP\nA=M-1\nM=-1\n(CONT" + str(self.countJumps) + ")\n"]

    def GTCommand(self):
        """if gt is set so we have to generate Jump command in assembly. if the Jump condition is true
        so set M register to be -1 , i.e true. otherwise, set M register to be 0, i.e false"""
        self.countJumps += 1  # every jump has to reffer to a deferent num of line in instruction, so by increment the countJump
        # field, we actually define differnt jump location for each vm Jump command
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D \n "
        "@Jump" + str(self.countJumps) + "\nD;JGT\n@SP\nA=M-1\nM=0\n@CONT" + str(self.countJumps) + "\n "
        "0;JMP\n(Jump" + str(self.countJumps) + ")\n@SP\nA=M-1\nM=-1\n(CONT" + str(self.countJumps) + ")\n"]

    def LTCommand(self):
        """if lt is set so we have to generate Jump command in assembly. if the Jump condition is true
        so set M register to be -1 , i.e true. otherwise, set M register to be 0, i.e false"""
        self.countJumps += 1  # every jump has to reffer to a deferent num of line in instruction, so by increment the countJump
        # field, we actually define differnt jump location for each vm Jump command
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n "
        "@Jump" + str(self.countJumps) + "\nD;JLT\n@SP\nA=M-1\nM=0\n@CONT" + str(self.countJumps) + "\n "
        "0;JMP\n(Jump" + str(self.countJumps) + ")\n@SP\nA=M-1\nM=-1\n(CONT" + str(self.countJumps) + ")\n"]
