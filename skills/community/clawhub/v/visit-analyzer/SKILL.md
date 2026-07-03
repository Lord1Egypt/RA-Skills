---
name: visit-analyzer
description: 拜访记录分析引擎。根据员工的拜访沟通记录，AI 分析销售阶段、跟进策略、客户洞察、承诺事项和风险预估。当员工要求查看某个客户/公司的聊天分析时触发，自动生成项目画像并输出 H5 链接。
metadata: {"clawdbot": {"emoji": "📊", "os": ["linux", "darwin"], "requires": {"bins": ["curl", "jq", "python3"]}}}
triggers:
 - "查看.*分析"
 - "聊天分析"
 - "拜访分析"
 - "项目画像"
 - "销售阶段"
 - "分析.*沟通记录"
 - "分析.*拜访"
 - "总结.*录音"
 - "重新总结"
 - "分析.*录音"
 - "录音.*分析"
 - "整理.*线索"
 - "线索跟进"
 - "跟进记录"
---

# Visit Analyzer（拜访记录分析引擎）

你是拜访记录分析引擎。核心职责：**解析员工意图 → 读取录音转录文件 → AI 分析对话内容 → 提取项目名称 → 生成项目画像 → 输出 H5 链接**。

## 核心工作流（7 步）

```
员工输入"查看我和XX公司/张三的聊天分析"
  → Step 1: Token 管理（复用 employee-radar 的分层续期逻辑）
  → Step 2: 解析意图（提取公司名/联系人/主题/项目名称 + 判断数据源类型）
  → Step 3: 客户确认（公司名不明确时，从数据库查询已有客户让员工选择）
  → Step 4: 根据 source_type 查找并读取聊天内容
            ├─ phone:   读取录音转录文件（transcripts/*.md）
            └─ wechat:  读取微信通知（notifications/YYYY-MM-DD.json）
  → Step 5: AI 分析聊天内容（5 大模块 + 项目名称识别）
  → Step 6: 生成项目画像
            （后端自动处理客户关联和画像存储）
  → Step 7: 输出摘要 + H5 链接（/project-portrait-new/{portraitId}）
```

**重要约束**：
- **不输出中间步骤状态**，直接输出最终结果（禁止输出"Token 有效"、"进入 Step X"、"保存成功"等过程性信息）
- 输出摘要后**禁止**追问"是否需要进一步分析"等引导语
- 完整数据通过 H5 链接查看
- 所有分析必须基于实际拜访记录，**绝不编造**
- **Skill 不需要手动创建 Customer 和 Visit**——`ingest` 接口会自动创建/关联客户
- **数据按员工+项目隔离**：`employee_code + company_name + project_name` 联合确定唯一画像记录
- **支持多数据源**：电话录音转录 + 微信聊天记录，同一客户的两种数据可增量合并
- **项目名称来源**：优先用户指定 → AI 自动识别 → 默认使用 company_name

---

## Step 1: Token 管理（分层续期）

**重要**：Token 有效期内自动续期，**不提示用户**。首次使用或 Token 失效时，引导用户输入账号和密码。

### 跨平台日期工具函数

macOS 不支持 `date -d` 和 `date -Iseconds`，统一使用 python3：

```bash
iso_now() { python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat())"; }
to_timestamp() { python3 -c "
from datetime import datetime, timezone
import sys
try:
    s = sys.argv[1]
    # 尝试解析带时区的 ISO 字符串
    if '+' in s or 'Z' in s:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
    else:
        # 无时区信息，假设为 UTC
        dt = datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    print(int(dt.timestamp()))
except Exception:
    print(0)
" "$1" 2>/dev/null || echo 0; }
now_ts() { python3 -c "from datetime import datetime, timezone; print(int(datetime.now(timezone.utc).timestamp()))"; }
```

### Token 续期策略

```
1. TOKEN_CACHE 不存在 → 交互输入账号和密码 → POST /auth/login
2. Token 仍有效（>7天）→ 直接使用
3. Token 即将过期（≤7天但仍未过期）→ /auth/renew-token（优先）→ 失败降级 POST /auth/login（需用户重新输入密码）
4. Token 已过期 → 引导用户重新登录（需输入账号和密码）
```

### Step 1.1: Skill 初始化（首次使用）

员工无需配置任何文件，首次使用时通过交互输入账号和密码即可完成初始化。

```bash
TOKEN_CACHE=~/.openclaw/workspace/scripts/.token-cache.json
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"

if [ ! -f "$TOKEN_CACHE" ]; then
    echo "🔑 需要验证您的员工身份"
    echo ""
    echo "请输入您的账号和密码，格式：账号 密码"
    echo "例如：emp-server-106 123456"
    echo ""
    echo "（等待用户输入...）"
    # AI 从用户回复中提取 employee_id（账号）和 password（密码）
    # 用户输入示例："emp-server-106 123456" 或 "我的账号是 emp-server-106，密码是 123456"
    # AI 需解析出 employee_id 和 password 两个值

    response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
      -H "Content-Type: application/json" \
      -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
      --max-time 120)

    code=$(echo "$response" | jq -r '.code')

    if [ "$code" = "0" ]; then
        API_TOKEN=$(echo "$response" | jq -r '.data.token')
        expires_at=$(echo "$response" | jq -r '.data.expires_at')
        expires_in_days=$(echo "$response" | jq -r '.data.expires_in_days')
        employee_name=$(echo "$response" | jq -r '.data.employee_name')
        must_change_pw=$(echo "$response" | jq -r '.data.must_change_pw')

        mkdir -p ~/.openclaw/workspace/scripts
        echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${employee_name}\", \"expires_at\": \"${expires_at}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"

        # 首次登录强制改密检测
        if [ "$must_change_pw" = "true" ]; then
            echo "⚠️ 检测到您是首次登录，需要先修改密码"
            echo ""
            echo "请输入新密码（至少6位）："
            echo "（等待用户输入新密码...）"

            # AI 从用户回复中提取 new_password
            pw_response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/change-password" \
              -H "Content-Type: application/json" \
              -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"old_password\": \"${PASSWORD}\", \"new_password\": \"${NEW_PASSWORD}\"}" \
              --max-time 120)

            pw_code=$(echo "$pw_response" | jq -r '.code')
            if [ "$pw_code" = "0" ]; then
                echo "✅ 密码修改成功！"
                # change-password 接口已返回新 token（旧 token 已被后端删除），直接更新缓存
                API_TOKEN=$(echo "$pw_response" | jq -r '.data.token')
                new_expires=$(echo "$pw_response" | jq -r '.data.expires_at')
                employee_name=$(echo "$pw_response" | jq -r '.data.employee_name')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${employee_name}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                pw_error=$(echo "$pw_response" | jq -r '.message')
                echo "⚠️ 密码修改失败：$pw_error"
                echo "您可以稍后在管理后台修改密码"
            fi
        fi

        echo "✅ 身份验证成功！欢迎 ${employee_name}"
    else
        error_message=$(echo "$response" | jq -r '.message')
        echo "⚠️ 登录失败：$error_message"
        echo "建议："
        echo "  1. 确认账号和密码正确"
        echo "  2. 联系管理员确认您的账号是否已创建"
        exit 1
    fi
fi
```

