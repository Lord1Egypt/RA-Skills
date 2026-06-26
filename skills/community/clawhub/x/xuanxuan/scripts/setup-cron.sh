#!/bin/bash
# 滚滚技能追踪自动化脚本
# 添加到 crontab: crontab -e

# 技能追踪目录
SKILL_TRACKER_DIR="/home/admin/.openclaw/workspace/skills/skill-tracker/scripts"

# 每天凌晨 3 点：计算健康度
0 3 * * * cd $SKILL_TRACKER_DIR && python3 calculate-health.py --summary >> /tmp/skill-health.log 2>&1

# 每周日凌晨 4 点：生成优化建议
0 4 * * 0 cd $SKILL_TRACKER_DIR && python3 generate-proposals.py --analyze >> /tmp/skill-proposals.log 2>&1

# 每月 1 号上午 9 点：生成月度报告
0 9 1 * * cd $SKILL_TRACKER_DIR && python3 generate-report.py --generate --days 30 >> /tmp/skill-report.log 2>&1

# 使用说明：
# 1. 编辑 crontab: crontab -e
# 2. 复制上面的行到 crontab 文件
# 3. 保存并退出
# 4. 验证：crontab -l
