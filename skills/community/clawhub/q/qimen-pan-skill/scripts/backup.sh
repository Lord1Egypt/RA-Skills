#!/bin/bash
# 奇门排盘技能备份脚本
# 天工长老开发 v1.0

# 配置
SKILL_DIR="$HOME/.openclaw/skills/qimen-pan-skill"
BACKUP_DIR="$SKILL_DIR/backup"
MAX_BACKUPS=5  # 保留最近 5 个版本

# 生成备份目录名（带时间戳）
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${TIMESTAMP}"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

# 创建备份目录
mkdir -p "$BACKUP_PATH"

# 备份文件
echo "🏮 天工长老：开始备份奇门排盘技能..."
echo "备份目标：$BACKUP_PATH"

# 复制技能文件
cp -r "$SKILL_DIR/scripts" "$BACKUP_PATH/"
cp -r "$SKILL_DIR/references" "$BACKUP_PATH/"
cp "$SKILL_DIR/SKILL.md" "$BACKUP_PATH/"

# 记录备份信息
cat > "$BACKUP_PATH/BACKUP_INFO.md" << EOF
# 备份信息

- **备份时间：** $(date '+%Y-%m-%d %H:%M:%S')
- **技能版本：** 待填写
- **备份原因：** 迭代更新前备份
- **备份人：** 天工长老

## 备份文件列表

$(find "$BACKUP_PATH" -type f -name "*.py" -o -name "*.md" | sort)

## 恢复方法

\`\`\`bash
# 恢复到技能目录
cp -r $BACKUP_PATH/scripts/* $SKILL_DIR/scripts/
cp -r $BACKUP_PATH/references/* $SKILL_DIR/references/
cp $BACKUP_PATH/SKILL.md $SKILL_DIR/
\`\`\`
EOF

# 检查备份是否成功
if [ -f "$BACKUP_PATH/SKILL.md" ]; then
    echo "✅ 备份成功！"
    echo "备份位置：$BACKUP_PATH"
    
    # 清理旧备份（保留最近 MAX_BACKUPS 个）
    cd "$BACKUP_DIR"
    BACKUP_COUNT=$(ls -1d backup_* 2>/dev/null | wc -l)
    
    if [ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]; then
        echo "清理旧备份（保留最近 $MAX_BACKUPS 个）..."
        ls -1dt backup_* | tail -n +$((MAX_BACKUPS + 1)) | xargs rm -rf
        echo "清理完成"
    fi
else
    echo "❌ 备份失败！"
    exit 1
fi

echo ""
echo "🏮 天工长老：备份完成，请主人放心。"