**交互输入解析规则**：

| 用户输入格式 | 解析方式 | 示例 |
|-------------|---------|------|
| `账号 密码` | 空格分隔，前者为账号（employee_id），后者为密码 | `emp-server-106 123456` |
| `我的账号是xxx，密码是xxx` | 自然语言提取账号和密码 | 自然语言提取 |
| `xxx xxx` | 空格分隔，前者为账号，后者为密码 | `106 Abc123` |

**重要**：交互输入仅在首次使用时触发一次，Token 写入缓存后后续自动读取，不再询问。

### Step 1.2: Token 缓存检查与分层续期

```bash
TOKEN_CACHE=~/.openclaw/workspace/scripts/.token-cache.json
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"

if [ -f "$TOKEN_CACHE" ]; then
    API_TOKEN=$(jq -r '.token' "$TOKEN_CACHE")
    expires_at=$(jq -r '.expires_at' "$TOKEN_CACHE")
    EMPLOYEE_ID=$(jq -r '.employee_id' "$TOKEN_CACHE")
    EMPLOYEE_NAME=$(jq -r '.employee_name' "$TOKEN_CACHE")

    # AI 从用户输入中解析出新账号时，若与缓存不一致则清除缓存并提示重新登录
    if [ -n "${INPUT_EMPLOYEE_ID:-}" ] && [ "$INPUT_EMPLOYEE_ID" != "$EMPLOYEE_ID" ]; then
        rm -f "$TOKEN_CACHE"
        echo "🔑 检测到账号切换，请重新输入密码"
        echo "（等待用户输入密码...）"
        # AI 从用户回复中提取 password

        response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
          -H "Content-Type: application/json" \
          -d "{\"employee_id\": \"${INPUT_EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
          --max-time 120)
        code=$(echo "$response" | jq -r '.code')
        if [ "$code" = "0" ]; then
            API_TOKEN=$(echo "$response" | jq -r '.data.token')
            new_expires=$(echo "$response" | jq -r '.data.expires_at')
            employee_name=$(echo "$response" | jq -r '.data.employee_name')
            EMPLOYEE_ID="$INPUT_EMPLOYEE_ID"
            EMPLOYEE_NAME="$employee_name"
            mkdir -p ~/.openclaw/workspace/scripts
            echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
        else
            error_message=$(echo "$response" | jq -r '.message')
            echo "⚠️ 登录失败：$error_message"
            echo "建议：确认账号和密码正确"
            exit 1
        fi
    fi

    if [ -n "$expires_at" ] && [ "$expires_at" != "null" ]; then
        expires_timestamp=$(to_timestamp "$expires_at")
        current_ts=$(now_ts)
        days_remaining=$(( (expires_timestamp - current_ts) / 86400 ))

        if [ $days_remaining -le 0 ]; then
            # Token 已过期 → 引导用户重新输入账号密码登录
            echo "⚠️ Token 已过期，请重新登录"
            echo "请输入您的账号和密码，格式：账号 密码"
            echo "（等待用户输入...）"

            response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
              -H "Content-Type: application/json" \
              -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
              --max-time 120)
            code=$(echo "$response" | jq -r '.code')
            if [ "$code" = "0" ]; then
                API_TOKEN=$(echo "$response" | jq -r '.data.token')
                new_expires=$(echo "$response" | jq -r '.data.expires_at')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                echo "⚠️ 登录失败，请确认账号和密码正确"
                exit 1
            fi
        elif [ $days_remaining -le 7 ]; then
            # Token 即将过期 → renew-token 优先
            response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/renew-token" \
              -H "Authorization: Bearer ${API_TOKEN}" \
              --max-time 120)
            code=$(echo "$response" | jq -r '.code')
            if [ "$code" = "0" ]; then
                API_TOKEN=$(echo "$response" | jq -r '.data.token')
                new_expires=$(echo "$response" | jq -r '.data.expires_at')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                # renew 失败 → 引导用户重新输入密码登录
                echo "⚠️ Token 续期失败，请重新输入密码"
                echo "（等待用户输入密码...）"

                response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
                  -H "Content-Type: application/json" \
                  -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
                  --max-time 120)
                code=$(echo "$response" | jq -r '.code')
                if [ "$code" = "0" ]; then
                    API_TOKEN=$(echo "$response" | jq -r '.data.token')
                    new_expires=$(echo "$response" | jq -r '.data.expires_at')
                    echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
                else
                    echo "⚠️ 登录失败，请确认账号和密码正确"
                    exit 1
                fi
            fi
        fi
        # else: Token 仍有效，直接使用
    fi
else
    # 缓存文件不存在 → 引导用户输入账号和密码
    echo "🔑 需要验证您的员工身份"
    echo ""
    echo "请输入您的账号和密码，格式：账号 密码"
    echo "例如：emp-server-106 123456"
fi

# ═══ Token 校验兜底：确保 Token 有效，否则提示用户重新登录 ═══
if [ -z "${API_TOKEN:-}" ] || [ "$API_TOKEN" = "null" ] || [ "$API_TOKEN" = "" ]; then
    echo "⚠️ 身份验证失败，无法获取有效凭证"
    echo ""
    echo "请输入您的账号和密码，重新登录："
    echo "格式：账号 密码（例如：emp-server-106 123456）"
    # AI 引导用户输入后，重新执行 /auth/login 流程
fi
```

