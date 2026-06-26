# 🧊 xueqiu-collector — 雪球帖子全量采集 Skill

> 一键采集任意雪球用户的全部帖子，自带智能分析引擎，零 API、零 token 消耗。

## ✨ 为什么需要这个 Skill？

雪球是中国最大的投资者社区，上面有大量高质量的投资分析、操作记录和讨论。但这些内容**只能通过浏览器查看**，雪球没有提供公开的数据导出 API。

**xueqiu-collector 解决这个问题：**
- 🔍 **全量采集** — 一个人的所有帖子（原创 + 评论），一条不漏
- 🧠 **智能分析** — 采集的同时自动做 V4 规则分析，不需要调用任何 AI API
- 💾 **多格式输出** — SQLite 数据库 + JSON + Markdown，方便后续处理
- 🖼️ **图片 OCR** — 帖子里的截图自动识别文字

## 🎯 核心能力

### 1. 全量 / 增量采集
- 自动判断模式：首次全量采集，后续只抓新帖
- 支持强制刷新列表、重新采集正文
- 内置反爬虫：随机延迟 2-5 秒、自动重试、429 限流检测
- 连续 N 页无新帖自动停止（避免傻翻到最后一页）

### 2. 完整正文提取
- 基于 playwright-cli 浏览器自动化，获取完整渲染后的正文
- YML 快照 → Markdown 格式化（支持引用块、代码块、列表）
- 评论帖三种格式全覆盖（A/B/C 型）
- 图片自动下载并本地嵌入 Markdown

### 3. V4 规则分析（零 AI 消耗！）

| 分析维度 | 说明 |
|---------|------|
| **帖子类型** | 原创 / 评论 / 错误 / 空内容 |
| **投资相关性** | high / medium / low / none |
| **情感倾向** | 看多 / 看空 / 中性 |
| **操作意图** | 买入 / 卖出 / 持有 / 观察 |
| **主题标签** | 估值分析、财务分析、操作记录…（12类）|
| **质量评分** | 0-5 分（基于字数+相关性+类型综合）|

> 不需要 OpenAI/DeepSeek/任何 AI API。纯规则引擎，基于关键词匹配和启发式算法。

### 4. 图片 OCR
- Windows: `winocr`（系统内置，无需安装）
- 降级方案: `tesseract`（需单独安装）
- 识别结果存入数据库，可搜索图片中的文字

### 5. 多格式数据导出

```
data/{昵称}/
├── posts_full.json          ← 所有帖子（JSON 数组，时间倒序）
├── posts_full.md            ← 所有帖子（Markdown 格式）
├── classified/              ← 按分类拆分
│   ├── 腾讯控股.json
│   ├── 操作日记.json
│   └── ...
├── md/                      ← 按分类 Markdown
└── images/                  ← 帖子图片
```

数据库表 `xueqiu_posts` 包含 **32 个字段**，覆盖基础信息 + V4 分析 + 互动数据 + OCR 内容。

## 🚀 快速开始

### 前置条件

```bash
# ① 检测环境（首次必跑！）
py scripts/check_env.py

# 如果显示 "🎉 环境就绪"，就可以直接用了
# 如果缺依赖，脚本会告诉你怎么装
```

**必须的依赖（5项）：**
- ✅ Python 3.10+
- ✅ Node.js + npx（用于 playwright-cli）
- ✅ Edge 浏览器 + 已登录雪球的 Profile
- ✅ playwright-cli npm 包（SkillHub 工具链通常已包含）
- ✅ SQLite（Python 内置，无需安装）

**可选增强（3项）：**
- ⚡ winocr — Windows 原生 OCR（`pip install winocr pillow`）
- ⚡ tesseract — 备选 OCR 引擎
- ⚡ Pillow — 图片处理库（winocr 需要）

### 三步上手

```bash
# Step 1: 环境检测
py scripts/check_env.py

# Step 2: 首次采集（向导模式，会提示输入昵称和 URL）
py scripts/collect.py

# Step 3: 补做规则分析（对已采集的帖子）
py scripts/analyze.py --db data/xueqiu.db --missing
```

或者一行命令跳过向导：

```bash
py scripts/collect.py --author "你的昵称" --url "https://xueqiu.com/u/你的ID"
```

### 高级用法

```bash
# 只采最新 10 条（快速测试）
py ... --force-collect --latest --limit 10

# 强制扫描列表找新帖（不采正文）
py ... --refresh-list

# 自定义数据库和输出目录
py ... --db "my_data.db" --out-dir "./output"

# 指定 npx 和 Edge 路径（通常自动探测）
py ... --npx "C:\path\to\npx.cmd" --edge-profile "C:\path\to\Edge\User Data"
```

## 📂 文件结构

```
xueqiu-collector/
├── SKILL.md                    # Skill 定义（触发词 + SOP）
├── README.md                   # 本文件
├── scripts/
│   ├── collect.py              # 核心采集脚本（~900行）
│   ├── analyze.py              # 独立 V4 规则分析脚本
│   └── check_env.py            # 环境检测工具（8项检查 + 自动修复）
└── references/
    └── category_keywords.json  # 股票/主题分类关键词（可自定义）
```

**零外部依赖**——只用 Python 标准库（json/sqlite3/subprocess/urllib/pathlib/re）。

## 🔧 自定义配置

### 分类关键词

编辑 `references/category_keywords.json`，添加你关注的股票：

```json
{
  "腾讯控股": ["腾讯", "TX", "00700", "微信"],
  "招商银行": ["招行", "招商银行", "03968"],
  "我的持仓": ["股票A", "股票B", "代码C"]
}
```

采集时会根据关键词自动给帖子打上分类标签。

### 反爬参数（在 collect.py 顶部调整）

```python
MIN_DELAY      = 2.0   # 最小请求间隔（秒）
MAX_DELAY      = 5.0   # 最大请求间隔（秒）
ERROR_DELAY    = 8.0   # 错误后延迟（秒）
MAX_RETRIES    = 3      # 最大重试次数
stop_on_no_new = 3     # 连续几页无新帖后停止
```

## 📊 典型应用场景

1. **投资记录归档** — 把自己在雪球的发帖全部备份到本地，建立完整的投资决策记录
2. **大V 跟踪** — 采集关注的大V历史帖子，用数据分析其投资风格和准确率
3. **舆情监控** — 定期采集某股票相关讨论，跟踪市场情绪变化
4. **知识沉淀** — 将高质量的投资分析帖子整理成个人知识库

## ⚠️ 注意事项

1. **Edge 登录态**：首次运行会启动 Edge 导航到目标页面，确保已登录雪球账号
2. **采集速度**：内置随机延迟，每条正文 2-5 秒，每 20 条休息 8-12 秒（防封号）
3. **日志文件**：同时写到终端屏幕和日志文件（`_Tee` 双写机制），可用 `type logs/xueqiu_collect.log` 查看
4. **合规使用**：请遵守雪球服务条款，仅用于个人数据备份和分析

## 技术架构

```
用户输入 (昵称 + URL)
        ↓
  列表页爬取 (playwright-cli snapshot)
  → 提取 post_id / 标题 / 摘要 / 时间
  → 增量去重（数据库已存在的跳过）
        ↓
  正文页爬取 (playwright-cli goto + snapshot)
  → YML 快照解析 → Markdown 格式化
  → 图片下载 → OCR 识别
        ↓
  V4 规则分析（纯本地，零 API 调用）
  → 帖子类型 / 相关性 / 情感 / 意图 / 标签 / 评分
        ↓
  三格式持久化 (SQLite + JSON + MD)
```

## License

MIT License — 自由使用、修改、分发。
