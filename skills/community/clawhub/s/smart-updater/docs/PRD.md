# Smart Updater — 产品需求文档

> **版本**：v0.1 (Draft)  
> **Author**: Smart Updater contributors  
> **日期**：2026-03-11  
> **定位**：OpenClaw 生态的智能升级管理 skill，HITL（Human-in-the-Loop）模式

---

## 一句话

**不要盲更新，先读 changelog 再决定。**

---

## 问题

OpenClaw 用户面临的升级现状：

1. **没有统一视图**——skill 装在 clawhub、GitHub、手动复制三种来源，extension 在 npm，OpenClaw 本体也是 npm，各管各的
2. **盲更新风险高**——现有 auto-updater skill 直接 `clawhub update --all`，不看 changelog，不区分 patch 和 breaking change（e.g. extension upgrade leaving .bak directory triggers duplicate plugin id）
3. **手动更新太碎**——要分别跑 `clawhub update`、`npm update`、`git pull`，记不住哪些装了、从哪来的
4. **built-in skills 不透明**——OpenClaw 自带 50+ skill，升级 OpenClaw 本体时它们会随之更新，但用户不知道变了什么

---

## 核心理念

```
扫描 → 读 changelog → AI 汇总 → 用户决策 → 安全升级 → 验证
```

**关键区别**：不是自动更新器，是**升级顾问 + 执行器**。AI 做分析和建议，人做决策。

---

## 产品需求

### 模块一：Inventory（资产盘点）

**目标**：一条命令生成完整的"我装了什么"清单。

#### 需要盘点的资产类型

| 类型 | 来源 | 示例 | 获取当前版本 | 获取最新版本 |
|------|------|------|-------------|-------------|
| **OpenClaw 本体** | npm | `openclaw@2026.3.8` | `openclaw --version` | `npm view openclaw version` |
| **npm extensions** | npm | `extension-a@1.0.0`, `extension-b@2.0.0` | `package.json` in `~/.openclaw/extensions/` | `npm view <pkg> version` |
| **ClawHub skills** | clawhub registry | `self-improving@1.2.10`、`proactive-agent@3.1.0` 等 | `clawhub list` | `clawhub update --all --dry-run`（或 API） |
| **GitHub skills** | git clone | `clawfeed`、`news-aggregator-skill` | `git log -1 --format=%H` | `git fetch && git log origin/main -1` |
| **手动安装 skills** | 文件复制（无 VCS） | `c-level-advisor`、`rag-architect` 等 | 无版本号（只有文件修改时间） | 需要记录来源 repo 才能检查 |
| **Built-in skills** | 随 OpenClaw 发布 | `summarize`、`coding-agent`、`weather` 等 50+ | 随 OpenClaw 版本 | 升级 OpenClaw 本体时自动更新 |

#### 资产清单文件：`~/.openclaw/inventory.json`

```json
{
  "version": 1,
  "lastScan": "2026-03-11T01:30:00+08:00",
  "assets": [
    {
      "name": "openclaw",
      "type": "core",
      "source": "npm",
      "currentVersion": "2026.3.8",
      "installedAt": "~global~",
      "updateCommand": "npm update -g openclaw"
    },
    {
      "name": "my-extension",
      "type": "extension",
      "source": "npm",
      "currentVersion": "1.0.32",
      "installedAt": "~/.openclaw/extensions/my-extension",
      "updateCommand": "cd ~/.openclaw/extensions/my-extension && npm install my-extension@latest"
    },
    {
      "name": "self-improving",
      "type": "skill",
      "source": "clawhub",
      "currentVersion": "1.2.10",
      "installedAt": "~/.openclaw/workspace/skills/self-improving",
      "updateCommand": "clawhub update self-improving"
    },
    {
      "name": "clawfeed",
      "type": "skill",
      "source": "github",
      "repo": "kevinho/clawfeed",
      "currentCommit": "abc1234",
      "installedAt": "~/.openclaw/workspace/skills/clawfeed",
      "updateCommand": "cd ~/.openclaw/workspace/skills/clawfeed && git pull"
    },
    {
      "name": "c-level-advisor",
      "type": "skill",
      "source": "github-manual",
      "repo": "alirezarezvani/claude-skills",
      "subpath": "c-level-advisor",
      "installedAt": "~/.openclaw/workspace/skills/c-level-advisor",
      "note": "手动从 repo 复制，无自动更新"
    }
  ]
}
```

