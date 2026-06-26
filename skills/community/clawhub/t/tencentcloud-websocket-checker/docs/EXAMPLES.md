# 使用示例大全

## 目录

1. [基础用法](#1-基础用法)
2. [协议切换](#2-协议切换)
3. [多轮测试](#3-多轮测试)
4. [批量检测](#4-批量检测)
5. [生产环境场景](#5-生产环境场景)
6. [结合其他工具](#6-结合其他工具)
7. [自定义配置](#7-自定义配置)
8. [CI/CD 集成](#8-cicd-集成)

---

## 1. 基础用法

### 1.1 最简使用（默认 3 轮 wss 测试）

```bash
./ws_check.sh wss://echo.websocket.org
```

### 1.2 指定完整 URL（包含路径和参数）

```bash
./ws_check.sh wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS
```

### 1.3 查看帮助信息

```bash
./ws_check.sh --help
```

---

## 2. 协议切换

### 2.1 通过 URL 前缀自动识别

```bash
# wss 协议（TLS 加密）
./ws_check.sh wss://example.com/ws

# ws 协议（明文）
./ws_check.sh ws://example.com/ws
```

### 2.2 通过 -p 参数强制指定

```bash
# 用 -p 指定协议，URL 可省略协议前缀
./ws_check.sh -p wss example.com/ws
./ws_check.sh --protocol ws example.com/ws
```

### 2.3 协议覆盖（-p 优先级最高）

```bash
# URL 写的是 wss，但实际使用 ws 协议
./ws_check.sh -p ws wss://example.com/ws

# 用于测试同一服务在不同协议下的性能差异
./ws_check.sh -p wss example.com/ws 3  # 先测 wss
./ws_check.sh -p ws  example.com/ws 3  # 再测 ws，对比 TLS 开销
```

---

## 3. 多轮测试

### 3.1 快速单轮测试

```bash
./ws_check.sh wss://example.com/ws 1
```

### 3.2 高精度多轮测试

```bash
# 5 轮测试，获取更稳定的统计数据
./ws_check.sh wss://example.com/ws 5

# 10 轮测试，适合严格的性能基准测试
./ws_check.sh wss://example.com/ws 10
```

---

## 4. 批量检测

### 4.1 使用批量检测脚本

```bash
# 创建 URL 列表文件
cat > urls.txt << 'EOF'
wss://server1.example.com/ws
wss://server2.example.com/ws
ws://server3.example.com/ws
EOF

# 批量检测
./utils/batch_check.sh urls.txt 3
```

### 4.2 手动循环检测多个地址

```bash
for url in \
    "wss://server1.example.com/ws" \
    "wss://server2.example.com/ws" \
    "wss://server3.example.com/ws"; do
    echo "===== 检测: $url ====="
    ./ws_check.sh "$url" 2
    echo ""
done
```

---

## 5. 生产环境场景

### 5.1 TTS 服务 WebSocket 端点检测

```bash
# 腾讯云 TTS 国际站
./ws_check.sh wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 5

# 国内站
./ws_check.sh wss://tts.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 5
```

### 5.2 定时巡检（配合 cron）

```bash
# 编辑 crontab
crontab -e

# 每小时执行一次检测，结果追加到日志文件
0 * * * * /path/to/ws_check.sh wss://your-server.com/ws 3 >> /var/log/ws_latency.log 2>&1
```

### 5.3 不同地域对比测试

```bash
# 从不同机器执行，对比各地域到同一服务的延迟
# 华南节点
ssh south-node './ws_check.sh wss://api.example.com/ws 5'

# 华北节点
ssh north-node './ws_check.sh wss://api.example.com/ws 5'

# 海外节点
ssh overseas-node './ws_check.sh wss://api.example.com/ws 5'
```

---

## 6. 结合其他工具

### 6.1 配合 watch 持续监控

```bash
# 每 30 秒执行一次（仅单轮快速检测）
watch -n 30 './ws_check.sh wss://example.com/ws 1'
```

### 6.2 输出重定向保存报告

```bash
# 保存到文件（去除颜色代码）
./ws_check.sh wss://example.com/ws 5 2>&1 | sed 's/\x1B\[[0-9;]*m//g' > report.txt

# 同时显示和保存
./ws_check.sh wss://example.com/ws 5 2>&1 | tee report.txt
```

### 6.3 使用报告生成工具

```bash
# 生成 CSV 格式报告（便于 Excel 分析）
./utils/report_generator.sh wss://example.com/ws 5 csv > report.csv

# 生成 JSON 格式报告
./utils/report_generator.sh wss://example.com/ws 5 json > report.json
```

---

## 7. 自定义配置

### 7.1 修改性能阈值

```bash
# 编辑 config.env
vim config.env

# 例如调整 TLS 阈值（对于海外服务可适当放宽）
# TLS_THRESHOLD_GOOD=300
# TLS_THRESHOLD_WARN=800
```

### 7.2 添加自定义请求头

```bash
# 在 config.env 中配置 Token 等请求头
# CUSTOM_HEADERS=("-H" "Authorization: Bearer your-token")
```

---

## 8. CI/CD 集成

### 8.1 在 Jenkins Pipeline 中使用

```groovy
stage('WebSocket Latency Check') {
    steps {
        sh '''
            chmod +x ws_check.sh
            ./ws_check.sh wss://staging.example.com/ws 3 2>&1 | tee ws_report.txt
        '''
        archiveArtifacts artifacts: 'ws_report.txt'
    }
}
```

### 8.2 作为发布前检查

```bash
#!/bin/bash
# pre_deploy_check.sh
RESULT=$(./ws_check.sh wss://production.example.com/ws 3 2>&1)
echo "$RESULT"

# 检查是否有"偏慢"评级
if echo "$RESULT" | grep -q "偏慢"; then
    echo "⚠ 检测到性能问题，请确认后再发布"
    exit 1
fi

echo "✅ 连接性能正常，可以发布"
```
