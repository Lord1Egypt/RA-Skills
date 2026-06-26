#!/bin/bash
# mqtt_tcp 模式使用示例 - AI 当作串口使用

set -e

ID="测试设备"

echo "=== mqtt_tcp 模式示例 ==="
echo ""

# 第一次使用时注册设备
echo "[1] 添加设备..."
python3 sp501lw_mqtt.py add \
  --id "$ID" \
  --cmd-topic "/public/a1b2c3d4e5f6/publish" \
  --data-topic "/public/a1b2c3d4e5f6/subscribe"

echo ""
echo "[2] 切换到 mqtt_tcp 模式..."
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "$ID"

echo ""
echo "[3] 使用方式："
echo ""
echo "终端 1：启动监听（接收数据）"
echo "  python3 sp501lw_mqtt.py listen --id \"$ID\" --format hex"
echo ""
echo "终端 2：发送命令（发送数据）"
echo "  python3 sp501lw_mqtt.py send --id \"$ID\" --data \"010301006400BD\" --format hex"
echo ""
echo "就像操作真实串口一样！"
