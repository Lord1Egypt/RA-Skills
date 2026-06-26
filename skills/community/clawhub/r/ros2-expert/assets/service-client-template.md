# ROS 2 服务通信代码模板

本文档提供服务通信的完整代码模板，可直接用于创建服务端和客户端节点。

---

## Python 模板

### 服务端节点（server）

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceServer(Node):
    """
    服务端节点示例
    
    功能：提供 'add_two_ints' 服务，计算两个整数的和
    """
    
    def __init__(self):
        super().__init__('service_server')
        
        # 创建服务
        # 参数：服务类型、服务名、回调函数
        self.srv = self.create_service(
            AddTwoInts, 
            'add_two_ints', 
            self.add_two_ints_callback)
        
        self.get_logger().info('服务端已启动，等待请求...')

    def add_two_ints_callback(self, request, response):
        """
        服务回调函数
        
        Args:
            request: 客户端请求，包含 a 和 b 两个整数
            response: 服务响应，包含 sum 结果
        
        Returns:
            response: 填充后的响应对象
        """
        response.sum = request.a + request.b
        self.get_logger().info(f'收到请求: {request.a} + {request.b}')
        self.get_logger().info(f'返回结果: {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    server = ServiceServer()
    
    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    finally:
        server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 客户端节点（client）

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceClient(Node):
    """
    客户端节点示例
    
    功能：调用 'add_two_ints' 服务，计算两个整数的和
    """
    
    def __init__(self):
        super().__init__('service_client')
        
        # 创建客户端
        # 参数：服务类型、服务名
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
        # 等待服务端启动
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务端启动...')
        
        self.req = AddTwoInts.Request()
        self.get_logger().info('客户端已就绪')

    def send_request(self, a, b):
        """
        发送服务请求
        
        Args:
            a: 第一个整数
            b: 第二个整数
        
        Returns:
            服务的响应结果
        """
        self.req.a = a
        self.req.b = b
        
        # 异步调用服务
        self.future = self.cli.call_async(self.req)
        
        # 等待服务响应
        rclpy.spin_until_future_complete(self, self.future)
        
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    client = ServiceClient()
    
    # 发送请求
    response = client.send_request(4, 5)
    client.get_logger().info(f'结果: 4 + 5 = {response.sum}')
    
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## C++ 模板

### 服务端节点（server）

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class ServiceServer : public rclcpp::Node {
public:
    ServiceServer() : Node("service_server") {
        // 创建服务
        // 参数：服务名、回调函数
        service_ = this->create_service<example_interfaces::srv::AddTwoInts>(
            "add_two_ints",
            std::bind(&ServiceServer::add, this, std::placeholders::_1, std::placeholders::_2));
        
        RCLCPP_INFO(this->get_logger(), "服务端已启动，等待请求...");
    }

private:
    void add(
        const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
        std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response) {
        
        response->sum = request->a + request->b;
        
        RCLCPP_INFO(this->get_logger(), "收到请求: %ld + %ld", 
                    (long int)request->a, (long int)request->b);
        RCLCPP_INFO(this->get_logger(), "返回结果: %ld", (long int)response->sum);
    }
    
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ServiceServer>());
    rclcpp::shutdown();
    return 0;
}
```

### 客户端节点（client）

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class ServiceClient : public rclcpp::Node {
public:
    ServiceClient() : Node("service_client") {
        // 创建客户端
        client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
        
        // 等待服务端启动
        while (!client_->wait_for_service(std::chrono::seconds(1))) {
            RCLCPP_INFO(this->get_logger(), "等待服务端启动...");
        }
        
        RCLCPP_INFO(this->get_logger(), "客户端已就绪");
    }
    
    void send_request(int64_t a, int64_t b) {
        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = a;
        request->b = b;
        
        // 异步调用服务
        auto future_result = client_->async_send_request(request);
        
        // 等待结果
        if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), 
                                                future_result) ==
            rclcpp::FutureReturnCode::SUCCESS) {
            RCLCPP_INFO(this->get_logger(), "结果: %ld + %ld = %ld", 
                        (long int)a, (long int)b, (long int)future_result.get()->sum);
        } else {
            RCLCPP_ERROR(this->get_logger(), "服务调用失败");
        }
    }

private:
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    
    auto client = std::make_shared<ServiceClient>();
    client->send_request(4, 5);
    
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
ros2 pkg create --build-type ament_python my_service_package \
    --dependencies rclpy example_interfaces

# 或创建功能包（C++）
ros2 pkg create --build-type ament_cmake my_service_package \
    --dependencies rclcpp example_interfaces
```

### 2. 添加源文件

**Python：**
将 `server.py` 和 `client.py` 放入 `my_service_package/my_service_package/` 目录。

更新 `setup.py`：
```python
entry_points={
    'console_scripts': [
        'server = my_service_package.server:main',
        'client = my_service_package.client:main',
    ],
},
```

**C++：**
将 `server.cpp` 和 `client.cpp` 放入 `my_service_package/src/` 目录。

更新 `CMakeLists.txt`：
```cmake
add_executable(server src/server.cpp)
ament_target_dependencies(server rclcpp example_interfaces)

add_executable(client src/client.cpp)
ament_target_dependencies(client rclcpp example_interfaces)

install(TARGETS server client
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

**终端 1（服务端）：**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_service_package server
```

**终端 2（客户端）：**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_service_package client
```

### 5. 使用命令行调用服务
```bash
# 查看服务列表
ros2 service list

# 查看服务类型
ros2 service type /add_two_ints

# 调用服务
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 10, b: 20}"
```

---

## 自定义服务类型

### 1. 创建服务定义文件
创建 `srv/CustomService.srv`：
```
# 请求部分
string name
int32 age
---
# 响应部分
bool success
string message
```

### 2. 更新 package.xml
```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

### 3. 更新 CMakeLists.txt
```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/CustomService.srv"
)

ament_export_dependencies(rosidl_default_runtime)
```

### 4. 使用自定义服务
```python
from my_package.srv import CustomService

# 客户端
self.cli = self.create_client(CustomService, 'custom_service')
req = CustomService.Request()
req.name = "ROS 2"
req.age = 5
future = self.cli.call_async(req)

# 服务端
def callback(self, request, response):
    response.success = True
    response.message = f"Hello {request.name}, age {request.age}"
    return response
```

---

## 异步客户端示例（推荐）

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AsyncServiceClient(Node):
    """异步服务客户端示例"""
    
    def __init__(self):
        super().__init__('async_service_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务端启动...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        
        # 注册回调函数
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        """响应回调函数"""
        try:
            response = future.result()
            self.get_logger().info(f'收到结果: {response.sum}')
        except Exception as e:
            self.get_logger().error(f'服务调用失败: {e}')

def main(args=None):
    rclpy.init(args=args)
    client = AsyncServiceClient()
    
    # 发送多个异步请求
    client.send_request(1, 2)
    client.send_request(3, 4)
    client.send_request(5, 6)
    
    # 持续 spin 以处理回调
    rclpy.spin(client)
    
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 注意事项
- 服务是同步的，客户端会阻塞等待响应
- 使用异步客户端可避免阻塞
- 服务端回调函数必须返回响应对象
- 确保客户端和服务端使用相同的服务类型
- 启动顺序：先启动服务端，再启动客户端
