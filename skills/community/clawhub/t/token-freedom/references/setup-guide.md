# AI API 平台注册 & 配置教程

## 通用流程

所有平台遵循相同模式：注册 → 实名/认证 → 创建API Key → 充值（可选）→ 调用

---

## 一、硅基流动 SiliconFlow（最推荐）

### 注册
1. 访问 https://cloud.siliconflow.cn
2. 手机号注册（支持微信登录）
3. 填写邀请码获得额外2000万Tokens

### 创建 API Key
1. 进入控制台 → API密钥
2. 点击「新建API密钥」
3. 输入名称（任意），点击创建
4. **立即复制保存**，关闭后不可再次查看

### 调用方式
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxxxxxx",
    base_url="https://api.siliconflow.cn/v1"
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 接入 QClaw
在 QClaw 模型配置中：
- Base URL: `https://api.siliconflow.cn/v1`
- API Key: 你的 `sk-xxx`
- 模型名: `deepseek-ai/DeepSeek-V3` 或 `Pro/DeepSeek-R1`

### 推荐官计划
- 每邀请1人 → 双方各得2000万Tokens
- 下级再邀请 → 你额外得20%
- 入口：控制台 → 推荐官

---

## 二、火山引擎

### 注册
1. 访问 https://www.volcengine.com
2. 手机号/邮箱注册
3. 实名认证（企业或个人信息）

### 创建 API Key
1. 控制台 → 火山方舟 → 在线推理
2. 创建API Key
3. 开通模型服务（首次需手动开通 DeepSeek-R1 等）

### 调用方式
```python
client = OpenAI(
    api_key="your-key",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)
```

### 接入 QClaw
- Base URL: `https://ark.cn-beijing.volces.com/api/v3`
- 模型名: `deepseek-r1-250120` 或对应endpoint ID

---

## 三、DeepSeek 官方

### 注册
1. 访问 https://platform.deepseek.com
2. 手机号注册

### 创建 API Key
1. 左侧菜单 → API Keys
2. 创建新key，立即复制

### 调用方式
```python
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.deepseek.com"
)
```

### 接入 QClaw
- Base URL: `https://api.deepseek.com`
- 模型名: `deepseek-chat`（V3）或 `deepseek-reasoner`（R1）

---

## 四、智谱 AI（GLM-5 旗舰 + GLM-4.7-Flash 免费）✅ 有邀请奖励

### 注册
1. 访问邀请链接 https://www.bigmodel.cn/invite?icode=你的邀请码（双方各得2000万Tokens）
2. 或直接访问 https://open.bigmodel.cn
3. 手机号注册

### 奖励
- 通过邀请链接注册 → **双方各得2000万Tokens**
- GLM-5 旗舰模型，推理/代码/智能体 SOTA 水平
- **GLM-4.7-Flash 免费调用**（注意：API 模型列表不显示 Flash 系列，但直接调用可用。免费模型有并发和速率限制）

### 调用方式
```python
# 付费模型（需余额/赠送额度）
client = OpenAI(
    api_key="your-key",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)
# 免费 Flash 模型，直接指定 model="glm-4.7-flash" 即可
```

### 接入 QClaw
- Base URL: `https://open.bigmodel.cn/api/paas/v4`
- 模型名: `glm-4.7-flash`（免费）/ `glm-5`（旗舰）

---

## 五、Sophnet 算力平台（算能 Sophgo）✅ 有邀请奖励

### 背景
算能（Sophgo）自研 TPU/RISC-V 芯片，软硬一体国产算力。深度适配 OpenClaw/Hermes Agent，提供 ¥78 万大龙虾一体机。

### 注册
1. 访问邀请链接 https://www.sophnet.com?code=你的邀请码（双方各得Token奖励）
2. 手机号注册
3. 注册送 ¥20 额度

### 奖励
- 通过邀请链接注册 → 双方各获 Token 奖励
- DeepSeek-V3 极速版 126 t/s（清华大学实测榜首）
- 自研 TPU，推理成本降低 35%

### 创建 API Key
1. 登录后进入控制台
2. 找到 API Key 管理
3. 创建新 Key，立即复制保存

### 调用方式
```python
client = OpenAI(
    api_key="your-key",
    base_url="https://api.sophnet.com/v1"
)
```

### 接入 QClaw
- Base URL: `https://api.sophnet.com/v1`
- 模型名: `deepseek-r1`（满血版）/ `deepseek-v3-fast`（极速 126t/s）/ `qwen-max`
- 新用户 ¥20 免费额度，高吞吐适合批量/Agent 场景

---

## 六、OpenRouter（海外模型聚合）

### 注册
1. 访问 https://openrouter.ai
2. 点击 Sign Up，支持 Google / GitHub / 邮箱注册
3. 完成邮箱验证

### 创建 API Key
1. 登录后 → 右上角头像 → Keys
2. 或直接访问 https://openrouter.ai/settings/keys
3. 点击 Create Key，命名后生成
4. 立即复制保存（`sk-or-v1-xxx` 格式）
5. 可选设置消费限额（Credit Limit）

