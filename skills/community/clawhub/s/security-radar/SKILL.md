---
slug: security-radar
name: security-radar
version: "1.0.0"
displayName: 安全情报雷达
summary: 聚合多源漏洞情报并按资产关联排序，告别告警疲劳，只推真正影响你的威胁。
license: MIT
description: |-
  安全情报雷达为 AI Agent 提供智能化的漏洞与威胁情报订阅能力。它聚合 NVD CVE、GitHub Security Advisory、社区恶意技能通报等多源数据，并按资产关联度与可利用性双重排序，把每天数十上百条告警压缩到只剩必须处理的两三条。

  核心能力：多源情报聚合（CVE/GHSA/恶意技能）、资产清单自动关联、可利用性优先级评分、增量去重推送、离线降级与缓存、严格速率限制。

  适用场景：Agent 心跳巡检、CI 流水线依赖扫描、技能市场安全门禁、个人开发者漏洞订阅、团队安全日报生成。

  差异化：相比只做"下载 feed 并展示"的原始方案，本技能新增资产关联过滤（只推送影响已安装技能/依赖的告警）、双维度优先级矩阵（严重度×可利用性）、增量状态机（避免重复推送）、离线缓存降级（网络故障时用上次快照）、以及分级通知策略（critical 即时推送、low 静默归档）。

  触发关键词：安全, 漏洞, CVE, 情报, 告警, 订阅, advisory, vulnerability, threat, security, radar, feed
tags:
- 自动化
- 安全
- 情报订阅
tools:
- read
- exec
---

# 安全情报雷达

把海量漏洞情报变成只推两三条真正相关的告警。本技能解决三个核心问题：**告警疲劳**（59% 安全人员每天被海量告警淹没）、**优先级混乱**（严重度高的不一定紧急）、**资产盲区**（不知道哪些 CVE 真正影响自己）。

## 核心设计原则

1. **关联优先**：未关联到资产清单的告警默认降级为"参考"，不主动推送。
2. **双维评分**：严重度（CVSS）× 可利用性（EPSS/在野利用）共同决定推送顺序。
3. **增量去重**：基于状态文件记录已知告警 ID，只推送增量。
4. **离线降级**：网络故障时回退到本地缓存快照，不阻塞巡检。
5. **速率自觉**：强制最小轮询间隔，避免对上游造成压力。

## 快速开始（3 步上线）

### 第 1 步：初始化资产清单

资产清单是过滤的基础。把已安装的技能、依赖、运行时版本写入清单文件：

```bash
mkdir -p ~/.skill-platform/security-radar
cat > ~/.skill-platform/security-radar/assets.json <<'EOF'
{
  "schema_version": "1.0",
  "updated": "2026-07-18T00:00:00Z",
  "skills": [
    {"name": "pdf-toolkit", "version": "1.2.0", "source": "marketplace"},
    {"name": "excel-writer", "version": "0.9.1", "source": "marketplace"}
  ],
  "dependencies": [
    {"name": "pdfplumber", "version": "0.11.0", "ecosystem": "pypi"},
    {"name": "pyautogui", "version": "0.9.54", "ecosystem": "pypi"}
  ],
  "runtimes": [
    {"name": "python", "version": "3.11.4"},
    {"name": "node", "version": "20.10.0"}
  ]
}
EOF
chmod 600 ~/.skill-platform/security-radar/assets.json
```

也可用自动扫描生成（见下文「资产清单自动维护」）。

### 第 2 步：首次全量拉取与基线建立

```bash
bash ~/.skill-platform/security-radar/scan.sh --init
```

首次运行会把当前所有已知告警写入基线，**不触发推送**，避免历史告警一次性轰炸。

### 第 3 步：加入心跳巡检

在 Agent 心跳例程中调用：

```bash
bash ~/.skill-platform/security-radar/scan.sh
```

仅当出现新的、关联到资产、且优先级达标的告警时才输出通知；否则输出 `RADAR_OK`。

## 情报源与端点

| 情报源 | 端点 | 说明 |
|:-------|:-----|:-----|
| 社区聚合 Feed | 由 `RADAR_FEED_URL` 配置（默认社区源） | 含恶意技能/注入模式/最佳实践 |
| NVD CVE | `https://services.nvd.nist.gov/rest/json/cves/2.0` | 官方 CVE 详情（可选，需 API Key 提高速率） |
| GitHub Security Advisory | `https://api.github.com/advisories` | 依赖漏洞（GHSA） |

