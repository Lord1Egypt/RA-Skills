#!/bin/bash
# RSS 文章转微信公众号 - 主脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 使用方法
usage() {
  cat << EOF
用法: $0 [选项]

选项:
  --url <URL>        指定文章 URL
  --auto             自动选择最新文章
  --config           显示配置帮助
  --check            检查配置和依赖
  --help             显示帮助信息

功能:
  1. 从 RSS 或指定 URL 获取文章
  2. 解析文章内容（标题、作者、正文）
  3. 提供 AI 助手生成微信格式 HTML 的指导
  4. 生成封面图（如果配置了 COVER_SKILL）
  5. 上传到微信草稿箱（如果配置了微信凭证）

示例:
  # 首次使用：检查配置
  $0 --check
  
  # 指定文章 URL
  $0 --url "https://simonwillison.net/2026/Mar/6/agentic-patterns/"
  
  # 自动选择最新文章（需要 blogwatcher）
  $0 --auto

配置:
  复制 config.example.sh 为 config.local.sh 并编辑你的配置。
  运行 $0 --config 查看详细说明。

EOF
  exit 1
}

# 解析参数
URL=""
AUTO=false
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --url)
      URL="$2"
      shift 2
      ;;
    --auto)
      AUTO=true
      shift
      ;;
    --config)
      show_config_help
      exit 0
      ;;
    --check)
      CHECK_ONLY=true
      shift
      ;;
    --help)
      usage
      ;;
    *)
      error "未知参数: $1"
      usage
      ;;
  esac
done

# 检查配置和依赖
if [ "$CHECK_ONLY" = true ]; then
  log "检查配置和依赖..."
  echo ""
  
  # 检查配置文件
  if [ -f "$SCRIPT_DIR/config.local.sh" ]; then
    echo "✅ 本地配置文件存在: config.local.sh"
  else
    echo "⚠️  本地配置文件不存在"
    echo "   运行: cp config.example.sh config.local.sh"
    echo "   然后编辑 config.local.sh 设置你的配置"
  fi
  
  echo ""
  
  # 检查必需工具
  echo "必需工具:"
  for cmd in curl jq pandoc; do
    if command -v "$cmd" &> /dev/null; then
      echo "  ✅ $cmd"
    else
      echo "  ❌ $cmd (未安装)"
    fi
  done
  
  echo ""
  
  # 检查可选工具
  echo "可选工具:"
  if command -v blogwatcher &> /dev/null; then
    echo "  ✅ blogwatcher (支持 --auto 模式)"
  else
    echo "  ⚠️  blogwatcher (未安装，--auto 模式不可用)"
  fi
  
  echo ""
  
  # 检查微信配置
  echo "微信公众号配置:"
  if [ -n "$WECHAT_APPID" ] && [ "$WECHAT_APPID" != "your_appid_here" ]; then
    echo "  ✅ WECHAT_APPID: $WECHAT_APPID"
  else
    echo "  ⚠️  WECHAT_APPID 未配置"
  fi
  
  if [ -n "$WECHAT_APPSECRET" ] && [ "$WECHAT_APPSECRET" != "your_secret_here" ]; then
    echo "  ✅ WECHAT_APPSECRET: ********"
  else
    echo "  ⚠️  WECHAT_APPSECRET 未配置"
  fi
  
  if [ -n "$WECHAT_PUBLISH_SCRIPT" ] && [ -f "$WECHAT_PUBLISH_SCRIPT" ]; then
    echo "  ✅ 发布脚本: $WECHAT_PUBLISH_SCRIPT"
  else
    echo "  ⚠️  发布脚本未配置或不存在"
  fi
  
  echo ""
  
  # 检查封面生成
  echo "封面生成:"
  if [ -n "$COVER_SKILL" ] && [ -f "$COVER_SKILL" ]; then
    echo "  ✅ 封面生成脚本: $COVER_SKILL"
  else
    echo "  ⚠️  封面生成脚本未配置（将跳过封面生成）"
  fi
  
  echo ""
  
  # 检查目录
  echo "工作目录:"
  echo "  输出目录: $OUTPUT_DIR"
  echo "  草稿目录: $DRAFTS_DIR"
  
  if [ -d "$OUTPUT_DIR" ] && [ -d "$DRAFTS_DIR" ]; then
    echo "  ✅ 目录已创建"
  fi
  
  echo ""
  
  # 验证配置
  if validate_config; then
    echo "✅ 配置检查通过！"
    exit 0
  else
    echo "❌ 配置检查失败，请修复上述问题"
    exit 1
  fi
fi

# 获取北京时间
DATE=$(TZ=Asia/Shanghai date "+%Y年%m月%d日")
WEEKDAY=$(TZ=Asia/Shanghai date "+星期%u" | sed 's/1/一/;s/2/二/;s/3/三/;s/4/四/;s/5/五/;s/6/六/;s/7/日/')
TIMESTAMP=$(TZ=Asia/Shanghai date "+%Y-%m-%d")

log "📰 RSS to WeChat - $DATE $WEEKDAY"
echo ""

# 1. 获取文章
if [ "$AUTO" = true ]; then
  log "1️⃣ 自动选择最新文章..."
  # 获取最新的未读文章
  LATEST=$(blogwatcher articles | grep "^\[" | grep "\[new\]" | head -1)
  if [ -z "$LATEST" ]; then
    error "没有找到未读文章"
    exit 1
  fi
  
  # 提取 URL
  URL=$(echo "$LATEST" | grep -oE 'https?://[^ ]+')
  TITLE=$(echo "$LATEST" | sed 's/^\[[0-9]*\] \[new\] //' | sed 's/ *$//')
  
  log "选中文章: $TITLE"
  log "URL: $URL"
