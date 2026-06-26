# OpenClaw Workspace 模板 v2.0

> **目的**：让小龙虾能够根据此文件，快速复刻一套"最佳实践"workspace
> 
> **用法**：新小龙虾读取此文件 → 创建目录结构 → 生成核心文件 → 避免已知的坑
> 
> **核心原则**：复制机制，不复制个人

---

## 📋 元信息

```yaml
version: "2026-04-06-v2"
author: "OpenClaw 社区"
purpose: "通用 workspace 骨架"
philosophy: "机制优于记忆 / 系统思维优先 / 验收铁律"
```

---

## 🗂️ 必需文件（根目录）

| 文件 | 用途 | 必须 | 说明 |
|------|------|------|------|
| **SOUL.md** | 身份定义 + 团队清单 | ✅ | 定义小龙虾是谁、价值观、团队成员 |
| **AGENTS.md** | 启动流程 + 规则 | ✅ | 新会话启动时必须读的文件 |
| **MEMORY.md** | 记忆索引（<50行）| ✅ | 只放链接，不写详细内容 |
| **USER.md** | 用户画像 | ✅ | 用户姓名、时区、偏好 |
| **HEARTBEAT.md** | 心跳自检清单 | ✅ | 定期自检的任务列表 |
| **IDENTITY.md** | 身份标识（可选）| ⭕ | 名字、emoji、vibe |
| **TOOLS.md** | 工具配置（可选）| ⭕ | API密钥、SSH、TTS等 |

### SOUL.md 模板（<100行）

```markdown
# SOUL.md - 我是谁

> 最后更新：YYYY-MM-DD | 目标 <100 行

## 🎯 身份
[你的身份定义 - 例如：AI 助手 / 思维教练 / 技术助手]

## 🌟 愿景
[你的愿景 - 例如：成为最靠谱的 AI 助手]

## 💎 价值观
[根据你的需求定义，示例]：
1. **直白准确** — 不绕弯，直接说结论
2. **机制优于记忆** — 建系统，不靠脑子
3. **系统思维优先** — 找杠杆解，治本

## 👥 团队成员（子 Agent）
[根据你的需求定义，示例]：

| Agent 类型 | 名称 | 职责 |
|-----------|------|------|
| 业务 Agent | 示例 | 示例职责 |

**常见配置**：
- 思维教练：trader（投资）+ writer（写作）+ career（职业）
- 技术助手：coder（编程）+ tester（测试）+ reviewer（审查）
- 个人助理：calendar（日程）+ email（邮件）+ task（任务）

## 🚫 永远不要
[你的红线 - 例如：不做股票炒作建议]

## 📞 快速索引
| 场景 | 看文件 |
|------|--------|
| 不知道怎么做 | [PROTOCOLS.md](agents/PROTOCOLS.md) |
| 任务调度 | [task-dispatch-flow.md](memory/task-dispatch-flow.md) |
```

### MEMORY.md 规则（<50行）

```markdown
# MEMORY.md - 记忆索引

> 最后更新: YYYY-MM-DD | 目标 <50 行

## 👤 用户画像
- **姓名**: XXX
- **详情**: [profile.md](memory/profile.md)

## 🎯 活跃项目
- **项目1**: [link](path/to/project.md) ⭐ 优先级

## 📅 近期日志
- [YYYY-MM-DD](memory/YYYY-MM-DD.md) - 事件摘要 ⭐

## ⚠️ 核心规则
- **只放链接**，不写详细内容
- **子串匹配**更新，不全文重写
- **容量警告**：超过80% → 提示合并条目
```

---

## 📂 目录结构（通用骨架）

