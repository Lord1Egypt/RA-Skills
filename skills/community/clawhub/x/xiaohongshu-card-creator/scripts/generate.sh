#!/bin/bash

# xiaohongshu-card-creator
# 将小红书文案转换为HTML图文卡片网页

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 加载 .env 文件中的环境变量
load_env_file() {
    local env_file="$SKILL_DIR/.env"
    if [ -f "$env_file" ]; then
        while IFS='=' read -r key value || [[ -n "$key" ]]; do
            # 跳过注释和空行
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            # 去除 key 的前后空格
            key=$(echo "$key" | xargs)
            # 如果环境变量未设置，则从文件加载
            if [ -z "${!key}" ]; then
                export "$key=$value"
            fi
        done < "$env_file"
    fi
}

# 加载环境变量
load_env_file

# 显示帮助
show_help() {
    echo -e "${BLUE}xiaohongshu-card-creator${NC}"
    echo ""
    echo "用法:"
    echo "  $0 <input-markdown-file> [options]"
    echo ""
    echo "参数:"
    echo "  input-markdown-file   小红书文案Markdown文件路径"
    echo ""
    echo "选项:"
    echo "  -n, --num-cards NUM   指定卡片数量（默认: 7, 范围: 1-20）"
    echo "  -o, --output DIR      输出目录（默认: ./output）"
    echo "  --concepts            使用7大AI概念专用模板"
    echo "  --llm                 使用LLM智能生成卡片（需配置API Key）"
    echo "  -h, --help            显示帮助"
    echo ""
    echo "环境变量:"
    echo "  LLM_API_KEY           LLM API密钥"
    echo "  LLM_PROVIDER          LLM提供商: openai/claude (默认: openai)"
    echo "  LLM_MODEL             模型名称 (默认: gpt-4o-mini)"
    echo ""
    echo "示例:"
    echo "  $0 article.md              # 默认生成7张卡片"
    echo "  $0 article.md --concepts   # 使用AI概念模板"
    echo "  $0 article.md --llm        # 使用LLM智能生成"
    echo "  $0 article.md -n 5         # 生成5张卡片"
}

# 默认参数
INPUT_FILE=""
NUM_CARDS=7
OUTPUT_DIR="./output"
USE_CONCEPTS=false
USE_LLM=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--num-cards)
            NUM_CARDS="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --concepts)
            USE_CONCEPTS=true
            shift
            ;;
        --llm)
            USE_LLM=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo -e "${YELLOW}错误: 未知选项 $1${NC}"
            show_help
            exit 1
            ;;
        *)
            if [ -z "$INPUT_FILE" ]; then
                INPUT_FILE="$1"
            fi
            shift
            ;;
    esac
done

# 检查输入文件
if [ -z "$INPUT_FILE" ]; then
    echo -e "${YELLOW}错误: 请提供输入文件${NC}"
    show_help
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${YELLOW}错误: 找不到输入文件: $INPUT_FILE${NC}"
    exit 1
fi

# 验证卡片数量
if ! [[ "$NUM_CARDS" =~ ^[0-9]+$ ]] || [ "$NUM_CARDS" -lt 1 ] || [ "$NUM_CARDS" -gt 20 ]; then
    echo -e "${YELLOW}错误: 卡片数量必须是 1-20 之间的数字${NC}"
    exit 1
fi

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}🎨 正在生成小红书卡片...${NC}"
echo -e "输入: $INPUT_FILE"
echo -e "卡片数量: $NUM_CARDS"
if [ "$USE_CONCEPTS" = true ]; then
    echo -e "模式: 7大AI概念专用模板"
fi
echo -e "输出: $OUTPUT_DIR/xiaohongshu-cards.html"

# 读取输入文件内容
TITLE=$(grep -m1 "^# " "$INPUT_FILE" | sed 's/^# //' || echo "小红书图文")

echo -e "${GREEN}✓ 读取标题: $TITLE${NC}"

