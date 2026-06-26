#!/usr/bin/env python3
"""Robot5 导航脚本 - 发布航点并监听状态，支持多航点巡航

通过rosbridge与Robot5的move_base交互
"""

import socket
import json
import math
import sys
import argparse
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from waypoints_manager import load_waypoints, get_waypoint


class Robot5Navigator:
    """Robot5导航客户端 - 发布航点并监听状态"""
    
    # Robot5默认配置
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 9090
    GOAL_TOPIC = '/move_base_simple/goal'
    STATUS_TOPIC = '/move_base/status'
    
    def __init__(self, host=None, port=None):
        self.host = host or self.DEFAULT_HOST
        self.port = port or self.DEFAULT_PORT
    
    def _connect(self):
        """建立rosbridge连接"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((self.host, self.port))
        return sock
    
    def publish_goal(self, sock, x, y, yaw_deg=0):
        """发布导航目标到move_base_simple/goal"""
        yaw = math.radians(yaw_deg)
        msg = json.dumps({
            "op": "publish",
            "topic": self.GOAL_TOPIC,
            "msg": {
                "header": {"frame_id": "map"},
                "pose": {
                    "position": {"x": float(x), "y": float(y), "z": 0.0},
                    "orientation": {
                        "x": 0, "y": 0,
                        "z": float(math.sin(yaw / 2)),
                        "w": float(math.cos(yaw / 2))
                    }
                }
            }
        })
        sock.send((msg + '\n').encode())
        return sock
    
    def subscribe_status(self, sock):
        """订阅move_base状态话题"""
        sub_msg = json.dumps({
            "op": "subscribe",
            "topic": self.STATUS_TOPIC
        })
        sock.send((sub_msg + '\n').encode())
    
    def monitor_single_status(self, sock, timeout=180):
        """
        监听单个航点的导航状态
        
        Returns:
            (success: bool, status: str)
        """
        print("   📡 开始监听导航状态...")
        
        start_time = time.time()
        tracked_goal = None
        seen_active = False
        
        def _goal_key(status_item):
            """提取goal唯一标识"""
            goal_id = status_item.get('goal_id', {})
            stamp = goal_id.get('stamp', {})
            secs = int(stamp.get('secs', 0) or 0)
            nsecs = int(stamp.get('nsecs', 0) or 0)
            gid = str(goal_id.get('id', '') or '')
            return (secs, nsecs, gid)
        
        def _same_goal(status_item, goal_key):
            """判断状态是否属于当前跟踪的目标"""
            if goal_key is None:
                return False
            s_secs, s_nsecs, s_gid = _goal_key(status_item)
            g_secs, g_nsecs, g_gid = goal_key
            if s_secs != g_secs or s_nsecs != g_nsecs:
                return False
            if g_gid:
                return s_gid == g_gid
            return True
        
        while time.time() - start_time < timeout:
            remaining = timeout - (time.time() - start_time)
            if remaining <= 0:
                break
            
            sock.settimeout(min(5, remaining))
            try:
                data = sock.recv(65536)
                for line in data.decode('utf-8', errors='ignore').strip().split('\n'):
                    s = line.find('{')
                    if s < 0:
                        continue
                    try:
                        msg = json.loads(line[s:])
                        if self.STATUS_TOPIC in msg.get('topic', ''):
                            status_list = msg.get('msg', {}).get('status_list', [])
                            if not status_list:
                                continue
                            
                            # 选时间戳最新的goal作为当前跟踪目标
                            newest = max(status_list, key=_goal_key)
                            newest_key = _goal_key(newest)
                            
                            if tracked_goal is None or \
                               newest_key[:2] > tracked_goal[:2] or \
                               (newest_key[:2] == tracked_goal[:2] and newest_key[2] != tracked_goal[2]):
                                tracked_goal = newest_key
                                seen_active = False
                                print(f"   🆕 检测到新导航目标")
                            
                            for status in status_list:
                                if not _same_goal(status, tracked_goal):
                                    continue
                                
                                st = status.get('status', -1)
                                
                                if st == 1:  # ACTIVE
                                    if not seen_active:
                                        print(f"   🚗 导航进行中...")
                                    seen_active = True
                                elif st == 3:  # SUCCEEDED
                                    if not seen_active:
                                        continue  # 忽略未激活目标的SUCCEEDED
                                    print(f"   ✅ 导航成功完成!")
                                    return True, "SUCCEEDED"
                                elif st == 4:  # ABORTED
                                    print(f"   ❌ 导航被中止 (ABORTED)")
                                    return False, "ABORTED"
                                elif st == 5:  # REJECTED
                                    print(f"   ⚠️ 导航被拒绝 (REJECTED)")
                                    return False, "REJECTED"
                                elif st == 8:  # RECALLED
                                    print(f"   ↩️ 导航被召回 (RECALLED)")
                                elif st == 9:  # LOST
                                    print(f"   🔍 导航目标丢失 (LOST)")
                                    return False, "LOST"
                    except Exception:
                        pass
            except socket.timeout:
                continue
        
        print(f"   ⏱️ 监听超时 ({timeout}秒)")
        return False, "TIMEOUT"
    
    def goto_waypoint(self, waypoint_name, timeout=180):
        """导航到单个命名航点"""
        wp = get_waypoint(waypoint_name)
        if not wp:
            print(f"❌ 未找到航点: {waypoint_name}")
            return False, "NOT_FOUND"
        
        print(f"📍 发布导航目标 → {waypoint_name}")
        print(f"   坐标: ({wp['x']:.2f}, {wp['y']:.2f}) 朝向 {wp.get('yaw', 0):.1f}°")
        
        try:
            sock = self._connect()
            self.subscribe_status(sock)
            
            # 清空残留数据
            sock.settimeout(0.5)
            for _ in range(3):
                try:
                    sock.recv(65536)
                except:
                    pass
            
            self.publish_goal(sock, wp['x'], wp['y'], wp.get('yaw', 0))
            print("✅ 目标已发布")
            
            success, status = self.monitor_single_status(sock, timeout)
            sock.close()
            return success, status
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False, "ERROR"
    
    def cruise_waypoints(self, waypoint_names, timeout_per_wp=180):
        """多航点依次巡航"""
        print("=" * 50)
        print(f"🚗 多航点巡航任务  共 {len(waypoint_names)} 个航点")
        print("=" * 50)
        
        results = []
        total_start = time.time()
        
        for i, wp_name in enumerate(waypoint_names):
            wp = get_waypoint(wp_name)
            if not wp:
                print(f"\n❌ 未找到航点: {wp_name}，跳过")
                results.append({"name": wp_name, "success": False, "status": "NOT_FOUND"})
                continue
            
            print(f"\n📍 第 {i+1}/{len(waypoint_names)} 站: {wp_name}")
            print(f"   目标: ({wp['x']:.2f}, {wp['y']:.2f}) 朝向 {wp.get('yaw', 0):.1f}°")
            
            try:
                sock = self._connect()
                self.subscribe_status(sock)
                
                # 清空残留数据
                sock.settimeout(0.5)
                for _ in range(3):
                    try:
                        sock.recv(65536)
                    except:
                        pass
                
                self.publish_goal(sock, wp['x'], wp['y'], wp.get('yaw', 0))
                print("   ✅ 目标已发布")
                
                success, status = self.monitor_single_status(sock, timeout_per_wp)
                sock.close()
                
                results.append({"name": wp_name, "success": success, "status": status})
                
                if not success:
                    print(f"\n⚠️ 巡航中断: {wp_name} 导航失败 ({status})")
                    break
                
                if i < len(waypoint_names) - 1:
                    print(f"   ⏳ 准备下一站...")
                    time.sleep(1)
                    
            except Exception as e:
                print(f"   ❌ 错误: {e}")
                results.append({"name": wp_name, "success": False, "status": "ERROR"})
                break
        
        # 总结
        elapsed = time.time() - total_start
        success_count = sum(1 for r in results if r["success"])
        
        print(f"\n{'=' * 50}")
        print(f"🎉 巡航完成: {success_count}/{len(waypoint_names)} 成功  耗时 {elapsed:.0f}秒")
        for r in results:
            icon = "✅" if r["success"] else "❌"
            print(f"   {icon} {r['name']} → {r['status']}")
        print(f"{'=' * 50}")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Robot5 导航 - 支持单点和多航点巡航'
    )
    sub = parser.add_subparsers(dest='mode')
    
    # cmd 命令模式（自然语言）
    c = sub.add_parser('cmd', help='命令模式: "去 <地点>" 或 "去 <地点1> <地点2> ..."')
    c.add_argument('command', help='命令，如: "去卧室" 或 "去卧室 餐厅"')
    c.add_argument('--timeout', type=int, default=180, help='每个航点超时时间(秒)')
    c.add_argument('--host', default='localhost', help='rosbridge主机')
    c.add_argument('--port', type=int, default=9090, help='rosbridge端口')
    
    # goto 命令
    g = sub.add_parser('goto', help='导航到命名航点')
    g.add_argument('name', help='航点名称')
    g.add_argument('--timeout', type=int, default=180, help='超时时间(秒)')
    g.add_argument('--host', default='localhost', help='rosbridge主机')
    g.add_argument('--port', type=int, default=9090, help='rosbridge端口')
    
    # cruise 命令
    cr = sub.add_parser('cruise', help='多航点巡航')
    cr.add_argument('names', nargs='+', help='航点名称列表')
    cr.add_argument('--timeout', type=int, default=180, help='每个航点超时时间(秒)')
    cr.add_argument('--host', default='localhost', help='rosbridge主机')
    cr.add_argument('--port', type=int, default=9090, help='rosbridge端口')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        return
    
    nav = Robot5Navigator(
        host=getattr(args, 'host', 'localhost'),
        port=getattr(args, 'port', 9090)
    )
    
    if args.mode == 'cmd':
        cmd = args.command.strip()
        if cmd.startswith('去'):
            places = cmd[1:].strip().split()
            if len(places) == 1:
                nav.goto_waypoint(places[0], args.timeout)
            else:
                nav.cruise_waypoints(places, args.timeout)
        else:
            print(f"❌ 未知命令格式: {cmd}")
            print('   正确格式: 去 <地点> 或 去 <地点1> <地点2> ...')
    
    elif args.mode == 'goto':
        nav.goto_waypoint(args.name, args.timeout)
    
    elif args.mode == 'cruise':
        nav.cruise_waypoints(args.names, args.timeout)


if __name__ == '__main__':
    main()
