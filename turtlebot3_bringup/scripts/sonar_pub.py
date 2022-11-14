#!/usr/bin/python3
import time
import rospy
from rospy.exceptions import ROSInterruptException
from sensor_msgs.msg import Range
import RPi.GPIO as GPIO

trig_pin = 27
echo_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)


class SonarSensor:
    def __init__(self):
        rospy.init_node('sonar_pub', anonymous=True)
        rospy.loginfo("Setup sonar_pub[sensor_msg/Range]")
        rospy.on_shutdown(self.shutdown)
        self.pub = rospy.Publisher('sonar', Range, queue_size=10)
        rospy.Timer(rospy.Duration(0.5), self.timer_callback)

    # HIGH or LOWの時計測
    def pulse_in(self, PIN, start=1, end=0):
        if start==0: end = 1
        t_start = 0
        t_end = 0
        # ECHO_PINがHIGHである時間を計測
        while GPIO.input(PIN) == end:
            t_start = time.time()
            
        while GPIO.input(PIN) == start:
            t_end = time.time()
        return t_end - t_start

    # 距離計測
    def calc_distance(self): 
        # TRIGピンを0.1[s]だけLOW
        GPIO.output(trig_pin, GPIO.LOW)
        time.sleep(0.05)
        # TRIGピンを0.00001[s]だけ出力(超音波発射)        
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        # HIGHの時間計測
        t = self.pulse_in(echo_pin)
        # 距離[cm] = 音速[cm/s] * 時間[s]/2
        v=34000
        distance = v * t/2
        return distance

    def timer_callback(self, data):
        distance = self.calc_distance()
        # rospy.loginfo("distance: %f", distance)
        sensor_data = Range()
        sensor_data.range = distance
        self.pub.publish(sensor_data)

    def shutdown(self):
        rospy.sleep(1)
        rospy.loginfo("Shutdown")


if __name__ == '__main__':
    try:
        SonarSensor()
        rospy.spin()
    except ROSInterruptException:
        # ピン設定解除
        GPIO.cleanup()
        pass
