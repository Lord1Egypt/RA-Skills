# 小红书 MCP 补丁包

部署小红书 MCP 时常见问题的自动化修复方案。

## 问题一：端口被占用

**问题描述**：启动 MCP 服务时提示 `bind: address already in use`

**自动修复代码**：

```bash
#!/bin/bash
# 检查并释放端口 18060

echo "检查端口 18060..."
PID=$(lsof -ti:18060 2>/dev/null)

if [ -n "$PID" ]; then
    echo "发现占用进程: $PID，正在终止..."
    kill -9 $PID
    sleep 2
    echo "进程已终止"
else
    echo "端口空闲"
fi

# 验证
if lsof -i :18060 >/dev/null 2>&1; then
    echo "错误：端口仍被占用"
    exit 1
else
    echo "端口已释放，可以启动服务"
fi
```

**使用方法**：
```bash
chmod +x fix-port.sh
./fix-port.sh
```

---

## 问题二：Cookie 路径问题

**问题描述**：MCP 服务找不到 cookies.json 文件

**自动修复代码**：

```bash
#!/bin/bash
# 将 cookie 文件复制到所有可能的位置

COOKIE_SOURCE="/path/to/your/cookies.json"

echo "复制 cookie 文件到多个位置..."

# 创建目录
mkdir -p /tmp/cookies
mkdir -p ~/.cache/rod/browser

# 复制到多个位置
cp "$COOKIE_SOURCE" /tmp/cookies.json
cp "$COOKIE_SOURCE" /tmp/cookies/cookies.json
cp "$COOKIE_SOURCE" ./cookies.json 2>/dev/null || true
cp "$COOKIE_SOURCE" ~/.cache/rod/browser/cookies.json

echo "Cookie 文件已放置到："
find /tmp -name "cookies.json" 2>/dev/null
find ~ -name "cookies.json" 2>/dev/null | head -5
```

**使用方法**：
```bash
chmod +x fix-cookie.sh
./fix-cookie.sh /path/to/your/cookies.json
```

---

## 问题三：调用卡住/超时

**问题描述**：调用 MCP 工具时无响应，可能是 Chrome 下载中

**自动修复代码**：

```bash
#!/bin/bash
# 等待 Chrome 下载完成

echo "等待 Chrome 下载完成..."
LOG_FILE="/tmp/mcp.log"

for i in {1..120}; do
    if grep -q "Downloaded:" "$LOG_FILE" 2>/dev/null; then
        echo "✅ Chrome 下载完成"
        break
    fi
    
    if grep -q "Unzip:" "$LOG_FILE" 2>/dev/null; then
        echo "✅ Chrome 解压中..."
        break
    fi
    
    PROGRESS=$(grep "Progress:" "$LOG_FILE" 2>/dev/null | tail -1)
    if [ -n "$PROGRESS" ]; then
        echo "进度: $PROGRESS"
    fi
    
    sleep 5
done

echo "准备就绪"
```

**使用方法**：
```bash
chmod +x wait-chrome.sh
./wait-chrome.sh
```

---

## 问题四：检查服务状态

**问题描述**：不确定 MCP 服务是否正常运行

**自动修复代码**：

```bash
#!/bin/bash
# 检查并重启 MCP 服务

echo "检查 MCP 服务状态..."

# 检查进程
if pgrep -f "xiaohongshu-mcp" >/dev/null; then
    echo "服务正在运行"
    ps aux | grep xiaohongshu-mcp | grep -v grep
else
    echo "服务未运行，正在启动..."
    cd /tmp
    nohup ./xiaohongshu-mcp-linux-amd64 >/tmp/mcp.log 2>&1 &
    sleep 3
    
    if pgrep -f "xiaohongshu-mcp" >/dev/null; then
        echo "✅ 服务已启动"
        tail -3 /tmp/mcp.log
    else
        echo "❌ 启动失败"
        exit 1
    fi
fi

# 测试连接
echo "测试 MCP 连接..."
SESSION=$(curl -s -N -D - -X POST http://localhost:18060/mcp \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}' 2>/dev/null | \
    grep -i "Mcp-Session-Id" | awk '{print $2}' | tr -d '\r')

if [ -n "$SESSION" ]; then
    echo "✅ MCP 连接正常，Session: $SESSION"
else
    echo "❌ MCP 连接失败"
    exit 1
fi
```

**使用方法**：
```bash
chmod +x check-service.sh
./check-service.sh
```

---

## 一键修复脚本

```bash
#!/bin/bash
# 小红书 MCP 一键修复

echo "===== 小红书 MCP 补丁包 ====="

# 1. 修复端口
echo "[1/4] 检查端口..."
lsof -ti:18060 | xargs kill -9 2>/dev/null
sleep 1

# 2. 检查 cookie
if [ -f "/tmp/cookies/cookies.json" ]; then
    echo "[2/4] Cookie 文件存在"
else
    echo "[2/4] ⚠️ 缺少 cookie 文件，请手动放置"
fi

# 3. 启动服务
echo "[3/4] 启动服务..."
cd /tmp
if pgrep -f "xiaohongshu-mcp" >/dev/null; then
    echo "服务已在运行"
else
    nohup ./xiaohongshu-mcp-linux-amd64 >/tmp/mcp.log 2>&1 &
    sleep 3
    echo "服务已启动"
fi

# 4. 测试连接
echo "[4/4] 测试连接..."
SESSION=$(curl -s -N -D - -X POST http://localhost:18060/mcp \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}' 2>/dev/null | \
    grep -i "Mcp-Session-Id" | awk '{print $2}' | tr -d '\r')

if [ -n "$SESSION" ]; then
    echo "✅ 修复完成，MCP 正常工作"
else
    echo "❌ 连接失败，请检查日志: tail -f /tmp/mcp.log"
fi
```

---

## 参考

- 小红书 MCP 项目：https://github.com/xpzouying/xiaohongshu-mcp
- OpenClaw 文档：https://docs.openclaw.ai
