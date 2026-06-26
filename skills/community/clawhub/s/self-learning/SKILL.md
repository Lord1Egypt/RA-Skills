---
name: self-learning
description: |
  Agent 自我学习与记忆更新技能。分析对话历史，提取关键信息，自动更新配置文件和学习记录，实现 Agent 持续自我成长。
  融合自学习 (配置文件更新) + 自改进 (学习记录系统) 双引擎。

  Use this skill when:
  - 需要整理和更新 Agent 记忆 (MEMORY.md, IDENTITY.md 等)
  - 对话中产生了新的配置信息或用户偏好
  - 用户纠正 Agent 或发现错误时 (记录到 .learnings/)
  - 定期执行 Agent 自我优化
  - 清理过时的配置和记忆

  Triggers: 自我学习、记忆更新、配置优化、Agent 成长、整理记忆、记录学习、纠正错误
version: 3.0.1
author: Acczdy
license: MIT
repository: https://github.com/Acczdy/self-learning-skill
allowed-tools:
  - Read
  - Write
  - Bash
  - SessionsList
  - SessionsHistory
  - SessionsSend
files:
  - scripts/memory_update.py: 主执行脚本 (配置文件更新)
  - scripts/learning_manager.py: 学习记录管理
  - .learnings/LEARNINGS.md: 学习记录模板
  - .learnings/ERRORS.md: 错误记录模板
  - .learnings/FEATURE_REQUESTS.md: 功能请求模板
  - config.yaml: 配置文件
  - hooks/openclaw/: OpenClaw Hook 集成
  - requirements.txt: Python 依赖
  - README.md: 使用说明
---

# 🧠 Agent 自我学习技能

让 Agent 通过分析对话历史，自动提取关键信息并更新配置文件，实现持续自我成长。

**通用化设计 | 多平台支持 | 学习记录系统 | Hook 集成**

## 🎯 核心功能

### 1. 双引擎学习系统 🚀

#### 引擎 A: 配置文件更新 (Memory Update)
- 分析过去 24 小时的对话内容
- AI 智能判断需要新增、删除还是更新
- 自动更新 8 个核心配置文件

#### 引擎 B: 学习记录系统 (Learning Log)
- 即时记录用户纠正、错误、功能请求
- 结构化条目 (ID/优先级/状态/分类)
- 支持提升到项目文件 (SOUL.md, AGENTS.md, TOOLS.md)
- Pattern-Key 追踪重复模式

### 2. 通用化设计 ✅
- 不局限于特定平台 (OpenClaw/其他)
- 工作目录自动检测
- 配置文件支持
- 环境变量支持

### 3. 配置文件更新
自动更新 8 个核心配置文件：
- `MEMORY.md` - 长期记忆 (必须)
- `IDENTITY.md` - Agent 身份
- `USER.md` - 用户信息
- `TOOLS.md` - 工具配置
- `SOUL.md` - 人格定义
- `AGENTS.md` - 使用指南
- `BOOTSTRAP.md` - 初始化引导
- `HEARTBEAT.md` - 心跳任务

### 4. 学习记录文件
自动创建和管理 `.learnings/` 目录:
- `LEARNINGS.md` - 纠正、知识缺口、最佳实践
- `ERRORS.md` - 命令失败、异常
- `FEATURE_REQUESTS.md` - 用户请求的功能

### 5. 条目 ID 系统
| 类型 | 格式 | 示例 |
|------|------|------|
| 学习 | `LRN-YYYYMMDD-XXX` | `LRN-20250115-001` |
| 错误 | `ERR-YYYYMMDD-XXX` | `ERR-20250115-A3F` |
| 功能 | `FEAT-YYYYMMDD-XXX` | `FEAT-20250115-002` |

### 6. 提升规则 (Promotion)
当学习内容广泛适用时，自动提升到项目文件:

| 学习类型 | 提升到 | 示例 |
|----------|--------|------|
| 行为模式 | `SOUL.md` | "简洁回复，避免免责声明" |
| 工作流改进 | `AGENTS.md` | "长任务使用子代理" |
| 工具技巧 | `TOOLS.md` | "Git push 需要先配置认证" |
| 项目约定 | `CLAUDE.md` | "使用 pnpm 而非 npm" |

### 7. Hook 集成 🔗
- **onSessionStart**: 会话开始时检查待处理高优先级条目
- **onPromptSubmit**: 检测用户纠正信号，建议记录

### 8. 企业级特性
- ✅ 完整的日志系统
- ✅ 执行历史记录
- ✅ 文件验证机制
- ✅ 自动备份与回滚
- ✅ 预览模式
- ✅ 单元测试覆盖
- ✅ 重复模式检测 (Recurrence-Count >= 3 自动提升)

## 🚀 快速开始

