#!/bin/bash
# 测试Robot5导航脚本

source /opt/ros/noetic/setup.bash
source ~/robot5/devel/setup.bash

cd ~/.openclaw/workspace/skills/ros1-for-robot5/scripts

python3 get_pose_tf.py "$@"