**首次运行**时自动扫描并生成此文件。后续每次扫描时更新。手动安装的 skill 首次需要用户补充来源信息（或标记为 `local`，不参与更新检查）。

---

### 模块二：Scan（扫描可用更新）

**目标**：检查所有资产是否有新版本。

#### 扫描策略

| Source | 方法 | 限流 |
|--------|------|------|
| npm | `npm view <pkg> version` | 串行，间隔 200ms |
| clawhub | `clawhub update --all --dry-run` | 单次调用 |
| GitHub | `git fetch --dry-run` 或 `git ls-remote` | 串行，间隔 500ms |
| Built-in | 对比 `openclaw --version` 与 npm latest | 随 core 扫描 |

#### 扫描输出

```json
{
  "scanTime": "2026-03-11T04:00:00+08:00",
  "updates": [
    {
      "name": "self-improving",
      "source": "clawhub",
      "current": "1.2.10",
      "latest": "1.3.0",
      "changeType": "minor",
      "changelogUrl": "https://clawhub.ai/pskoett/self-improving-agent/changelog"
    },
    {
      "name": "my-extension",
      "source": "npm",
      "current": "1.0.32",
      "latest": "1.0.33",
      "changeType": "patch",
      "changelogUrl": "https://www.npmjs.com/package/my-extension?activeTab=changelog"
    }
  ],
  "upToDate": ["openclaw", "proactive-agent", "..."],
  "unreachable": []
}
```

---

### 模块三：Changelog Analysis（变更分析）

**目标**：自动读取 changelog，AI 生成一句话摘要 + 风险评估。

#### Changelog 来源

| Source | Changelog 位置 |
|--------|---------------|
| clawhub skill | `clawhub.ai/<author>/<skill>` 页面 CHANGELOG.md（或 SKILL.md 内嵌） |
| npm package | npm registry `changelog` 字段 / GitHub releases |
| GitHub skill | `CHANGELOG.md` 或 `git log --oneline current..latest` |

#### AI 分析输出

对每个可用更新，生成：

```
📦 self-improving 1.2.10 → 1.3.0 (minor)
📝 新增 auto-consolidation 功能，改进了记忆去重逻辑
⚠️ 风险：中（minor 版本，新增功能，无 breaking change 声明）
💡 建议：可升级，建议先备份
```

```
📦 my-extension 1.0.32 → 1.0.33 (patch)
📝 修复了 embedding 缓存过期不刷新的问题
⚠️ 风险：低（patch，纯 bugfix）
💡 建议：推荐升级
```

```
📦 openclaw 2026.3.8 → 2026.3.9 (patch)
📝 修复 Telegram channel 在 IPv6 环境下的连接问题；新增 2 个内置 skill
⚠️ 风险：中（本体升级影响面广，built-in skills 会随之更新）
💡 建议：建议在低峰时段升级，升级后运行 gateway status 验证
```

#### 风险评级规则

| 条件 | 风险 | 默认策略 |
|------|------|---------|
| patch + 纯 bugfix | 🟢 低 | 推荐升级 |
| minor + 新增功能 | 🟡 中 | 建议升级 |
| major + breaking change | 🔴 高 | 需要人工确认 |
| extension 类资产 | 🟡+ | 始终走 Gate 2 完整流程（jiti + restart + 日志验证） |
| changelog 拿不到 | 🟠 未知 | 标注"无法评估"，建议人工查看 |
| 新增可执行脚本 | 🟠+ | Post-flight 提醒过 skill-vetter |
| 名字冲突 | 🔴 | Pre-flight 阻止（Gate 1） |

---

### 模块四：HITL Decision（用户决策）

**目标**：汇总所有可用更新，让用户选择升级哪些。

#### 汇总报告格式

通过 Telegram/DingTalk 发送：

```
🔄 Smart Updater — 升级扫描报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 扫描了 42 个资产，发现 3 个可用更新：

🟢 推荐升级（1）
  1. my-extension 1.0.32 → 1.0.33
     修复 embedding 缓存过期问题（patch bugfix）

🟡 建议升级（1）
  2. self-improving 1.2.10 → 1.3.0
     新增 auto-consolidation（minor，无 breaking）

🟡 需确认（1）
  3. openclaw 2026.3.8 → 2026.3.9
     Telegram IPv6 修复 + 2 个新内置 skill（本体升级）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
回复编号选择升级，如 "1 2" 升级前两个
回复 "all" 全部升级
回复 "skip" 跳过本次
```

