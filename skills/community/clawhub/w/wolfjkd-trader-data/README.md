# wolfjkd-trader-data

<p align="center">
  <strong>A股数据获取体系 + 多源智能路由</strong><br>
  <i>零依赖 · 自动故障切换 · 开箱即用</i>
</p>

---

## ✨ 这是什么？

**wolfjkd-trader-data** 是一个面向A股交易员的完整数据获取解决方案，核心亮点：

| 能力 | 说明 |
|------|------|
| 📊 **5大数据源** | 腾讯实时行情、ftshare公告、Wind深度数据、AkShare、WebSearch |
| 🔄 **智能路由** | `data_router.py` — 自动探测所有数据源健康状态，评分择优 |
| ⚡ **毫秒级响应** | 腾讯行情接口 <200ms，并行多线程探测 |
| 🔌 **零依赖** | data_router.py 仅用Python标准库，无需pip install任何包 |
| 🛡️ **自动容错** | 某个源挂了自动切到下一个，报告标注来源和评分 |

### 核心架构

```
请求 → 并行探测(腾讯 + Wind + ftshare) → 评分排序 → 选最优
                                              ↓
                                    某源挂了？自动降级到备选
```

## 🚀 快速开始（3步）

### 1. 下载

```bash
git clone https://github.com/wolfjkd/wolfjkd-trader-data.git
cd wolfjkd-trader-data
```

### 2. 健康检测

```bash
python data_router.py health
```

预期输出：
```
====================================================================
    数据源健康检测  2026-05-22 10:30:00
====================================================================

[1/3] 检测腾讯行情接口...
  [+] [TENCENT] 评分: 100.0/100 (A级)
     响应时间: 196ms
     可用性: 100 | 及时性: 100 | 质量: 100

[2/3] 检测Wind万得...
  [!] Wind未安装（路径不存在: ...）

[3/3] 检测FTShare公告...
  [+] [FTSHARE] 评分: 88.0/100 (B级)
     响应时间: 1800ms
     ...

====================================================================
    汇总
====================================================================
数据源       状态      评分      响应       等级
--------------------------------------------------------------------
tencent        OK    100.0     196ms       A
wind           FAIL    0.0      N/A        D  
ftshare        OK     88.0   1800ms       B  

[*] 最佳数据源: tencent（评分 100.0, 等级 A）
```

### 3. 查行情

```bash
# 三大指数
python data_router.py quote --codes sh000001,sz399001,sz399006

# 自选股（修改WATCHLIST后）
python data_router.py watchlist

# JSON输出（供脚本调用）
python data_router.py quote --codes sh600519 --json

# 多源对比
python data_router.py compare --code 600519.SH --type quote
```

## 📁 文件说明

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 完整文档：数据源配置、API速查表、部署步骤、故障排除 |
| `data_router.py` | 多源智能路由脚本（~795行），核心执行文件 |
| `README.md` | 本文件，项目介绍和快速上手 |

## ⚙️ 配置你的自选股

编辑 `data_router.py` 中的 `WATCHLIST` 列表：

```python
WATCHLIST = [
    ("sh600519", "贵州茅台"),
    ("sz000001", "平安银行"),
    # 添加你关注的股票...
]
```

格式：`("sh" + 6位代码, "名称")` — 上海以`sh`开头，深圳以`sz`开头。

## 📊 数据源覆盖矩阵

| 数据类型 | 免费源 | 付费增强源 |
|---------|--------|-----------|
| 实时行情快照 | ✅ 腾讯接口 (毫秒级) | Wind (字段更丰富) |
| 历史K线 | AkShare (腾讯源) | Wind (质量更高) |
| A股公告 | ✅ ftshare (结构化) | Wind RAG (语义搜索) |
| 财经新闻 | WebSearch | Wind RAG |
| 财务报表/ROE | - | ✅ Wind |
| 技术指标(MACD等) | - | ✅ Wind |
| 板块涨跌/资金流 | WebSearch | ✅ Wind index_data |
| 宏观指标(CPI等) | WebSearch | ✅ Wind economic_data |
| 大宗商品(金/银/油) | ✅ 腾讯接口 | - |
| 美股指数 | ✅ 腾讯接口 | Wind global_stock |

