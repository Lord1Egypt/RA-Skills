#!/bin/bash

set -euo pipefail

if [ -f /proc/device-tree/model ]; then
  tr -d '\0' < /proc/device-tree/model
  exit 0
fi

if [ -f /sys/firmware/devicetree/base/model ]; then
  tr -d '\0' < /sys/firmware/devicetree/base/model
  exit 0
fi

if [ -f /sys/class/dmi/id/product_name ]; then
  cat /sys/class/dmi/id/product_name
  exit 0
fi

if command -v hostname >/dev/null 2>&1; then
  hostname
  exit 0
fi

grep "Model" /proc/cpuinfo || true
