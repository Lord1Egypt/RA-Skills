# OpenClaw 随机提问技能

**作者:** 咕咕嘎嘎
**版本:** 1.0.0
**许可证:** MIT License

一个智能的随机提问技能，帮助您进行自我觉察、反思和个人成长。

## 功能特点
- 🎯 **智能随机**：从8个维度、28个话题中均匀随机选择
- ⏰ **定时触发**：可配置的心跳机制，实现定时随机提问
- 🎨 **多维覆盖**：情绪、身体、思维、行动、关系、环境、反思、未来
- 🔧 **高度可定制**：支持话题库扩展、触发概率调整、个性化设置
- 📊 **使用统计**：详细的统计报告和图表分析
- 🔄 **上下文感知**：结合对话历史和个人档案

## 快速开始

### 1. 安装
```bash
chmod +x install.sh
./install.sh
```

### 2. 配置
1. 根据提示完成安装
2. 根据需要编辑配置文件：
```bash
vim ~/.openclaw/workspace/skills/random-question/config/default.yaml
```

### 3. 启动
```bash
# 启动心跳服务
openclaw heartbeat start

# 或手动测试
openclaw run "随机问我一个问题"
```

## 配置说明

### 基本配置
```yaml
settings:
  trigger_probability: 30        # 触发概率 (0-100)
  active_hours:
    start: "08:00"              # 开始时间
    end: "23:00"               # 结束时间
  min_interval_minutes: 30     # 最小间隔
```

### 个性化设置
```yaml
personalization:
  excluded_questions:           # 排除的问题ID
    - "B1"                     # 身体信号
    - "G4"                     # 定义今天
  favorite_categories:         # 偏好的类别
    - "A"                      # 内在状态层
    - "G"                      # 反思与元认知层
```

## 使用方法

### 手动触发
```
随机问我一个问题
!ask-random
来个随机问题
我想被提问一下
```

### 定时触发
默认每30分钟有30%概率触发随机提问，可在Heartbeat中调整。

### 查看统计
```bash
# 生成统计报告
python3 scripts/question_stats.py --report

# 生成图表
python3 scripts/question_stats.py --plot usage_trend.png

# JSON格式输出
python3 scripts/question_stats.py --report --format json
```

## 扩展开发

### 添加自定义问题
编辑 `SKILL.md` 文件，在相应类别下添加新问题。

### 集成到其他技能
```python
from scripts.random_selector import RandomQuestionGenerator

generator = RandomQuestionGenerator()
question = generator.get_random_question(force=True)
print(f"!announce {question['question']}")
```

## 故障排除

### 常见问题
1. **技能未加载**
```bash
# 检查技能列表
openclaw skill list

# 重新加载技能
openclaw skill reload random-question
```

2. **未收到提问**
```bash
# 检查心跳服务状态
openclaw heartbeat status

# 查看日志
openclaw heartbeat logs

# 手动测试
python3 scripts/random_selector.py --force
```

3. **问题重复**
- 调整 `question_weights.category_distribution` 设置
- 增加话题库数量
- 清除选择历史

## 文件结构
```
random-question-skill/
├── SKILL.md                    # 核心技能定义
├── README.md                   # 使用说明
├── HEARTBEAT.md                # 心跳配置文件
├── install.sh                  # 安装脚本
├── uninstall.sh               # 卸载脚本
├── scripts/
│   ├── random_selector.py     # 随机选择器
│   └── question_stats.py       # 统计工具
├── config/
│   └── default.yaml           # 默认配置文件
└── docs/                      # 文档
```

## 许可证
MIT License

## 支持
- 问题反馈：GitHub Issues
- 功能建议：GitHub Discussions
- 文档：查看 `docs/` 目录

## 贡献
欢迎提交Issue和Pull Request！
