from functools import partial
import sys

from user import User

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import pyqtgraph as pg


class GUIManager(QWidget):
    '''Main GUI'''

    def __init__(self, app, user=None):
        '''Initialize'''
        super().__init__()
        self.user = user
        self.main_menu = MainMenu(self, self.user)
        self.app = app
        self.active_window = self.main_menu
        self.active_window.show()
        sys.exit(self.app.exec())


class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self, master, user):
        '''Initialize'''
        super().__init__()
        self.master = master
        self.user = user
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
        self.user_layout = UserLayout(self)
        self.show()

    def check_user_status(self):
        if self.user == None:
            self.new_user_layout()
        else:
            self.existing_user_layout()

    def new_user_layout(self):
        new_user_layout = NewUserLayout(self)
        self.change_layout(new_user_layout)

    def existing_user_layout(self):
        existing_user_layout = UserLayout(self)
        self.change_layout(existing_user_layout)

    def change_layout(self, layout):
        self.setLayout(layout)


class UserLayout(QLayout):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        # Initializes the layouts with a master layout
        self.layout = QHBoxLayout(self.parent)
        self.layout_left = QVBoxLayout()
        self.layout_center = QGridLayout()
        self.layout_right = QVBoxLayout()
        # Initializes widgets to display user metrics
        self.user_name = QLineEdit(self.parent)
        self.user_weight = QLineEdit(self.parent)
        self.user_height = QLineEdit(self.parent)
        # Initializes a tree for displaying all user's weight history and buttons for editing DB
        self.user_history = QTreeWidget(self.parent)
        self.add_entry = QPushButton()
        self.modify_entry = QPushButton()
        self.delete_entry = QPushButton()
        # Initializes the graph for visualizing weight history with buttons for modifying display
        self.user_history_graph = pg.PlotWidget()
        # Sets the properties for all widgets and their layouts
        self.set_widget_properties()
        self.generate_layout()

    def user_name_properties(self):
        self.user_name.setReadOnly(True)

    def user_weight_properties(self):
        self.user_weight.setReadOnly(True)

    def user_height_properties(self):
        self.user_height.setReadOnly(True)

    def user_history_properties(self):
        label_list = ['Date', 'Weight']
        self.user_history.setHeaderLabels(label_list)

    def add_entry_button(self):
        pass

    def modify_entry_button(self):
        pass

    def delete_entry_button(self):
        pass

    def user_graph_properties(self):
        pass

    def set_widget_properties(self):
        self.user_name_properties()
        self.user_weight_properties()
        self.user_height_properties()
        self.user_graph_properties()
        self.user_history_properties()

    def generate_left_layout(self):
        self.layout_left.addWidget(self.user_name)
        self.layout_left.addWidget(self.user_weight)
        self.layout_left.addWidget(self.user_height)

    def generate_center_layout(self):
        self.layout_center.addWidget(self.user_history, 0, 0, 4, 4)
        self.layout_center.addWidget(self.add_entry, 5, 0, 1, 1)
        self.layout_center.addWidget(self.modify_entry, 5, 1, 1, 1)
        self.layout_center.addWidget(self.delete_entry, 5, 2, 1, 1)

    def generate_right_layout(self):
        self.layout_right.addWidget(self.user_history_graph)

    def generate_master_layout(self):
        self.layout.addLayout(self.layout_left, 1)
        self.layout.addLayout(self.layout_center, 1)
        self.layout.addLayout(self.layout_right, 1)

    def generate_layout(self):
        self.generate_left_layout()
        self.generate_center_layout()
        self.generate_right_layout()
        self.generate_master_layout()

class NewUserLayout(QLayout):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.user = User()
        self.layout = QGridLayout(self.parent)
        self.name = QLineEdit(self.parent)
        self.weight = QLineEdit(self.parent)
        self.height = QLineEdit(self.parent)
        self.confirm = QPushButton('Confirm', self.parent)
        self.cancel = QPushButton('Cancel', self.parent)
        self.set_widget_properties()
        self.generate_layout()

    def name_properties(self):
        self.name.setPlaceholderText('Name')
        self.name.editingFinished.connect(partial(self.user_setup, name=self.name))

    def weight_properties(self):
        self.weight.setPlaceholderText('Current Weight')
        validator = QDoubleValidator(0, 2000, 2, self.weight)
        self.weight.setValidator(validator)
        self.weight.editingFinished.connect(partial(self.user_setup, weight=self.weight))

    def height_properties(self):
        self.height.setPlaceholderText('Height')
        validator = QDoubleValidator(0, 110, 2, self.height)
        self.height.setValidator(validator)
        self.height.editingFinished.connect(partial(self.user_setup, height=self.height))

    def confirm_properties(self):
        self.confirm.setFixedHeight(35)
        self.confirm.clicked.connect(partial(self.confirm_transition))

    def cancel_properties(self):
        self.cancel.setFixedHeight(35)
        self.cancel.clicked.connect(self.cancel_transition)

    def confirm_transition(self):
        self.master.set_active_window(self.master.main_menu)

    def cancel_transition(self):
        self.master.set_active_window(self.master.user_selection_menu)

    def set_widget_properties(self):
        self.name_properties()
        self.weight_properties()
        self.height_properties()
        self.confirm_properties()
        self.cancel_properties()

    def generate_layout(self):
        self.layout.addWidget(self.name, 1, 0)
        self.layout.addWidget(self.weight, 2, 0)
        self.layout.addWidget(self.height, 3, 0)
        self.layout.addWidget(self.confirm, 4, 0, Qt.Alignment.AlignRight)
        self.layout.addWidget(self.cancel, 4, 1, Qt.Alignment.AlignRight)
