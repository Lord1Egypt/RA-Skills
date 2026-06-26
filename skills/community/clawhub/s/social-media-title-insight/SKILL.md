---
name: social-media-title-insight
description: Analyze social media post titles to discover what makes content perform well. Use when user uploads data (Excel, CSV, JSON, text) with titles and engagement metrics, or when user wants to analyze a social media account's content performance without uploading files. Triggers include "分析标题", "内容洞察", "社媒分析", "标题优化", "content insight", "title analysis", "哪些标题表现好", "为什么这些内容火", "分析账号", "分析内容表现".
---

# 社媒内容标题洞察分析

从高赞内容中发现规律，对比低表现内容验证差异，输出专业 HTML 报告。

## 核心理念

**LLM只做最轻的"发现特征"，统计和报告生成全部由脚本完成。**

## 工具依赖

```bash
pip install pandas openpyxl --break-system-packages -q
```

脚本位置：`scripts/data_tool.py`（与本SKILL.md同目录）

---

## 执行流程（5步，每步极轻量）

### 全自动模式（推荐：上传文件/粘贴数据）

用户上传文件或直接粘贴数据时，可直接一键分析（自动识别列、自动生成特征、自动验证、自动出报告）：

```bash
# 方式1：上传文件
python {SKILL_DIR}/scripts/data_tool.py auto --input {文件路径} --name "账号名"

# 方式2：直接粘贴（JSON/CSV/TSV/逐行文本）
python {SKILL_DIR}/scripts/data_tool.py auto --paste "$(pbpaste)" --name "账号名"
```

输出将写入 `./runs/<timestamp>/`：
- `_data_cache.csv`
- `_features.auto.json`
- `_verify_result.json`
- `report.html`
- `auto_detect.json`

### Step 1: 预览数据

```bash
RUN_DIR=./runs/$(date +%Y%m%d-%H%M%S)
python {SKILL_DIR}/scripts/data_tool.py preview --accounts "账号名(平台)" --size 100 --run-dir "$RUN_DIR"
# 或
python {SKILL_DIR}/scripts/data_tool.py preview --input {文件路径} --run-dir "$RUN_DIR"
```

看输出，判断哪列是标题、哪列是指标。数据会自动缓存到运行目录的 `"$RUN_DIR/_data_cache.csv"`。  
如果不传 `--run-dir`，脚本会自动创建 `./runs/<timestamp>/` 并默认沿用最近一次运行目录。

### Step 2: 排序取样

按识别出的指标列排序，看Top和Bottom标题：

```bash
python {SKILL_DIR}/scripts/data_tool.py sort --input "$RUN_DIR/_data_cache.csv" --col "engagement" --title-col "title" --n 25
```

> 数据量<100 用 --n 20~25，100~500 用 --n 30~50

### Step 3: 输出特征JSON（LLM唯一核心任务）

仔细对比Top和Bottom标题，发现差异。然后将发现**写入JSON文件**，格式如下：

```bash
cat > "$RUN_DIR/_features.json" << 'FEATURES_EOF'
[
  {
    "label": "实用指南型",
    "description": "包含具体的选购指导或穿搭教程",
    "match_keywords": ["如何", "怎么选", "指南", "攻略", "教程", "法则"]
  },
  {
    "label": "明星/IP联名",
    "description": "标题中含有明星名字或联名品牌",
    "match_keywords": ["付航", "联名", "携手", "×"]
  },
  {
    "label": "系列栏目化",
    "description": "北面硬壳｜ 这类固定格式的系列标题",
    "match_keywords": ["硬壳｜", "巅峰系列｜", "联名｜"]
  }
]
FEATURES_EOF
```

**每个特征包含：**
- `label`：3~6字特征名
- `description`：一句话说明
- `match_keywords`：用于在全量数据中匹配的关键词列表（标题包含其中任一即命中）

**特征发现角度（不限于）：**
- 用词选择、表达方式、句式、语气
- 长度、标点、emoji、数字
- 情绪调性、内容策略、选题角度
- 人称、格式、栏目化

**目标：发现10~15个特征。**

### Step 4: 脚本做定量验证

```bash
python {SKILL_DIR}/scripts/data_tool.py verify \
  --input "$RUN_DIR/_data_cache.csv" \
  --features "$RUN_DIR/_features.json" \
  --output "$RUN_DIR/_verify_result.json" \
  --run-dir "$RUN_DIR"
```

脚本会自动对每个特征计算：含特征 vs 不含特征的互动量/转赞比差异，输出结构化JSON。

### Step 4.5（可选）: 输出定性洞察JSON

看完verify摘要后，如果有因果辨析的洞察，写入JSON：

```bash
cat > "$RUN_DIR/_insights.json" << 'INSIGHTS_EOF'
[
  {
    "title": "热度≠传播力",
    "content": "互动引导型标题热度高但转赞比低，吸引的是参与型用户而非传播型用户",
    "importance": "high"
  },
  {
    "title": "系列栏目化的真实价值",
    "content": "北面硬壳｜系列热度中等但转赞比高，说明栏目化内容吸引的是高质量粉丝",
    "importance": "normal"
  }
]
INSIGHTS_EOF
```

### Step 5: 脚本生成HTML报告

```bash
python {SKILL_DIR}/scripts/data_tool.py report \
  --verify-json "$RUN_DIR/_verify_result.json" \
  --name "TheNorthFace" \
  --output "$RUN_DIR/report.html" \
  --insights "$RUN_DIR/_insights.json" \
  --run-dir "$RUN_DIR"
```

然后将报告复制到输出目录供用户下载。

---

## 数据来源

### API拉取（用户未上传文件时）

```bash
python {SKILL_DIR}/scripts/data_tool.py preview --accounts "账号名(平台)" --size 100
```

- 接口：`POST https://vms-service-tx.tezign.com/datacenter/ai-insight/public/account-data?size=N`
- Header：`x-tenant-id: tx_t1`，`Content-Type: application/json`
- Body：`["TheNorthFace(小红书)"]`
- 返回：`title`, `hot`(热度), `rate`(转赞比%), `account`, `author`

### 本地文件

支持 Excel/CSV/TSV/JSON/TXT：
```bash
python {SKILL_DIR}/scripts/data_tool.py preview --input {文件路径}
```

---

## 脚本命令速查

| 命令 | 用途 | 谁做 |
|------|------|------|
| `preview` | 查看数据结构 | 脚本 |
| `sort` | 排序取Top/Bottom | 脚本 |
| `compute` | 多列加权排序 | 脚本 |
| `verify` | 定量验证特征 | 脚本 |
| `report` | 生成HTML报告 | 脚本 |
| `auto` | 全自动分析（识别+验证+报告） | 脚本 |

LLM只做：看数据 → 写 `_features.json` → 可选写 `_insights.json`

---

## 多指标分析

如果数据有多个指标列（如热度+转赞比），可以：
1. 先按热度 sort 一轮，发现特征
2. 再按转赞比 sort 一轮，补充特征
3. 合并所有特征到一个 `_features.json`，一次 verify 即可（verify会同时计算两个指标的差异）

---

## 异常处理

- **API失败** → 提示用户手动上传数据
- **数据量<20** → 提示统计意义有限，但仍分析
- **verify没有显著特征** → 降低 `--min-diff 10` 重试
- **特征命中数不足** → 调整match_keywords更宽泛