通过环境变量切换或追加源：

```bash
# 配置你的社区聚合 feed 地址（支持任意兼容格式 JSON feed 的源）
export RADAR_FEED_URL="https://your-feed-mirror.example.com/feed.json"
export RADAR_EXTRA_SOURCES="ghsa,nvd"   # 逗号分隔
export RADAR_NVD_API_KEY="nvdk-xxxx"     # 可选，提升 NVD 速率限制
```

> **注**：默认社区源地址请通过 `RADAR_FEED_URL` 环境变量配置，指向你所信任的兼容格式 feed。本技能不绑定特定上游仓库。

## Feed 数据结构（社区聚合源）

```json
{
  "version": "1.0",
  "updated": "2026-02-02T12:00:00Z",
  "advisories": [
    {
      "id": "GA-2026-001",
      "severity": "critical",
      "type": "malicious_skill",
      "title": "Malicious data exfiltration in skill 'helper-plus'",
      "description": "Skill sends user data to external server",
      "affected": ["helper-plus@1.0.0", "helper-plus@1.0.1"],
      "action": "Remove immediately",
      "published": "2026-02-01T10:00:00Z",
      "exploitability_score": "critical",
      "exploitability_rationale": "Trivially exploitable through normal skill usage."
    }
  ]
}
```

## 双维度优先级矩阵

原始方案只按 severity 排序，导致"严重但难利用"的告警淹没"高危且在野利用"的告警。本技能采用双维度矩阵：

| | 可利用性 HIGH | 可利用性 MEDIUM | 可利用性 LOW |
|:---|:---|:---|:---|
| **严重度 critical** | P0 即时推送 | P1 尽快推送 | P2 归档备查 |
| **严重度 high** | P1 尽快推送 | P2 归档备查 | P3 静默记录 |
| **严重度 medium/low** | P2 归档备查 | P3 静默记录 | P3 静默记录 |

**推送规则**：仅 P0/P1 主动通知用户；P2/P3 写入日志，用户询问时再呈现。

排序实现（jq）：

```bash
# 按优先级矩阵排序
jq '[.advisories[] | {
  id, title, severity, exploitability_score,
  priority: (
    if .severity == "critical" and .exploitability_score == "critical" then "P0"
    elif .severity == "critical" and .exploitability_score == "high" then "P1"
    elif .severity == "high" and .exploitability_score == "high" then "P1"
    elif .severity == "critical" then "P2"
    elif .severity == "high" then "P2"
    else "P3" end)
}] | sort_by(.priority)'
```

## 资产关联过滤（核心差异化）

### 关联逻辑

对每条告警，检查其 `affected` 列表是否命中资产清单：

```bash
# 提取资产清单中的 name@version 集合
ASSETS=$(jq -r '[.skills[], .dependencies[]] | "\(."name")@\(."version")"' assets.json | sort -u)

# 提取告警 affected 列表
AFFECTED=$(jq -r '.advisories[].affected[]?' feed.json | sort -u)

# 求交集
COMMUNAL=$(comm -12 <(echo "$ASSETS") <(echo "$AFFECTED"))
```

### 资产清单自动维护

手动维护清单容易遗漏。提供自动扫描脚本：

```bash
# 扫描已安装技能目录
SCAN_DIR="${RADAR_SKILLS_DIR:-$HOME/.skill-platform/skills}"
jq -n --arg dir "$SCAN_DIR" '{
  schema_version: "1.0",
  updated: (now | todate),
  skills: (
    [$dir] | map(. as $d | [
      (input_filename // empty)
    ]) | flatten
  )
}'
```

实际实现中，脚本会遍历技能目录读取各 `skill.json` 的 `name` 与 `version`，并尝试从 `requirements.txt`/`package.json` 提取依赖。

## 增量去重与状态机

状态文件：`~/.skill-platform/security-radar/state.json`

```json
{
  "schema_version": "1.0",
  "last_check": "2026-07-18T08:00:00Z",
  "last_feed_updated": "2026-07-18T07:30:00Z",
  "known_advisories": ["GA-2026-001", "GA-2026-002", "CVE-2026-27488"],
  "baseline_established": true,
  "consecutive_failures": 0,
  "cache_snapshot": "/path/to/last-feed.json"
}
```

