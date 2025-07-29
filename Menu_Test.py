#Prompt user for input
    #1) List existing files
        #1a) Write to existing file
        #1b) Delete existing file
        #1c) View size of existing file
    #2) Make new file, and start writing to it

import os

SD_CARD_PATH = "/run/media/dpsimon/TEST_DRIVE"

def list_files():
    files = [f for f in os.listdir(SD_CARD_PATH) if os.path.isfile(os.path.join(SD_CARD_PATH, f))]
    for i, f in enumerate(files):
        print(f"{i + 1}: {f}")
    return files

def write_to_file(filename):
    filepath = os.path.join(SD_CARD_PATH, filename)
    text = input("Enter text to write: ")
    with open(filepath, 'a') as f:
        f.write(text + '\n')
    print(f"Text written to {filename}.")

def delete_file(filename):
    filepath = os.path.join(SD_CARD_PATH, filename)
    choice = input("Are you sure? y/n")
    if choice == 'y':
        os.remove(filepath)
        print(f"{filename} deleted.")

def file_size(filename):
    filepath = os.path.join(SD_CARD_PATH, filename)
    size = os.path.getsize(filepath)
    print(f"{filename} size: {size} bytes")

def create_and_write_file():
    filename = input("Enter new file name: ")
    filepath = os.path.join(SD_CARD_PATH, filename)
    text = input("Enter initial text: ")
    with open(filepath, 'w') as f:
        f.write(text + '\n')
    print(f"{filename} created and written to.")

def main():
    found = False
    while True:
        print("\nOptions:")
        print("1. List existing files")
        print("2. Create new file and write to it")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            files = list_files()
            if not files:
                print("No files found.")
                continue

            sub_choice = input("a) Write\nb) Delete\nc) View size\nChoice: ").lower()
            try:
                file_index = int(input("Enter file number: ")) - 1
                filename = files[file_index]
            except (IndexError, ValueError):
                print("Invalid selection.")
                continue

            if sub_choice == 'a':
                write_to_file(filename)
            elif sub_choice == 'b':
                delete_file(filename)
            elif sub_choice == 'c':
                file_size(filename)
            else:
                print("Invalid option.")
        elif choice == '2':
            create_and_write_file()
        elif choice == '3':
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()

void setup() {
  Serial.begin(115200);
}

void loop() {
  float temperature = readSensor(); // Replace with real function
  Serial.print("Temp: ");
  Serial.println(temperature);
  delay(1000);
}


from pyb import UART
import time

# UART(1) corresponds to X1=RX, X2=TX on original Pyboard
uart = UART(1, 115200)  # Baud rate must match Artemis
uart.init(115200, bits=8, parity=None, stop=1)

while True:
    if uart.any():
        line = uart.readline()
        if line:
            print(line.decode().strip())
    time.sleep(0.1)
Step 1 — Edit /flash/boot.py
You only need this once — place it on internal flash:

import pyb
import os

# Force boot from internal flash
pyb.boot('F')  # 'F' for Flash boot

# Try to mount SD card for storage
try:
    sd = pyb.SDCard()
    os.mount(sd, '/sd')
    print("SD card mounted at /sd")
except OSError:
    print("No SD card detected.")

# Write to file on SD card
with open('/sd/myfile.txt', 'w') as f:
    f.write('Logging data to SD card')

# Read from file
with open('/sd/myfile.txt', 'r') as f:
    print(f.read())

from machine import I2C, Pin
import time
===================================
# Initialize I2C (adjust pins as needed)
i2c = I2C(1, freq=100_000)  # X9=SCL, X10=SDA by default
address = 0x36

# Helper to read 16-bit signed integer from registers 0x00 and 0x01
def read_encoder_position():
    data = i2c.readfrom_mem(address, 0x00, 2)
    pos = int.from_bytes(data, 'little', signed=True)
    return pos

# Read button state (0 = not pressed, 1 = pressed)
def read_button_state():
    data = i2c.readfrom_mem(address, 0x03, 1)
    return bool(data[0])

# Optionally read event flags (not always necessary)
def read_button_event():
    data = i2c.readfrom_mem(address, 0x05, 1)
    return data[0]

# Store previous state
last_position = read_encoder_position()
last_button = read_button_state()

print("Begin reading encoder and button via I2C...")

while True:
    position = read_encoder_position()
    if position != last_position:
        direction = "Right" if position > last_position else "Left"
        print(f"Rotated {direction}: {position}")
        last_position = position

    button = read_button_state()
    if button and not last_button:
        print("Button Pressed")
    elif not button and last_button:
        print("Button Released")
    last_button = button

    time.sleep(0.05)
========================================================
String* parseCSV(String line, int* fieldCount) {
  // Count how many commas (fields = commas + 1)
  int count = 1;
  for (int i = 0; i < line.length(); i++) {
    if (line.charAt(i) == ',') {
      count++;
    }
  }

  // Allocate array on heap
  String* fields = new String[count];
  int startIdx = 0;
  int idx = 0;

  for (int i = 0; i <= line.length(); i++) {
    if (line.charAt(i) == ',' || i == line.length()) {
      fields[idx++] = line.substring(startIdx, i);
      startIdx = i + 1;
    }
  }

  *fieldCount = count;
  return fields;
}

void setup() {
  Serial.begin(9600);
  delay(500);  // Wait for Serial monitor to open

  String csv = "2025-07-28,25.6,26.3,0.7,extra,data,fields";
  int numFields = 0;

  String* parsed = parseCSV(csv, &numFields);

  for (int i = 0; i < numFields; i++) {
    Serial.print("Field ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(parsed[i]);
  }

  delete[] parsed;  // Free heap memory
}

void loop() {
  // Nothing here
}
