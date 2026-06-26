#!/bin/bash

echo "🚀 开始全量任务巡检..."

qslazy task list | grep '^  - ' | sed 's/^  - //' | while read -r task_name; do
    echo ""
    echo "================================================"
    echo "🔍 正在检查: '$task_name'"
    
    # 执行查询
    qslazy task status "$task_name" 
    
    # 执行完后，强制休息 3 秒，防止 QAS 后端过载
    echo "------------------------------------------------"
    echo "💤 休息 3 秒，等待后端缓冲..."
    sleep 10
done

echo ""
echo "✅ 全部检查完成。"
