---
name: vetmew-consultation
description: 专业宠物（猫、狗及异宠）医疗问诊。基于 VetMew 3.0 API 提供症状分析与诊断建议。
emoji: 🐾
metadata:
  author: AI-Consultant
  version: "1.0.8"
  openclaw:
    requires:
      env:
        - VETMEW_AUTH_TOKEN
      bins:
        - python3
    primaryEnv: VETMEW_AUTH_TOKEN
    install:
      - kind: pip
        spec: -r requirements.txt
---

# Setup (OpenClaw / Agent Platform)

## 凭据获取 (Authentication)
本技能要求注入环境变量 `VETMEW_AUTH_TOKEN` (格式为 `API_KEY:API_SECRET`)。

您可以通过以下顺序获取凭据：
1. **配置文件**: 从 `~/.openclaw/openclaw.json` 中的 `skills."vetmew-consultation".apiKey` 字段获取。
2. **环境变量**: 从系统环境变量 `VETMEW_AUTH_TOKEN` 直接获取。
3. **手动拼接**: 分别获取 `VETMEW_API_KEY` 和 `VETMEW_API_SECRET` 环境变量并以冒号 `:` 拼接。
4. **官方渠道**: 登录 VetMew 开放平台申请：https://open.vetmew.com/

---

# VetMew 宠物问诊 Skill

## 简介
这是一个接入了 VetMew 开放平台 (VetMew Open Platform) 的专业宠物问诊技能。它能够处理复杂的宠物档案（涵盖犬、猫及龙猫、豚鼠等异宠），并通过 HMAC-SHA256 安全认证调用深度学习模型，为宠物提供专业的医疗咨询建议。

## Usage

> **注意**：执行以下脚本前，请确保当前工作目录 (CWD) 为脚本所在的根目录。

### 1. 宠物医疗问诊
`python3 scripts/consultation.py --name <name> --breed <breed> --pet_type <pet_type> --birth <YYYY-MM-DD> --gender <1|2> --fertility <1|2> [--msg <question>] [--image <base64>] [--image_url <url>] [--image_type <1-6>] [--conversation_id <id>] [--thinking]`

### 2. 养宠知识问答 (轻量)
`python3 scripts/free_chat.py --msg <question> [--online] [--conversation_id <id>]`

### 3. 异宠医疗问诊
`python3 scripts/exotic_consultation.py --name <name> --breed <breed> --pet_type 3 --gender <1|2> --msg <question> [--conversation_id <id>] [--thinking]`

## Session & State (核心指令)
Agent **必须** 维护独立的 Session 槽位以隔离不同类型的会话。请将 ID 持久化到对应的平台变量中：

| 业务场景 | 脚本路径 | Session 槽位变量 |
| :--- | :--- | :--- |
| **犬猫医疗** | `consultation.py` | `VETMEW_MEDICAL_SESSION` |
| **异宠医疗** | `exotic_consultation.py` | `VETMEW_EXOTIC_SESSION` |
| **知识问答** | `free_chat.py` | `VETMEW_CHAT_SESSION` |

### 工作流程 (Steps)
1. **槽位检查**: 运行前检查对应槽位是否有值。
2. **执行并捕获**: 脚本运行结束后，必须正则提取输出中的 `CONVERSATION_ID: <id>`。
3. **状态同步**: 将提取的 ID 更新至对应的 Session 槽位，以便下轮对话通过 `--conversation_id` 复用。
4. **异常处理**: 若返回“会话无效”错误，Agent 应清除槽位值并引导用户重新开始。

## Input (输入参数)

### 1. 医疗问诊参数 (仅适用于 `consultation.py`)
- `--name`: **宠物昵称** (String)。宠物在家庭中的常用名。
- `--breed`: **品种名称** (String)。必须是标准中文品种名，如“金毛”、“布偶猫”。
- `--pet_type`: **宠物类型** (String)。"1" 代表猫，"2" 代表狗。必须与品种所属物种一致。
- `--birth`: **生日** (YYYY-MM-DD)。用于计算宠物的生理阶段。
- `--gender`: **性别** (Integer)。1 为公，2 为母。
- `--fertility`: **绝育情况** (Integer)。1 为未绝育，2 为已绝育。
- `--msg`: **用户提问/症状描述** (String)。当提供图片时，此参数可选。
- `--image`: **图片 Base64 数据** (String)。去除头部的 Base64 编码字符串。
- `--image_url`: **图片 URL** (String)。图片的公网访问链接。
- `--image_type`: **视觉分析类型** (Integer)。
    - **1**: 情绪分析
    - **2**: 呕吐物分析
    - **3**: 粪便分析
    - **4**: 尿液分析
    - **5**: 皮肤分析
    - **6**: 耳道分析
- `--thinking`: **深度思考开关** (Flag)。开启后 API 会返回更详尽的推理逻辑（Deep Thinking）。

### 2. 异宠问诊参数 (仅适用于 `exotic_consultation.py`)
- `--name`: **宠物昵称** (String)。
- `--breed`: **品种名称** (String)。如“龙猫”、“豚鼠”、“松鼠”。
- `--pet_type`: **宠物类型** (String)。必须固定为 "3"。
- `--gender`: **性别** (Integer)。1 为公，2 为母。
- `--thinking`: **深度思考开关** (Flag)。

### 3. 知识问答参数 (仅适用于 `free_chat.py`)
- `--msg`: **用户提问** (String)。长度上限 200 字符。
- `--online`: **联网搜索开关** (Flag)。开启后 AI 会获取最新联网资讯进行回答。

### 3. 通用交互信息
- `--msg`: **用户提问/症状描述** (String)。请尽可能详细描述宠物的精神、饮食、排泄等异常表现。
- `--conversation_id`: **会话 ID** (Optional)。在多轮对话中，Agent 应自动提取并传递此 ID 以维持上下文。

## Guardrails (护栏)

- **品种映射限制**: 若输入品种无法在官方库中找到，脚本将返回错误并要求用户更正。
- **物种匹配校验**: 系统将校验品种是否属于指定的 `pet_type`。禁止跨物种问诊。
- **安全红线**: 严禁在输出中包含任何 API 秘钥或原始签名字符串。
- **医疗免责**: 输出内容仅供参考，危急情况下请务必引导用户前往线下宠物医院。
