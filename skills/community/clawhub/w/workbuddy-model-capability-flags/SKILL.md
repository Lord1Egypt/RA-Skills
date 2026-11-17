---
name: workbuddy-model-capability-flags
description: 排查并修复 WorkBuddy 里自定义模型「不支持读图 / 不调用工具 / 不能推理」的能力位标错问题，以及新增自定义模型（OpenCode Zen、自建或其他厂商的 OpenAI 兼容端点）时一次性探测能力位并生成配置。当用户说「为什么说不支持读图」「模型读不了图片」「附件发不进去」「custom-local 模型能力不对」，或问「加新模型要测什么」「怎么知道这个模型支持读图/思考强度」时使用。含通用探测器 probe_model.py（一条命令测出读图/工具调用/effort 档位）、能力位定位法、直连端点自证法、以及「改完必须重启」这一必踩的坑。
slug: workbuddy-model-capability-flags
displayName: WorkBuddy 自定义模型能力位排查（读图/工具/推理）
version: 1.0.0
category: development
visibility: public
license: MIT
agent_created: true
---

# WorkBuddy 自定义模型能力位排查

## 症状

用 `Read` 读图片（png/jpg/jpeg/gif/webp/bmp）时返回：

```
Error: Current model (custom-local:<model-id>) does not support reading images
```

**关键判读**：这是**本地元数据拦截**，不是网络错误、不是模型真的不支持。
请求根本没发出去。

## 根因

`C:\Users\DELL\.workbuddy\models.json` 里每个模型的能力位被标错，最常见的是 `supportsImages: false`。

判定代码（v5.6.2 实测）在
`<安装目录>\resources\app.asar.unpacked\cli\dist\codebuddy-lite-wb.mjs` 的 Read 工具分支：

```js
if(await this.isImageFile(el, ea.context)){
  let ei = await nY.ModelUtils.getCurrentModel(ea.context);
  if(ei?.supportsImages === !1){        // ← 严格等于 false 才拦
    return { content: `Error: Current model (${ei.id}) does not support reading images`, ... }
  }
```

注意是 `=== false`（严格）。理论上把字段**删掉**（undefined）也能绕过，但不建议 —— 应用会在启动时重写该文件。

`getModelsPath()` 的读取位置：
- WorkBuddy 产品：`~/.workbuddy/models.json`
- 其他产品：`~/.codebuddy/models.json`
- 可用环境变量 `CODEBUDDY_CONFIG_DIR` 覆盖

## 排查步骤

### 0. 加新模型 / 改配置前，先跑通用探测器（推荐第一步）

本技能自带 `probe_model.py`，**探测读图、工具调用、思考强度档位三件事**，
`--apply` 可直接把结论写回 `models.json`（自动备份）：

```bash
# 探测 models.json 里全部模型（只读，不改文件）
python probe_model.py

# 探测 + 直接写回配置（改前自动备份到 ~/.workbuddy/backups/）
python probe_model.py --apply

# 加一个全新模型：先追加条目，再探测，再按探测结果填能力位
python probe_model.py --add --model my-new-model \
  --url https://api.example.com/chat/completions --key sk-xxx \
  --name "My Model" --vendor "Example"

# 常用组合
python probe_model.py --model deepseek-v4-flash          # 只探一个
python probe_model.py --model xxx --no-vision             # 纯文本模型，省一次大请求
python probe_model.py --model xxx --image D:\pics\t.jpg   # 用自己的图
python probe_model.py --apply --default-effort high       # 强制指定默认档位
```

**`--apply` 的安全设计**（都已实测）：
- 只改 `supportsImages` / `supportsToolCall` / `supportsReasoning` / `reasoning`，
  **绝不碰** `id` / `name` / `url` / `apiKey`
- 写前自动备份到 `~/.workbuddy/backups/models.json.bak-probe-<时间戳>`
- 结论与现状一致 → **不重写文件**（避免无谓的重启要求）
- 探测结果全部不完整（网络故障/限流伪装成"全不支持"）→ **拒绝写入**，需 `--force` 才强写
- 单项探测异常 → **保留原值**，绝不把已验证的 `true` 降级成 `false`
- **保留你已有的 `defaultEffort`**（只要它还在探测到的可用档位里）
- 探测确认不支持推理 → 自动删除遗留的 `reasoning` 块，避免自相矛盾配置

回归测试（改动脚本后务必跑）：
```bash
python test_apply_logic.py        # 17 项，覆盖写入/幂等/降级保护/备份
python test_vision_stability.py   # 读图判定稳定性（需联网）
```

**能照抄结论就别手写探测脚本** —— 手写一次要花掉半小时，且极易漏掉假阴性那个坑。