> **关键**: 员工身份（`employee_code`）由后端从 Token 自动提取，Skill 不需要在 payload 中传递。
> **关键**: 项目名称（`project_name`）由 AI 从对话中识别或用户指定，如未识别则使用 `company_name` 作为默认值。

---

## Step 2: 解析意图（语义理解）

从用户输入中提取以下信息，**由 AI 自行判断，无需正则或关键词表**：

| 提取项 | 说明 | 示例 |
|--------|------|------|
| `company_name` | 用户提到的公司/客户名称 | "陌陌科技"、"数智云创" |
| `contact_name` | 用户提到的联系人姓名 | "张三"、"李总" |
| `project_name` | 用户提到的项目/系统/产品名 | "CRM项目"、"数据中台" |
| `title_keywords` | 用于文件匹配的主题关键词 | "价格谈判"、"方案对比" |
| `source_type` | 数据源类型 | `phone` / `wechat` / `auto` |

**提取原则**：
- 从用户原话中直接提取，不做过度推断
- 提取不到就留空，后续步骤有兜底逻辑
- 不要因为没匹配到某个模式就认为"无法识别"

**数据源判断**：
- 提到"电话/录音/通话/拜访" → `phone`
- 提到"微信/聊天/消息" → `wechat`
- 未明确 → `auto`（两个源都查）

**客户标识优先级**：
1. `company_name`（公司全称或简称，用户明确提到）→ 直接进入 Step 4
2. 无公司名但有 `contact_name` → 进入 Step 3 客户确认
3. 都没有但有 `title_keywords` → 用主题关键词匹配文件名，进入 Step 3 客户确认
4. 都没有 → 提示用户补充信息（见下方引导模板）

**信息不足时的引导提示**：

当用户输入过于笼统（如"整理线索"、"跟进记录"、"分析录音"），无法提取客户名或联系人时，**不要猜测**，主动引导用户补充：

```
请告诉我您想分析的内容，例如：

• "分析我和陌陌公司的通话录音"
• "查看我和张三的微信聊天记录"
• "总结上周拜访客户的录音"
• "分析CRM项目的沟通记录"

需要指定：客户名称 或 联系人姓名，我会帮您分析拜访记录并生成项目画像。
```

**项目名称优先级**：
1. 用户明确指定（最高优先级）
2. AI 在 Step 5 分析时从对话内容自动识别
3. 默认使用 `company_name`

---

## Step 3: 客户确认（公司名不明确时）

当 Step 2 未能明确识别 `company_name`（只有 `contact_name` 或 `title_keywords`）时，**先查询数据库已有客户**，让员工确认或选择，避免用错误名称创建新客户。

### 判断条件

| 条件 | 动作 |
|------|------|
| `company_name` 已明确（用户直接提到公司名） | **跳过此步**，直接进入 Step 4 |
| 仅有 `contact_name` 或 `title_keywords` | **执行客户查询**，让员工确认 |

### 查询已有客户

```bash
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"

customers_response=$(curl -s -X GET "${FASTAPI_BASE_URL}/project-portrait/customers" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  --max-time 10)

customers_code=$(echo "$customers_response" | jq -r '.code')

if [ "$customers_code" = "0" ]; then
    customers=$(echo "$customers_response" | jq -r '.data')
    customer_count=$(echo "$customers" | jq 'length')
fi
```

### 匹配与展示逻辑

```
1. 用 contact_name / title_keywords 在客户列表中模糊匹配
   - 匹配 company_name 字段
   - 匹配 contact_name 字段

2. 匹配结果分支：
   ├─ 精确匹配到 1 个客户 → 自动使用该客户的 company_name（静默确认）
   ├─ 匹配到多个客户 → 展示列表让员工选择
   ├─ 无匹配 → 询问员工输入企业全称
   └─ 客户列表为空（新员工）→ 询问员工输入企业全称
```

### 多客户匹配时的展示格式

```
📋 找到以下相关客户，请选择要分析的客户：

1. XX科技有限公司（联系人：王厂长）
2. XX智能装备集团（联系人：王建国）
3. XX电子有限公司（联系人：王总）

请回复序号选择，或输入新的企业名称。
```

### 无匹配时的引导格式

```
📋 未在您的客户库中找到与「{contact_name}」匹配的企业。

请输入该客户的**企业全称**（如：深圳市XX科技有限公司），我将以此创建新客户档案。
```

### 确认后

员工确认 `company_name` 后，后续 Step 4-7 使用该确认值，确保数据准确。

---

## Step 4: 查找并读取聊天内容（多源分支）

根据 Step 2 解析出的 `source_type` 走不同分支：

| source_type | 走哪条路径 | 说明 |
|-------------|----------|------|
| `phone`   | 分支 A：电话录音转录 | 用户明确提到"电话/录音/通话" |
| `wechat`  | 分支 B：微信聊天记录 | 用户明确提到"微信/聊天记录" |
| `auto`    | 两个分支都执行，合并结果 | 用户未指定来源 |

