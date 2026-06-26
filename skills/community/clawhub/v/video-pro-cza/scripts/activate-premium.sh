#!/bin/bash
# Video Pro - 高级版激活脚本

set -e

CONFIG_DIR="$HOME/.video-pro"
LICENSE_FILE="$CONFIG_DIR/license.key"
CONFIG_FILE="$CONFIG_DIR/config.json"

# 显示欢迎信息
echo "🎬 Video Pro 高级版激活"
echo "========================"
echo ""

# 检查是否已激活
if [ -f "$LICENSE_FILE" ]; then
    echo "当前许可证信息:"
    echo "----------------"
    cat "$LICENSE_FILE"
    echo ""
    echo "许可证已激活，无需重复激活"
    exit 0
fi

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 显示授权选项
echo "请选择授权级别:"
echo "1. 个人版 - $9.99/月"
echo "   - 每月100个视频"
echo "   - 5个高级模板"
echo "   - 基础支持"
echo ""
echo "2. 专业版 - $29.99/月"
echo "   - 每月500个视频"
echo "   - 所有模板"
echo "   - 优先支持"
echo "   - API访问"
echo ""
echo "3. 企业版 - $99.99/月"
echo "   - 无限视频生成"
echo "   - 自定义模板开发"
echo "   - 专属技术支持"
echo "   - SLA保证"
echo ""
echo "4. 试用版 - 7天免费试用"
echo "   - 所有高级功能"
echo "   - 最多50个视频"
echo "   - 7天后需要购买"
echo ""

# 获取用户选择
read -p "请选择 (1-4): " choice

case $choice in
    1)
        license_type="personal"
        price="$9.99/月"
        features="100视频/月, 5模板, 基础支持"
        ;;
    2)
        license_type="professional"
        price="$29.99/月"
        features="500视频/月, 所有模板, 优先支持, API访问"
        ;;
    3)
        license_type="enterprise"
        price="$99.99/月"
        features="无限视频, 自定义模板, 专属支持, SLA保证"
        ;;
    4)
        license_type="trial"
        price="免费试用"
        features="所有高级功能, 最多50视频, 7天试用"
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "您选择了: $license_type 版"
echo "价格: $price"
echo "功能: $features"
echo ""

# 获取许可证密钥
if [ "$license_type" = "trial" ]; then
    # 生成试用许可证
    license_key="TRIAL-$(uuidgen | tr '[:lower:]' '[:upper:]' | cut -d'-' -f1)"
    expiry_date=$(date -v+7d '+%Y-%m-%d')
    
    echo "生成试用许可证..."
    echo "许可证密钥: $license_key"
    echo "有效期至: $expiry_date"
else
    echo "请访问以下链接购买许可证:"
    echo "https://clawhub.com/@cza999/video-pro"
    echo ""
    read -p "请输入您的许可证密钥: " license_key
    
    if [ -z "$license_key" ]; then
        echo "错误: 许可证密钥不能为空"
        exit 1
    fi
    
    # 这里可以添加许可证验证逻辑
    echo "验证许可证..."
    
    # 模拟验证（实际应该调用API）
    if [[ "$license_key" =~ ^VIDEOPRO- ]]; then
        echo "✅ 许可证验证通过"
        expiry_date="2099-12-31"  # 永久
    else
        echo "❌ 无效的许可证格式"
        echo "许可证密钥应以 VIDEOPRO- 开头"
        exit 1
    fi
fi

# 保存许可证信息
cat > "$LICENSE_FILE" << EOF
{
  "license_type": "$license_type",
  "license_key": "$license_key",
  "price": "$price",
  "features": "$features",
  "activated_at": "$(date -Iseconds)",
  "expires_at": "$expiry_date",
  "customer_id": "$USER",
  "machine_id": "$(hostname)"
}
EOF

# 更新配置文件
if [ -f "$CONFIG_FILE" ]; then
    jq ".license = \"$license_type\"" "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
else
    echo "{\"license\": \"$license_type\", \"activated\": true}" > "$CONFIG_FILE"
fi

echo ""
echo "✅ 高级版激活成功!"
echo ""
echo "激活信息:"
echo "---------"
cat "$LICENSE_FILE"
echo ""
echo "您现在可以使用以下高级功能:"
echo "1. 批量视频生成: ./batch-generate.sh scripts.txt"
echo "2. 高级模板: --template marketing/education/social-media"
echo "3. 自定义语音: --voice nova/echo/shimmer"
echo "4. API访问: 查看文档获取API密钥"
echo ""
echo "感谢选择 Video Pro! 🎬"

# 记录激活日志
echo "$(date '+%Y-%m-%d %H:%M:%S') | $license_type | $license_key | $USER@$(hostname)" >> "$CONFIG_DIR/activation.log"