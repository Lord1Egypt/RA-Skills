#!/usr/bin/env python3
"""Move a ROS1 robot by distance using cmd_vel + odometry closed loop."""

import argparse
import math
import sys

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Closed-loop forward movement by odometry")
    p.add_argument("--cmd-topic", default="/cmd_vel")
    p.add_argument("--odom-topic", default="/odom")
    p.add_argument("--distance", type=float, default=1.0)
    p.add_argument("--speed", type=float, default=0.2)
    p.add_argument("--rate", type=float, default=20.0)
    p.add_argument("--timeout", type=float, default=20.0)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if args.distance <= 0:
        print("ERROR: --distance must be > 0", file=sys.stderr)
        return 2
    if args.speed <= 0:
        print("ERROR: --speed must be > 0", file=sys.stderr)
        return 2

    rospy.init_node("move_forward_by_odom", anonymous=True)

    pub = rospy.Publisher(args.cmd_topic, Twist, queue_size=10)

    try:
        first = rospy.wait_for_message(args.odom_topic, Odometry, timeout=5.0)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: failed to read odometry from {args.odom_topic}: {e}", file=sys.stderr)
        return 3

    sx = first.pose.pose.position.x
    sy = first.pose.pose.position.y

    cmd = Twist()
    cmd.linear.x = args.speed

    stop = Twist()
    rate = rospy.Rate(args.rate)
    start_time = rospy.Time.now().to_sec()
    last_d = 0.0
    reached = False

    try:
        while not rospy.is_shutdown():
            try:
                od = rospy.wait_for_message(args.odom_topic, Odometry, timeout=0.5)
            except Exception as e:  # noqa: BLE001
                print(f"ERROR: odometry timeout: {e}", file=sys.stderr)
                break

            x = od.pose.pose.position.x
            y = od.pose.pose.position.y
            last_d = math.hypot(x - sx, y - sy)

            if last_d >= args.distance:
                reached = True
                break

            pub.publish(cmd)

            if rospy.Time.now().to_sec() - start_time > args.timeout:
                print(f"TIMEOUT: {args.timeout}s, moved={last_d:.3f}m", file=sys.stderr)
                break

            rate.sleep()
    finally:
        for _ in range(10):
            pub.publish(stop)
            rate.sleep()

    print(f"RESULT reached={reached} distance={last_d:.3f}m target={args.distance:.3f}m")
    return 0 if reached else 1


if __name__ == "__main__":
    raise SystemExit(main())