---

### 分支 A：电话录音转录

#### A.1 转录文件存储路径

```
/home/admin/.openclaw/plugins/phone-notifications/recordings/transcripts/
```

> **性能约束**：该目录可能有数百甚至上千个转录文件，**禁止全量 grep**。必须采用"分层过滤"策略逐步缩小范围。

#### A.2 文件名格式

`{UUID}_{AI生成的标题}.md`（UUID 固定 36 字符，标题为 AI 从对话内容总结的主题，**不含时间信息**）

示例：
```
611a199a-1fcd-4604-85c6-774bd7160784_哒，开始了，嗯，可以.md
8bc14a02-29e3-4bd6-986a-faa69a8bb929_CRM方案价格相对比及商务谈判进展.md
```

#### A.3 分层过滤策略（4 级缩小范围）

#### 第 1 级：限定时间范围（必做，最高效）

默认只看最近 30 天内的文件（按文件修改时间）。如果用户明确提到"上个月"/"最近一周"，则按用户指定的范围过滤。

```bash
TRANSCRIPTS_DIR="/home/admin/.openclaw/plugins/phone-notifications/recordings/transcripts"
DAYS_BACK="${DAYS_BACK:-30}"  # 默认 30 天

# 用 find 按 mtime 过滤，只列出时间范围内的 .md 文件
recent_files=$(find "$TRANSCRIPTS_DIR" -maxdepth 1 -name "*.md" -type f -mtime -${DAYS_BACK} 2>/dev/null)

if [ -z "$recent_files" ]; then
    echo "⚠️ 最近 ${DAYS_BACK} 天内没有转录文件"
    echo "尝试扩大范围到 90 天..."
    DAYS_BACK=90
    recent_files=$(find "$TRANSCRIPTS_DIR" -maxdepth 1 -name "*.md" -type f -mtime -${DAYS_BACK} 2>/dev/null)
fi

if [ -z "$recent_files" ]; then
    echo "⚠️ 90 天内仍无转录文件，请确认录音是否已转录"
    exit 1
fi

total_count=$(echo "$recent_files" | wc -l)
echo "📂 最近 ${DAYS_BACK} 天内有 ${total_count} 个转录文件"
```

#### 第 2 级：优先按文件名标题部分匹配（零开销，命中率高）

文件名中 UUID 后面是 AI 生成的标题，**标题通常包含客户名、产品名、场景关键词**，命中率很高。先用 `basename` 提取标题部分做字符串匹配（不读文件内容，开销为 0）：

```bash
# 提取标题部分（跳过 UUID 前缀，匹配 UUID 后的内容）
# 文件名格式：{UUID}_{标题}.md，UUID 固定 36 字符
name_matched=""
# 按优先级尝试匹配：公司名 → 联系人 → 主题关键词
keywords=()
[ -n "$company_name" ] && keywords+=("$company_name")
[ -n "$contact_name" ] && keywords+=("$contact_name")
# 主题关键词数组（来自 Step 2）
for kw in "${title_keywords[@]}"; do keywords+=("$kw"); done

for kw in "${keywords[@]}"; do
    name_matched=$(echo "$recent_files" | while read f; do
        title_part=$(basename "$f" .md | cut -c38-)
        echo "$title_part" | grep -qi "$kw" && echo "$f"
    done)
    [ -n "$name_matched" ] && break
done

if [ -n "$name_matched" ]; then
    matched_files="$name_matched"
    echo "✅ 文件名标题命中"
else
    # 进入第 3 级
fi
```

#### 第 3 级：小范围内容匹配（只在第 1 级过滤后的文件上做 grep）

**只有第 2 级没命中时**，才对第 1 级筛选出来的小集合做内容 grep，**绝不对整个目录 grep**：

```bash
# 只在 recent_files 上做 grep（而不是 *.md 全量）
keyword="${company_name:-$contact_name}"
matched_files=$(echo "$recent_files" | xargs grep -l -i "$keyword" 2>/dev/null)

if [ -z "$matched_files" ]; then
    echo "⚠️ 未匹配到包含「${keyword}」的转录文件"
    echo ""
    echo "📋 最近 ${DAYS_BACK} 天最新 10 个文件："
    echo "$recent_files" | xargs ls -lt 2>/dev/null | head -10 | while read line; do
        filename=$(echo "$line" | awk '{print $NF}')
        echo "  - $(basename $filename)"
    done
    echo ""
    echo "请回复文件名、具体日期或更多关键词（如客户提到的产品名）"
    exit 1
fi
```

#### 第 4 级：取最新一条（多条匹配时）

```bash
# 多条匹配时按 mtime 排序，取最新的
target_file=$(echo "$matched_files" | xargs ls -t 2>/dev/null | head -1)
echo "📄 匹配到文件：$(basename $target_file)"
```

#### A.4 读取聊天内容

```bash
chat_content=$(cat "$target_file")
```

#### A.5 转录文件格式（电话录音转录）

```markdown
# CRM方案价格对比及商务谈判进展

> 录音名称：2026_06_10 17:04:10
> 时长：02:10
> 创建时间：2026-06-10T09:04:10.570Z

---

说话人0：李总，您好！感谢您抽出时间。上次给您发的CRM方案...
```

**关键特征**:
- **标题**：自动生成（主题概括）
- **元数据**：`录音名称`（含日期）、`时长`、`创建时间`
- **对话**：只有 `说话人0` 标识，包含双方对话内容（无角色分离）

**Skill 自动识别并提取**：
- **通话日期**：优先从 `录音名称` 行提取 `YYYY_MM_DD`，备选从 `创建时间` 提取 ISO 格式
- **完整对话**：`说话人0` 后的全部内容
- AI 分析时从上下文推断销售和客户角色

---

### 分支 B：微信聊天记录

#### B.1 微信通知存储路径

```
/home/admin/.openclaw/plugins/phone-notifications/notifications/
```

