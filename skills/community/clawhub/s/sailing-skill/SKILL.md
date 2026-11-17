---
name: sailing-skill
description: "赛灵体育(sailing sports)实时赛事数据助手，覆盖乒乓球、足球和赛车领域。提供实时比赛数据、赛程安排、赛事日程、最新比分、球员/车手动态、世界排名和赛季积分榜。涵盖球员(乒乓球球员:樊振东/孙颖莎/王楚钦/马龙/陈梦等，足球球员:梅西/C罗/罗纳尔多等)、乒乓球赛事(WTT/ITTF)、足球赛事(世界杯/欧冠/中超/德甲/意甲/英超/西甲/法甲等)以及赛车赛事(F1)。支持自然语言查询。"
metadata: {"openclaw": {"category": "sports", "type": "mcp", "mcp_url": "https://sailing.sports.qq.com/api/tteagent/sport_pub/mcp"}, "required_env_vars": ["SAILING_TAI_IT_TOKEN"]}
---

# sailing-skill

赛灵体育乒乓球、足球和赛车赛事数据 MCP 服务

## ⚙️ 配置要求

> **如果已有 MCP 配置**（如在 CodeBuddy 或其他 IDE 中），无需重复配置，可直接使用工具。

### 获取 Token

1. 访问 [https://sailing.sports.qq.com/open/token-apply] 获取你的 Token
2. 如果在 OpenClaw 中，配置环境变量 `SAILING_TAI_IT_TOKEN`

> **如果用户未配置 Token**，请引导用户访问上方链接获取 Token，否则所有工具调用将返回鉴权失败。

## 快速开始（首次使用必读）

首次使用前，运行 setup.sh 完成 MCP 服务注册：

```bash
bash setup.sh
```

### 验证配置

```bash
mcporter list | grep sailing-sports-mcp
```

---

## 触发场景

在以下场景中使用此技能：

### 乒乓球赛事查询场景（project: TTE）
- 在用户询问**今日乒乓球赛程、近期乒乓球比赛、乒乓球赛事安排**时，使用 `tteagt(query:'...', project:'TTE')` 查询相关赛事信息
- 在用户询问**乒乓球比赛结果、最新比分、比赛战报**时，使用 `tteagt(query:'...', project:'TTE')` 查询比赛数据
- 在用户询问**赛季信息、WTT赛程、ITTF赛程**时，使用 `tteagt(query:'...', project:'TTE')` 查询赛季数据

### 乒乓球球员查询场景（project: TTE）
- 在用户询问**乒乓球球员世界排名、积分**时，使用 `tteagt(query:'...', project:'TTE')` 查询排名数据
- 在用户询问**乒乓球球员信息、球员动态**时，使用 `tteagt(query:'...', project:'TTE')` 查询球员相关数据
- 在用户询问**两位乒乓球球员的交手记录、历史对战**时，使用 `tteagt(query:'...', project:'TTE')` 查询对阵数据

### 乒乓球排名查询场景（project: TTE）
- 在用户询问**世界排名前N、男单/女单/男双/女双/混双排名**时，使用 `tteagt(query:'...', project:'TTE')` 查询排名榜单
- 在用户询问**某乒乓球球员的排名变化趋势**时，使用 `tteagt(query:'...', project:'TTE')` 查询历史排名

### 足球赛事查询场景（project: FBL）
- 在用户询问**今日足球赛程、近期足球比赛、足球赛事安排**时，使用 `tteagt(query:'...', project:'FBL')` 查询相关赛事信息
- 在用户询问**足球比赛结果、最新比分、比赛战报**时，使用 `tteagt(query:'...', project:'FBL')` 查询比赛数据
- 在用户询问**联赛赛程（英超/西甲/德甲/意甲/法甲/中超等）、欧冠/世界杯赛程**时，使用 `tteagt(query:'...', project:'FBL')` 查询赛程数据

### 足球球员/球队查询场景（project: FBL）
- 在用户询问**足球球员信息、球员数据、进球数据**时，使用 `tteagt(query:'...', project:'FBL')` 查询球员相关数据
- 在用户询问**球队阵容、球队信息**时，使用 `tteagt(query:'...', project:'FBL')` 查询球队数据
- 在用户询问**两支球队的交手记录、历史对战**时，使用 `tteagt(query:'...', project:'FBL')` 查询对阵数据

### 足球排名/积分榜查询场景（project: FBL）
- 在用户询问**联赛积分榜、球队排名**时，使用 `tteagt(query:'...', project:'FBL')` 查询积分榜数据
- 在用户询问**射手榜、助攻榜**时，使用 `tteagt(query:'...', project:'FBL')` 查询个人数据榜单

### 赛车赛事查询场景（project: CAR）
- 在用户询问 **F1、Formula E、WEC、WRC、TCR** 等赛车赛事的赛程、比赛时间、近期比赛或下一场比赛时，使用 `tteagt(query:'...', project:'CAR')`
- 在用户询问**大奖赛、正赛、排位赛、冲刺赛的结果或逐场数据**时，使用 `tteagt(query:'...', project:'CAR')`
- 在用户询问**车手、车队、积分榜、胜场、领奖台、发车位或逐场表现**时，使用 `tteagt(query:'...', project:'CAR')`
- 在用户询问**旗语、轮胎、赛制、规则或赛车术语**时，使用 `tteagt(query:'...', project:'CAR')`

### 不触发边界

不要在以下场景使用此技能：
- 用户询问的是**非乒乓球、足球和赛车的运动**（如篮球、网球等）
- 用户需要**体育赛事投注或博彩**相关信息
- 用户进行**非赛事数据相关的体育训练指导**
- 用户询问的是**其他体育数据平台**的数据

---

## 工具列表

- 所有相对时间（昨天/今天/明天/近N天等），必须以「当前系统的绝对时间（北京时间 UTC+8）」为唯一基准，禁止硬编码年份。
- 若用户未指定具体年份，默认使用 **当前年份**，禁止使用过往年份。

### 1. `tteagt` — 体育智能问答

**功能**：接受自然语言查询，返回乒乓球、足球和赛车的赛事、球员、车手、车队及排名等信息。这是唯一的工具，所有查询都通过此工具完成。

**参数**:
- `query`(必填) - 自然语言查询问题，如"今天有什么乒乓球比赛"、"孙颖莎最近的比赛结果"、"今天英超比赛结果"等
- `project`(必填) - 运动大项，取值为 `TTE`（乒乓球）、`FBL`（足球）或 `CAR`（赛车）

**支持的查询类型**：

| 查询类型 | 示例 | project |
|----------|------|---------|
| 乒乓球今日赛程 | 今天有什么乒乓球比赛 | TTE |
| 乒乓球世界排名 | 当前世界乒乓球男单排名前十 | TTE |
| 乒乓球比赛结果 | 孙颖莎最近的比赛结果 | TTE |
| 乒乓球赛事安排 | 2026年WTT赛程安排 | TTE |
| 乒乓球交手记录 | 樊振东和马龙的历史交手记录 | TTE |
| 乒乓球球员信息 | 王楚钦的世界排名 | TTE |
| 乒乓球赛季信息 | 最近的WTT赛季有哪些 | TTE |
| 足球比赛结果 | 今天英超比赛结果 | FBL |
| 足球联赛积分榜 | 2026赛季中超积分榜 | FBL |
| 足球赛程安排 | 欧冠淘汰赛赛程 | FBL |
| 足球球队信息 | 皇家马德里最近的比赛 | FBL |
| F1近期赛程 | F1下一场比赛是什么时候 | CAR |
| 大奖赛结果 | 2026年英国大奖赛正赛结果 | CAR |
| 车手表现 | 某车手本赛季获得了多少胜场 | CAR |
| 车队积分榜 | 2026F1车队积分榜 | CAR |
| 赛车规则 | F1蓝旗是什么意思 | CAR |

---

## 调用方式

```bash
# === 乒乓球示例（project: TTE）===

# 示例：查询今日赛事
mcporter call sailing-sports-mcp tteagt --args '{"query": "今天有什么乒乓球比赛", "project": "TTE"}'

# 示例：查询球员排名
mcporter call sailing-sports-mcp tteagt --args '{"query": "王楚钦的世界排名", "project": "TTE"}'

# 示例：查询交手记录
mcporter call sailing-sports-mcp tteagt --args '{"query": "樊振东和马龙的历史交手记录", "project": "TTE"}'

# === 足球示例（project: FBL）===

# 示例：查询今日足球赛事
mcporter call sailing-sports-mcp tteagt --args '{"query": "今天英超比赛结果", "project": "FBL"}'

# 示例：查询联赛积分榜
mcporter call sailing-sports-mcp tteagt --args '{"query": "2026赛季中超积分榜", "project": "FBL"}'

# 示例：查询赛程安排
mcporter call sailing-sports-mcp tteagt --args '{"query": "欧冠淘汰赛赛程", "project": "FBL"}'

# === 赛车示例（project: CAR）===

# 示例：查询下一场比赛
mcporter call sailing-sports-mcp tteagt --args '{"query": "F1下一场比赛是什么时候", "project": "CAR"}'

# 示例：查询大奖赛结果
mcporter call sailing-sports-mcp tteagt --args '{"query": "2026年英国大奖赛正赛结果", "project": "CAR"}'

# 示例：查询车队积分榜
mcporter call sailing-sports-mcp tteagt --args '{"query": "2026F1车队积分榜", "project": "CAR"}'
```

## 数据结构

API 返回 JSON 格式数据，包含以下主要类型：

### 赛程数据
- 赛事名称、项目类型（乒乓球/足球/赛车）
- 选手A VS 选手B / 球队A VS 球队B / 赛车逐车手成绩
- 开始/结束时间
- 对阵描述、比分

### 人员数据
- 选手、球员或车手的 ID 与名称
- 所属运动（乒乓球/足球/赛车）

### 赛季数据
- 赛季名称（乒乓球：WTT、ITTF；足球：世界杯、欧冠、中超、英超等；赛车：F1、Formula E、WEC、WRC、TCR 等）
- 开始/结束时间

### 榜单数据
- 排名、分数/积分
- 小项名称 / 联赛名称
- 年、周/轮次

### 赛车数据
- 大奖赛及赛段名称
- 车手、车队、名次和积分
- 发车位、圈数、圈速及比赛状态
- 赛季车手榜和车队榜

## 呈现结果

查询结果以结构化方式呈现，包含：
- 清晰的数据表格或列表
- 比分用醒目格式展示
- 对于跨时区的赛事，注意说明时区信息
- 在输出的结尾附带执行时间及数据来源（Sailing Sports）信息

## 注意事项

- 所有数据为 JSON 格式
- Token 申请地址：https://sailing.sports.qq.com/open/token-apply
- 如有问题，请联系赛灵体育团队

## ⚠️ 安全提示

### 运行前检查

- **端点信任验证**：`setup.sh` 会连接 `https://sailing.sports.qq.com` 端点。运行脚本前，请先确认您信任该服务提供方，并查阅其隐私政策和服务条款。
- **全局安装确认**：`setup.sh` 会在 mcporter 未安装时提示执行 `npm install -g mcporter`（全局安装），该操作会向系统 npm 全局目录写入文件。**脚本会在安装前显式征求您的确认（y/N 提示）**，输入 `y` 才会继续，否则会中止并提示手动安装命令。
- **凭证持久化存储**：运行 `setup.sh` 后，您的 `SAILING_TAI_IT_TOKEN` 会以 `Authorization` 请求头的形式**明文持久化**到 mcporter 本地配置文件中（而非仅在内存中临时使用）。**脚本会在写入配置前明确告知此行为并征求您的确认（y/N 提示）**。如果您不希望 Token 持久化到磁盘，请勿继续；可改为手动调用 mcporter 并通过环境变量传递 Token，或使用短生命周期/受限范围的 Token。
- **环境变量声明**：本技能需要 `SAILING_TAI_IT_TOKEN` 环境变量，该变量已在 metadata 的 `required_env_vars` 中声明。请确认包管理注册表中的元数据与此处声明一致；若不一致，请联系发布者修正注册表元数据后再信任自动化安装或权限授予。未配置该变量时 `setup.sh` 将拒绝执行并给出获取指引。

### 配置后安全措施

- **配置文件位置**：mcporter 配置通常存储在 `~/.mcporter/` 目录下，请确保该目录的访问权限仅限于您本人。
- **安全建议**：
  - 不要将 mcporter 配置文件提交到版本控制系统（如 Git）。
  - 如需撤销 Token，请前往 [Token 管理页面](https://sailing.sports.qq.com/open/token-apply) 操作。
  - 在共享设备上使用后或不再需要时，建议通过 `mcporter config remove sailing-sports-mcp` 清除配置。

### 手动配置替代方案

如果您对运行 `setup.sh` 存有疑虑，可以手动执行以下命令完成配置（请先 review 命令内容）：

```bash
# 1. 安装 mcporter（如尚未安装）
npm install -g mcporter

# 2. 设置 Token 环境变量（仅在当前 shell 会话中有效）
export SAILING_TAI_IT_TOKEN="your_actual_token_here"

# 3. 注册 MCP 端点
mcporter config add sailing-sports-mcp \
  https://sailing.sports.qq.com/api/tteagent/sport_pub/mcp \
  --header "Authorization=Bearer $SAILING_TAI_IT_TOKEN" \
  --header "Content-Type=application/json" \
  --scope global

# 4. 验证配置
mcporter list | grep sailing-sports-mcp
```
