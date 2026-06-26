---
name: trtc-ai-customer-service
version: 1.2.5
description: |
  Build an AI e-commerce customer service Web app with TRTC ConversationAI — real-time voice/text dual-mode, trilingual (Chinese/English/Cantonese), digital avatar optional. Covers order inquiry, returns, shipping tracking, and promotions.
  基于腾讯云 TRTC Conversational AI 快速构建 AI 电商客服 Web 应用 — 实时语音/文字双模、中英粤三语、数字人可选。覆盖订单查询、退换货、物流追踪、商品咨询等场景。
homepage: https://github.com/jerryang-cool/trtc-ai-customer-service-skill
metadata:
  openclaw:
    emoji: "🛍️"
    requires:
      bins:
        - python3
---

# TRTC AI 电商客服 Skill

本 Skill 指导你基于腾讯云 TRTC Conversational AI 能力，快速构建 AI 电商客服 Web 应用。
场景预置了订单查询、退换货处理、商品咨询、物流追踪、优惠活动等电商业务模块。

## 触发条件

当用户**表达构建/搭建/集成意图**时使用此 Skill：
- "做一个 AI 客服" "搭建电商客服" "帮我做个智能客服系统" "语音客服 demo"
- "build an AI customer service" "e-commerce customer service app"
- "TRTC ConversationAI" "TRTC + AI 客服" "TRTC e-commerce support"
- "StartAIConversation" "StopAIConversation" "ControlAIConversation"（TRTC API 名称）
- "数字人客服" "avatar customer service"
- "实时语音 AI 对话" "ASR + LLM + TTS 客服"

**不应触发的场景**：
- 用户仅在讨论客服概念，没有构建/开发意图
- 用户询问通用 chat bot 方案，不需要语音能力或电商场景
- 关键词如 "voice bot" "chat bot" 单独出现且无构建上下文

## 架构总览

```
浏览器 (TRTC Web SDK v5)
     ↕ 音频 (WebRTC) + 自定义消息 (字幕/状态/文字输入)
TRTC Room
     ↕ 内置 ASR → LLM → TTS → 推回房间
TRTC AI Bot (云端)
     ↕ OpenAPI (TC3-HMAC-SHA256)
Flask 后端 (app.py)  —— 仅 UserSig 签发 + OpenAPI 中转
```

| 平面 | 通道 | 内容 |
|------|------|------|
| **媒体面** | WebRTC 音频流 | 用户麦克风 ↔ TRTC 房间 ↔ AI Bot |
| **控制面** | HTTP `/action` | 前端 → Flask → TRTC OpenAPI |
| **数据面** | TRTC 自定义消息 | 字幕(10000) / AI 状态(10001) / 文字输入(20000) / 打断(20001) |

后端**完全不调用 LLM**——LLM 由 TRTC 云端 AI Bot 内部调用，后端只负责签发 UserSig 和中转 OpenAPI 请求。

---

## 工作流程

根据用户需求选择合适的路径。

### 路径 A：从零创建新项目（推荐）

#### Step 1: 生成项目

运行脚手架脚本：

```bash
python {baseDir}/scripts/scaffold.py <项目目录> [--name <商城名称>] [--name-en <English name>]
```

- `{baseDir}`：本 Skill 所在目录的绝对路径（由 Agent 自动替换为实际路径）
- `--name`：商城名称（默认"云尚商城"），用于中文/粤语的 SystemPrompt、欢迎语、告别语、前端 UI
- `--name-en`：英文商城名称（默认自动推导：中文名时为"CloudShop Mall"，英文名时与 `--name` 相同），用于英文 SystemPrompt、英文欢迎语/告别语
- 默认支持中文/英文/粤语三语，无需手动指定语言
- 脚本自动生成全部文件：后端 + 前端 + 头像 + 鉴权库 + 启动脚本，无需手动复制任何文件

**检查点**：确认用户看到 `✅ 电商客服项目已生成到: xxx` 和完整文件列表，再继续。

#### Step 2: 配置密钥