该目录下所有文件是**按日期命名**的 JSON 数组，每个文件记录当天所有 App 推送通知：

```
notifications/
├── 2026-06-04.json
├── 2026-06-05.json
├── 2026-06-06.json
├── ...
└── 2026-06-10.json
```

#### B.2 文件结构（JSON 数组，每条是一个推送通知）

```json
[
  {
    "appName": "微信",
    "title": "销售伴侣",
    "content": "吴云成: http://118.196.83.38/ai/salebp/-/tree/develop",
    "timestamp": "2026-06-09T17:13:42+08:00",
    "appDisplayName": "微信"
  },
  {
    "appName": "微信",
    "title": "沈莹玉",
    "content": "。。。刚看到，晚上中兴加班的",
    "timestamp": "2026-06-09T21:16:29+08:00",
    "appDisplayName": "微信"
  },
  {
    "appName": "钉钉",
    "title": "工作通知:南京绛门信息科技有限公司",
    "content": "考勤打卡：18:00 极速打卡·成功",
    "timestamp": "2026-06-09T18:00:21+08:00",
    "appDisplayName": "钉钉"
  }
]
```

**字段含义**：
| 字段 | 含义 | 示例 |
|------|------|------|
| `appName` | 应用包名标识 | `"微信"` / `"钉钉"` / `"菜鸟"` |
| `title` | 聊天对象名/群名（微信场景） | `"沈莹玉"` / `"销售伴侣群"` |
| `content` | 单条消息内容 | `"。。。刚看到，晚上中兴加班的"` |
| `timestamp` | 精确时间戳（带时区） | `"2026-06-09T21:16:29+08:00"` |
| `appDisplayName` | 应用显示名 | `"微信"` |

#### B.3 微信过滤策略（3 级）

```bash
NOTIFICATIONS_DIR="/home/admin/.openclaw/plugins/phone-notifications/notifications"
DAYS_BACK="${DAYS_BACK:-30}"

# 第 1 级：按文件名日期过滤（文件名是 YYYY-MM-DD.json，零成本）
recent_json_files=$(find "$NOTIFICATIONS_DIR" -maxdepth 1 -name "*.json" -type f -mtime -${DAYS_BACK} 2>/dev/null)

if [ -z "$recent_json_files" ]; then
    echo "⚠️ 最近 ${DAYS_BACK} 天内没有通知文件"
    exit 1
fi

# 第 2 级：用 jq 筛选 appName=="微信" 的记录，并按 title 匹配联系人
wechat_messages=$(echo "$recent_json_files" | xargs jq -s '
    [ .[][] | select(.appName == "微信") ]
' 2>/dev/null)

# 第 3 级：按 title（联系人/群名）过滤
if [ -n "$contact_name" ]; then
    wechat_messages=$(echo "$wechat_messages" | jq --arg name "$contact_name" '
        [ .[] | select(.title | test($name; "i")) ]
    ')
elif [ -n "$company_name" ]; then
    wechat_messages=$(echo "$wechat_messages" | jq --arg name "$company_name" '
        [ .[] | select(.title | test($name; "i")) ]
    ')
fi

msg_count=$(echo "$wechat_messages" | jq 'length')
if [ "$msg_count" -eq 0 ]; then
    echo "⚠️ 未找到与「${contact_name:-$company_name}」相关的微信聊天记录"
    echo ""
    echo "📋 最近 ${DAYS_BACK} 天微信联系人统计："
    echo "$wechat_messages" | jq -r '[ .[].title ] | group_by(.) | map({name: .[0], count: length}) | sort_by(-.count) | .[:10][] | "  - \(.name) (\(.count) 条)"'
    exit 1
fi

echo "✅ 找到 ${msg_count} 条与「${contact_name:-$company_name}」的微信消息"
```

#### B.4 聚合消息为对话格式（供 AI 分析）

把同一联系人的多条消息按时间排序，拼接为对话格式（类似录音转录）：

```bash
chat_content=$(echo "$wechat_messages" | jq -r '
    sort_by(.timestamp) |
    .[] |
    "[\(.timestamp | split("T")[1] | split("+")[0])] \(.title): \(.content)"
')

# 提取最早消息日期作为 visit_date
visit_date=$(echo "$wechat_messages" | jq -r '
    sort_by(.timestamp) | .[0].timestamp | split("T")[0]
')

# 设置 transcript_file_path 为虚拟路径（表明数据源）
transcript_file_path="wechat://${contact_name:-$company_name}/${visit_date}"
```

聚合后的 `chat_content` 示例：
```
[21:16:29] 沈莹玉: 。。。刚看到，晚上中兴加班的
[21:17:14] 沈莹玉: 晚上吧
[21:17:22] 沈莹玉: 明晚
```

#### B.5 微信 vs 电话录音差异

| 维度 | 电话录音 | 微信聊天 |
|------|---------|---------|
| 粒度 | 一次通话=一个文件 | 单条消息，需聚合 |
| 角色分离 | 无（全在 `说话人0`） | 仅我方收到的消息（`title`=对方） |
| 时间信息 | 需从内容提取 | `timestamp` 字段直接可用 |
| 完整性 | 完整对话 | 仅通知栏内容（撤回/图片/语音可能缺失） |
| 虚拟路径 | 真实文件路径 | `wechat://{联系人}/{日期}` |

---

## Step 5: AI 分析聊天转录内容（核心）

### 分析提示词模板

