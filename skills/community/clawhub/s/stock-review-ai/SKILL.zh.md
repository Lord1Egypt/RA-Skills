---
name: stock-review
description: A股市场自动化复盘分析系统，基于Gemini AI生成每日市场洞察报告，支持发布到Hugo博客和微信公众号
version: 1.0.1
metadata:
  openclaw:
    homepage: https://github.com/donvink/stock-review
    requires:
      anyBins:
        - python3
        - python
---

# 🚀 Stock Review

👉 **[在线演示博客](https://donvink.github.io/stock-review/)**

### GitHub: 👉 **[https://github.com/Donvink/stock-review](https://github.com/Donvink/stock-review)**

## Language

**匹配用户语言**: 使用用户使用的相同语言回复。如果用户用中文写，就用中文回复。如果用户用英文写，就用英文回复。

## 脚本目录

**Agent执行**: 确定此SKILL.md目录为 `{baseDir}`，然后使用 `{baseDir}/scripts/<name>.py`。运行时需确保Python 3.10+已安装，依赖包已配置。

| 脚本 | 用途 |
|------|------|
| `scripts/fetch_data.py` | 获取A股市场数据（指数、个股、板块等） |
| `scripts/analyze.py` | Gemini AI分析市场数据 |
| `scripts/post_to_hugo.py` | 发布到Hugo博客 |
| `scripts/post_to_wechat.py` | 发布到微信公众号 |
| `scripts/main.py` | 主执行脚本，协调整个流程 |

## 偏好配置

1. 检查config.yaml是否存在: `{baseDir}/stock-review/config.yaml`

2. 检查.env文件是否存在并且已配置好 `GEMINI_API_KEY`、`WECHAT_APP_ID`、`WECHAT_APP_SECRET`: `{baseDir}/stock-review/.env`


**config.yaml支持**: 默认发布平台 | 默认是否跳过AI分析 | 默认数据回溯天数 | 默认请求延迟 | 默认重试次数 | API密钥配置
**.env支持**: API密钥配置

**最小支持键** (不区分大小写，接受 `1/0` 或 `true/false`):

| 键 | 默认值 | 说明 |
|-----|---------|------|
| `date` | `null` | 日期，格式YYYYMMDD |
| `force_refresh` | `false` | 是否强制更新已经获取的数据 |
| `skip_ai_analysis` | `false` | 是否跳过AI分析 |
| `platforms` | `["hugo"]` | 默认发布平台 (['hugo']/['wechat']/['hugo', 'wechat']) |
| `data_dir` | `null` | 数据保存的地址 |
| `max_retries` | `3` | 默认重试次数 |
| `request_delay` | `0.5` | 默认请求延迟(秒) |
| `backtrack_days` | `0` | 默认数据回溯天数 |
| `type` | `gemini` | 模型类型 |
| `model_name` | `gemini-2.5-flash` | 模型名称 |


**推荐config.yaml示例**:

```yml
# default configuration for stock review skill
review:
  markets:                          # can include "shanghai", "shenzhen", "hongkong"
    - "shanghai"
    - "shenzhen"
    - "hongkong"
  default_period: "daily"           # can be "daily", "weekly", "monthly"
  date: null                        # can be specific date "YYYYMMDD" like "20260101" or null for today
  force_refresh: false              # whether to force refresh data even if cached data is available
  skip_ai_analysis: false           # whether to skip AI analysis and just return raw data
  platforms: ["hugo"]               # platforms to publish the report, e.g. ['hugo', 'wechat'] or ['hugo'] or ['wechat']

paths:
  data_dir: null                    # directory to store fetched data and cache, null means current project directory

parameters:
  max_retries: 3
  request_delay: 0.5
  backtrack_days: 0
  
models:
  type: "gemini"
  model_name: "gemini-2.5-flash"
```

**.env示例**:

```md
# Gemini API Key
GEMINI_API_KEY="your_gemini_api_key"

# WeChat Official Account Configuration
WECHAT_APP_ID="your_wechat_app_id"
WECHAT_APP_SECRET="your_wechat_app_secret"
```

### 获取Gemini API Key的方法：
1. 访问官方入口：前往 https://aistudio.google.com/ 并使用你的 Google 账号登录。

2. 创建 API Key：点击左侧边栏的 "Get API key"，点击 "Create API key in new project"，复制生成的字符串（请务必妥善保存，关闭窗口后将无法再次查看完整 Key）。

3. 注意事项：
**免费层级**：提供免费额度，但有请求频率限制（RPM/RPD）。
**数据隐私**：免费版数据可能会被用于模型改进，商业敏感数据建议开启付费模式。

### 获取微信公众号凭证的方法：

1. 访问 https://developers.weixin.qq.com/platform/
2. 进入：我的业务 → 公众号 → 开发密钥
3. 添加开发密钥，复制 AppID 和 AppSecret
4. **将你操作的机器 IP 加入白名单**


## 环境检查

首次使用前，先安装依赖包。

```bash
pip install -r {baseDir}/requirements.txt
```

检查项: Python版本 | 依赖包 | API密钥 | 网络连接 | 目录权限

**如果任何检查失败**，提供修复指导：

| 检查项 | 修复方法 |
|-------|----------|
| Python版本 | 安装Python 3.10+：`brew install python@3.10` (macOS) 或 `apt install python3.10` (Linux) |
| 依赖包 | 运行 `pip install -r {baseDir}/requirements.txt` |
| Gemini API密钥 | 在.env中设置或通过环境变量配置 |
| 微信公众号凭证 | 在.env中设置或通过环境变量配置 |
| 网络连接 | 检查网络代理设置 |
| 目录权限 | 确保data/和content/posts/目录可写 |

## 工作流程概览

复制此清单并随进度勾选：

```
复盘分析进度:
- [ ] 步骤0: 加载偏好配置 (config.yaml, .env)，确定执行参数
- [ ] 步骤1: 获取市场数据
- [ ] 步骤2: 运行AI分析（可选）
- [ ] 步骤3: 生成报告
- [ ] 步骤4: 发布到平台
- [ ] 步骤5: 报告完成
```

### 步骤0: 加载偏好配置

检查并加载config.yaml设置（见上方偏好配置部分），解析并存储默认值供后续步骤使用。

### 步骤1: 获取市场数据

根据指定日期获取以下数据：

| 数据类型 | 来源 | 文件 |
|----------|------|------|
| 指数数据 | stock_zh_index_spot_sina | `data/{date}/index_{date}.csv` |
| 涨停池 | stock_zt_pool_em | `data/{date}/zt_pool_{date}.csv` |
| 跌停池 | stock_zt_pool_dtgc_em | `data/{date}/dt_pool_{date}.csv` |
| 炸板池 | stock_zt_pool_zbgc_em | `data/{date}/zb_pool_{date}.csv` |
| 全市场数据 | stock_zh_a_spot_em | `data/{date}/A_stock_{date}.csv` |
| 成交额前20 | 计算得出 | `data/{date}/top_amount_stocks_{date}.csv` |
| 概念板块 | stock_board_concept_name_em | `data/{date}/concept_summary_{date}.csv` |
| 龙虎榜 | stock_lhb_detail_daily_sina | `data/{date}/lhb_{date}.csv` |
| Watchlist | 计算得出 | `data/{date}/watchlist*_{date}.csv` |

**重试机制**:
- 默认重试3次
- 请求间隔0.5秒
- 失败自动切换备用接口

### 步骤2: 运行AI分析

**CRITICAL**: 仅在以下情况运行AI分析：
- `--skip-ai` 未设置
- `GEMINI_API_KEY` 已配置（通过config.yaml或环境变量）

**AI分析提示词**:

```python
prompt = f"""
角色设定：你是一位拥有20年经验的A股资深策略分析师...

任务描述：基于【当日复盘数据】进行多维度复盘：
1. 🚩 市场情绪诊断
2. 💰 核心主线与资金流向
3. 🪜 连板梯度与空间博弈
4. ⚡ 重点异动个股分析
5. 🧭 次日交易策略建议

📊 当日复盘数据:
{market_summary}
"""
```

**输出**: `data/{date}/ai_analysis_{date}.md`

### 步骤3: 生成报告

**市场汇总报告**:
- 文件: `data/{date}/market_summary_{date}.md`
- 格式: Markdown
- 内容: 所有数据的表格化汇总

**AI分析报告** (如果运行):
- 文件: `data/{date}/ai_analysis_{date}.md`
- 格式: Markdown
- 内容: Gemini生成的深度分析

### 步骤4: 发布到平台

**Hugo博客发布**:

```bash
python3 {baseDir}/scripts/post_to_hugo.py --market-summary <file> --ai-analysis <file> --date <date>
```

**输出**: `content/posts/stock-analysis-{YYYY-MM-DD}.md`

**微信公众号发布** (需要API凭证):

```bash
python3 {baseDir}/scripts/post_to_wechat.py --market-summary-file <file> --ai-analysis-file <file> --date <date> --cover-file <file> --title <title>
```

**微信公众号API请求规则**:
- 端点: `POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN`
- `article_type`: `news`
- 需要 `thumb_media_id` (封面图)
- 评论设置: `need_open_comment=1`, `only_fans_can_comment=0`

### 步骤5: 完成报告

**成功执行后报告**:

```
✅ A股复盘分析完成！

日期: 2026-03-04
数据: data/20260304/ (12个文件)
AI分析: ✓ 已生成 (Gemini 2.0 Flash)

发布平台:
→ Hugo博客: content/posts/stock-analysis-2026-03-04.md
→ 微信公众号: 草稿ID: abc123def456

市场快照:
• 上证指数: 3350.52 (+1.02%)
• 成交额: 1.95万亿
• 涨跌比: 2857 / 2058
• 涨停/跌停: 78 / 3

查看博客: https://donvink.github.io/stock-review/
```

**错误时报告**:

```
❌ 复盘分析失败

错误: 无法获取涨停板数据
建议: 
1. 检查网络连接
2. 尝试 --force 参数强制刷新
3. 增加 --date 指定其他日期
```

## 详细功能说明

### 数据获取模块

| 函数 | 用途 | 重试 | 缓存 |
|------|------|------|------|
| `stock_summary()` | 获取指数数据 | ✓ | ✓ |
| `stock_zt_dt_pool()` | 获取涨跌停数据 | ✓ | ✓ |
| `fetch_all_stock_data()` | 获取全市场数据 | ✓ (3次) | ✓ |
| `get_top_amount_stocks()` | 获取成交额前20 | ✓ | ✓ |
| `get_concept_summary()` | 获取概念板块 | ✓ | ✓ |
| `get_lhb_data()` | 获取龙虎榜 | ✓ | ✓ |

### AI分析模块

**模型**: `gemini-2.5-flash`

**分析维度**:
1. **市场情绪诊断** - 涨跌比、涨停跌停对比、成交额
2. **核心主线追踪** - 资金流向、热点板块
3. **连板梯度分析** - 空间板高度、连板结构
4. **异动个股分析** - 大额成交、龙虎榜
5. **次日策略建议** - 基于数据的操作建议

### 发布模块

| 平台 | 方式 | 要求 | 输出 |
|------|------|------|------|
| Hugo博客 | 文件写入 | 无 | Markdown文件 |
| 微信公众号 | API | AppID/Secret | 草稿ID |

## 功能对比

| 功能 | 数据获取 | AI分析 | Hugo发布 | 微信发布 |
|------|----------|--------|----------|----------|
| 自动获取最新日期 | ✓ | - | - | - |
| 数据缓存 | ✓ | - | - | - |
| 重试机制 | ✓ | - | - | - |
| 多源备份 | ✓ | - | - | - |
| 格式化数值(亿/万) | ✓ | - | - | - |
| 过滤ST股票 | ✓ | - | - | - |
| Watchlist构建 | ✓ | - | - | - |
| 市场情绪诊断 | - | ✓ | - | - |
| 连板梯度分析 | - | ✓ | - | - |
| 策略建议 | - | ✓ | - | - |
| Markdown格式 | - | ✓ | ✓ | ✓ |
| 时区处理 | - | - | ✓ | - |
| Hugo frontmatter | - | - | ✓ | - |
| 微信HTML转换 | - | - | - | ✓ |
| 评论设置 | - | - | - | ✓ |

## 先决条件

**必需**:
- Python 3.10+
- 依赖包: `pip install -r requirements.txt`
- Gemini API密钥（用于AI分析）

**可选**:
- 微信公众号AppID和AppSecret（用于微信发布）
- Hugo博客环境（用于博客发布）

**配置位置** (优先级):
1. CLI参数
2. config.yaml, .env (项目级/用户级)
3. 环境变量
4. 默认值

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 无法获取数据 | 检查网络，指定其他日期 |
| Gemini API错误 | 检查API密钥是否有效，配额是否足够 |
| 涨停板数据为空 | 可能是非交易日，尝试回溯其他日期 |
| 微信发布失败 | 检查AppID/Secret，**确认IP已加入白名单** |
| 中文乱码 | 确保文件编码为UTF-8 |
| 数据格式错误 | 检查CSV文件，确认代码列未转为数字 |
| 超时错误 | 增加 `request_delay` 或 `max_retries` |
| 内存不足 | 减少数据量，或分批处理 |

## 扩展支持

通过config.yaml自定义配置。参见**偏好配置**部分了解路径和支持的选项。

## 相关参考

| 主题 | 参考 |
|------|------|
| AkShare文档 | https://akshare.akfamily.xyz/index.html |
| Gemini API | https://aistudio.google.com/ |
| 微信公众号API | https://developers.weixin.qq.com/platform |
| Hugo文档 | https://gohugo.io/ |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-11 | 初始版本 |


