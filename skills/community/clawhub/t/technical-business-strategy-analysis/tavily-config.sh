#!/bin/bash
# Business Strategy Analysis - Tavily 配置脚本
# 统一使用 ~/.openclaw/.env 中的 TAVILY_API_KEY

echo "🔄 配置 Business Strategy Analysis 使用统一的 Tavily API Key..."

# 检查 ~/.openclaw/.env 是否存在
if [ ! -f "$HOME/.openclaw/.env" ]; then
    echo "❌ 错误: ~/.openclaw/.env 文件不存在"
    echo "请先配置 Tavily API Key: echo 'TAVILY_API_KEY=your_key' > ~/.openclaw/.env"
    exit 1
fi

# 创建配置目录（如果不存在）
mkdir -p ~/.config/business-strategy-analysis

# 创建域名白名单配置
cat > ~/.config/business-strategy-analysis/tavily_domains.json << EOF
{
  "financial": ["finance.yahoo.com", "sec.gov", "statista.com", "ibisworld.com", "marketwatch.com"],
  "technical": ["mlperf.org", "arxiv.org", "paperswithcode.com", "techcrunch.com"],
  "company": ["crunchbase.com", "linkedin.com", "bloomberg.com", "reuters.com"]
}
EOF

echo "✅ Business Strategy Analysis Tavily 配置完成！"
echo "   - API Key: 从 ~/.openclaw/.env 读取"
echo "   - 域名白名单: ~/.config/business-strategy-analysis/tavily_domains.json"