```markdown
# 角色
你是资深 B2B 销售分析师，精通 LTC（Lead to Cash）销售流程。

# 任务
根据以下拜访沟通记录，分析生成项目画像的 5 大模块数据，并**识别项目名称**。

# 输入数据
- 公司名称：{company_name}（优先）
- 联系人：{contact_name}（备选）
- 项目名称：{project_name}（如已提取）
- 聊天文件：{target_file}
- 聊天内容：{chat_content}

# 输出要求（严格 JSON 格式）

{
  "project_name": "识别出的项目名称（如CRM系统采购、数据中台建设等）",
  "sales_stage": {
    "steps": [
      {"label": "线索", "active": false},
      {"label": "商机确认", "active": false},
      {"label": "方案评估", "active": false},
      {"label": "商务谈判", "active": false},
      {"label": "赢单/关单", "active": false}
    ],
    "progress_percent": 60,
    "current_stage": "方案评估",
    "description": "基于沟通记录，客户已明确需求并进入方案对比阶段..."
  },
  "follow_up_strategies": [
    {
      "icon": "fa-calendar-check",
      "title": "跟进策略标题",
      "description": "具体跟进动作描述",
      "tag_icon": "fa-tag",
      "tag_text": "策略标签"
    }
  ],
  "customer_insights": [
    {"title": "客户意向", "content": "..."},
    {"title": "项目新增线索", "content": "..."},
    {"title": "客户关注点", "content": "..."},
    {"title": "个人诉求", "content": "..."}
  ],
  "commitments": [
    {
      "type": "our_promise",
      "type_label": "我方承诺",
      "content": "承诺内容",
      "meta": "责任人/时间"
    },
    {
      "type": "customer_promise",
      "type_label": "客户承诺",
      "content": "客户承诺内容",
      "meta": "客户方责任人"
    }
  ],
  "risk_assessment": [
    {"title": "影响项目推进信息", "content": "...", "level": "high"},
    {"title": "影响价格谈判信息", "content": "...", "level": "medium"},
    {"title": "影响成单信息", "content": "...", "level": "low"},
    {"title": "竞品相关信息", "content": "...", "level": "medium"}
  ],
  "visit_summary": "本次拜访的核心总结（100字以内）"
}

# 分析维度说明

## 0. 项目名称识别（新增）
从对话内容中识别项目名称，常见特征：
- 明确提及："关于你们的**CRM系统项目**"、"**数据中台建设**的进展"
- 项目代号："**凤凰计划**"、"**星辰工程**"
- 产品/系统名："**销售管理系统**"、"**客户数据平台**"
- 如无法识别，返回空字符串 ""（后端将使用 company_name 作为默认值）

## 1. 销售阶段（基于 LTC 流程）
- 线索：初次接触，尚未明确需求
- 商机确认：需求明确，确认有采购意向
- 方案评估：客户对比多家方案，进入评估阶段
- 商务谈判：方案已认可，进入价格/条款谈判
- 赢单/关单：合同签订或项目关闭
根据沟通记录判断当前阶段，设置 active=true，progress_percent 对应 20/40/60/80/100。

## 2. 跟进策略（4个维度，至少 3 条）
(1) 当前销售阶段 → 下一阶段的推进动作
(2) 既往/本次承诺事项 → 需要跟进的兑现动作
(3) 项目风险 → 需要化解风险的跟进动作
(4) 客户最新动态/意向 → 需要抓住机会的跟进动作

## 3. 客户洞察（至少 3 条）
- 客户意向、项目新增线索、客户关注点、个人诉求

## 4. 承诺事项（识别所有承诺）
- our_promise：我方承诺（如"下周提供方案"、"月底前给报价"）
- customer_promise：客户承诺（如"下周内部讨论"、"月底给答复"）
- customer_request：客户要求（如"希望增加某功能"、"要求降价"）

## 5. 风险预估
- 从沟通记录中识别所有潜在风险，不限于固定类别
- 每条风险标注等级：`high` / `medium` / `low`
- **由 AI 根据对话内容自行判断等级**，不要套用固定规则：
  - 如果客户明确表示不合作、项目暂停、预算砍掉 → `high`
  - 如果客户有顾虑、需要额外审批、竞品介入 → `medium`
  - 如果只是常规提醒、轻微分歧 → `low`
- 没有明显风险时，输出空数组 `[]`

# 重要规则
1. 所有分析必须基于实际沟通记录，绝不编造
2. 如果某维度无相关信息，输出空数组 []
3. description 和 content 要具体、可执行，不要泛泛而谈
4. 使用中文输出
```

### 提取日期（用于 `visit_date`）

```bash
# 优先从"录音名称"行提取 YYYY_MM_DD
visit_date=$(echo "$chat_content" | grep "录音名称" | grep -oE '[0-9]{4}_[0-9]{2}_[0-9]{2}' | tr '_' '-' | head -1)

if [ -z "$visit_date" ]; then
    # 备选：从"创建时间"行提取 ISO 格式
    visit_date=$(echo "$chat_content" | grep "创建时间" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
fi

if [ -z "$visit_date" ]; then
    # 兜底：文件修改时间
    visit_date=$(date +%Y-%m-%d)
fi
```

---

## Step 6: 保存项目画像

### 请求地址

| 项 | 说明 |
|---|---|
| URL | `POST ${FASTAPI_BASE_URL}/project-portrait/ingest` |
| 认证 | `Authorization: Bearer ${API_TOKEN}`（员工 Token） |
| Content-Type | `application/json` |

### 请求参数

```json
{
  "company_name": "string (必填，公司名优先；无公司名时传联系人)",
  "project_name": "string (可选，项目名称；AI识别或用户指定，为空时后端使用 company_name)",
  "contact_name": "string (可选，联系人姓名)",
  "transcript_file_path": "string (可选，电话录音为真实文件路径；微信为虚拟路径 wechat://{联系人}/{日期})",
  "visit_date": "string (YYYY-MM-DD)",
  "data_source": "string (电话录音转录 | 微信聊天记录)",
  "sales_stage": {
    "steps": [{"label": "线索", "active": false}, ...],
    "progress_percent": 60,
    "current_stage": "方案评估",
    "description": "..."
  },
  "follow_up_strategies": [
    {"icon": "", "title": "", "description": "", "tag_icon": "", "tag_text": ""}
  ],
  "customer_insights": [
    {"title": "", "content": ""}
  ],
  "commitments": [
    {"type": "our_promise|customer_promise|customer_request", "type_label": "", "content": "", "meta": ""}
  ],
  "risk_assessment": [
    {"title": "", "content": "", "level": "low"}
  ],
  "raw_analysis": "string (可选，AI 原始返回)",
  "visit_summary": "string (可选，100字以内总结)"
}
```

