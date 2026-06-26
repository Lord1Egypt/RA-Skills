# ROS 2 动作通信代码模板

本文档提供动作通信的完整代码模板，可直接用于创建动作服务端和客户端节点。

---

## Python 模板

### 动作定义文件

创建 `action/Fibonacci.action`：
```
# 目标（Goal）
int32 order
---
# 结果（Result）
int32[] sequence
---
# 反馈（Feedback）
int32[] partial_sequence
```

### 动作服务端节点（server）

```python
#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from action_msgs.msg import GoalStatus
import time

from custom_action_msgs.action import Fibonacci

class FibonacciActionServer(Node):
    """
    动作服务端示例
    
    功能：计算斐波那契数列，提供实时反馈
    """
    
    def __init__(self):
        super().__init__('fibonacci_action_server')
        
        # 使用 ReentrantCallbackGroup 允许并发执行
        self._callback_group = ReentrantCallbackGroup()
        
        # 创建动作服务端
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self._callback_group
        )
        
        self.get_logger().info('动作服务端已启动，等待目标...')

    def goal_callback(self, goal_request):
        """目标请求回调函数"""
        self.get_logger().info(f'收到目标请求: order={goal_request.order}')
        
        # 接受所有目标
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """取消请求回调函数"""
        self.get_logger().info('收到取消请求')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        """
        执行回调函数（异步）
        
        这是动作的核心逻辑，执行长时间任务并提供反馈
        """
        self.get_logger().info('开始执行任务...')
        
        # 获取目标参数
        order = goal_handle.request.order
        
        # 初始化反馈消息
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]
        
        # 执行任务（计算斐波那契数列）
        for i in range(1, order):
            # 检查是否被取消
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('任务已取消')
                return Fibonacci.Result()
            
            # 计算下一个数
            next_val = feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1]
            feedback_msg.partial_sequence.append(next_val)
            
            # 发布反馈
            self.get_logger().info(f'反馈: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            
            # 模拟耗时操作
            time.sleep(1)
        
        # 任务完成
        goal_handle.succeed()
        
        # 设置结果
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        
        self.get_logger().info('任务完成')
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = FibonacciActionServer()
    
    # 使用多线程执行器以支持异步操作
    from rclpy.executors import MultiThreadedExecutor
    executor = MultiThreadedExecutor()
    
    try:
        rclpy.spin(action_server, executor=executor)
    except KeyboardInterrupt:
        pass
    finally:
        action_server.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 动作客户端节点（client）

```python
#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from custom_action_msgs.action import Fibonacci

class FibonacciActionClient(Node):
    """
    动作客户端示例
    
    功能：发送目标、接收反馈和结果
    """
    
    def __init__(self):
        super().__init__('fibonacci_action_client')
        
        # 创建动作客户端
        self._action_client = ActionClient(
            self, Fibonacci, 'fibonacci')
        
        self.get_logger().info('动作客户端已就绪')

    def send_goal(self, order):
        """
        发送目标
        
        Args:
            order: 斐波那契数列的阶数
        """
        self.get_logger().info('等待动作服务端...')
        self._action_client.wait_for_server()
        
        # 创建目标消息
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        self.get_logger().info(f'发送目标: order={order}')
        
        # 异步发送目标
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        # 注册完成回调
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """目标响应回调函数"""
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('目标被拒绝')
            return
        
        self.get_logger().info('目标被接受')
        
        # 等待结果
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """结果回调函数"""
        result = future.result().result
        self.get_logger().info(f'收到结果: {result.sequence}')
        
        # 任务完成，关闭节点
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        """反馈回调函数"""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'收到反馈: {feedback.partial_sequence}')

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    
    # 发送目标
    action_client.send_goal(order=10)
    
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

---

## C++ 模板

### 动作服务端节点（server）

```cpp
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "custom_action_msgs/action/fibonacci.hpp"

#include <memory>
#include <thread>

class FibonacciActionServer : public rclcpp::Node {
public:
    using Fibonacci = custom_action_msgs::action::Fibonacci;
    using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;
    
    explicit FibonacciActionServer(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
        : Node("fibonacci_action_server", options) {
        
        // 创建动作服务端
        action_server_ = rclcpp_action::create_server<Fibonacci>(
            this,
            "fibonacci",
            std::bind(&FibonacciActionServer::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
            std::bind(&FibonacciActionServer::handle_cancel, this, std::placeholders::_1),
            std::bind(&FibonacciActionServer::handle_accepted, this, std::placeholders::_1));
        
        RCLCPP_INFO(this->get_logger(), "动作服务端已启动，等待目标...");
    }

private:
    rclcpp_action::GoalResponse handle_goal(
        const rclcpp_action::GoalUUID & uuid,
        std::shared_ptr<const Fibonacci::Goal> goal) {
        
        RCLCPP_INFO(this->get_logger(), "收到目标请求: order=%d", goal->order);
        
        // 拒绝无效目标
        if (goal->order <= 0) {
            RCLCPP_WARN(this->get_logger(), "拒绝无效目标");
            return rclcpp_action::GoalResponse::REJECT;
        }
        
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    }
    
    rclcpp_action::CancelResponse handle_cancel(
        const std::shared_ptr<GoalHandleFibonacci> goal_handle) {
        
        RCLCPP_INFO(this->get_logger(), "收到取消请求");
        return rclcpp_action::CancelResponse::ACCEPT;
    }
    
    void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle) {
        // 在新线程中执行，避免阻塞
        std::thread{std::bind(&FibonacciActionServer::execute, this, std::placeholders::_1), goal_handle}.detach();
    }
    
    void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle) {
        RCLCPP_INFO(this->get_logger(), "开始执行任务...");
        
        rclcpp::Rate loop_rate(1);
        auto goal = goal_handle->get_goal();
        auto feedback = std::make_shared<Fibonacci::Feedback>();
        auto result = std::make_shared<Fibonacci::Result>();
        
        feedback->partial_sequence.push_back(0);
        feedback->partial_sequence.push_back(1);
        
        for (int i = 1; i < goal->order; ++i) {
            // 检查是否被取消
            if (goal_handle->is_canceling()) {
                result->sequence = feedback->partial_sequence;
                goal_handle->canceled(result);
                RCLCPP_INFO(this->get_logger(), "任务已取消");
                return;
            }
            
            // 计算下一个数
            feedback->partial_sequence.push_back(
                feedback->partial_sequence[i] + feedback->partial_sequence[i-1]);
            
            // 发布反馈
            goal_handle->publish_feedback(feedback);
            RCLCPP_INFO(this->get_logger(), "发布反馈");
            
            loop_rate.sleep();
        }
        
        // 任务完成
        result->sequence = feedback->partial_sequence;
        goal_handle->succeed(result);
        RCLCPP_INFO(this->get_logger(), "任务完成");
    }
    
    rclcpp_action::Server<Fibonacci>::SharedPtr action_server_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FibonacciActionServer>());
    rclcpp::shutdown();
    return 0;
}
```

