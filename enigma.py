from encoder import Encoder
from rotors import Rotor
from plugboard import Plugboard
from reflector import Reflector

class EnigmaMachine(Encoder):

    def __init__(self, *configs):
        self.plugboard = Plugboard(configs[-1])

        self.rotors = []  # initially no rotors
        for rotor_path in configs[:-1]:
            self.rotors.append(Rotor(rotor_path))

        self.reflector = Reflector(13)

    # DEBUGGING
    def print_rotors(self):
        rotor_num = 1
        for rotor in self.rotors:
            print "Rotor" + str(rotor_num) + " encode:\t" + str(self.rotors[rotor_num-1].config_encode)
            print "Rotor" + str(rotor_num) + " decode:\t" + str(self.rotors[rotor_num-1].config_decode)
            rotor_num += 1
        print ""
    # DEBUGGING

    def encode(self, input):
        input = ord(input) - ord('A')  # A -> 0, ..., Z -> 25
        output = self.plugboard.encode(input)
        print "After plugboard:\t", output, chr(output+ord('A'))
        output = self.pass_rotors('encode', output)
        print "After rotors:\t\t", output, chr(output+ord('A'))
        output = self.reflector.encode(output)
        print "After reflector:\t", output, chr(output+ord('A'))
        output = self.pass_rotors('decode', output)
        print "After rotors:\t\t", output, chr(output+ord('A'))
        output = self.plugboard.decode(output)
        print "After plugboard:\t", output, chr(output+ord('A'))

        if len(self.rotors) > 0:  # check for rotors
            print "\t\t", range(26)
            self.print_rotors()
            print "ROTATE!"
            print ""
            self.rotate_rotors(0)  # rotate necessary rotors
            self.print_rotors()

        return chr(output + ord('A'))

    def encode_message(self, message):
        encoded_message = ''
        for letter in message:
            encoded_message += self.encode(letter)
        return encoded_message

    def decode(self, output):
        return self.encode(output)  # symmetric operation

    def rotate_rotors(self, rotor_i):
        if self.rotors[rotor_i].rotate():
            rotor_i += 1
            if rotor_i < len(self.rotors):
                self.rotate_rotors(rotor_i)

    def pass_rotors(self, transformer, input):
        direc = -1 if transformer == 'decode' else 1
        for rotor_num, rotor in enumerate(self.rotors[::direc]):
            # get output of current rotor
            if transformer == 'encode':
                input = rotor.encode(input)
            else:  # decode
                input = rotor.decode(input) 
        return input










