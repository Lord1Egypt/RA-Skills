# Tencent Docs Reader（腾讯文档读取器）📄

> Author: [Cm-wenge](https://github.com/Cm-wenge) | License: MIT

让 AI Agent 能够读取腾讯文档在线表格数据的工具。

## 这是什么？

腾讯文档用 Canvas 渲染表格，导致：
- 大模型拿到链接也读不了内容
- 传统网页抓取（DOM解析、accessibility tree）全部失效
- 没有公开 API 可以调用

这个工具通过浏览器自动化 + 复制粘贴的方式，成功提取腾讯文档表格内容。

## 快速开始

### 安装依赖

```bash
# 安装 agent-browser
npm install -g agent-browser

# 启动 agent-browser 守护进程
agent-browser start
```

### 使用

```bash
# 克隆仓库
git clone https://github.com/Cm-wenge/tencent-docs-reader.git
cd tencent-docs-reader

# 读取腾讯文档表格
python scripts/read_sheet.py --url "https://docs.qq.com/sheet/YOUR_SHEET_ID" --tab "SheetName"

# 保存到文件
python scripts/read_sheet.py --url "https://docs.qq.com/sheet/YOUR_SHEET_ID" --tab "SheetName" --output result.txt
```

### 在 OpenClaw 中使用

将本项目复制到 OpenClaw 的 skills 目录：

```bash
cp -r tencent-docs-reader ~/.openclaw/skills/
```

或通过 ClawHub 安装（即将上线）：

```bash
npx clawhub install tencent-docs-reader
```

## 输出格式

制表符分隔的纯文本：

```
姓名    年龄    城市
张三    30      北京
李四    25      上海
```

## 限制

- 仅支持**在线表格**，不支持在线文档和幻灯片
- 仅支持**所有人可读**的共享文档
- 超大表格可能较慢
- 腾讯文档前端改版可能导致失效

## License

MIT License - see [LICENSE](LICENSE)
