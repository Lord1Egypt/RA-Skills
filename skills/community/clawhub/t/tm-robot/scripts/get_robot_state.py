#!/usr/bin/env python3
"""
TM Robot - Read Robot State via SVR Connection
TMflow variables: https://docs.tm-robot.com/
"""

import asyncio
import sys


ROBOT_IP = "192.168.1.13"


async def get_robot_state():
    """Read robot state using SVR connection"""
    try:
        from techmanpy import connect_svr
        
        print("Connecting to SVR...")
        async with connect_svr(robot_ip=ROBOT_IP) as conn:
            print("[OK] Connected!\n")
            
            # Common TM variables for robot state
            # Format: ("variable_name", "type")
            variables = [
                # Joint angles (degrees)
                ("Joint_Target", "J"),      # Target joint angles
                ("Joint_Actual", "J"),      # Actual joint angles
                ("Joint_Angle", "J"),        # Current joint angles
                
                # Cartesian position (mm, degrees)
                ("Cartesian_Target", "P"),   # Target position
                ("Cartesian_Actual", "P"),   # Actual position
                ("Pos_Target", "P"),         # Target
                ("Pos_Actual", "P"),         # Actual
                
                # Robot mode
                ("RobotMode", ""),          # Robot mode
                ("RobotErrCode", ""),        # Error code
                ("ProjectName", ""),        # Current project
            ]
            
            print("Reading variables:")
            print("-" * 50)
            
            for var_name, var_type in variables:
                try:
                    if var_type:
                        value = await conn.get_value(var_name, var_type)
                    else:
                        value = await conn.get_value(var_name)
                    
                    if value is not None and value != "":
                        print(f"  {var_name}: {value}")
                except Exception as e:
                    pass  # Variable might not exist
                    
            print("-" * 50)
            print("\n[OK] State read complete!")
            
    except ImportError:
        print("[FAIL] techmanpy not installed. Run: pip install techmanpy")
    except Exception as e:
        print(f"[FAIL] {e}")


async def get_joint_angles_simple():
    """Simple joint angle read - try common variable names"""
    from techmanpy import connect_svr
    
    print("Testing joint angle reading...")
    async with connect_svr(robot_ip=ROBOT_IP) as conn:
        # Try different variable names
        test_vars = [
            ("Joint_Angle", "J"),
            ("JointAngle", "J"),
            ("Joint_Actual", "J"),
            ("Joint_Target", "J"),
            ("CurJnt", "J"),
        ]
        
        for name, vtype in test_vars:
            try:
                val = await conn.get_value(name, vtype)
                print(f"  {name} = {val}")
            except:
                pass


def main():
    print("=" * 50)
    print("TM Robot State Reader")
    print(f"IP: {ROBOT_IP}")
    print("=" * 50 + "\n")
    
    asyncio.run(get_robot_state())


if __name__ == "__main__":
    main()
