__author__ = 'cltanuki'
from gi.repository import Gtk


class HelpDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Help", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class LoginWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Login")

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.help_button = Gtk.Button(label="Help")
        self.help_button.connect("clicked", self.help_button_clicked)
        self.login_button = Gtk.Button(label="Login")
        self.login_button.connect("clicked", self.login_button_clicked)

        self.login_label = Gtk.Label("Login")
        self.passwd_label = Gtk.Label("Password")

        self.login = Gtk.Entry()
        self.passwd = Gtk.Entry()

        self.grid.add(self.login_label)
        self.grid.attach_next_to(self.passwd_label, self.login_label, Gtk.PositionType.BOTTOM, 1, 3)
        self.grid.attach_next_to(self.help_button, self.passwd_label, Gtk.PositionType.BOTTOM, 1, 3)
        self.grid.attach(self.login, 1, 0, 1, 3)
        self.grid.attach_next_to(self.passwd, self.login, Gtk.PositionType.BOTTOM, 2, 3)
        self.grid.attach_next_to(self.login_button, self.passwd, Gtk.PositionType.BOTTOM, 1, 2)

    def login_button_clicked(self, widget):
        print("Hello World")

    def help_button_clicked(self, widget):
        dialog = HelpDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            dialog.destroy()

win = LoginWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()