# 生成动态HTML
generate_html() {
    local num_cards=$1
    local title=$2
    
    # 读取模板头部
    cat "$SKILL_DIR/templates/card-template.html" | sed -n '1,/<body>/p' | sed '$d'
    
    echo "<body>"
    echo "    <!-- 控制栏 -->"
    echo "    <div class=\"controls\">"
    echo "        <button id=\"downloadBtn\" onclick=\"downloadAllCards()\">📸 下载卡片图</button>"
    echo "        <div id=\"progress\" class=\"progress\">正在生成: 0/${num_cards}</div>"
    echo "    </div>"
    echo "    "
    echo "    <!-- 卡片容器 -->"
    echo "    <div id=\"cards-container\">"
    
    if [ "$USE_CONCEPTS" = true ] && [ "$num_cards" -eq 7 ]; then
        # 使用7大AI概念专用模板
        generate_concept_cards "$title"
    else
        # 循环生成通用卡片
        for i in $(seq 1 $num_cards); do
            local card_type=$(( (i - 1) % 7 + 1 ))  # 循环使用7种预设样式
            local card_content=$(get_card_content "$i" "$card_type" "$title")
            echo "$card_content"
        done
    fi
    
    echo "    </div>"
    echo "    "
    
    # 输出JavaScript
    cat <<'JAVASCRIPT'
    <script>
        // 下载所有卡片
        async function downloadAllCards() {
            const btn = document.getElementById('downloadBtn');
            const progress = document.getElementById('progress');
            const cards = document.querySelectorAll('.card');
            const totalCards = cards.length;
            
            btn.disabled = true;
            btn.textContent = '📸 生成中...';
            progress.classList.add('show');
            
            for (let i = 0; i < cards.length; i++) {
                const card = cards[i];
                const index = card.getAttribute('data-index') || (i + 1);
                
                progress.textContent = `正在生成: ${index}/${totalCards}`;
                
                try {
                    // 使用html2canvas截图
                    const canvas = await html2canvas(card, {
                        scale: 3, // 3倍缩放，达到1242x1660px
                        useCORS: true,
                        allowTaint: true,
                        backgroundColor: null,
                        logging: false
                    });
                    
                    // 转换为图片下载
                    const link = document.createElement('a');
                    link.download = `xhs-card-${String(index).padStart(2, '0')}.png`;
                    link.href = canvas.toDataURL('image/png');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    // 延迟，避免浏览器阻塞
                    await new Promise(resolve => setTimeout(resolve, 500));
                    
                } catch (err) {
                    console.error(`卡片${index}生成失败:`, err);
                    alert(`卡片${index}生成失败，请重试`);
                }
            }
            
            progress.textContent = '✅ 全部生成完成!';
            btn.disabled = false;
            btn.textContent = '📸 下载卡片图';
            
            setTimeout(() => {
                progress.classList.remove('show');
            }, 3000);
        }
        
        // 监听Ctrl+S快捷键
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                downloadAllCards();
            }
        });
    </script>
</body>
</html>
JAVASCRIPT
}

# 生成7大AI概念专用卡片
generate_concept_cards() {
    local title=$1
    
    # 第1张：封面
    generate_card_1_cover "$title"
    
    # 第2张：大模型
    generate_card_2_llm
    
    # 第3张：Token
    generate_card_3_token
    
    # 第4张：API
    generate_card_4_api
    
    # 第5张：Skill/MCP
    generate_card_5_skill_mcp
    
    # 第6张：Agent
    generate_card_6_agent
    
    # 第7张：OpenClaw
    generate_card_7_openclaw
}

