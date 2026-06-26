# ROS 2 核心概念详解

## 目录
1. [节点（Node）](#节点node)
2. [话题（Topic）](#话题topic)
3. [服务（Service）](#服务service)
4. [动作（Action）](#动作action)
5. [参数（Parameter）](#参数parameter)
6. [通信机制对比](#通信机制对比)

---

## 节点（Node）

### 概念定义
节点是 ROS 2 中执行计算的基本单元。每个节点都是一个独立的进程，负责单一的功能模块。

### 核心特性
- **独立性**：每个节点独立运行，可单独启动、停止、重启
- **通信能力**：通过话题、服务、动作、参数与其他节点通信
- **生命周期管理**：支持生命周期节点（Lifecycle Node），可管理节点状态转换

### 代码示例（Python）
```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('节点已启动')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 代码示例（C++）
```cpp
#include "rclcpp/rclcpp.hpp"

class MinimalNode : public rclcpp::Node {
public:
    MinimalNode() : Node("minimal_node") {
        RCLCPP_INFO(this->get_logger(), "节点已启动");
    }
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalNode>());
    rclcpp::shutdown();
    return 0;
}
```

### 文档参考
- 官方文档：Tutorials -> Understanding ROS 2 Nodes
- 文档链接：http://fishros.org/doc/ros2/humble/Tutorials/Understanding-ROS2-Nodes.html

---

## 话题（Topic）

### 概念定义
话题是节点间传递数据的通信通道，采用发布-订阅模式，适用于连续数据流传输。

### 核心特性
- **多对多通信**：多个发布者可向同一话题发布消息，多个订阅者可订阅同一话题
- **异步通信**：发布者无需等待订阅者，松耦合设计
- **消息类型**：支持标准消息类型（std_msgs, sensor_msgs 等）和自定义消息类型

### 适用场景
- 传感器数据流（激光雷达、相机、IMU）
- 状态信息广播（机器人位置、速度）
- 日志信息输出

### 代码示例（Python - 发布者）
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2: {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'发布消息: {msg.data}')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    talker = Talker()
    rclpy.spin(talker)
    talker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 代码示例（Python - 订阅者）
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String, 'chatter', self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'收到消息: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 文档参考
- 官方文档：Tutorials -> Understanding ROS 2 Topics
- 文档链接：http://fishros.org/doc/ros2/humble/Tutorials/Topics.html

---

## 服务（Service）

### 概念定义
服务采用请求-响应模式，适用于一次性任务或需要返回结果的操作。

### 核心特性
- **同步通信**：客户端发送请求后等待服务端响应
- **一对一通信**：一个服务端对应多个客户端
- **返回结果**：服务端处理后返回结果给客户端

### 适用场景
- 参数查询与设置
- 触发一次性操作（如抓取物体、拍照）
- 状态查询（如获取当前电量）

### 代码示例（Python - 服务端）
```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceServer(Node):
    def __init__(self):
        super().__init__('service_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('服务已启动，等待请求...')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'收到请求: {request.a} + {request.b}')
        self.get_logger().info(f'返回结果: {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    server = ServiceServer()
    rclpy.spin(server)
    server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 代码示例（Python - 客户端）
```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务端启动...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    client = ServiceClient()
    response = client.send_request(4, 5)
    client.get_logger().info(f'结果: 4 + 5 = {response.sum}')
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 文档参考
- 官方文档：Tutorials -> Understanding ROS 2 Services
- 文档链接：http://fishros.org/doc/ros2/humble/Tutorials/Services.html

---

## 动作（Action）

### 概念定义
动作是 ROS 2 的高级通信机制，结合了话题和服务的特性，适用于长时间运行的任务。

### 核心特性
- **三部分组成**：
  - Goal（目标）：客户端发送的任务目标
  - Feedback（反馈）：服务端定期发送的进度信息
  - Result（结果）：任务完成后的最终结果
- **可抢占**：客户端可在任务执行过程中取消目标
- **异步执行**：客户端无需阻塞等待

### 适用场景
- 导航任务（移动到目标位置）
- 机械臂运动（执行复杂轨迹）
- 长时间计算任务（如图像处理）

### 代码示例（Python - 服务端）
```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from action_msgs.msg import GoalStatus
from example_interfaces.action import Fibonacci

class ActionServerNode(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self, Fibonacci, 'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

    def goal_callback(self, goal_request):
        self.get_logger().info(f'收到目标请求: order={goal_request.order}')
        return rclpy.action.GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('收到取消请求')
        return rclpy.action.CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        self.get_logger().info('开始执行任务...')
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('任务已取消')
                return Fibonacci.Result()
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            self.get_logger().info(f'反馈: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            await rclpy.sleep(1)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info('任务完成')
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = ActionServerNode()
    rclpy.spin(action_server)

if __name__ == '__main__':
    main()
```

### 文档参考
- 官方文档：Tutorials -> Understanding ROS 2 Actions
- 文档链接：http://fishros.org/doc/ros2/humble/Tutorials/Actions.html

---

## 参数（Parameter）

### 概念定义
参数是节点的配置值，可在运行时动态修改，用于调整节点行为。

### 核心特性
- **类型支持**：支持 bool, int, double, string, byte[], 数组等类型
- **动态修改**：可通过命令行或代码动态修改参数值
- **声明与获取**：节点需先声明参数，再获取参数值

### 适用场景
- 调整算法参数（如 PID 控制系数）
- 配置传感器参数（如采样频率）
- 设置运行模式（如调试模式开关）

### 代码示例（Python）
```python
import rclpy
from rclpy.node import Node

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')
        
        # 声明参数并设置默认值
        self.declare_parameter('my_param', 'default_value')
        self.declare_parameter('int_param', 42)
        self.declare_parameter('double_param', 3.14)
        
        # 获取参数值
        my_param = self.get_parameter('my_param').value
        int_param = self.get_parameter('int_param').value
        double_param = self.get_parameter('double_param').value
        
        self.get_logger().info(f'字符串参数: {my_param}')
        self.get_logger().info(f'整数参数: {int_param}')
        self.get_logger().info(f'浮点参数: {double_param}')
        
        # 注册参数修改回调
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, params):
        for param in params:
            self.get_logger().info(f'参数 {param.name} 已修改为: {param.value}')
        return rclpy.node.SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 参数命令行操作
```bash
# 列出节点的所有参数
ros2 param list /parameter_node

# 获取参数值
ros2 param get /parameter_node my_param

# 设置参数值
ros2 param set /parameter_node my_param new_value
```

### 文档参考
- 官方文档：Tutorials -> Understanding ROS 2 Parameters
- 文档链接：http://fishros.org/doc/ros2/humble/Tutorials/Parameters.html

---

## 通信机制对比

| 特性 | 话题（Topic） | 服务（Service） | 动作（Action） |
|------|--------------|----------------|---------------|
| 通信模式 | 发布-订阅 | 请求-响应 | 目标-反馈-结果 |
| 通信方向 | 单向 | 双向 | 双向 |
| 同步性 | 异步 | 同步 | 异步 |
| 数据流 | 连续流 | 一次性 | 长时间任务 |
| 是否有反馈 | 否 | 否（仅有结果） | 是（中间反馈） |
| 典型应用 | 传感器数据 | 参数查询、一次性操作 | 导航、运动控制 |

### 选择建议
1. **使用话题**：当数据是连续流，且接收者无需回复时（如传感器数据）
2. **使用服务**：当需要一次性操作并等待结果时（如查询状态）
3. **使用动作**：当任务需要长时间执行且需要实时反馈时（如导航）

---

## 文档导航
- ROS 2 官方文档首页：http://fishros.org/doc/ros2/humble/
- 核心概念章节：http://fishros.org/doc/ros2/humble/Concepts.html
- 教程章节：http://fishros.org/doc/ros2/humble/Tutorials.html
