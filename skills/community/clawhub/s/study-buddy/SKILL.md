---
name: study-buddy
description: 初高中学生家长的学习陪伴助手，帮助家长为孩子制定学习计划、追踪学习进度、管理错题本、生成学习报告。适用于家长辅导孩子学习、监督学习进度、记录学习成果。触发词包括"帮我制定学习计划"、"孩子学习打卡"、"查看学习进度"、"记录错题"、"生成学习报告"。
version: 1.2.0
author: jianghaidong
runtime:
  permissions:
    filesystem: true
  requires:
    python: ">=3.8"
---

# Study Buddy - 初高中学生家长学习陪伴助手

专为初高中学生家长设计的智能学习陪伴工具，帮助家长科学规划孩子学习、追踪学习进度、管理错题、生成学习报告，成为孩子学习路上的得力助手。

> 💡 **核心定位**：不做学科教学，专注学习管理——帮助家长和孩子建立良好的学习习惯，记录成长轨迹。

## 核心功能

1. **📋 学习档案** - 为每个孩子建立专属学习档案，记录学科、目标、水平、时间安排
2. **📅 学习计划** - 基于孩子实际情况生成阶段性学习计划（适应期→养成期→巩固期）
3. **✅ 每日打卡** - 记录每日学习内容和时长，培养坚持习惯
4. **📊 进度跟踪** - 统计学习天数、连续打卡、本周/本月学习情况
5. **📈 学习报告** - 周期性生成学习报告，评估学习阶段，给出家长建议
6. **📝 错题本** - 按学科分类记录错题，支持复习追踪和掌握标记
7. **👨‍👩‍👧 家长视角** - 专为家长设计，方便监督、查看、反馈孩子学习情况

## 🔒 安全说明

### 权限声明
- **文件系统访问**: 需要读写本地 JSON 文件，存储学习档案、计划、打卡记录和错题本
- **Python 环境**: 需要 Python 3.8+ 运行环境
- **数据处理**: 仅在本地处理用户学习数据，不发送到外部服务

### 安全边界
- ✅ 纯本地数据处理，不连接外部 API
- ✅ 使用标准 Python 库 (`json`, `os`, `datetime` 等)
- ✅ 数据默认存储在用户主目录 `~/.study-buddy/` 下，可用 `STUDY_BUDDY_HOME` 覆盖
- ✅ 代码开源可审计
- ❌ 不访问网络资源
- ❌ 不执行特权操作
- ❌ 不收集用户隐私信息

### 隐私保护
- 所有学习数据存储在 `~/.study-buddy/` 目录
- 不收集身份信息或学习内容到外部
- 用户完全控制数据删除和导出

## 命令入口

```bash
# 🚀 快速开始

# 1. 为孩子创建学习档案（交互式设置）
python3 scripts/study-buddy.py start

# 2. 查看今日学习任务
python3 scripts/study-buddy.py today

# 3. 学习打卡（记录学习内容和时长）
python3 scripts/study-buddy.py checkin "完成数学作业第3章" --duration "45分钟"

# 4. 查看学习进度统计
python3 scripts/study-buddy.py progress

# 5. 查看学习计划详情
python3 scripts/study-buddy.py plan

# 6. 生成学习周报/月报
python3 scripts/study-buddy.py report

# 7. 错题本管理
python3 scripts/study-buddy.py wrong add "二次函数求根公式应用错误" --subject "数学"
python3 scripts/study-buddy.py wrong list                    # 查看所有错题
python3 scripts/study-buddy.py wrong review "错题ID"         # 记录错题复习
python3 scripts/study-buddy.py wrong master "错题ID"         # 标记已掌握

# 8. 获取学习建议
python3 scripts/study-buddy.py feedback

# 9. 查看数据存储位置
python3 scripts/study-buddy.py data
```

## 数据存储

用户数据默认存储在: `~/.study-buddy/`

测试、演示或共享机器上可以设置隔离目录:

```bash
STUDY_BUDDY_HOME=/tmp/study-buddy-demo python3 scripts/study-buddy.py data
```

- `profile.json` - 学习背景档案
- `plans/` - 学习计划目录
- `logs/` - 学习记录日志
- `wrong_questions/` - 错题本
- `report_YYYYMMDD.json` - 学习报告

## 验证

```bash
python3 scripts/verify.py
```

验证脚本会使用临时 `STUDY_BUDDY_HOME`，覆盖新用户空档案状态和基础命令。

## 家长使用流程

### 第一步：初始化档案
运行 `start` 为孩子创建学习档案，记录学科、目标、每日时间等

### 第二步：查看学习计划
使用 `plan` 查看自动生成的三阶段计划（适应期→养成期→巩固期）

### 第三步：每日陪伴
- 使用 `today` 查看今日学习任务
- 孩子学习后，使用 `checkin` 记录学习内容和时长

### 第四步：定期复盘
- 使用 `progress` 查看学习统计数据
- 使用 `report` 生成周报/月报，评估学习效果

### 第五步：错题管理
使用 `wrong` 命令记录、复习、追踪错题掌握情况

## 目标用户

**核心用户**：初高中学生家长（初中、高中）

**使用场景**：
- 👨‍👩‍👧 家长为孩子制定学期/假期学习计划
- 📚 每日学习打卡和时长记录
- 📊 定期查看孩子学习进度和习惯养成情况
- 📝 整理各学科错题，追踪掌握程度
- 📈 阶段性复盘，调整学习策略

## 安全边界

### 我们提供的
- ✅ 学习计划制定框架和工具
- ✅ 学习进度追踪和统计
- ✅ 每日打卡记录
- ✅ 错题本管理
- ✅ 学习报告生成
- ✅ 学习习惯培养建议

### 我们不提供的
- ❌ 具体学科教学内容（如数学题解答、作文批改）
- ❌ 替代老师或家长的教育决策
- ❌ 连接外部教育平台或课程
- ❌ 夸张的学习效果承诺
- ❌ 收集敏感隐私信息

### 使用建议
- 💡 本工具是家长辅导的辅助，不能替代真人教师
- 💡 学习数据本地存储，家长完全掌控
- 💡 建议结合学校教学和专业辅导机构使用

## 扩展计划（未来规划，非当前版本）

以下功能为后续迭代方向，当前 MVP 版本未实现：

- [ ] Feishu集成
- [ ] 可视化报告
- [ ] 智能提醒功能
- [ ] 多计划管理
- [ ] 数据导出功能
- [ ] 更智能的计划生成算法

## 参考文档

- 命令详细说明: [references/commands.md](references/commands.md)
- 开发待办清单: [references/todo.md](references/todo.md)
