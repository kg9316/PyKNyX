# -*- coding: utf-8 -*-

from __future__ import print_function

from pyknyx.api import FunctionalBlock, Device
from pyknyx.core.ets import ETS

GAD_MAP = {1: {'root': "heating",
               1: {'root': "setpoint",
                   1: "living",
                   2: "bedroom 1",
                   3: "bedroom 2",
                   4: "bedroom 3"
                  },
               2: {'root': "temperature",
                   1: "living",
                   2: "bedroom 1",
                   3: "bedroom 2",
                   4: "bedroom 3"
                  }
              },
           2: {'root': "lights",
               1: {'root': None,
                   1: 'living',
                 },
               2: {'root': "etage",
                   1: None,
                   2: "bedroom 1"
                 }
              }
          }


class WeatherWindBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="wind_speed", access="output", dptId="9.005", default=0.)
    DP_02 = dict(name="wind_alarm", access="output", dptId="1.005", default="No alarm")
    DP_03 = dict(name="wind_speed_limit", access="input", dptId="9.005", default=15.)
    DP_04 = dict(name="wind_alarm_enable", access="input", dptId="1.003", default="Disable")

    # Group Objects datapoints definition (can (should?) be defined in subclass)
    GO_01 = dict(dp="wind_speed", flags="CRT", priority="low")
    GO_02 = dict(dp="wind_alarm", flags="CRT", priority="normal")
    GO_03 = dict(dp="wind_speed_limit", flags="CWTU", priority="low")
    GO_04 = dict(dp="wind_alarm_enable", flags="CWTU", priority="low")

    DESC = "Wind management block"

    #@Device.schedule.every(minute=5)
    def refreshWindSpeed(self, event):

        # How we retrieve the speed is out of the scope of this proposal
        # speed = xxx

        # Now, write the new speed value to the Datapoint
        # This will trigger the bus notification, if a group object is associated
        self.dp["wind_speed"].value = speed

    #@Device.notify.datapoint(name="wind_speed_limit")
    #@Device.notify.datapoint(name="temperature")  # Single DP
    #@Device.notify.datapoint(name=("wind_speed", "wind_alarm"))  # Multiple DP
    #@Device.notify.datapoint()  # All DP
    #@Device.notify.datapoint(name="wind_speed", change=True)  # Only if value changed
    #@Device.notify.datapoint(name="wind_speed", condition="change")  # Only if value changed (could be "always")
    #@Device.notify.group(gad="1/1/1")  # Single group address
    #@Device.notify.groupObject(name="temperature")  # Single group object
    def checkWindSpeed(self, event):

        # Check alarm speed
        if self.dp["wind_alarm_enable"].value == "Enable":
            if speed >= self.dp["wind_speed_limit"].value:
                self.dp["wind_alarm"].value = "Alarm"
            elif speed < self.dp["wind_speed_limit"].value - 5.:
                self.dp["wind_alarm"].value = "No alarm"


class WeatherTemperatureBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="temperature", access="output", dptId="9.007", default=19.)
    DP_02 = dict(name="humidity", access="output", dptId="9.007", default=50.)

    # Group Objects datapoints definition (can (should?) be defined in subclass)
    GO_01 = dict(dp="temperature", flags="CRT", priority="low")
    GO_02 = dict(dp="humidity", flags="CRT", priority="low")

    DESC = "Temperature management block"

    #@Device.schedule.every(minute=5)
    def refreshTemperature(self, event):

        # How we retrieve the temperature/humidity is out of the scope of this proposal
        # temperature = xxx
        # humidity = xxx
        self.dp["temperature"] = temperature
        self.dp["humidity"] = humidity


class WeatherSunPositionBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="right_ascension", access="output", dptId="9.xxx", default=0.)
    DP_02 = dict(name="declination", access="output", dptId="9.xxx", default=0.)
    DP_03 = dict(name="elevation", access="output", dptId="9.xxx", default=0.)
    DP_04 = dict(name="azimuth", access="output", dptId="9.xxx", default=0.)
    DP_05 = dict(name="lattitude", access="param", dptId="9.xxx", default=0.)
    DP_06 = dict(name="longitude", access="param", dptId="9.xxx", default=0.)
    DP_07 = dict(name="altitude", access="param", dptId="9.xxx", default=0.)

    # Group Objects definition
    GO_01 = dict(dp="right_ascension", flags="CRT", priority="low")
    GO_02 = dict(dp="declination", flags="CRT", priority="low")
    GO_03 = dict(dp="elevation", flags="CRT", priority="low")
    GO_04 = dict(dp="azimuth", flags="CRT", priority="low")

    # Interface Object Properties definition
    #PR_01 = dict(dp="lattitude")
    #PR_02 = dict(dp="longitude")
    #PR_03 = dict(dp="altitude")

    DESC = "Sun position management block"


# Weather station class definition
class WeatherStation(Device):

    FB_01 = dict(cls=WeatherWindBlock, name="weather_wind_block", desc="Wind")
    FB_02 = dict(cls=WeatherTemperatureBlock, name="weather_temperature_block", desc="Temp")
    FB_03 = dict(cls=WeatherSunPositionBlock, name="weather_sun_position_block", desc="Sun")

    LNK_01 = dict(fb="weather_temperature_block", dp="temperature", gad="1/1/1")
    LNK_02 = dict(fb="weather_temperature_block", dp="humidity", gad="1/1/2")
    LNK_03 = dict(fb="weather_wind_block", dp="wind_speed", gad="1/1/3")
    LNK_04 = dict(fb="weather_wind_block", dp="wind_alarm", gad="1/1/4")
    LNK_05 = dict(fb="weather_wind_block", dp="wind_speed_limit", gad="1/1/5")
    LNK_06 = dict(fb="weather_wind_block", dp="wind_alarm_enable", gad="1/1/6")

def main():

    ets = ETS("7.9.99")
    ets._gadMap = GAD_MAP

# Instanciation of the weather station device object
    station = WeatherStation(ets, "1.2.3")

# Linking weather station Datapoints to Group Address

    ets.printGroat(by="gad")
    print()
    ets.printGroat(by="go")

if __name__ == "__main__":
    main()
