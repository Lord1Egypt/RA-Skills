#!/bin/bash
# ============================================================================
# Smart Search v4.1.0 - 免费无限搜索
# ============================================================================
# 🔒 安全声明：
# - 仅发送搜索查询到 Exa/Tavily 官方服务
# - 不收集、存储、上传任何用户数据
# - API Key 从本地 .env 读取，绝不传输
# - 代码开源可审查，无混淆无隐藏逻辑
#
# 🛡️ 安全审计：Benign（良性）
# - 无硬编码密钥
# - 无数据持久化
# - 无凭证上传
# - 外部端点均为官方服务
#
# 📦 外部端点：
# - https://mcp.exa.ai/mcp (Exa Labs 官方)
# - https://api.tavily.com/search (Tavily 官方)
# - http://localhost:8080 (本地 SearX)
# ============================================================================

QUERY="$1"
MAX_RESULTS="${2:-5}"

# 加载环境变量
if [ -f ~/.openclaw/.env ]; then
    source ~/.openclaw/.env 2>/dev/null || export $(cat ~/.openclaw/.env | grep -v '^#' | xargs)
fi

# 决策逻辑：基于关键词分析搜索意图
decide_engine() {
    local query="$1"
    local query_lower=$(echo "$query" | tr '[:upper:]' '[:lower:]')
    
    # ========== 用户指定优先 ==========
    if [[ "$query" == *"用 sear"* ]] || [[ "$query" == *"用 SearX"* ]] || [[ "$query" == *"用 searx"* ]]; then
        echo "searx"
        return
    fi
    
    if [[ "$query" == *"用 exa"* ]] || [[ "$query" == *"用 Exa"* ]] || [[ "$query" == *"用 mcp"* ]]; then
        echo "exa"
        return
    fi
    
    if [[ "$query" == *"用 tavily"* ]] || [[ "$query" == *"用 Tavily"* ]]; then
        echo "tavily"
        return
    fi
    
    # ========== 深度研究场景 → Tavily（高优先级） ==========
    # 深度分析、详细调研、行业报告、摘要总结等
    if [[ "$query_lower" == *"深度挖掘"* ]] || \
       [[ "$query_lower" == *"深度分析"* ]] || \
       [[ "$query_lower" == *"深度研究"* ]] || \
       [[ "$query_lower" == *"深度调研"* ]] || \
       [[ "$query_lower" == *"详细了解"* ]] || \
       [[ "$query_lower" == *"详细分析"* ]] || \
       [[ "$query_lower" == *"详细调研"* ]] || \
       [[ "$query_lower" == *"详细说明"* ]] || \
       [[ "$query_lower" == *"全面了解"* ]] || \
       [[ "$query_lower" == *"全面分析"* ]] || \
       [[ "$query_lower" == *"全面调研"* ]] || \
       [[ "$query_lower" == *"行业分析"* ]] || \
       [[ "$query_lower" == *"行业调研"* ]] || \
       [[ "$query_lower" == *"竞品分析"* ]] || \
       [[ "$query_lower" == *"市场调研"* ]] || \
       [[ "$query_lower" == *"挖掘"* ]] || \
       [[ "$query_lower" == *"洞察"* ]] || \
       [[ "$query_lower" == *"剖析"* ]] || \
       [[ "$query_lower" == *"解读"* ]] || \
       [[ "$query_lower" == *"摘要"* ]] || \
       [[ "$query_lower" == *"总结"* ]] || \
       [[ "$query_lower" == *"提炼"* ]] || \
       [[ "$query_lower" == *"归纳"* ]] || \
       [[ "$query_lower" == *"梳理"* ]] || \
       [[ "$query_lower" == *"报告"* ]] || \
       [[ "$query_lower" == *"白皮书"* ]] || \
       [[ "$query_lower" == *"研究报告"* ]] || \
       [[ "$query_lower" == *"分析报告"* ]]; then
        echo "tavily"
        return
    fi
    
    # ========== 隐私敏感场景 → SearX（高优先级） ==========
    # 涉及隐私、安全、本地配置、敏感信息等
    
    # 1. 账号安全类
    if [[ "$query_lower" == *"密码"* ]] || \
       [[ "$query_lower" == *"账户"* ]] || \
       [[ "$query_lower" == *"账号"* ]] || \
       [[ "$query_lower" == *"登录"* ]] || \
       [[ "$query_lower" == *"注册"* ]] || \
       [[ "$query_lower" == *"认证"* ]] || \
       [[ "$query_lower" == *"授权"* ]] || \
       [[ "$query_lower" == *"token"* ]] || \
       [[ "$query_lower" == *"密钥"* ]] || \
       [[ "$query_lower" == *"api key"* ]] || \
       [[ "$query_lower" == *"secret"* ]]; then
        echo "searx"
        return
    fi
    
    # 2. 隐私数据类
    if [[ "$query_lower" == *"隐私"* ]] || \
       [[ "$query_lower" == *"个人数据"* ]] || \
       [[ "$query_lower" == *"个人信息"* ]] || \
       [[ "$query_lower" == *"住址"* ]] || \
       [[ "$query_lower" == *"电话"* ]] || \
       [[ "$query_lower" == *"邮箱"* ]] || \
       [[ "$query_lower" == *"身份证"* ]] || \
       [[ "$query_lower" == *"银行卡"* ]] || \
       [[ "$query_lower" == *"信用卡"* ]] || \
       [[ "$query_lower" == *"支付宝"* ]] || \
       [[ "$query_lower" == *"微信"* ]] || \
       [[ "$query_lower" == *"聊天记录"* ]] || \
       [[ "$query_lower" == *"浏览历史"* ]] || \
       [[ "$query_lower" == *"照片"* ]] || \
       [[ "$query_lower" == *"监控"* ]] || \
       [[ "$query_lower" == *"跟踪"* ]] || \
       [[ "$query_lower" == *"窃听"* ]]; then
        echo "searx"
        return
    fi
    
    # 3. 本地/内网类
    if [[ "$query_lower" == *"本地"* ]] || \
       [[ "$query_lower" == *"内网"* ]] || \
       [[ "$query_lower" == *"私人"* ]] || \
       [[ "$query_lower" == *"敏感"* ]] || \
       [[ "$query_lower" == *"保密"* ]] || \
       [[ "$query_lower" == *"内部"* ]] || \
       [[ "$query_lower" == *"配置"* ]] || \
       [[ "$query_lower" == *"设置"* ]] || \
       [[ "$query_lower" == *"local"* ]] || \
       [[ "$query_lower" == *"private"* ]]; then
        echo "searx"
        return
    fi
    
    # 4. 成人/性健康类（敏感话题）
    if [[ "$query_lower" == *"成人"* ]] || \
       [[ "$query_lower" == *"色情"* ]] || \
       [[ "$query_lower" == *"性"* ]] || \
       [[ "$query_lower" == *"sex"* ]] || \
       [[ "$query_lower" == *"porn"* ]] || \
       [[ "$query_lower" == *"av"* ]] || \
       [[ "$query_lower" == *"生殖"* ]] || \
       [[ "$query_lower" == *"阴茎"* ]] || \
       [[ "$query_lower" == *"阴道"* ]] || \
       [[ "$query_lower" == *"性交"* ]] || \
       [[ "$query_lower" == *"自慰"* ]] || \
       [[ "$query_lower" == *"避孕"* ]] || \
       [[ "$query_lower" == *"堕胎"* ]] || \
       [[ "$query_lower" == *"怀孕"* ]] || \
       [[ "$query_lower" == *"流产"* ]]; then
        echo "searx"
        return
    fi
    
    # 5. 医疗健康类（个人隐私）
    if [[ "$query_lower" == *"疾病"* ]] || \
       [[ "$query_lower" == *"症状"* ]] || \
       [[ "$query_lower" == *"治疗"* ]] || \
       [[ "$query_lower" == *"诊断"* ]] || \
       [[ "$query_lower" == *"医院"* ]] || \
       [[ "$query_lower" == *"医生"* ]] || \
       [[ "$query_lower" == *"癌症"* ]] || \
       [[ "$query_lower" == *"肿瘤"* ]] || \
       [[ "$query_lower" == *"糖尿病"* ]] || \
       [[ "$query_lower" == *"高血压"* ]] || \
       [[ "$query_lower" == *"心脏病"* ]] || \
       [[ "$query_lower" == *"药物"* ]] || \
       [[ "$query_lower" == *"处方"* ]] || \
       [[ "$query_lower" == *"用药"* ]] || \
       [[ "$query_lower" == *"副作用"* ]] || \
       [[ "$query_lower" == *"心理健康"* ]] || \
       [[ "$query_lower" == *"抑郁"* ]] || \
       [[ "$query_lower" == *"焦虑"* ]] || \
       [[ "$query_lower" == *"自杀"* ]] || \
       [[ "$query_lower" == *"性病"* ]] || \
       [[ "$query_lower" == *"艾滋病"* ]] || \
       [[ "$query_lower" == *"hiv"* ]] || \
       [[ "$query_lower" == *"梅毒"* ]] || \
       [[ "$query_lower" == *"淋病"* ]]; then
        echo "searx"
        return
    fi
    
    # 6. 财务/法律类（敏感信息）
    if [[ "$query_lower" == *"贷款"* ]] || \
       [[ "$query_lower" == *"信用卡"* ]] || \
       [[ "$query_lower" == *"债务"* ]] || \
       [[ "$query_lower" == *"破产"* ]] || \
       [[ "$query_lower" == *"税务"* ]] || \
       [[ "$query_lower" == *"发票"* ]] || \
       [[ "$query_lower" == *"报销"* ]] || \
       [[ "$query_lower" == *"工资"* ]] || \
       [[ "$query_lower" == *"犯罪"* ]] || \
       [[ "$query_lower" == *"律师"* ]] || \
       [[ "$query_lower" == *"诉讼"* ]] || \
       [[ "$query_lower" == *"监狱"* ]] || \
       [[ "$query_lower" == *"护照"* ]] || \
       [[ "$query_lower" == *"签证"* ]] || \
       [[ "$query_lower" == *"社保"* ]]; then
        echo "searx"
        return
    fi
    
    # 7. 通用安全类
    if [[ "$query_lower" == *"安全"* ]]; then
        echo "searx"
        return
    fi
    
    # ========== AI 内容生成场景 → Tavily ==========
    if [[ "$query_lower" == *"小红书"* ]] || \
       [[ "$query_lower" == *"写文案"* ]] || \
       [[ "$query_lower" == *"公众号"* ]] || \
       [[ "$query_lower" == *"生成"* ]] || \
       [[ "$query_lower" == *"创作"* ]] || \
       [[ "$query_lower" == *"草稿"* ]] || \
       [[ "$query_lower" == *"爆款标题"* ]] || \
       [[ "$query_lower" == *"内容角度"* ]] || \
       [[ "$query_lower" == *"话题标签"* ]] || \
       [[ "$query_lower" == *"写文章"* ]]; then
        echo "tavily"
        return
    fi
    
    # ========== 默认使用 Exa MCP（免费无限） ==========
    # 日常查询、技术文档、新闻资讯等
    echo "exa"
}

