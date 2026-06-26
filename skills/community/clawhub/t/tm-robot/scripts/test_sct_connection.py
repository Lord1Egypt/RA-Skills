#!/usr/bin/env python3
"""
TM Robot - SCT Connection Test (Listen Mode)
Connects via SCT port 5890 (Listen Node)
"""

import asyncio
import sys


ROBOT_IP = "192.168.1.13"


async def test_sct():
    """Test SCT connection - Listen Mode"""
    from techmanpy import connect_sct
    
    print("=" * 50)
    print("TM Robot SCT Connection Test")
    print(f"IP: {ROBOT_IP}")
    print("=" * 50)
    
    try:
        async with connect_sct(robot_ip=ROBOT_IP) as conn:
            print("[OK] SCT Connected!")
            print("     (Listen Node is running)\n")
            
            # Get connection info
            print("SCT Commands available:")
            print("  - move_to_joint_angles_ptp()")
            print("  - move_to_point_line()")
            print("  - stop_motion()")
            print("  - set_tcp()")
            print("  - etc.\n")
            
            print("=" * 50)
            print("SUCCESS: Robot is ready!")
            print("=" * 50)
            return True
            
    except Exception as e:
        print(f"[FAIL] {e}")
        return False


def main():
    asyncio.run(test_sct())


if __name__ == "__main__":
    main()
