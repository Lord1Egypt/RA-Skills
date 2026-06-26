#!/usr/bin/env python3
"""读取Robot5小车当前位置 - 通过TF获取 (Cartographer)"""

import argparse
import rospy
import tf2_ros
import tf
from geometry_msgs.msg import TransformStamped

def get_pose_from_tf(target_frame='base_link', source_frame='map', timeout=5.0):
    """
    通过TF获取小车位置
    
    Args:
        target_frame: 小车坐标系，通常是 'base_link' 或 'base_footprint'
        source_frame: 地图坐标系，通常是 'map'
        timeout: 等待TF的超时时间
    
    Returns:
        dict: 包含位置(x,y,z)和朝向(yaw_deg)的字典，失败返回None
    """
    rospy.init_node('get_pose_tf_node', anonymous=True)
    
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    
    try:
        # 等待TF可用
        rospy.loginfo(f"等待TF变换: {source_frame} -> {target_frame}...")
        transform = tf_buffer.lookup_transform(
            source_frame,      # 目标坐标系
            target_frame,      # 源坐标系（小车）
            rospy.Time(0),     # 最新时间
            rospy.Duration(timeout)
        )
        
        # 提取位置和四元数
        trans = transform.transform.translation
        rot = transform.transform.rotation
        
        # 四元数转欧拉角（获取yaw）
        quaternion = [rot.x, rot.y, rot.z, rot.w]
        euler = tf.transformations.euler_from_quaternion(quaternion)
        roll, pitch, yaw = euler
        yaw_deg = yaw * 180.0 / 3.14159
        
        return {
            'x': trans.x,
            'y': trans.y,
            'z': trans.z,
            'yaw_rad': yaw,
            'yaw_deg': yaw_deg,
            'frame': target_frame,
            'reference': source_frame
        }
        
    except (tf2_ros.LookupException, 
            tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException) as e:
        rospy.logerr(f"获取TF失败: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='通过TF读取Robot5小车位置 (Cartographer)'
    )
    parser.add_argument('--target-frame', default='base_link', 
                        help='小车坐标系，默认: base_link')
    parser.add_argument('--source-frame', default='map',
                        help='地图坐标系，默认: map')
    parser.add_argument('--timeout', type=float, default=5.0,
                        help='TF等待超时时间(秒)')
    parser.add_argument('--json', action='store_true', 
                        help='输出JSON格式')
    args = parser.parse_args()
    
    pose = get_pose_from_tf(args.target_frame, args.source_frame, args.timeout)
    
    if pose:
        if args.json:
            import json
            # 移除不可序列化的对象
            output = {k: v for k, v in pose.items() if k not in ['quaternion']}
            print(json.dumps(output, indent=2))
        else:
            print(f"📍 小车位置 ({pose['frame']} 相对于 {pose['reference']}):")
            print(f"   x: {pose['x']:.3f} m")
            print(f"   y: {pose['y']:.3f} m")
            print(f"   z: {pose['z']:.3f} m")
            print(f"🧭 朝向: {pose['yaw_deg']:.1f}°")
    else:
        print("❌ 无法获取TF变换，请检查:")
        print("   1. Cartographer是否已启动")
        print("   2. TF树是否正常发布 (rosrun tf view_frames)")
        print("   3. 坐标系名称是否正确")
        exit(1)

if __name__ == '__main__':
    main()
