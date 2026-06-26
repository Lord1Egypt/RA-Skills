# Study Buddy - 初高中学生家长学习陪伴助手

> 专为初高中学生家长设计的智能学习管理工具，帮助家长科学规划孩子学习、追踪学习进度、管理错题、生成学习报告。

## 🎯 产品定位

**不做学科教学，专注学习管理**

Study Buddy 是家长辅导孩子学习的得力助手，帮助建立良好的学习习惯，记录成长轨迹，让学习过程可视化、可追踪、可复盘。

**核心用户**：初高中学生家长

## ✨ 核心特性

| 功能 | 说明 | 家长价值 |
|------|------|----------|
| 📋 **学习档案** | 为孩子建立专属学习档案 | 全面了解孩子学习背景 |
| 📅 **学习计划** | 自动生成三阶段计划 | 科学规划，循序渐进 |
| ✅ **每日打卡** | 记录学习内容和时长 | 培养坚持习惯，可视化努力 |
| 📊 **进度统计** | 学习天数、连续打卡、周月统计 | 掌握孩子学习规律 |
| 📈 **学习报告** | 周期性生成评级报告 | 阶段性复盘，调整策略 |
| 📝 **错题本** | 按学科分类管理错题 | 针对性复习，追踪掌握程度 |
| 💡 **学习建议** | 基于数据给出个性化建议 | 获得科学辅导指导 |

## 🚀 快速开始

### 安装要求

```bash
# 确保有 Python 3.8+
python3 --version

# 进入 skill 目录
cd ~/.openclaw/workspace/study-buddy
```

### 家长使用指南

```bash
# 1️⃣ 为孩子创建学习档案
python3 scripts/study-buddy.py start

# 2️⃣ 查看今日学习任务
python3 scripts/study-buddy.py today

# 3️⃣ 孩子学习后打卡记录
python3 scripts/study-buddy.py checkin "完成数学作业第3章" --duration "45分钟"

# 4️⃣ 查看学习进度统计
python3 scripts/study-buddy.py progress

# 5️⃣ 查看学习计划
python3 scripts/study-buddy.py plan

# 6️⃣ 生成学习周报/月报
python3 scripts/study-buddy.py report

# 7️⃣ 错题本管理
python3 scripts/study-buddy.py wrong add "二次函数求根公式应用错误" --subject "数学"
python3 scripts/study-buddy.py wrong list
python3 scripts/study-buddy.py wrong review "错题ID"
python3 scripts/study-buddy.py wrong master "错题ID"

# 8️⃣ 获取学习建议
python3 scripts/study-buddy.py feedback

# 9️⃣ 查看数据存储位置
python3 scripts/study-buddy.py data

# 可选：隔离演示/测试数据，不碰真实 ~/.study-buddy/
STUDY_BUDDY_HOME=/tmp/study-buddy-demo python3 scripts/study-buddy.py data
```

## 📁 数据存储

所有数据默认存储在本地 `~/.study-buddy/` 目录，可用
`STUDY_BUDDY_HOME` 覆盖到临时目录：

```
~/.study-buddy/
├── profile.json           # 学习档案
├── plans/                 # 学习计划
│   └── plan_YYYYMMDD.json
├── logs/                  # 学习日志
│   └── YYYY-MM-DD.json
├── wrong_questions/       # 错题本
│   └── wrong_questions.json
└── report_YYYYMMDD.json   # 学习报告
```

## ✅ 验证

```bash
python3 scripts/verify.py
```

验证脚本会使用临时 `STUDY_BUDDY_HOME`，覆盖新用户空档案状态和基础命令，不会污染真实学习数据。

## 🎯 目标用户

### 核心用户
- 👨‍👩‍👧 初高中学生家长

### 适用场景
- 📚 制定学期/假期学习计划
- ⏰ 每日学习打卡和时长记录
- 📊 定期查看学习进度和习惯养成
- 📝 整理各学科错题，追踪掌握程度
- 📈 阶段性复盘，调整学习策略

### 使用建议
- 建议家长与孩子共同使用，培养自主学习能力
- 适合作为学校教育的补充，而非替代
- 数据本地存储，家长完全掌控

## 🛡️ 安全边界

- ✅ 学习计划制定、进度跟踪、打卡、反馈、学习报告
- ❌ 不提供具体学科教学内容（如数学题解答）
- ❌ 不替代老师/家长决策
- ❌ 不接外部教育平台
- ❌ 不做夸张的学习效果承诺
- ✅ 尊重用户隐私，数据本地存储

## 📚 文档

- [命令详细说明](references/commands.md)
- [开发待办清单](references/todo.md)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
