#!/bin/bash
# QWeather China Skill 安装脚本
# 版本: 1.2.2
# 用途: 安装必要的依赖并验证配置

set -e

echo "🔧 QWeather China Skill 安装脚本"
echo "=================================="
echo ""
echo "此脚本将执行以下操作:"
echo "  1. 检查 Python3 环境"
echo "  2. 安装必要的 Python 依赖 (pyjwt, cryptography, requests)"
echo "  3. 创建配置目录 (~/.config/qweather)"
echo "  4. 创建缓存目录 (~/.cache/qweather)"
echo "  5. 验证配置"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python3，请先安装 Python3"
    exit 1
fi

echo "✅ Python3 已安装"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 需要 pip3，请先安装 pip"
    exit 1
fi

echo "✅ pip3 已安装"

# 检查必要文件
REQUIRED_FILES=("qweather.py" "SKILL.md" "config.json" "skill.yaml")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件: $file"
        exit 1
    fi
done

echo "✅ 所有必要文件都存在"

# 安装Python依赖
echo ""
echo "📦 安装Python依赖..."
echo "   即将安装: pyjwt>=2.0.0, cryptography>=3.0, requests>=2.25"
pip3 install pyjwt>=2.0.0 cryptography>=3.0 requests>=2.25 --quiet

if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装成功"
else
    echo "⚠️  Python依赖安装可能有问题，请手动检查: pip3 install pyjwt cryptography requests"
fi

# 创建配置目录
echo ""
echo "📁 创建配置目录..."
CONFIG_DIR="$HOME/.config/qweather"
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
    chmod 700 "$CONFIG_DIR"
    echo "✅ 创建配置目录: $CONFIG_DIR (权限: 700)"
else
    echo "✅ 配置目录已存在: $CONFIG_DIR"
fi

# 创建缓存目录
CACHE_DIR="$HOME/.cache/qweather"
if [ ! -d "$CACHE_DIR" ]; then
    mkdir -p "$CACHE_DIR"
    chmod 755 "$CACHE_DIR"
    echo "✅ 创建缓存目录: $CACHE_DIR"
else
    echo "✅ 缓存目录已存在: $CACHE_DIR"
fi

# 检查私钥文件
echo ""
echo "🔑 检查私钥配置..."
PRIVATE_KEY="$HOME/.config/qweather/private.pem"
if [ ! -f "$PRIVATE_KEY" ]; then
    echo "⚠️  未找到私钥文件: $PRIVATE_KEY"
    echo ""
    echo "请完成以下步骤:"
    echo "  1. 访问 https://dev.qweather.com/ 注册并创建项目"
    echo "  2. 在控制台下载 JWT 认证私钥"
    echo "  3. 将私钥复制到: $PRIVATE_KEY"
    echo "  4. 设置权限: chmod 600 $PRIVATE_KEY"
    echo ""
    echo "或者通过环境变量配置:"
    echo "  export QWEATHER_PRIVATE_KEY_PATH=/path/to/your/private.pem"
else
    echo "✅ 私钥文件存在: $PRIVATE_KEY"
    # 检查权限
    PERM=$(stat -c %a "$PRIVATE_KEY" 2>/dev/null || stat -f %Lp "$PRIVATE_KEY" 2>/dev/null)
    if [ "$PERM" != "600" ]; then
        echo "⚠️  私钥文件权限不是 600，建议执行: chmod 600 $PRIVATE_KEY"
    else
        echo "✅ 私钥文件权限正确 (600)"
    fi
fi

# 检查环境变量
echo ""
echo "🔧 检查环境变量配置..."
MISSING_ENV=0

if [ -z "$QWEATHER_API_HOST" ]; then
    echo "  ⚠️  QWEATHER_API_HOST 未设置"
    MISSING_ENV=$((MISSING_ENV + 1))
else
    echo "  ✅ QWEATHER_API_HOST: $QWEATHER_API_HOST"
fi

if [ -z "$QWEATHER_PROJECT_ID" ]; then
    echo "  ⚠️  QWEATHER_PROJECT_ID 未设置"
    MISSING_ENV=$((MISSING_ENV + 1))
else
    echo "  ✅ QWEATHER_PROJECT_ID: 已设置"
fi

if [ -z "$QWEATHER_CREDENTIALS_ID" ]; then
    echo "  ⚠️  QWEATHER_CREDENTIALS_ID 未设置"
    MISSING_ENV=$((MISSING_ENV + 1))
else
    echo "  ✅ QWEATHER_CREDENTIALS_ID: 已设置"
fi

if [ $MISSING_ENV -gt 0 ]; then
    echo ""
    echo "⚠️  缺少 $MISSING_ENV 个必需环境变量"
    echo "请设置以下环境变量:"
    echo "  export QWEATHER_API_HOST=your-api-host.re.qweatherapi.com"
    echo "  export QWEATHER_PROJECT_ID=your-project-id"
    echo "  export QWEATHER_CREDENTIALS_ID=your-credentials-id"
    echo "  export QWEATHER_PRIVATE_KEY_PATH=~/.config/qweather/private.pem"
else
    echo "✅ 所有必需环境变量已设置"
fi

# 设置执行权限
chmod +x qweather.py 2>/dev/null || true

echo ""
echo "=================================="
echo "🎉 安装完成！"
echo ""

if [ $MISSING_ENV -gt 0 ] || [ ! -f "$PRIVATE_KEY" ]; then
    echo "⚠️  配置尚未完成，请按上述提示完成配置"
    echo ""
else
    # 测试API连接
    echo "🔗 测试API连接..."
    python3 -c "
import sys
try:
    from qweather import QWeatherClient
    client = QWeatherClient()
    weather = client.get_weather_now('beijing')
    print(f'✅ API连接成功！北京当前温度: {weather.temp}°C')
except Exception as e:
    print(f'❌ API连接测试失败: {e}')
    sys.exit(1)
"
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 配置验证通过，可以正常使用！"
    else
        echo ""
        echo "⚠️  API连接测试失败，请检查配置"
    fi
fi

echo ""
echo "使用说明:"
echo "  实时天气: python qweather.py now --city beijing"
echo "  天气预报: python qweather.py forecast --city shanghai --days 3"
echo "  生活指数: python qweather.py indices --city guangzhou"
echo "  完整报告: python qweather.py full --city hangzhou"
echo ""
echo "在OpenClaw中使用:"
echo "  直接发送: '北京天气'、'上海未来3天预报' 等自然语言查询"
echo ""
echo "查看帮助: python qweather.py --help"
echo ""