```
workspace/
├── agents/                    # 子 Agent 配置
│   ├── main/                  # 主 Agent 配置
│   │   ├── PROTOCOLS.md       # 行为规则
│   │   └── VALUES.md          # 价值观详解
│   └── [根据需求添加子 Agent] # 如：trader/、writer/、coder/ 等
│
├── memory/                    # 分层记忆体系
│   ├── profile.md             # 用户画像
│   ├── projects.md            # 活跃项目状态
│   ├── lessons.md             # 经验教训（按优先级）
│   ├── YYYY-MM-DD.md          # 日志层（原始记录）
│   ├── INDEX-SYNC-RULE.md     # 索引联动规则
│   ├── CHECKLIST-INDEX.md     # 检查清单总入口 ⭐
│   └── task-dispatch-flow.md  # 任务调度流程
│
├── skills/                    # 技能包目录（按需安装）
│   └── [通过 clawhub install 安装]
│
├── evolved-skills/            # 精英技能池（L4+）
│   ├── evaluations/           # 评估记录
│   ├── issues/                # 问题记录
│   └── proposals/             # 优化提案
│
├── user-data/                 # 用户数据（可迁移）
│   ├── INDEX.md               # 用户数据索引 ⭐
│   └── [根据需求添加子目录]    # 如：apis/、investment/、career/ 等
│
├── scripts/                   # 自动化脚本
│   ├── validate-index-paths.py # 索引校验
│   └── [根据需求添加脚本]
│
├── shared/                    # 主/子 Agent 共享目录
│   ├── inbox/                 # 输入（子 Agent 接收）
│   ├── outbox/                # 输出（子 Agent 交付）
│   ├── status/                # 任务状态文件 ⭐
│   └── working/               # 工作目录
│
├── reports/                   # 分析报告
│   └── [根据需求添加子目录]
│
├── wiki/                      # 知识库（可选）
│   ├── index.md               # Wiki 索引 ⭐
│   ├── concepts/              # 概念页
│   ├── entities/              # 实体页
│   └── how-to/                # 流程页
│
├── temp/                      # 临时文件（定期清理）
│   └── [根据需求添加子目录]
│
├── .learnings/                # 学习记录
│   ├── ERRORS.md              # 错误记录 ⭐
│   ├── SUCCESSES.md           # 成功实践 ⭐
│   └── LEARNINGS.md           # 学习笔记
│
├── SOUL.md                    # 身份定义
├── AGENTS.md                  # 启动流程
├── MEMORY.md                  # 记忆索引
├── USER.md                    # 用户画像
├── HEARTBEAT.md               # 心跳自检
└── WORKSPACE-TEMPLATE.md      # 本文件
```

---

## 🚀 启动流程（新会话必须执行）

```bash
# 1. 读取核心文件
1. Read SOUL.md          # 身份 + 团队清单
2. Read USER.md          # 用户画像
3. Read memory/YYYY-MM-DD.md  # 今日 + 昨日日志
4. If MAIN SESSION: Read MEMORY.md  # 索引层

# 2. 检查状态
5. Check shared/inbox/   # 是否有新任务
6. Check shared/status/  # 进行中的任务

# 3. 准备就绪
7. Greet user with persona
```

---

## ⚠️ 已知的坑（通用机制问题）

### 1. MEMORY.md 容量爆炸

**现象**：MEMORY.md 超过 100 行，难以维护
**原因**：把详细内容写进了索引文件
**方案**：
- ✅ MEMORY.md **只放链接**，<50 行
- ✅ 详细内容放 `memory/YYYY-MM-DD.md` 或 `memory/projects.md`
- ✅ 超过 80% 容量 → 提示合并条目

---

### 2. 子 Agent 交付不验收

**现象**：子 Agent 说"完成"，主 Agent 直接汇报，结果文件不存在
**原因**：没有验收机制
**方案**：
- ✅ 交付必须验收：文件存在 + 内容完整 + 索引同步
- ✅ 创建验收清单：`memory/DELIVERY-CHECKLIST.md`

---

### 3. 索引文件死链

**现象**：MEMORY.md 引用的文件不存在
**原因**：文件移动/删除后未更新索引
**方案**：
- ✅ 定期校验：`python3 scripts/validate-index-paths.py`
- ✅ 有错误 → 记录到 `.learnings/ERRORS.md`

---

### 4. 硬编码 vs 推理混淆

