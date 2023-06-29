# -*- coding: utf-8 -*-
"""
Created on Wed Okt 10 11:11:49 2018

@author: Daniel Schiessl

------------------------------------------------------------------------------------------------
(c) COPYRIGHT 2018 by attocube systems AG, Germany. All rights reserved.

This module shall be a starting point for everyone working with Python and wanting
to integrate an AMC100 to their setup. For any suggestions on code optimization
or already modified code please contact Daniel Schiessl:
daniel.schiessl@attocube.com

HISTORY:
Date Author Description
2017-07-20 DSc created
2018-08-24 DSc updated for usage in Python
2018-09-26 JH added Function Decsriptions
------------------------------------------------------------------------------------------------

"""

import ACS
import System

class Device(ACS.Device, System.Device):
    def setActorParametersByParamName(self, axis, paramname, paramvalue):
        """
        Control the actors parameters of an actor parameter  name ( search through an internal parameter list)  for integer paramaters
        
        Parameters
        ----------
        axis:  [0|1|2]
        paramname:  possible parameter:  actortype (0 to 2), fmax (> freqmin < freqmax controller),amax (> 0 < ampmax controller)
      sensor_dir(boolean), pitchofgrading(>0), sensitivity  ( 1 to 15) , stepsize (>0)
        paramvalue: 
        Returns
        -------
        errNo: errNo
        """
        response = self.request("com.attocube.amc.control.setActorParametersByParamName", [axis, paramname, paramvalue])
        errNo = self.handleError(response)
        return errNo

    def setActorParamJson(self, axis, data):
        response = self.request("com.attocube.amc.control.setActorParametersJson", [axis, data])
        errCode = self.handleError(response)
        return errCode

    def setOutput(self, axis, enable):
        """
            This function sets the status of the output relays of the selected axis
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        enable : bool
            Switches the output relais
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlOutput", [axis, enable])
        errNo = self.handleError(response)
        return errNo

    def getOutput(self, axis):
        """
            This function gets the status of the output relays of the selected axis
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        enable : Bool
           Status of Output relais
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.getControlOutput", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setAmplitude(self, axis, amplitude):
        """
            Controls the amplitude of the actuator signal.
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        amplitude : int
            Amplitude in mV
        Returns
        ----------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlAmplitude", [axis, amplitude])
        errNo = self.handleError(response)
        return errNo

    def getAmplitude(self, axis):
        """
            Get Status of the amplitude of the actuator signal.
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        amplitude : int
            Amplitude in mV
        """
        response = self.request("com.attocube.amc.control.getControlAmplitude", [axis])
        errNo = self.handleError(response) # and check the answer from the apply message
        return errNo, response['result'][1]

    def setFrequency(self, axis, frequency):
        """
            Controls the frequency of the actuator signal.
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        frequency : int
            Frequency in mHz
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlFrequency", [axis, frequency])
        errNo = self.handleError(response)
        return errNo

    def getFrequency(self, axis):
        """
            Get Status of the frequency of the actuator signal.
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        frequency : int
            Frequency in mHz
        """
        response = self.request("com.attocube.amc.control.getControlFrequency", [axis])
        errNo = self.handleError(response) # and check the answer from the apply message
        return errNo, response['result'][1]

    def setActorSelection(self, axis, name):
        """
            This function sets the name for the positioner on the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        name : str
            name of the positioner
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = \
        self.request("com.attocube.amc.control.setActorParametersByName", [axis, name])
        errNo = self.handleError(response)
        return errNo

    def getActorName(self, axis):
        """
            This function gets the name of the positioner of the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        actor name : str
           name of the positioner
        """
        response = self.request("com.attocube.amc.control.getActorParametersActorName", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getActorType(self, axis):
        """
            This function gets the type of the positioner of the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        positioner type : str
           type of the positioner
        """
        response = self.request("com.attocube.amc.control.getActorType", [axis])
        errNo = self.handleError(response)
        # 0 = linear , 1 = rotator,  2 = goniometer
        return errNo, response['result'][1]

    def setReset(self, axis):
        """
            Resets the actual position to zero and marks the reference position as invalid.
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setReset", [axis])
        errNo = self.handleError(response)
        return errNo

    def setMove(self, axis, enable):
        """
            Controls the approach of the actor to the target position
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        enable : bool
            True: enable actor approach towards target position
            Falsee: disable actor approach towards target position
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlMove", [axis, enable])
        errNo = self.handleError(response)
        return errNo

    def getMove(self, axis):
        """
            status of the approach of the actor to the target position
        Parameters
        ----------
        axis : int
            Number of the axis to be monitored [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        movingStatus : int
           0 = not moving; 1 = moving
        """
        response = self.request("com.attocube.amc.control.getControlMove", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setNSteps(self, axis, backward, n):
        """
            triggers N steps in desired direction.
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        backward : bool
            Selects the desired direction.
        N : int
            Number of steps
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.move.setNSteps", [axis, backward, n])
        errNo = self.handleError(response)
        return errNo

    def setSingleStep(self, axis, direction):
        """
            triggers one step in desired direction.
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        direction : bool
            direction of movement
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.move.setNSteps", [axis, direction])
        errNo = self.handleError(response)
        return errNo

    def getNSteps(self, axis):
        """
            gets number of steps set
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        N : int
            Number of steps
        """
        response = self.request("com.attocube.amc.move.getNSteps", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setContinuousFwd(self, axis, enable):
        """
            set a continuous movement on the selected axis in positive direction
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        enable : bool
            True: enable continuous movement in forward direction
            False = disable continuous movement in forward direction
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.move.setControlContinousFwd", [axis, enable])
        errNo = self.handleError(response)
        return errNo

    def getContinuousFwd(self, axis):
        """
            get information about continuous movement on the selected axis in positive direction
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        statusContinuousFwd : bool
            True: continuous movement in forward direction enabled
            False = disable continuous movement in forward disabled
        """
        response = self.request("com.attocube.amc.move.getControlContinousFwd", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setContinuousBkwd(self, axis, enable):
        """
            set a continuous movement on the selected axis in negative direction
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        enable : bool
            True: enable continuous movement in forward direction
            False = disable continuous movement in forward direction
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.move.setControlContinousBkwd", [axis, enable])
        errNo = self.handleError(response)
        return errNo

    def getContinuousBkwd(self, axis):
        """
            get information about continuous movement on the selected axis in negative direction
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        statusContinuousFwd : bool
            True: continuous movement in forward direction enabled
            False = disable continuous movement in forward disabled
        """
        response = self.request("com.attocube.amc.move.getControlContinousBkwd", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setTargetPosition(self, axis, target):
        """
            sets the target position for the movement on the selected axis
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        target : int
            target position in nm
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.move.setControlTargetPosition", [axis, target])
        errNo = self.handleError(response)
        return errNo

    def getTargetPosition(self, axis):
        """
            get the target position for the selected axis
        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        target : int
            target position in nm
        """
        response = self.request("com.attocube.amc.move.getControlTargetPosition", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getStatusReference(self, axis):
        """
           gets information about the status of the reference position
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        status : bool
            True: Reference position is valid
            False: Reference position is invalid
        """
        response = self.request("com.attocube.amc.status.getStatusReference", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getStatusMoving(self, axis):
        """
            get information about the status of the stage output
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        status : int
           0: idle (no movement commands for positioner pending)
           1: moving (positioner actively driven to target position)
           2: pending (positioner in target range and not actively driven)
        """
        response = self.request("com.attocube.amc.status.getStatusMoving", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]


    def getStatusConnected(self, axis):
        """
        This function gets information about the connection status of the selected axis’ positioner.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------#
        errorNumber : int
           No error = 0
        conected : bool
           true: positioner electrically connected to controller
           false: positioner not electrically connected to controller
        """
        response = self.request("com.attocube.amc.status.getStatusConnected", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getReferencePosition(self, axis):
        """
           This function gets the reference position of the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        reference : int
           reference position in nm
        """
        response = self.request("com.attocube.amc.control.getReferencePosition", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getPosition(self, axis):
        """
            This function gets the current position of the positioner on the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        position : int
           positioner’s position in nm
        """
        response = self.request("com.attocube.amc.move.getPosition", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setReferenceAutoUpdate(self, axis, enable):
        """
            This function sets the status of whether the reference position is updated when the reference mark is hit.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        enable : bool
            true: update reference position every time the reference mark is hit
            false: update reference position just once when the reference mark is hit for
            the first time, ignore further hits
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlReferenceAutoUpdate", [axis, enable])
        return self.handleError(response)

    def getReferenceAutoUpdate(self, axis):
        """
            This function gets the status of whether the reference position is updated
            when the reference mark is hit.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
         enable : bool
            true: update reference position every time the reference mark is hit
            false: update reference position just once when the reference mark is hit
            for the first time, ignore further hits
        """
        response = self.request("com.attocube.amc.control.getControlReferenceAutoUpdate", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setAutoReset(self, axis, enable):
        """
            This function resets the position every time the reference position is detected.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        enable : bool
            true: reset position every time the reference position is detected
            false: do not reset the position every time the reference position is detected
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlAutoReset", [axis, enable])
        errNo = self.handleError(response)
        return errNo

    def getAutoReset(self, axis):
        """
            This function gets the Status if the controller resets the position every
            time the reference position is detected.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        enable : bool
            true: reset position every time the reference position is detected
            false: do not reset the position every time the reference position is detected
        """
        response = self.request("com.attocube.amc.control.getControlAutoReset", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setTargetRange(self, axis, value):
        """
            Set the range around the target position in which the flag "In Target Range"
            becomes active.
            
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        value : int
           target range in nm
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlTargetRange", [axis, value])
        errNo = self.handleError(response)
        return errNo

    def getTargetRange(self, axis):
        """
           get the range around the target position in which the flag "In Target Range"
           becomes active.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        Range : int
           target range in nm
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.getControlTargetRange", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getStatusTargetRange(self, axis):
        """
           get information about whether the selected axis’ positioner is in target range
           or not
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        in target range : bool
            True: positioner is within target range
            False: positioner is not within target range
        """
        response = self.request("com.attocube.amc.status.getStatusTargetRange", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getFpgaVersion(self):
        """
            This function gets the version number of the controller’s FPGA.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
           No error = 0
        version : str
           FPGA version number
        """
        response = self.request("com.attocube.amc.description.getFpgaVersion")
        return  response['result'][0]

    def getDeviceType(self):
        """
            This function gets the device type based on its EEPROM configuration.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
           No error = 0
        type : str
           type of the device
        """
        response = self.request("com.attocube.amc.description.getDeviceType")
        return  response['result'][0]

    def getStatusEotFwd(self, axis):
        """
            This function gets the status of the end of travel detection on the selected axis in forward direction.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        EotDetected : bool
           true: end of travel in forward direction detected false: end of travel in forward direction not detected
        """
        response = self.request("com.attocube.amc.status.getStatusEotFwd", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def getStatusEotBkwd(self, axis):
        """
            This function gets the status of the end of travel detection on the selected axis in backward direction.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        EotDetected : bool
           true: end of travel in forward direction detected false: end of travel in forward direction not detected
        """
        response = self.request("com.attocube.amc.status.getStatusEotBkwd", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setEotOutputDeactive(self, axis, enable):
        """
            This function sets he output applied to the selected axis on the end of travel.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        enable : bool
            true: deactivate output on end of travel false: keep output active on end of travel
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.move.setControlEotOutputDeactive", [axis, enable])
        errNo = self.handleError(response)
        return errNo

    def getEotOutputDeactive(self, axis):
        """
            This function gets the output applied to the selected axis on the end of travel.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        enable : bool
            true: deactivate output on end of travel false: keep output active on end of travel
        """
        response = self.request("com.attocube.amc.move.getControlEotOutputDeactive", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setFixOutputVoltage(self, axis, voltage):
        """
            This function sets the DC level output of the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Voltage : int
            DC output in mV
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.control.setControlFixOutputVoltage", [axis, voltage])
        errNo = self.handleError(response)
        return errNo

    def getFixOutputVoltage(self, axis):
        """
            This function gets the DC level output of the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        Voltage : int
            DC output in mV
        """
        response = self.request("com.attocube.amc.control.getControlFixOutputVoltage", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]


    def getPositionersList(self):
        """
            This function gets a list of the positioners connected to the device.
        Parameters
        -------
        Returns
        -------
        errorNumber : int
           No error = 0
        list : str
           name of Positioner
        listSize : int
           Size of List
        """
        response = self.request("com.attocube.amc.description.getPositionersList")
        return  response['result'][0]

    def setAQuadBInResolution(self, axis, resolution):
        """
            This function sets the real time input resolution for the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        resolution : int
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.rtin.setControlAQuadBInResolution", [axis, resolution])
        errNo = self.handleError(response)
        if errNo != 0: response = self.request("com.attocube.amc.rtin.apply", [axis]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getAQuadBInResolution(self, axis):
        """
            This function gets the real time input resolution for the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        resolution : int
        """
        response = self.request("com.attocube.amc.rtin.getControlAQuadBInResolution", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setAQuadBOut(self, axis, enable):
        """
            This function enables the real time output for the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        enable : bln
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.rtout.setControlAQuadBOut", [axis, \
                                                                               enable])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [axis]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getAQuadBOut(self, axis):
        """
            This function gets the status of the real time output for the selected axis.

        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]

        Returns
        -------
        errorNumber : int
            No error = 0
        enable : int
        """
        response = self.request("com.attocube.amc.rtout.getControlAQuadBOut", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setAQuadBOutResolution(self, axis, resolution):
        """
            This function sets the real time output resolution for the selected axis.

        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        resolution : int

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.amc.rtout.setControlAQuadBOutResolution", [axis, resolution])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [axis]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getAQuadBOutResolution(self, axis):
        """
            This function gets the real time output resolution for the selected axis.

        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]

        Returns
        -------
        errorNumber : int
            No error = 0
        resolution : int
        """
        response = self.request("com.attocube.amc.rtout.getControlAQuadBOutResolution", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setAQuadBOutclock(self, axis, clock):
        """
            This function sets the real time output clock for the selected axis.

        Parameters
        ----------
        axis : int
            Number of the axis to be used [0..2]
        clock : int

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.amc.rtout.setControlAQuadBOutclock", [axis, clock])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [0]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getAQuadBOutclock(self, axis):
        """
            This function gets the real time output clock for the selected axis.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]

        Returns
        -------
        errorNumber : int
           No error = 0
        clock : int
        """
        response = self.request("com.attocube.amc.rtout.getControlAQuadBOutclock", [axis])
        errNo = self.handleError(response)
        return errNo, response['result'][1]

    def setRtOutsignalMode(self, signalMode):
        """
            This function sets the real time output Signal mode for the selected axis.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        signalMode : int

        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.rtout.setRtOutsignalMode", [signalMode])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [0]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getRtOutsignalMode(self):
        """
            This function gets the real time output Signal mode for the selected axis.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]

        Returns
        -------
        errorNumber : int
           No error = 0
        SinalMode : int
        """
        response = self.request("com.attocube.amc.rtout.getRtOutsignalMode", [0])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setRealTimeInMode(self, axis, rtMode):
        """
            This function sets the real time input mode for the selected axis.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        rtMode : int
            0: Aquadb (LVTTL) 1: AquadB (LVDS) 8: Stepper (LVTTL) 9: Stepper(LVDS) 0: Trigger (LVTTL 11: Trigger (LVDS) 15: disable

        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.rtin.setRealTimeInMode", [axis, rtMode])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [0]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getRealTimeInMode(self, axis):
        """
            This function gets the real time input mode for the selected axis.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]

        Returns
        -------
        errorNumber : int
           No error = 0
        rtMode : int
            0: Aquadb (LVTTL) 1: AquadB (LVDS) 8: Stepper (LVTTL) 9: Stepper(LVDS)
            0: Trigger (LVTTL 11: Trigger (LVDS) 15: disable
        """
        response = self.request("com.attocube.amc.rtin.getRealTimeInMode", [axis])
        errNo = self.handleError(response)
        return errNo, self.convert_ModeNo2string(response['result'][1])

    def convert_ModeNo2string(self, rtMode):
        """
            converts Numbers to names
        Parameters
        ----------
        rtMode : int
            0: Aquadb (LVTTL) 1: AquadB (LVDS) 8: Stepper (LVTTL) 9: Stepper(LVDS) 0: Trigger (LVTTL 11: Trigger (LVDS) 15: disable
        Returns
        -------
        Mode : str
           0: Aquadb (LVTTL) 1: AquadB (LVDS) 8: Stepper (LVTTL) 9: Stepper(LVDS) 0: Trigger (LVTTL 11: Trigger (LVDS) 15: disable
        """
        if rtMode == 0:
            Mode = 'AquadB_LVTTL'
        elif rtMode == 1:
            Mode = 'AquadB_LVDS'
        elif rtMode == 2:
            Mode = 'HSSL_LVTTL' # currently not supported
        elif rtMode == 3:
            Mode = 'HSSL_LVDS' # currently not supported
        elif rtMode == 4:
            Mode = 'SPI_LVTTL' # currently not supported
        elif rtMode == 8:
            Mode = 'STEPPER_LVTTL'
        elif rtMode == 9:
            Mode = 'STEPPER_LVDS'
        elif rtMode == 10:
            Mode = 'TRIGGER_LVTTL'
        elif rtMode == 11:
            Mode = 'TRIGGER_LVDS'
        elif rtMode == 15:
            Mode = 'OFF'
        else:
            Mode = 'unknown'
        return Mode

    def setRealTimeInFeedbackLoopMode(self, axis, rtMode):
        """
            This function sets the real time input loop mode for the selected axis
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        rtMode : int
           0: open-loop
           1: closed-loop
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.rtin.setRealTimeInFeedbackLoopMode", [axis, rtMode])
        errNo = self.handleError(response)
        return errNo

    def getRealTimeInFeedbackLoopMode(self, axis):
        """
            This function gets the real time input loop mode for the selected axis
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        Returns
        -------
        errorNumber : int
           No error = 0
        rtMode : int
           0: open-loop
           1: closed-loop
        """
        response = self.request("com.attocube.amc.rtin.getRealTimeInFeedbackLoopMode", [axis])
        # True gets the temp value (if no apply has been sent)
        errNo = self.handleError(response)
        if errNo != 0:
            if response['result'][1] == 0:
                return_value = 'open-loop'
            elif response['result'][1] == 1:
                return_value = 'closed-loop'
        return return_value

    def setRealtimeInputChangePerPulse(self, axis, change):
        """
            This function sets the real time input change per Pulse for the selected axis.
        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        change : int
            change per pulse in nm – maximum 1,000,000 nm
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.rtin.setRealTimeInChangePerPulse", [axis, change])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [0]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getRealtimeInputChangePerPulse(self, axis):
        """
            This function gets the real time input change per Pulse for the selected axis.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]

        Returns
        -------
        errorNumber : int
           No error = 0
        change : int
            change per pulse in nm – maximum 1,000,000 nm
        """
        response = self.request("com.attocube.amc.rtin.getRealTimeInChangePerPulse", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setRealtimeInputStepsPerPulse(self, axis, steps):
        """
            This function sets the steps per pulse for the selected axis under real time input in closed-loop mode.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        steps : int
            number of steps per pulse – maximum 10,000 steps

        Returns
        -------
        errorNumber : int
           No error = 0
        """

        response = self.request("com.attocube.amc.rtin.setRealTimeInStepsPerPulse", [axis, steps])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [0]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getRealtimeInputStepsPerPulse(self, axis):
        """
            This function gets the steps per pulse for the selected axis under real time input in closed-loop mode.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]

        Returns
        -------
        errorNumber : int
           No error = 0
        steps : int
            number of steps per pulse – maximum 10,000 steps
        """
        response = self.request("com.attocube.amc.rtin.getRealTimeInStepsPerPulse", [axis])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]

    def setRealtimeInputMove(self, axis, enable):
        """
            This function sets the status for real time input on the selected axis in closed-loop mode.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]
        enable : bool
            true: enable movements
            false: disable movements

        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.amc.rtin.setControlMoveGPIO", [axis, enable])
        errNo = self.handleError(response)
        if errNo != 0:
            response = self.request("com.attocube.amc.rtout.apply", [0]) # if no error s apply message
        errNo = self.handleError(response)
        return errNo

    def getRealtimeInputMove(self, axis):
        """
            This function gets the status for real time input on the selected axis in closed-loop mode.

        Parameters
        ----------
        axis : int
           Number of the axis to be used [0..2]

        Returns
        -------
        enable : int
            true: enable movements
            false: disable movements
        raises exception otherwise
        """
        response = self.request("com.attocube.amc.rtin.getControlMoveGPIO", [axis, 0])
        errNo = self.handleError(response)
        return  errNo, response['result'][1]
