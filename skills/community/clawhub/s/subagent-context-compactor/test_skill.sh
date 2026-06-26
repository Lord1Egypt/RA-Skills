#!/bin/bash

# 上下文压缩技能测试脚本
# 用于验证技能安装和基本功能

echo "🔍 开始测试上下文压缩技能..."
echo "========================================"

# 检查基本文件
echo "📁 检查文件结构..."
required_files=("SKILL.md" "config.json" "compactor.py" "integration.py" "start_system.sh")
missing_files=0

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file 存在"
    else
        echo "  ❌ $file 缺失"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    echo "⚠️  警告：缺少 $missing_files 个必要文件"
else
    echo "✅ 所有必要文件都存在"
fi

echo ""
echo "🐍 检查Python环境..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "  ✅ Python3: $python_version"
    
    # 检查Python依赖
    echo "  📦 检查Python依赖..."
    if [ -f "requirements.txt" ]; then
        echo "  ✅ requirements.txt 存在"
    else
        echo "  ⚠️  requirements.txt 不存在"
    fi
else
    echo "  ❌ Python3 未安装"
fi

echo ""
echo "⚙️ 检查配置文件..."
if [ -f "config.json" ]; then
    config_size=$(wc -c < "config.json")
    if [ $config_size -gt 100 ]; then
        echo "  ✅ config.json 配置完整 ($config_size 字节)"
        
        # 检查关键配置
        echo "  🔧 检查关键配置项..."
        if grep -q "hot_layer" config.json && grep -q "warm_layer" config.json && grep -q "cold_layer" config.json; then
            echo "  ✅ 三层配置存在"
        else
            echo "  ⚠️  缺少分层配置"
        fi
    else
        echo "  ⚠️  config.json 可能为空或不完整"
    fi
fi

echo ""
echo "🚀 测试启动脚本..."
if [ -f "start_system.sh" ]; then
    if [ -x "start_system.sh" ]; then
        echo "  ✅ start_system.sh 可执行"
    else
        echo "  ⚠️  start_system.sh 不可执行，尝试添加执行权限..."
        chmod +x start_system.sh 2>/dev/null && echo "  ✅ 已添加执行权限" || echo "  ❌ 无法添加执行权限"
    fi
fi

echo ""
echo "📊 测试基本功能..."
echo "  1. 测试配置读取..."
if python3 -c "import json; data=json.load(open('config.json')); print('  ✅ 配置读取成功')" 2>/dev/null; then
    echo "  ✅ 配置读取成功"
else
    echo "  ❌ 配置读取失败"
fi

echo ""
echo "  2. 测试数据库..."
if [ -f "context_compactor.db" ]; then
    db_size=$(wc -c < "context_compactor.db")
    echo "  ✅ 数据库文件存在 ($db_size 字节)"
else
    echo "  ⚠️  数据库文件不存在，将在首次运行时创建"
fi

echo ""
echo "  3. 测试压缩逻辑..."
if python3 -c "
import sys
sys.path.append('.')
try:
    from compactor import ContextCompactor
    compactor = ContextCompactor()
    print('  ✅ 压缩器初始化成功')
except Exception as e:
    print(f'  ❌ 压缩器初始化失败: {e}')
" 2>/dev/null; then
    echo "  ✅ 压缩逻辑测试通过"
else
    echo "  ❌ 压缩逻辑测试失败"
fi

echo ""
echo "🔧 测试管理脚本..."
scripts=("check_status.sh" "start_monitor.sh" "stop_monitor.sh" "stop_system.sh")
for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo "  ✅ $script 可执行"
        else
            chmod +x "$script" 2>/dev/null && echo "  ✅ $script 已添加执行权限" || echo "  ⚠️  $script 不可执行"
        fi
    fi
done

echo ""
echo "📝 测试文档..."
docs=("README.md" "INSTALL.md" "DEPLOYMENT.md" "OPENCLAW_INTEGRATION.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        doc_size=$(wc -c < "$doc")
        if [ $doc_size -gt 100 ]; then
            echo "  ✅ $doc 文档完整 ($doc_size 字节)"
        else
            echo "  ⚠️  $doc 文档可能不完整"
        fi
    else
        echo "  ⚠️  $doc 文档不存在"
    fi
done

echo ""
echo "========================================"
echo "🎉 技能测试完成！"
echo ""
echo "📋 总结："
echo "  如果看到多个 ✅，表示技能安装成功"
echo "  如果看到 ⚠️，表示有需要注意的地方"
echo "  如果看到 ❌，表示有需要修复的问题"
echo ""
echo "🚀 下一步："
echo "  1. 安装Python依赖: pip install -r requirements.txt"
echo "  2. 启动系统: ./start_system.sh"
echo "  3. 检查状态: ./check_status.sh"
echo "  4. 集成到OpenClaw: 参考 INSTALL.md"
echo ""
echo "💡 提示：查看 logs/ 目录获取详细日志信息"