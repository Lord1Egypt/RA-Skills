# 🧠 Agent Self-Learning Skill

让 Agent 通过分析对话历史，自动提取关键信息并更新配置文件，实现持续自我成长。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-3.0.0-green.svg)](CHANGELOG.md)

---

## ✨ 特性

### 双引擎学习系统

#### 🔄 引擎 A: 配置文件更新
- 分析对话历史，提取关键信息
- AI 判断需要新增/删除/更新
- 自动更新 8 个核心配置文件

#### 📝 引擎 B: 学习记录系统
- 即时记录纠正、错误、功能请求
- 结构化条目 (ID/优先级/状态)
- Pattern-Key 追踪重复模式
- 自动提升到项目文件

### 企业级特性
- 💾 **安全备份** - 自动备份，支持回滚
- 📊 **完整日志** - 详细的执行日志和历史记录
- 🔧 **灵活配置** - YAML 配置文件支持
- 🧪 **单元测试** - 完整的测试覆盖
- 🌐 **通用化** - 支持任何 Agent 平台
- 🔗 **Hook 集成** - OpenClaw 自动提醒

---

## 🚀 快速开始

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/Acczdy/self-learning-skill.git
cd self-learning-skill

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化学习记录目录
python3 scripts/learning_manager_cli.py --workspace /path/to/workspace init
```

### 配置文件更新

```bash
# 自动检测工作目录
python3 scripts/memory_update.py

# 指定工作目录
python3 scripts/memory_update.py --workspace /path/to/workspace

# 预览模式
python3 scripts/memory_update.py --dry-run
```

### 学习记录管理

```bash
# 添加学习记录
python3 scripts/learning_manager_cli.py --workspace /path/to/workspace add-learning \
  --category "correction" \
  --summary "用户纠正了 API 用法" \
  --priority "high"

# 添加错误记录
python3 scripts/learning_manager_cli.py --workspace /path/to/workspace add-error \
  --command "git push" \
  --error "permission denied"

# 添加功能请求
python3 scripts/learning_manager_cli.py --workspace /path/to/workspace add-feature \
  --capability "支持 Telegram 推送"

# 查看待处理条目
python3 scripts/learning_manager_cli.py --workspace /path/to/workspace list-pending

# 检查重复模式
python3 scripts/learning_manager_cli.py --workspace /path/to/workspace check-recurring
```

### Hook 配置 (OpenClaw)

```bash
# 复制 Hook
cp -r hooks/openclaw ~/.openclaw/hooks/self-learning

# 启用 Hook
openclaw hooks enable self-learning
```

---

## 📋 目录结构

```
self-learning-skill/
├── scripts/
│   ├── memory_update.py    # 主执行脚本 (27KB)
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

---

## 🔧 配置说明

### config.yaml

```yaml
# 工作目录配置
workspace:
  default: ./workspace
  auto_detect: true

# 核心配置文件
core_files:
  - MEMORY.md
  - IDENTITY.md
  - USER.md
  - TOOLS.md
  - SOUL.md
  - AGENTS.md
  - BOOTSTRAP.md
  - HEARTBEAT.md

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

---

## 📊 执行流程

```
1. 自动检测工作目录
   ↓
2. 读取 8 个核心配置文件
   ↓
3. 获取过去 24 小时对话历史
   ↓
4. AI 智能分析需要更新的内容
   ↓
5. 备份所有配置文件
   ↓
6. 执行更新操作
   ↓
7. 验证文件有效性
   ↓
8. 创建每日记忆文件
   ↓
9. 保存执行历史
   ↓
10. 清理 7 天前的备份
   ↓
完成 ✅
```

---

## 🧪 测试

```bash
# 运行所有测试
python3 -m pytest tests/

# 运行特定测试类
python3 -m pytest tests/test_main.py::TestConfig

# 查看测试覆盖率
python3 -m pytest tests/ --cov=scripts
```

---

## 📈 版本历史

详见 [CHANGELOG.md](CHANGELOG.md)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 支持

- 问题反馈：[GitHub Issues](https://github.com/Acczdy/self-learning-skill/issues)
- 讨论交流：[GitHub Discussions](https://github.com/Acczdy/self-learning-skill/discussions)

---

*Made with ❤️ by Acczdy*
