---
slug: update-guardian
name: update-guardian
version: "1.0.0"
displayName: 更新守护者
summary: 解决破坏性变更、无法回滚、版本冲突、时机不当四大痛点，预检+快照+回滚三段式。
license: MIT
description: |-
  更新守护者是面向Agent平台与已安装技能包的自动更新能力包。它不只是设个每日cron跑
  update命令，更解决四个高频痛点：更新引入破坏性变更导致线上崩、更新后无法回滚、
  依赖版本冲突、更新时机撞上业务高峰。

  核心能力：
  - 预检干跑：先dry-run检查兼容性，发现breaking change先告警不自动应用
  - 版本快照：更新前自动快照当前版本与配置，可一键回滚
  - 兼容性矩阵：检测新版本与已安装技能/依赖的版本冲突
  - 智能调度：按业务低峰期调度更新，避开高峰
  - 配置备份：更新前备份配置文件，更新后自动diff校验
  - 健康检查：更新后跑健康检查，失败自动回滚

  适用场景：
  - Agent平台与技能包每日自动更新
  - 担心更新引入破坏性变更
  - 更新后出问题不知怎么回滚
  - 多技能依赖同一库的不同版本冲突
  - 需要在业务低峰期安全更新

  差异化：
  - 原始版本只设cron跑update，本版补齐"预检+快照+回滚"三段式安全更新
  - 移除原仓库特定烙印，通用化适配任意Agent平台与技能包管理器
  - 新增兼容性矩阵与依赖冲突检测
  - 新增智能调度（业务低峰期）
  - 新增健康检查失败自动回滚

  触发关键词：自动更新、技能更新、版本回滚、破坏性变更、兼容性检查、快照、更新调度
tags:
- 自动化
- 版本管理
- 运维
tools:
- read
- exec
---

# 更新守护者

自动更新Agent平台与所有已安装技能包，但更新前先预检、先快照，更新后跑健康检查，失败自动回滚。核心信条：**更新可以自动，但回滚必须一键。**

## 四大痛点与对策

| 痛点 | 典型表现 | 本skill对策 |
|:-----|:---------|:------------|
| 破坏性变更 | 更新后技能报错、API不兼容 | 预检干跑 + 兼容性矩阵 |
| 无法回滚 | 更新后坏了不知道旧版本号 | 版本快照 + 一键回滚 |
| 版本冲突 | 技能A要lib v2，技能B要lib v3 | 依赖冲突检测 |
| 时机不当 | 业务高峰期更新导致服务中断 | 智能调度（低峰期） |

---

## 三段式安全更新流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  预检干跑    │ ──→ │  快照+应用   │ ──→ │  健康检查    │
│ dry-run     │     │ snapshot    │     │ health      │
│ 兼容性检查   │     │ apply       │     │ fail→rollback│
└─────────────┘     └─────────────┘     └─────────────┘
```

### 第一段：预检干跑

```bash
# 1. 检查有哪些更新可用（不应用）
update-manager check --all --dry-run

# 2. 输出示例
# Platform: v2026.1.9 → v2026.1.10 (minor, safe)
# Skill prd: 2.0.3 → 2.0.4 (patch, safe)
# Skill browser: 1.2.0 → 2.0.0 (MAJOR, breaking changes detected!)
#   - Breaking: API renamed fetch() to request()
#   - Affected: 3 other skills depend on browser
# Skill nano: 3.1.0 → 3.1.2 (patch, safe)

# 3. 兼容性矩阵检查
update-manager check-conflicts
# Conflict: skill-A requires lib-x>=2.0, skill-B requires lib-x<2.0
# Recommendation: skip skill-A update or pin lib-x to 1.9
```

### 第二段：快照+应用

```bash
# 1. 快照当前状态
update-manager snapshot --output ~/.update-snapshots/$(date +%Y%m%d)

# 2. 快照内容
# - platform版本号
# - 所有技能版本号
# - 配置文件备份（~/.config/agent/）
# - 依赖锁文件（package-lock.json / requirements.txt）

# 3. 应用安全更新（跳过breaking change）
update-manager apply --safe-only  # 只应用patch/minor
# 或指定强制
update-manager apply --include browser --force
```

### 第三段：健康检查

```bash
# 1. 更新后跑健康检查
update-manager health-check

# 2. 检查项
# - 平台启动正常？
# - 所有技能可加载？
# - 关键工作流能跑？
# - 配置文件无diff异常？