### 响应格式

```json
{
  "code": 0,
  "data": {
    "portrait_id": 123,
    "ingested": true
  },
  "message": "ok"
}
```

### 执行脚本

```bash
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"

INGEST_PAYLOAD=$(jq -n \
  --arg company_name "$company_name" \
  --arg project_name "${project_name:-}" \
  --arg contact_name "${contact_name:-}" \
  --arg transcript_file_path "$target_file" \
  --arg visit_date "$visit_date" \
  --arg data_source "电话录音转录" \
  --argjson sales_stage "$(echo "$parsed_result" | jq '.sales_stage')" \
  --argjson follow_up_strategies "$(echo "$parsed_result" | jq '.follow_up_strategies')" \
  --argjson customer_insights "$(echo "$parsed_result" | jq '.customer_insights')" \
  --argjson commitments "$(echo "$parsed_result" | jq '.commitments')" \
  --argjson risk_assessment "$(echo "$parsed_result" | jq '.risk_assessment')" \
  --arg raw_analysis "$(echo "$parsed_result" | jq -r '.' | head -c 10000)" \
  --arg visit_summary "$(echo "$parsed_result" | jq -r '.visit_summary')" \
  '{
    company_name: $company_name,
    project_name: $project_name,
    contact_name: $contact_name,
    transcript_file_path: $transcript_file_path,
    visit_date: $visit_date,
    data_source: $data_source,
    sales_stage: $sales_stage,
    follow_up_strategies: $follow_up_strategies,
    customer_insights: $customer_insights,
    commitments: $commitments,
    risk_assessment: $risk_assessment,
    raw_analysis: $raw_analysis,
    visit_summary: $visit_summary
  }')

ingest_response=$(curl -s -X POST "${FASTAPI_BASE_URL}/project-portrait/ingest" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -d "$INGEST_PAYLOAD" \
  --max-time 30)

ingest_code=$(echo "$ingest_response" | jq -r '.code')

if [ "$ingest_code" = "0" ]; then
    echo "✅ 项目画像已生成"
    PORTRAIT_ID=$(echo "$ingest_response" | jq -r '.data.portrait_id')
else
    echo "⚠️ 生成失败：$(echo "$ingest_response" | jq -r '.message')"
    mkdir -p /tmp/sales-companion-fallback
    echo "$INGEST_PAYLOAD" > "/tmp/sales-companion-fallback/portrait_$(date +%s).json"
    exit 1
fi
```

### 后端自动处理（无需 Skill 感知）

请求被处理后，系统会自动完成：

1. 自动关联或创建客户信息
2. 建立员工与客户的归属关系
3. 增量更新或首次创建项目画像
4. 返回画像 ID

> **数据隔离**：`employee_code + company_name + project_name` 联合确定唯一画像。同一公司同一项目，员工 A 和员工 B 的画像互相隔离，互不可见。同一公司不同项目，画像也互相独立。

---

## Step 7: 输出摘要 + H5 链接

### 生成 H5 链接（优先换码，兜底完整 Token）

```bash
exchange_response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/exchange-code" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}' \
  --max-time 10)

exchange_code=$(echo "$exchange_response" | jq -r '.data.code // empty')

H5_BASE_URL="http://47.116.49.218:5173"

if [ -n "$exchange_code" ] && [ "$exchange_code" != "null" ]; then
    h5_url="${H5_BASE_URL}/project-portrait-new/${PORTRAIT_ID}?code=${exchange_code}"
else
    # 兜底：使用完整 Token（禁止截断、禁止带 ...）
    h5_url="${H5_BASE_URL}/project-portrait-new/${PORTRAIT_ID}?token=${API_TOKEN}"
fi
```

### 输出格式

```markdown
📊 {company_name} · {project_name} · 项目画像分析

📅 聊天日期：{visit_date}
📱 数据源：{data_source}  ← "电话录音转录" 或 "微信聊天记录"
👤 联系人：{contact_name}
📍 当前阶段：{sales_stage.current_stage}（进度 {sales_stage.progress_percent}%）

🎯 核心总结：{visit_summary}

📈 [查看完整项目画像 →]({h5_url})

────────────────────────────────────────

💡 **下一步行动建议**

分析完成后，建议将此项目同步到 CRM 管理系统，方便后续跟进和团队协作。

🔄 [同步到 CRM 管理 →] 对我说"同步到CRM"

────────────────────────────────────────

🔒 数据隔离：此分析记录属于员工 {employee_code}，项目 {project_name}
```

---



---

## 数据库 Schema（参考）

### project_portraits 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 画像 ID（URL 中使用） |
| employee_code | VARCHAR INDEX | 员工号（数据隔离键） |
| company_name | VARCHAR INDEX | 公司名称 |
| project_name | VARCHAR INDEX | 项目名称（数据隔离键：employee_code + company_name + project_name） |
| contact_name | VARCHAR | 联系人 |
| transcript_file_path | VARCHAR | 转录文件路径 |
| visit_date | VARCHAR | 聊天日期 |
| data_source | VARCHAR | 数据来源 |
| sales_stage | JSON TEXT | 销售阶段 |
| follow_up_strategies | JSON TEXT | 跟进策略（列表） |
| customer_insights | JSON TEXT | 客户洞察（列表） |
| commitments | JSON TEXT | 承诺事项（列表） |
| risk_assessment | JSON TEXT | 风险预估（列表） |
| raw_analysis | TEXT | AI 原始返回 |
| visit_summary | TEXT | 拜访总结 |
| created_at / updated_at | DATETIME | 时间戳 |

