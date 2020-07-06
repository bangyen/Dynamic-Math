from .dynamath import *


class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.dyna_math = DynaMathManager(self)

        self.setWindowTitle("DynaMath Addon")
        self.setMinimumSize(500, 500)

        self.text_editor = QTextEdit()
        self.output_text = QTextEdit()
        self.saved_texts = ['', '', '', '']
        self.menu_triggered = 1

        # menu_triggered | 0 = graphic text ; 1 = question text ; 2 = answer text ; 3 = algorithm text

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
        action_editQuestionText = QAction("Edit Question Text", self)
        action_editQuestionText.triggered.connect(lambda checked: self.switchMenu(1))
        action_editAnswerText = QAction("Edit Question Text", self)
        action_editAnswerText.triggered.connect(lambda checked: self.switchMenu(2))
        action_editAlgorithm = QAction("Edit Algorithm", self)
        action_editAlgorithm.triggered.connect(lambda checked: self.switchMenu(3))
        action_showPreview = QAction("Show Preview", self)
        action_showPreview.triggered.connect(self.showPreview)

        toolbar_bottom = QToolBar()
        toolbar_bottom.addAction(action_showGraphicText)
        toolbar_bottom.addAction(action_editQuestionText)
        toolbar_bottom.addAction(action_editAnswerText)
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
    # Execute
    #
    def showPreview(self):
        self.saved_texts[self.menu_triggered] = self.text_editor.toPlainText()

        question = self.saved_texts[1]
        answer = self.saved_texts[2]
        algorithm = self.saved_texts[3]
        self.dyna_math.showPreview(question, answer, algorithm)
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
    # GUI FUNCTIONS
    #
    # menu_triggered | 0 = graphic text ; 1 = question text ; 2 = answer text ; 3 = algorithm text
    def switchMenu(self, menu_num):
        # saves current text in the correct location
        currentMenu = self.menu_triggered
        self.saved_texts[currentMenu] = self.text_editor.toPlainText()
        # sets text box to desired cached text
        self.text_editor.setText(self.saved_texts[menu_num])
        self.menu_triggered = menu_num

    def makeBold(self):
        action_called = self.sender()
        font = action_called.font()
        font.setBold(True)
        action_called.setFont(font)

    # function that's called when closed by dialog manager (found in qt/aqt/__init__.py) (REQUIRED BY ANKI)
    def closeWithCallback(self, *args):
        dialogs.markClosed("testD")


# About QDialog | https://doc.qt.io/qtforpython/PySide2/QtWidgets/QDialog.html#more
def main_func():
    d = QDialog()
    name = "testD"
    dialogs.register_dialog(name, CustomDialog)
    dialogs.open(name, mw)


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(main_func)
# and add it to the tools menu
mw.form.menuTools.addAction(action)





