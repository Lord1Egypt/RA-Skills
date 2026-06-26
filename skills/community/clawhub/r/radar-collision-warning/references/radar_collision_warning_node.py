#!/usr/bin/env python3
"""
雷达防撞预警节点 — ROS2 Python 节点

订阅 /scan (LaserScan)，计算最近有效距离，通过 Service 供外部调用。

使用方法：
  # 赋予执行权限
  chmod +x radar_collision_warning_node.py
  
  # 运行节点
  ros2 run radar_collision_warning radar_collision_warning_node

Service:
  名称: /radar_collision_warning
  类型: std_srvs/srv/Trigger
  请求: 空（Trigger 无参数）
  响应:
    success: bool   — true=危险, false=安全
    message: str    — 中文描述信息

话题:
  订阅: /scan (sensor_msgs/LaserScan) — 激光雷达数据
  发布（预留）: /flight_control_cmd (std_msgs/String) — 飞控指令
"""

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_srvs.srv import Trigger
from std_msgs.msg import String


class RadarCollisionWarning(Node):
    def __init__(self):
        super().__init__('radar_collision_warning_node')

        # ========== 参数 ==========
        self.declare_parameter('collision_threshold', 0.05)  # 5cm
        self.collision_threshold = self.get_parameter('collision_threshold').value
        # ==========================

        # 订阅激光雷达 /scan 话题
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self._scan_callback,
            qos_profile=10
        )

        # 当前最近有效距离（米）和对应角度
        self.latest_min_distance = float('inf')
        self.latest_min_angle = 0.0

        # Service 调用计数（用于调试）
        self._call_count = 0

        # 创建 ROS2 Service（供外部 WebSocket/rosbridge 调用）
        self.warning_service = self.create_service(
            Trigger,
            'radar_collision_warning',   # → 全局名 /radar_collision_warning
            self._service_callback
        )

        # 预留：飞控指令发布器
        self.flight_pub = self.create_publisher(String, 'flight_control_cmd', qos_profile=10)

        self.get_logger().info(
            f"雷达防撞预警节点已启动，碰撞阈值: {self.collision_threshold * 100:.1f}cm"
        )

    # ──────────────────────────────────────────────
    def _scan_callback(self, msg: LaserScan):
        """ LaserScan 回调：过滤无效值，找到最近有效距离及角度 """
        range_min = msg.range_min
        range_max = msg.range_max

        # 角度分辨率
        angle_increment = msg.angle_increment
        angle_min = msg.angle_min

        min_dist = float('inf')
        min_angle = 0.0

        for i, r in enumerate(msg.ranges):
            # 过滤: inf, nan, 超出物理范围
            if math.isfinite(r) and range_min <= r <= range_max:
                if r < min_dist:
                    min_dist = r
                    # 计算该点的角度（弧度转度）
                    min_angle = math.degrees(angle_min + i * angle_increment)

        self.latest_min_distance = min_dist
        self.latest_min_angle = min_angle

        # DEBUG: 每次 scan 回调打印一次
        if min_dist < float('inf'):
            self.get_logger().debug(
                f"scan 回调: 最近障碍物 {min_dist*100:.1f}cm @ {min_angle:.1f}°"
            )
    # ──────────────────────────────────────────────

    # ──────────────────────────────────────────────
    def _service_callback(self, request, response):
        """ Service 回调：被外部调用时返回当前预警状态 """
        self._call_count += 1
        dist = self.latest_min_distance
        threshold = self.collision_threshold

        if dist < threshold:
            response.success = True
            response.message = (
                f"⚠️ 碰撞危险！距离: {dist*100:.1f}cm "
                f"@ {self.latest_min_angle:.1f}° "
                f"(< {threshold*100:.1f}cm)"
            )

            # 预留：发布飞控避障指令（如"stop"）
            # cmd = String()
            # cmd.data = "stop"
            # self.flight_pub.publish(cmd)

            self.get_logger().warn(
                f"[#{self._call_count}] {response.message} | "
                f"scan累积最小: {dist*100:.1f}cm"
            )
        else:
            response.success = False
            if dist < float('inf'):
                response.message = f"✅ 安全，最近障碍物: {dist*100:.1f}cm @ {self.latest_min_angle:.1f}°"
            else:
                response.message = "⚠️ 尚未收到有效 scan 数据"
            self.get_logger().info(f"[#{self._call_count}] {response.message}")

        return response
    # ──────────────────────────────────────────────


def main(args=None):
    rclpy.init(args=args)
    node = RadarCollisionWarning()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
