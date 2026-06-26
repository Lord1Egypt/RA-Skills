---
name: company-info-personal
description: 员工个人版公司情报查询工具。当员工输入公司名称时触发，直接调用公司 API 采集端点，由公司端 company-info-aggregator 内部决定走缓存还是搜索，员工端无需关心中间状态。适用于 B2B 销售人员的日常客户查询场景。
metadata: {"clawdbot": {"emoji": "👤", "os": ["linux", "darwin"], "requires": {"bins": ["jq", "python3"]}}}
triggers:
 - "查询公司"
 - "公司情报"
 - "搜索公司"
 - "查一下公司"
 - "查询 {公司名}"
 - "{公司名} 情报"
 - "有限公司"
 - "有限责任公司"
 - "科技公司"
 - "公司信息"
 - "企业背景"
 - "工商信息"
---

# Company Info Personal (员工个人版公司情报官)

你是员工个人版的公司情报查询工具。你的核心职责是：**一次调用，智能响应**。

## 核心工作流

```
用户输入公司名
  → Step 1: 生成 company_id
  → Step 2: 自动 Token 续期
  → Step 3: 直接调用公司 API 采集端点（POST /collect）
  → Step 4: 统一处理响应 & 输出报告（含商机信号）
```

**设计说明**：不再分两步（先 GET 查询，未命中再 POST 采集），而是直接调用 collect 端点。公司端的 `company-info-aggregator` 内部已有缓存检查逻辑（Step 0），命中时秒回，未命中时自动采集。员工端无需关心中间状态。

**重要约束**：输出报告后**禁止**追问"是否需要商机洞察"或类似引导语。商机信号已在报告中直接展示，不需要二次确认。如用户主动要求深入分析，再调用 `b2b-opportunity-insighter`。

## Step 1: 生成 company_id

```bash
company_id=$(echo "{公司名}" | python3 -c "
import sys
name = sys.stdin.read().strip()
for suffix in ['有限公司','股份有限公司','有限责任公司','集团','公司','Co.Ltd','Inc.','Corp.','Ltd.']:
    name = name.replace(suffix, '')
print(name[:4].lower())
")
```

示例：
- "南京绛门信息科技有限公司" → `nanj`
- "Microsoft Corporation" → `micr`
- "华为技术有限公司" → `huaw`

## Step 2: 自动 Token 续期

**重要**：在调用 API 前，先检查 Token 是否即将过期，自动刷新。**无感知，不提示用户**。

### Step 2.1: Skill 初始化（首次使用）

```bash
TOKEN_CACHE=~/.openclaw/workspace/scripts/.token-cache.json

# 检查 Token 缓存是否存在
if [ ! -f "$TOKEN_CACHE" ]; then
    echo "🔑 首次使用，需要初始化..."
    echo ""
    echo "请输入您的员工号（如 emp-server-106）："
    read EMPLOYEE_ID
    
    if [ -z "$EMPLOYEE_ID" ]; then
        echo "⚠️ 员工号不能为空，请重新输入"
        结束执行
    fi
    
    echo ""
    echo "请输入您的姓名："
    read EMPLOYEE_NAME
    
    if [ -z "$EMPLOYEE_NAME" ]; then
        echo "⚠️ 姓名不能为空，请重新输入"
        结束执行
    fi
    
    echo ""
    echo "正在获取 Token..."
    
    # 调用 auto-token 接口
    AUTO_TOKEN_URL="${COMPANY_INFO_API_URL:-http://47.116.49.218:3000/api}/auth/auto-token"
    
    response=$(curl -s -X POST "$AUTO_TOKEN_URL" \
      -H "Content-Type: application/json" \
      -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\"}" \
      --max-time 10)
    
    status=$(echo "$response" | jq -r '.status')
    
    if [ "$status" = "success" ]; then
        API_TOKEN=$(echo "$response" | jq -r '.token')
        expires_at=$(echo "$response" | jq -r '.expires_at')
        expires_in_days=$(echo "$response" | jq -r '.expires_in_days')
        
        # 保存 Token 缓存
        mkdir -p ~/.openclaw/workspace/scripts
        echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${expires_at}\", \"updated_at\": \"$(date -Iseconds)\"}" > "$TOKEN_CACHE"
        
        echo "✅ Token 获取成功（有效期 ${expires_in_days} 天）"
        echo ""
    else
        error_message=$(echo "$response" | jq -r '.message')
        echo "⚠️ Token 获取失败：$error_message"
        echo ""
        echo "建议："
        echo "  1. 确认员工号正确"
        echo "  2. 联系管理员添加到白名单"
        结束执行
    fi
fi
```

