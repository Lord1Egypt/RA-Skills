#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - UR Official RTDE Library Test
Test URSim connection and basic functionality

Source: https://github.com/UniversalRobots/RTDE_Python_Client_Library
"""

import sys
import time

# UR official library import
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

# URSim local connection (Docker)
ROBOT_HOST = "localhost"
ROBOT_PORT = 30004

print("=" * 70)
print("UR Robot - UR Official RTDE Library Test")
print("=" * 70)

try:
    # Connect
    print("\n[1] Connecting to robot %s:%d..." % (ROBOT_HOST, ROBOT_PORT))
    con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    con.connect()
    print("[OK] Connected")
    
    # Get controller version
    print("\n[2] Getting controller version...")
    version = con.get_controller_version()
    if version:
        print("Version: %d.%d.%d.%d" % (version[0], version[1], version[2], version[3]))
    else:
        print("Cannot get version")
    
    # Setup output configuration
    print("\n[3] Setting up data output...")
    variables = ["actual_q", "actual_TCP_pose"]
    con.send_output_setup(variables, frequency=10)
    print("Config: %s" % str(variables))
    
    # Start data sync
    print("\n[4] Starting data sync...")
    con.send_start()
    print("[OK] Sync started")
    
    # Read state
    print("\n[5] Reading current state...")
    data = con.receive()
    if data:
        print("Joint angles: %s" % str(data.actual_q))
        print("TCP pose: %s" % str(data.actual_TCP_pose))
    else:
        print("No data received")
    
    # Pause sync
    print("\n[6] Pausing data sync...")
    con.send_pause()
    print("[OK] Sync paused")
    
    # Disconnect
    print("\n[7] Disconnecting...")
    con.disconnect()
    print("[OK] Disconnected")
    
    print("\n" + "=" * 70)
    print("Test completed!")
    print("=" * 70)
    
except Exception as e:
    print("\n[ERROR] %s" % str(e))
    print("\nPossible issues:")
    print("1. URSim not started")
    print("2. Docker container ports not mapped")
    print("3. Robot not in Program mode")
    print("\nSolutions:")
    print("1. Check URSim Docker container:")
    print("   docker ps | grep ursim")
    print("2. Check port mapping (30004):")
    print("   docker port ursim")
    print("3. Open browser: http://localhost:6080/vnc.html")
    print("   Click: Program -> Empty Program -> Play")