### 调用方式
```python
client = OpenAI(
    api_key="sk-or-v1-xxx",
    base_url="https://openrouter.ai/api/v1"
)

# 搜索免费模型：https://openrouter.ai/models?q=free
response = client.chat.completions.create(
    model="google/gemma-7b-it:free",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 接入 QClaw
- Base URL: `https://openrouter.ai/api/v1`
- 模型名: 从 https://openrouter.ai/models 查找（如 `qwen/qwen3.6-plus-preview:free`）
- 大量免费模型可用，无需绑卡

### 亮点
- 250+ 模型聚合，含 Claude / GPT / Gemini / Qwen
- 部分模型免费（搜索 `:free`）
- 按量付费，无月费

---

## 七、ModelScope 魔搭（阿里）

### 注册
1. 访问 https://modelscope.cn
2. 支持手机号 / 邮箱 / 阿里云账号注册
3. ⚠️ 必须绑定阿里云账号才能用 API（系统会引导）

### 创建 Access Token
1. 登录 → 右上角头像 → 个人中心
2. 进入「我的 Access Token」或直接访问 https://modelscope.cn/my/myaccesstoken
3. 生成新 Token，格式为 `ms-xxxxxxxx`
4. 如用于 Claude Code 等工具，需去掉 `ms-` 前缀（只保留后半部分）

### 调用方式
```python
client = OpenAI(
    api_key="ms-xxxxxxxx",
    base_url="https://api-inference.modelscope.cn/v1"
)
```

### 接入 QClaw
- Base URL: `https://api-inference.modelscope.cn/v1`
- 模型名: `Qwen/Qwen3.5-397B-A17B` 等
- 每日 2000 次免费调用额度

---

## 八、Groq（全球最快推理）

### 注册
1. 访问 https://console.groq.com
2. 支持 Google / GitHub / 邮箱注册
3. 无需绑卡

### 创建 API Key
1. 登录 → 左侧 API Keys
2. 点击 Create API Key
3. 命名后生成，立即复制

### 调用方式
```python
client = OpenAI(
    api_key="gsk_xxx",
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 接入 QClaw
- Base URL: `https://api.groq.com/openai/v1`
- 模型名: `llama-3.3-70b-versatile` 或 `mixtral-8x7b-32768`
- 免费额度充足，推理速度极快（LPU 芯片）

### 亮点
- 全球最快 LLM 推理速度
- 大量免费额度
- 支持 Llama / Mixtral 等开源模型

---

## 九、阿里云百炼（通义千问 + 300+模型）

### 注册
1. 访问 https://bailian.console.aliyun.com
2. 阿里云账号登录（需实名认证，支持支付宝授权，1分钟完成）
3. 首次开通自动获赠 90 天免费额度（各模型共 7000 万 Token）

### 创建 API Key
1. 控制台右上角头像 → API-KEY
2. 点击「创建我的API-KEY」
3. 选择默认业务空间，命名后创建
4. 立即复制保存（仅显示一次）

### 调用方式
```python
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-max",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 接入 QClaw
- Base URL: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- 模型名: `qwen-max` / `qwen-plus` / `deepseek-r1` / `deepseek-v3`
- 300+ 模型可选，覆盖文本/图像/音频/视频全模态

### 亮点
- 阿里云生态无缝集成（存储/数据库/函数计算）
- 低代码 RAG 知识库、Agent 构建
- 企业级应用开发首选

---

## 十、小米 MiMo ✅ 有邀请奖励

### 背景
小米自研大模型，V2.5 系列 MIT 开源可商用。启动百万亿 Token Orbit 计划，与 Hermes Agent / OpenClaw 深度生态合作。

### 注册（两步走）
**第一步：申请百万亿 Token**
1. 访问 https://100t.xiaomimimo.com 提交申请
2. 填写邮箱、项目描述等信息
3. 等待 3 个工作日审核

**第二步：注册平台**
1. 审核通过后，用申请邮箱注册 https://platform.xiaomimimo.com?ref=你的邀请码
2. 通过邀请链接注册 → 双方各得 ¥10 API 体验金
3. 进入「订阅管理」查看免费额度（通常数亿 Token）

### 创建 API Key
1. ⚠️ 使用免费额度：去「订阅管理」获取专属 Base URL + API Key（格式 tp-xxxxx）
2. 不要自己创建 API Key（创建的是按量付费的 sk-xxx）
3. 支持 OpenAI 兼容协议和 Anthropic 兼容协议

### 调用方式（Token Plan）
```python
client = OpenAI(
    api_key="tp-xxxxx",
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)
```

### 接入 QClaw
- Base URL: `https://token-plan-cn.xiaomimimo.com/v1`（Token Plan 套餐）
- 或: `https://api.xiaomimimo.com/v1`（按量付费）
- 模型名: `mimo-v2.5-pro` / `mimo-v2.5`

### 亮点
- MIT 开源可商用
- 百亿 Token 免费送
- OpenAI + Anthropic 双协议
- MiMo-V2.5-Pro 代码/推理能力强劲

---

## 十一、腾讯混元

### 注册
1. 访问 https://console.cloud.tencent.com/hunyuan
2. 腾讯云账号登录（需实名认证）
3. 首次开通赠送 100 万 Token（1 年有效）

