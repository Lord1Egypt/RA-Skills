#!/usr/bin/env python3
"""
TM Robot Connection Diagnostic - ASCII Only Version
"""

import socket
import asyncio
import sys


def check_port(ip, port, timeout=3):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python diagnose_simple.py <robot_ip>")
        print("Example: python diagnose_simple.py 192.168.1.1")
        sys.exit(1)
    
    robot_ip = sys.argv[1]
    
    print("=" * 50)
    print("TM Robot Connection Diagnostic")
    print(f"Target: {robot_ip}")
    print("=" * 50)
    
    # Check common ports
    ports = {
        5890: "SCT Port (techmanpy default)",
        5891: "SVR Port (listen mode)",
        8080: "HTTP Port"
    }
    
    print("\n[1] Port Scan:")
    for port, name in ports.items():
        status = "OPEN" if check_port(robot_ip, port) else "CLOSED"
        print(f"  Port {port} ({name}): {status}")
    
    # Try techmanpy connection
    print("\n[2] Testing techmanpy connection...")
    try:
        import techmanpy
        
        async def test():
            try:
                async with techmanpy.connect_sct(robot_ip=robot_ip) as conn:
                    print("  [OK] Connected!")
                    joints = await conn.get_joint_angles()
                    print(f"  Joint angles: {joints}")
                    return True
            except Exception as e:
                print(f"  [FAIL] {e}")
                return False
        
        result = asyncio.run(test())
        
    except ImportError:
        print("  [FAIL] techmanpy not installed. Run: pip install techmanpy")
        result = False
    except Exception as e:
        print(f"  [FAIL] {e}")
        result = False
    
    print("\n" + "=" * 50)
    if result:
        print("SUCCESS! Robot is accessible.")
    else:
        print("FAILED! Check:")
        print("  1. Is Listen Node running in TMflow?")
        print("  2. Is robot IP correct?")
        print("  3. Is cable connected?")
    print("=" * 50)


if __name__ == "__main__":
    main()
