#!/usr/bin/env python3
"""
TM Robot - Move All Joints to Zero
All joints (J1-J6) move to 0 degrees
"""

import asyncio
import sys


ROBOT_IP = "192.168.1.13"


async def move_all_zero():
    """Move all joints to 0 degrees"""
    from techmanpy import connect_sct
    
    print("=" * 50)
    print("TM Robot - All Joints to Zero")
    print("=" * 50)
    
    try:
        async with connect_sct(robot_ip=ROBOT_IP) as conn:
            print("[OK] Connected!")
            print("\n[INFO] Target: All joints = 0 degrees")
            print("[INFO] Speed: 10%, Acceleration: 50%")
            print("\n[WARNING] Robot will move! Keep clear!\n")
            
            # Move all joints to zero
            # Parameters: [J1, J2, J3, J4, J5, J6], speed(0-1), acceleration_duration
            await conn.move_to_joint_angles_ptp(
                joint_angles_goal=[0, 0, 0, 0, 0, 0],
                speed_perc=0.1,      # 10% speed - slow and safe
                acceleration_duration=50  # 50% acceleration
            )
            
            print("[OK] Motion command sent!")
            print("[INFO] Robot is moving to home position...")
            
    except Exception as e:
        print(f"[FAIL] {e}")


def main():
    print("\n" + "=" * 50)
    print("SAFETY WARNING")
    print("=" * 50)
    print("Robot will move all joints to 0 degrees.")
    print("Keep clear of the robot's working area!")
    print("=" * 50 + "\n")
    
    asyncio.run(move_all_zero())


if __name__ == "__main__":
    main()
