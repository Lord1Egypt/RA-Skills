# Skill Creator - 自动 Skill 生成系统

当检测到复杂或重复的任务模式时，自动生成新的 skill 来封装解决方案。

## 核心功能

1. **复杂任务检测** - 检测同一问题出现 3 次以上
2. **Skill 生成** - 根据任务模式生成新的 skill 文件
3. **触发词注册** - 自动注册触发新 skill 的关键词
4. **自我改进** - 跟踪 skill 使用效果并优化
5. **周期性提醒** - 主动扫描近期会话，建议写入记忆
6. **执行记录** - 记录 skill 执行结果，用于后续分析改进

## 工作流程

```
检测到重复问题 (≥3次)
        ↓
分析问题模式 & 提取解决方案
        ↓
生成新 Skill (SKILL.md + scripts/)
        ↓
注册触发词
        ↓
建议用户启用
        ↓
使用反馈 → 自我改进
```

## 自动生成的 Skill 结构

```
{skill-name}/
├── SKILL.md           # Skill 定义
├── README.md          # 使用说明
├── scripts/
│   ├── main.py        # 主入口
│   └── ...
└── references/
    └── SPEC.md        # 规范文档
```

## 使用方式

```bash
# 检测复杂任务
python3 auto_skill_generator.py --detect

# [NEW] 周期性提醒：检查值得记住的内容
python3 auto_skill_generator.py --remind
python3 auto_skill_generator.py --remind --days 7  # 扫描近7天

# 生成新 Skill
python3 auto_skill_generator.py --generate --name "项目任务追踪"

# 注册触发词
python3 auto_skill_generator.py --register --skill "任务追踪" --triggers "任务,追踪,todo"

# 查看统计
python3 auto_skill_generator.py --stats

# [NEW] 记录 Skill 执行结果（Hook: session:end 调用）
python3 auto_skill_generator.py --record --skill "task-tracker" --success --feedback "工作正常"

# [NEW] 自我改进
python3 auto_skill_generator.py --improve
python3 auto_skill_generator.py --improve --skill "task-tracker"  # 改进指定 Skill
python3 auto_skill_generator.py --improve --dry-run  # 预览模式
```

## 触发时机

- 同一问题/话题出现 3 次以上时自动建议
- 用户显式请求 "帮我自动化这个流程"
- consolidation 时发现可封装的模式