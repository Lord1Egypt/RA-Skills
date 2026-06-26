---
name: xhs-monitor
description: 小红书竞品监控 - 自动采集竞品笔记，推送飞书通知，写入数据看板
homepage: https://github.com/openclaw/xhs-monitor
metadata:
  {
    "openclaw": {
      "emoji": "📕",
      "requires": {
        "bins": ["node"],
        "env": ["PATH"]
      },
      "install": [
        {
          "id": "puppeteer",
          "kind": "npm",
          "module": "puppeteer-core",
          "label": "安装 puppeteer-core"
        }
      ]
    }
  }
---

# 小红书竞品监控系统 (xhs-monitor)

自动采集小红书竞品账号的笔记，解析有价值内容，推送到飞书。

## 功能

- ✅ 自动采集多个竞品账号的笔记
- ✅ 本地去重（避免重复推送）
- ✅ 智能解析（提取标题、正文、商品、直播时间）
- ✅ 飞书卡片推送
- ✅ 定时自动运行（14:06 / 18:06 / 21:06）
- ✅ 支持手动触发

## 安装

### 方式一：使用 ClawHub 安装（推荐）

```bash
# 安装 Skill
npx clawhub@latest install xhs-monitor

# 或使用 clawhub CLI
clawhub install xhs-monitor
```

### 方式二：手动安装

```bash
# 克隆项目
git clone https://github.com/你的用户名/xhs-monitor.git
cd xhs-monitor

# 安装依赖
npm install puppeteer-core
```

### 3. 配置

```bash
# 复制配置模板
cp config.example.js config.js
cp notify.example.js notify.js
```

### 4. 配置账号

编辑 `config.js`：

```javascript
// 竞品账号列表（必填）
// 从小红书用户主页URL获取：xiaohongshu.com/user/profile/用户ID
const ACCOUNTS = [
  { name: '账号名1', id: '用户ID1' },
  { name: '账号名2', id: '用户ID2' },
];

// 账号主页URL映射（用于跳转链接）
const ACCOUNT_URLS = {
  '账号名1': 'https://www.xiaohongshu.com/user/profile/用户ID1',
  '账号名2': 'https://www.xiaohongshu.com/user/profile/用户ID2',
};
```

### 5. 启动浏览器（调试模式）

首次需要手动启动浏览器并扫码登录：

```bash
# Mac
export CHROMIUM_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROMIUM_PATH" \
  --remote-debugging-port=9223 \
  --user-data-dir="$HOME/xhs-monitor/data/browser" \
  "https://www.xiaohongshu.com/"

# 或使用 run.sh（自动检测）
bash run.sh
```

扫码登录后，浏览器保持打开状态即可。

### 6. 运行

```bash
cd xhs-monitor/src
node main.js
```

## 配置说明

### config.js

| 参数 | 说明 | 示例 |
|------|------|------|
| ACCOUNTS | 监控的账号列表 | `{ name: '账号名', id: '用户ID' }` |
| ACCOUNT_URLS | 账号主页URL映射 | 用于跳转链接 |

### notify.js（可选）

如需使用飞书通知，需要：
1. 配置飞书应用权限：`im:message.send_as_user`
2. 如需写入多维表格，配置 BITABLE_CONFIG

## 项目结构

```
xhs-monitor/
├── src/
│   ├── main.js         # 主程序入口
│   ├── config.js      # 账号配置 ⚠️ 需复制 config.example.js
│   ├── config.example.js  # 配置模板
│   ├── notify.js      # 飞书推送 ⚠️ 需复制 notify.example.js
│   ├── notify.example.js  # 推送模板
│   ├── parser.js      # 内容解析
│   ├── dedupe.js      # 去重模块
│   └── scraper.js     # 浏览器采集
├── data/
│   └── history.csv    # 历史记录（自动生成）
└── README.md
```

## 使用方式

### 手动运行

```bash
node src/main.js
```

### 定时任务（Mac）

编辑 crontab：

```bash
crontab -e

# 添加以下行：
6 14 * * * /usr/bin/node /path/to/xhs-monitor/src/main.js
6 18 * * * /usr/bin/node /path/to/xhs-monitor/src/main.js
6 21 * * * /usr/bin/node /path/to/xhs-monitor/src/main.js
```

## 常见问题

### Q: 浏览器需要一直开着吗？
A: 是的，首次登录后保持浏览器打开，程序会复用会话。

### Q: 为什么抓不到内容？
A: 检查浏览器是否以调试模式运行（--remote-debugging-port=9222）。

### Q: 如何添加新账号？
A: 编辑 config.js 中的 ACCOUNTS 数组。

## 待优化

- [ ] 多维表格自动写入
- [ ] LLM智能解析
- [ ] 笔记详情链接获取
- [ ] 登录状态自动检测
