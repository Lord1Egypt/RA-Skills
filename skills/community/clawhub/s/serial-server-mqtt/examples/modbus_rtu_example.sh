#!/bin/bash
# modbus_rtu 模式使用示例 - AI 当作数据采集器使用

set -e

ID="测试设备"

echo "=== modbus_rtu 模式示例 ==="
echo ""

# 第一次使用时注册设备
echo "[1] 添加设备..."
python3 sp501lw_mqtt.py add \
  --id "$ID" \
  --cmd-topic "/public/a1b2c3d4e5f6/publish" \
  --data-topic "/public/a1b2c3d4e5f6/subscribe"

echo ""
echo "[2] 切换到 modbus_rtu 模式..."
python3 sp501lw_mqtt.py set-mode modbus_rtu --id "$ID"
echo "等待设备重启（5-30 秒）..."
sleep 20

echo ""
echo "[3] 设置轮询周期..."
python3 sp501lw_mqtt.py set-poll-time 60000 --id "$ID"
echo "等待设备重启..."
sleep 15

echo ""
echo "[4] 添加采集任务 1（从站 1，读温度）"
python3 sp501lw_mqtt.py add-modbus --id "$ID" \
  --slave-addr 1 \
  --function-code 3 \
  --register-addr 0 \
  --register-num 2 \
  --interval 5000 \
  --timeout 1000 \
  --data-format Float \
  --report-format mqtt

echo ""
echo "[5] 添加采集任务 2（从站 2，读压力）"
python3 sp501lw_mqtt.py add-modbus --id "$ID" \
  --slave-addr 2 \
  --function-code 3 \
  --register-addr 0 \
  --register-num 2 \
  --interval 10000 \
  --timeout 1000 \
  --data-format Unsigned \
  --report-format mqtt

echo ""
echo "[6] 监听采集数据..."
echo "python3 sp501lw_mqtt.py listen --id \"$ID\" --format json"
echo ""
echo "设备会定期上报采集的数据！"
