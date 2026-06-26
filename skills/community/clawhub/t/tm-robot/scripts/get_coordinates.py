#!/usr/bin/env python3
"""
TM Robot - Get Current Coordinates
Try SVR connection to read robot state variables
"""

import asyncio


ROBOT_IP = "192.168.1.13"


async def get_coordinates():
    """Read robot coordinates via SVR"""
    from techmanpy import connect_svr
    
    print("=" * 50)
    print("TM Robot Coordinate Reader")
    print("=" * 50)
    
    try:
        print("\n[INFO] Connecting to SVR (port 5891)...")
        async with connect_svr(robot_ip=ROBOT_IP) as conn:
            print("[OK] SVR Connected!\n")
            
            # TM robot state variables
            # J = Joint angles (degrees)
            # P = Position (mm, degrees)
            
            variables = [
                # Joint Angles
                ("Joint_Angle", "J"),
                # Cartesian Position
                ("Pos_Actual", "P"),
                ("Cartesian_Actual", "P"),
                # Additional info
                ("RobotMode", ""),
                ("ProjectName", ""),
            ]
            
            print("Robot State:")
            print("-" * 50)
            
            for var_name, var_type in variables:
                try:
                    if var_type:
                        value = await conn.get_value(var_name, var_type)
                    else:
                        value = await conn.get_value(var_name)
                    print(f"  {var_name}: {value}")
                except Exception as e:
                    print(f"  {var_name}: ERROR ({e})")
            
            print("-" * 50)
            
    except ImportError:
        print("[FAIL] techmanpy not installed")
    except Exception as e:
        print(f"[FAIL] {e}")
        print("\nNOTE: SVR connection requires SVR Server enabled in TMflow")
        print("      Go to TMflow -> Listen Node -> Enable SVR Server")


def main():
    asyncio.run(get_coordinates())


if __name__ == "__main__":
    main()
