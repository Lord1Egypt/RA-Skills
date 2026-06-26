#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - Continuous Motion Test
Send multiple commands and restart program after each one
"""

import socket
import time

ROBOT_HOST = "localhost"
ROBOT_PORT = 30003

def send_urscript(command):
    """Send URScript command to robot"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect((ROBOT_HOST, ROBOT_PORT))
        full_command = command + "\n"
        sock.sendall(full_command.encode('utf-8'))
        print("[SENT] %s" % command[:60])
        time.sleep(0.1)
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        return True
    except Exception as e:
        print("[ERROR] %s" % str(e))
        return False
    finally:
        sock.close()

print("=" * 70)
print("UR Robot - Continuous Motion Test")
print("=" * 70)

# Test sequence: multiple positions
positions = [
    ([0, -1.57, 1.57, -1.57, -1.57, 0], "Home position"),
    ([0.5, -1.57, 1.57, -1.57, -1.57, 0], "J1 +28 degrees"),
    ([-0.5, -1.57, 1.57, -1.57, -1.57, 0], "J1 -28 degrees"),
    ([0, -1.57, 1.57, -1.57, -1.57, 0], "Back to home"),
    ([0, -0.5, 0.5, 0, 0.5, 0], "Zero position"),
]

for i, (position, description) in enumerate(positions, 1):
    print("\n[%d/%d] %s" % (i, len(positions), description))
    command = "movej(%s, a=0.3, v=0.3)" % str(position)
    success = send_urscript(command)
    
    if success:
        print("[OK] Command sent - Please wait 5 seconds for motion")
        print("[INFO] After motion completes, click Play (>) to restart program")
        time.sleep(5)
    else:
        print("[FAIL] Command failed")
        break

print("\n" + "=" * 70)
print("Test completed!")
print("Note: You need to click Play (>) after each motion completes")
print("=" * 70)
