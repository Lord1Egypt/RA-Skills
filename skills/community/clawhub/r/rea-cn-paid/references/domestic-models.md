# 国内大模型清单（可接入 REA-CN 的 LLM）

> **核心约束**：REA-CN 通过 MCP 把 **170 个工具**交给 LLM 调用，因此**所选模型必须支持 function / tool calling**。
> 优先选择 **OpenAI 兼容协议**的端点（接入成本最低，直接填入 MCP 客户端的 base_url + api_key 即可）。
> 下列清单覆盖闭源 API、开源可本地部署、国内聚合平台三类，并说明在 WorkBuddy 模型选择器中的接入方式。

---

## 1. 闭源 API（联网调用，多数 OpenAI 兼容）

| 厂商 | 代表模型 | 协议/平台 | 备注 |
|---|---|---|---|
| 智谱 AI（Zhipu） | GLM-4、GLM-4-Plus、GLM-4-Air、GLM-4-Flash、GLM-4-Long | 智谱开放平台 / BigModel，OpenAI 兼容 | 工具调用成熟 |
| 阿里 通义千问 | qwen-max、qwen-plus、qwen-turbo、qwen-long、qwen2.5 系列 | 阿里云百炼 / DashScope，OpenAI 兼容 | function calling 原生支持 |
| 百度 文心一言 | ERNIE 4.0 / 3.5、ERNIE-Speed、ERNIE-Lite、ERNIE-Tiny | 百度智能云千帆 | 支持 function_call / 插件 |
| 字节 豆包 | Doubao-pro、Doubao-lite、Doubao-vision | 火山方舟 | 支持 tools |
| 腾讯 混元 | Hunyuan-Pro、Hunyuan-Standard、Hunyuan-Turbo | 腾讯云 TI / 混元 | function calling |
| 深度求索 DeepSeek | deepseek-chat、deepseek-reasoner | DeepSeek 开放平台，OpenAI 兼容 | 强工具调用 |
| 月之暗面 Kimi | moonshot-v1-8k / 32k / 128k | Moonshot 开放平台，OpenAI 兼容 | 支持 tools |
| MiniMax | abab6.5、abab7 系列 | MiniMax 开放平台 | 支持 function calling |
| 阶跃星辰 Step | step-1、step-2、step-1o | 阶跃开放平台 | 工具调用支持 |
| 百川智能 Baichuan | baichuan4、baichuan3-turbo、baichuan2 | 百川开放平台 | 支持 |
| 零一万物 Yi | yi-large、yi-medium、yi-large-rag | 零一开放平台 | 支持 |
| 讯飞星火 Spark | spark-3.5、spark-4.0、spark-lite | 讯飞开放平台 | function call 支持 |
| 商汤 日日新 | SenseNova / nova 系列 | 商汤大装置 | 支持 |
| 昆仑万维 天工 | Skywork 系列 | 天工开放平台 | 支持 |
| 360 智脑 | 360GPT | 360 智脑 | 支持 |
| 华为 盘古 | Pangu 系列 | 华为云 | 主要企业级，需评估 tool calling |
| 京东 言犀 | 言犀大模型 | 京东云 | 企业级 |
| 小米 小爱 / MiLM | MiLM 系列 | 小米 | 部分开放 |

---

## 2. 开源可本地部署（自托管 + 中转网关接入 MCP）

本地部署后，套一层 OpenAI 兼容网关（如 `ollama`、[One API](https://github.com/songquanpeng/one-api)、[vLLM](https://github.com/vllm-project/vllm)、[LMStudio](https://lmstudio.ai/)）即可作为 REA-CN 的 LLM 后端。下列模型工具调用能力较强：

| 模型 | 许可 | 特点 |
|---|---|---|
| Qwen2.5 / Qwen3 系列（0.5B–72B） | Apache 2.0 | 工具调用强，中英文俱佳，首选本地方案 |
| DeepSeek-V3 / R1（含蒸馏版） | MIT | 推理与工具调用强 |
| GLM-4-9B / GLM-4-32B | Zhipu 开源许可 | 中文工具调用好 |
| InternLM2.5 / InternLM3 | Apache 2.0 | 上海 AI 实验室 |
| Yi-1.5 / Yi-34B | Apache 2.0 | 01.AI |
| Baichuan2 / Baichuan4 | 百川许可 | 中文友好 |
| MiniMax-Text-01 | 开源 | 长上下文 |
| 书生·浦语 / InternLM 系列 | Apache 2.0 | 同 InternLM |

> 本地部署优点：数据不出内网、可审计、适合安全研究场景；缺点：需 GPU 资源，小模型工具调用稳定性弱于云 API。

---

## 3. 国内聚合平台（统一接入多家模型）

通过以下平台可取用上面多数闭源/开源模型，且均为 OpenAI 兼容，便于直接接入 MCP 客户端：

| 平台 | 特点 |
|---|---|
| 硅基流动 SiliconFlow | 托管 Qwen/DeepSeek/GLM 等，按量计费，OpenAI 兼容 |
| 火山方舟 | 字节系，托管豆包与第三方模型 |
| 阿里云百炼 | 通义全系 + 第三方 |
| 腾讯云混元 / TI 平台 | 混元 + 第三方 |
| 百度智能云千帆 | 文心 + 第三方 |
| 智谱 BigModel | 智谱全系 |
| 302.AI | 聚合多家，OpenAI 兼容 |
| 派欧云 PPIO | 推理聚合 |
| 月之暗面开放平台 | Kimi 系列 |

---

## 4. WorkBuddy 模型选择器接入

WorkBuddy 自带模型选择器，可接入任意 **OpenAI 兼容端点**。接入 REA-CN 时：
- 在 WorkBuddy 的模型设置中选择「自定义 / OpenAI 兼容」；
- 填入上表任一国内端点的 `base_url` 与 `api_key`；
- 确保该模型在端点侧开启了 **tool/function calling**；
- 之后在本技能中调用 REA 工具时，WorkBuddy 即可驱动 170 个 MCP 工具。

> 选用哪个模型取决于任务：反编译/调用图等复杂推理建议用较强模型（qwen-max / GLM-4-Plus / deepseek-chat）；简单查询可用轻量模型（GLM-4-Flash / qwen-turbo）以省成本。

---

## 5. 接入自检

- [ ] 端点为 OpenAI 兼容（或客户端原生支持该厂商）
- [ ] 已开启 tool/function calling
- [ ] `base_url` + `api_key` 已正确填入客户端
- [ ] 用一次简单工具（如 `binary_session`）验证可成功调用
