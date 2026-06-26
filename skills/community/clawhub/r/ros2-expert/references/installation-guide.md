# ROS 2 一键安装工具使用指南

## 目录
1. [工具概述](#工具概述)
2. [安装步骤](#安装步骤)
3. [安装后检验](#安装后检验)
4. [常见问题排查](#常见问题排查)
5. [高级功能](#高级功能)

---

## 工具概述

### 一键安装工具简介
小鱼的一键安装工具是一个便捷的 ROS/ROS 2 环境配置工具，支持多种功能：
- ROS/ROS 2 一键安装
- rosdep 配置
- 系统源更换
- Docker 安装
- VSCode 配置

### 文档来源
- 官方文档：https://fishros.org.cn/forum/topic/20/

### 安装指令
```bash
wget http://fishros.com/install -O fishros && . fishros
```

---

## 安装步骤

### 第一步：运行安装指令
在终端中执行：
```bash
wget http://fishros.com/install -O fishros && . fishros
```

### 第二步：选择功能
工具会显示功能菜单，根据需求输入对应编号：

**常用选项：**
1. **更换系统源**：首次安装建议先换源（选项 2：更换系统源并清理第三方源）
2. **安装 ROS 2**：选择对应的 ROS 2 发行版（如 Humble）
3. **配置 rosdep**：用于依赖管理

### 第三步：首次安装注意事项
根据文档说明，首次安装时：
- **务必换源并清理三方源**：系统默认国外源容易失败
- 推荐选择：`2：更换系统源并清理第三方源`

### 第四步：等待安装完成
安装过程中终端会显示进度，请关注输出信息，若出现错误需记录错误内容。

---

## 安装后检验

### 1. 检查环境变量
```bash
printenv | grep ROS
```
**预期输出：**
```
ROS_VERSION=2
ROS_PYTHON_VERSION=3
ROS_DISTRO=humble
...
```

### 2. 检查安装目录
```bash
ls /opt/ros/humble
```
**预期输出：**
应显示 `setup.bash`, `bin/`, `lib/`, `share/` 等目录

### 3. 测试基本命令
```bash
ros2 --help
```
**预期输出：**
显示 ros2 命令的帮助信息

### 4. 运行示例节点
打开两个终端：

**终端 1（发布者）：**
```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

**终端 2（订阅者）：**
```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

**预期结果：**
- 终端 1 显示发布消息的日志
- 终端 2 显示接收到的消息

### 5. 配置环境变量（持久化）
若每次都需手动 source，可添加到 `~/.bashrc`：
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 常见问题排查

### 问题 1：NO_PUBKEY 错误
**错误信息：**
```
NO_PUBKEY <KEY>
```

**解决方案：**
```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <KEY>
```

**说明：**
将 `<KEY>` 替换为错误信息中显示的实际公钥。

---

### 问题 2：APT 锁错误
**错误信息：**
```
Could not get lock /var/lib/apt/lists/lock
E: Unable to lock directory /var/lib/apt/lists/
```

**原因：**
其他包管理进程正在运行（如 apt-get, aptitude, Software Center）

**解决方案：**
1. 关闭其他包管理器
2. 若无其他进程，手动删除锁：
```bash
sudo rm /var/lib/apt/lists/lock
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/dpkg/lock
```

---

### 问题 3：重复源配置警告
**错误信息：**
```
Target Packages (main/binary-amd64/Packages) is configured multiple times
```

**解决方案：**
检查并清理重复的源配置：
```bash
ls /etc/apt/sources.list.d/
```
找到重复的 `.list` 文件，删除多余项：
```bash
sudo rm /etc/apt/sources.list.d/<duplicate-file>.list
```

---

### 问题 4：网络问题导致下载失败
**错误信息：**
```
Failed to fetch http://...
Connection failed
```

**解决方案：**
1. 确保网络连接正常
2. 使用一键安装工具的"更换系统源"功能
3. 尝试多次运行安装命令

---

### 问题 5：安装后命令找不到
**错误信息：**
```
Command 'ros2' not found
```

**解决方案：**
1. 检查是否 source 了环境：
```bash
source /opt/ros/humble/setup.bash
```
2. 检查安装是否成功：
```bash
ls /opt/ros/humble
```
3. 若目录不存在，重新运行安装工具

---

## 高级功能

### 1. rosdep 配置
rosdep 用于自动安装依赖包：
```bash
# 初始化 rosdep
rosdep init

# 更新 rosdep
rosdep update
```

若 rosdep update 失败，可使用一键安装工具的 rosdep 配置功能。

### 2. 工作空间配置
创建 ROS 2 工作空间：
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

配置工作空间环境变量：
```bash
source ~/ros2_ws/install/setup.bash
```

### 3. Docker 环境
一键安装工具支持 Docker 安装，适合隔离开发环境。

---

## 问题反馈

若安装过程中遇到文档未覆盖的问题：
1. 保存终端完整输出日志
2. 访问一键安装工具文档：https://fishros.org.cn/forum/topic/20/
3. 在社区中搜索类似问题或发帖求助

---

## 文档导航
- 一键安装工具文档：https://fishros.org.cn/forum/topic/20/
- ROS 2 官方文档：http://fishros.org/doc/ros2/humble/
- 安装教程：http://fishros.org/doc/ros2/humble/Installation.html
