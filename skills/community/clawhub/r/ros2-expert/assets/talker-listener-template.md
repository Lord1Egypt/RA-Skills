# ROS 2 话题通信代码模板

本文档提供话题通信的完整代码模板，可直接用于创建发布者和订阅者节点。

---

## Python 模板

### 发布者节点（talker）

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    """
    话题发布者节点示例
    
    功能：定时向 'chatter' 话题发布字符串消息
    """
    
    def __init__(self):
        super().__init__('talker')
        
        # 创建发布者
        # 参数：消息类型、话题名、队列大小
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        
        # 创建定时器，每 0.5 秒调用一次 timer_callback
        timer_period = 0.5  # 单位：秒
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.count = 0
        self.get_logger().info('发布者节点已启动')

    def timer_callback(self):
        """定时器回调函数，发布消息"""
        msg = String()
        msg.data = f'Hello ROS 2: {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'发布消息: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    talker = Talker()
    
    try:
        rclpy.spin(talker)
    except KeyboardInterrupt:
        pass
    finally:
        talker.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 订阅者节点（listener）

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    """
    话题订阅者节点示例
    
    功能：订阅 'chatter' 话题并打印接收到的消息
    """
    
    def __init__(self):
        super().__init__('listener')
        
        # 创建订阅者
        # 参数：消息类型、话题名、回调函数、队列大小
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        
        self.subscription  # 防止未使用变量警告
        self.get_logger().info('订阅者节点已启动')

    def listener_callback(self, msg):
        """订阅者回调函数，处理接收到的消息"""
        self.get_logger().info(f'收到消息: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    
    try:
        rclpy.spin(listener)
    except KeyboardInterrupt:
        pass
    finally:
        listener.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## C++ 模板

### 发布者节点（talker）

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class Talker : public rclcpp::Node {
public:
    Talker() : Node("talker"), count_(0) {
        // 创建发布者
        // 参数：话题名、队列大小
        publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);
        
        // 创建定时器，每 500ms 调用一次 timer_callback
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&Talker::timer_callback, this));
        
        RCLCPP_INFO(this->get_logger(), "发布者节点已启动");
    }

private:
    void timer_callback() {
        auto message = std_msgs::msg::String();
        message.data = "Hello ROS 2: " + std::to_string(count_++);
        
        RCLCPP_INFO(this->get_logger(), "发布消息: '%s'", message.data.c_str());
        publisher_->publish(message);
    }
    
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    size_t count_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Talker>());
    rclcpp::shutdown();
    return 0;
}
```

### 订阅者节点（listener）

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class Listener : public rclcpp::Node {
public:
    Listener() : Node("listener") {
        // 创建订阅者
        // 参数：话题名、队列大小、回调函数
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "chatter",
            10,
            std::bind(&Listener::listener_callback, this, std::placeholders::_1));
        
        RCLCPP_INFO(this->get_logger(), "订阅者节点已启动");
    }

private:
    void listener_callback(const std_msgs::msg::String::SharedPtr msg) {
        RCLCPP_INFO(this->get_logger(), "收到消息: '%s'", msg->data.c_str());
    }
    
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Listener>());
    rclcpp::shutdown();
    return 0;
}
```

---

## 使用方法

### 1. 创建功能包
```bash
# 创建工作空间
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 创建功能包（Python）
ros2 pkg create --build-type ament_python my_topic_package --dependencies rclpy std_msgs

# 或创建功能包（C++）
ros2 pkg create --build-type ament_cmake my_topic_package --dependencies rclcpp std_msgs
```

### 2. 添加源文件

**Python：**
将 `talker.py` 和 `listener.py` 放入 `my_topic_package/my_topic_package/` 目录。

更新 `setup.py`：
```python
entry_points={
    'console_scripts': [
        'talker = my_topic_package.talker:main',
        'listener = my_topic_package.listener:main',
    ],
},
```

**C++：**
将 `talker.cpp` 和 `listener.cpp` 放入 `my_topic_package/src/` 目录。

更新 `CMakeLists.txt`：
```cmake
add_executable(talker src/talker.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/listener.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

install(TARGETS talker listener
  DESTINATION lib/${PROJECT_NAME}
)
```

### 3. 编译
```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

### 4. 运行
打开两个终端：

**终端 1（发布者）：**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_topic_package talker
```

**终端 2（订阅者）：**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_topic_package listener
```

---

## 扩展示例

### 自定义消息类型

1. 创建消息定义文件 `msg/CustomMessage.msg`：
```
string name
int32 age
float32 score
```

2. 更新 `package.xml`：
```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

3. 更新 `CMakeLists.txt`：
```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CustomMessage.msg"
)

ament_export_dependencies(rosidl_default_runtime)
```

4. 使用自定义消息：
```python
from my_package.msg import CustomMessage

msg = CustomMessage()
msg.name = "ROS 2"
msg.age = 5
msg.score = 95.5
self.publisher.publish(msg)
```

---

## 注意事项
- 确保发布者和订阅者使用相同的消息类型和话题名
- 队列大小（queue_size）根据实际需求调整
- 使用 `rclpy.spin()` 保持节点运行并处理回调
- 发布者和订阅者可在不同节点或同一节点中
