#!/bin/bash
# 闲鱼数据抓取技能 - 统一入口脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$SCRIPT_DIR/../.."
cd "$WORKSPACE_DIR"

echo "🐾 闲鱼数据抓取技能 v2.0"
echo "========================================"
echo ""

# 检查配置
if [ ! -f ".xianyu-grabber-config.json" ]; then
    echo "⚠️  配置文件不存在，使用模板创建..."
    cp .xianyu-grabber-config.template.json .xianyu-grabber-config.json
    echo "📝 请编辑 .xianyu-grabber-config.json 填入你的配置"
    echo ""
fi

# 显示帮助
show_help() {
    echo "用法：$0 [命令] [参数]"
    echo ""
    echo "命令:"
    echo "  grab [关键词...]    抓取指定关键词（不传则使用配置文件）"
    echo "  grab-all            抓取所有 60+ 关键词"
    echo "  ocr [截图路径]      对指定截图进行 OCR"
    echo "  upload              上传数据到 Gitee"
    echo "  report              生成汇总报告"
    echo "  visualize           生成可视化图表（价格分布/热度图）"
    echo "  recommend           生成智能推荐（选品/定价/利润）"
    echo "  cron                配置定时任务"
    echo "  check-update        检查新版本"
    echo "  self-update         自动更新到最新版本"
    echo "  clean               清理临时文件"
    echo "  status              显示当前状态"
    echo "  help                显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 grab Magisk KernelSU          # 抓取 2 个关键词"
    echo "  $0 grab-all                       # 抓取所有关键词"
    echo "  $0 visualize                      # 生成可视化图表"
    echo "  $0 recommend                      # 生成智能推荐"
    echo "  $0 cron                           # 配置定时任务"
    echo "  $0 upload                         # 上传到 Gitee"
    echo ""
}

# 抓取函数
do_grab() {
    echo "🚀 开始抓取..."
    node "$SCRIPT_DIR/grabber-enhanced.js" "$@"
}

# 抓取全部
do_grab_all() {
    echo "🚀 抓取所有 60+ 关键词（预计 30-40 分钟）..."
    node "$SCRIPT_DIR/grabber-enhanced.js" --all
}

# OCR 函数
do_ocr() {
    if [ -z "$1" ]; then
        echo "❌ 请指定截图路径"
        exit 1
    fi
    echo "🔍 OCR 识别：$1"
    python3 "$SCRIPT_DIR/ocr-enhanced.py" "$1"
}

# 上传函数
do_upload() {
    echo "📤 上传到 Gitee..."
    bash "$SCRIPT_DIR/uploader.sh" legion/data legion/xianyu-enhanced-final-report.md
}

# 生成报告
do_report() {
    echo "📄 生成汇总报告..."
    python3 << 'EOF'
import json
import os

data_dir = 'legion/data'
data_file = os.path.join(data_dir, 'xianyu-43keywords-data.json')

if not os.path.exists(data_file):
    print("❌ 数据文件不存在")
    exit(1)

with open(data_file, 'r', encoding='utf8') as f:
    data = json.load(f)

total = sum(r['count'] for r in data)
with_price = sum(1 for r in data for p in r['products'] if p['price'])

print(f"\n📊 数据统计:")
print(f"   关键词：{len(data)} 个")
print(f"   商品：{total} 个")
print(f"   含价格：{with_price} ({with_price/total*100:.1f}%)")

# TOP10
print(f"\n🔥 TOP10 关键词:")
sorted_data = sorted(data, key=lambda x: x['count'], reverse=True)
for i, r in enumerate(sorted_data[:10], 1):
    print(f"   {i:2}. {r['keyword']:15} {r['count']:3} 个")
EOF
}

# 可视化
do_visualize() {
    echo "📊 生成可视化图表..."
    python3 "$SCRIPT_DIR/visualize.py"
}

# 智能推荐
do_recommend() {
    echo "🤖 生成智能推荐..."
    python3 "$SCRIPT_DIR/recommend.py"
}

# 定时任务配置
do_cron() {
    echo "⏰ 配置定时任务..."
    bash "$SCRIPT_DIR/cron-setup.sh"
}

# 检查更新
do_check_update() {
    echo "🔍 检查更新..."
    bash "$SCRIPT_DIR/update.sh"
}

# 自动更新
do_self_update() {
    echo "🔄 自动更新..."
    bash "$SCRIPT_DIR/update.sh"
}

# 清理函数
do_clean() {
    echo "🧹 清理临时文件..."
    find legion/screenshots -name "*_processed.png" -delete 2>/dev/null || true
    find legion/data -name "*.tmp" -delete 2>/dev/null || true
    echo "✅ 清理完成"
}

# 状态函数
do_status() {
    echo "📊 当前状态:"
    echo ""
    echo "截图:"
    ls legion/screenshots/xianyu-*.png 2>/dev/null | wc -l
    echo "张"
    echo ""
    echo "数据文件:"
    ls -lh legion/data/xianyu-*.json 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
    echo ""
    echo "报告文件:"
    ls -lh legion/data/xianyu-*.md legion/*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
}

# 主逻辑
case "${1:-help}" in
    grab)
        shift
        do_grab "$@"
        ;;
    grab-all)
        do_grab_all
        ;;
    ocr)
        shift
        do_ocr "$@"
        ;;
    upload)
        do_upload
        ;;
    report)
        do_report
        ;;
    visualize)
        do_visualize
        ;;
    recommend)
        do_recommend
        ;;
    cron)
        do_cron
        ;;
    check-update)
        do_check_update
        ;;
    self-update)
        do_self_update
        ;;
    clean)
        do_clean
        ;;
    status)
        do_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ 未知命令：$1"
        show_help
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "👋 完成"
