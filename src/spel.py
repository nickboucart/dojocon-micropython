import machine
import time
import servo
import ldr

def spring(s):
    s.write_angle(120)
    time.sleep(0.2)
    s.write_angle(90)
    
    
def spel():
    p=machine.Pin(2)
    s=servo.Servo(p)
    w=ldr.LDR(32)
    s.write_angle(90)
    while True:
        r=w.read()
        print(r)
        if r <600:  
            spring(s)
        time.sleep(0.05)
        
        
        
        