# 3. 失败则自动回滚
update-manager health-check --auto-rollback
```

---

## 版本快照与回滚

### 快照结构

```yaml
snapshot:
  date: "2026-07-18"
  timestamp: "2026-07-18T04:00:00Z"
  platform:
    name: agent-platform
    version: "2026.1.9"
    install_method: npm  # npm|pnpm|bun|source
  skills:
    - name: prd
      version: "2.0.3"
      path: ~/.skills/prd/
    - name: browser
      version: "1.2.0"
      path: ~/.skills/browser/
  config_files:
    - path: ~/.config/agent/config.json
      hash: sha256:abc123...
    - path: ~/.config/agent/cron.json
      hash: sha256:def456...
  dependencies:
    - name: lib-x
      version: "1.9.0"
      required_by: [skill-A, skill-B]
```

### 一键回滚

```bash
# 回滚到最近快照
update-manager rollback --latest

# 回滚到指定快照
update-manager rollback --snapshot ~/.update-snapshots/20260718

# 仅回滚指定技能
update-manager rollback --skill browser --to 1.2.0
```

### 回滚流程

```text
1. 停止平台服务
2. 恢复平台二进制/包到快照版本
3. 恢复所有技能到快照版本
4. 恢复配置文件（用hash校验完整性）
5. 恢复依赖锁文件
6. 重启平台服务
7. 跑健康检查确认恢复
```

---

## 兼容性矩阵

### 依赖冲突检测

```yaml
# 检测规则
conflict_detection:
  - type: version_range
    # 技能A要lib-x>=2.0，技能B要lib-x<2.0 → 冲突
    check: "any two skills require non-overlapping version range of same dep"
    action: skip_update + alert

  - type: breaking_change
    # 技能升级到MAJOR版本，检查其他技能是否依赖旧API
    check: "new major version has breaking API changes"
    action: check_dependents + alert

  - type: peer_dependency
    # 技能声明peerDep，检查宿主版本是否匹配
    check: "skill peerDep range vs platform version"
    action: skip + alert
```

### 兼容性矩阵示例

| 技能 | 依赖lib-x | 兼容lib-x版本 | 当前lib-x | 状态 |
|:-----|:----------|:--------------|:----------|:-----|
| skill-A | >=2.0 | 2.0-3.0 | 1.9.0 | 不兼容（需先升lib-x） |
| skill-B | <2.0 | 1.0-1.9 | 1.9.0 | 兼容 |
| skill-C | any | 1.0-3.0 | 1.9.0 | 兼容 |

**冲突解决**：skill-A与skill-B不能共存于同一lib-x版本。方案：二选一保留，或隔离运行环境。

---

## 智能调度

### 业务低峰期检测

```yaml
schedule:
  strategy: off_peak
  detection:
    - 检查历史工作流执行日志，找运行最少的时段
    - 默认低峰：凌晨2:00-5:00（按业务调整）
  fallback:
    # 找不到低峰则用固定时间
    cron: "0 4 * * *"
    tz: "Asia/Shanghai"
  blackout:
    # 业务高峰期禁止更新
    periods:
      - "每周一9:00-12:00"  # 周报高峰
      - "每月1日0:00-6:00"  # 月结高峰
      - "节假日全天"
```

### 调度示例

```bash
# 自动找低峰期
update-manager schedule --auto

# 输出
# Detected off-peak window: 03:00-05:00 daily
# Scheduling updates at 03:30 Asia/Shanghai
# Blackout periods: Mon 9-12, month-start 0-6

# 手动指定
update-manager schedule --cron "0 3 * * *" --tz Asia/Shanghai
```

---

## 配置备份与校验

### 更新前备份

```bash
# 备份配置目录
update-manager backup-config --output ~/.config-backups/$(date +%Y%m%d)

# 备份内容
# - ~/.config/agent/*.json
# - ~/.config/agent/*.yaml
# - ~/.skills/*/config.*
# - 环境变量快照（仅key名，不含value）
```

### 更新后校验

```bash
# diff配置文件，发现意外变更
update-manager diff-config --before ~/.config-backups/20260718 --after ~/.config/agent/

