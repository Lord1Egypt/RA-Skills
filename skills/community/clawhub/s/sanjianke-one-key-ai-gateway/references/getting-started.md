# 起步：从注册到跑通第一个请求

## 1. 注册与实名

1. 打开 [算力集市](https://api.a7w.cn/)，注册账号。
2. 完成**实名认证**——没有实名无法创建 API Key。
3. 登录 [用户中心](https://api.a7w.cn/user-center.html)。

## 2. 充值：点数怎么来的

平台按**点数**计费，**1 元 = 100 点**。当前只有「会员套餐」一种开通方式：

| 套餐 | 价格 | 到账 | 附带权益 |
|---|---|---|---|
| 体验包 | ¥10 | 600 点 | 含 7 天会员权益 |
| 标准包 | ¥99 | 10000 点 | 全部模型与应用接口、异步调度、用量统计/流水导出 |
| 企业 / 渠道 | 定制 | 定制 | 批量充值、阶梯折扣、下级账号与分成、专属对接 |

要点：

- **点数永久有效**，不是按月清零。
- 消费**优先扣会员点数，不足再扣充值额度**。
- 计费是「**先冻结、后结算**」：提交任务时按预估价冻结，完成后按实际用量多退少补，**失败不计费**。
- 用量与流水在用户中心实时可查、可导出，适合做对账。

## 3. 创建 API Key

**用户中心 → API 密钥 → 创建**。创建时注意两件事：

### 3.1 消费上限（quota）

每个 Key 可以单独设**消费上限**。这是一个独立于账号余额的闸门：

| 现象 | 错误码 | 真正的含义 |
|---|---|---|
| 账号余额不足 | 402 `insufficient_points` | 去充值 |
| 这个 Key 的额度打满 | 402 `key_quota_exceeded` | 去调高/重置这个 Key 的 quota，**不用充值** |

**别把这两个搞混**——把 `key_quota_exceeded` 当成没钱去充值，是白花钱。

### 3.2 权限范围

Key 可能被限制为只能调部分模型/应用。越权调用返回 **403 `permission_denied`**，这也和余额无关。

## 4. 把 Key 配到本机

```bash
# 方式一：写进本机配置（Windows/macOS/Linux 通用，权限 600）
python3 scripts/client.py login --key sk-你的key

# 方式二：环境变量（优先级高于本机配置，适合 CI）
export A7W_API_KEY=sk-你的key        # Linux / macOS
$env:A7W_API_KEY="sk-你的key"        # Windows PowerShell
```

`login` 会用真实接口验证 Key，并把 `key` + `host` 写进 `~/.a7w/config.json`：

```json
{ "key": "sk-xxxx", "host": "https://api.a7w.cn" }
```

验证当前 Key：

```bash
python3 scripts/client.py whoami
```

## 5. Key 的安全底线

- **不要硬编进代码**，不要提交进 Git，不要贴进聊天记录或 issue。
- 本机配置由脚本设为 `600`（仅本人可读写）。
- Key 一旦外泄，等于把余额交出去——立刻到用户中心删除并重建。
- 本 Skill 的脚本**不内嵌任何密钥**，只从 `~/.a7w/config.json` 或 `A7W_API_KEY` 读，并且只把请求发往 `api.a7w.cn`。

## 6. 跑通第一个请求

```bash
# ① 看有哪些模型
python3 scripts/client.py models --filter deepseek

# ② 调一次（模型网关）
python3 scripts/client.py chat --model DeepSeek-V4-Flash --prompt "用一句话解释什么是向量数据库"

# ③ 看有哪些生成类应用
python3 scripts/client.py apps --brief

# ④ 看某个应用的接口与参数
python3 scripts/client.py schema voice_tts
```

四步都通了，就说明鉴权、网络出口、Key 权限、点数余额四项都是好的。

## 7. 内网 / CI 环境注意

脚本只访问 `https://api.a7w.cn`（443）。内网、容器或 CI 需要放行该域名，否则会报网络错误（退出码 3），而不是鉴权错误——**先分清是网络不通还是 Key 不对**：`whoami` 能区分，它会报告每个候选端点的实际 HTTP 状态。

## 8. 下一步

| 你要做的事 | 看哪份 |
|---|---|
| 用 OpenAI SDK 接代码 | `api-openai-compat.md` |
| 提交图像/视频/语音任务 | `api-apps-tasks.md` |
| 估算成本、查错误码 | `api-billing-errors.md` |
| 记住 CLI 命令 | `client-cli.md` |