### 创建 API Key
1. 控制台左侧 → 「使用 OpenAI SDK 方式接入」
2. 点击「创建 API KEY」
3. 生成后立即复制保存

### 调用方式
```python
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.hunyuan.cloud.tencent.com/v1"
)

response = client.chat.completions.create(
    model="hunyuan-turbos-latest",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 接入 QClaw
- Base URL: `https://api.hunyuan.cloud.tencent.com/v1`
- 模型名: `hunyuan-turbos-latest` / `hunyuan-t1-latest` / `hunyuan-large`

### 亮点
- 腾讯自研旗舰模型
- 文生图、文生视频多模态
- 微信小程序生态集成
- 企业级安全合规

---

## 十二、Anthropic Claude

### 注册
1. 访问 https://console.anthropic.com
2. Google/邮箱注册
3. 部分地区需上传身份证 KYC 验证（1-3 工作日）
4. ⚠️ 需绑定海外信用卡，无免费额度

### 创建 API Key
1. Dashboard → API Keys → Create Key
2. 命名后复制保存

### 调用方式
```python
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-xxx")
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 接入 QClaw
- Base URL: `https://api.anthropic.com`
- 模型名: `claude-sonnet-4-20250514` / `claude-haiku-4-20250514` / `claude-opus-4-20250514`

### 亮点
- Claude Code 开发神器
- 代码/Agent 能力市场领先
- AI 安全合规标杆

---

## 十三、OpenAI

### 注册
1. 访问 https://platform.openai.com
2. 邮箱/Google/微软 注册
3. 绑定海外信用卡（支持 Visa/Mastercard）
4. 新用户获 $5 赠金（3 个月有效）

### 创建 API Key
1. Dashboard → API Keys → Create new secret key
2. 立即复制保存（仅显示一次）

### 调用方式
```python
from openai import OpenAI
client = OpenAI(api_key="sk-xxx")
response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 接入 QClaw
- Base URL: `https://api.openai.com/v1`
- 模型名: `gpt-5` / `gpt-4o` / `o1`

### 亮点
- 最成熟 API 生态
- GPT-5 + o1 推理
- DALL-E/Sora 多模态

---

## 十四、Google Gemini

### 注册（免费层 — 无需绑卡）
1. 访问 https://aistudio.google.com
2. Google 账号登录
3. 左侧菜单 → Get API Key → 免费创建
4. 无需绑卡即可使用 Gemini 2.5 系列

### 注册（GCP $300 赠金 — 需绑卡）
1. 访问 https://cloud.google.com 注册 GCP
2. 绑定 Visa/Mastercard（$1 验证后退回）
3. 获 $300/90 天赠金，可调所有模型

### 调用方式
```python
import google.generativeai as genai
genai.configure(api_key="AIzaSy-xxx")
model = genai.GenerativeModel("gemini-2.5-flash")
```

### 接入 QClaw（OpenAI 兼容）
- Base URL: `https://generativelanguage.googleapis.com/v1beta/openai`
- 模型名: `gemini-2.5-flash` / `gemini-2.5-pro`

### 亮点
- 免费层最慷慨（2.5 Flash 每日几千次）
- 2M token 超长上下文
- 原生多模态（图/音/视）

---

## 十五、MiniMax

### 注册
1. 访问 https://platform.minimaxi.com
2. 手机号注册
3. 新用户获 ¥15 免费额度

### 创建 API Key
1. 控制台 → 个人中心 → 接口密钥
2. 生成 API Key（比一般平台长很多，属正常）
3. 绑定支付方式（Token Plan 订阅制）

### 调用方式
```python
from openai import OpenAI
client = OpenAI(
    api_key="eyJhbGciOi...",
    base_url="https://api.minimaxi.com/v1"
)
```

### 接入 QClaw
- Base URL: `https://api.minimaxi.com/v1`
- 模型名: `minimax-m3` / `minimax-m2.5`

### 亮点
- M3 旗舰编程 + Agent（1M 上下文）
- 海螺视频生成
- 全模态（文/音/视/图）
- Token Plan 统一订阅

---

## 十六、Moonshot 月之暗面 Kimi

### 注册
1. 访问 https://platform.moonshot.cn
2. 手机号/微信注册
3. 新用户获 ¥15 额度或 100 万 tokens

### 创建 API Key
1. 右上角头像 → API 管理
2. 创建新的 secret key
3. 立即复制保存

### 调用方式
```python
from openai import OpenAI
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.moonshot.cn/v1"
)
```

### 接入 QClaw
- Base URL: `https://api.moonshot.cn/v1`
- 模型名: `kimi-k2.6` / `kimi-k2.5`

### 亮点
- Kimi K2.6 MIT 开源可商用
- 最强代码 + Agent 模型
- 128K 长上下文
- 累计融资 376 亿

---

## API Key 安全提示

⚠️ **务必遵守**：
1. API Key 等同于密码，绝不要分享给他人
2. 不要在公开代码仓库中提交 API Key
3. 建议设置消费额度上限（各平台均支持）
4. 定期检查 API 调用记录，发现异常立即重置 Key
