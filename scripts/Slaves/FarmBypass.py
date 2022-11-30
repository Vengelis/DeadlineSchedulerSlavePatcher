import os
import sys

import requests
from System.IO import *

from Deadline.Scripting import *
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

########################################################################
## Globals
########################################################################
scriptDialog = None
scriptDialog2 = None
########################################################################
## Main Function Called By Deadline
########################################################################

machineSlected = []

def __main__():

    global scriptDialog

    slvs = MonitorUtils.GetSelectedSlaveInfoSettings()
    machineListNoDssp = []
    machineListDssp = []
    for s in slvs:
        if s.Settings.SlaveExtraInfo9 == "BypassEnabled" :
            machineListDssp.append(s.SlaveName)
        else:
            machineListNoDssp.append(s.SlaveName)

    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetTitle( "Farm Bypass" )

    scriptDialog.AddGroupBox("DSSP", "DSSP", True)

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("DSSP", "LabelControl", "Disabled", 0, 0)
    scriptDialog.AddComboControlToGrid("MachineListComboControlNoDssp", "MultiSelectListControl", "",
                                                        machineListNoDssp, 1, 0, tooltip="Machines to manipule bypass",
                                                        expand=False)

    scriptDialog.AddControlToGrid("DSSP", "LabelControl", "Enabled", 0, 1)
    scriptDialog.AddComboControlToGrid("MachineListComboControlDssp", "MultiSelectListControl", "",
                                                               machineListDssp, 1, 1,
                                                               tooltip="Machines to manipule bypass",
                                                               expand=False)
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    addBypassButton = scriptDialog.AddControlToGrid("StartWorkers", "ButtonControl", "Add Bypass", 0, 0, expand=True)
    addBypassButton.ValueModified.connect(AddBypassToSlaves)

    removeBypassButton = scriptDialog.AddControlToGrid("StopWorkers", "ButtonControl", "Remove Bypass", 0, 1, expand=True)
    removeBypassButton.ValueModified.connect(RemoveBypassToSlaveSlaves)
    scriptDialog.EndGrid()

    scriptDialog.EndGroupBox(False)

    slvs = MonitorUtils.GetSelectedSlaveNames()
    slavesList = ""
    for s in slvs:
        slavesList = slavesList + s + ","

    scriptDialog.ShowDialog(True)

def AddBypassToSlaves( *args ):
    machineNames = scriptDialog.GetValue("MachineListComboControlNoDssp")
    new = scriptDialog.GetItems("MachineListComboControlDssp")
    old = scriptDialog.GetItems("MachineListComboControlNoDssp")
    for machineName in machineNames:
        svl = RepositoryUtils.GetSlaveSettings(machineName, False)
        svl.SlaveExtraInfo9 = "BypassEnabled"
        RepositoryUtils.SaveSlaveSettings(svl)
        new.append(machineName)
        old.remove(machineName)
    scriptDialog.SetItems("MachineListComboControlDssp", new)
    scriptDialog.SetItems("MachineListComboControlNoDssp", old)


def RemoveBypassToSlaveSlaves( *args ):
    machineNames = scriptDialog.GetValue("MachineListComboControlDssp")
    new = scriptDialog.GetItems("MachineListComboControlNoDssp")
    old = scriptDialog.GetItems("MachineListComboControlDssp")
    for machineName in machineNames:
        svl = RepositoryUtils.GetSlaveSettings(machineName, False)
        svl.SlaveExtraInfo9 = ""
        RepositoryUtils.SaveSlaveSettings(svl)
        new.append(machineName)
        old.remove(machineName)
    scriptDialog.SetItems("MachineListComboControlNoDssp", new)
    scriptDialog.SetItems("MachineListComboControlDssp", old)