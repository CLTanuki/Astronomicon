__author__ = 'cltanuki'
import npyscreen
import pdb
from pony.orm import *
from models import db, Satellite


class AddressDatabase(object):
    def __init__(self, filename="example-addressbook.db"):
        db.generate_mapping(create_tables=True)

    @db_session
    def add_record(self, params):
        Satellite(**params)
        commit()
    #
    # @db_session
    # def update_record(self, record_id, params):
    #     Satellite[record_id]
    #     commit()

    @db_session
    def delete_record(self, record_id):
        Satellite[record_id].delete()
        commit()

    @db_session
    def list_all_records(self):
        satellites = select(s for s in Satellite)
        return(list(satellites))

    @db_session
    def get_record(self, record_id):
        return Satellite[record_id]


class SatelliteList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(SatelliteList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return(vl.title)

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('VIEW').satellite = act_on_this
        self.parent.parentApp.switchForm('VIEW')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITRECORDFM').value = None
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
        self.parent.update_list()


class SatelliteListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = SatelliteList

    @db_session
    def beforeEditing(self):
        self.update_list()

    @db_session
    def update_list(self):
        self.wMain.values = self.parentApp.myDatabase.list_all_records()
        self.wMain.display()


class SatelliteView(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(SatelliteView, self).__init__(*args, **keywords)
        self.satellite = None

    def display_value(self, sat):
        self.satellite = sat
        return(sat.title)

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITRECORDFM').value = act_on_this[0]
        self.parent.parentApp.switchForm('EDITRECORDFM')


class SatelliteViewDisplay(npyscreen.FormMutt):

    def __init__(self, *args, **keywords):
        super(SatelliteViewDisplay, self).__init__(*args, **keywords)
        self.satellite = None

    MAIN_WIDGET_CLASS = SatelliteView

    @db_session
    def beforeEditing(self):
        self.update_list()

    @db_session
    def update_list(self):
        self.wStatus1 = self.satellite.title
        self.wMain.values = self.parentApp.myDatabase.list_all_records()
        self.wStatus2 = self.satellite.sync
        self.wMain.display()



class EditRecord(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgTitle = self.add(npyscreen.TitleText, name="Title:",)
        self.wgSync = self.add(npyscreen.TitleDateCombo, name="Last sync:")
        self.wgActive = self.add(npyscreen.TitleSelectOne, name="Active:")
        self.wgActive.values = [True, False]

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_record(self.value)
            self.name = "Record id : %s" % record[0]
            self.record_id          = record[0]
            self.wgTitle.value   = record[1]
            self.wgSync.value = record[2]
            self.wgActive.value      = record[3]
        else:
            self.name = "New Record"
            self.record_id = ''
            self.wgTitle.value = ''
            self.wgSync.value = ''
            self.wgActive.value = ''

    def on_ok(self):
        # if self.record_id:
        #     self.parentApp.myDatabase.update_record(self.record_id,
        #                                     title=self.wgTitle.value,
        #                                     sync=self.wgSync.value,
        #                                     active=self.wgActive.value,
        #                                     )
        # else:
        params = {'title': self.wgTitle.value,
                  'sync': self.wgSync.value,
                  'active': self.wgActive.value}
        self.parentApp.myDatabase.add_record(params)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class AddressBookApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = AddressDatabase()
        self.addForm("MAIN", SatelliteListDisplay)
        self.addForm("VIEW", SatelliteViewDisplay)
        self.addForm("EDITRECORDFM", EditRecord)

if __name__ == '__main__':
    myApp = AddressBookApplication()
    myApp.run()