# 第1张：封面
generate_card_1_cover() {
    cat <<'EOF'
        <!-- 第1张：封面 -->
        <div class="card concept-cover" data-index="1">
            <div class="cover-header">
                <div class="cover-icon">🤖</div>
                <h1>7个AI概念<br>一次搞懂</h1>
            </div>
            <div class="cover-concepts">
                <div class="concept-tag llm">大模型</div>
                <div class="concept-tag token">Token</div>
                <div class="concept-tag api">API</div>
                <div class="concept-tag skill">Skill</div>
                <div class="concept-tag mcp">MCP</div>
                <div class="concept-tag agent">Agent</div>
                <div class="concept-tag openclaw">OpenClaw</div>
            </div>
            <div class="cover-footer">
                <p>🎯 不再被技术黑话绕晕</p>
                <p class="sub">小白也能听懂的AI科普</p>
            </div>
        </div>
EOF
}

# 第2张：大模型
generate_card_2_llm() {
    cat <<'EOF'
        <!-- 第2张：大模型 -->
        <div class="card concept-detail llm-card" data-index="2">
            <div class="concept-header">
                <div class="concept-num">01</div>
                <div class="concept-title-group">
                    <h2>大模型</h2>
                    <span class="concept-en">Large Language Model</span>
                </div>
            </div>
            
            <div class="concept-def">
                <div class="def-icon">🧠</div>
                <p class="def-text">AI的<strong>"大脑"</strong>，会思考、会说话、会创作的数字智能</p>
            </div>
            
            <div class="concept-analogy"
                <h4>💡 生活类比</h4>
                <p>就像读完<strong>全世界所有书</strong>的超级学霸，你问什么他都能答</p>
            </div>
            
            <div class="concept-examples"
                <h4>🌟 常见代表</h4>
                <div class="example-tags"
                    <span class="ex-tag">GPT-4</span>
                    <span class="ex-tag">Claude</span>
                    <span class="ex-tag">通义千问</span>
                    <span class="ex-tag">DeepSeek</span>
                </div>
            </div>
            
            <div class="concept-keypoint"
                <p>⚡ <strong>关键特点</strong>：能对话✅ 能创作✅ 但<strong>不能</strong>自己上网❌</p>
            </div>
        </div>
EOF
}

# 第3张：Token
generate_card_3_token() {
    cat <<'EOF'
        <!-- 第3张：Token -->
        <div class="card concept-detail token-card" data-index="3">
            <div class="concept-header">
                <div class="concept-num">02</div>
                <div class="concept-title-group">
                    <h2>Token</h2>
                    <span class="concept-en">令牌 / 词元</span>
                </div>
            </div>
            
            <div class="concept-def">
                <div class="def-icon">📝</div>
                <p class="def-text">大模型处理信息的<strong>最小单位</strong>，相当于"信息积木块"</p>
            </div>
            
            <div class="concept-analogy"
                <h4>💡 生活类比</h4>
                <p>厨师切菜，把整颗白菜切成一小块一小块。Token就是AI处理文字时的"小块"</p>
            </div>
            
            <div class="concept-formula"
                <h4>📐 换算关系</h4>
                <div class="formula-box"
                    <div class="formula-item">
                        <span class="lang">英文</span>
                        <span class="equals">1个单词 ≈ 1-2 Token</span>
                    </div>
                    <div class="formula-item"
                        <span class="lang">中文</span>
                        <span class="equals">1个汉字 ≈ 1-2 Token</span>
                    </div>
                </div>
            </div>
            
            <div class="concept-keypoint"
                <p>💰 <strong>为什么重要</strong>：计费单位 + 长度限制（4K/8K/128K）</p>
            </div>
        </div>
EOF
}

