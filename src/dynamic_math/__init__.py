# import the main window object (mw) from aqt
from aqt import *
from aqt import gui_hooks
from aqt import utils
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from abc import ABC, abstractmethod
from numbers import *
from random import *
from anki.notes import *
from ctypes import *
import json
import pathlib
import time

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

    def varString(self, args):
        ret_str = "name: " + self.name
        ret_str += " type: " + type(self.math_obj).__name__
        ret_str += " args: "
        for arg in args:
            ret_str += arg + ", "
        return ret_str


class MankiCard():

    def __init__(self, name):
        self.name = name
        self.rawText = ""
        self.algoText = ""


class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Manki Addon")
        self.setMinimumSize(500, 500)

        self.text_editor = QTextEdit()
        self.output_text = QTextEdit()
        self.save_algoText = ""
        self.save_plainText = ""
        self.menu_triggered = 2
        self.variables = [] # TODO change into map?
        self.temp_variables = {}
        self.supportedOperations = ['+', '-', '*', '/', '(', ')', '^']
        self.supportedFunctions = ["der","int"]
        # menu_triggered | 1 = graphic text ; 2 = plain text ; 3 = algorithm text ; 4 = preview

        # TOP TOOLBAR
        action_create = QAction("Create new algorithm", self)
        action_create.triggered.connect(self.makeBold)
        action_edit = QAction("Edit existing algorithm", self)
        action_help = QAction("Help", self)

        toolbar = QToolBar()
        toolbar.addAction(action_create)
        toolbar.addAction(action_edit)
        toolbar.addAction(action_help)

        # BOTTOM TOOLBAR
        action_showGraphicText = QAction("Show Graphic Text", self)
        self.action_showPlainText = QAction("Show Plain Text", self)
        self.action_showPlainText.triggered.connect(self.showPlainText)
        action_editAlgorithm = QAction("Edit Algorithm", self)
        action_editAlgorithm.triggered.connect(self.showEditAlgorithm)
        action_showPreview = QAction("Show Preview", self)
        action_showPreview.triggered.connect(self.showPreview)

        toolbar_bottom = QToolBar()
        toolbar_bottom.addAction(action_showGraphicText)
        toolbar_bottom.addAction(self.action_showPlainText)
        toolbar_bottom.addAction(action_editAlgorithm)
        toolbar_bottom.addAction(action_showPreview)

        self.layout = QVBoxLayout()
        self.layout.addWidget(toolbar)
        self.layout.addWidget(self.text_editor)
        self.layout.addWidget(self.output_text)
        self.layout.addWidget(toolbar_bottom)

        self.setLayout(self.layout)
        self.show()
        # action_showPlainText.setFont(
        # FONTS

    #
    # RAW TEXT HELPER FUNCTIONS
    #

    def parseVarStr(self, str):
        params = []

        start = str.find('(')
        end = str.find(')')

        if str[1:start] == "Var":
            tmp_str = str[start + 1:end]
            comma_ind = tmp_str.find(',')
            while comma_ind != -1:
                params.append(tmp_str[:comma_ind])
                tmp_str = tmp_str[comma_ind + 1:]
                comma_ind = tmp_str.find(',')
            # account for the last arg
            params.append(tmp_str)
        else:
            showInfo("another type")
        return params

    def findVariable(self, x):
        for obj in self.variables:
            if obj.name == x:
                return obj
        return None

    #
    # OUTPUT "CONSOLE" HELPER FUNCTIONS
    #

    def setOutput(self, text):
        self.output_text.setText(text)

    def print(self, text):
        prevText = self.output_text.toPlainText()
        self.output_text.setText(prevText + text + "\n")

    def printArr(self, arr):
        for i in arr:
            self.print(str(i))

    #
    # ALGORITHM LOGIC FUNCTIONS
    #

    def Der(self, x, param1, param2):
        self.print("Received params: " + param1 + ', ' + param2)
        return 100

    #
    # ALGORITHM HELPER FUNCTIONS
    #

    def prec(self, c):
        if c == '+' or c == '-':
            return 1
        elif c == '*' or c == '/':
            return 2
        elif c == '^':
            return 3
        elif c == '(' or c == ')':
            return 4
        return -1

    def handleOperation(self, values, val2, val1, c):
        if c == '+':
            values.append(val2 + val1)
        elif c == '-':
            values.append(val2 - val1)
        elif c == '*':
            values.append(val2 * val1)
        elif c == '/':
            values.append(val2 / val1)
        elif c == '^':
            values.append(val2 ** val1)

    def processLogic(self, text):
        # TODO : functions,
        operators = []
        values = []
        # first search for known keywords for FUNCTIONS
        # if found, then run those functions and replace the function call in text with the output string
        # if not then treat everything else as values and operators as it should be
        words = text.split(" ")

        # remove white space from beginning and end
        for i in words:
            if i == ' ' or len(i) == 0:
                words.pop(words.index(i))

        for i in words:  # iterate through the logic line, word by word
            if i in self.supportedOperations:  # is it an operator?
                # Can you do an operation?
                if len(operators) != 0 and i != '(':
                    op = operators[-1]  # operation to be done

                    if i == ')' and op == '(':
                        operators.pop()
                    elif self.prec(op) >= self.prec(i) and op != '(' or i == ')':  # how about ( x )
                        val1 = values.pop()
                        val2 = values.pop()

                        self.handleOperation(values, val2, val1, op)

                        operators.pop()
                        if i == ')':
                            self.print("Should be (: " + str(operators.pop()))  # should be opening parenthesis
                if i != ')':
                    operators.append(i)
            else:  # not an operator. it's a value
                value = 0
                var = self.findVariable(i)
                if var is not None:
                    value = var.value
                elif self.temp_variables.get(i) is not None:
                    value = self.temp_variables[i]
                else:
                    value = float(i)
                values.append(value)

        # Handle the remaining operations
        while len(operators) > 0:
            op = operators[-1]
            val1 = values.pop()  # get values to do operation on
            val2 = values.pop()

            self.handleOperation(values, val2, val1, op)

            operators.pop()  # operation is done

        if len(values) != 1 or len(operators) != 0:
            self.print("Error: len(values) = "+str(len(values)) + " OR len(operators) = " + str(len(operators)))
            raise Exception

        return values[0]

    def runFunctionInLogic(self, name, params):
        if not name in self.supportedFunctions:
            self.print(name + " is not supported (yet).")
            raise Exception
        elif name == "der":
            return self.Der(*params)
        elif name == "int":
            return

    def unpackFunctionList(self, text):
        toBeRemoved = ['[', ']', "'", '"', ' ']
        params = text.split(',')
        self.print("Params (before): " + str(params))
        new_params = []
        for p in params:
            new_param = ''
            for char in p:
                if char in toBeRemoved:
                    p = p.replace(char, '')
            new_param = p
            new_params.append(new_param)

        self.print("Params (after): " + str(new_params))
        return new_params

    def processLogic_v2(self, logic_tokens):
        # Stacks (as lists) for evaluating the POST-FIX notation
        operators = []
        values = []

        for item in logic_tokens:
            # Remember the tokens are tuples : (value,type)
            value = item[0]  # value is either an operation, value, or function

            if value in self.supportedOperations:  # OPERATION

                if len(operators) != 0 and value != '(':
                    op = operators[-1]  # top of operators

                    if value == ')' and op == '(':  # handles ( x )
                        operators.pop()  # popped '('
                    elif self.prec(op) >= self.prec(value) and op != '(' or value == ')':
                        val1 = values.pop()
                        val2 = values.pop()
                        self.handleOperation(values, val2, val1, op)
                        operators.pop()

                        if value == ')':
                            self.print("Should be '(': " + str(operators.pop()))  # should be opening parenthesis
                if value != ')':
                    operators.append(value)

            else:  # VALUE OR FUNCTION
                if item[1] == 'func':
                    # Remember, item[0] is a string rep of list with entries as [name, <params> , param_num]
                    ftn = self.unpackFunctionList(item[0])
                    ftn_name = ftn[0]
                    self.print(ftn_name)
                    value = self.runFunctionInLogic(ftn_name, ftn[1:len(ftn)-1])

                var = self.findVariable(value)
                if var is not None:  # is the value an existing variable?
                    new_value = var.value
                elif self.temp_variables.get(value) is not None:  # is the value a temporary variable?
                    new_value = self.temp_variables[value]
                else:  # value must be a number or it's undefined
                    if item[1] == 'str':
                        self.print("ERROR: " + str(value) + " is undefined.")
                        raise Exception
                    new_value = float(value)

                values.append(new_value)

        # Handle the remaining operations
        while len(operators) > 0:
            op = operators[-1]
            val1 = values.pop()  # get values to do operation on
            val2 = values.pop()
            self.handleOperation(values, val2, val1, op)

            operators.pop()  # operation is done

        if len(values) != 1 or len(operators) != 0:
            self.print("Error: len(values) = " + str(len(values)) + " OR len(operators) = " + str(len(operators)))
            raise Exception

        return values[0]

    #
    # MAIN PARSING FUNCTIONS
    #
    def tokenizeAlgorithm(self, text):
        # types: char, num, operator
        tokens = []
        operators = [40, 41, 42, 43, 44, 45, 47, 61, 94]
        # classify each non whitespace character
        for char in text:
            ascii = ord(char)
            if 65 <= ascii <= 90 or 97 <= ascii <= 122:
                # letter
                tokens.append((char, "char"))
            elif 48 <= ascii <= 57:
                # number
                tokens.append((char, "num"))
            elif ascii in operators:
                # operator
                tokens.append((char, "op"))

        # self.print("Tokens: " + str(tokens))

        word = False
        number = False
        double = False
        func = False
        buffer = ""
        tokens_adv = []
        func_form = []
        param_num = 0
        # adding more context to the tokens.
        for token in tokens:
            if sum([word, number, double, func]) > 1:
                self.print("Multiple TRUE. Booleans = " + str([word, number, double, func]))
                raise Exception

            if token[1] == "char":
                if number is True:  # "Word" started with number -> INVALID
                    self.print("INVALID NAME - CAN'T START WITH A NUMBER")
                    raise Exception
                if func is True:  # Constructing Function Param
                    buffer += token[0]
                else:  # Start of a word
                    word = True
                    buffer += token[0]

            elif token[1] == "num":
                if word is True:  # Word + Num // part of a variable
                    buffer += token[0]
                elif double is True:  # Double + Num // adding to the double
                    buffer += token[0]
                elif number is True:  # Already Construct Num // adding to num
                    buffer += token[0]
                elif func is True:
                    buffer += token[0]
                else:  # Start to a number
                    number = True
                    buffer += token[0]

            elif token[1] == "op":
                # Special Cases
                if func is True and token[0] == ',':
                    func_form.append(buffer)
                    buffer = ''
                    param_num += 1
                elif func is True and token[0] == ')':  # Func -> ')' // end of function
                    func_form.append(buffer)  # last param
                    func_form.append(param_num+1)  # last entry = num of arg
                    tokens_adv.append((str(func_form), "func"))
                    func_form.clear()
                    param_num = 0
                    buffer = ''
                    func = False
                elif number and token[1] == '.':  # Number -> '.' // double
                    double = True
                    number = False
                # Normal Cases
                elif word is True:
                    if token[0] == '(':  # Word -> '(' // start to a function
                        func_form.append(buffer)  # func_form[0] = function name
                        buffer = ''
                        func = True
                        word = False
                    else:  # Word -> Operator
                        tokens_adv.append((buffer, "str"))
                        tokens_adv.append((token[0], "op"))
                        buffer = ''
                        word = False
                elif number is True:  # Number -> Operator
                    tokens_adv.append((buffer, "num"))
                    tokens_adv.append((token[0], "op"))
                    buffer = ''
                    number = False
                elif double is True:  # Double -> Operator
                    tokens_adv.append((buffer, "double"))
                    tokens_adv.append((token[0], "op"))
                    buffer = ''
                    double = False
                else:
                    tokens_adv.append((token[0], "op"))
        # handle extra
        if len(buffer) != 0:
            if word:
                tokens_adv.append((buffer, "str"))
            elif number:
                tokens_adv.append((buffer, "num"))
            elif double:
                tokens_adv.append((buffer, "double"))
            elif func:
                tokens_adv.append((buffer, "func"))
            else:
                self.print("handle extra type error. Buffer = " + buffer)
                raise Exception
        self.print(str(tokens_adv))
        return tokens_adv

    def parseAlgorithm(self, text):
        # generates random numbers for each variable that was created in parseRawText()
        # goes through the written function and generates an output.
        # types of input/output are: integer, double, integral, complex number, function, etc.

        # get every line of the code

        # while:
        # find '='
        # left side is output // right side is logic (post fix) OR right side is function

        # TODO: each line goes through lexer (in C) -> parser (in C) -> sends back output value and is assigned
        # TODO: in either variables or temp variables

        lines = text.splitlines()

        # Restricted to lines of the form: "var_name = <logic here>"
        for line in lines:
            processed_tokens = self.tokenizeAlgorithm(line)
            if processed_tokens[0][1] != "str":
                self.print("LHS not valid.")
                raise Exception
            elif processed_tokens[1][0] != '=':
                self.print("'=' is missing")
                raise Exception

            var_name = processed_tokens[0][0]
            logic = processed_tokens[2:]

            var = self.findVariable(var_name)
            if var is None:
                self.print("Temp Variable")
                self.temp_variables[var_name] = self.processLogic_v2(logic)
            else:
                self.print("Existing Variable")
                var.value = self.processLogic_v2(logic)
                # need to check if output is of correct type

        self.print("Temporary Variables: ")
        for key, val in self.temp_variables.items():
            self.print(key + ":" + str(val))
        self.print("Existing Variables: ")
        for var in self.variables:
            self.print(var.name + ":" + str(var.value))

        return

    def parseRawText(self, text):
        # parses raw text and saves any variables that are explicitly written along with what type of number it is.
        # converts raw text into text for a front of a card (without the values of the variables written)
        # variables are then used by the algorithm written by the user
        # possible notation to use: { Variable(x,Integer(1,50)) }
        i = 0
        special_data = []
        while i < len(text):
            if text[i] == '{':
                # find where the ending } is.
                for j in range(i, len(text)):
                    if text[j] == '}':
                        var_str = text[i:j + 1]
                        params = self.parseVarStr(var_str)
                        special_data.append((var_str, params[0]))
                        if len(params) == 1:  # then it may be an existing variable
                            if self.findVariable(params[0]) is not None:
                                i = j
                                break
                            else:
                                # showInfo("Variable does not exist: " + params[0])
                                break
                        self.variables.append(Variable(params[0], params[1], params[2:]))
                        i = j
                        break
            i += 1

        final_str = text
        for var in special_data:
            self.print(str(var[0]))

        for var in special_data:
            final_str = final_str.replace(var[0], var[1])
        self.print("Final string: " + final_str)
        return final_str

    def showPreview(self):
        self.variables = []
        content_text = ""
        algo_text = ""
        self.text_editor.setText("What is [$]{Var(x,Integer,1,10)} + {Var(y,Integer,11,100)} - 2{Var(x)}[/$]")

        if self.menu_triggered == 2:
            self.save_plainText = self.text_editor.toPlainText()
        elif self.menu_triggered == 3:
            self.save_algoText = self.text_editor.toPlainText()

        content_text = self.save_plainText
        # algo_text = self.save_algoText
        content_text = "What is [$]{Var(x,Integer,1,10)} + {Var(y,Integer,11,100)} - 2{Var(x)}[/$]"

        algo_text = "t = 4 + 9 \n " \
                    "F = der(x,p1,p2) + t"

        start = time.time()
        content_text = self.parseRawText(content_text)
        self.parseAlgorithm(algo_text)

        # TODO: should be export button or make card button

        self.addMathNote(content_text, algo_text)
        self.print("Process Time = " + str(time.time() - start))

        so_file = "C:/Scripts/testfile.so"
        my_functions = CDLL(so_file)

        self.print("C OUTPUT: " + str(my_functions.square(10)))

        # add to .json file

        # data should be split in Decks -> Notes
        data = {'front': content_text, 'back': algo_text}

        path = str(pathlib.Path(__file__).parent.absolute()) + "/data.txt"

        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def createTestModel(self, deck_name, model_name):
        models = mw.col.models  # Collection's Model Manager
        deck_id = mw.col.decks.id(deck_name)
        deck1 = mw.col.decks.get(deck_id)

        cur_model = models.new(model_name)

        # adding fields
        models.addField(cur_model, models.newField("question"))
        models.addField(cur_model, models.newField("answer"))

        # add template (NEEDED FOR CARD CREATION) P.S needs to go after the fields are created
        t = models.newTemplate("Normal")
        t['qfmt'] = "<p>{{question}}</p>"  # cannot be empty
        t['afmt'] = "<p>{{answer}}</p>"  # cannot be empty
        models.addTemplate(cur_model, t)  # adds template to cur_model

        models.add(cur_model)
        mw.col.models.save(cur_model)

        mw.col.decks.select(deck_id)
        mw.col.decks.current()['mid'] = cur_model['id']  # deck's model id is cur_model's id
        mw.col.decks.save(deck1)  # commit in the DB

        mw.col.models.setCurrent(cur_model)  # current model = cur_model
        models.current()['did'] = mw.col.decks.current()['id']  # cur_model's deck id is the deck's id
        mw.col.models.save(cur_model)  # commit in the DB
        return cur_model

    def addMathNote(self, front, back):
        # did = deck id, mid = model id, ... etc.

        deck_name = "testDeck"
        model_name = "TestModel2"

        deck_id = mw.col.decks.id(deck_name)

        models = mw.col.models  # Collection's Model Manager

        cur_model = models.byName(model_name)
        self.print(str(models.allNames()))
        todel= models.get(models.byName("TestModel"))['id']
        models.rem(todel)
        if cur_model is None:  # model not found? Then create it
            cur_model = self.createTestModel(deck_name, model_name)

        note = Note(mw.col, cur_model)  # returns Note using the currently selected model

        note.fields[0] = front
        note.fields[1] = back

        mw.col.decks.select(deck_id)  # selecting "testDeck"
        card_num = mw.col.addNote(note)  # mw.col adds note to currently selected deck

        self.print("Add Note Returned: " + str(card_num))

        mw.col.reset()  # reset DB for GUI to show
        mw.reset()

        self.print("Keys: " + str(note.keys()))
        self.print("Values: " + str(note.values()))
        self.print("Cards: " + str(note.cards()))
    #
    # GUI FUNCTIONS
    #

    def showPlainText(self):
        if self.menu_triggered != 2:
            self.save_algoText = self.text_editor.toPlainText()
            self.text_editor.setText(self.save_plainText)
            self.menu_triggered = 2

    def showEditAlgorithm(self):
        if self.menu_triggered != 3:
            self.save_plainText = self.text_editor.toPlainText()
            self.text_editor.setText(self.save_algoText)
            self.menu_triggered = 3

    def makeBold(self):
        action_called = self.sender()
        font = action_called.font()
        font.setBold(True)
        action_called.setFont(font)

    # function that's called when closed by dialog manager (found in qt/aqt/__init__.py) (REQUIRED BY ANKI)
    def closeWithCallback(self, *args):
        dialogs.markClosed("testD")


# About QDialog | https://doc.qt.io/qtforpython/PySide2/QtWidgets/QDialog.html#more
def testFunction():
    d = QDialog()
    name = "testD"
    dialogs.register_dialog(name, CustomDialog)
    dialogs.open(name, mw)


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)





