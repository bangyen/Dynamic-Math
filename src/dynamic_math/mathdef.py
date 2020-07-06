from abc import ABC, abstractmethod
from numbers import *
from random import *


def handle_math_object(math_obj):
    # return correct type with the correct params
    if math_obj == "Integer":
        return Integer()
    elif math_obj == "Real":
        return RealNumber()
    elif math_obj == "Rational":
        return RationalNumber()

class Variable:

    def __init__(self, name, math_obj, args):
        self.value = 0
        self.name = name
        self.math_obj = handle_math_object(math_obj)
        self.args = []
        self.str = self.varString(args)

        for i in range(0, len(args)):
            self.args.append(int(args[i]))

    def generateRandomValue(self):
        self.value = self.math_obj.generateRand(*self.args)

    def __add__(self, x):
        return self.value + x.value

    def __sub__(self, x):
        return self.value - x.value

    def __mul__(self, x):
        return self.value * x.value

    def __truediv__(self, x):
        return self.value / x.value

    def __pow__(self, x):
        return self.value ** x.value

    def __mod__(self, x):
        return self.value % x.value

    # for Debug
    def varString(self, args):
        ret_str = "name: " + self.name
        ret_str += " type: " + type(self.math_obj).__name__
        ret_str += " args: "
        for arg in args:
            ret_str += arg + ", "
        return ret_str

# Integer
class Integer(int):

    def __init__(self):
        super().__init__()

    def generateRand(self, a, b):
        return randint(a, b)


# Rational Numbers
class RationalNumber(Rational, ABC):

    def __init__(self):
        super().__init__()

    def generateRand(self, a, b, c, d):
        rand1 = randint(a, b)
        rand2 = randint(c, d)
        return Rational(rand1, rand2)


# Real Number
class RealNumber(Real, ABC):

    def __init__(self):
        super().__init__()

    def generateRand(self, a, b):
        return random() + randint(a, b)


# Complex Number # TODO

# Integral

# Derivative # TODO

# Function f(x) # TODO

# Matrix

# Vector

#
# ALGORITHM LOGIC FUNCTIONS
#

def Der(x, param1, param2):
    return 100