### Step 2.2: Token 缓存检查与自动续期

```bash
TOKEN_CACHE=~/.openclaw/workspace/scripts/.token-cache.json

if [ -f "$TOKEN_CACHE" ]; then
    cache_updated=$(jq -r '.updated_at' "$TOKEN_CACHE")
    expires_at=$(jq -r '.expires_at' "$TOKEN_CACHE")
    
    # 计算剩余天数
    if [ -n "$expires_at" ] && [ "$expires_at" != "null" ]; then
        expires_timestamp=$(date -d "$expires_at" +%s 2>/dev/null || echo 0)
        now_timestamp=$(date +%s)
        days_remaining=$(( (expires_timestamp - now_timestamp) / 86400 ))
        
        # 检测即将过期（<7天）或已过期，自动续期（无感知）
        if [ $days_remaining -lt 7 ]; then
            # 后台自动续期，不提示用户
            AUTO_TOKEN_URL="${COMPANY_INFO_API_URL:-http://47.116.49.218:3000/api}/auth/auto-token"
            EMPLOYEE_ID=$(jq -r '.employee_id' "$TOKEN_CACHE")
            EMPLOYEE_NAME=$(jq -r '.employee_name' "$TOKEN_CACHE")
            
            response=$(curl -s -X POST "$AUTO_TOKEN_URL" \
              -H "Content-Type: application/json" \
              -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\"}" \
              --max-time 10 > /dev/null 2>&1)
            
            status=$(echo "$response" | jq -r '.status')
            
            if [ "$status" = "success" ]; then
                API_TOKEN=$(echo "$response" | jq -r '.token')
                new_expires_at=$(echo "$response" | jq -r '.expires_at')
                
                # 更新缓存（无感知）
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires_at}\", \"updated_at\": \"$(date -Iseconds)\"}" > "$TOKEN_CACHE"
            fi
        fi
        
        API_TOKEN=$(jq -r '.token' "$TOKEN_CACHE")
    else
        API_TOKEN="${COMPANY_INFO_API_TOKEN}"
    fi
else
    API_TOKEN="${COMPANY_INFO_API_TOKEN}"
fi
```

---

## Step 3: 直接调用公司 API 采集端点

**设计说明**：直接调用 collect 端点，由公司端 `company-info-aggregator` 内部决定走缓存还是搜索。员工端只需一次调用，无需关心中间状态。

```bash
COMPANY_API_URL="${COMPANY_INFO_API_URL:-http://47.116.49.218:3000/api/company-info}"

FORCE_REFRESH=false
if 用户输入包含 ["重新搜索","更新","刷新","re-search","update","refresh"]; then
    FORCE_REFRESH=true
fi

if [ "$FORCE_REFRESH" = true ]; then
    echo "🔄 强制刷新模式，跳过公司端缓存..."
fi

response=$(curl -s -X POST "${COMPANY_API_URL}/collect" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"company_name\": \"${company_name}\", \"force_refresh\": ${FORCE_REFRESH}}" \
  --max-time 120)

status=$(echo "$response" | jq -r '.status')
```