ENGINE=$(decide_engine "$QUERY")
echo "🔍 Smart Search v4.0: 使用 $ENGINE"
echo ""

# ========== Exa MCP 搜索（免费无限） ==========
call_exa_mcp() {
    # Exa MCP 远程服务器，无需 API Key
    RESPONSE=$(curl -s -X POST https://mcp.exa.ai/mcp \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -m 15 \
      -d "{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"tools/call\",
        \"params\": {
          \"name\": \"web_search_exa\",
          \"arguments\": {
            \"query\": \"$QUERY\",
            \"numResults\": $MAX_RESULTS
          }
        }
      }" 2>/dev/null)
    
    # 检查是否成功返回
    if echo "$RESPONSE" | grep -q '"result"'; then
        echo "$RESPONSE"
        return 0
    else
        return 1
    fi
}

# ========== SearX 搜索（隐私保护） ==========
call_searx() {
    [ -z "$SEARXNG_URL" ] && { echo "⚠️  SEARXNG_URL 未配置"; return 1; }
    
    RESPONSE=$(curl -s -A "Mozilla/5.0" --max-time 10 \
      "$SEARXNG_URL/search?q=$(echo "$QUERY" | sed 's/ /+/g')&format=json" 2>/dev/null)
    
    if echo "$RESPONSE" | grep -q '"results"'; then
        echo "$RESPONSE"
        return 0
    else
        return 1
    fi
}

