#!/bin/bash
# 小红书内容生成主脚本
# 用法: bash generate_content.sh "内容" "标题"

cd "$(dirname "$0")/.."

CONTENT="${1:-}"
TITLE="${2:-内容标题}"
OUTPUT_DIR="outputs/$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT_DIR"

# 生成 HTML 文件
HTML_FILE="$OUTPUT_DIR/content.html"

cat > "$HTML_FILE" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #fff5f5 0%, #fff9f0 50%, #f0f8ff 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 680px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(255,107,107,0.3);
        }
        .header h1 { color: white; font-size: 28px; font-weight: 700; margin-bottom: 8px; }
        .header .subtitle { color: rgba(255,255,255,0.9); font-size: 14px; }
        .tag-row { display: flex; gap: 8px; margin-top: 15px; flex-wrap: wrap; }
        .tag { background: rgba(255,255,255,0.25); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }
        .card-title { font-size: 18px; font-weight: 600; color: #333; margin-bottom: 12px; }
        .section {
            background: linear-gradient(135deg, #fef6f3 0%, #fdfbf9 100%);
            border-left: 4px solid #ff6b6b;
            padding: 16px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 16px;
        }
        .highlight-box {
            background: linear-gradient(135deg, #fff5f5, #fff);
            border: 1px solid #ffcccc;
            border-radius: 12px;
            padding: 16px;
            margin: 12px 0;
        }
        .conclusion {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
            border-radius: 16px;
            padding: 24px;
            color: white;
        }
        .conclusion h3 { font-size: 18px; margin-bottom: 12px; }
        .footer {
            text-align: center;
            padding: 30px;
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>__TITLE__</h1>
            <div class="subtitle">__SUBTITLE__</div>
            <div class="tag-row">
                <span class="tag">__TAGS__</span>
            </div>
        </div>
        <div class="card">
            <div class="section">
                <p>__CONTENT__</p>
            </div>
        </div>
        <div class="footer">
            收藏 ❤️ 后慢慢看 | 关注获取更多干货 🔔
        </div>
    </div>
</body>
</html>
HTMLEOF

# 替换占位符
sed -i "s/__TITLE__/$TITLE/g" "$HTML_FILE"
sed -i "s/__SUBTITLE__/$SUBTITLE/g" "$HTML_FILE"
sed -i "s/__TAGS__/$TAGS/g" "$HTML_FILE"
sed -i "s/__CONTENT__/$CONTENT/g" "$HTML_FILE"

echo "✅ HTML 已生成: $HTML_FILE"
echo "📁 输出目录: $OUTPUT_DIR"
