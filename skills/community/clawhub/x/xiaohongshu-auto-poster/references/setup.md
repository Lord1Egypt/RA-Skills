# 小红书 MCP 服务配置教程

## 系统要求

- macOS（Apple Silicon M1/M2/M3）或 Linux
- 已安装 Node.js 18+
- 小红书账号（手机号或微信登录）

## 第一步：下载 MCP 服务

访问 GitHub：https://github.com/xpzouying/xiaohongshu-mcp/releases

下载对应系统的二进制文件：
- macOS Apple Silicon：`xiaohongshu-mcp-darwin-arm64`
- macOS Intel：`xiaohongshu-mcp-darwin-amd64`
- Linux AMD64：`xiaohongshu-mcp-linux-amd64`

## 第二步：赋予执行权限

```bash
chmod +x xiaohongshu-mcp-darwin-arm64
```

## 第三步：启动服务

```bash
# 后台运行
nohup ./xiaohongshu-mcp-darwin-arm64 > mcp.log 2>&1 &

# 验证服务运行
curl -s -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{},"id":1}'
```

看到返回包含 `"protocolVersion":"2025-06-18"` 即成功。

## 第四步：登录小红书

对我说「小红书重新登录」，我会帮你获取登录二维码。

用小红书 App 扫描二维码完成授权。

## 验证登录状态

对我说「检查小红书登录状态」。

## 设置开机自启动（macOS）

```bash
# 创建 plist 文件
cat > ~/Library/LaunchAgents/com.xiaohongshu.mcp.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.xiaohongshu.mcp</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/xiaohongshu-mcp-darwin-arm64</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/xiaohongshu-mcp</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.xiaohongshu.mcp.plist
```

把 `YOUR_USERNAME` 替换成你的用户名。

## 常见问题

**服务启动后立即退出？**
```bash
# 查看错误日志
cat mcp.log
```

**端口 18060 被占用？**
修改启动命令指定其他端口：
```bash
./xiaohongshu-mcp-darwin-arm64 --port 18061
```
