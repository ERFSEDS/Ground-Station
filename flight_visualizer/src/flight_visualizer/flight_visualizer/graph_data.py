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
            10)
        self.subscription_time  # prevent unused variable warning
        self.subscription_alt = self.create_subscription(
            Float64,
            'TrueAltitude',
            self.values_alt_callback,
            10)
        self.subscription_alt  # prevent unused variable warning
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
        # This needs to be global because the variable has to persists
        global ani
        ani = animation.FuncAnimation(plt.gcf(), self.animate, interval=1000)
        # Sometimes the time and altitude don't get reported concurrently. This just helps make sure that the size of
        # each list is the same so they can be plotted. Made branchless for speed, but the branched code is left for
        # reference under
        time_len = len(self.time)
        alt_len = len(self.alt)
        x_vals = ((time_len > alt_len) * (self.time[0: alt_len]) + (alt_len >= time_len) * self.time)
        y_vals = ((time_len >= alt_len) * self.alt + (alt_len > time_len) * (self.alt[0: time_len]))
        """
        if time_len > alt_len:
            x_vals = self.time[0: alt_len]
            y_vals = self.alt
        elif alt_len > time_len:
            x_vals = self.time
            y_vals = self.alt[0: time_len]
        else:
            x_vals = self.time
            y_vals = self.alt
        """
        self.ys = y_vals
        self.xs = x_vals
        ani
        plt.pause(1)  # Value here is in seconds. A higher value will result in a higher resolution graph, but will be
        # slower to plot
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