引导用户运行启动脚本（**根据操作系统自动选择**：macOS/Linux 用 `./start.sh`，Windows 用 `start.bat`），首次运行会进入交互式引导：

- [0/4] 选择部署区域（默认 `intl` 国际站，可选 `cn` 中国站）— 后续步骤会根据所选区域展示对应的控制台链接
- [1/4] 腾讯云 API 密钥 → 脚本会展示对应区域的 [CAM 控制台](https://console.intl.cloud.tencent.com/cam/capi) 链接
- [2/4] TRTC 应用凭据 → 脚本会展示对应区域的 [TRTC 控制台](https://console.trtc.io/app) 链接
- [3/4] LLM 配置 → **建议优先使用 TokenHub**（腾讯云统一 LLM 网关，开箱即用）：
  - `LLMConfig.LLMType`：`openai`（固定）
  - `LLMConfig.Model`：`deepseek-v4-flash`（推荐）
  - `LLMConfig.APIUrl`：
    - 国际站：`https://tokenhub-intl.tencentcloudmaas.com/v1/chat/completions`
    - 中国站：`https://tokenhub.tencentmaas.com/v1/chat/completions`
  - `LLMConfig.APIKey`：在 TokenHub 控制台获取（[国际站](https://console.intl.cloud.tencent.com/tokenhub) | [中国站](https://console.cloud.tencent.com/tokenhub)）
  - 也支持其他兼容 OpenAI 协议的 LLM，参考配置指南：[国际站](https://trtc.io/document/68338?product=conversationalai) | [中国站](https://cloud.tencent.com/document/product/647/115413)

**检查点**：确认用户看到 `✓ 所有密钥已配置完成！`。如果有跳过项，提醒手动编辑 `env.yaml`。

> **提示用户**：以上为最小必填项，启动成功后还有丰富的可定制选项（角色定制、商城名称、欢迎语、TTS 音色、关键词等），详见 Step 4。

#### Step 3: 启动验证

启动脚本会自动创建虚拟环境、安装依赖、启动服务。

**验证标准**（告知用户逐项确认）：
1. 终端显示 `🚀 启动 TRTC AI 智能客服` + 访问地址（公网服务器会自动检测公网 IP 并启用 HTTPS，显示 `https://<公网IP>:8080`；本地开发则显示 `http://localhost:8080`）
2. 浏览器打开页面 → 能看到客服头像选择界面
3. 选择客服 → 点击"开始对话" → 听到 AI 播报欢迎语
4. 说话或打字 → AI 能正常回复

#### Step 4: 定制化（可选）

启动成功后，**主动告知用户**以下所有可定制项，引导按需修改：

| 定制项 | 修改位置 | 说明 |
|--------|---------|------|
| **AI 客服角色** | 交互式引导 [4/4]（删除 `env.yaml` 后重新运行 `./start.sh`），或直接编辑 `env.yaml` → `SystemPrompt` / `SystemPromptYue` / `SystemPromptEn` | 预设品类 + 语气快速定制（见下方枚举表），也可手动编辑三语 SystemPrompt 做精细调整 |
| **商城名称/品牌** | scaffold 的 `--name` / `--name-en` 参数 | 一键替换全链路品牌文案（三语 SystemPrompt、欢迎语、告别语、前端 UI） |
| **欢迎语 / 告别语** | `env.yaml` → `WelcomeMessage` / `FarewellMessage`（`.zh` / `.yue` / `.en`） | AI 进房首条播报 / 关键词触发结束时播报 |
| **LLM 模型** | `env.yaml` → `LLMConfig.Model` / `APIUrl` / `APIKey` | LLM 配置指南：[国际站](https://trtc.io/document/68338?product=conversationalai) \| [中国站](https://cloud.tencent.com/document/product/647/115413) |
| **TTS 音色** | `config_loader.py` → `TTS_VOICE_MAP` | TTS 音色配置指南：[国际站](https://trtc.io/document/79682?product=conversationalai) \| [中国站](https://cloud.tencent.com/document/product/647/115414) |
| **商品/订单数据** | `static/mock-orders.json`，或参考 `references/frontend-guide.md` 对接真实 API | JSON 格式含三语名称和价格，可替换为真实订单系统 |
| **数字人** | `env.yaml` → `AvatarConfig` 三项 | 三项全填启用数字人视频模式，否则纯语音 |
| **部署方式** | 自动检测公网 IP 启用 HTTPS；生产环境用 Gunicorn + Nginx + 正式证书 | WebRTC 要求 HTTPS；生产还需添加 `/action` 接口鉴权 |

**AI 客服角色预设枚举值**（`start.sh` 交互式引导 [4/4]）：

商城品类（影响 AI 的专业知识方向）：

| 选项 | 品类 | AI 擅长方向 |
|------|------|------------|
| 1 | 综合电商（默认） | 通用电商场景，不修改 SystemPrompt |
| 2 | 数码产品 | 参数对比、兼容性问题、保修政策、使用教程 |
| 3 | 服装鞋帽 | 尺码推荐、面料材质、搭配建议、洗涤保养、退换尺码 |
| 4 | 食品生鲜 | 保质期、储存方式、配送时效、食材产地、过敏原信息 |
| 5 | 家居百货 | 商品尺寸规格、安装方式、材质说明、配送安装服务 |

客服语气风格（影响 AI 的表达方式）：

| 选项 | 风格 | 效果 |
|------|------|------|
| 1 | 亲切自然（默认） | 像朋友聊天，已内置于默认 SystemPrompt |
| 2 | 专业严谨 | 用词准确规范，适合高端品牌/B2B |
| 3 | 活泼可爱 | 轻松表达方式，适合年轻用户群体 |

> 选择后自动注入三语 SystemPrompt（中文/粤语/英文同步）。如需更精细定制，直接编辑 `env.yaml` 中的 SystemPrompt 即可。

### 路径 B：为现有项目集成 TRTC AI 对话

#### Step 1: 了解现有架构

询问并确认：
- 后端语言和框架（Python/Node/Go/Java？）
- 前端技术栈（React/Vue/原生 JS？已有 TRTC SDK？）
- 集成范围：仅后端 API？还是含前端 UI？

#### Step 2: 按需读取参考文档并输出代码

根据用户技术栈，读取对应文档并**直接输出可集成的代码片段**：

| 需求 | 读取文档 | 输出内容 |
|------|----------|----------|
| 后端 API | `references/architecture.md` | 用户语言的 5 个 Action 处理器代码（join / Start / Stop / Farewell / Transfer） |
| 配置体系 | `references/config-guide.md` | 生成 `env.yaml` 模板 + 配置加载代码 |
| 前端对话 UI | `references/frontend-guide.md` | TRTC SDK 进房 + 消息监听 + 字幕渲染代码 |

**关键**：如果用户不是 Python 技术栈，需要将参考文档中的 Python 逻辑**翻译为用户的语言**（如 Node.js / Go / Java），核心逻辑不变。

#### Step 3: 验证集成

引导用户完成最小可用流程并逐步确认：
1. 后端 `/action` 接口能正常响应（`curl -X POST /action -H "Action: join"` 返回 UserSig）
2. 前端成功进入 TRTC 房间（控制台无报错）
3. `StartAIConversation` 调用成功返回 TaskId
4. 用户说话 → 听到 AI 回复（完整链路跑通）

**如果卡在某一步**，参照下方 FAQ 表逐条排查。

---

## 常见问题排查

当用户遇到问题时，按以下清单排查：

| 现象 | 原因 | 解决方案 |
|------|------|----------|
| scaffold.py 报错退出 | Python 版本或参数错误 | 确认 Python 3.8+；检查输出目录路径是否合法 |
| `start.sh` 报 Python 版本不够 | Python < 3.8 | 安装 Python 3.8+ |
| venv 创建失败 | 缺少 `python3-venv` 包 | Ubuntu/Debian: `sudo apt install python3-venv`；macOS 自带 |
| 依赖安装失败 | 网络问题 | `start.sh` 会自动 fallback 官方源；或手动 `pip install -r requirements.txt` |
| `env.yaml` 解析报错 | YAML 缩进或格式错误 | 用在线 YAML 校验器检查；常见：冒号后缺空格、中文引号 |
| 页面打开空白 | 静态文件缺失 | 确认 `static/app.js` 和 `templates/customer_service.html` 存在 |
| 点"开始对话"无反应 | 密钥未填或填错 | 检查 `env.yaml` 中 SDKAPPID 不为 0、SECRET_ID/KEY 正确 |
| 点"开始对话"提示**进房失败** | TRTC 进房参数异常 | 检查 `SDKAPPID` 是否正确填写；UserSig 是否校验失败（核对 `TRTC.SECRET`） |
| 说话**无任何响应**（语音不可用） | 浏览器麦克风权限未授予或设备异常 | 检查浏览器地址栏麦克风权限；测试系统设备：录音机能否录到声音 |
| 仅显示**本地字幕，AI 无回应** | LLM 服务异常 | 检查 `LLMConfig.APIKey` / `APIUrl` / `Model` 是否正确；确认 LLM 账户额度充足 |
| AI 有字幕但**无语音播报** | TTS 服务异常 | 核对 TTS 参数（VoiceId、Language）；确认 TTS 套餐包资源充足 |
| LLM **长时间不回复**或超时报错 | LLM Timeout | 调大 `env.yaml` → `LLMConfig.Timeout`（如 5.0 → 10.0） |
| 进房成功但无欢迎语 | LLM APIKey 错误或 TRTC 服务未开通 | 检查 `LLMConfig.APIKey`；确认 TRTC 控制台已开通 AI 对话能力 |
| 非 localhost 访问**无声音或麦克风不可用** | WebRTC 安全策略要求 HTTPS | 运行 `./start.sh --https` 自动生成自签证书并启用 HTTPS；首次访问浏览器点击"高级→继续前往" |
| 公网 IP 访问**页面打不开** | 防火墙未放行端口 | 确认服务器防火墙/安全组已放行 8080 端口（TCP）|
| 端口 8080 被占用 | 其他进程占用 | `start.sh` 会自动检测并询问是否终止 |
| 浏览器控制台报 CORS 错误 | 前后端不同源 | 确保前端页面由 Flask 提供（同源）；不要用 `file://` 打开 HTML |

---

## 速查参考

### 后端 API（`POST /action` + `Action` 请求头）

| Action | 职责 |
|--------|------|
| `join` | 签发 UserSig（用户/机器人/数字人），下发关键词/告别语/数字人开关 |
| `StartAIConversation` | 组装参数调用 TRTC OpenAPI 启动 AI 对话 |
| `StopAIConversation` | 兜底停止（正常走 FarewellAndStop） |
| `FarewellAndStop` | 推送告别语 + StopAfterPlay 一站式结束 |
| `TransferAndStop` | 推送转接提示语 + StopAfterPlay 一站式结束 |

### 核心设计模式（详见 `references/architecture.md`）

| 模式 | 要点 |
|------|------|
| StopAfterPlay 一站式结束 | `ControlAIConversation` + `StopAfterPlay=true`，TTS 播完自动停止 |
| 文字输入跳过 ASR | `type: 20000` 自定义消息直送 LLM |
| 中英文词边界匹配 | 中文用非中文字符边界，英文用 `\b` |
| 增量/累积自适应字幕 | 自动检测 TRTC 下发模式 |
| 机器人退房 + AI 状态双保险 | `REMOTE_USER_LEAVE` + `state=5` |
| 数字人可选降级 | `AvatarConfig` 三项齐全启用，否则纯语音 |

### 技术栈

Python 3.8+ · Flask · tencentcloud-sdk-python · 原生 JS · TRTC Web SDK v5 · YAML（envyaml）

### 安全

- `env.yaml` 含密钥，加入 `.gitignore`，切勿提交
- UserSig 服务端签发，密钥不暴露给前端
- 生产环境添加 `/action` 接口鉴权
- 非 localhost 部署必须 HTTPS（WebRTC 安全策略）
