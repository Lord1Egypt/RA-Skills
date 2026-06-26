# 浏览器自动化助手

## 前置条件

1. 启动Chrome远程调试：
```bash
chrome.exe --remote-debugging-port=9222
```

## 使用方法

```bash
cd scripts
node cdp-helper.js --url=https://example.com
```

## 功能

- 连接Chrome CDP
- 获取WebSocket URL
- 验证连接状态