# 输出
# config.json: 2 keys changed
#   - cron.enabled: true → false  (WARNING: unexpected)
#   - log.level: info → debug
# cron.json: no changes
```

**规则**：任何配置项意外变更（非更新日志声明的）都告警。

---

## 健康检查

### 检查项

```yaml
health_check:
  - id: platform_start
    name: "平台启动"
    check: "agent --version 能正常输出"
    on_fail: rollback

  - id: skills_loadable
    name: "技能可加载"
    check: "遍历~/.skills/，每个技能能正常加载"
    on_fail: rollback_affected

  - id: critical_workflow
    name: "关键工作流可跑"
    check: "跑dry-run测试3个最关键工作流"
    on_fail: rollback

  - id: config_valid
    name: "配置文件有效"
    check: "JSON/YAML语法校验 + schema校验"
    on_fail: restore_config

  - id: deps_consistent
    name: "依赖一致性"
    check: "无版本冲突"
    on_fail: alert
```

### 失败自动回滚

```bash
update-manager health-check --auto-rollback --notify slack
```

---

## 更新摘要格式

更新完成后收到消息：

```text
更新守护者报告 2026-07-18

平台: v2026.1.9 → v2026.1.10 (minor, 安全)

技能已更新 (3):
- prd: 2.0.3 → 2.0.4
- browser: 1.2.0 → 1.2.1
- nano: 3.1.0 → 3.1.2

技能跳过 (1):
- browser-major: 1.2.0 → 2.0.0 (MAJOR, 检测到breaking change, 需人工确认)

技能已最新 (5):
gemini, sag, things, himalaya, peekaboo

健康检查: 全部通过
快照: ~/.update-snapshots/20260718 (可回滚)
```

---

## 手动命令

```bash
# 检查更新不应用
update-manager check --all --dry-run

# 查看当前版本
update-manager list

# 查看平台版本
agent --version

# 手动应用指定技能更新
update-manager apply --skill prd

# 强制应用MAJOR更新（需确认）
update-manager apply --skill browser --force --confirm-breaking

# 回滚
update-manager rollback --latest

# 查看快照列表
update-manager snapshots --list
```

---

## 边界情况与陷阱

- **更新中途断网**：可能半更新状态。用事务式更新（要么全成功要么全回滚）。
- **配置文件被改**：更新可能覆盖用户自定义配置。更新前必备份，更新后diff校验。
- **依赖锁文件丢失**：导致依赖版本漂移。锁文件纳入快照。
- **磁盘空间不足**：更新前检查可用空间。
- **权限问题**：确保更新用户对技能目录有写权限。
- **MAJOR版本跳变**：从v1直接跳v3可能漏掉v2的迁移步骤。逐版本升级。

---

## FAQ

**Q：更新后平台起不来了怎么办？**
A：自动健康检查会检测到并触发回滚。手动回滚：`update-manager rollback --latest`，恢复到更新前快照。

**Q：怎么知道哪个技能有breaking change？**
A：预检干跑阶段会输出。MAJOR版本号变更默认跳过，需手动`--force --confirm-breaking`。

**Q：两个技能依赖同一库的不同版本怎么办？**
A：兼容性矩阵会检测到冲突。方案：二选一保留，或为冲突技能隔离运行环境（容器/虚拟环境）。

**Q：更新撞上业务高峰怎么办？**
A：智能调度会自动检测低峰期（默认凌晨2-5点）。可配blackout时段禁止更新。

**Q：配置文件被更新覆盖了怎么办？**
A：更新前自动备份到`~/.config-backups/`。更新后diff校验，意外变更会告警。可手动恢复。

---

## 故障排查

| 症状 | 可能原因 | 解决 |
|:-----|:---------|:-----|
| 更新不运行 | cron未启用 | 检查cron.enabled与Gateway运行状态 |
| 更新失败 | 权限/网络/磁盘 | 检查写权限、网络、磁盘空间 |
| 更新后崩溃 | breaking change | 跑健康检查，自动回滚或手动`rollback --latest` |
| 技能加载失败 | 依赖冲突 | 跑兼容性矩阵，隔离冲突技能 |
| 配置异常 | 更新覆盖 | 从`~/.config-backups/`恢复，加diff告警 |
| 半更新状态 | 中途中断 | `update-manager rollback --latest`回到一致状态 |

---

## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **技能包管理器**：update-manager CLI（或平台自带等价命令）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 技能包管理器 | CLI | 必需 | 平台自带或独立安装 |
| 通知通道（Slack/邮件） | 集成 | 可选 | 用户自有账号 |

### API Key 配置
- 本skill基于Markdown指令，无需额外API Key
- 涉及外部技能源（如私有registry）时，通过环境变量配置访问Token

### 可用性分类
- **分类**：MD+EXEC（Markdown指令 + CLI执行）
- **说明**：通过自然语言指令驱动Agent调用update-manager完成三段式安全更新
