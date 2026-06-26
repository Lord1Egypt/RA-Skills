#!/bin/bash
# 股票分析报告 PDF 生成脚本（支持直接下载）
# 用法：./generate-pdf-report.sh <股票代码> <公司名>

STOCK_CODE=$1
COMPANY_NAME=$2
REPORT_DIR="/app/skills/stock-analysis/reports"
HTTP_PORT=8888

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码> <公司名>"
    exit 1
fi

mkdir -p "$REPORT_DIR"

# 1. 生成 HTML 报告
HTML_FILE="$REPORT_DIR/${COMPANY_NAME}_${STOCK_CODE}.html"
cat > "$HTML_FILE" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>$COMPANY_NAME ($STOCK_CODE) 投资价值分析报告</title>
    <style>
        body { font-family: Arial, 'Microsoft YaHei', sans-serif; margin: 2cm; line-height: 1.6; }
        h1 { color: #1a5490; border-bottom: 3px solid #1a5490; padding-bottom: 10px; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #1a5490; color: white; }
        .conclusion { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
<h1>📈 $COMPANY_NAME ($STOCK_CODE) 投资价值分析报告</h1>
<p style="text-align:center;">Stock Analysis Skill v1.4.1 | $(date +"%Y-%m-%d %H:%M")</p>

<div class="conclusion">
    <h2 style="color:white;margin:0;">🎯 核心结论</h2>
    <p>报告已生成完成！</p>
</div>

<div style="margin-top: 30px; text-align: center; font-size: 12px; color: #999;">
    <p>本报告由 Stock Analysis Skill 生成 | 仅供参考，不构成投资建议</p>
</div>
</body>
</html>
EOF

# 2. 启动 HTTP 服务器
if ! pgrep -f "http.server.*8888" > /dev/null; then
    cd "$REPORT_DIR" && python3 -m http.server $HTTP_PORT > /tmp/http-server.log 2>&1 &
    sleep 2
fi

# 3. 提供多种下载方式
echo ""
echo "✅ 报告生成完成！"
echo "📄 HTML 报告: $HTML_FILE"
echo ""
echo "🔗 下载方式："
echo ""
echo "方式 1: OpenClaw 文件浏览"
echo "   - 在 OpenClaw UI 中浏览路径：/app/skills/stock-analysis/reports/"
echo "   - 点击 ${COMPANY_NAME}_${STOCK_CODE}.html 文件"
echo "   - 按 Ctrl+P 选择 '另存为 PDF'"
echo ""
echo "方式 2: Docker 端口映射（如果已配置）"
echo "   - 确保容器 8888 端口映射到宿主机"
echo "   - 访问：http://localhost:8888/${COMPANY_NAME}_${STOCK_CODE}.html"
echo ""
echo "方式 3: 手动复制文件"
echo "   - docker cp <container>:$HTML_FILE ."
echo "   - 本地浏览器打开并另存为 PDF"
echo ""
echo "📁 报告目录: $REPORT_DIR"