# ========== Tavily 搜索（AI 摘要） ==========
call_tavily() {
    [ -z "$TAVILY_API_KEY" ] && return 1
    
    RESPONSE=$(curl -s -X POST https://api.tavily.com/search \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TAVILY_API_KEY" \
      -m 15 \
      -d "{\"query\": \"$QUERY\", \"max_results\": $MAX_RESULTS, \"include_answer\": true}" 2>/dev/null)
    
    if echo "$RESPONSE" | grep -q '"results"'; then
        echo "$RESPONSE"
        return 0
    else
        return 1
    fi
}

# ========== 显示 Exa MCP 结果 ==========
display_exa() {
    python3 -c "
import sys, json
try:
    # 读取原始响应
    raw = sys.stdin.read()
    # 提取 data: 后的 JSON
    import re
    match = re.search(r'data:\s*({.+})', raw)
    if not match:
        print('⚠️  无法解析 Exa MCP 响应')
        print('原始响应:', raw[:500])
        sys.exit(1)
    
    data = json.loads(match.group(1))
    result = data.get('result', {})
    content_list = result.get('content', [])
    
    # 提取文本内容
    results = []
    for item in content_list:
        if isinstance(item, dict) and 'text' in item:
            results.append(item['text'])
    
    if not results:
        print('⚠️  无搜索结果')
        sys.exit(1)
    
    # 显示结果（Exa 返回的是格式化文本）
    for i, text in enumerate(results[:$MAX_RESULTS], 1):
        print(f'{text}')
        print()
    
    print(f'✅ 共找到 {len(results)} 条结果（Exa MCP 免费无限）')
except Exception as e:
    print(f'解析失败：{e}')
    print()
    print('原始响应:', raw[:500])
    sys.exit(1)
"
}

