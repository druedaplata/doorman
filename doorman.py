#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os
import pandas as pd
from mfrc522 import SimpleMFRC522
from pwgen import pwgen

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Doorman():

    def __init__(self, csv_file):
        if os.path.exists(csv_file):
            self.data = pd.read_csv(csv_file, index_col='Key')
        else:
            self.data = pd.DataFrame([], columns=['Nombre','Apellido','Key','Password'], index_col='Key')
        self.reader = SimpleMFRC522()

    def read_card(self):
        try:
            key, password = self.reader.read()
            if key in self.data.Key.values:
                current_password = self.data[self.data['Key'] == key]['Passowrd'].values[0]
                if password == current_password:
                    self._update_password(key)
                    self._open_door()
                else:
                    print('Password in Card is different from CSV.')
            else:
                print('Card ID is not registered.')
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise

    def _open_door(self):
        # Activate PIN
        GPIO.setup(17,GPIO.OUT)
        # Open Door
        GPIO.output(17,GPIO.HIGH)
        time.sleep(2)
        # Close Door
        GPIO.output(17,GPIO.LOW)

    def _update_password(self, key):
        # Update password in Card
        new_password = pwgen()
        self.reader.write(new_password)

        # Update password in CSV
        self.data.loc[key].password = new_password


if __name__ == "__main__":

    # Keep waiting for card
    doorman = Doorman('accesslist.csv')
    while True:
        doorman.read_card()



        
        



    

