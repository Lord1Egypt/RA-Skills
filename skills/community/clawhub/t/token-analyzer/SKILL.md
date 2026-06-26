---
name: token-analyzer
version: 2.5.0
description: "基于官方 GMGN API 的代币分析工具。通过合约地址查询代币在 SOL/BSC/Base 链上的准确市场数据、安全检测、KOL 分析、开发者分析和 AI 智能分析（叙事/筹码/老鼠仓/机器人）。支持自动识别链。"
---

# Token Analyzer v2.5 - 基于官方 GMGN API + AI 智能分析

## 概述

此技能使用官方 GMGN API 接口获取代币的准确数据，支持 Solana (SOL)、Binance Smart Chain (BSC)、Base 链。

## 前置条件

### 方案 1：使用带插件的 Chrome（推荐）

此技能需要通过浏览器访问 GMGN API 以绕过 Cloudflare 防护。

#### 1. 停止 OpenClaw 自带浏览器

```bash
# 查看当前浏览器进程
ps aux | grep chrome

# 如果有 OpenClaw 自带的浏览器（端口 18800），建议停止
```

#### 2. 启动带插件的 Chrome（开放 CDP 端口 9222）

**安装 OpenClaw Browser Relay 插件：**
- Chrome 应用商店：https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp
- 或手动下载解压后加载

**启动 Chrome：**

```bash
xvfb-run -a env -u DBUS_SESSION_BUS_ADDRESS -u DBUS_SYSTEM_BUS_ADDRESS \
  google-chrome \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir=/root/chrome-profile \
  --load-extension=/path/to/openclaw-browser-relay \
  --no-sandbox --disable-dev-shm-usage \
  --disable-gpu --use-gl=swiftshader \
  --disable-features=VizDisplayCompositor,DBus \
  --disable-vulkan \
  about:blank
```

**注意：** 将 `/path/to/openclaw-browser-relay` 替换为实际的插件路径。

验证 CDP 可用：
```bash
curl -s http://127.0.0.1:9222/json/version
```

#### 3. 配置 OpenClaw 连接到远程 Chrome

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "browser": {
    "defaultProfile": "myremote",
    "attachOnly": true,
    "profiles": {
      "myremote": {
        "cdpUrl": "http://127.0.0.1:9222",
        "color": "#00AA00"
      }
    }
  }
}
```

- `attachOnly: true` - OpenClaw 不启动浏览器，只连接已有的
- `cdpUrl` - 指向你的 Chrome CDP 端口

#### 4. 测试连接

```bash
openclaw browser --browser-profile myremote tabs
openclaw browser --browser-profile myremote open https://gmgn.ai
```

### 方案 2：使用 OpenClaw 自带浏览器

如果不需要插件，可以直接使用 OpenClaw 自带浏览器（但可能遇到 Cloudflare 拦截）。

## 核心改进

### v2.0 更新
- ✅ 使用官方 GMGN API 接口
- ✅ 修复数据不准确问题
- ✅ 移除 Chrome DevTools 依赖
- ✅ 更快的响应速度
- ✅ 更准确的数据

## 核心功能

### 1. 多链支持
- Solana (SOL)
- Binance Smart Chain (BSC)
- Base
- 自动检测代币所属链

### 2. 数据来源
- 使用官方 GMGN API
- 实时市场数据
- 安全检测信息
- 持有者分析
- KOL 持仓分析
- 开发者历史分析

### 3. AI 评分系统
- Early Score 评分 (1-10分)
- Conviction 信心评分 (1-10分)
- 考虑流动性、市值、持有者数量
- 风险等级识别（🟢 Low / 🟡 Medium / 🔴 High）
- Top10 持仓集中度分析

### 4. 安全检测
- 蜜罐检测
- 开源验证
- 权限放弃检查
- 税率分析
- 持仓集中度

### 5. KOL 分析
- 显示已上车的知名持有者
- 包含 KOL 名称和排名
- 统计 KOL 总数

### 6. 开发者分析 🆕
- 开发者名称和推特账号
- 历史发币总数
- 本币盈亏情况
- PNL 倍数
- 历史成功项目（市值 > 1M 的代币）

## 使用方法

直接发送合约地址：
```
0x768f922312e223d9276d8c06d3226e35514e4444
```

指定链：
```
bsc 0x768f922312e223d9276d8c06d3226e35514e4444
```

## 输出示例

```
🔔 代币分析 | BSC

死对头 ($死对头) | BSC

CA: 0xe1c73aa0ac443f69aec9704d8b87209aa0a54444
| 指标 | 数值 |
| ---------- | ----------------- |
| 💰 价格 | $0.00012277094 |
| 📊 市值 | $122.8K |
| 💧 流动性 | $35.8K |
| ⚡ 5m | +11.41% |
| ⏱️ 1h | +167.01% |
| 📈 24h | +2729.54% |
| 👥 Holders | 677 |
| 📦 24h Vol | $652.1K (531% of MC) |

