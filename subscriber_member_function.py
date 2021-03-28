# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import pyowm

class MinimalSubscriber(Node):


    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'weather/request',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
         

    def listener_callback(self, msg):
    	self.get_logger().info('Now presenting the weather for the location "%s"' % msg.data)
    	owm = pyowm.OWM('72c302d83fd2cfe236f4982010a2ef66')
    	mng = owm.weather_manager()
    	obs = mng.weather_at_place(msg.data).weather.temperature('celsius')
    	
    	location = 'weather/%s' % msg.data
    	if obs is not None:
    		self.publisher_ = self.create_publisher(String,location, 10)
    		mag = String()
    		mag.data = "Process Completed"
    		self.publisher_.publish(mag)
    		self.get_logger().info('CURRENT WEATHER of: "%s "%s" "%s"' % (msg.data ,obs, mag.data))

    	

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

