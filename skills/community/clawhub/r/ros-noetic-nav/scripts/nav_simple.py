#!/usr/bin/env python3
"""ROS 导航脚本 - 发布航点并监听状态，支持多航点巡航"""

import socket, json, math, sys, argparse, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from waypoints_manager import load_waypoints, get_waypoint


class NavWithStatus:
    """导航客户端 - 发布航点并监听状态"""
    
    def __init__(self, host='localhost', port=9090):
        self.host, self.port = host, port
    
    def _connect(self):
        """建立连接"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((self.host, self.port))
        return sock
    
    def publish_goal(self, sock, x, y, yaw_deg=0):
        """发布导航目标"""
        yaw = math.radians(yaw_deg)
        msg = json.dumps({
            "op": "publish",
            "topic": "/move_base_simple/goal",
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
        """订阅 move_base 状态话题"""
        sock.send((json.dumps({"op": "subscribe", "topic": "/move_base/status"}) + '\n').encode())
    
    def monitor_single_status(self, sock, timeout=180):
        """监听单个航点的状态"""
        print("   📡 开始监听导航状态...")
        
        start_time = time.time()
        tracked_goal = None  # (secs, nsecs, id)
        seen_active = False

        def _goal_key(status_item):
            goal_id = status_item.get('goal_id', {})
            stamp = goal_id.get('stamp', {})
            secs = int(stamp.get('secs', 0) or 0)
            nsecs = int(stamp.get('nsecs', 0) or 0)
            gid = str(goal_id.get('id', '') or '')
            return (secs, nsecs, gid)

        def _same_goal(status_item, goal_key):
            if goal_key is None:
                return False
            s_secs, s_nsecs, s_gid = _goal_key(status_item)
            g_secs, g_nsecs, g_gid = goal_key
            if s_secs != g_secs or s_nsecs != g_nsecs:
                return False
            # 当 id 可用时必须一致，避免同秒历史目标混淆
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
                        if '/move_base/status' in msg.get('topic', ''):
                            status_list = msg.get('msg', {}).get('status_list', [])
                            if not status_list:
                                continue

                            # 每帧都选时间戳最新的 goal 作为当前跟踪目标
                            newest = max(status_list, key=_goal_key)
                            newest_key = _goal_key(newest)
                            if tracked_goal is None or newest_key[:2] > tracked_goal[:2] or (newest_key[:2] == tracked_goal[:2] and newest_key[2] != tracked_goal[2]):
                                tracked_goal = newest_key
                                seen_active = False
                                print(f"   🆕 检测到新导航目标 (stamp={tracked_goal[0]}.{tracked_goal[1]:09d})")

                            for status in status_list:
                                if not _same_goal(status, tracked_goal):
                                    continue

                                st = status.get('status', -1)

                                # 先看到 ACTIVE，再接受 SUCCEEDED，避免旧成功状态误触发
                                if st == 1:  # ACTIVE
                                    if not seen_active:
                                        print(f"   🚗 导航进行中...")
                                    seen_active = True
                                elif st == 3:  # SUCCEEDED
                                    if not seen_active:
                                        print("   ⏭️ 忽略未激活目标的 SUCCEEDED（疑似历史状态）")
                                        continue
                                    print(f"   ✅ 导航成功完成!")
                                    return True, "SUCCEEDED"
                                elif st == 4:  # ABORTED
                                    print(f"   ❌ 导航被中止 (ABORTED)")
                                    return False, "ABORTED"
                                elif st == 5:  # REJECTED
                                    print(f"   ⚠️ 导航被拒绝 (REJECTED)")
                                    return False, "REJECTED"
                                elif st == 2:  # PREEMPTED
                                    print(f"   🔄 导航被抢占 (PREEMPTED)")
                                elif st == 6:  # PREEMPTING
                                    pass  # 内部状态，不显示
                                elif st == 7:  # RECALLING
                                    pass  # 内部状态，不显示
                                elif st == 8:  # RECALLED
                                    print(f"   ↩️ 导航被召回 (RECALLED)")
                                elif st == 9:  # LOST
                                    print(f"   🔍 导航目标丢失 (LOST)")
                                    return False, "LOST"
                    except:
                        pass
            except socket.timeout:
                continue
        
        print(f"   ⏱️ 监听超时 ({timeout}秒)")
        return False, "TIMEOUT"
    
    def go_single(self, waypoint_name, timeout=180):
        """导航到单个航点并监听状态"""
        wp = get_waypoint(waypoint_name)
        if not wp:
            print(f"❌ 未找到航点: {waypoint_name}")
            return False, "NOT_FOUND"
        
        print(f"📍 发布导航目标 → {waypoint_name}")
        print(f"   坐标: ({wp['x']:.2f}, {wp['y']:.2f}) 朝向 {wp.get('yaw', 0):.1f}°")
        
        try:
            # 先订阅状态，避免发布后才订阅导致读到历史状态
            sock = self._connect()
            self.subscribe_status(sock)

            # 清空订阅建立前后的残留数据
            sock.settimeout(0.5)
            for _ in range(3):
                try:
                    sock.recv(65536)
                except:
                    pass

            # 发布目标
            self.publish_goal(sock, wp['x'], wp['y'], wp.get('yaw', 0))
            print("✅ 目标已发布")
            
            # 监听状态
            success, status = self.monitor_single_status(sock, timeout)
            sock.close()
            return success, status
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False, "ERROR"
    
    def go_multiple(self, waypoint_names, timeout_per_wp=180):
        """多航点依次导航"""
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
                # 先订阅状态，避免发布后才订阅导致读到历史状态
                sock = self._connect()
                self.subscribe_status(sock)

                # 清空订阅建立前后的残留数据
                sock.settimeout(0.5)
                for _ in range(3):
                    try:
                        sock.recv(65536)
                    except:
                        pass

                # 发布目标
                self.publish_goal(sock, wp['x'], wp['y'], wp.get('yaw', 0))
                print("   ✅ 目标已发布")
                
                # 监听状态
                success, status = self.monitor_single_status(sock, timeout_per_wp)
                sock.close()
                
                results.append({"name": wp_name, "success": success, "status": status})
                
                # 如果失败，停止巡航
                if not success:
                    print(f"\n⚠️ 巡航中断: {wp_name} 导航失败 ({status})")
                    break
                
                # 如果还有下一个航点，等待一下再继续
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
    parser = argparse.ArgumentParser(description='ROS 导航 - 发布航点并监听状态，支持多航点巡航')
    sub = parser.add_subparsers(dest='mode')
    
    # cmd 命令模式
    c = sub.add_parser('cmd', help='命令模式: "去 <地点>" 或 "去 <地点1> <地点2> ..."')
    c.add_argument('command', help='命令，如: "去卧室" 或 "去卧室 餐厅 书房"')
    c.add_argument('--timeout', type=int, default=180, help='每个航点的超时时间(秒)')
    
    # named 命令
    n = sub.add_parser('named', help='导航到命名航点')
    n.add_argument('name', help='航点名称')
    n.add_argument('--timeout', type=int, default=180, help='超时时间(秒)')
    
    # cruise 命令
    cr = sub.add_parser('cruise', help='多航点巡航')
    cr.add_argument('names', nargs='+', help='航点名称列表')
    cr.add_argument('--timeout', type=int, default=180, help='每个航点的超时时间(秒)')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        return
    
    nav = NavWithStatus()
    
    if args.mode == 'cmd':
        cmd = args.command.strip()
        if cmd.startswith('去'):
            places = cmd[1:].strip().split()
            if len(places) == 1:
                # 单个航点
                nav.go_single(places[0], args.timeout)
            else:
                # 多个航点
                nav.go_multiple(places, args.timeout)
        else:
            print(f"❌ 未知命令格式: {cmd}")
            print("   正确格式: 去 <地点> 或 去 <地点1> <地点2> ...")
            print("   例如: 去卧室")
            print("   例如: 去卧室 餐厅 书房")
    
    elif args.mode == 'named':
        nav.go_single(args.name, args.timeout)
    
    elif args.mode == 'cruise':
        nav.go_multiple(args.names, args.timeout)


if __name__ == '__main__':
    main()
