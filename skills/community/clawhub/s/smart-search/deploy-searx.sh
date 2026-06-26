#!/bin/bash
# SearX 1.1.0 一键部署脚本
# 旧版本无 bot 检测，JSON API 完全可用

set -e

echo "🚀 SearX 1.1.0 一键部署脚本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    echo "   官方文档：https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker 已安装：$(docker --version)"
echo ""

# 检查端口占用
PORT=${1:-8080}
if netstat -tuln 2>/dev/null | grep -q ":$PORT "; then
    echo "⚠️  端口 $PORT 已被占用"
    read -p "是否继续？(y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "❌ 部署已取消"
        exit 1
    fi
fi

# 停止旧容器
echo "📦 检查旧容器..."
if docker ps -a --format '{{.Names}}' | grep -q "^searx$"; then
    echo "⚠️  发现已存在的 searx 容器"
    read -p "是否删除并重新部署？(y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        docker stop searx 2>/dev/null || true
        docker rm searx 2>/dev/null || true
        echo "✅ 旧容器已删除"
    else
        echo "❌ 部署已取消"
        exit 1
    fi
fi

# 创建配置目录
CONFIG_DIR="$(pwd)/searx-config"
mkdir -p "$CONFIG_DIR"
echo ""
echo "📁 配置目录：$CONFIG_DIR"

# 创建 SearX 配置文件
cat > "$CONFIG_DIR/settings.yml" << 'EOF'
# SearX 1.1.0 配置文件
# 适用于 smart-search 技能

general:
  instance_name: "My SearX"
  privacypolicy_url: false
  donation_url: false
  contact_url: false
  enable_metrics: true

search:
  safe_search: 0
  autocomplete: ""
  default_lang: ""
  formats:
    - html
    - json

server:
  secret_key: "searx-local-secret-change-me"
  limiter: false
  public_instance: false
  image_proxy: true
  port: 8080
  bind_address: "0.0.0.0"

ui:
  static_use_hash: true
  default_theme: simple
  default_locale: ""

# 启用常用搜索引擎
engines:
  - name: google
    engine: google
    shortcut: g
    disabled: false
  
  - name: bing
    engine: bing
    shortcut: b
    disabled: false
  
  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg
    disabled: false
  
  - name: wikipedia
    engine: wikipedia
    shortcut: wiki
    disabled: false
  
  - name: arch linux wiki
    engine: archlinux
    shortcut: al
    disabled: false
  
  - name: github
    engine: github
    shortcut: gh
    disabled: false
  
  - name: docker hub
    engine: docker_hub
    shortcut: dh
    disabled: false
  
  - name: npm
    engine: npm
    shortcut: npm
    disabled: false
  
  - name: pypi
    engine: pypi
    shortcut: pypi
    disabled: false
  
  - name: news
    engine: google_news
    shortcut: news
    disabled: false
  
  - name: images
    engine: google_images
    shortcut: img
    disabled: false
  
  - name: videos
    engine: google_videos
    shortcut: vid
    disabled: false
EOF

echo "✅ 配置文件已创建：$CONFIG_DIR/settings.yml"

# 启动容器
echo ""
echo "🐳 启动 SearX 容器..."
docker run -d \
  --name searx \
  -p "$PORT":8080 \
  -v "$CONFIG_DIR:/etc/searx:rw" \
  -e SEARX_SECRET="searx-local-secret-$(date +%s)" \
  --restart unless-stopped \
  searx/searx:1.1.0-69-75b859d2

# 等待启动
echo "⏳ 等待 SearX 启动..."
sleep 10

# 检查状态
if docker ps --format '{{.Names}}' | grep -q "^searx$"; then
    echo ""
    echo "🎉 部署成功！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 访问地址：http://localhost:$PORT"
    echo "🔧 配置目录：$CONFIG_DIR"
    echo "📊 容器状态：$(docker ps --filter name=searx --format '{{.Status}}')"
    echo ""
    echo "🧪 测试 API："
    echo "   curl \"http://localhost:$PORT/search?q=test&format=json\""
    echo ""
    echo "⚙️  配置 smart-search："
    echo "   编辑 ~/.openclaw/.env"
    echo "   添加：SEARXNG_URL=http://localhost:$PORT"
    echo ""
    echo "📚 管理命令："
    echo "   查看日志：docker logs searx --tail 20"
    echo "   重启：docker restart searx"
    echo "   停止：docker stop searx"
    echo "   删除：docker rm -f searx"
    echo ""
else
    echo ""
    echo "❌ 容器启动失败，请查看日志："
    echo "   docker logs searx"
    exit 1
fi