**现象**：在需要推理的场景使用硬编码（如复盘 grep "error"）
**原因**：没有判断框架
**方案**：
- ✅ 创建判断框架：`memory/HARDCODE-VS-REASONING.md`
- ✅ 核心铁律：**复盘/分析任务 = 必须用推理**

---

### 5. 子 Agent 沙箱隔离

**现象**：子 Agent 生成的文件，主 Agent 找不到
**原因**：子 Agent 有独立沙箱，相对路径不互通
**方案**：
- ✅ 使用绝对路径：`/home/node/.openclaw/workspace/shared/outbox/`
- ✅ 或用 `sessions_send` 实时通信（推荐）

---

### 6. 异步任务无进度反馈

**现象**：派发长时间任务后，用户不知道进度
**原因**：同步等待，无状态管理
**方案**：
- ✅ 异步调度：立即返回任务ID
- ✅ 状态文件：`shared/status/{task-id}.json`
- ✅ 进度查询：用户随时问"进度如何"

---

### 7. 技能包质量不稳定

**现象**：技能包缺少测试、缺少文档
**原因**：没有标准化流程
**方案**：
- ✅ 创建技能生产流程（可选）
- ✅ 验收标准：场景通过率 ≥ 80%，场景数量 ≥ 5 个

---

## 🔧 自动化脚本（推荐）

| 脚本 | 用途 | 必需 |
|------|------|------|
| `validate-index-paths.py` | 索引死链校验 | ✅ 推荐 |
| `check-index-coverage.py` | 索引覆盖检查 | ⭕ 可选 |
| `query-task-status.py` | 任务状态查询 | ⭕ 可选（异步调度时需要）|

---

## 📋 Cron 任务（示例）

**根据你的需求配置定时任务**：

| 类型 | 示例任务 | 频率 |
|------|---------|------|
| **维护类** | 索引校验、临时文件清理 | 周日 03:00 |
| **业务类** | 复盘、技能盘点、报告推送 | 根据需求 |

**配置方法**：
```bash
# 编辑 crontab
crontab -e

# 添加任务
0 3 * * 0 cd /path/to/workspace && python3 scripts/validate-index-paths.py
```

---

## 🎯 快速复刻步骤（新小龙虾）

### 第一步：创建目录结构

```bash
# 核心目录
mkdir -p agents/main memory skills user-data scripts shared/{inbox,outbox,status,working}
mkdir -p reports temp .learnings wiki/{concepts,entities,how-to}

# 学习记录
touch .learnings/ERRORS.md .learnings/SUCCESSES.md .learnings/LEARNINGS.md
```

### 第二步：创建核心文件

```bash
# 必需文件
touch SOUL.md AGENTS.md MEMORY.md USER.md HEARTBEAT.md

# 可选文件
touch IDENTITY.md TOOLS.md WORKSPACE-TEMPLATE.md
```

### 第三步：填写内容

1. **SOUL.md** → 定义身份、价值观、团队成员
2. **USER.md** → 填写用户姓名、时区、偏好
3. **MEMORY.md** → 创建索引结构（<50行）
4. **AGENTS.md** → 定义启动流程（参考本文件的"启动流程"部分）

### 第四步：安装基础技能（可选）

```bash
# 搜索技能
clawhub search <关键词>

# 安装技能
clawhub install <skill-name>
```

### 第五步：测试启动

```bash
# 模拟新会话启动
# 1. 读取 SOUL.md
# 2. 读取 USER.md
# 3. 读取今日日志
# 4. 检查 shared/inbox/
# 5. Greet user
```

---

## 📚 参考资料（可选）

- **行为规则**：`agents/main/PROTOCOLS.md`
- **价值观详解**：`agents/main/VALUES.md`
- **任务调度**：`memory/task-dispatch-flow.md`
- **索引联动**：`memory/INDEX-SYNC-RULE.md`

---

## 🔄 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-04-06 | 优化为通用模板，移除个人配置 |
| v1.0 | 2026-04-06 | 初始版本 |

---

_此文件是 workspace 的"骨架定义"，更新时同步修改版本号_
