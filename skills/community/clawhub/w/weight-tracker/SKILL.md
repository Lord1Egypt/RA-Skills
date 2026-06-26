---
name: weight-tracker
description: 减肥进度追踪助手。用户告诉 AI 今天的体重，AI 自动帮您记录并生成漂亮的图表，清晰展示减肥进度。支持中英文界面，macOS/Windows/Linux 多平台使用。当用户说"记录体重"、"今天体重"、"减肥打卡"、"体重多少"时自动触发。
---

# Weight Tracker - 体重追踪器

可视化追踪减肥进度，支持图表展示、进度对比、数据导出、中英文双语、macOS/Windows/Linux 跨平台。

## 文件结构

```
weight-tracker/
├── SKILL.md
└── assets/
    ├── jianfei.html          # 主页面
    ├── config.json            # 用户配置
    ├── weight_history.json    # 体重数据
    └── setup.sh              # 跨平台初始化向导
```

## 快速开始

### 1. 初始化（仅首次需要）

```bash
cd <skill-directory>/assets
chmod +x setup.sh
./setup.sh
```

向导会自动检测平台（macOS/Windows/Linux），并引导配置：
- 语言选择（en/zh）
- 端口选择（自动检测可用端口）
- 减肥目标（起始/目标体重、日期周期）
- 初始体重记录

### 2. 启动服务

**macOS:**
```bash
cd <jianfei.html目录>
python3 -m http.server <PORT>
```

**Windows (PowerShell):**
```powershell
cd <jianfei.html目录>
python -m http.server <PORT>
```

**Linux:**
```bash
cd <jianfei.html目录>
python3 -m http.server <PORT>
```

### 3. 打开页面

浏览器访问: `http://localhost:<PORT>/jianfei.html`

## 配置文件说明

### config.json

```json
{
  "title": "Weight Tracker",
  "language": "en",
  "port": 8080,
  "startWeight": 70,
  "targetWeight": 60,
  "startDate": "2026-01-01",
  "endDate": "2026-03-31",
  "startDateLabel": "01/01",
  "endDateLabel": "03/31"
}
```

**关键字段：**
- `language`: `zh` = 中文界面，`en` = 英文界面
- `port`: 本地服务器端口号
- `startDate` / `endDate`: 减肥周期（YYYY-MM-DD 格式）

### weight_history.json

```json
{
  "records": [
    {"date": "2026-03-29", "weight": 68.5}
  ]
}
```

## 切换语言

修改 `config.json` 中的 `language` 字段为 `zh` 或 `en`，然后刷新页面即可切换界面语言。

## AI 工作流程

### 记录体重数据

1. 读取 `weight_history.json`
2. 解析 `records` 数组
3. 检查当天是否已有记录
4. 如果有，更新体重值；如果没有，添加新记录
5. 写回文件

### 打开浏览器并截图（跨平台）

1. **启动本地服务器**
   ```bash
   cd <jianfei.html目录>
   
   # macOS
   python3 -m http.server <PORT>
   
   # Windows (PowerShell)
   python -m http.server <PORT>
   
   # Linux
   python3 -m http.server <PORT>
   ```

2. **打开浏览器**
   - 启动 HTTP 服务器后等待 1-2 秒
   - 用 browser 工具打开 `http://localhost:<PORT>/jianfei.html`

3. **调整视口**
   - 内容区尺寸：450 × 749 CSS像素
   - 视口调整为内容区的 110%：495 × 824

4. **截图**
   - 使用 browser 工具的 screenshot 功能

5. **关闭浏览器并停止服务器** ⭐重要
   - 关闭浏览器标签页
   - **停止 HTTP 服务器**：

   ```bash
   # macOS
   lsof -ti :<PORT> | xargs kill
   
   # Linux
   fuser -k <PORT>/tcp 2>/dev/null || kill $(lsof -ti:<PORT>) 2>/dev/null
   
   # Windows (PowerShell)
   netstat -ano | findstr :<PORT>
   taskkill /PID <PID> /F
   ```

## 快捷键

- 按 `W` 键：导出当前数据为 JSON 文件

## 关键实现细节

1. **HTML 通过 fetch API 加载外部 JSON 文件**
2. **必须通过 HTTP 服务器访问**（file:// 不支持 fetch）
3. **setup.sh 自动检测平台并适配命令**
4. **端口默认为 8080，可在 config.json 中修改**
5. **日期格式化兼容 macOS (date -j) 和 Linux (date -d)**

## 目录规划建议

用户应将文件放在自己的目录下，例如：
```
~/Desktop/weight-tracker/
├── jianfei.html
├── config.json
├── weight_history.json
└── setup.sh
```