• Early Score: 6/10
• Conviction: 5/10
• Risk: 🟡 Medium
• Action: 👀 可以关注
• Why Alpha: 这支名为"死对头"的 BSC 代币，24小时内上涨 2729.54%，1小时内上涨 167.01%。当前市值约为 $122.8K，流动性为 $35.8K。24小时交易量为 $652.1K，占市值的 531%，交易较为活跃。持有者数量为 677 人。
• Narrative Vibe: BSC 生态, MEME币
• 🎯 已上车KOL: 阿峰_Afeng(TOP1) (共1个)
• 👨💻 开发者: joao victor (0x05f0...848c) | 发币4个 | 本币盈利$5.2K | PNL 7.4x
• 💎 历史成功项目: 哈基米($哈基米) $9.93M 0x82ec...4444

🐦 Twitter | 🔗 GMGN
```

## 技术说明

### 依赖
- Python 3.7+
- websockets
- aiohttp (可选，用于备用方案)

### API 接口
使用以下 GMGN API：
- `/api/v1/token_stat` - 代币统计
- `/api/v1/mutil_window_token_security_launchpad` - 安全检测
- `/vas/api/v1/search_v3` - 搜索和基础信息
- `/api/v1/token_mcap_candles` - K线数据（5分钟、1小时涨跌幅）
- `/api/v1/mutil_window_token_link_rug_vote` - 链接信息
- `/vas/api/v1/token_holders` - KOL 和开发者持仓分析
- `/api/v1/dev_created_tokens` - 开发者历史代币

### 安装依赖
```bash
apt-get install -y python3-websockets python3-aiohttp
```

或使用 pip：
```bash
pip3 install websockets aiohttp
```

## 注意事项

- 需要配置浏览器 CDP 连接
- 通过浏览器绕过 Cloudflare 防护
- 数据直接来自 GMGN API
- 响应速度快，数据准确

## 更新日志

### v2.5.0 (2026-03-06)
- ✅ 新增 🤖 AI 机器人分析模块
- ✅ 使用 bird CLI 获取开发者推特数据
- ✅ 分析推特账号：粉丝数、Bio、推文内容
- ✅ 识别风险信号：rug、scam、dev wallet 等关键词
- ✅ 自动判断身份和风险等级
- ✅ 支持从推文链接提取用户名

### v2.4.0 (2026-03-06)
- ✅ 新增自动识别链功能
- ✅ 支持只传地址，自动判断 BSC/BASE/SOL
- ✅ 优化查询顺序：BSC 优先（更常用）
- ✅ 使用方式：`python3 token_query_v2.py <address>`

### v2.3.0 (2026-03-06)
- ✅ 新增三个AI智能分析模块
- 📖 代币叙事分析：基于描述和交易热度分析代币故事/概念
- 💰 筹码分布分析：分析Top10持有者盈亏、CEX地址、控盘风险
- 🐀 老鼠仓分析：检测早期买入者的sniper/bundler标签，识别内幕交易
- ✅ 新增交易记录数据采集（最近50条）
- ✅ 新增持有者详细列表数据采集（前100个）
- ✅ 所有分析基于真实数据，非固定模板

### v2.2.2 (2026-03-05)
- 🐛 修复 PNL 为 None 时的格式化错误
- ✅ 优化错误处理

### v2.2.1 (2026-03-05)
- 📝 更新文档：添加开发者分析功能说明

### v2.2.0 (2026-03-05)
- ✅ 新增开发者分析功能
- ✅ 显示开发者名称、推特账号
- ✅ 显示历史发币总数
- ✅ 显示本币盈亏和 PNL 倍数
- ✅ 显示历史成功项目（市值 > 1M）

### v2.1.0 (2026-03-05)
- ✅ 新增开发者基础信息展示

### v2.0.0 (2026-03-05)
- ✅ 重构为使用官方 GMGN API
- ✅ 通过浏览器 CDP 绕过 Cloudflare
- ✅ 新增 KOL 持仓分析
- ✅ 新增 Early Score 和 Conviction 评分
- ✅ 新增 Why Alpha 智能分析
- ✅ 新增 Narrative Vibe 叙事识别
- ✅ Markdown 表格格式输出
- ✅ 完整推特链接显示
- ✅ 移除 Chrome DevTools 依赖
- ✅ 移除 Ave.ai 集成
- ✅ 修复数据不准确问题

### v1.0.1
- 初始版本
- 使用 Chrome DevTools + Ave.ai
