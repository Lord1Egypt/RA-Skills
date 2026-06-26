---
name: toutiao-publisher
description: |
  今日头条微头条自动发布工具。自动发布短内容到今日头条平台，支持文本和图片。
  使用场景：(1) 用户说"发布头条"、"发微头条"、"头条发布"时触发 (2) 
  需要自动发布社交媒体内容时 (3) 需要定时发布今日头条时
---

# 今日头条发布工具

使用此 skill 可以自动发布微头条到今日头条平台。

## 前置要求

1. **Chrome 远程调试已启动**：
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```

2. **Chrome 已登录今日头条**：访问 https://mp.toutiao.com 完成登录

3. **Python 依赖**：
   ```bash
   pip3 install playwright --break-system-packages
   playwright install chromium
   ```

## 使用方法

### 基本发布

```bash
cd ~/.openclaw/workspace/skills/toutiao-publisher/scripts
python3 toutiao_publish.py "要发布的文字内容"
```

### 带话题发布

```bash
# 单个话题
python3 toutiao_publish.py "内容文字" --topic "#AI#"

# 多个话题
python3 toutiao_publish.py "内容文字" --topic "#AI#,#OpenClaw#,#科技#"
```

### 带图片发布

```bash
python3 toutiao_publish.py "内容" --image /path/to/image.jpg
```

### 从文件读取内容

```bash
python3 toutiao_publish.py -f content.txt
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| content | 发布内容 | `"今天天气很好"` |
| -f, --file | 从文件读取 | `-f post.txt` |
| -i, --image | 图片路径 | `--image pic.jpg` |
| -t, --topic | 话题标签，多个用逗号分隔 | `--topic "#AI#,#OpenClaw#"` |
| --headless | 无头模式 | `--headless` |
| --no-wait | 不等待登录 | `--no-wait` |

## 话题格式

话题必须使用 **双 #** 格式：
- ✅ 正确：`#AI#`、`#OpenClaw#`、`#科技前沿#`
- ❌ 错误：`#AI`、`AI#`

多个话题用逗号分隔，脚本会自动用空格连接。

## 输出

- **成功截图**：`~/Desktop/toutiao_publish_success.png`
- **错误截图**：`~/Desktop/toutiao_error.png`

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 无法连接 Chrome | 确保 Chrome 已启动并开启 9222 端口 |
| 未检测到登录 | 在 Chrome 中访问 mp.toutiao.com 完成登录 |
| 发布失败 | 检查网络连接，查看错误截图 |