### 1. 看当前模型和标记

```bash
python -c "
import json
d=json.load(open(r'C:\Users\DELL\.workbuddy\models.json',encoding='utf-8'))
for m in d: print(m['id'].ljust(22),'images =',m.get('supportsImages'))
"
```

报错信息里的 `custom-local:<id>` 就是当前模型 id。

### 2. 直连端点自证「模型其实支持图片」

**不要凭猜测改配置**，先实测端点。用该模型自己的 url / apiKey：

> ⚠️ **`max_tokens` 必须 ≥ 800**。reasoning 模型会先把 token 花在思维链上，
> 给小了会出现「HTTP 200 但 content 为空」的**假阴性**，让你误判成"模型不支持读图"。
> 这个坑我踩过一次：DeepSeek 读图明明支持，却因为 `max_tokens: 400` 被误判为不支持。

```bash
python -c "
import base64,json,urllib.request
p=r'<图片绝对路径>'
b=base64.b64encode(open(p,'rb').read()).decode()
body=json.dumps({'model':'<model-id>','messages':[{'role':'user','content':[
  {'type':'text','text':'Look at the image. Answer exactly two things on separate lines:\nANIMAL: <the animal>\nSTYLE: <the art style>'},
  {'type':'image_url','image_url':{'url':'data:image/png;base64,'+b}}]}],
  'max_tokens':900}).encode()   # ← 必须 800+，否则 reasoning 吃光 token
req=urllib.request.Request('<模型 url>',data=body,headers={
  'Content-Type':'application/json',
  'Authorization':'Bearer <apiKey>',
  'User-Agent':'curl/8.0'})   # ← 必须带，否则 Cloudflare 挡 403 error code: 1010
r=urllib.request.urlopen(req,timeout=120)
d=json.loads(r.read().decode())
print('HTTP',r.status)
print('finish_reason:',d['choices'][0].get('finish_reason'))
print(d['choices'][0]['message'].get('content'))
print('[reasoning]',(d['choices'][0]['message'].get('reasoning_content') or '')[:200])
print('[usage]',d.get('usage'))
"
```

判读：
- **HTTP 200 且能说出图里内容** → 模型支持，配置标错了，改 `supportsImages: true`。
- ⚠️ **content 为空但 `reasoning_content` 里描述了图像内容 → 也算支持**。
  实测 DeepSeek 用橙圆蓝底测试图时，**6/6 次 content 全空**，但 reasoning 里明确写着
  "an orange circle on a blue background" —— 模型读到了，只是 900 token 全被推理吃掉，
  轮不到写正文。**只判 content 会把"支持"误报成"不支持"。**
- **别用「HTTP 200」当"支持多模态"的证据** —— 必须看 content **或 reasoning** 里有没有
  对图像内容的实际描述。用结构化提问（问形状+颜色，而不是问动物）能一眼看出真读了图还是在编造。
- 提问要和测试图**匹配**：拿几何图形问"什么动物"会让模型答"没有动物"，看起来像失败。
- HTTP 400/422 报 unsupported content type / invalid image → 模型真的不支持，别改。
- 完整响应体要打出来看 `finish_reason` / `message` 的字段名 / `usage`，
  有些端点会把内容放在非标准字段里。
- **纯色/极小图可能被直接拒**（实测 Space Bunny 对 8×8 纯色 PNG 返回 400，
  换 256×256 有内容的图就正常）→ 测试图要有明确视觉内容。

### 3. 改配置（改前必备份）

```bash
cp ~/.workbuddy/models.json ~/.workbuddy/models.json.bak
```

然后编辑目标模型的 `supportsImages`。改完必须校验 JSON：

```bash
python -c "
import json
d=json.load(open(r'C:\Users\DELL\.workbuddy\models.json',encoding='utf-8'))
for m in d: print(m['id'].ljust(22),'images =',m.get('supportsImages'))
print('JSON OK')
"
```

### 4. 重启 WorkBuddy（不可跳过）

**改了不重启 = 无效。** 已实测：
- 代码里虽写了 `watchFile` + `[HotReload]`，但改文件后当前会话仍报错，
  `~/.workbuddy/logs/daemon.log` 里**没有** HotReload 记录。
- daemon 是独立常驻进程，模型元数据在 `daemon-server:daemon-bootstrap` 时载入。
  查 daemon 何时启动：
  ```bash
  cd ~/.workbuddy/logs && grep -a -oE '\{"timestamp":"[^"]+","level":"[^"]+","scope":"daemon-server:daemon-bootstrap"' daemon.log | tail -3
  ```
- 子代理（subagent）继承同一进程的缓存，重启前同样报错。