# 第4张：API
generate_card_4_api() {
    cat <<'EOF'
        <!-- 第4张：API -->
        <div class="card concept-detail api-card" data-index="4">
            <div class="concept-header"
003e
                <div class="concept-num">03</div>
                <div class="concept-title-group">
                    <h2>API</h2>
                    <span class="concept-en">Application Interface</span>
                </div>
            </div>
            
            <div class="concept-def">
                <div class="def-icon">🚪</div>
                <p class="def-text">你和AI大脑之间的<strong>"传话筒"</strong>，按规矩发送请求、接收回答</p>
            </div>
            
            <div class="concept-analogy">
                <h4>💡 生活类比：餐厅服务员</h4>
                <div class="analogy-flow">
                    <div class="flow-item">你点菜</div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-item">服务员传话</div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-item">厨师做菜</div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-item">服务员端菜</div>
                </div>
            </div>
            
            <div class="concept-why">
                <h4>🤔 为什么用API？</h4>
                <div class="why-grid">
                    <div class="why-item">
                        <span class="why-icon">🔒</span>
                        <p>安全</p>
                    </div>
                    <div class="why-item">
                        <span class="why-icon">📐</span>
                        <p>标准化</p>
                    </div>
                    <div class="why-item">
                        <span class="why-icon">🔄</span>
                        <p>可复用</p>
                    </div>
                </div>
            </div>
        </div>
EOF
}

# 第5张：Skill/MCP
generate_card_5_skill_mcp() {
    cat <<'EOF'
        <!-- 第5张：Skill/MCP -->
        <div class="card concept-detail skill-card" data-index="5">
            <div class="concept-header">
                <div class="concept-num">04</div>
                <div class="concept-title-group">
                    <h2>Skill / MCP</h2>
                    <span class="concept-en">技能 / Model Context Protocol</span>
                </div>
            </div>
            
            <div class="concept-def">
                <div class="def-icon">🔧</div>
                <p class="def-text">给AI大脑安装的<strong>"App"或"插件"</strong>，让它拥有具体技能</p>
            </div>
            
            <div class="concept-analogy">
                <h4>💡 生活类比</h4>
                <p>就像手机里的<strong>各种App</strong>：查天气、导航、订外卖...</p>
            </div>
            
            <div class="concept-examples">
                <h4>📱 常见 Skill 示例</h4>
                <div class="skill-list">
                    <div class="skill-item">
                        <span class="skill-icon">🌤️</span>
                        <span class="skill-name">天气查询</span>
                    </div>
                    <div class="skill-item">
                        <span class="skill-icon">📧</span>
                        <span class="skill-name">邮件发送</span>
                    </div>
                    <div class="skill-item">
                        <span class="skill-icon">🔍</span>
                        <span class="skill-name">网页搜索</span>
                    </div>
                    <div class="skill-item">
                        <span class="skill-icon">💾</span>
                        <span class="skill-name">文件操作</span>
                    </div>
                </div>
            </div>
            
            <div class="concept-keypoint">
                <p>🔗 <strong>MCP</strong>：Anthropic推出的<strong>开放协议</strong>，标准化Skill的接入方式</p>
            </div>
        </div>
EOF
}

# 第6张：Agent
generate_card_6_agent() {
    cat <<'EOF'
        <!-- 第6张：Agent -->
        <div class="card concept-detail agent-card" data-index="6">
            <div class="concept-header">
                <div class="concept-num">05</div>
                <div class="concept-title-group">
                    <h2>Agent</h2>
                    <span class="concept-en">智能体 / AI Agent</span>
                </div>
            </div>
            
            <div class="concept-def">
                <div class="def-icon">🤖</div>
                <p class="def-text">能自主规划、使用工具、完成复杂任务的<strong>"数字员工"</strong></p>
            </div>
            
            <div class="concept-analogy">
                <h4>💡 生活类比：全能管家</h4>
                <p>你说"安排一次上海出差"，他会自动：</p>
            </div>
            
            <div class="agent-flow">
                <div class="flow-step">
                    <div class="step-num">1</div>
                    <p>查机票</p>
                </div>
                <div class="flow-step">
                    <div class="step-num">2</div>
                    <p>订酒店</p>
                </div>
                <div class="flow-step">
                    <div class="step-num">3</div>
                    <p>写行程</p>
                </div>
                <div class="flow-step">
                    <div class="step-num">4</div>
                    <p>发通知</p>
                </div>
            </div>
            
            <div class="concept-keypoint">
                <p>⚡ <strong> vs 大模型</strong>：能对话 ✅ 能<strong>用工具</strong> ✅ 能<strong>自主规划</strong> ✅</p>
            </div>
        </div>
EOF
}