### customers 表 & employee_customers 表

`ingest` 接口会自动维护这两张表，Skill 无需感知。

---

## 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| 无匹配客户 | 输出相似客户列表，让用户选择 |
| 无拜访记录 | 提示录入拜访沟通内容 |
| 拜访记录无沟通内容 | 提示补充对话记录 |
| AI 分析失败 | 提示"分析失败，请重试" |
| 保存失败 | 兜底写入 `/tmp/sales-companion-fallback/`，提示联系管理员 |
| Token 过期或失效 | 自动续期；续期失败则提示用户输入账号和密码重新登录 |

---

## 使用示例

### 示例 1：电话录音分析

```
用户：查看我和陌陌公司CRM项目的聊天分析

输出：
📊 陌陌公司 · CRM项目 · 项目画像分析

📅 聊天日期：2026-06-10
� 数据源：电话录音转录
� 联系人：李总
📍 当前阶段：方案评估（进度 60%）

🎯 核心总结：客户已明确需求，正在对比 3 家方案，对我方技术方案认可度高，但价格敏感...

📈 [查看完整项目画像 →]({h5_url})

────────────────────────────────────────

💡 **下一步行动建议**

分析完成后，建议将此项目同步到 CRM 管理系统，方便后续跟进和团队协作。

�🔄 [同步到 CRM 管理 →] 对我说"同步到CRM"

────────────────────────────────────────

🔒 数据隔离：此分析记录属于员工 E10001，项目 CRM项目
```

### 示例 2：微信聊天分析

```
用户：查看我和沈莹玉的微信聊天记录

输出：
📊 沈莹玉 · Mochac 科技 · 项目画像分析

📅 聊天日期：2026-06-09
📱 数据源：微信聊天记录
👤 联系人：沈莹玉
📍 当前阶段：商机确认（进度 40%）

🎯 核心总结：客户对方案表现出兴趣，但提及晚上加班，时间紧张...

📈 [查看完整项目画像 →]({h5_url})

────────────────────────────────────────

💡 **下一步行动建议**

分析完成后，建议将此项目同步到 CRM 管理系统，方便后续跟进和团队协作。

🔄 [同步到 CRM 管理 →] 对我说"同步到CRM"

────────────────────────────────────────
```

---

## 与 employee-radar 的区别

| 对比项 | employee-radar | visit-analyzer |
|--------|---------------|----------------|
| 数据来源 | 公域（官网/公众号/招投标/招聘） | 私域（拜访沟通记录） |
| 分析对象 | 企业整体情报 | 具体项目/拜访 |
| 输出内容 | 客户画像 + 企业动态 + AI商机 | 销售阶段 + 跟进策略 + 客户洞察 + 承诺事项 + 风险预估 |
| H5 路由 | `/intelligence-radar/{companyId}` | `/project-portrait-new/{portraitId}` |
| 触发场景 | "查询XX公司情报" | "查看我和XX的聊天分析" |
| 生成方式 | 查询缓存 → 触发采集 | 直接生成画像（自动创建客户） |
| 数据隔离 | 企业级 | **员工+项目级**（`employee_code + company_name + project_name`） |

---

## 变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-10 | 新建 visit-analyzer Skill，实现拜访记录 AI 分析 |
| v1.1 | 2026-06-10 | 工作流从 10 步简化为 6 步，删除 Customer/Visit 手动创建逻辑 |
| v1.2 | 2026-06-10 | 彻底移除 visits 表相关描述；明确 visits 表已删除，改用 transcript_file_path 引用原始录音；明确 ingest 接口自动创建 Customer + EmployeeCustomer；补充数据隔离说明（employee_code + company_name）；更新 API Schema 和 H5 链接格式 |
| v1.3 | 2026-06-10 | Step 3 文件匹配策略从"全量 grep"优化为"4 级分层过滤"（时间范围 find → 文件名匹配 → 小范围内容 grep → 取最新），避免在数千文件上全量扫描 |
| v1.4 | 2026-06-10 | 明确实际文件名格式 `{UUID}_{AI标题}.md`（无时间信息，标题为 AI 生成）；Step 2 新增 `title_keywords` 主题关键词提取（CRM/方案/价格/谈判等）；Step 3 第 2 级改为提取 UUID 后的标题部分匹配，按 company_name → contact_name → title_keywords 优先级尝试，提升命中率 |
| v1.5 | 2026-06-10 | **新增微信聊天记录数据源**：Step 2 新增 `source_type` 判断（wechat/phone/auto）；Step 3 重构为多源分支（A 电话录音 / B 微信通知 JSON）；微信源使用 `jq` 按 appName+title 过滤，聚合同联系人多消息为对话格式；`data_source` 支持"微信聊天记录"，`transcript_file_path` 使用虚拟路径 `wechat://{联系人}/{日期}`；新增示例 4/5（微信场景和自动合并） |
| v1.6 | 2026-06-11 | **意图解析从规则引擎改为语义理解**：删除 Step 2 的正则伪代码和硬编码关键词表，改为 AI 自行判断；5 个详细示例精简为 2 个（电话录音 + 微信聊天），只展示输出格式不展示内部步骤流转；删除两个重复的"性能对比"表；输出格式新增"同步到 CRM"引导提示 |
| v1.7 | 2026-06-13 | **新增客户确认步骤（Step 3）**：工作流从 6 步升级为 7 步；当 Step 2 未明确识别 `company_name` 时，调用 `GET /project-portrait/customers` 查询员工已有客户列表，模糊匹配后展示给员工选择或输入新企业名；避免用错误名称创建新客户产生脏数据；客户标识优先级更新，仅 `contact_name`/`title_keywords` 时进入客户确认而非直接回退 |
