# This takes data being published to the ResponseData topic and publishes the individual data points to separate topics

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import Int64


class ValuesInput(Node):

    def __init__(self):
        # values_input node is subscribed to the ResponseData topic and publishes to various topics
        super().__init__('sensor_values')
        self.subscription = self.create_subscription(
            # TODO figure out for sure what data type is being used here
            Float64MultiArray,
            'ResponseData',
            self.values_input_callback,
            100)
        self.subscription  # prevent unused variable warning
        # All the different topics different sensors are being published to
        self.publisher_time_ = self.create_publisher(Float64, 'ElapsedTime', 50)
        self.publisher_messagenum_ = self.create_publisher(Int64, 'MessageNum', 50)
        self.publisher_accelx_ = self.create_publisher(Float64, 'AccelX', 50)
        self.publisher_accely_ = self.create_publisher(Float64, 'AccelY', 50)
        self.publisher_accelz_ = self.create_publisher(Float64, 'AccelZ', 50)
        self.publisher_gyrox_ = self.create_publisher(Float64, 'GyroX', 50)
        self.publisher_gyroy_ = self.create_publisher(Float64, 'GyroY', 50)
        self.publisher_gyroz_ = self.create_publisher(Float64, 'GyroZ', 50)
        self.publisher_pressure_ = self.create_publisher(Float64, 'Pressure', 50)
        self.publisher_truealt_ = self.create_publisher(Float64, 'TrueAltitude', 50)
        self.publisher_trueangle_ = self.create_publisher(Float64, 'TrueAngle', 50)

    def values_output_callback(self, msg):
        output_data = msg.data
        # Maybe there is a way to make this more compact, but I don't know it
        # Initializes each variable with the correct data type
        timeelapsed = Float64()
        msgnum = Int64()
        accelx = Float64()
        accely = Float64()
        accelz = Float64()
        gyrox = Float64()
        gyroy = Float64()
        gyroz = Float64()
        pressure = Float64()
        truealt = Float64()
        trueangle = Float64()
        # Setting each variable's data
        timeelapsed.data = float(output_data[0])
        msgnum.data = int(output_data[1])
        accelx.data = float(output_data[2])
        accely.data = float(output_data[3])
        accelz.data = float(output_data[4])
        gyrox.data = float(output_data[5])
        gyroy.data = float(output_data[6])
        gyroz.data = float(output_data[7])
        pressure.data = float(output_data[8])
        truealt.data = float(output_data[9])
        trueangle.data = float(output_data[10])
        # Publishing each variable to their respective topic
        self.publisher_time_.publish(timeelapsed)
        self.publisher_messagenum_.publish(msgnum)
        self.publisher_accelx_.publish(accelx)
        self.publisher_accely_.publish(accely)
        self.publisher_accelz_.publish(accelz)
        self.publisher_gyrox_.publish(gyrox)
        self.publisher_gyroy_.publish(gyroy)
        self.publisher_gyroz_.publish(gyroz)
        self.publisher_pressure_.publish(pressure)
        self.publisher_truealt_.publish(truealt)
        self.publisher_trueangle_.publish(trueangle)

    def values_input_callback(self, msg):
        self.values_output_callback(msg)


def main(args=None):
    rclpy.init(args=args)

    process_values = ValuesInput()
    rclpy.spin(process_values)

    process_values.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