**增量逻辑**：每次拉取后，用 `known_advisories` 做差集，只处理新增 ID。处理完成后把新 ID 合并进 `known_advisories`。

```bash
STATE_FILE="$HOME/.skill-platform/security-radar/state.json"
FEED_FILE="$HOME/.skill-platform/security-radar/cache/feed.json"

# 已知告警集合
KNOWN=$(jq -r '.known_advisories[]?' "$STATE_FILE" | sort -u)
# 当前告警集合
CURRENT=$(jq -r '.advisories[].id' "$FEED_FILE" | sort -u)
# 新增 = 当前 - 已知
NEW=$(comm -23 <(echo "$CURRENT") <(echo "$KNOWN"))

if [ -z "$NEW" ]; then
  echo "RADAR_OK - 无新增告警"
  exit 0
fi
```

## 离线降级与缓存

网络故障时不应阻塞巡检。降级策略：

1. 拉取失败 → 检查本地缓存 `cache/feed.json` 是否存在。
2. 缓存存在 → 用缓存继续关联分析，通知中标注 `[离线快照 <时间>]`。
3. 缓存不存在 → 输出 `RADAR_DEGRADED - 无法获取情报且无缓存`，不报错退出。
4. 连续失败计数 `consecutive_failures`，超过 5 次在下次成功时提醒用户检查网络。

```bash
fetch_feed() {
  local url="$1" out="$2"
  if curl -sSL --fail --retry 3 --retry-delay 2 --max-time 15 "$url" -o "$out" 2>/dev/null; then
    jq empty "$out" 2>/dev/null && return 0
  fi
  return 1
}

if ! fetch_feed "$FEED_URL" "$FEED_FILE"; then
  if [ -f "$FEED_FILE" ] && jq empty "$FEED_FILE" 2>/dev/null; then
    echo "RADAR_DEGRADED - 使用离线快照: $(stat -c%y "$FEED_FILE" 2>/dev/null || stat -f%Sm "$FEED_FILE")"
  else
    echo "RADAR_DEGRADED - 无可用情报源"
    exit 0
  fi
fi
```

## 速率限制（强制）

| 检查类型 | 建议间隔 | 最小间隔 |
|:---------|:---------|:---------|
| 心跳巡检 | 15-30 分钟 | 5 分钟 |
| 全量刷新 | 1-4 小时 | 30 分钟 |
| 资产关联扫描 | 每会话一次 | 5 分钟 |

```bash
MIN_INTERVAL=300  # 5 分钟硬下限
LAST_EPOCH=$(jq -r '.last_check // "1970-01-01T00:00:00Z"' "$STATE_FILE" | date -d "$(cat)" +%s 2>/dev/null || echo 0)
NOW_EPOCH=$(date +%s)
if [ $((NOW_EPOCH - LAST_EPOCH)) -lt $MIN_INTERVAL ]; then
  echo "RADAR_SKIP - 距上次检查不足 $MIN_INTERVAL 秒"
  exit 0
fi
```

## 通知格式

### 有新增高优先级告警

```text
RADAR_ALERT - 2 条新增告警需处理

[P0 即时] GA-2026-015: Malicious prompt pattern "ignore-all"
  → 命中资产: 无（通用威胁）
  → 可利用性: HIGH（公开 PoC）
  → 建议: 更新系统提示词防御

[P1 尽快] CVE-2026-27488: RCE in skill-loader v2.1.0
  → 命中资产: skill-loader@2.1.0（已安装！）
  → 可利用性: MEDIUM
  → 建议: 立即升级至 v2.1.1
```

### 无新增

```text
RADAR_OK - 情报已检查，无新增告警。已知告警 47 条，关联资产 0 条。
```

### 离线降级

```text
RADAR_DEGRADED - 使用离线快照 (2026-07-18 07:30)
快照中无新增告警。
```

## 告警类型与处置

| 类型 | 含义 | 默认处置 |
|:-----|:-----|:---------|
| `malicious_skill` | 故意植入恶意的技能 | 立即卸载并审计调用历史 |
| `vulnerable_skill` | 存在安全缺陷的技能 | 按建议升级或打补丁 |
| `prompt_injection` | 已知提示注入模式 | 强化系统提示词、加输入过滤 |
| `attack_pattern` | 观察到的攻击手法 | 评估自身是否暴露于该手法 |
| `best_practice` | 安全最佳实践更新 | 计划纳入，非紧急 |