# 第7张：OpenClaw
generate_card_7_openclaw() {
    cat <<'EOF'
        <!-- 第7张：OpenClaw -->
        <div class="card concept-detail openclaw-card" data-index="7">
            <div class="concept-header">
                <div class="concept-num">06</div>
                <div class="concept-title-group">
                    <h2>OpenClaw</h2>
                    <span class="concept-en">Agent Operating System</span>
                </div>
            </div>
            
            <div class="concept-def">
                <div class="def-icon">🏠</div>
                <p class="def-text">运行和管理AI Agent的<strong>"操作系统"</strong>或<strong>"工作平台"</strong></p>
            </div>
            
            <div class="concept-analogy">
                <h4>💡 生活类比</h4>
                <p>像 <strong>iOS/Android</strong> 之于手机App，<strong>Windows/MacOS</strong> 之于电脑软件</p>
            </div>
            
            <div class="openclaw-functions">
                <h4>⚙️ 核心功能</h4>
                <div class="func-grid">
                    <div class="func-item">
                        <span class="func-icon">🏃</span>
                        <p>运行Agent</p>
                    </div>
                    <div class="func-item">
                        <span class="func-icon">🧩</span>
                        <p>管理Skills</p>
                    </div>
                    <div class="func-item">
                        <span class="func-icon">🔌</span>
                        <p>连接模型</p>
                    </div>
                    <div class="func-item">
                        <span class="func-icon">🔒</span>
                        <p>安全管控</p>
                    </div>
                </div>
            </div>
            
            <div class="concept-summary">
                <p>🎯 <strong>一句话总结</strong></p>
                <p class="summary-text">大模型是<strong>"脑"</strong>，Agent是<strong>"人"</strong>，OpenClaw是<strong>"他们生活的世界"</strong></p>
            </div>
        </div>
EOF
}

# 获取通用卡片内容（保留原有函数）
get_card_content() {
    local index=$1
    local card_type=$2
    local title=$3
    
    case $card_type in
        1)
            # 封面图样式
            cat <<EOF
        <!-- 第${index}张：封面图 -->
        <div class="card card-1" data-index="${index}">
            <div class="icon-group">
                <div class="robot-icon">🤖</div>
                <div class="warning-icon">⚠️</div>
            </div>
            <h1>${title}</h1>
            <div class="subtitle">
                <p>精彩内容<br>点击查看详情</p>
            </div>
        </div>
EOF
            ;;
        2)
            # 问题引入样式
            cat <<EOF
        <!-- 第${index}张：问题引入 -->
        <div class="card card-2" data-index="${index}">
            <div class="header">
                <div class="logo">💡</div>
                <div class="title-text">
                    <h2>引发思考的话题</h2>
                </div>
            </div>
            <div class="content-box">
                <p>👇 这是一个值得探讨的问题</p>
                <p>让我们一起深入了解</p>
            </div>
            <div class="warning-box">
                <div class="skull">🎯</div>
                <p>核心观点<br>重点内容提炼<br><br>值得关注的关键信息</p>
            </div>
        </div>
EOF
            ;;
        3)
            # 大佬观点样式
            cat <<EOF
        <!-- 第${index}张：观点分享 -->
        <div class="card card-3" data-index="${index}">
            <div class="avatars">
                <div class="avatar">
                    <div class="avatar-circle">⭐</div>
                    <span>观点</span>
                </div>
                <div class="avatar">
                    <div class="avatar-circle">💎</div>
                    <span>精华</span>
                </div>
            </div>
            <div class="quote-box">
                <p>"重要的观点<br>值得分享的内容<br><br>深入思考后的见解"</p>
            </div>
            <div class="summary">
                <h3>💡 核心要点</h3>
                <p>抓住重点✅<br>理解本质💪</p>
            </div>
        </div>
