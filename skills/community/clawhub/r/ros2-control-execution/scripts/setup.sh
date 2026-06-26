#!/bin/bash
echo "Configuring ros2-control-execution skill..."

ROS2_BIN=$(which ros2 2>/dev/null)
if [ -z "$ROS2_BIN" ]; then
    echo "Error: ros2 not found in PATH. Please source your ROS 2 environment before running setup."
    exit 1
fi

ROS_SETUP_PATH="$(dirname "$(dirname "$ROS2_BIN")")/setup.bash"

if [ -z "$AMENT_PREFIX_PATH" ]; then
    echo "Error: AMENT_PREFIX_PATH is empty. Make sure ROS 2 is sourced."
    exit 1
fi

JSON_ARRAY=$(echo "$AMENT_PREFIX_PATH" | tr ':' '\n' | awk '{print "\"" $0 "\""}' | paste -sd, -)

mkdir -p "$(dirname "$0")/../config"
cat <<EOF > "$(dirname "$0")/../config/config.json"
{
  "ros_setup_path": "$ROS_SETUP_PATH",
  "workspace_roots": [$JSON_ARRAY]
}
EOF
echo "Configuration updated successfully."