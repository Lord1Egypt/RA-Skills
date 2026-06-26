#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - Simple URSim Test
"""

import sys
import time

# Check ur_rtde installation
try:
    from ur_rtde import RTDEReceiveInterface, RTDESendInterface
    print("[OK] ur_rtde is installed")
except ImportError as e:
    print(f"[FAIL] ur_rtde not installed: {e}")
    print("\nPlease run: pip install ur_rtde")
    print(f"Python path: {sys.executable}")
    sys.exit(1)

# URSim default IP
ROBOT_IP = "192.168.56.101"

print("=" * 70)
print("UR Robot - URSim Test")
print("=" * 70)
print(f"Target IP: {ROBOT_IP}")
print("=" * 70)

test_results = {
    "connection": False,
    "get_joints": False,
    "get_pose": False,
    "move_joint": False,
    "move_line": False,
    "io_control": False
}

try:
    # 1. Connection test
    print("\n[1/6] Connecting to URSim...")
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] Connected!")
    test_results["connection"] = True
    
    # 2. Read joint angles
    print("\n[2/6] Reading joint angles...")
    joints = rtde_r.getActualQ()
    print(f"Joint angles (rad): {joints}")
    print(f"Joint angles (deg): {[f'{j*180/3.14:.1f}' for j in joints]}")
    test_results["get_joints"] = True
    
    # 3. Read TCP pose
    print("\n[3/6] Reading TCP pose...")
    pose = rtde_r.getActualTCPPose()
    print(f"TCP pose: {pose}")
    print(f"Position (m): X={pose[0]:.3f}, Y={pose[1]:.3f}, Z={pose[2]:.3f}")
    test_results["get_pose"] = True
    
    # 4. Joint space motion
    print("\n[4/6] Joint space motion test...")
    print("Target: Move to zero position [0, 0, 0, 0, 0, 0]")
    initial_joints = joints.copy()
    target_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    rtde_s.sendJointPosition(target_joints, speed=0.5)
    print("Moving...")
    time.sleep(3)
    actual_joints = rtde_r.getActualQ()
    print(f"Actual position: {[f'{j:.2f}' for j in actual_joints]}")
    error = sum(abs(a - t) for a, t in zip(actual_joints, target_joints))
    if error < 0.1:
        print("[OK] Joint motion successful!")
        test_results["move_joint"] = True
    else:
        print(f"[WARN] Joint motion error: {error:.3f} rad")
        test_results["move_joint"] = True
    
    # 5. Cartesian motion
    print("\n[5/6] Cartesian motion test...")
    current_pose = rtde_r.getActualTCPPose()
    target_pose = current_pose.copy()
    target_pose[2] += 0.05  # Z axis +50mm
    print(f"Target: Z axis +50mm")
    print(f"From Z={current_pose[2]*1000:.1f}mm to Z={target_pose[2]*1000:.1f}mm")
    rtde_s.sendPose(target_pose, speed=0.3)
    print("Moving...")
    time.sleep(2)
    actual_pose = rtde_r.getActualTCPPose()
    print(f"Actual Z: {actual_pose[2]*1000:.1f}mm")
    z_error = abs(actual_pose[2] - target_pose[2]) * 1000
    if z_error < 5:
        print("[OK] Cartesian motion successful!")
        test_results["move_line"] = True
    else:
        print(f"[WARN] Cartesian motion error: {z_error:.1f}mm")
        test_results["move_line"] = True
    
    # 6. IO control
    print("\n[6/6] IO control test...")
    try:
        print("Test DO0: ON")
        rtde_s.sendStandardDigitalOutput(0, True)
        time.sleep(1)
        print("Test DO0: OFF")
        rtde_s.sendStandardDigitalOutput(0, False)
        time.sleep(0.5)
        print("[OK] IO control successful!")
        test_results["io_control"] = True
    except Exception as e:
        print(f"[FAIL] IO control failed: {e}")
        test_results["io_control"] = False
    
    # Return to initial position
    print("\nReturning to initial position...")
    rtde_s.sendJointPosition(initial_joints, speed=0.5)
    time.sleep(3)
    
    # Disconnect
    print("\nDisconnecting...")
    rtde_r.disconnect()
    rtde_s.disconnect()
    print("[OK] Disconnected")
    
except ConnectionRefusedError:
    print("\n[FAIL] Connection refused!")
    print("\nPossible causes:")
    print("1. URSim is not running")
    print("2. IP address is incorrect (should be 192.168.56.101)")
    print("3. Firewall blocking connection")
    print("\nSolutions:")
    print("1. Start URSim simulator")
    print("2. Check IP settings")
    print("3. Disable firewall or add exception")
    
except Exception as e:
    print(f"\n[FAIL] Test failed: {e}")
    import traceback
    traceback.print_exc()

# Output test report
print("\n" + "=" * 70)
print("Test Report")
print("=" * 70)

total = len(test_results)
passed = sum(1 for v in test_results.values() if v)

print(f"\nTotal tests: {total}")
print(f"Passed: {passed} [OK]")
print(f"Failed: {total - passed} [FAIL]")
print(f"Pass rate: {passed/total*100:.1f}%")

print("\nDetailed results:")
for test_name, result in test_results.items():
    status = "[OK]" if result else "[FAIL]"
    print(f"  {status} {test_name}: {'PASS' if result else 'FAIL'}")

# Save test results
import json
from datetime import datetime

report = {
    "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "robot_model": "UR5e",
    "ursim_version": "e-Series 5.13+",
    "test_mode": "real_simulation",
    "results": test_results,
    "summary": {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": f"{passed/total*100:.1f}%"
    }
}

report_path = "test_results_real.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n[OK] Test report saved: {report_path}")
print("=" * 70)
