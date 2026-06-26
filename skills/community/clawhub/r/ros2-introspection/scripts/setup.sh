#!/bin/bash
echo "Configuring ros2-introspection skill..."

# Detect ROS 2 setup path based on current environment
ROS2_BIN=$(which ros2 2>/dev/null)
if [ -z "$ROS2_BIN" ]; then
    echo "Error: ros2 not found in PATH. Please source your ROS 2 environment before running setup."
    exit 1
fi

ROS_SETUP_PATH="$(dirname "$(dirname "$ROS2_BIN")")/setup.bash"

mkdir -p "$(dirname "$0")/../config"
cat <<EOF > "$(dirname "$0")/../config/config.json"
{
  "ros_setup_path": "$ROS_SETUP_PATH"
}
EOF

echo "Configuration updated:"
echo "  - ROS_SETUP_PATH: $ROS_SETUP_PATH"
