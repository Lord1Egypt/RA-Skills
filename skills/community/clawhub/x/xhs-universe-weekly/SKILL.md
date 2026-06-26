---
name: xhs-universe-weekly
description: 人群宇宙投放追踪周报自动生成工具。支持任意行业（家清、美妆、母婴、食品等），只需提供 RedBI 看板地址和行业人群包名称，自动拉取数据、对比人群宇宙 vs 整体种草效果、按三类逻辑分层客户优先级（未投放/效果好投入少/数据不及整体），生成可视化 HTML 周报和 Redoc 在线文档。触发词：人群宇宙周报、人群周报、人群渗透分析、人群宇宙、人群分析、人群渗透追踪、人群包优质素材分析。
---

# xhs-universe-weekly — 人群宇宙投放追踪周报

---

## 触发方式

触发词：**人群宇宙周报、人群周报、人群渗透分析、人群宇宙、人群分析、人群渗透追踪、人群包优质素材分析**

用户只需说：**「帮我出 XX 行业人群宇宙周报，WXX，X.XX-X.XX」**

AI 自动完成：SSO 登录 → 下载 CSV → 分析 → HTML + Redoc 双版本输出

**所有小红书内部员工均可使用，无需提前配置权限。用户无需手动下载任何文件。**

### 触发后必须确认三要素（缺一必须追问）

| 要素 | 示例 | 缺失时提示 |
|------|------|------|
| 行业 | 家清、美妆、母婴 | 「请问是哪个行业的周报？」 |
| 时间段 | W14，4.6-4.12 | 「请问数据周期是哪一周？」 |
| 看板链接 | RedBI 看板 URL | 「请提供您的 RedBI 看板链接，或告知行业（家清行业已内置，无需提供）」 |

> 家清行业已内置看板，用户无需提供链接。其他行业需要用户提供 RedBI 看板 URL。

---

## ⚠️ 铁律（每次必须执行，不得偷懒）

1. **必须同时输出两个版本**：HTML 可视化版 + Redoc 在线文档，缺一不可
   - ✅ HTML 文件保存到工作区，同时起一个本地预览服务，回复可访问的 HTTP 链接
   - ✅ Redoc 文档发布后回复文档链接
   - ❌ 禁止只回复 Redoc 文档链接而不生成 HTML
   - ❌ 禁止只生成 HTML 而不发布 Redoc 文档
   - **最终回复必须同时包含两个链接，缺一不可**
2. **HTML 版必须包含素材封面图**：base64 内嵌，不依赖外链
3. **消耗口径必须用「策略流水」**：禁止使用「策略消耗（复记）」
4. **五节内容缺一不可**：总览 → 渗透 → 人群包 → 单客户 → 行动建议
5. **数据不能省略**：每节必须有完整数据表格，不能只写结论
6. **取数方式灵活**：优先走自动取数流程；如果自动取数失败，可以请用户手动下载文件提供，但必须先询问行业和人群包范围

---

## 已配置看板（按行业）

### 家清行业

- 看板 URL：`https://redbi.devops.xiaohongshu.com/dashboard/list?dashboardId=45500&pageId=page_pWvbwhxFPz&projectId=4`
- Tab 1（整体投放情况）：pageId = `page_pWvbwhxFPz`
- Tab 2（优质素材分析）：pageId = `page_8dCnfPXLa1`
- analysisId 对应：
  - `42623804` — 广告主人群宇宙投放分析 → universe_clients.csv
  - `42626327` — 整体种草投放情况 → overall_clients.csv
  - `42701238` — 宇宙人群包投放分析 → crowd_packs.csv
  - `42626064` — 广告主x人群包x笔记分析 → materials.csv
  - `42625208` — 人群宇宙消耗走势图 → universe_trend.csv
  - `42703713` — 整体种草消耗走势 → overall_trend.csv

> **其他行业**：用户提供看板链接，AI 自动解析 dashboardId / pageId / analysisId，无需手动配置。

---

## 取数工作流（AI 自动执行，用户无需操作）

```bash
# Step 1：SSO 登录（所有小红书内部用户均可）
COOKIE=$(cat /home/node/.token/sso_token.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('cookie',''))")

# Step 2：查询最新下载任务列表
curl -s -X POST "https://redbi.devops.xiaohongshu.com/api/download/task/list" \
  -H "Cookie: $COOKIE" \
  -H "Content-Type: application/json" \
  -d '{"pageNo":1,"pageSize":30}'

# Step 3：找到对应 analysisId 且状态为 FINISHED 的任务，下载 CSV
curl -s "{fileUrl}" -H "Cookie: $COOKIE" -o /tmp/weekly_wXX/{filename}.csv

# Step 4：用 openpyxl 或 csv.DictReader 读取
import openpyxl
wb = openpyxl.load_workbook('/tmp/weekly_wXX/universe_clients.csv', data_only=True)
```

