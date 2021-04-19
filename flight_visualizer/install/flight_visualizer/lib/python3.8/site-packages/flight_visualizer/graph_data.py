# This displays graphs of the flight data

import rclpy
from rclpy.node import Node
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from std_msgs.msg import Float64


class CreateGraphs(Node):

    def __init__(self):
        super().__init__('display_graphs')
        # TODO subscriptions
        self.subscription_time = self.create_subscription(
            Float64,
            'ElapsedTime',
            self.values_time_callback,
            100)
        self.subscription_time # prevent unused variable warning
        self.subscription_alt = self.create_subscription(
            Float64,
            'TrueAltitude',
            self.values_alt_callback,
            100)
        self.subscription_alt # prevent unused variable warning
        self.i = 0
        self.time = []
        self.index = []
        self.alt = []
        # self.xs and self.ys are temporary (but I'll probably forget)
        # TODO clean up self.<variable>
        self.ys = []
        self.xs = []

    def values_time_callback(self, msg):
        self.time.append(msg.data)
        self.get_logger().info('Timer heard: "%s"' % msg)

    def values_alt_callback(self, msg):
        self.alt.append(msg.data)
        self.index.append(self.i)
        self.i += 1
        self.get_logger().info('Alt heard: "%s"' % msg)
        # TODO make this branchless because that's *fancy*
        # Sometimes the time and altitude don't get reported
        # concurrently. This just helps make sure that the size of each list is the same so they can be plotted
        if len(self.time) > len(self.alt):
            x_vals = self.time[0: len(self.alt)]
            y_vals = self.alt
        elif len(self.alt) > len(self.time):
            x_vals = self.time
            y_vals = self.alt[0: len(self.time)]
        else:
            x_vals = self.time
            y_vals = self.alt
        self.ys = y_vals
        self.xs = x_vals
        # plt.show()
        # This needs to be global because the variable has to persists
        global ani
        ani = animation.FuncAnimation(plt.gcf(), self.animate, interval=200)
        # plt.tight_layout()
        # plt.ion()
        # plt.show()
        plt.pause(0.1)
        # TODO This entire thing is slow and needs to be optimized

    def animate(self, i):
        plt.cla()
        plt.plot(self.xs, self.ys)


def main(args=None):
    rclpy.init(args=args)

    display_graphs = CreateGraphs()
    rclpy.spin(display_graphs)

    display_graphs.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
