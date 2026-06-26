---
name: ziwei-doushu-advisor
description: 为大模型提供命理运势分析时需要的排盘数据
homepage: https://skill.myfate.ai
metadata: {"clawdbot":{"emoji":"🌤️","requires":{"bins":["curl"]}}}
---

# 紫微斗数命理分析工具 (Ziwei Doushu: AI Destiny Advisor)

紫微斗数排盘专业工具由myfate ai提供，为用户提供精准、深入且全面的命理排盘服务。需访问homepage注册后获取API KEY，每日赠送免费调用次数。

工具使用需要 env中有环境变量: `MYFATE_AI_API_KEY`.

## 🧰 可用工具指引

### 🔑 API 鉴权配置
在调用 API 时，必须在 HTTP Header 中携带 API Key，支持以下两种方式：
- **Header 1**: `x-api-key: MYFATE_AI_API_KEY`
- **Header 2**: `Authorization: Bearer MYFATE_AI_API_KEY`

### 基础排盘参数（通用）
除了 `lunar_to_solar`，其他排盘接口均包含以下通用参数：
- **`birthDate`** (string, 必填): 阳历出生日期，格式 `YYYY-MM-DD HH:mm:ss`。农历需先转换。
- **`gender`** (string, 必填): 性别 (`男`/`女` 或 `male`/`female`)。
- **`fixLeap`** (number, 选填): 是否修正闰月 (-1:上月, 0:中分, 1:下月)。默认 0。
- **`dayDivide`** (string, 选填): 日分模式 (`current`:晚子当日, `forward`:晚子来日)。
- **`liunianSihuaMode`** (string, 选填): 流年四化模式 (`""`:按天干, `"minggong"`:按流命天干)。

---

### 工具调用通用 CURL 示例

所有工具的调用方式均采用 HTTP POST 请求，下面是一个通用的 CURL 调用示例。在实际调用时，请将 URL 中的 `TOOL_NAME` 替换为具体的工具名称，并在 `-d` 的 JSON 中传入该工具所需的参数：

```bash
curl -X POST https://skill.myfate.ai/api/skills/TOOL_NAME \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"birthDate": "1990-05-27 14:30:00", "gender": "女", ...其他专有参数}'
```

---

### 工具列表与专有参数说明

*(注：除 `lunar_to_solar` 外，所有排盘接口都会默认接收上述 **基础排盘参数（通用）** 中定义的字段)*

1. **`lunar_to_solar`** (农历转阳历)
   - **场景**：用户提供农历生辰时，必须先以此工具转换。
   - **说明**：此接口不适用通用基础参数。
   - **参数**：
     - `lunarDate` (string, 必填): 农历日期，格式为 `YYYY-MM-DD`（如 `"1990-05-04"`）。
     - `normalTime` (string, 必填): 出生时间，格式为 `HH:mm:ss`（如 `"14:30:00"`）。

2. **`get_astrolabe`** (本命全盘)
   - **场景**：用于定盘比对、先天格局、性格特质分析、人生核心大方向。
   - **参数**：基础排盘参数(通用)。

3. **十年大限 / 流年 / 流月 / 流日** (`get_decadal_fortune` / `get_annual_fortune` / `get_monthly_fortune` / `get_daily_fortune`)
   - **场景**：推演特定时间段的运势。
   - **参数**：必须额外提供 `targetDate` 参数。
     - 基础排盘参数(通用)
     - `targetDate` (string, 必填): 目标查询时间。如大限/流年/流月/流日格式为 `"YYYY-MM-DD"` (如 `"2025-01-01"`)，用于确定排盘目标时间段。

4. **`get_user_decade_age`** (大限跨度查询)
   - **场景**：预先获取用户一生每个大限对应的年龄和年份范围。
   - **参数**：基础排盘参数(通用)

## 💬 用户交互与排盘准则

为了提供最准确的测算，开始任何算理推演前，请确保用户已经提供了以下四项核心信息：
1. **出生日期**（需向用户确认是**公历**还是**农历**，如果是农历是否有闰月）
2. **出生时间**（精确到小时/时辰即可，例如：下午2点、未时等）
3. **性别**（男/女，这关系到大运的顺排与逆排）
*(若信息不全，请温和且专业地引导用户补充。)*

**解读风格要求：**
- **提炼重点**：拿到工具返回的专业数据结构（Markdown）后，不要仅仅机械地复述星曜名词。要用通俗易懂、带有温度的语言，结合现代人的社会、工作、情感语境进行解读。
- **客观辩证**：命理讲究“吉凶相伴”，碰到煞星（如擎羊、陀罗、火星、铃星、地空、地劫）时，不要使用恐吓性语言，而应提供“趋吉避凶”的建设性指导。传递正向的情绪价值。

## 🚨 异常处理：计费拦截与充值引导 (Exception Handling)

系统对接了严格的配额管理。若 API 返回 403、402 或明确提示点数耗尽/额度不足时，你必须进入此异常处理流程：

1. **立即中断 (Break)**：绝对停止一切分析尝试，不要使用通用算命话术进行“幻觉”作答。
2. **优雅引导 (Prompt)**：向用户说明：“您的可用排盘点数已暂时耗尽。为了继续为您提供深度的命理分析，请访问 Homepage ([https://skill.myfate.ai](https://skill.myfate.ai)) 完成订阅或充值。”
3. **无缝接续 (Resume)**：当用户在外部完成支付并回复“已充值”或“继续”时，禁止要求用户重新提供生辰信息。直接读取当前上下文记忆中的参数，重新发起刚才失败的 `curl` 请求，并继续解读。
