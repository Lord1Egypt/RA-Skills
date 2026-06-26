#!/usr/bin/env python3
"""读取ROS小车当前位置 (/amcl_pose话题)"""

import socket
import json
import math
import argparse

def get_pose(host='localhost', port=9090, topic='/amcl_pose'):
    """连接rosbridge并读取小车位置"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    try:
        sock.connect((host, port))
        
        # 订阅话题
        subscribe_msg = json.dumps({"op": "subscribe", "topic": topic})
        sock.send((subscribe_msg + '\n').encode())
        
        # 接收一条消息
        data = sock.recv(4096).decode()
        for line in data.strip().split('\n'):
            if line:
                msg = json.loads(line)
                if msg.get('op') == 'publish' and msg.get('topic') == topic:
                    pose = msg['msg']['pose']['pose']
                    position = pose['position']
                    orientation = pose['orientation']
                    
                    # 计算yaw角度
                    yaw = math.atan2(
                        2 * (orientation['w'] * orientation['z'] + orientation['x'] * orientation['y']),
                        1 - 2 * (orientation['y']**2 + orientation['z']**2)
                    )
                    yaw_deg = math.degrees(yaw)
                    
                    return {
                        'x': position['x'],
                        'y': position['y'],
                        'z': position['z'],
                        'yaw_deg': yaw_deg,
                        'orientation': orientation
                    }
    finally:
        sock.close()
    
    return None

def main():
    parser = argparse.ArgumentParser(description='读取ROS小车位置')
    parser.add_argument('--host', default='localhost', help='rosbridge主机')
    parser.add_argument('--port', type=int, default=9090, help='rosbridge端口')
    parser.add_argument('--topic', default='/amcl_pose', help='位置话题')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    args = parser.parse_args()
    
    pose = get_pose(args.host, args.port, args.topic)
    
    if pose:
        if args.json:
            print(json.dumps(pose, indent=2))
        else:
            print(f"📍 小车位置: x={pose['x']:.3f}m, y={pose['y']:.3f}m, z={pose['z']:.3f}m")
            print(f"🧭 朝向角度: {pose['yaw_deg']:.1f}°")
    else:
        print("❌ 无法读取位置数据")
        exit(1)

if __name__ == '__main__':
    main()
