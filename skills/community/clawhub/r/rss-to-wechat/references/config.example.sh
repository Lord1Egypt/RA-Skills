#!/bin/bash
# 配置示例文件
# 复制此文件为 config.local.sh 并修改为你的配置

# ============ 微信公众号配置（必需）============
# 从微信公众平台获取: https://mp.weixin.qq.com
# 设置与开发 → 基本配置 → 开发者ID(AppID) 和 开发者密码(AppSecret)
WECHAT_APPID="your_appid_here"
WECHAT_APPSECRET="your_secret_here"

# ============ 品牌配置 ============
BRAND_NAME="你的公众号名称"
BRAND_SLOGAN="你的 Slogan"
BRAND_COLOR="#c41e3a"  # 主色调（十六进制颜色）

# ============ RSS 订阅源（可选）============
# 你关注的博客或网站
RSS_SOURCES=(
  "example.com"
  "another-blog.com"
)

# ============ 筛选条件（可选）============
MIN_VIEWS_DAILY=10000       # 日报最低观看量
MAX_VIEWS_DAILY=100000      # 日报最高观看量
MIN_VIEWS_FEATURED=100000   # 精选最低观看量

# ============ 主题关键词（可选）============
# 优先级关键词（匹配这些的文章优先推荐）
PRIORITY_KEYWORDS=(
  "AI"
  "Machine Learning"
  "Technology"
)

# 通用关键词
GENERAL_KEYWORDS=(
  "programming"
  "software"
  "development"
)

# 排除关键词（包含这些的文章会被过滤）
EXCLUDE_KEYWORDS=(
  "crypto"
  "blockchain"
)

# ============ 路径配置（可选）============
# 如果不设置，将使用默认路径
# WORKSPACE="$HOME/my-workspace"
# OUTPUT_DIR="$WORKSPACE/output"
# DRAFTS_DIR="$WORKSPACE/drafts"

# ============ 外部工具（可选）============
# 如果你有自己的封面生成脚本
# COVER_SKILL="/path/to/your/cover-generator.sh"

# 如果你有自己的发布脚本
# WECHAT_PUBLISH_SCRIPT="/path/to/your/publish-script.sh"

# ============ 时区（可选）============
# TZ="Asia/Shanghai"  # 默认：Asia/Shanghai

# ============ 调试模式（可选）============
# DEBUG=1  # 启用详细日志
