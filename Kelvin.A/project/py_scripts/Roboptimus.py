##DRAFT - No Time

from time import sleep_ms

from lib.servomovement import ServoMovement
from lib.colourscreen   import ColourScreen
from PiicoDev_Ultrasonic import PiicoDev_Ultrasonic
from PiicoDev_VEML6040    import PiicoDev_VEML6040
from PiicoDev_SSD1306     import create_PiicoDev_SSD1306


class Roboptimus:
    def __init__(self): 
        self.__movement = ServoMovement(
            forward=(2500,  500),
            left=( 500,  500),
            right=(2500, 2500),
            reverse=( 500, 2500),
            stop=(1500, 1500),
        )
        self.__display = create_PiicoDev_SSD1306() ##Shows 'Green' when green has been detected
                                                    #if hue > 90:
                                                    # self.__display.fill(0)
                                                    # self.__display.text("Green Detected", 0, 20, 0)
        self.__range_Front = PiicoDev_Ultrasonic(id=[1, 0, 0, 0])
        self.__range_Right = PiicoDev_Ultrasonic(id=[0, 0, 0, 0])
        self.__sensor = PiicoDev_VEML6040()
        self.__cs = ColourSensor(self.__sensor, debug=True)

    def read_sensor(self):
        Front_us = self.__range_Front.distance_mm()
        Right_us = self.__range_Right.distance_mm()
        hsv = self.__cs.sensecolour()
        hue = hsv['hue']
        return Front_us, Right_us, hue
    
    def navigate(self, Front_us, Right_us, hue):
        if hue > 90:
            self.__movement.stop()
            sleep_ms(2000)
            return

        if Front_us <= 100 and Right_us < 100:
            self.__movement.stop()
            sleep_ms(600)
            self.__movement.left()
            sleep_ms(475)

        elif Front_us <= 100 and Right_us > 101:
            self.__movement.stop()
            sleep_ms(600)
            self.__movement.right()
            sleep_ms(475)

        else:
            self.__movement.forward()

    def run(self):
        while True:
            Front_us, Right_us, hue = self.read_sensor()
            print(f"Front: {Front_us}, Right: {Right_us}, Hue: {hue}")
            self.navigate(Front_us, Right_us, hue)


while True:
    roboptimus = Roboptimus()
    roboptimus.run()