### 动作客户端节点（client）

```cpp
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "custom_action_msgs/action/fibonacci.hpp"

class FibonacciActionClient : public rclcpp::Node {
public:
    using Fibonacci = custom_action_msgs::action::Fibonacci;
    using GoalHandleFibonacci = rclcpp_action::ClientGoalHandle<Fibonacci>;
    
    explicit FibonacciActionClient(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
        : Node("fibonacci_action_client", options) {
        
        // 创建动作客户端
        client_ptr_ = rclcpp_action::create_client<Fibonacci>(this, "fibonacci");
        
        // 发送目标
        send_goal();
    }
    
    void send_goal() {
        // 等待服务端
        if (!client_ptr_->wait_for_action_server(std::chrono::seconds(10))) {
            RCLCPP_ERROR(this->get_logger(), "动作服务端不可用");
            rclcpp::shutdown();
            return;
        }
        
        auto goal_msg = Fibonacci::Goal();
        goal_msg.order = 10;
        
        RCLCPP_INFO(this->get_logger(), "发送目标");
        
        // 发送目标选项
        auto send_goal_options = rclcpp_action::Client<Fibonacci>::SendGoalOptions();
        send_goal_options.goal_response_callback =
            [this](const GoalHandleFibonacci::SharedPtr & goal_handle) {
                if (!goal_handle) {
                    RCLCPP_ERROR(this->get_logger(), "目标被拒绝");
                } else {
                    RCLCPP_INFO(this->get_logger(), "目标被接受");
                }
            };
        
        send_goal_options.feedback_callback =
            [this](GoalHandleFibonacci::SharedPtr, 
                   const std::shared_ptr<const Fibonacci::Feedback> feedback) {
                std::stringstream ss;
                ss << "收到反馈: ";
                for (auto num : feedback->partial_sequence) {
                    ss << num << " ";
                }
                RCLCPP_INFO(this->get_logger(), "%s", ss.str().c_str());
            };
        
        send_goal_options.result_callback =
            [this](const GoalHandleFibonacci::WrappedResult & result) {
                switch (result.code) {
                    case rclcpp_action::ResultCode::SUCCEEDED:
                        RCLCPP_INFO(this->get_logger(), "任务成功");
                        break;
                    case rclcpp_action::ResultCode::ABORTED:
                        RCLCPP_ERROR(this->get_logger(), "任务被中止");
                        break;
                    case rclcpp_action::ResultCode::CANCELED:
                        RCLCPP_ERROR(this->get_logger(), "任务被取消");
                        break;
                    default:
                        RCLCPP_ERROR(this->get_logger(), "未知结果");
                        break;
                }
                
                std::stringstream ss;
                ss << "结果: ";
                for (auto num : result.result->sequence) {
                    ss << num << " ";
                }
                RCLCPP_INFO(this->get_logger(), "%s", ss.str().c_str());
                
                rclcpp::shutdown();
            };
        
        client_ptr_->async_send_goal(goal_msg, send_goal_options);
    }

private:
    rclcpp_action::Client<Fibonacci>::SharedPtr client_ptr_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FibonacciActionClient>());
    rclcpp::shutdown();
    return 0;
}
```

---

## 使用方法

### 1. 创建功能包和消息定义
```bash
# 创建功能包
ros2 pkg create custom_action_msgs --dependencies action_msgs

# 创建 action 目录
mkdir -p custom_action_msgs/action
```

### 2. 编写动作定义文件
在 `custom_action_msgs/action/Fibonacci.action` 中编写定义。

### 3. 更新配置文件

**package.xml:**
```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

**CMakeLists.txt:**
```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/Fibonacci.action"
)

ament_export_dependencies(rosidl_default_runtime)
```

### 4. 编译和运行
```bash
# 编译
colcon build

# 运行服务端
ros2 run my_action_package action_server

# 运行客户端
ros2 run my_action_package action_client
```

### 5. 使用命令行操作动作
```bash
# 查看动作列表
ros2 action list

# 查看动作信息
ros2 action info /fibonacci

# 发送动作目标
ros2 action send_goal /fibonacci custom_action_msgs/action/Fibonacci "{order: 5}"
```

---

## 注意事项
- 动作适用于长时间运行的任务
- 支持实时反馈和取消操作
- 使用多线程执行器处理并发
- 服务端需实现目标、取消、执行三个回调
- 客户端需注册反馈和结果回调
