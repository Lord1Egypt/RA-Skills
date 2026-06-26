# WebSocket 延迟检测工具 - 使用示例参考

## 基础用法

```bash
# wss 协议（默认3轮）
./ws_check.sh wss://example.com/ws

# ws 协议
./ws_check.sh ws://example.com/ws

# 指定轮数
./ws_check.sh wss://example.com/ws 5
```

## 协议切换

```bash
# -p 参数强制指定（优先级最高）
./ws_check.sh -p wss example.com/ws
./ws_check.sh -p ws wss://example.com/ws  # 覆盖 URL 中的 wss

# 对比 TLS 开销
./ws_check.sh -p wss example.com/ws 5
./ws_check.sh -p ws  example.com/ws 5
```

## 批量检测

```bash
# 创建 URL 列表
cat > urls.txt << 'EOF'
wss://server1.example.com/ws
wss://server2.example.com/ws
ws://server3.example.com/ws
EOF

./utils/batch_check.sh urls.txt 3
```

## 结构化报告

```bash
./utils/report_generator.sh wss://example.com/ws 5 csv > report.csv
./utils/report_generator.sh wss://example.com/ws 5 json > report.json
```

## 定时巡检

```bash
# crontab 每小时检测
0 * * * * /path/to/ws_check.sh wss://server.com/ws 3 >> /var/log/ws_latency.log 2>&1
```

## CI/CD 集成

```bash
RESULT=$(./ws_check.sh wss://production.example.com/ws 3 2>&1)
if echo "$RESULT" | grep -q "偏慢"; then
    echo "⚠ 检测到性能问题" && exit 1
fi
```

## 持续监控

```bash
watch -n 30 './ws_check.sh wss://example.com/ws 1'
```

## 输出保存（去除颜色）

```bash
./ws_check.sh wss://example.com/ws 5 2>&1 | sed 's/\x1B\[[0-9;]*m//g' > report.txt
```
