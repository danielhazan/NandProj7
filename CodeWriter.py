from Parser import *


class CodeWriter:
    def __init__(self):
        self.countJumps = 0
        self.parser = Parser
        self.call_index = 1

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
            return ["@R5\nD=A\n@" + str(ValueToPush) + "\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]

    def writePop(self, CodeSegment, OffsetIndexToStore, filename):
        """switch case according to the CodeSegment"""
        if CodeSegment == "local":
            return ["@" + str(
                OffsetIndexToStore) + "\nD=A\n@LCL\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "argument":
            return ["@" + str(
                OffsetIndexToStore) + "\nD=A\n@ARG\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "this":
            return ["@" + str(
                OffsetIndexToStore) + "\nD=A\n@THIS\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "that":
            return ["@" + str(
                OffsetIndexToStore) + "\nD=A\n@THAT\nA=M\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]
        elif CodeSegment == "pointer":
            if OffsetIndexToStore == '0':
                return ["@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"]
            else:
                return ["@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"]

        elif CodeSegment == "static":
            return ["@SP\nM=M-1\nA=M\nD=M\n@" + filename.split(".")[0] + "." + str(OffsetIndexToStore) + "\nM=D\n"]
        elif CodeSegment == "temp":
            return [
                "@" + str(OffsetIndexToStore) + "\nD=A\n@R5\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"]

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
        self.countJumps += 1  # every jump has to reffer to a deferent num of line in instruction, so by increment the countJump
        # field, we actually define differnt jump location for each vm Jump command
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n \
        @Jump" + str(self.countJumps) + "\nD;JEQ\n@SP\nA=M-1\nM=0\n@CONT" + str(self.countJumps) + "\n "
                                                                                                   "0;JMP\n(Jump" + str(
            self.countJumps) + ")\n@SP\nA=M-1\nM=-1\n(CONT" + str(self.countJumps) + ")\n"]

    def GTCommand(self):
        """if gt is set so we have to generate Jump command in assembly. if the Jump condition is true
        so set M register to be -1 , i.e true. otherwise, set M register to be 0, i.e false"""
        self.countJumps += 1  # every jump has to reffer to a deferent num of line in instruction, so by increment the countJump
        # field, we actually define differnt jump location for each vm Jump command
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D \n "
                "@Jump" + str(self.countJumps) + "\nD;JGT\n@SP\nA=M-1\nM=0\n@CONT" + str(self.countJumps) + "\n "
                                                                                                            "0;JMP\n(Jump" + str(
            self.countJumps) + ")\n@SP\nA=M-1\nM=-1\n(CONT" + str(self.countJumps) + ")\n"]

    def LTCommand(self):
        """if lt is set so we have to generate Jump command in assembly. if the Jump condition is true
        so set M register to be -1 , i.e true. otherwise, set M register to be 0, i.e false"""
        self.countJumps += 1  # every jump has to reffer to a deferent num of line in instruction, so by increment the countJump
        # field, we actually define differnt jump location for each vm Jump command
        return ["@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n "
                "@Jump" + str(self.countJumps) + "\nD;JLT\n@SP\nA=M-1\nM=0\n@CONT" + str(self.countJumps) + "\n "
                                                                                                            "0;JMP\n(Jump" + str(
            self.countJumps) + ")\n@SP\nA=M-1\nM=-1\n(CONT" + str(self.countJumps) + ")\n"]

    def writeInit(self):
        return ["@256\nD=A\n@SP\nM=D\n"] + self.writeCall("Sys.init")

    def writeLabel(self, label):
        return ["(" + str(label) + ")\n"]

    def writeGoto(self, label):
        return ["@" + str(label) + "\n0;JMP\n"]

    def writeIf(self, label):
        return ["@SP\nAM=M-1\nD=M\n@" + str(label) + "\nD;JNE\n"]

    def writeFunction(self, function_name, numVars):
        call_segment = self.writeLabel(function_name)
        for i in range(int(numVars)):
            call_segment += self.writePush('constant', 0, 'NULL')
        #call_segment += self.writeReturn()
        return call_segment


    def pushCodeSegments(self, CodeSegment):
        """this template pushes CodeSegments to the stack to save if for the caller function"""
        return ["@" + str(CodeSegment) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"]

    def writeCall(self, function_name, numArgs  = 0):
        """<-----SLIDE 8.6------>"""
        self.call_index += 1
        # first we push a return address using the label declared at the end of the call segment
        call_segment = self.writePush('constant', 'RETURNADRESS' + str(self.call_index), None)

        # now push the LCL , ARG, THIS, THAT to save it for the caller
        call_segment += self.pushCodeSegments('LCL')
        call_segment += self.pushCodeSegments('ARG')
        call_segment += self.pushCodeSegments('THIS')
        call_segment += self.pushCodeSegments('THAT')

        # now reposition the ARG to the location where the return value has to be poped latter
        # remember that ARG = SP -5 -numArgs
        ARG_DISTANCE = int(numArgs) + 5
        call_segment += ["@" + str(ARG_DISTANCE) + "\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n"]

        # now reposition LCL to point where the SP points at the beggining of the calee's segment

        call_segment += ["@SP\nD=M\n@LCL\nM=D\n"]

        # now transfering control to the callee function

        call_segment += self.writeGoto(function_name)
        call_segment += self.writeLabel('RETURNADRESS' + str(self.call_index))

        #call_segment += [
            #"@" + str(function_name) + "\n0;JMP\n(RETURN" + str(function_name) + str(self.call_index) + ")\n"]
        return call_segment

    def writeReturn(self):

        # first to get the return address of the caller function,  we have to instore the LCL
        # address in temporary variable (endFrame) and get the return address by retAddr = *(endFrame -5)

        # we use register R15 to temporarily restore the LCL address as shown on the slides
        call_segment = ["@LCL\nD=M\n@R15\nM=D\n@5\nD=D-A\nA=D\nD=M\n"]

        # now we restore the return Adress (retAddr)in register R14
        call_segment += ["@R14\nM=D\n"]

        # now reposiotion the return value to the ARG segment of the caller (*ARG = pop() ) and then
        # increment the pointer of SP by 1 (SP = ARG +1)
        call_segment += ["@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\nD=A\n@SP\nM=D+1\n"]

        # now we have to restore again the code segments THAT, THIS , ARG ,LCL to the caller and return to
        # retAddr (stored in R14)

        # THAT = *(R15 [endFrame] - 1) , THIS = *(R15[endFrame] -2 ) etc....
        call_segment += ["@R15\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n"]
        call_segment += ["@R15\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n"]
        call_segment += ["@R15\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n"]
        call_segment += ["@R15\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n"]

        # jump to the return address (i.e jump to the **address** which is stores into it)

        call_segment += ["@R14\nA=M\n0;JMP\n"]
        #call_segment += self.writeGoto('R14')
        return call_segment