**如果任务不存在或已过期（> 3 天）：**
- 提示用户在看板点击图表 `···` → 导出 CSV，等 FINISHED 后 AI 自动继续
- 禁止用截图替代，截图数据不准确

**字段口径：**
- ✅ 「策略流水」= 正确，用这个
- ❌ 「策略消耗（复记）」= 错误，不要用

---

## 内容结构（五节，必须完整）

### 第一节：消耗总览

必须包含：
- KPI 卡片（5个）：本周宇宙消耗 / 整体种草消耗 / 本周渗透率 / 宇宙进店率 / 进店率提升倍数
- 走势表格：时间段 + 宇宙消耗（万）+ 环比 / 整体消耗（万）+ 环比
- 广告主宇宙消耗明细表：广告主 / 消耗 / CTR / I+TI / 淘宝进店率 / 淘宝进店成本 / 消耗环比

### 第二节：渗透情况

必须包含：
- **两个**渗透率大字卡片（不要三个）：
  - 卡片一：本周消耗渗透率（宇宙消耗/整体消耗）
  - 卡片二：客户使用渗透率（宇宙客户数/整体种草客户数）
  - ❌ 禁止单独展示「宇宙淘宝进店率」大卡片（进店率在效率对比表里展示即可）
- 拓新优先级分析汇总表：三类 × 数量 × 说明 × 建议动作
- 效率对比表：CTR / I+TI / 淘宝进店率 / 淘宝进店成本（宇宙 vs 整体，含倍数）
- **对客核心话术**（进店率倍数、进店成本节省比例、客户待开发数，必须突出显示）
- 三类客户分层完整列表：
  - **类型一（未投放）**：广告主 / 整体消耗 / CTR / I+TI / 进店率 / 进店成本 / 优先级
  - **类型二（效果好投入少）**：整体消耗 / 宇宙消耗 / 宇宙占比 / 宇宙进店率 / 宇宙进店成本 / 整体进店率；目标把宇宙占比推到 20-30%
  - **类型三（数据不及整体）**：宇宙消耗 / 宇宙进店率 / 整体进店率 / 差距 / 追踪方向

### 第三节：人群包 TOP10

必须包含：排名 / 人群包名称 / 本周消耗 / CTR / I+TI / 淘宝进店率 / 淘宝进店成本 / 环比

高效情绪型人群包重点标注（如「家清-沉浸式解压」「家清-平静松弛感」「衣物清洁-柔顺人群」）

### 第四节：重点客户深度分析

分析范围：**TOP5 消耗客户 + 进店效率标杆客户（如 RUFI）**，共 6 个

每个客户必须包含：
- 客户标签（💰消耗No.1 / ⚡品质增长 / 🌸香氛种草王 等）
- 6 格指标：宇宙消耗 / 宇宙占比 / CTR / I+TI / 淘宝进店率（❌不展示进店成本）
- **每客户 2 篇不同笔记**（按消耗排序，NID 去重，禁止同一客户重复展示同一篇笔记）
- 每篇笔记：封面图（base64 内嵌）+ 标题 + 人群包 + 消耗 + CTR + **五维内容结构分析**

**五维内容结构分析模板：**

| 维度 | 说明 |
|------|------|
| 内容公式 | 如「情绪爆点型」「场景解决方案型」「UGC征集互动型」等 |
| 钩子 | 标题/首句如何抓住用户 |
| 内容结构 | 笔记的逐步展开逻辑 |
| 内容切角 | 产品植入的视角与场景 |
| 为何有效 | 为什么这篇笔记能种草 |

素材卡片展示指标：消耗 + CTR，**如有进店成本数据则一并展示**

### 第五节：行动建议

至少 4 条，每条格式：标题（一句话）+ 数字依据 + 可执行操作

---

## 环比计算铁律

**禁止**直接使用数据文件中的「动态同环比变化率」字段——该字段是同比或多周前对比，数值偏差极大（如实际 -4.5% 但字段显示 -23.3%）。

**必须**用相邻两个时间段的策略流水自己计算：

