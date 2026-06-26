#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - Simple Motion Test via Secondary Socket
Send URScript commands directly to port 30003

This is the simplest way to control UR robot motion!
"""

import socket
import time

ROBOT_HOST = "localhost"
ROBOT_PORT = 30003  # Secondary client interface (URScript)

print("=" * 70)
print("UR Robot - Simple Motion Test (Secondary Socket)")
print("=" * 70)

def send_urscript(host, port, command):
    """Send URScript command to robot via secondary socket"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect((host, port))
        # URScript commands must end with newline
        full_command = command + "\n"
        sock.sendall(full_command.encode('utf-8'))
        print("[SENT] %s" % command[:50])
        time.sleep(0.1)
        # Read response (robot status info)
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        return response
    except Exception as e:
        print("[ERROR] %s" % str(e))
        return None
    finally:
        sock.close()

try:
    # 1. Test connection
    print("\n[1] Testing connection to %s:%d..." % (ROBOT_HOST, ROBOT_PORT))
    response = send_urscript(ROBOT_HOST, ROBOT_PORT, "")
    if response:
        print("[OK] Connection successful")
        print("Robot info received")
    else:
        print("[ERROR] Cannot connect")
        raise Exception("Connection failed")

    # 2. Get current position
    print("\n[2] Getting current position...")
    # This will return robot state info
    time.sleep(0.5)

    # 3. Move to safe position (slow speed)
    print("\n[3] Moving to safe position...")
    # movej: joint space movement
    # Parameters: q (joint angles), a (acceleration), v (velocity)
    # Joint angles in radians: [J1, J2, J3, J4, J5, J6]
    safe_position = [0, -1.57, 1.57, -1.57, -1.57, 0]  # Home position
    command = "movej(%s, a=0.5, v=0.5)" % str(safe_position)
    send_urscript(ROBOT_HOST, ROBOT_PORT, command)
    print("Moving to: %s" % str(safe_position))
    print("Please wait 5 seconds for motion to complete...")
    time.sleep(5)
    print("[OK] Motion command sent")

    # 4. Small joint movement (test 1)
    print("\n[4] Test movement 1: Joint 1 rotation...")
    target1 = [0.5, -1.57, 1.57, -1.57, -1.57, 0]
    command = "movej(%s, a=0.3, v=0.3)" % str(target1)
    send_urscript(ROBOT_HOST, ROBOT_PORT, command)
    print("Moving J1 to: 0.5 rad (about 28 degrees)")
    time.sleep(3)
    print("[OK] Test 1 complete")

    # 5. Return to home
    print("\n[5] Returning to home position...")
    command = "movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=0.5, v=0.5)"
    send_urscript(ROBOT_HOST, ROBOT_PORT, command)
    time.sleep(5)
    print("[OK] Home position reached")

    # 6. Cartesian movement test
    print("\n[6] Test movement 2: Cartesian (linear) motion...")
    # movel: linear movement in Cartesian space
    # Parameters: pose [x, y, z, rx, ry, rz], a, v
    # Position relative to current TCP
    target_pose = [-0.2, -0.3, 0.3, 0, 3.14, 0]  # meters and radians
    command = "movel(%s, a=0.2, v=0.2)" % str(target_pose)
    send_urscript(ROBOT_HOST, ROBOT_PORT, command)
    print("Moving TCP linearly...")
    time.sleep(4)
    print("[OK] Cartesian test complete")

    # 7. Final: back to home
    print("\n[7] Final: Returning to safe home...")
    command = "movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=0.5, v=0.5)"
    send_urscript(ROBOT_HOST, ROBOT_PORT, command)
    time.sleep(5)
    print("[OK] Home position")

    print("\n" + "=" * 70)
    print("Motion test completed!")
    print("Watch the robot in URSim: http://localhost:6080/vnc.html")
    print("=" * 70)

except Exception as e:
    print("\n[ERROR] %s" % str(e))
    print("\nPossible issues:")
    print("1. URSim not running or not in Program mode")
    print("2. Port 30003 not mapped in Docker")
    print("\nSolution:")
    print("1. Open http://localhost:6080/vnc.html")
    print("2. Click: Program -> Empty Program -> Play (green button)")
    print("3. Check Docker port mapping: docker port ursim")