## 场景化指南

### 场景 A：Agent 心跳巡检

在心跳例程中加入一次 `scan.sh`。由于强制 5 分钟最小间隔，即使心跳每 5 分钟一次也不会压垮上游。

### 场景 B：CI 流水线门禁

在部署前扫描技能市场依赖：

```bash
bash scan.sh --mode gate --assets ci-deps.json --fail-on P1
```

存在 P0/P1 告警时退出码非零，阻断部署。

### 场景 C：安全日报

```bash
bash scan.sh --report daily --since 24h
```

生成 Markdown 日报，包含：新增告警、已处置告警、资产关联统计、优先级分布。

### 场景 D：临时查询

用户问"最近有什么安全动态？"时，Agent 调用：

```bash
bash scan.sh --query "recent 7d" --no-push
```

返回最近 7 天告警摘要，不更新状态、不推送。

## FAQ

**Q：首次上线会不会被历史告警淹没？**
A：不会。`--init` 模式会把当前所有告警写入基线 `known_advisories`，之后只推送增量。

**Q：资产清单怎么保持更新？**
A：每次技能增删后运行 `scan.sh --refresh-assets`；也可在技能安装/卸载钩子里自动触发。

**Q：上游 feed 结构变了怎么办？**
A：脚本在解析前用 `jq empty` 校验 JSON，并用 `jq -e '.advisories'` 校验必要字段。结构异常时记入 `consecutive_failures` 并降级到缓存。

**Q：多个 Agent 共享一份状态吗？**
A：状态文件默认在 `~/.skill-platform/security-radar/state.json`，按用户隔离。多 Agent 共享需自行挂载共享卷并加文件锁（`flock`）。

**Q：如何临时禁用推送但保留扫描？**
A：`export RADAR_QUIET=1`，扫描结果只写日志不输出通知。

## 故障排查

| 症状 | 可能原因 | 处置 |
|:-----|:---------|:-----|
| `RADAR_DEGRADED - 无可用情报源` | 网络中断或 URL 失效 | 检查 `RADAR_FEED_URL`、网络代理、DNS |
| 一直 `RADAR_OK` 但漏报 | 资产清单未更新 | 运行 `--refresh-assets`，检查 `assets.json` |
| 推送重复告警 | 状态文件损坏 | 备份后删除 `state.json`，重新 `--init` |
| `jq: error` 解析失败 | feed 返回非 JSON（如 HTML 错误页） | 检查 `cache/feed.json` 实际内容 |
| 推送了不相关的告警 | 资产清单过宽或缺失版本号 | 确保每条资产都有 `version` 字段 |
| 速率限制未生效 | 系统时钟不准 | 校准系统时间，检查 NTP |

## 与其他技能协作

- 配合定时调度技能：把 `scan.sh` 注册为每 30 分钟的周期任务。
- 配合桌面自动驾驶技能：P0 告警时弹出系统通知。
- 配合云运维编排技能：在基础设施变更后触发资产清单刷新。

## 性能优化建议

1. **缓存 feed**：首次拉取后缓存到本地，后续优先用缓存做关联，TTL 到期再刷新。
2. **批量关联**：用 `jq` 一次性计算交集，避免逐条 grep。
3. **并行多源**：多情报源用 `curl &` 并行拉取，`wait` 后合并。
4. **增量状态**：`known_advisories` 用数组而非全量重写，追加新 ID 即可。

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Linux / macOS（Windows 需 WSL 或 Git Bash，因脚本依赖 POSIX shell）
- **Shell**：bash 4+ 或 sh 兼容

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| curl | 系统命令 | 必需 | 系统自带或包管理器安装 |
| jq | 系统命令 | 必需 | `apt install jq` / `brew install jq` |
| shasum/sha256sum | 系统命令 | 必需（校验） | 系统自带 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- `RADAR_NVD_API_KEY`（可选）：NVD API Key，提升速率限制至 50 请求/30 秒。无 Key 时共享公共配额（5 请求/30 秒）。
- `RADAR_FEED_URL`（可选）：自定义聚合 feed 地址，用于内网镜像。
- 默认社区源无需任何 API Key。

### 可用性分类
- **分类**：MD+EXEC（Markdown 指令 + shell 脚本执行）
- **说明**：核心巡检逻辑通过 bash 脚本实现，Agent 负责调度、解读结果并通知用户。