elif [ -n "$URL" ]; then
  log "1️⃣ 解析指定文章..."
  log "URL: $URL"
else
  error "请指定 --url 或 --auto"
  usage
fi

echo ""

# 2. 解析文章内容
log "2️⃣ 解析文章内容..."
ARTICLE_JSON="$OUTPUT_DIR/rss-article-$TIMESTAMP.json"
bash "$SCRIPT_DIR/parse-article.sh" "$URL" "$ARTICLE_JSON"

# 读取解析结果
ARTICLE_TITLE=$(jq -r '.title' "$ARTICLE_JSON")
ARTICLE_AUTHOR=$(jq -r '.author' "$ARTICLE_JSON")
ARTICLE_PUBLISHED=$(jq -r '.published' "$ARTICLE_JSON")
ARTICLE_CONTENT=$(jq -r '.content' "$ARTICLE_JSON")

log "标题: $ARTICLE_TITLE"
log "作者: $ARTICLE_AUTHOR"
log "发布: $ARTICLE_PUBLISHED"
log "内容长度: $(echo "$ARTICLE_CONTENT" | wc -c) 字符"

echo ""

# 3. 提供 AI 助手指导
log "3️⃣ 数据已准备，请使用 AI 助手生成微信格式 HTML"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 文章数据"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 数据文件: $ARTICLE_JSON"
echo ""
echo "📝 文章信息:"
echo "   标题: $ARTICLE_TITLE"
echo "   作者: $ARTICLE_AUTHOR"
echo "   发布: $ARTICLE_PUBLISHED"
echo "   URL: $URL"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎨 生成要求"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. HTML 格式要求:"
echo "   ✓ 使用 <section> 和 <p> 标签（不用 <div>）"
echo "   ✓ 所有样式内联（style=\"...\"）"
echo "   ✓ 不使用 class 和 id 属性"
echo "   ✓ 不使用相对链接（<a> 标签）"
echo "   ✓ 使用 <strong> 和 <em> 而非 <span>"
echo "   ✓ 使用 <br/> 换行"
echo ""
echo "2. 内容结构:"
echo "   ✓ 头部品牌 Logo（内联 SVG）"
echo "   ✓ 日期栏（$DATE $WEEKDAY）"
echo "   ✓ 标题"
echo "   ✓ 核心观点（TL;DR）"
echo "   ✓ 详细内容（分段落）"
echo "   ✓ 原文链接"
echo ""
echo "3. 品牌配置:"
echo "   名称: $BRAND_NAME"
echo "   Slogan: $BRAND_SLOGAN"
echo "   主色: $BRAND_COLOR"
echo ""
echo "4. 参考模板:"
echo "   $SCRIPT_DIR/html-template.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💾 输出文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "HTML: $DRAFTS_DIR/rss-$TIMESTAMP.html"
if [ -n "$COVER_SKILL" ]; then
  echo "封面: $DRAFTS_DIR/rss-$TIMESTAMP-cover.png"
fi
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 后续步骤"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 生成 HTML（AI 助手）:"
echo "   根据上述要求和参考模板，生成微信格式 HTML"
echo "   保存到: $DRAFTS_DIR/rss-$TIMESTAMP.html"
echo ""

# 封面生成步骤（如果配置了）
if [ -n "$COVER_SKILL" ] && [ -f "$COVER_SKILL" ]; then
  echo "2. 生成封面:"
  echo "   bash \"$COVER_SKILL\" \\"
  echo "     \"$ARTICLE_TITLE\" \\"
  echo "     \"$DRAFTS_DIR/rss-$TIMESTAMP-cover.png\""
  echo ""
  STEP_NUM=3
else
  warn "封面生成脚本未配置，跳过封面生成步骤"
  echo "2. 封面生成: 跳过（未配置 COVER_SKILL）"
  echo ""
  STEP_NUM=3
fi

# 发布步骤（如果配置了）
if [ -n "$WECHAT_PUBLISH_SCRIPT" ] && [ -f "$WECHAT_PUBLISH_SCRIPT" ]; then
  if [ -n "$WECHAT_APPID" ] && [ -n "$WECHAT_APPSECRET" ]; then
    echo "$STEP_NUM. 上传草稿:"
    echo "   bash \"$WECHAT_PUBLISH_SCRIPT\" \\"
    echo "     \"$ARTICLE_TITLE\" \\"
    echo "     \"$DRAFTS_DIR/rss-$TIMESTAMP.html\" \\"
    if [ -n "$COVER_SKILL" ]; then
      echo "     \"$DRAFTS_DIR/rss-$TIMESTAMP-cover.png\""
    else
      echo "     # 封面路径（如果有）"
    fi
    echo ""
  else
    warn "微信公众号配置不完整，跳过发布步骤"
    echo "$STEP_NUM. 上传草稿: 跳过（微信配置不完整）"
    echo "   请在 config.local.sh 中设置 WECHAT_APPID 和 WECHAT_APPSECRET"
    echo ""
  fi
else
  echo "$STEP_NUM. 上传草稿: 手动发布"
  echo "   登录微信公众平台: https://mp.weixin.qq.com"
  echo "   内容管理 → 草稿箱 → 新建图文 → 粘贴 HTML"
  echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 数据准备完成！"