#### 用户交互

- 回复 `1 2` → 升级选定的
- 回复 `all` → 全部升级
- 回复 `skip` → 本次跳过
- 回复 `detail 3` → 查看 #3 的完整 changelog
- 不回复 → 24h 后自动过期，不执行任何升级

---

### 模块五：Safe Upgrade（安全升级执行）

**目标**：按类型安全执行升级，内含备份和验证。

#### 升级流程（分类型，遵循 Three Gates）

每种类型都走 Gate 1 → Gate 2 → Gate 3，区别在于各门的具体检查项：

| 阶段 | Skill（clawhub/GitHub） | Extension（npm） | Core（OpenClaw 本体） |
|------|------------------------|------------------|--------------------|
| **Gate 1** | 名字冲突检查 | Gateway 健康检查 | 记录当前版本 |
| **Gate 2 备份** | → `skill-backups/` | → `extensions-backup/` | → `plist-backup/` + `openclaw backup create` |
| **Gate 2 缓存** | 无 | `rm -rf /tmp/jiti/` | 无 |
| **Gate 2 执行** | `clawhub update` / `git pull` | `npm install <pkg>@latest` | `npm update -g openclaw` + `gateway install` |
| **Gate 2 配置保护** | 无 | 清理 extensions/ 下残留 .bak* | diff 新旧 plist，恢复自定义环境变量 |
| **Gate 3 验证** | SKILL.md 存在 + 文件完整 | gateway restart → 日志 plugin registered → status 全绿 | 版本确认 + status 全绿 + extensions 正常 |
| **Fail → 回滚** | 恢复备份 | 恢复备份 + 清 jiti + restart | `npm install openclaw@<prev>` + 恢复 plist |

---

### 模块六：Cron 集成

**目标**：每天自动扫描，发现更新后通知用户。

#### 默认配置

```
扫描时间：每天 06:00（可配置）
扫描模式：scan + changelog analysis
执行模式：仅通知，不自动升级（HITL）
通知渠道：当前 session 的主 channel（Telegram / DingTalk）
```

#### 可选配置

```json
{
  "schedule": "0 6 * * *",
  "autoUpgrade": {
    "patch": true,      // patch 自动升级
    "minor": false,     // minor 需确认
    "major": false      // major 需确认
  },
  "skipAssets": ["c-level-advisor"],  // 跳过特定资产
  "backupBeforeUpgrade": true,
  "notifyOnNoUpdates": false
}
```

---

## 与现有 auto-updater 的对比

| 维度 | auto-updater | Smart Updater（我们） |
|------|-------------|---------------------|
| 更新模式 | 全自动，盲更新 | HITL，先分析后决策 |
| Changelog | 不读 | 自动读取 + AI 摘要 |
| 风险评估 | 无 | 基于 semver + changelog 的三级风险 |
| 覆盖范围 | clawhub + OpenClaw | npm + clawhub + GitHub + 本体 + extensions |
| 备份 | 无 | 升级前自动备份 |
| 回滚 | 无 | 验证失败自动回滚 |
| 资产盘点 | 无 | inventory.json，完整视图 |
| 用户交互 | 事后通知 | 事前决策 |

---

## 升级安全框架：三道门（Three Gates）

> 所有升级事故都发生在三个阶段：升级前没检查、升级中污染了环境、升级后没验证。
> 每道门有明确的 pass/fail 条件。任何一道门 fail → 中止或回滚，不允许带病通过。

### Gate 1: Pre-flight（能不能升）

在触发任何变更之前，必须通过：

| 检查项 | 规则 | Fail 行为 |
|--------|------|----------|
| **来源可追溯** | 每个资产必须有注册的 source（npm/clawhub/github/local）。无来源 = 不参与升级 | 跳过，标记 `untracked` |
| **名字无冲突** | 升级目标与本地已有资产的 name/dir 不能冲突（防静默覆盖） | 阻止升级，报告冲突 |
| **环境健康** | Extension 升级前 gateway 必须处于健康状态（三行全绿） | 阻止，提示先修 gateway |
| **路径可达** | 脚本中所有路径用 `$HOME` 绝对路径 + `resolve_openclaw()`，不依赖 runtime 变量 | — |

