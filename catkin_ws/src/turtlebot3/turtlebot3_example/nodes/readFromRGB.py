import smbus
import time
import RPi.GPIO as GPIO

bus = smbus.SMBus(1)
bus.write_byte_data(0x44, 0x01, 0x05)

led = 18 # Se slides week 2 slide 4 for GPIO nr.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)

def mean_lists(a, b, c):
        liste = []
        for i in range(len(a)):
                liste.append((a[i] + b[i] + c[i]) / 3)
        return sum(liste) / len(liste)

def detectVictim():
        reds = []
        greens = []
        blues = []

        for i in range(10):
                green = (bus.read_byte_data(0x44, 0x09) + bus.read_byte_data(0x44, 0x0A)*255) / 255
                red = (bus.read_byte_data(0x44, 0x0B) + bus.read_byte_data(0x44, 0x0C)*255) / 255
                blue = (bus.read_byte_data(0x44, 0x0D) + bus.read_byte_data(0x44, 0x0E)*255) / 255 * 1.75
                greens.append(green)
                reds.append(red)
                blues.append(blue)

        if mean_lists(reds, greens, blues) < 3:
                return True
        return False

def blinkLED():
        GPIO.output(led,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led,GPIO.LOW)

if detectVictim():
        print("Victim detected")