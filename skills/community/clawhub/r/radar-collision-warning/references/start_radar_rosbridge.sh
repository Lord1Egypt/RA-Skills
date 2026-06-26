#!/bin/bash
# 树莓派 ROS2 雷达预警 + rosbridge 启动脚本
# 用法: bash start_radar_rosbridge.sh
# 确保已复制 radar_collision_warning_node.py 到 ros_ws/src/radar_pkg/src/

set -e

ROS_WS=~/ros_ws
LIDAR_PKG_NAME=ldlidar
RADAR_PKG_NAME=radar_pkg
RADAR_NODE_NAME=radar_collision_warning_node

echo "🔹 加载 ROS2 Jazzy 环境..."
source /opt/ros/jazzy/setup.bash
source $ROS_WS/install/setup.bash

echo "🔹 检查雷达预警节点包..."
if [ ! -d "$ROS_WS/src/$RADAR_PKG_NAME/src/$RADAR_NODE_NAME.py" ] && \
   [ ! -f "$ROS_WS/src/$RADAR_PKG_NAME/src/radar_collision_warning_node.py" ]; then
  echo "⚠️  未找到雷达预警节点，请先将 references/radar_collision_warning_node.py 复制过来"
  echo "    cp references/radar_collision_warning_node.py ~/ros_ws/src/$RADAR_PKG_NAME/src/"
fi

echo "🔹 启动 rosbridge_server（WebSocket :8080）..."
pkill -f rosbridge_websocket || true
ros2 launch rosbridge_server rosbridge_websocket_launch.py \
  > $ROS_WS/rosbridge.log 2>&1 &
echo "✅ rosbridge 已启动，PID=$! 日志: tail -f $ROS_WS/rosbridge.log"

echo "🔹 启动激光雷达节点..."
pkill -f "$LIDAR_PKG_NAME" || true
ros2 run $LIDAR_PKG_NAME $LIDAR_PKG_NAME \
  > $ROS_WS/ldlidar.log 2>&1 &
echo "✅ 激光雷达已启动，PID=$!"

echo "🔹 启动雷达防撞预警节点..."
pkill -f "$RADAR_NODE_NAME" || true
ros2 run $RADAR_PKG_NAME $RADAR_NODE_NAME \
  > $ROS_WS/radar_node.log 2>&1 &
echo "✅ 雷达预警节点已启动，PID=$!"

echo ""
echo "🎉 服务启动完成！"
echo "  rosbridge: ws://$(hostname -I | awk '{print $1}'):8080"
echo "  Service:  /radar_collision_warning"
echo "  Topic:    /scan"
echo ""
echo "🛑 停止: pkill -f rosbridge_websocket && pkill -f $LIDAR_PKG_NAME && pkill -f $RADAR_NODE_NAME"