### 5. 确认重启是否吃掉你的改动

应用启动时 `[LocalModelHardwareGate]` 会重写 models.json。查：

```bash
cd ~/.workbuddy/logs && grep -a "LocalModelHardwareGate" main.log | tail -3
diff ~/.workbuddy/models.json.bak ~/.workbuddy/models.json
```

实测：重写时**保留了**手工改的 `supportsImages`。若发现被还原，说明该模型另有权威来源
（服务端 product config / UI 设置），需从 UI 侧改。

## 已验证事实（2026-09-30）

| 模型 | 官方是否支持图像 | models.json 默认值 | 结论 |
|---|---|---|---|
| space-bunny-free（OpenCode Zen） | 是，text/image/video，1M ctx | `false` | 标错，已改 true |
| deepseek-v4-flash（api.deepseek.com） | 是，实测读出图中动物+画风 | `false` | 标错，已改 true |
| WorkBuddy 官方内置模型（快速/均衡/极致/Hy3/Hy4/GLM/Kimi/MiniMax…） | 是 | 全部 `true` | 正常 |

- 前端**没有**「自定义模型是否支持图片」的 UI 开关（搜过 app.asar，无对应文案），
  只能改 models.json。
- 已有相邻技能 `claude-code-third-party-model`（管 Claude Code 接第三方端点），
  本技能管 WorkBuddy 侧，勿混用。

## 思考强度（reasoning_effort）怎么配

`supportsReasoning: true` 只是**开权限**；真正决定可用档位的是 `reasoning.supportedEfforts`。
**三套枚举互不相同，必须实测，不能照抄任何一方。**

### 用非法值套出服务端真实枚举（最快的一招）

传一个服务端不认的值，报错通常直接把候选列表吐出来：

```bash
# DeepSeek：422 并列出全部合法值
# {"message":"...reasoning_effort: unknown variant `__probe__`,
#  expected one of `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `ultra`, `max`"}
```

### 客户端 UI 的内置枚举（读自 codebuddy-lite-wb.mjs）

```js
["off","minimal","low","medium","high","xhigh","max"]   // off 走 canDisableThinking 单独处理
```

**配置里写客户端不认识的词（如 DeepSeek 的 `none`/`ultra`）不会报错，只会被静默吞掉**，
用户在 UI 里根本选不到 → 只写上面这 6 档。

### 客户端怎么消费 supportedEfforts

`withSupportedEffortsFallback` 把它转成 `thinkingLevelMap`（`effort → effort` 一对一），
再原样发给服务端。所以**写服务端真实接受的词即可**，不需要自己做映射。

### 实测结果（2026-09-30）

| 模型 | 服务端接受 | 写进配置 |
|---|---|---|
| `deepseek-v4-flash` | none/minimal/low/medium/high/xhigh/ultra/max（8 档全通） | minimal…max（6 档） |
| `space-bunny-free` | minimal/low/medium/high/xhigh/max（6 档）；**`none` 和 `ultra` 被拒 400** | minimal…max（6 档） |

Space Bunny 拒 `none`/`ultra` 时只返回一句笼统的
`invalid_request_error: Upstream request failed`，**不会告诉你哪些词合法** → 只能逐档试。

### 两个反直觉的坑

1. **不传 `reasoning_effort` 不代表不推理**。Space Bunny / DeepSeek 不传时照样返回
   非空 `reasoning_content`，只是档位由服务端自定。`defaultEffort` 仍建议显式写，
   这样档位才可预期。
2. **档位更高 ≠ 答得更对**。同一道 bat-and-ball（答案 $0.05），Space Bunny `max` 出现过
   答 $0.10；复测 4 次，`minimal` 2/4、`low` 3/4、`medium`+ 各 4/4。
   **别用"档位高"当"更聪明"的依据**，也别指望调高档位能修好数学错误。
3. **探测工具本身会骗你**。同一张图、同一个模型，判定可能因运气在 true/false 之间跳
   （`max_tokens` 到底够不够看模型当天状态）。所以 `probe_model.py` 的读图判定
   **允许 reasoning 里出现描述就算通过**，并且加了 3 次重试。
   **任何 `--apply` 之前，先看探测输出里 `[1/4] 读图` 那行到底是什么结论**，
   别只看最后的汇总。

## 其他能力位

同一文件里还有同类字段，症状不同根因相同：
- `supportsToolCall: false` → 模型不调工具，只聊天
- `supportsReasoning: false` → 推理档位不生效（`reasoning.supportedEfforts` 也不生效）
- 服务端配置里另有 `disabledMultimodal` —— 那是内置模型的开关，自定义模型不走这里
