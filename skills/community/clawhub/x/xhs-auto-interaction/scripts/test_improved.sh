#!/bin/bash

# 测试改进版脚本

echo "=== 测试小红书互动技能改进版 ==="
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 检查脚本是否存在
if [ ! -f "xhs_interaction_improved.sh" ]; then
    echo "❌ 错误：xhs_interaction_improved.sh 不存在"
    echo "请先复制脚本到工作空间："
    echo "cp scripts/xhs_interaction_improved.sh ~/.openclaw/workspace/"
    exit 1
fi

# 检查执行权限
if [ ! -x "xhs_interaction_improved.sh" ]; then
    echo "⚠️ 警告：脚本没有执行权限，正在添加..."
    chmod +x xhs_interaction_improved.sh
fi

# 检查依赖工具
echo "检查依赖工具..."
for cmd in curl jq; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ 错误：缺少必要工具 $cmd"
        exit 1
    else
        echo "✅ $cmd 已安装"
    fi
done

# 检查MCP服务
echo "检查MCP服务..."
MCP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:18060/mcp)
if [ "$MCP_STATUS" = "200" ]; then
    echo "✅ MCP服务正常 (HTTP $MCP_STATUS)"
else
    echo "❌ MCP服务异常 (HTTP $MCP_STATUS)"
    echo "请确保小红书MCP服务已启动："
    echo "检查端口 18060 是否监听"
    exit 1
fi

# 清理旧的测试文件
echo "清理旧的测试文件..."
rm -f xhs_interaction_improved.log
rm -f xhs_interaction_history.txt

# 运行测试（限制为3个内容，快速测试）
echo -e "\n运行快速测试（限制为3个内容）..."
echo "注意：这只是一个快速功能测试，完整功能请运行完整脚本"

# 修改脚本临时限制为3个内容
cp xhs_interaction_improved.sh xhs_interaction_test.sh
sed -i 's/MAX_ATTEMPTS=10/MAX_ATTEMPTS=3/' xhs_interaction_test.sh
chmod +x xhs_interaction_test.sh

# 运行测试
echo -e "\n开始测试..."
./xhs_interaction_test.sh 2>&1 | tee test_output.log

# 检查结果
echo -e "\n=== 测试结果分析 ==="

if [ -f "xhs_interaction_improved.log" ]; then
    echo "✅ 日志文件已创建: xhs_interaction_improved.log"
    
    # 检查关键步骤
    echo -e "\n检查关键步骤完成情况:"
    grep -E "✅|❌|⚠️|📊|执行统计" xhs_interaction_improved.log | head -20
    
    # 检查历史记录
    if [ -f "xhs_interaction_history.txt" ]; then
        echo -e "\n✅ 历史记录文件已创建"
        echo "历史记录内容:"
        cat xhs_interaction_history.txt
    else
        echo "⚠️ 历史记录文件未创建"
    fi
else
    echo "❌ 日志文件未创建，测试可能失败"
fi

# 清理临时文件
rm -f xhs_interaction_test.sh
rm -f test_output.log

echo -e "\n=== 测试完成 ==="
echo "完整功能测试请运行: ./xhs_interaction_improved.sh"
echo "查看日志: tail -f xhs_interaction_improved.log"
echo "查看历史记录: cat xhs_interaction_history.txt"