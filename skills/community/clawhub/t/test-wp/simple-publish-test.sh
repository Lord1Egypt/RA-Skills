#!/bin/bash

# 简单WordPress发布测试
echo "📝 WordPress文章发布测试"
echo "========================"
echo "站点: https://openow.ai"
echo "时间: $(date)"
echo ""

# 读取测试文章内容
ARTICLE_FILE="posts/test-article-2026-04-12.md"
echo "📄 读取文章: $ARTICLE_FILE"

# 提取文章内容
TITLE="OpenClaw WordPress自动发布测试文章"
CONTENT=$(cat << 'EOF'
<h1>OpenClaw WordPress自动发布测试</h1>

<p>这是一个通过 <strong>OpenClaw WordPress自动发布技能</strong> 发布的测试文章。</p>

<h2>测试目的</h2>

<ol>
<li><strong>验证发布功能</strong> - 测试WordPress REST API连接</li>
<li><strong>检查格式转换</strong> - Markdown到HTML的转换效果</li>
<li><strong>测试元数据</strong> - 分类、标签、作者等元数据</li>
<li><strong>验证链接生成</strong> - 查看文章发布后的URL</li>
</ol>

<h2>当前时间</h2>

<ul>
<li><strong>发布日期</strong>: 2026年4月12日</li>
<li><strong>发布时间</strong>: 08:15 AM (欧洲/伦敦时区)</li>
<li><strong>发布方式</strong>: OpenClaw自动发布技能</li>
</ul>

<h2>预期结果</h2>

<p>如果一切正常，这篇文章应该：</p>

<ol>
<li>✅ 成功发布到WordPress</li>
<li>✅ 保持所有格式</li>
<li>✅ 正确显示分类和标签</li>
<li>✅ 生成可访问的URL</li>
</ol>

<hr />

<p><strong>测试说明</strong>: 这是一个自动化测试文章，用于验证OpenClaw的WordPress发布功能。如果看到这篇文章，说明自动发布功能正常工作！ 🎉</p>

<p><strong>测试人员</strong>: Paco Guo<br />
<strong>测试工具</strong>: OpenClaw WordPress Auto-Publish Skill<br />
<strong>测试时间</strong>: 2026年4月12日</p>
EOF
)

echo "📤 准备发布文章..."
echo "标题: $TITLE"

# 创建JSON数据
JSON_DATA=$(cat << EOF
{
  "title": "$TITLE",
  "content": "$CONTENT",
  "status": "draft",
  "categories": [1],
  "tags": [5, 6],
  "excerpt": "这是一个通过OpenClaw技能自动发布的测试文章，用于验证WordPress发布功能"
}
EOF
)

echo "🔐 使用Basic Auth发布文章..."
echo "用户名: inkmind"
echo ""

# 发布文章
RESPONSE=$(curl -s -w "\nHTTP状态码: %{http_code}" \
  -u "inkmind:QLHH6))acWR&At*PE4uBv5TM" \
  -X POST "https://openow.ai/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA")

# 提取HTTP状态码
HTTP_CODE=$(echo "$RESPONSE" | tail -1 | grep -o '[0-9]*$')
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

echo ""
echo "📊 发布结果:"
echo "HTTP状态码: $HTTP_CODE"

if [ "$HTTP_CODE" -eq 201 ] || [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ 文章发布成功!"
    
    # 提取文章ID和链接
    POST_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
    POST_LINK=$(echo "$RESPONSE_BODY" | grep -o '"link":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    echo "📝 文章ID: $POST_ID"
    echo "🔗 文章链接: $POST_LINK"
    
    # 保存结果
    echo "文章ID: $POST_ID" > publish-result.txt
    echo "文章链接: $POST_LINK" >> publish-result.txt
    echo "发布时间: $(date)" >> publish-result.txt
    
    echo ""
    echo "📁 结果已保存到: publish-result.txt"
else
    echo "❌ 文章发布失败"
    echo "错误响应: $RESPONSE_BODY"
fi

echo ""
echo "🎯 测试完成"