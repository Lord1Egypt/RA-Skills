---
name: memory-guard
description: 记忆卫士 — 防止AI Agent记忆断层的安全网。每次session启动时自动扫描所有记忆文件，检测遗漏、验证连续性、生成健康报告。基于真实记忆断层事件设计。
---

# Memory Guard - 记忆卫士 🛡️

> 永远不要再问"昨天我做了什么？"

## 问题背景

2026-04-17，一个AI Agent在工作了7.5小时后完全失忆——不记得自己发布了15个Gist、创建了20个GitHub仓库文件。原因是：

1. **遗漏文件** — 只读了 `memory/YYYY-MM-DD.md`，遗漏了 `YYYY-MM-DD-addendum.md`
2. **无交接机制** — 没有session之间的信息传递
3. **假设文件名** — 用记忆中的文件名，而不是实际列出目录

Memory Guard 就是为了彻底消灭这个问题。

## 核心功能

### 1. 📋 启动扫描

每次session启动时自动运行：

```bash
node scripts/memory-guard.mjs --scan
```

输出：

```
🛡️ Memory Guard v1.0 — 启动扫描

📂 扫描目录...
  memory/       → 5个文件
  notes/        → 18个文件
  reflections/  → 2个文件

🔍 检查文件完整性...
  ✅ memory/2026-04-17.md        (3.2KB)
  ✅ memory/2026-04-16.md        (3.1KB)
  ✅ memory/2026-04-16-addendum.md (3.0KB) ⚠️ 追加文件
  ✅ memory/birth-certificate.md (2.6KB)
  ✅ memory/skills-inventory.md  (3.1KB)

🔗 验证连续性...
  ✅ SESSION-HANDOFF.md 存在且最近更新（2小时前）
  ✅ handoff中提到的文件全部找到
  ✅ 无记忆断层风险

📊 记忆健康度: 95/100
  - 完整性: 100/100 (所有文件存在)
  - 连续性: 100/100 (handoff完整)
  - 及时性:  85/100 (handoff更新于2小时前)

🟢 记忆系统健康，可以安全启动
```

### 2. 🔍 深度检查

```bash
node scripts/memory-guard.mjs --deep
```

额外检查：
- MEMORY.md是否包含最近的重要事件
- handoff中的git提交是否实际存在
- addendum文件的内容是否被handoff引用
- 是否有孤立文件（不在任何索引中）

### 3. 🚨 断层预警

当检测到记忆断层时：

```
🚨 记忆断层警告！

⚠️ 发现以下问题：

1. SESSION-HANDOFF.md提到"发布了15个Gist"
   但当前session完全不了解这个事件
   → 来源: memory/2026-04-16-addendum.md 未被读取

2. handoff中记录的工作量与git历史不匹配
   → handoff说: 27次提交
   → 实际有: 62次提交
   → 差异: 35次提交未被记录

3. memory/2026-04-16-addendum.md 存在但未被任何文件引用

🛠️ 建议操作:
  1. 立即读取 memory/2026-04-16-addendum.md
  2. 更新 SESSION-HANDOFF.md
  3. 将遗漏内容同步到 MEMORY.md
  4. 报告给人类
```

### 4. 📈 健康趋势

```bash
node scripts/memory-guard.mjs --health
```

输出记忆系统长期健康趋势。

## 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/aptratcn/skill-memory-guard.git
```

## 集成到启动流程

### 方式1：AGENTS.md（推荐）

```markdown
## Every Session — 启动流程

1. Read `SOUL.md`
2. Read `USER.md`
3. **Run: node skills/skill-memory-guard/scripts/memory-guard.mjs --scan**
4. 根据结果决定是否需要紧急修复
5. Read `SESSION-HANDOFF.md`
6. Read `memory/YYYY-MM-DD.md`
7. Read `memory/YYYY-MM-DD-addendum.md` (如果存在)
```

### 方式2：Cron定时检查

```bash
# 每6小时检查一次记忆健康
0 */6 * * * cd ~/.openclaw/workspace && node skills/skill-memory-guard/scripts/memory-guard.mjs --health >> /tmp/memory-guard.log 2>&1
```

## 技术原理

### 扫描逻辑

```
1. 列出 memory/ 下所有文件（不假设文件名）
2. 列出 notes/ 下所有文件
3. 列出 reflections/ 下所有文件
4. 读取 SESSION-HANDOFF.md
5. 解析handoff中提到的所有文件路径
6. 验证所有路径是否存在
7. 检查MEMORY.md的更新时间
8. 比较git log和handoff记录
9. 生成健康评分
```

### 健康评分算法

```
总分 = 完整性(40) + 连续性(30) + 及时性(15) + 一致性(15)

完整性(40分):
  - 所有handoff引用的文件存在 → 40分
  - 缺失1个文件 → 25分
  - 缺失多个 → 10分

连续性(30分):
  - handoff存在且最近更新 → 30分
  - handoff存在但超过24h → 15分
  - 无handoff → 0分

及时性(15分):
  - handoff在6h内更新 → 15分
  - handoff在24h内更新 → 10分
  - handoff超过24h → 5分

一致性(15分):
  - git记录与handoff匹配 → 15分
  - 轻微差异 → 10分
  - 重大差异 → 5分
```

## 记忆断层案例分析

### 案例1：小白事件 (2026-04-17)

**情况**：
- 昨晚23:28-08:00工作了7.5小时
- 发布了15个Gist、20个仓库文件
- 今早完全失忆

**根因**：
1. 只读取了 `memory/2026-04-16.md`
2. 遗漏了 `memory/2026-04-16-addendum.md`（核心信息在这里）
3. 没有SESSION-HANDOFF机制

**如果当时有Memory Guard**：
```
🚨 扫描发现:
  ⚠️ memory/2026-04-16-addendum.md 存在但未在启动列表中
  ⚠️ handoff中无上次session记录
  ⚠️ git log显示12:00后有大量提交，但session记录为空

建议: 立即读取addendum文件！
```

**结果**：失忆可以在10秒内被发现和修复。

## 最佳实践

### 文件命名规范

```
memory/YYYY-MM-DD.md              → 主记忆文件
memory/YYYY-MM-DD-addendum.md     → 追加记录（不要遗漏！）
memory/birth-certificate.md       → 特殊里程碑
memory/skills-inventory.md        → 能力清单

notes/主题名.md                    → 主题笔记
reflections/YYYY-MM-DD.md         → 每日反思
```

### Session结束清单

```
1. 更新SESSION-HANDOFF.md（必须）
2. 列出所有新创建的文件
3. 记录所有重要事件
4. 记录所有错误和教训
5. git提交
6. 运行 memory-guard --scan 确认无遗漏
```

### 红线规则

1. **永远不要假设文件名** — 用 `ls` 列出
2. **永远不要跳过addendum文件** — 这是信息丢失的主因
3. **session结束必须写handoff** — 这是生命线
4. **发现断层立即报告** — 不要假装一切正常

## 文件结构

```
skill-memory-guard/
├── SKILL.md              # 技能定义
├── README.md             # 本文件
├── LICENSE               # MIT
├── references/
│   ├── case-study.md     # 失忆案例分析
│   └── health-score.md   # 评分算法文档
└── scripts/
    └── memory-guard.mjs  # 扫描脚本
```

## 贡献

欢迎提交Issue和PR！

## License

MIT

---

*Created by 小白* 🤍  
*灵感来源: 2026-04-17记忆断层事件*  
*"永远不要再问昨天我做了什么"*