### 环境变量配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "company-info-personal": {
        "env": {
          "COMPANY_INFO_API_URL": "https://company-server/api/company-info",
          "COMPANY_INFO_API_TOKEN": "员工访问令牌"
        }
      }
    }
  }
}
```

## Step 4: 统一处理响应

无需区分"查询命中"和"采集完成"，统一处理公司端返回的结果：

```bash
case "$status" in
    "success")
        last_updated=$(echo "$response" | jq -r '.data.last_updated')
        data_completeness=$(echo "$response" | jq -r '.data.data_completeness.coverage_rate')
        priority_level=$(echo "$response" | jq -r '.data.priority_level')
        source=$(echo "$response" | jq -r '.data.source // "unknown"')

        if [ "$source" = "cache" ]; then
            echo "📦 已加载缓存数据（<5 秒响应）"
        else
            echo "✅ 情报采集完成"
        fi

        echo "📊 数据概览：更新于 ${last_updated} | 完整度 ${data_completeness} | 优先级 ${priority_level}"
        echo ""

        # 优先使用 report 字段，没有则用 raw_data 渲染
        if [ -n "$(echo "$response" | jq -r '.data.report // empty')" ]; then
            echo "$response" | jq -r '.data.report'
        elif [ -n "$(echo "$response" | jq -r '.data.raw_data // empty')" ]; then
            echo "$response" | jq -r '.data.raw_data'
        else
            echo "$response" | jq -r '.data'
        fi

        # 如果 raw_data 中包含商机信号，直接输出
        signals=$(echo "$response" | jq -r '.data.raw_data.signals // empty')
        if [ -n "$signals" ]; then
            echo ""
            echo "## 🎯 商机信号"
            echo "$response" | jq -r '.data.raw_data.signals.strong[]? // empty' | while read s; do echo "- 🟢 $s"; done
            echo "$response" | jq -r '.data.raw_data.signals.medium[]? // empty' | while read s; do echo "- 🟡 $s"; done
            echo "$response" | jq -r '.data.raw_data.signals.weak[]? // empty' | while read s; do echo "- 🔵 $s"; done
        fi

        # 如果有商机洞察报告，直接输出
        insight=$(echo "$response" | jq -r '.data.opportunity_insight // empty')
        if [ -n "$insight" ]; then
            echo ""
            echo "$insight"
        fi
        结束执行
        ;;
    "guide_mode")
        echo "⚠️ 线上公开信息有限（受反爬限制）"
        echo ""
        echo "💡 但这反而是机会！竞争对手也找不到这家公司，你先拜访就占优势。"
        echo ""
        echo "已尝试的数据源："
        echo "$response" | jq -r '.details.attempted_sources[] | "| \(.source) | \(.status) | \(.reason) |"' | column -t -s '|'
        echo ""
        echo "$response" | jq -r '.guide_mode_report'
        结束执行
        ;;
    "error")
        error_message=$(echo "$response" | jq -r '.message')

        if echo "$error_message" | grep -qi "过期\|expired"; then
            echo "⚠️ Token 已过期，正在自动刷新..."
            $REFRESH_SCRIPT --force
            API_TOKEN=$(jq -r '.skills.entries["company-info-personal"].env.COMPANY_INFO_API_TOKEN' ~/.openclaw/openclaw.json)
            echo "🔄 已刷新 Token，正在重试..."
        else
            echo "⚠️ API 调用失败：$error_message"
            echo ""
            echo "建议："
            echo "  1. 稍后重试"
            echo "  2. 联系管理员检查公司服务器采集配置"
        fi
        ;;
    *)
        echo "⚠️ 未知响应格式：$response"
        结束执行
        ;;
esac
```

## 输出格式

### 统一输出格式

**必须按以下顺序完整输出，不得省略任何部分：**

1. **公司情报**：基本信息、业务概况、核心人员、近期动态
2. **商机信号**：强/中/弱信号分级展示
3. **商机洞察报告**：如果 API 返回了 `opportunity_insight` 字段，**必须完整输出该内容**，这是公司资产库中已有的深度分析报告，包含执行摘要、战略态势、需求-方案-价值映射、决策链分析、行动计划等。不得省略、不得摘要、不得询问用户是否需要。

```markdown
# 🏢 {公司名} - 公司情报报告

