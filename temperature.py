import os
import glob
import time

# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_c_calibrated = round(tempCalibrate(temp_c), 1)
        temp_f_calibrated = round(temp_c_calibrated * 9.0 / 5.0 + 32.0, 1)
        return temp_c_calibrated, temp_f_calibrated

def tempCalibrate(temp):
    '''
    Calibrate temperature, accept celcius
    '''
    caltem = temp * 0.69086 + 12.85
    return caltem

def temp_chk():
    print(' rom: '+ read_rom())
    print('Mengukur suhu, tunggu 2 menit')
    time.sleep(60)
    print('Tunggu 1 menit lagi...')
    time.sleep(30)
    print('Tunggu 30 detik lagi...')
    tmp = read_temp()
    print(f"Your current temperature is {tmp[0]}C {tmp[1]}F")
    return tmp[0]
    
def logic(tmp):
    if tmp <= 36:
        print("Error: Suhu terlalu rendah")
    elif tmp > 36 and tmp <= 37.5:
        print("Normal")
    elif tmp > 37.5 and tmp <= 38.5:
        print("Sakit ringan")
    else:
        print('Sakit parah')

if __name__ == '__main__':
    while True:
        logic(temp_chk())
        time.sleep(1)

        input('Press enter key to continue...')

