# ROS 2 开发最佳实践

## 目录
1. [代码规范](#代码规范)
2. [节点设计原则](#节点设计原则)
3. [通信机制选择](#通信机制选择)
4. [性能优化](#性能优化)
5. [调试与日志](#调试与日志)
6. [包管理规范](#包管理规范)

---

## 代码规范

### 命名规范

#### 节点命名
- 使用小写字母和下划线
- 描述节点功能：`camera_driver`, `motion_controller`, `navigation_server`
- 避免通用名称：`node1`, `test_node`

#### 话题命名
- 使用小写字母和下划线
- 描述数据内容：`/camera/image_raw`, `/robot/odom`, `/scan`
- 使用命名空间组织：`/sensor/imu/data`, `/actuator/motor/cmd`

#### 服务命名
- 使用动词描述操作：`/get_pose`, `/set_velocity`, `/start_navigation`
- 遵循 `<action>_<target>` 格式

#### 动作命名
- 使用动词描述任务：`/navigate_to_goal`, `/execute_trajectory`
- 明确任务目标

### 代码结构（Python）

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ExampleNode(Node):
    """示例节点，展示标准代码结构"""
    
    def __init__(self):
        # 初始化节点，指定名称
        super().__init__('example_node')
        
        # 声明参数
        self.declare_parameter('param_name', default_value)
        
        # 创建通信对象（发布者、订阅者、服务、动作）
        self.publisher = self.create_publisher(String, 'topic', 10)
        self.subscription = self.create_subscription(
            String, 'topic', self.callback, 10)
        
        # 创建定时器
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        # 初始化成员变量
        self.count = 0
        
        self.get_logger().info('节点已初始化')

    def timer_callback(self):
        """定时器回调函数"""
        msg = String()
        msg.data = f'Count: {self.count}'
        self.publisher.publish(msg)
        self.count += 1

    def callback(self, msg):
        """订阅者回调函数"""
        self.get_logger().info(f'收到: {msg.data}')

def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    node = ExampleNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 代码结构（C++）

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class ExampleNode : public rclcpp::Node {
public:
    ExampleNode() : Node("example_node"), count_(0) {
        // 声明参数
        this->declare_parameter("param_name", default_value);
        
        // 创建发布者
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
        
        // 创建订阅者
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "topic", 10, 
            std::bind(&ExampleNode::callback, this, std::placeholders::_1));
        
        // 创建定时器
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&ExampleNode::timer_callback, this));
        
        RCLCPP_INFO(this->get_logger(), "节点已初始化");
    }

private:
    void timer_callback() {
        auto message = std_msgs::msg::String();
        message.data = "Count: " + std::to_string(count_++);
        publisher_->publish(message);
    }
    
    void callback(const std_msgs::msg::String::SharedPtr msg) {
        RCLCPP_INFO(this->get_logger(), "收到: '%s'", msg->data.c_str());
    }
    
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
    rclcpp::TimerBase::SharedPtr timer_;
    size_t count_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ExampleNode>());
    rclcpp::shutdown();
    return 0;
}
```

---

## 节点设计原则

### 单一职责原则
每个节点应专注于单一功能：
- `camera_driver_node`：仅负责相机数据采集
- `image_processor_node`：仅负责图像处理
- `object_detector_node`：仅负责目标检测

### 避免反模式
- **上帝节点（God Node）**：一个节点承担过多职责
- **过度碎片化**：一个功能拆分成过多节点

### 生命周期节点
对于需要状态管理的节点（如传感器驱动），使用生命周期节点：

```python
from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn

class LifecycleExampleNode(LifecycleNode):
    def __init__(self):
        super().__init__('lifecycle_example')
        
    def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info('配置中...')
        # 初始化资源
        return TransitionCallbackReturn.SUCCESS
    
    def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info('激活中...')
        # 启动发布者、订阅者
        return TransitionCallbackReturn.SUCCESS
    
    def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info('停用中...')
        # 停止通信
        return TransitionCallbackReturn.SUCCESS
    
    def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info('清理中...')
        # 释放资源
        return TransitionCallbackReturn.SUCCESS
    
    def on_shutdown(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info('关闭中...')
        # 关闭节点
        return TransitionCallbackReturn.SUCCESS
```

---

## 通信机制选择

### 决策流程
```
开始
  ↓
是否需要返回结果？
  ├─ 否 → 话题（Topic）
  └─ 是 ↓
      是否为长时间任务？
          ├─ 是 → 动作（Action）
          └─ 否 → 服务（Service）
```

### 详细对比

| 场景 | 推荐机制 | 原因 |
|------|---------|------|
| 传感器数据传输 | 话题 | 连续数据流，无需回复 |
| 状态广播 | 话题 | 多接收者，异步通信 |
| 参数查询 | 服务 | 一次性，需要返回值 |
| 触发操作 | 服务 | 同步执行，确认结果 |
| 导航任务 | 动作 | 长时间，需反馈 |
| 机械臂运动 | 动作 | 可取消，需进度反馈 |

---

## 性能优化

### QoS 配置
Quality of Service 配置用于优化数据传输：

```python
from rclpy.qos import QoSProfile
from rclpy.qos import ReliabilityPolicy, DurabilityPolicy

# 传感器数据（可靠性优先）
qos_sensor = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    depth=10
)

# 参数配置（可靠性优先）
qos_param = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    depth=10
)

self.subscription = self.create_subscription(
    Image, 'camera/image_raw', self.callback, qos_sensor)
```

### 避免阻塞回调
在回调函数中避免执行耗时操作：

```python
# 错误示例：在回调中执行耗时计算
def callback(self, msg):
    result = heavy_computation(msg)  # 阻塞回调
    self.publisher.publish(result)

# 正确示例：使用线程或异步处理
import threading

def callback(self, msg):
    thread = threading.Thread(target=self.process_data, args=(msg,))
    thread.start()

def process_data(self, msg):
    result = heavy_computation(msg)
    self.publisher.publish(result)
```

### 消息类型优化
- 使用紧凑的消息类型（避免传输不必要的数据）
- 合并多个小消息为一个大消息
- 使用数组代替多个独立字段

---

## 调试与日志

### 日志级别
```python
# 设置日志级别
self.get_logger().set_level(rclpy.logging.LoggingSeverity.DEBUG)

# 不同级别的日志
self.get_logger().debug('调试信息')
self.get_logger().info('普通信息')
self.get_logger().warning('警告信息')
self.get_logger().error('错误信息')
self.get_logger().fatal('致命错误')
```

### 调试工具

#### 1. 查看节点列表
```bash
ros2 node list
```

#### 2. 查看节点信息
```bash
ros2 node info /node_name
```

#### 3. 查看话题列表
```bash
ros2 topic list
```

#### 4. 查看话题数据
```bash
ros2 topic echo /topic_name
```

#### 5. 查看话题频率
```bash
ros2 topic hz /topic_name
```

#### 6. 发布测试消息
```bash
ros2 topic pub /topic_name std_msgs/msg/String "data: 'test'"
```

#### 7. 调用服务
```bash
ros2 service call /service_name example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"
```

---

## 包管理规范

### package.xml
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_package</name>
  <version>0.1.0</version>
  <description>ROS 2 包描述</description>
  <maintainer email="user@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <!-- 构建依赖 -->
  <buildtool_depend>ament_cmake</buildtool_depend>
  
  <!-- 运行时依赖 -->
  <depend>rclcpp</depend>
  <depend>std_msgs</depend>
  
  <!-- 测试依赖 -->
  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.8)
project(my_package)

# 设置 C++ 标准
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找依赖
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# 添加可执行文件
add_executable(my_node src/my_node.cpp)
ament_target_dependencies(my_node rclcpp std_msgs)

# 安装目标
install(TARGETS my_node
  DESTINATION lib/${PROJECT_NAME}
)

# 安装 launch 文件
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# 测试
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
```

---

## 文档导航
- ROS 2 官方文档：http://fishros.org/doc/ros2/humble/
- 教程：http://fishros.org/doc/ros2/humble/Tutorials.html
- 开发指南：http://fishros.org/doc/ros2/humble/Developer-Guide.html