### Gate 2: Isolation（升级过程不污染环境）

升级执行中，确保变更的「爆炸半径」受控：

| 规则 | 说明 |
|------|------|
| **备份路径隔离** | 备份必须在 scanner/loader 扫描路径之外。Extension → `~/.openclaw/extensions-backup/`；Skill → `~/.openclaw/skill-backups/`。违反此规则会导致 duplicate id 等扫描冲突 |
| **缓存失效** | Extension（编译型）升级后必须清 jiti 缓存（`rm -rf /tmp/jiti/`）。Skill（markdown）不需要 |
| **配置保护** | Core 升级可能重新生成 plist/config，升级前快照关键配置文件，升级后 diff + 恢复用户自定义项 |

### Gate 3: Post-flight（升级后验证）

升级完成后，按资产类型执行验证，全部通过才算成功：

| 资产类型 | 验证标准 | Fail 行为 |
|---------|---------|----------|
| **Skill** | SKILL.md 存在 + 文件数 ≥ 旧版本 | 回滚 |
| **Extension** | gateway restart → 日志出现 `plugin registered`，无 `duplicate plugin id` → gateway status 三行全绿 | 回滚 + 清 jiti |
| **Core** | `openclaw --version` 确认新版本 + gateway status 全绿 + extensions 全部正常加载 | 回滚到 `openclaw@<prev>` |
| **安全信号**（可选） | 新版本如果新增了可执行脚本（scripts/），在报告中标注，建议用户过 skill-vetter | 不阻止，仅提醒 |

### 框架总结

```
Pre-flight ──pass──→ Backup + Execute (Isolation) ──pass──→ Post-flight ──pass──→ ✅ 完成
    │                        │                                  │
    fail                     fail                               fail
    ↓                        ↓                                  ↓
  阻止升级               中止 + 清理                        回滚 + 通知
```

三道门的设计原则：**宁可不升，不可升坏。**

---

## 技术实现方案

### Skill 结构

```
skills/smart-updater/
├── SKILL.md              # 主入口，AI 读取后执行
├── scripts/
│   ├── scan.sh           # 扫描脚本（生成 scan-result.json）
│   ├── inventory.sh      # 资产盘点（生成/更新 inventory.json）
│   └── upgrade.sh        # 升级执行（接受 asset name + version）
├── references/
│   ├── upgrade-types.md  # 各类型升级的详细步骤
│   └── risk-matrix.md    # 风险评估规则
├── CHANGELOG.md
└── PRD.md                # 本文档
```

### 核心逻辑在 AI 侧

Shell 脚本负责：数据采集（版本号、changelog 文本）和执行（备份、安装、验证）。

AI 负责：changelog 解读、风险评估、生成用户报告、解析用户决策、编排升级顺序。

这样的分工利用了 AI 的强项（理解 changelog 语义、判断 breaking change），同时把确定性操作交给脚本。

---

## MVP 范围（v0.1）

**包含**：
- [x] inventory.json 资产盘点（自动扫描 + 生成）
- [x] 三源扫描（npm / clawhub / GitHub）
- [x] Changelog 读取 + AI 摘要
- [x] 风险评级
- [x] Telegram 交互式报告
- [x] 安全升级执行（备份 + 升级 + 验证）
- [x] 单条 `升级检查` 命令触发

**不包含（v0.2+）**：
- [ ] Cron 自动扫描
- [ ] patch 自动升级模式
- [ ] 回滚能力（v0.1 只做备份，回滚手动）
- [ ] Built-in skills 变更追踪（需要 diff OpenClaw 版本间的 skill 目录）
- [ ] Multi-host inventory sync

---

## 为什么这会是爆款

1. **痛点真实**：每个 OpenClaw 用户都面临"装了一堆 skill 不知道怎么升级"的问题
2. **差异化明显**：市面唯一的 auto-updater 是盲更新，我们是智能分析 + HITL
3. **低成本高价值**：一个 SKILL.md + 几个 shell 脚本，开发成本低，但对用户的信任感和安全感提升巨大
4. **网络效应**：用户使用后产生的升级数据可以反哺风险评估（"这个版本有 3 个用户回滚了"）
5. **天然分发**：clawhub 上发布，OpenClaw 用户直接 `clawhub install smart-updater`

---


