#!/usr/bin/env python3
"""
TM Robot - Move J3=90, J5=90 with 40% Speed
"""

import asyncio


ROBOT_IP = "192.168.1.13"


async def move_j3_j5():
    """Move J3 to 90 degrees, J5 to 90 degrees"""
    from techmanpy import connect_sct
    
    print("=" * 50)
    print("TM Robot - Move J3 & J5 to 90 degrees")
    print("=" * 50)
    
    try:
        async with connect_sct(robot_ip=ROBOT_IP) as conn:
            print("[OK] Connected!")
            
            # Target: J1=0, J2=0, J3=90, J4=0, J5=90, J6=0
            target = [0, 0, 90, 0, 90, 0]
            
            print(f"\n[INFO] Target joints: {target}")
            print(f"[INFO] Speed: 40%")
            print("\n[WARNING] Robot will move! Keep clear!\n")
            
            # Move to target with 40% speed
            # Parameters: joint_angles, speed(0-1), acceleration_duration
            await conn.move_to_joint_angles_ptp(
                joint_angles_goal=target,
                speed_perc=0.4,      # 40% speed
                acceleration_duration=50
            )
            
            print("[OK] Motion command sent!")
            print("[INFO] J3 -> 90, J5 -> 90")
            
    except Exception as e:
        print(f"[FAIL] {e}")


def main():
    print("\n" + "=" * 50)
    print("SAFETY WARNING")
    print("=" * 50)
    print("Robot will move J3 and J5 to 90 degrees.")
    print("Keep clear of the robot's working area!")
    print("=" * 50 + "\n")
    
    asyncio.run(move_j3_j5())


if __name__ == "__main__":
    main()
