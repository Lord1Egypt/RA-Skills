#!/bin/bash
# 使用自定义 Broker 和自定义主题的示例

set -e

ID="公司网关"

echo "=== 自定义 Broker 和主题示例 ==="
echo ""

echo "[1] 注册设备到自定义 Broker..."
python3 sp501lw_mqtt.py add \
  --id "$ID" \
  --cmd-topic "/mycompany/devices/gateway/cmd" \
  --data-topic "/mycompany/devices/gateway/data" \
  --broker-host mqtt.mycompany.com \
  --broker-port 8883 \
  --username company_user \
  --password company_password123

echo ""
echo "[2] 列出已保存的设备..."
python3 sp501lw_mqtt.py list

echo ""
echo "[3] 切换工作模式..."
python3 sp501lw_mqtt.py set-mode mqtt_tcp --id "$ID"

echo ""
echo "[4] 开始使用..."
echo "python3 sp501lw_mqtt.py listen --id \"$ID\" --format hex"
echo ""
echo "所有 MQTT 通信都会通过自定义 Broker 和主题进行！"
