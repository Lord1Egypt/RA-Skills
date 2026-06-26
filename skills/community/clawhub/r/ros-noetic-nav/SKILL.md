# ROS Noetic Navigation Skill

通过rosbridge与ROS Noetic导航系统交互，支持地图读取、航点管理、单点导航和多航点巡航。适用于使用AMCL定位的ROS导航系统。

## 🚨 重要：前置条件

**必须启动 rosbridge_server**：
```bash
source /opt/ros/noetic/setup.bash
roslaunch rosbridge_server rosbridge_tcp.launch
```

如果没有运行rosbridge，所有导航命令都会失败！

## 文件结构

```
ros-noetic-nav/
├── SKILL.md                      # 说明文档
├── waypoints.json                # 保存的命名航点
└── scripts/
    ├── read_map.py               # 读取解析地图
    ├── waypoints_manager.py      # 航点管理
    ├── nav.py                    # 导航脚本（单点+巡航）
    ├── get_pose.py               # 读取小车位置
    └── publish_goal.py           # 发布单个航点
```

## 配置

在 `TOOLS.md` 中添加：

```markdown
### ROS Noetic Navigation (AMCL)

- rosbridge_host: localhost
- rosbridge_port: 9090
- pose_topic: /amcl_pose
- goal_topic: /move_base_simple/goal
- waypoints_file: ~/.openclaw/workspace/skills/ros-noetic-nav/waypoints.json
- map_path: ~/catkin_ws/src/wpr_simulation/maps/map.pgm
```

## 使用方法

### 1. 读取地图

```bash
# 基本读取
python3 scripts/read_map.py --map /path/to/map.pgm

# 输出四象限航点
python3 scripts/read_map.py --map /path/to/map.pgm --quadrants

# JSON格式输出
python3 scripts/read_map.py --map /path/to/map.pgm --json
```

### 2. 航点管理

```bash
# 列出所有航点
python3 scripts/waypoints_manager.py list

# 保存航点
python3 scripts/waypoints_manager.py add 客厅 --x 3.0 --y 2.0 --yaw 0
python3 scripts/waypoints_manager.py add 卧室 --x -2.5 --y -3.0 --yaw 90
python3 scripts/waypoints_manager.py add 厨房 --x 1.5 --y -2.0

# 获取航点
python3 scripts/waypoints_manager.py get 客厅

# 删除航点
python3 scripts/waypoints_manager.py remove 厨房

# 导出/导入
python3 scripts/waypoints_manager.py export --output backup.json
python3 scripts/waypoints_manager.py import --input backup.json
```

### 3. 导航

#### 单点导航

```bash
# 直接坐标
python3 scripts/nav.py goto --x 3.0 --y 2.0 --yaw 0 --name "客厅门口"

# 命名航点
python3 scripts/nav.py named 客厅
```

#### 多航点巡航

```bash
# 使用保存的命名航点
python3 scripts/nav.py cruise --waypoints 客厅 卧室 厨房

# 使用坐标列表
python3 scripts/nav.py cruise --coords 3.0,2.0 -2.5,-3.0 1.5,-2.0
```

### 4. 基础功能

```bash
# 读取当前位置
python3 scripts/get_pose.py

# 发布单个航点
python3 scripts/publish_goal.py --x 3.0 --y 2.0 --yaw 0
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | rosbridge主机 | localhost |
| `--port` | rosbridge端口 | 9090 |
| `--thresh` | 到达阈值 (米) | 1.0 |
| `--timeout` | 导航超时 (秒) | 60 |
| `--map` | 地图文件路径 | 必填 |
| `--yaml` | YAML配置文件 | 自动检测 |
| `--wp-file` | 航点文件路径 | 默认waypoints.json |

## 示例工作流

### 首次设置

```bash
# 1. 启动rosbridge
roslaunch rosbridge_server rosbridge_tcp.launch

# 2. 读取地图，了解环境
python3 scripts/read_map.py --map ~/catkin_ws/src/wpr_simulation/maps/map.pgm --quadrants

# 3. 保存常用航点
python3 scripts/waypoints_manager.py add 充电座 --x 0.0 --y 0.0
python3 scripts/waypoints_manager.py add 客厅 --x 3.0 --y 2.0
python3 scripts/waypoints_manager.py add 卧室 --x -2.5 --y -3.0

# 4. 测试导航
python3 scripts/nav.py named 客厅
```

### 日常使用

```bash
# 去某个地方
python3 scripts/nav.py named 客厅

# 巡航多个地方
python3 scripts/nav.py cruise --waypoints 客厅 卧室 充电座
```

## 依赖

- Python 3
- Pillow (`pip install Pillow`)
- NumPy (`pip install numpy`)
- rosbridge_server (TCP, 默认端口9090)

## 注意事项

1. **rosbridge检查**：每次使用前确保rosbridge已启动
2. **航点可达性**：发布的航点需要在costmap的可通行区域内
3. **坐标系统**：使用ROS世界坐标系，原点在地图左下角
4. **朝向角度**：使用度数，0°=正东，90°=正北，180°=正西，-90°=正南
5. **导航失败**：如果目标不可达，尝试更近的中间点

## 故障排查

### rosbridge连接失败
```bash
# 检查rosbridge是否运行
curl http://localhost:9090

# 启动rosbridge
roslaunch rosbridge_server rosbridge_tcp.launch
```

### 导航无响应
```bash
# 检查move_base状态
rostopic echo /move_base/status

# 检查目标是否发布
rostopic echo /move_base_simple/goal
```

## 扩展

可以扩展的功能：
- 从配置文件批量加载航点
- 支持相对位置（"充电座左边2米"）
- 路径规划和避障状态查询
- 与语音助手集成
