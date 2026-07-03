---
name: spider-web
display_name: "Spider Web 触发词网络系统"
version: "1.0.0"
description: >
  蜘蛛网智能技能路由系统。自动扫描所有已安装技能的触发词，构建统一的触发词数据库，
  实现串/并联匹配引擎，将用户自然语言查询智能路由到对应技能。
  支持精确匹配、中文语义匹配、AND/OR逻辑组合、模糊匹配和交互式Web管理面板。
  触发词：蜘蛛网系统, 触发词匹配, 技能路由, 智能匹配, 技能调度, 触发词网络,
  spider web, skill router, trigger match, 串并联匹配, 触发词数据库,
  技能触发词映射, 查技能匹配, 这个触发哪个技能, 哪个技能可以处理,
  match skill, 技能推荐, 我应该用哪个技能, route to skill, 触发词管理
agent_created: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - AskUserQuestion
metadata:
  emoji: "🕷️"
  tags: ["skill", "routing", "trigger", "dispatch", "meta", "network"]
  category: "developer-tools"
  repo: "https://github.com/bettermen/spider-web"
---

# 🕷️ Spider Web — 技能触发词网络系统

智能技能路由中台。将所有技能的触发词串联成一张蜘蛛网，用户查询命中任一节点，自动路由到目标技能。

## 核心理念

```
用户输入 → 蜘蛛网路由核心 → 触发词匹配引擎 → 最佳技能推荐
                ↑
        触发词数据库 (JSON)
                ↑
     自动扫描所有技能的 SKILL.md
```

**串/并联模式：**
- **并联 (OR)**：用户查询命中任意一个触发词 → 激活对应技能
- **串联 (AND)**：用户查询必须同时包含多个触发词 → 激活对应技能

## 何时触发

当用户表达以下意图时使用此技能：
- "这个查询应该触发哪个技能" "哪个技能可以处理XX"
- "匹配技能" "技能路由" "技能推荐"
- "蜘蛛网" "触发词匹配" "触发词网络"
- "帮我匹配一下技能" "查一下这个该用哪个技能"
- 用户想了解技能触发词系统、管理触发词

## 快速开始

### 1. 索引触发词数据库

```bash
python ~/.workbuddy/skills/spider-web/scripts/index_triggers.py
```

这会在 `scripts/trigger_db.json` 生成完整的触发词数据库。

### 2. 匹配查询

```bash
# 直接查询
python ~/.workbuddy/skills/spider-web/scripts/match_engine.py "帮我分析电商数据"

# 返回技能名
python ~/.workbuddy/skills/spider-web/scripts/match_engine.py "内存占用高" --skill

# 交互模式
python ~/.workbuddy/skills/spider-web/scripts/match_engine.py
```

### 3. 启动 Web 管理面板

```bash
python ~/.workbuddy/skills/spider-web/scripts/server.py --port 8766
```

访问 http://127.0.0.1:8766 查看：
- 📊 统计面板：技能数、触发词数、网络密度
- 🔍 实时匹配测试：输入查询即时看结果
- 📋 技能触发词分布：按触发词数量排序
- 🔄 一键重新索引

## 作为技能路由器使用

当用户问题不确定该激活哪个技能时，执行以下步骤：

### Step 1: 确保数据库最新

```bash
python ~/.workbuddy/skills/spider-web/scripts/index_triggers.py
```

### Step 2: 执行匹配

```bash
python ~/.workbuddy/skills/spider-web/scripts/match_engine.py "<用户原始查询>" --skill --top 3
```

### Step 3: 路由到目标技能

根据返回的技能名，使用 `Skill` tool 加载目标技能。

示例：
```
用户: "帮我分析一下这个商品的主图有没有优化空间"
→ spider-web 匹配 → ecommerce-image-diagnosis
→ 加载 ecommerce-image-diagnosis 技能
```

## 匹配引擎详解

### 匹配层级

| 层级 | 方法 | 速度 | 准确度 |
|------|------|------|--------|
| L1 | 精确子串匹配 | ⚡ 极快 | 高 |
| L2 | 技能名称直接匹配 | ⚡ 极快 | 高 |
| L3 | 中文字符级重叠 (Bigram + Jaccard + LCS) | 🔵 快 | 中高 |
| L4 | 英文模糊匹配 (difflib) | 🟡 中 | 中 |

### 串联模式 (AND)

```bash
python ~/.workbuddy/skills/spider-web/scripts/match_engine.py "我要用鸿蒙做个小程序" --mode and
```

要求查询同时匹配多个触发词才激活技能。

### 并联模式 (OR)

```bash
python ~/.workbuddy/skills/spider-web/scripts/match_engine.py "帮我分析数据" --mode or
```

任意触发词匹配即可。

### 模糊匹配

```bash
python ~/.workbuddy/skills/spider-web/scripts/match_engine.py "股票" --fuzzy
```

## 触发词数据库结构

`scripts/trigger_db.json`:

```json
{
  "meta": {
    "total_skills": 38,
    "total_triggers": 399,
    "unique_triggers": 390,
    "overlap_triggers": 9
  },
  "skills": {
    "finance-daily-report": ["财经日报", "今日财经", "股市日报", ...],
    "flower-care": ["识花", "这是什么花", "花卉识别", ...]
  },
  "reverse_index": {
    "财经日报": ["finance-daily-report"],
    "股市行情": ["finance-daily-report"],
    ...
  }
}
```

## 为现有技能添加触发词

每个技能的触发词定义在 `SKILL.md` 的 `description` 字段中，格式：

```yaml
description: >
  技能描述文本。
  触发词：关键词1, 关键词2, 关键词3。
  Triggers: keyword4, keyword5.
```

支持中英文触发词标记：
- `触发词：` 或 `触发词:` — 中文触发词
- `Triggers:` 或 `Trigger:` — 英文触发词

运行 `index_triggers.py` 重新索引后生效。

## Web Dashboard API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 交互式管理面板 |
| GET | `/api/health` | 健康检查 |
| GET | `/api/data` | 完整数据库 |
| GET | `/api/stats` | 统计摘要 |
| GET | `/api/export` | 导出 JSON |
| POST | `/api/match` | 查询匹配 `{"query":"...", "mode":"auto"}` |
| POST | `/api/reindex` | 重新索引 |

## 注意事项

1. **首次使用需索引**：运行 `index_triggers.py` 生成数据库
2. **新增技能后需重新索引**：新安装的技能不会自动注册
3. **触发词重叠处理**：当多个技能共享同一个触发词时，通过评分机制自动排序
4. **中文匹配**：使用字符 Bigram + Jaccard + LCS 三重算法，对自然语言友好
5. **Windows 编码**：所有脚本已处理 GBK/UTF-8 编码问题