EOF
            ;;
        4)
            # 案例故事样式
            cat <<EOF
        <!-- 第${index}张：案例分享 -->
        <div class="card card-4" data-index="${index}">
            <div class="case-header">
                <div class="case-icon">📊</div>
                <h3>实际案例分析</h3>
            </div>
            <div class="timeline">
                <div class="timeline-item round">
                    <p><span class="round-num">Step 1</span>问题发现</p>
                </div>
                <div class="timeline-item round">
                    <p><span class="round-num">Step 2</span>分析原因</p>
                </div>
                <div class="timeline-item round">
                    <p><span class="round-num">Step 3</span>解决方案</p>
                </div>
                <div class="timeline-item round">
                    <p><span class="round-num">Step 4</span>成果展示✅</p>
                </div>
            </div>
            <div class="result-box">
                <p>🎯 实践出真知<br>理论结合实际</p>
            </div>
        </div>
EOF
            ;;
        5)
            # 三阶段能力样式
            cat <<EOF
        <!-- 第${index}张：方法总结 -->
        <div class="card card-5" data-index="${index}">
            <h3>🔥 实用方法分享</h3>
            <div class="stages">
                <div class="stage-item stage-1">
                    <div class="stage-icon">1️⃣</div>
                    <div class="stage-content">
                        <h4>第一步：理解问题</h4>
                        <p>明确目标，找准方向</p>
                    </div>
                </div>
                <div class="stage-item stage-2">
                    <div class="stage-icon">2️⃣</div>
                    <div class="stage-content">
                        <h4>第二步：制定策略</h4>
                        <p>规划路径，分步执行</p>
                    </div>
                </div>
                <div class="stage-item stage-3">
                    <div class="stage-icon">3️⃣</div>
                    <div class="stage-content">
                        <h4>第三步：落实行动</h4>
                        <p>持续改进，达成目标</p>
                    </div>
                </div>
            </div>
            <div class="highlight">
                <p>💡 每个步骤都是精心设计<br>帮助你快速上手！</p>
            </div>
        </div>
EOF
            ;;
        6)
            # 数据真相样式
            cat <<EOF
        <!-- 第${index}张：数据展示 -->
        <div class="card card-6" data-index="${index}">
            <div class="truth-header">
                <h3>📈 数据说话</h3>
                <div class="big-number">90<span>%</span></div>
                <p style="color: #666; font-size: 14px; margin-top: 5px;">用户反馈积极好评👍</p>
            </div>
            <div class="compare-box">
                <div class="compare-item wrong">
                    <div class="icon">📉</div>
                    <h4>传统方式</h4>
                    <p>效率较低<br>耗时较长<br>成本较高</p>
                </div>
                <div class="compare-item right">
                    <div class="icon">📈</div>
                    <h4>新方法</h4>
                    <p>效率提升<br>时间节省<br>效果更好💪</p>
                </div>
            </div>
        </div>
EOF
            ;;
        7)
            # 互动+CTA样式
            cat <<EOF
        <!-- 第${index}张：互动与行动 -->
        <div class="card card-7" data-index="${index}">
            <div class="poll-section">
                <h3>💬 你觉得这个内容有帮助吗？</h3>
                <div class="poll-options">
                    <div class="poll-btn">
                        <span class="opt-letter">A</span>
                        <span class="opt-text">非常有用 👍</span>
                    </div>
                    <div class="poll-btn">
                        <span class="opt-letter">B</span>
                        <span class="opt-text">还不错 😊</span>
                    </div>
                    <div class="poll-btn">
                        <span class="opt-letter">C</span>
                        <span class="opt-text">一般般 🤔</span>
                    </div>
                    <div class="poll-btn">
                        <span class="opt-letter">D</span>
                        <span class="opt-text">期待更多 🚀</span>
                    </div>
                </div>
            </div>
            <div class="cta-section">
                <h4>📚 持续学习，不断进步</h4>
                <p>关注我，获取更多干货内容<br>一起成长！</p>
                <div class="cta-btn">💌 点赞关注</div>
                <div class="tags">
                    #干货分享 #学习成长 #知识分享 #自我提升
                </div>
            </div>
        </div>
