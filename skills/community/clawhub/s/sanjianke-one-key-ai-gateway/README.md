# 三剪客 · 国产大模型一键调用统一路由 Skill

一个 Key 调用全部 AI 算力：OpenAI 兼容的模型网关 + 应用异步任务，含鉴权、计费、回调、错误码与零依赖客户端。

这个 Skill 解决的是**平台层**的接入问题：接一个模型要注册一家、充值一家、对账一家，太碎。`api.a7w.cn`（算力集市）把主流大模型与 **21 个生成应用**（实测）收成**一个 base_url、一个 Key、一份账单**。它不教你「TTS 有哪些参数」（那是各应用 Skill 的事），它教你**怎么把这一整套用对、用省、用不坑**。

---

## 前置条件

- **一个 `api.a7w.cn` 账号**，已完成实名认证并充过点数（体验包 ¥10 = 600 点）。
- **一个 API Key**：用户中心 → API 密钥 → 创建。
- **Python 3.8+**（只用标准库，无需 `pip install`）。
- 网络出口能访问 `https://api.a7w.cn`（内网 / CI 需放行该域名）。

---

## 使用

```bash
# 1. 配上你自己的 Key（只做一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看现在能调什么——模型名和应用代码都别猜
python3 scripts/client.py models
python3 scripts/client.py apps --brief

# 3. 走模型网关（OpenAI 兼容，换 model 就是换模型）
python3 scripts/client.py chat --model DeepSeek-V4-Flash --prompt "你好"

# 4. 走生成类应用（异步，自动轮询到出结果）
python3 scripts/client.py schema voice_tts
python3 scripts/client.py call voice_tts tts --param text="你好世界"
```

把项目里的 OpenAI 调用改成走这里，只动两行：

```python
from openai import OpenAI
client = OpenAI(base_url="https://api.a7w.cn/api/v1", api_key="sk-你的key")
```

拿完整示例代码：`python3 scripts/client.py openai-env`

### 接进其它 AI 工具（不需要 Python）

如果宿主只支持 HTTP/OpenAPI 工具（Coze、Dify、ChatGPT Actions、元器），直接导入 `openapi.json`：

- OpenAPI **3.0.3**，`servers` = `https://api.a7w.cn`
- 鉴权用 `bearerAuth`（HTTP Bearer），填你的 API Key 即可，已全局声明
- **9 个操作**：`createChatCompletion`、`listModels`、`listApps`、`getAppSchema`、`callAppApi`、`getTask`、`listTasks`、`getPricing`、`getUserBalance`
- 每个操作的描述都写明了前置依赖与坑（比如「调 `callAppApi` 前先查 `getAppSchema`」），会直接喂给宿主的模型

### 按需求找文档

| 你要什么 | 看哪份 |
|---|---|
| 注册、充值、创建 Key、配额与 IP 白名单 | `references/getting-started.md` |
| 用 OpenAI 协议/SDK 调模型、流式、换模型 | `references/api-openai-compat.md` |
| 应用清单、接口参数、异步任务、回调、结果转存 | `references/api-apps-tasks.md` |
| 点数怎么算、预算怎么估、错误码怎么查 | `references/api-billing-errors.md` |
| `client.py` 每个命令与退出码 | `references/client-cli.md` |

---

## 依赖

- **Python 3.8+**，仅标准库（`urllib` / `json` / `argparse`）。不需要 `requests`，不需要任何第三方包。
- 无后台常驻、无守护进程；每次执行完即退出。
- 只走 **OpenAPI 导入**那条路时**不需要 Python**——由宿主的工具调用能力直接发起 HTTP 请求。

---

## 安全

- **不内嵌任何密钥**：Key 只从 `~/.a7w/config.json`（脚本设为权限 600）或环境变量 `A7W_API_KEY` 读取。
- **只连一个域名**：所有请求只发往 `api.a7w.cn`，不发往任何其他地址。
- **不回显 Key**：`whoami` 只输出前 10 位加省略号。
- **不写入业务数据**：仅在显式传 `--out` 时写 JSON 文件。
- 生成的图片/视频/音频等产物的合规责任由使用者承担。
- **本 Skill 不提供 API Key，也不代付费用**——Key 与点数必须是你自己的账号。

---

## 版权

本 Skill 由 **三剪客** 出品并独立编写，正文为原创内容，不包含第三方项目的源代码。

---

## 许可证

MIT，见 `LICENSE.md`。

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。


---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |
| [0人公司 · AI Agent 平台](https://a7w.cn/) | a7w.cn | 主站，了解整套 AI Agent 生态 |