> 更新时间：{last_updated} | 数据完整度：{coverage_rate}

---

[输出公司情报内容：基本信息、业务、人员、动态]

---

## 🎯 商机信号

[直接输出 signals 数据]

---

[完整输出 opportunity_insight 内容，不得省略]

---

如需更新情报，回复"重新搜索 {公司名}"
```

**说明**：不标注数据来源，用户体验一致。

## 触发规则

| 用户输入 | 是否触发 |
|---------|---------|
| "{公司名}"（单独公司名） | ✅ 触发 |
| "查一下 {公司名}" | ✅ 触发 |
| "{公司名} 的公司情报" | ✅ 触发 |
| "重新搜索 {公司名}" | ✅ 触发（force_refresh=true，跳过公司端缓存） |
| "分析 {公司名} 商机" | ❌ 不触发（由 b2b-opportunity-insighter 处理） |

## 与 company-info-aggregator 的区别

| 维度 | company-info-aggregator（公司版） | company-info-personal（个人版） |
|------|--------------------------------|-------------------------------|
| 部署位置 | 公司服务器（隔离） | 员工服务器（100+ 实例） |
| 定位 | 情报采集层 | 情报查询层 |
| 数据源 | 外部搜索引擎 + 权威数据源 | 公司 API（POST /collect） |
| 缓存逻辑 | 内置 Step 0 缓存检查 | 无需关心，由公司端处理 |
| 响应速度 | 慢（30-120 秒，首次） | 快（缓存命中时<5 秒） |
| 适用场景 | 首次采集、强制更新 | 日常查询 |
| 数据存储 | 公司资产库（敏感） | 不存储，仅缓存会话 |
| 权限模型 | 采集权限 | 只读查询权限 |

## 自动链式执行

**重要**：报告输出完成后，如果数据中包含商机信号（signals），**直接输出商机信号**，不再询问用户。信号分级展示：

- 🟢 强信号（strong）：立即行动
- 🟡 中等信号（medium）：重点关注
- 🔵 弱信号（weak）：持续观察

**禁止行为**：报告输出后**不得**追问"是否需要商机洞察"、"是否需要深入分析"等引导语。商机信号已直接展示，无需二次确认。只有用户主动要求时才调用 `b2b-opportunity-insighter`。

## 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| Token 过期 | 自动刷新 Token 并重试 |
| 公司服务器不可达 | 提示网络错误，建议检查连接 |
| 采集超时 | 建议稍后重试 |
| 公司名称模糊 | 询问用户确认具体公司 |

## 使用示例

**示例 1：公司端缓存命中（<5 秒）**
```
用户：南京绛门信息科技有限公司
→ 生成 company_id: nanj
→ POST /api/company-info/collect { company_name, force_refresh: false }
→ 公司端 aggregator Step 0 缓存命中 → 直接返回
→ 输出报告（<5 秒）
```

**示例 2：公司端缓存未命中（首次采集）**
```
用户：上海某某科技公司
→ 生成 company_id: shan
→ POST /api/company-info/collect { company_name, force_refresh: false }
→ 公司端 aggregator Step 0 缓存未命中 → 执行搜索采集
→ 采集完成 → 返回报告（30-120 秒）
```

**示例 3：强制刷新**
```
用户：重新搜索南京绛门信息科技有限公司
→ POST /api/company-info/collect { company_name, force_refresh: true }
→ 公司端 aggregator 跳过缓存 → 重新采集
→ 返回最新报告（30-120 秒）
```

---

## 📝 修改记录

| 日期 | 修改内容 | 修改人 |
|------|---------|--------|
| 2026-05-24 | 初始创建：员工个人版公司情报 skill | 用户要求 |
| 2026-05-26 | 优化：去掉两步调用（GET→POST），改为直接 POST /collect，由公司端 aggregator 内部决定走缓存还是搜索 | 用户要求 |