> 💡 **免费模式**：仅使用腾讯+ftshare+WebSearch，已覆盖80%的日常需求。Wind是可选增强。

## 🔄 智能路由评分模型

每次查询都会对数据源进行三维打分：

| 维度 | 权重 | 说明 |
|------|------|------|
| 可用性 | 40% | 连通且有有效数据 = 100分 |
| 及时性 | 25-30% | 腾讯<500ms满分，Wind<1.5s满分 |
| 质量 | 30-35% | 数据完整度 + 数值合理性 |

**等级**：A≥85 / B≥70 / C≥50 / D<50（D级自动弃用）

## 🔧 进阶配置

### 安装Wind（可选，需要API Key）

详见 [SKILL.md](./SKILL.md) 第5节。

```bash
# 安装Skill
npx skills add https://gitee.com/wind_info/wind-skills.git --skill wind-mcp-skill -g -y

# 配置Key
node <WIND_SKILL_DIR>/scripts/cli.mjs open-portal
node <WIND_SKILL_DIR>/scripts/cli.mjs setup-key <YOUR_KEY> --scope global
```

### 安装ftshare公告（推荐）

```bash
npx openclaw skills install shawn92/ftshare-announcement-data
```

### 集成到WorkBuddy Skill系统

将整个目录放到你的skills文件夹：

```bash
cp -r wolfjkd-trader-data ~/.workbuddy/skills/
# 或
cp -r wolfjkd-trader-data ~/.openclaw/workspace/skills/
```

## 使用场景

### 场景1：AI Agent定时报告

结合 WorkBuddy Automation 定时生成晚间财经报告：

```bash
#!/bin/bash
# evening_report.sh
echo "=== 数据源健康 ==="
python data_router.py health
echo ""
echo "=== 行情快照 ==="
python data_router.py quote --json
echo ""
echo "=== 自选股 ==="
python data_router.py watchlist --json
```

### 场景2：交易盯盘辅助

```bash
# 每30秒刷新自选股
watch -n 30 'python data_router.py watchlist'
```

### 场景3：程序化接入

```python
import subprocess, json

# 获取JSON格式行情
result = subprocess.run(
    ['python', 'data_router.py', 'quote', '--codes', 'sh600519,sz000001', '--json'],
    capture_output=True, text=True
)
data = json.loads(result.stdout)

print(f"最佳数据源: {data['best_source']}")
for stock in data['data']:
    print(f"{stock['name']}: {stock['price']} ({stock['change_pct']}%)")
```

## 已知限制

| 限制 | 影响 | 解决方案 |
|------|------|---------|
| akshare东方财富被拒 | 板块数据不可用 | Wind替代或WebSearch |
| Wind日额度限制 | 不能无限调用 | 优先腾讯做实时快照 |
| 单工具单标的(Wind) | 批量需循环 | for循环逐只查询 |
| 无本地缓存 | 每次都实时探测 | 后续版本加入 |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.0 | 2026-05-22 | 新增 data_router.py 多源智能路由 |
| v2.0 | 2026-05-22 | 整合Wind万得金融8大能力 |
| v1.0 | 2026-05-20 | 初始版：腾讯+ftshare+AkShare体系 |

## License

MIT License — 自由使用、修改、分发。

## 致谢

- [腾讯财经](https://qt.gtimg.cn/) — 免费实时行情接口
- [Wind万得金融](https://www.wind.com.cn/) — 专业金融数据
- [ftshare-announcement-data](https://clawhub.ai) — A股公告数据
- [AkShare](https://akshare.akfamily.xyz/) — Python财经数据接口库

---

<p align="center">
  <sub>Made with trading discipline by <a href="https://github.com/wolfjkd">wolfjkd</a></sub>
</p>
