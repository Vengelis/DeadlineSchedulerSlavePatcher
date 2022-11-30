import os
import platform
from pprint import pprint

import requests
from Deadline.Events import *
from Deadline.Jobs import *
import csv
import json
from datetime import datetime

from Deadline.Scripting import *

EXCLUDED_MACHINE_STARTING_WITH = ['R', 'S', 'A']

#   Deadline event allowing to stop the calculation of a machine when the tag "BypassEnabled" is written in the ExtraInfo9 of the slave between 9:00 and 18:00.
#   The event is ignored on weekend days

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return DSSP()


######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


######################################################################
## This is the main DeadlineEventListener class for DsspEvent.
######################################################################
class DSSP(DeadlineEventListener):

    def __init__(self):
        self.OnSlaveStartingJobCallback += self.SlaveStartingJob

    def Cleanup(self):
        del self.OnSlaveStartingJobCallback

    def SlaveStartingJob(self, slave, job):

        slaveName = list(str(slave))
        slaveName[0] = slaveName[0].upper()

        cancel = False

        if slaveName[0] in EXCLUDED_MACHINE_STARTING_WITH:
            cancel = True

        if not cancel:

            svl = RepositoryUtils.GetSlaveSettings(slave, False)
            if svl.SlaveExtraInfo9 != "BypassEnabled":

                timeNow = datetime.today().strftime('%H:%M')

                stop = False

                if timeNow <= '12:00':
                    if timeNow >= '09:00':
                        stop = True
                else:
                    if timeNow <= '18:00':
                        stop = True

                if datetime.today().strftime('%A') == 'Saturday':
                    return
                if datetime.today().strftime('%A') == 'Sunday':
                    return

                if stop:
                    SlaveUtils.SendRemoteCommandNoWait(slave,
                                                           r'StopSlave')
                    print("DSSP : Order of extinction of the worker sent")