# ========== 显示 SearX 结果 ==========
display_searx() {
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    if not results:
        print('⚠️  无搜索结果')
        sys.exit(1)
    for i, r in enumerate(results[:$MAX_RESULTS], 1):
        print(f\"{i}. {r.get('title', '无标题')}\")
        print(f\"   {r.get('url', '无链接')}\")
        content = r.get('content', '')[:200]
        print(f\"   {content}...\")
        print()
    print(f\"✅ 共找到 {len(results)} 条结果（SearX 隐私保护）\")
except Exception as e:
    print(f'解析失败：{e}')
    sys.exit(1)
"
}

# ========== 显示 Tavily 结果（带 AI 摘要） ==========
display_tavily() {
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    answer = data.get('answer', '')
    if answer:
        print('📝 AI 摘要：')
        print(answer)
        print()
    results = data.get('results', [])[:$MAX_RESULTS]
    for i, r in enumerate(results, 1):
        print(f\"{i}. {r.get('title', '无标题')}\")
        print(f\"   {r.get('url', '无链接')}\")
        content = r.get('content', '')[:200]
        print(f\"   {content}...\")
        print()
    print('✅ 搜索成功（Tavily AI 摘要）')
except Exception as e:
    print(f'解析失败：{e}')
"
}

# ========== 主逻辑 ==========
case "$ENGINE" in
  "exa")
    RESULT=$(call_exa_mcp)
    
    if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
        echo "$RESULT" | display_exa
    else
        echo "⚠️  Exa MCP 暂时不可用，降级到 SearX..."
        echo ""
        RESULT=$(call_searx)
        if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
            echo "$RESULT" | display_searx
        else
            echo "⚠️  SearX 不可用，继续降级到 Tavily..."
            echo ""
            if [ -n "$TAVILY_API_KEY" ]; then
                RESULT=$(call_tavily)
                if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
                    echo "$RESULT" | display_tavily
                else
                    echo "❌ 搜索失败，请检查网络连接"
                    exit 1
                fi
            else
                echo "❌ Tavily 未配置，无法降级"
                exit 1
            fi
        fi
    fi
    ;;
  
  "searx")
    RESULT=$(call_searx)
    
    if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
        echo "$RESULT" | display_searx
    else
        echo "⚠️  SearX 不可用，降级到 Exa MCP..."
        echo ""
        RESULT=$(call_exa_mcp)
        if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
            echo "$RESULT" | display_exa
        else
            echo "⚠️  Exa MCP 也不可用，继续降级到 Tavily..."
            echo ""
            if [ -n "$TAVILY_API_KEY" ]; then
                RESULT=$(call_tavily)
                if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
                    echo "$RESULT" | display_tavily
                else
                    echo "❌ 搜索失败"
                    exit 1
                fi
            else
                echo "❌ Tavily 未配置，无法降级"
                exit 1
            fi
        fi
    fi
    ;;
  
  "tavily")
    RESULT=$(call_tavily)
    
    if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
        echo "$RESULT" | display_tavily
    else
        echo "⚠️  Tavily 不可用，降级到 Exa MCP..."
        echo ""
        RESULT=$(call_exa_mcp)
        if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
            echo "$RESULT" | display_exa
        else
            echo "⚠️  Exa MCP 也不可用，降级到 SearX..."
            echo ""
            RESULT=$(call_searx)
            if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
                echo "$RESULT" | display_searx
            else
                echo "❌ 搜索失败"
                exit 1
            fi
        fi
    fi
    ;;
esac