```python
# ✅ 正确：相邻两周自行计算
pct_chg = (week2_flow - week1_flow) / week1_flow  # 如 (21.36-22.37)/22.37 = -4.5%

# ❌ 错误：直接用文件里的环比字段
pct_chg = row['策略流水环比 环比-变化率']  # 可能是同比，不准确
```

---

## 客户渗透率定义

「**客户使用渗透率**」= 人群宇宙投放客户数 ÷ 整体种草投放客户数

- 从 `universe_clients` 数据中统计唯一广告主数（去除「总计」行）
- 从 `overall_clients` 数据中统计唯一广告主数（去除「总计」行）
- 这是判断拓新空间的核心指标，必须展示在第二节

---

## HTML 生成规范

### 技术要求
- 内嵌 CSS，无外链依赖（确保内网环境完整显示）
- 启动本地 HTTP 服务提供预览，端口建议 18765
- 回复预览链接格式：`http://{pod_ip}:18765/universe_weekly_report.html`
- 如用户反馈页面是旧版本，提示在链接末尾加 `?v=N` 参数（浏览器缓存问题）

### 封面图抓取
```bash
SSO_COOKIE=$(cat /home/node/.token/sso_token.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('cookie',''))")
nid="笔记ID"
PAGE=$(curl -s --max-time 15 \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Cookie: ${SSO_COOKIE}" \
  "https://www.xiaohongshu.com/explore/${nid}")
img_url=$(echo "$PAGE" | grep -o 'og:image" content="[^"]*"' | head -1 | sed 's/og:image" content="//;s/"//')
curl -s --max-time 15 -H "Referer: https://www.xiaohongshu.com/" "$img_url" -o /tmp/covers/$nid.jpg
```
- 文件 > 50KB 才算成功（小于说明是占位图）
- base64 内嵌：`data:image/jpeg;base64,xxx`，禁止外链
- 缓存 base64 到 `covers_b64.json`，避免重复抓取
- 样式：`width:100%; height:150px; object-fit:cover; border-radius:8px; margin-bottom:10px`
- 放在素材卡片最顶部（标题之前）
- 抓不到：显示灰色「暂无封面」占位块

---

## Redoc 发布命令

```bash
# 生成 operateCode（每次必须重新生成）
OP=$(bunx @xhs/hi-workspace-cli@0.2.11 docs:generate-operate-code | python3 -c "import sys,json; print(json.load(sys.stdin).get('operateCode',''))")

# 新建文档
bunx @xhs/hi-workspace-cli@0.2.11 docs:create \
  --title "家清行业人群宇宙投放追踪周报 YYYY.M.D-M.D" \
  --content - \
  --operate-code "$OP" \
  < /tmp/weekly_wXX/weekly_redoc.md

# 更新已有文档（需先 docs:get 获取最新 hash）
HASH=$(bunx @xhs/hi-workspace-cli@0.2.11 docs:get --shortcut-id "{shortcutId}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('hash',''))")
bunx @xhs/hi-workspace-cli@0.2.11 docs:edit \
  --shortcut-id "{shortcutId}" \
  --hash "$HASH" \
  --target "原始文本" \
  --replace "替换后的内容"
```

---

## 关键数据基准（W14-W15，2026.4.1-4.11，策略流水）

| 指标 | 数值 | 说明 |
|------|------|------|
| 人群宇宙消耗 | 43.73 万 | 策略流水口径 |
| 整体种草消耗 | 441.62 万 | 策略流水口径 |
| 消耗渗透率 | 9.9% | 宇宙/整体 |
| 宇宙淘宝进店率 | 39.4% | vs 整体 25.4%，高 1.6x |
| 宇宙 I+TI | 16.0% | vs 整体 7.8%，高 2.0x |
| 宇宙进店成本 | ¥1.67 | 比整体节省 42.6% |
| 客户使用渗透率 | 42.1% | 16 客 / 38 客，待开发 22 个 |
| 最高效人群包 | 家清-沉浸式解压 | 进店成本 ¥0.28，I+TI 71.3% |
| 进店率最高客户 | RUFI | 宇宙进店率 692%，但占比仅 2.2% |

---

## 参考产出文档

- **W14-W15 周报 HTML**：`http://10.40.93.90:18765/universe_weekly_report.html`
- **W14-W15 周报 Redoc**：`https://docs.xiaohongshu.com/doc/49ba86d5dcd0e5fe8d0f96c99f152d78`
- **skill 使用指南**：`https://docs.xiaohongshu.com/doc/86833739ca1981f4212f3c1adcc87d33`
