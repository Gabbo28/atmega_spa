from instruments import DS1000Z
import matplotlib.pyplot as plt
import time
import serial
import numpy as np


def read_until(until):
    out=b''
    while until.encode() not in out:
        out+=(ser.read())
    return out

def check_trace(trace,position):
    if trace[100+325+50*position]<-1.40:
        return True
    else:
        return False

def set_rigol(ip):
    instrument=DS1000Z(ip)
    print(instrument.get_identification())
    instrument.reset()

    #set ch2
    instrument.show_channel(2)
    instrument.set_probe_ratio(1,2)
    instrument.set_channel_scale(2,2)
    instrument.set_channel_offset(-4,2)


    #set trigger on ch2
    instrument.set_trigger_source(2)
    instrument.set_trigger_sweep('NORM')
    instrument.set_trigger_mode() #EDGE
    instrument.set_trigger_level(2)



    ##set ch1 for measurement
    instrument.show_channel(1)
    instrument.set_probe_ratio(1,1)
    instrument.enable_vernier(1)
    instrument.set_channel_scale(0.5,1)
    instrument.set_channel_offset(-2.5,1)



    #set time scale and offset
    instrument.set_timebase_scale(1e-06)
    instrument.set_timebase_offset(5e-06)

    print("Done setting oscilloscope!")
    return instrument



def main():
    test_letters = 'abcdefgioprsuwtm'
    guessed = ''
    response=''
    try:
        ser = serial.Serial(
        port = '/dev/ttyACM0',
        baudrate=9600,
        timeout=0.5
        )

        instrument = set_rigol('192.168.0.51')
        time.sleep(2)
        instrument.run()
    
        while 'Password is correct' not in response:
            values={}
            for l in test_letters:
                ser.read_until(': ')
                ser.write((guessed+l*(11-len(guessed))+'\n').encode())
                x,y = instrument.get_waveform_samples()
                y=(y-np.mean(y))/np.std(y)
                values[l]=y[100+325+50*(len(guessed))]
            good_guess=min(values, key=values.get)
            #print(f'{good_guess} is a good guess, double-checking..')

            ser.write((guessed+good_guess*(11-len(guessed))+'\n').encode())
            response=ser.read_until('!!').decode().replace('\n','')
            x,y = instrument.get_waveform_samples()
            y=(y-np.mean(y))/np.std(y)

            if check_trace(y,len(guessed)):
                guessed+=good_guess
                print(f'Password: {guessed}')
        print(f'Boom!!')

    finally:

        ser.close()
        #print("ser closed\n")
        instrument.stop()

if __name__ == "__main__":
    main()