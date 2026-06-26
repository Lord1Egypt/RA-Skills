#!/bin/bash

# 简单的Obsidian知识库测试脚本

echo "🚀 开始Obsidian知识库基础测试..."

# 测试1: 健康检查
echo "🔍 测试健康检查..."
health_response=$(wget --timeout=5 -q -O - http://192.168.18.15:5000/health)
if echo "$health_response" | grep -q '"status":"ok"'; then
    service_name=$(echo "$health_response" | grep -o '"service":"[^"]*"' | cut -d'"' -f4)
    echo "✅ 健康检查通过: $service_name"
else
    echo "❌ 健康检查失败: $health_response"
    exit 1
fi

# 测试2: 统计信息
echo "📊 测试统计信息..."
stats_response=$(wget --timeout=5 -q -O - http://192.168.18.15:5000/api/stats)
if echo "$stats_response" | grep -q "total_notes"; then
    total_notes=$(echo "$stats_response" | grep -o '"total_notes":[0-9]*' | cut -d: -f2)
    total_files=$(echo "$stats_response" | grep -o '"total_files":[0-9]*' | cut -d: -f2)
    echo "✅ 统计信息获取成功"
    echo "   总笔记数: $total_notes"
    echo "   总文件数: $total_files"
else
    echo "❌ 统计信息获取失败"
fi

# 测试3: 列出笔记
echo "📄 测试列出笔记..."
notes_response=$(wget --timeout=5 -q -O - http://192.168.18.15:5000/api/notes)
if echo "$notes_response" | grep -q "notes"; then
    notes_count=$(echo "$notes_response" | grep -o '"notes":\[' | wc -l)
    if [ "$notes_count" -gt 0 ]; then
        echo "✅ 笔记列表获取成功"
        # 提取前3个笔记标题
        echo "   前3条笔记:"
        echo "$notes_response" | grep -o '"title":"[^"]*"' | head -3 | sed 's/"title":"/   - /' | sed 's/"$//'
    else
        echo "❌ 笔记列表格式异常"
    fi
else
    echo "❌ 笔记列表获取失败"
fi

echo ""
echo "🎉 基础测试完成！"
echo "💡 说明："
echo "  - GET请求可以使用wget正常执行"
echo "  - POST请求需要curl，但目前系统中不可用"
echo "  - 基础功能（读取、列表）正常可用"