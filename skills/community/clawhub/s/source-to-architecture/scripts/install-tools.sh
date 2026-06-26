#!/bin/bash
# 源码到架构技能 - 工具安装脚本

set -e

echo "🚀 安装源码到架构技能所需工具..."

# 检查基础依赖
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ $2 not found. Please install it first."
        exit 1
    fi
}

# 检查 Python
check_dependency python3 "Python 3"

# 检查 Node.js (用于 drawio)
check_dependency npm "Node.js"

# 安装 drawio-desktop
echo "📦 Installing drawio-desktop..."
npm install -g drawio-desktop

# 验证 drawio 安装
if ! command -v drawio &> /dev/null; then
    echo "❌ DrawIO installation failed."
    exit 1
fi

# 安装 ripgrep (用于代码搜索)
echo "🔍 Installing ripgrep..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y ripgrep
elif command -v yum &> /dev/null; then
    sudo yum install -y ripgrep
elif command -v brew &> /dev/null; then
    brew install ripgrep
else
    echo "⚠️  Cannot automatically install ripgrep. Please install it manually."
fi

# 安装 tree (用于目录结构)
echo "🌳 Installing tree..."
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y tree
elif command -v yum &> /dev/null; then
    sudo yum install -y tree
elif command -v brew &> /dev/null; then
    brew install tree
else
    echo "⚠️  Cannot automatically install tree. Please install it manually."
fi

# 安装 Graphviz (可选，用于额外图表支持)
echo "📊 Installing Graphviz (optional)..."
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y graphviz
elif command -v yum &> /dev/null; then
    sudo yum install -y graphviz
elif command -v brew &> /dev/null; then
    brew install graphviz
fi

# 创建 Dockerfile (可选)
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Install drawio-desktop
RUN npm install -g drawio-desktop

# Install ripgrep
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb && \
    dpkg -i ripgrep_13.0.0_amd64.deb && \
    rm ripgrep_13.0.0_amd64.deb

# Set working directory
WORKDIR /workspace

# Copy scripts
COPY scripts/ /workspace/scripts/

# Make scripts executable
RUN chmod +x /workspace/scripts/*.py

CMD ["bash"]
EOF

echo ""
echo "✅ 所有工具安装完成！"
echo ""
echo "💡 使用方法:"
echo "   1. 分析源码: python scripts/source-analyzer.py <项目路径> analysis.json"
echo "   2. 生成图表: python scripts/drawio-generator.py analysis.json output/"
echo "   3. 导出图片: drawio --export --format png output/*.drawio"
echo ""
echo "🐳 Docker 支持: 已生成 Dockerfile，可构建容器化环境"
echo "   docker build -t source-to-architecture ."