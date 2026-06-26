#!/bin/bash
# Session Guardian 配置文件

# ============================================
# 备份路径配置
# ============================================

# 备份根目录（可改为外部磁盘）
BACKUP_ROOT="${BACKUP_ROOT:-$HOME/.openclaw/workspace/Assets/SessionBackups}"

# OpenClaw agents 目录
AGENTS_DIR="${AGENTS_DIR:-$HOME/.openclaw/agents}"

# OpenClaw cron 目录
CRON_DIR="${CRON_DIR:-$HOME/.openclaw/cron}"

# ============================================
# 备份频率配置
# ============================================

# 增量备份间隔（分钟）
INCREMENTAL_INTERVAL=5

# 快照间隔（小时）
HOURLY_INTERVAL=1

# 每日总结时间（cron 表达式）
DAILY_SUMMARY_CRON="0 2 * * *"

# 时区
TIMEZONE="Asia/Shanghai"

# ============================================
# 保留策略配置
# ============================================

# 增量备份保留时间（天）
INCREMENTAL_KEEP_DAYS=7

# 快照保留时间（小时）
HOURLY_KEEP_HOURS=24

# 每日总结保留时间（天，0=永久）
DAILY_KEEP_DAYS=0

# ============================================
# AI 总结配置
# ============================================

# 总结模型（推荐使用 Claude Opus 4.6，效果最好）
SUMMARY_MODEL="claude-opus-4-6"

# 可选其他模型：
# SUMMARY_MODEL="qwen-max"         # 阿里云（便宜）
# SUMMARY_MODEL="gpt-4o"           # OpenAI
# SUMMARY_MODEL="deepseek-chat"    # DeepSeek（便宜）
# SUMMARY_MODEL="gemini-2.0-flash" # Google（快速）

# 总结提示词模板
SUMMARY_PROMPT_TEMPLATE="分析今天的所有对话记录，生成结构化总结。

要求：
1. 统计信息：总消息数、参与 Agent、活跃时段
2. 主要成果：列出完成的任务和交付物
3. 关键决策：记录重要决策及其依据
4. 军团协作：各军团的工作内容
5. 技术亮点：值得记录的技术细节
6. 待办事项：未完成的任务

格式：Markdown，清晰易读。"

# ============================================
# 推送配置
# ============================================

# 是否启用推送
DELIVERY_ENABLED=true

# 推送渠道
# - "last": 自动推送到用户最后使用的渠道（推荐，适配所有用户）
# - "webchat": Web 控制台（所有用户都有）
# - "telegram": Telegram
# - "whatsapp": WhatsApp
# - "discord": Discord
# - "slack": Slack
# - "signal": Signal
# - "imessage": iMessage
# - "dingtalk-connector": 钉钉（插件）
# - "feishu": 飞书（插件）
DELIVERY_CHANNEL="last"

# 推送目标（根据渠道不同格式不同）
# - "last": 留空即可，自动路由
# - Telegram: -1001234567890 或 -1001234567890:topic:123
# - WhatsApp: +15551234567
# - Discord: channel:123456789 或 user:123456789
# - 钉钉: user:2729293505776209
# - 飞书: user:ou_xxx
DELIVERY_TARGET=""

# 推送说明
# 如果使用 "last" 渠道，系统会自动推送到用户最后使用的渠道
# 这样无论用户用 Web、Telegram、钉钉还是其他渠道，都能收到通知

# ============================================
# 告警配置
# ============================================

# 是否启用告警
ALERT_ENABLED=false

# 钉钉 Webhook（用于告警）
ALERT_WEBHOOK=""

# 告警条件
ALERT_ON_BACKUP_FAIL=true       # 备份失败
ALERT_ON_LOW_SPACE=true         # 磁盘空间不足
ALERT_ON_FILE_COUNT_LOW=true    # 备份文件数量异常

# 磁盘空间告警阈值（GB）
ALERT_DISK_THRESHOLD_GB=1

# 备份文件数量告警阈值
ALERT_FILE_COUNT_THRESHOLD=3

# ============================================
# 性能优化配置
# ============================================

# rsync 超时时间（秒）
RSYNC_TIMEOUT=10

# 压缩工具（gzip / pigz）
# pigz 是多线程版本，速度快 3-4 倍
COMPRESS_TOOL="gzip"

# 压缩级别（1-9，9 最高压缩比但最慢）
COMPRESS_LEVEL=6

# 并发备份数量
MAX_CONCURRENT_BACKUPS=1

# ============================================
# 高级配置
# ============================================

# 是否启用加密
ENCRYPTION_ENABLED=false

# GPG 密钥 ID
GPG_KEY_ID=""

# 是否启用远程同步
REMOTE_SYNC_ENABLED=false

# 远程同步方式（rsync / rclone）
REMOTE_SYNC_METHOD="rsync"

# rsync 远程主机
REMOTE_RSYNC_HOST=""
REMOTE_RSYNC_USER=""
REMOTE_RSYNC_PATH=""

# rclone 远程配置
REMOTE_RCLONE_REMOTE=""

# ============================================
# 日志配置
# ============================================

# 日志文件路径
LOG_FILE="$BACKUP_ROOT/backup.log"

# 日志级别（DEBUG / INFO / WARN / ERROR）
LOG_LEVEL="INFO"

# 日志保留时间（天）
LOG_KEEP_DAYS=30

# ============================================
# 健康检查配置
# ============================================

# Session 文件大小限制（MB）
SESSION_SIZE_LIMIT_MB=1

# 默认模型（用于自动修复缺失的 defaultModel）
DEFAULT_MODEL="opencode/claude-opus-4-6"

# 健康检查间隔（小时）
HEALTH_CHECK_INTERVAL=6

# 推送健康检查告警
PUSH_CHANNEL="${DELIVERY_CHANNEL}"
PUSH_TARGET="${DELIVERY_TARGET}"

# ============================================
# v2.0 新增配置
# ============================================

# 固定Agent vs 临时Subagent
FIXED_AGENT_SESSION_LIMIT_MB=5
SUBAGENT_SESSION_LIMIT_MB=1
FIXED_AGENT_KEEP_DAYS=90
SUBAGENT_KEEP_DAYS=7

# 协作追踪
COLLABORATION_TRACKING_ENABLED=true
COLLABORATION_GRAPH_ENABLED=true

# 知识提取
KNOWLEDGE_EXTRACTION_ENABLED=true
KNOWLEDGE_EXTRACTION_INTERVAL="0 0 * * 0"  # 每周日

# 协作健康度
COLLABORATION_HEALTH_CHECK_ENABLED=true
COLLABORATION_HEALTH_THRESHOLD=70  # 低于70分告警

# ============================================
# 内部变量（不要修改）
# ============================================

INCREMENTAL_DIR="$BACKUP_ROOT/incremental"
HOURLY_DIR="$BACKUP_ROOT/hourly"
DAILY_DIR="$BACKUP_ROOT/daily"
LOCK_FILE="/tmp/session-guardian-incremental.lock"
