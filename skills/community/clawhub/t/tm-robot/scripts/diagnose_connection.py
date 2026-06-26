#!/usr/bin/env python3
"""
达明机器人连接诊断脚本
检查网络、端口、机器人状态等
"""

import socket
import asyncio
import sys


# ============================================================
# 配置
# ============================================================
ROBOT_IP = "192.168.1.1"  # 默认IP
PORT = 5890  # techmanpy 默认端口


# ============================================================
# 1. 网络诊断
# ============================================================
def check_network(robot_ip: str):
    """检查网络连接"""
    print("\n" + "=" * 50)
    print("1. 网络诊断")
    print("=" * 50)
    
    # Ping 测试
    print(f"[INFO] 尝试 Ping {robot_ip}...")
    response = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response.settimeout(3)
    
    try:
        # 尝试TCP连接
        result = response.connect_ex((robot_ip, PORT))
        if result == 0:
            print(f"[✓] {robot_ip}:{PORT} 端口可访问!")
            return True
        else:
            print(f"[✗] 无法连接到 {robot_ip}:{PORT}")
            print(f"    错误码: {result}")
            return False
    except socket.gaierror:
        print(f"[✗] DNS 解析失败: {robot_ip}")
        return False
    except Exception as e:
        print(f"[✗] 连接错误: {e}")
        return False
    finally:
        response.close()


# ============================================================
# 2. 端口扫描
# ============================================================
def scan_ports(robot_ip: str):
    """扫描常用端口"""
    print("\n" + "=" * 50)
    print("2. 端口扫描")
    print("=" * 50)
    
    ports = {
        5890: "TM Robot SCT Port",
        5891: "TM Robot SVR Port", 
        8080: "TM Robot HTTP",
    }
    
    for port, name in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((robot_ip, port))
        if result == 0:
            print(f"[✓] {port} ({name}) - 开放")
        else:
            print(f"[✗] {port} ({name}) - 关闭")
        sock.close()


# ============================================================
# 3. techmanpy 连接测试
# ============================================================
async def test_techmanpy(robot_ip: str):
    """测试 techmanpy 连接"""
    print("\n" + "=" * 50)
    print("3. techmanpy 连接测试")
    print("=" * 50)
    
    try:
        import techmanpy
        print(f"[INFO] 尝试连接 {robot_ip}...")
        
        async with techmanpy.connect_sct(robot_ip=robot_ip) as conn:
            print("[✓] techmanpy 连接成功!")
            
            # 获取关节角度
            joints = await conn.get_joint_angles()
            print(f"[INFO] 关节角度: {joints}")
            
            return True
            
    except ImportError:
        print("[✗] techmanpy 未安装")
        print("    运行: pip install techmanpy")
        return False
    except Exception as e:
        print(f"[✗] techmanpy 连接失败: {e}")
        return False


# ============================================================
# 4. 检查 TMflow 状态
# ============================================================
async def check_tmflow(robot_ip: str):
    """检查 TMflow 服务器"""
    print("\n" + "=" * 50)
    print("4. TMflow 服务器检查")
    print("=" * 50)
    
    try:
        import techmanpy
        
        # 尝试 SVR 连接 (用于监听)
        async with techmanpy.connect_svr(robot_ip=robot_ip) as conn:
            print("[✓] TMflow SVR 连接成功")
            print("[INFO] Listen Node 可能在运行中")
            return True
            
    except Exception as e:
        print(f"[✗] TMflow SVR 连接失败")
        print(f"    可能原因:")
        print(f"    - Listen Node 未开启")
        print(f"    - TMflow 版本低于 1.80")
        print(f"    - 防火墙阻止")
        return False


# ============================================================
# 主函数
# ============================================================
async def main():
    if len(sys.argv) < 2:
        robot_ip = ROBOT_IP
        print(f"使用默认IP: {robot_ip}")
        print(f"用法: python diagnose_connection.py <机器人IP>")
    else:
        robot_ip = sys.argv[1]
    
    print("\n" + "=" * 50)
    print("达明机器人连接诊断")
    print(f"目标: {robot_ip}")
    print("=" * 50)
    
    # 运行所有诊断
    net_ok = check_network(robot_ip)
    scan_ports(robot_ip)
    
    if net_ok:
        await test_techmanpy(robot_ip)
        await check_tmflow(robot_ip)
    else:
        print("\n[!] 网络不通，请检查:")
        print("    1. 机器人IP地址是否正确")
        print("    2. 网线连接是否正常")
        print("    3. 电脑IP是否在同网段")
    
    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