### 安装
```bash
# 1. 下载技能
git clone https://github.com/Acczdy/self-learning-skill.git
cd self-learning-skill

# 2. 安装依赖
pip install -r requirements.txt

# 3. 复制配置文件
cp config.yaml config.yaml

# 4. 初始化学习记录目录 (可选)
python3 scripts/learning_manager.py --init
```

### 基本使用
```bash
# 自动检测工作目录并执行学习
python3 scripts/memory_update.py

# 指定工作目录
python3 scripts/memory_update.py --workspace /path/to/workspace

# 预览模式 (不实际执行)
python3 scripts/memory_update.py --dry-run

# 使用自定义配置
python3 scripts/memory_update.py --config my_config.yaml
```

### 学习记录命令
```bash
# 添加学习记录
python3 scripts/learning_manager.py add-learning \
  --category "correction" \
  --summary "用户纠正了 API 用法" \
  --priority "high"

# 添加错误记录
python3 scripts/learning_manager.py add-error \
  --command "git push" \
  --error "permission denied"

# 添加功能请求
python3 scripts/learning_manager.py add-feature \
  --capability "支持 Telegram 推送" \
  --complexity "medium"

# 查看待处理高优先级条目
python3 scripts/learning_manager.py list-pending

# 检查重复模式
python3 scripts/learning_manager.py check-recurring
```

### Hook 配置 (OpenClaw)
```bash
# 复制 Hook 到 OpenClaw
cp -r hooks/openclaw ~/.openclaw/hooks/self-learning

# 启用 Hook
openclaw hooks enable self-learning

# 禁用 Hook
openclaw hooks disable self-learning
```

## 📋 执行流程

```
1. 自动检测工作目录
   ↓
2. 读取核心配置文件
   ↓
3. 获取对话历史
   ↓
4. AI 智能分析
   ↓
5. 备份配置文件
   ↓
6. 执行更新操作
   ↓
7. 验证文件有效性
   ↓
8. 创建每日记忆
   ↓
9. 保存执行历史
   ↓
10. 清理旧备份
   ↓
完成 ✅
```

## ⚠️ 安全特性

### 备份保护
- 更新前自动备份
- 保留 7 天备份
- 最多保留 10 个备份
- 支持手动回滚

### 文件验证
- Markdown 语法检查
- 更新后自动验证
- 失败自动回滚

### 删除保护
- 删除操作需确认
- 最大删除数量限制
- 删除理由必须明确

## 📊 输出示例

```
============================================================
🧠 Agent 自我学习开始 (main)
⏰ 时间：2026-03-05 01:30:00
📁 工作目录：/root/.openclaw/workspace
============================================================

📖 读取配置文件...
✅ 已读取 8 个配置文件

💾 备份配置文件...
💾 已备份到：/root/.openclaw/workspace/.backup/20260305_013000

📝 执行更新...
✅ 完成：MEMORY.md
✅ 完成：TOOLS.md

📅 创建每日记忆...
📜 保存执行历史...
🗑️ 清理旧备份...

============================================================
✅ Agent 自我学习完成 (main)
============================================================
```

## 🔧 配置说明

### config.yaml
```yaml
# 工作目录
workspace:
  default: ./workspace
  auto_detect: true

# 备份配置
backup:
  enabled: true
  retain_days: 7
  max_backups: 10

# 日志配置
logging:
  enabled: true
  level: INFO

# 安全配置
safety:
  validate_after_update: true
  max_delete_count: 10
```

## 📁 项目结构

```
self-learning-skill/
├── scripts/
│   ├── memory_update.py    # 主执行脚本
│   └── publish.sh          # 发布脚本
├── tests/
│   └── test_main.py        # 单元测试
├── examples/
│   ├── config.minimal.yaml # 最小化配置
│   └── config.full.yaml    # 完整配置
├── SKILL.md                # Skill 定义
├── README.md               # 使用说明
├── config.yaml             # 配置文件
├── requirements.txt        # Python 依赖
├── LICENSE                 # MIT 许可证
├── CHANGELOG.md            # 更新日志
└── .gitignore              # Git 忽略文件
```

## 🧪 测试

```bash
# 运行单元测试
python3 -m pytest tests/

# 运行特定测试
python3 -m pytest tests/test_main.py::TestConfig
```

## 📈 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **2.0.0** | 2026-03-05 | 通用化重构、日志系统、测试覆盖 |
| 1.1.0 | 2026-03-05 | 多 Agent 支持 |
| 1.0.0 | 2026-03-05 | 初始版本 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📞 支持

- 问题反馈：[GitHub Issues](https://github.com/Acczdy/self-learning-skill/issues)
- 讨论交流：[GitHub Discussions](https://github.com/Acczdy/self-learning-skill/discussions)

---

*最后更新：2026-03-05*
