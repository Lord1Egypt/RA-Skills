# ROS Noetic Navigation - Cartographer Edition

专为使用Cartographer定位的ROS Noetic导航系统设计。通过TF获取位姿，通过rosbridge与move_base交互。

## 🚨 重要：前置条件

**必须启动 rosbridge_server**：
```bash
source /opt/ros/noetic/setup.bash
roslaunch rosbridge_server rosbridge_tcp.launch
```

**Cartographer导航系统**：
```bash
# 示例启动命令（根据实际项目调整）
roslaunch robot_navigation navigation_with_cartographer_cpp.launch
```

如果没有运行rosbridge，所有导航命令都会失败！

## 与原版（AMCL）的区别

| 特性 | 原版 (AMCL) | Cartographer版 |
|------|------------|----------------|
| 定位算法 | AMCL | **Cartographer** |
| 位姿获取 | `/amcl_pose` Topic | **TF变换** |
| 地图格式 | `.pgm` + `.yaml` | `.pbstream` |
| 重定位 | 自动 | 需手动设置初始位姿 |

## 文件结构

```
ros-noetic-nav-cartographer/
├── SKILL.md                      # 本说明文档
├── waypoints.json                # Cartographer专用航点
└── scripts/
    ├── waypoints_manager.py      # 航点管理
    ├── nav.py                    # 导航脚本（单点+巡航）
    └── get_pose_tf.py            # 通过TF获取位姿
```

## 配置

在 `TOOLS.md` 中添加：

```markdown
### ROS Noetic Navigation - Cartographer

- workspace: ~/robot5  # 根据实际项目调整
- rosbridge_host: localhost
- rosbridge_port: 9090
- pose_tf_target: base_link      # 小车坐标系
- pose_tf_source: map            # 地图坐标系
- waypoints_file: ~/.openclaw/workspace/skills/ros-noetic-nav-cartographer/waypoints.json
- map_file: ~/robot5/src/robot_navigation/maps/my_map.pbstream
```

## 使用方法

### 1. 查看当前位置（TF方式）

```bash
# 基本查询
python3 scripts/get_pose_tf.py

# 指定坐标系
python3 scripts/get_pose_tf.py --target-frame base_footprint --source-frame map

# JSON格式输出
python3 scripts/get_pose_tf.py --json
```

### 2. 航点管理

```bash
# 列出所有航点
python3 scripts/waypoints_manager.py list

# 添加航点
python3 scripts/waypoints_manager.py add 充电座 --x 0.0 --y 0.0 --yaw 0
python3 scripts/waypoints_manager.py add 客厅 --x 3.0 --y 2.0 --yaw 90

# 获取航点
python3 scripts/waypoints_manager.py get 客厅

# 删除航点
python3 scripts/waypoints_manager.py remove 客厅
```

### 3. 导航

#### 单点导航

```bash
# 使用命名航点
python3 scripts/nav.py goto 客厅

# 自然语言命令
python3 scripts/nav.py cmd "去客厅"
```

#### 多航点巡航

```bash
# 巡航多个航点
python3 scripts/nav.py cruise 卧室 餐厅 书房

# 自然语言命令
python3 scripts/nav.py cmd "去卧室 餐厅 书房"
```

#### 自定义rosbridge地址

```bash
python3 scripts/nav.py goto 客厅 --host 192.168.1.100 --port 9090
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | rosbridge主机 | localhost |
| `--port` | rosbridge端口 | 9090 |
| `--timeout` | 导航超时(秒) | 180 |
| `--target-frame` | TF目标坐标系（小车） | base_link |
| `--source-frame` | TF源坐标系（地图） | map |

## 首次设置流程

1. **启动rosbridge**：
   ```bash
   roslaunch rosbridge_server rosbridge_tcp.launch
   ```

2. **启动Cartographer导航**：
   ```bash
   roslaunch robot_navigation navigation_with_cartographer_cpp.launch
   ```

3. **在RViz中手动重定位**（2D Pose Estimate）

4. **驾驶小车到目标位置**，记录航点：
   ```bash
   # 获取当前位置
   python3 scripts/get_pose_tf.py
   
   # 保存航点
   python3 scripts/waypoints_manager.py add 客厅 --x <x值> --y <y值> --yaw <角度>
   ```

5. **测试导航**：
   ```bash
   python3 scripts/nav.py goto 客厅
   ```

## 依赖

- Python 3
- ROS Noetic
- rosbridge_server (TCP, 端口9090)
- tf2_ros, tf (ROS Python库)
- Cartographer ROS

## 注意事项

1. **rosbridge检查**：每次使用前确保rosbridge已启动
2. **重定位**：Cartographer需要手动设置初始位姿（RViz的2D Pose Estimate）
3. **TF延迟**：TF变换可能有短暂延迟，get_pose_tf.py会等待最多5秒
4. **坐标系**：确保TF树中有 `map -> base_link` 变换
5. **航点独立性**：Cartographer和AMCL的航点文件相互独立，因为地图坐标系不同

## 故障排查

### rosbridge连接失败
```bash
# 检查rosbridge是否运行
curl http://localhost:9090

# 启动rosbridge
roslaunch rosbridge_server rosbridge_tcp.launch
```

### TF获取失败
```bash
# 检查TF树
rosrun tf view_frames

# 检查Cartographer是否正常发布TF
rostopic echo /tf

# 检查话题
rostopic list | grep cartographer
```

### 导航无响应
```bash
# 检查move_base状态
rostopic echo /move_base/status

# 检查目标是否发布
rostopic echo /move_base_simple/goal
```

## 适用场景

- 使用Cartographer进行SLAM和定位的项目
- 需要高精度定位的机器人
- 大规模环境下的导航
- 需要保存和加载地图的长期运行项目