EOF
            ;;
    esac
}

# 使用 LLM 生成卡片 HTML
generate_llm_cards() {
    local title="$1"
    local content="$2"
    local temp_file=$(mktemp)
    
    # 准备提示内容
    cat > "$temp_file" << EOF
请将以下 Markdown 内容转换为小红书风格的 HTML 卡片。

## 要求：
1. 输出必须是纯 HTML 代码（不包含 markdown 代码块标记）
2. 使用内联样式，适配 414x553px 的卡片尺寸
3. 字体大小：标题 20-24px，正文 13-15px
4. 配色使用现代渐变风格
5. 重要概念用 <strong> 加粗
6. 适当使用 emoji 增加趣味性
7. 代码块使用特殊样式展示

## 内容：

$content

## 输出格式：
直接返回 <div class="card" style="...">...</div> 的内容，不要返回完整的 HTML 文档。
EOF
    
    # 调用 LLM (使用虚拟环境的 Python)
    local python_path="/home/claw/venv/bin/python3"
    if [ ! -f "$python_path" ]; then
        python_path="python3"
    fi
    
    if [ -f "$SKILL_DIR/scripts/llm_helper.py" ]; then
        "$python_path" "$SKILL_DIR/scripts/llm_helper.py" "$temp_file" 2>/dev/null || echo ""
    else
        echo ""
    fi
    
    rm -f "$temp_file"
}

# 生成HTML文件
if [ "$USE_LLM" = true ] && [ -n "$LLM_API_KEY" ]; then
    echo -e "${BLUE}🤖 使用 LLM 智能生成卡片...${NC}"
    
    # 手动加载 .env 文件中的变量
    env_file="$SKILL_DIR/.env"
    if [ -f "$env_file" ]; then
        while IFS= read -r line || [[ -n "$line" ]]; do
            # 跳过注释和空行
            [[ "$line" =~ ^#.*$ ]] && continue
            [[ -z "$line" ]] && continue
            # 只处理包含 = 的行
            if [[ "$line" == *"="* ]]; then
                key="${line%%=*}"
                value="${line#*=}"
                # 去除 key 的前后空格
                key=$(echo "$key" | xargs)
                export "$key=$value"
            fi
        done < "$env_file"
    fi
    
    # 调用 generate_llm.py
    python_path="/home/claw/venv/bin/python3"
    if [ ! -f "$python_path" ]; then
        python_path="python3"
    fi
    
    "$python_path" "$SKILL_DIR/scripts/generate_llm.py" \
        "$INPUT_FILE" \
        -o "$OUTPUT_DIR/xiaohongshu-cards.html" \
        -n "$NUM_CARDS"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ LLM卡片生成完成!${NC}"
    else
        echo -e "${YELLOW}⚠️ LLM生成失败，回退到通用模板模式${NC}"
        generate_html "$NUM_CARDS" "$TITLE" > "$OUTPUT_DIR/xiaohongshu-cards.html"
        echo -e "${GREEN}✓ 卡片生成完成!${NC}"
    fi
else
    # 原有生成逻辑
    generate_html "$NUM_CARDS" "$TITLE" > "$OUTPUT_DIR/xiaohongshu-cards.html"
    
    echo -e "${GREEN}✓ 卡片生成完成!${NC}"
fi

echo ""
echo -e "${BLUE}📤 导出方法:${NC}"
echo "  1. 浏览器打开: $OUTPUT_DIR/xiaohongshu-cards.html"
echo "  2. 点击'📸 下载卡片图'按钮自动导出所有卡片"
echo "  3. 或使用快捷键 Ctrl+S 快速触发下载"
echo ""
if [ "$USE_CONCEPTS" = true ]; then
    echo -e "${YELLOW}提示: 使用7大AI概念专用模板生成${NC}"
fi
echo -e "${YELLOW}提示: 每张卡片尺寸为 414×553px (等比3倍后为小红书标准 1242×1660px)${NC}"