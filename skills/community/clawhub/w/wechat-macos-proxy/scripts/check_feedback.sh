#!/bin/bash
# 查询 wechat-macos-proxy 技能反馈

SKILL_SLUG="wechat-macos-proxy"
LOG_FILE="/tmp/wechat_proxy_feedback.log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') 查询技能反馈 ===" | tee -a "$LOG_FILE"

# 方法1：通过 clawhub inspect 获取技能信息
echo "[ClawHub 技能信息]" | tee -a "$LOG_FILE"
clawhub inspect "$SKILL_SLUG" 2>&1 | tee -a "$LOG_FILE" || echo "查询失败" | tee -a "$LOG_FILE"

# 方法2：检查是否有安装统计
echo "" | tee -a "$LOG_FILE"
echo "[技能统计]" | tee -a "$LOG_FILE"
clawhub explore --limit 50 2>&1 | grep -A5 -B5 "$SKILL_SLUG" | tee -a "$LOG_FILE" || echo "未在探索列表中找到" | tee -a "$LOG_FILE"

# 方法3：检查 GitHub 仓库（如果有）
# 暂时跳过，需要知道具体仓库地址

echo "" | tee -a "$LOG_FILE"
echo "=== 查询完成 ===" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 返回日志路径
echo "LOG_FILE:$LOG_FILE"
