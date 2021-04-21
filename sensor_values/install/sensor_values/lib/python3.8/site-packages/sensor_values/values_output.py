# This is just here to test the functionality of process_values node
# User will be prompted for a path to a CSV file containing the test data

from itertools import islice
import csv
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class TestNode(Node):

    def __init__(self):
        super().__init__('test_nodes')
        self.publisher_ = self.create_publisher(Float64MultiArray, 'ResponseData', 100)
        # Gets data path to a csv file for example data. Open the file and stores it in self.data_array
        data_path = input('Input the path to the test data CSV file </path/to/file.csv>: ')
        with open(data_path, 'r') as my_file:
            self.data_array = list(csv.reader(my_file))
        timer_period = 0.0001  # seconds, test data is in 0.0001 time step. My laptop is slow (and so is python) so
        # it never actually gets this fast
        self.i = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Float64MultiArray()
        # Goes line by line, publishes the data and deletes the line
        cur_line = self.data_array.pop(1)
        for i in list(range(0, 11)):
            cur_line[i] = float(cur_line[i])
        msg.data = list(cur_line)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing message number: %d' % self.i)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    test_node = TestNode()
    rclpy.spin(test_node)

    test_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
