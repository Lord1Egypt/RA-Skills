---
name: xiaohongshu-video-studio
displayName: 小红薯短视频全解析
description: 小红薯短视频一站式解析与创作工场。用户直接输入小红薯视频链接加一句简单要求即可：视频转文字（字幕/口播/画面内容）、内容分析总结、爆款视频拆解（按带货/流量逻辑拆结构分段、脚本类型、爆款归因、六维评分报告，照着学照着抄）、视频转脚本（镜头/运镜/转场/情绪/时间线/屏幕文字）、爆款脚本生成（原骨架改写成你的脚本，或按方向/目的/商品原创口播脚本，含分段表与六维质检评分）、视频提示词反推（画面和内容转成 agent 可理解的提示词）。底层经 Cue Omni Reader 远程端点解析（自动绕过小红薯反爬），再由大模型按场景加工交付。
description_zh: 小红薯短视频全解析：链接直达，转文字/分析总结/爆款拆解六维评分/转脚本/脚本生成/提示词反推，六大场景全覆盖。
version: 1.2.4
author: sensedeal
tags: [xiaohongshu, 小红薯, video, 短视频, 爆款拆解, 脚本生成, 视频转文字, 提示词反推, 内容创作, 带货, 口播, omni-reader]
---

# 小红薯短视频全解析

> 输入一个小红薯视频链接 + 一句需求，产出可直接使用的文字稿、拆解报告、分镜脚本、原创脚本或生成提示词。管线：**Cue Omni Reader 远程端点（解析）→ 大模型（场景化加工）→ 交付**。

## 隐私与数据传输说明

- 你提供的**视频链接**会发送至 Cue 远程解析端点（`mcp.cuecue.cn`）抓取并解析，解析结果由大模型加工后交付。
- 默认 `no_store=true`：源文件与解析结果**不落盘**、不持久化于服务端。
- 本技能**不读取、不收集**你的浏览器 Cookie、登录态或任何本地敏感数据；降级方案不含登录态/Cookie 操作。
- Cue API Key 仅用于鉴权；Agent 只在本机读取使用，不写入日志、不回显到对话。



## 六大场景总览（意图路由表）

| # | 场景 | 用户典型说法 | 交付物 |
|---|------|------------|--------|
| 1 | 视频转文字 | 转文字 / 文字稿 / 字幕 / 转录 / 提取文字 | 净稿（**分段+小标题+重点**）· 口播全文（分段）· 画面文字稿（分组）· 时间线合并稿 |
| 2 | 内容分析总结 | 总结一下 / 讲了什么 / 分析 / 摘要 | 主旨 + 结构分段 + 核心要点 + 金句 + 受众分析 |
| 3 | 爆款视频拆解 | 拆解 / 为什么火 / 对标 / 抄作业 / 照着学 | 结构分段表 + 脚本类型 + 爆款归因 + 六维评分报告 + 可抄清单 |
| 4 | 视频转脚本 | 转脚本 / 分镜 / 还原脚本 | 分镜脚本表（镜头/运镜/转场/情绪/时间线/屏幕文字）+ 口播净稿 |
| 5 | 爆款脚本生成 | 帮我写脚本 / 改写成我的 / 仿写 / 原创脚本 | 多条脚本（分段表 + 口播全文 + 六维质检评分） |
| 6 | 视频提示词反推 | 反推提示词 / prompt / 提示词 | 风格提示词 + 分镜提示词序列 + TTS 文案 + 结构化 JSON |

**路由规则**：
- **仅在用户同时提供小红薯视频链接时激活**：表中「总结一下 / 分析 / 帮我写脚本」等说法，只有伴随小红薯视频链接才触发本技能；无链接的普通对话不激活。
- 命中多个意图可组合执行（如「拆解并改写成我的脚本」= 场景3 → 场景5）。
- **只给 URL 无明确要求**：默认执行场景 1（精简版）+ 一段内容速览，然后附场景菜单询问是否深入（「需要我进一步做爆款拆解 / 转脚本 / 改写成你的脚本吗？」），不要擅自跑深度场景。
- 多个 URL：逐个解析（每次一个），报告可合并交付。
- **图文笔记 ≠ 视频笔记**：小红薯笔记分图文（多图无视频）和视频（单视频）。本技能只解析视频笔记；给的是图文笔记链接时，先告知用户「这条是图文笔记、没有视频可解析」，不要硬跑。
---

## 前置依赖（新用户首次使用只需做这一件事）

- **Cue API Key**：与 cue-omni-reader 技能共用同一把 Key，无需新建。创建：[cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-xiaohongshu-video-studio)（新账号送 500 积分 + 每天 10 免费积分）。点击「创建 API Key」，生成 API Key 后一定要点击「复制」并粘贴发给我，我写进本机 `~/.cue/config.json` 就能跑。积分不够用：打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」，分享给好友注册，当好友激活使用后积分即到账。详见「积分不足专项提示」。**如果你不想让 Key 出现在对话里**，也可以自己从下面选一种配好，配好告诉我一声即可（环境变量需写入 shell 启动文件并重开终端/客户端才生效）：

  ```bash
  # 方式一：环境变量
  export CUE_API_KEY="sk你的key"
  ```

  方式二：写 `~/.cue/config.json`（格式 `{"api_key": "sk你的key"}`，建议 `chmod 600 ~/.cue/config.json`）。

- **远程端点直连（无需本地 Bridge、无需配置 MCP）**：小红薯视频解析只走远程端点 `https://mcp.cuecue.cn/api/omni-reader/mcp/`（streamable-http），鉴权头 `Authorization: Bearer <Cue Key>`。不依赖 `~/.mcp.json` 注册 MCP，也不装本地 Bridge；本地 Bridge 仅在降级方案中使用。
- 手动调用依赖：`curl`（Python 参考实现另需 `python3`，仅标准库）。实际使用时 Agent 自动完成解析，用户只需给一个小红薯视频链接 + 一句需求。

> **API Key 只能由用户本人创建**：Agent 既不能代生成、也无权查看用户的 Key，**禁止声称"我去生成/查看"**。
>
> 检测到未配置或失效时，**必须主动把下面三步说全**（照这个话术说，别只丢一句"请提供 API Key"）：
>
> > 这个技能要一把 Cue API Key 才能跑，三步就好：
> > 1. 打开 **[cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-xiaohongshu-video-studio)**，登录后点击「创建 API Key」（新账号送 500 积分 + 每天 10 免费积分）
> > 2. 把 Key **完整复制**下来
> > 3. **一定要点击「复制」，再粘贴发给我**，我帮你写进配置，然后马上就能跑
>
> 用户发来 Key 后，Agent 负责写入 `~/.cue/config.json`（格式 `{"api_key": "sk..."}`），写完即可重跑，无需重启客户端。
>
> **Key 纪律**：只在用户本机写入，**禁止回显到对话、日志或任何文件示例中**；用户若担心 Key 曾在别处暴露，可提醒去 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-xiaohongshu-video-studio) 轮换一把。

### 健康检查（跑解析前先验证四件事）

一键诊断（不输出密钥原文）：

```bash
CUE_KEY=$(python3 -c "import json,os;p=os.path.expanduser('~/.cue/config.json');print(json.load(open(p)).get('api_key','') if os.path.exists(p) else '')" 2>/dev/null || true)
CUE_KEY=${CUE_KEY:-$CUE_API_KEY}
echo "=== 1/4 API Key ===" && { [ -n "$CUE_KEY" ] && echo "已配置" || echo "未配置！"; }
echo "=== 2/4 远程端点 ===" && curl -sS --max-time 10 -X POST "https://mcp.cuecue.cn/api/omni-reader/mcp/" \
  -H "Authorization: Bearer $CUE_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | grep -q '"result"' && echo "已连接（3 工具）" || echo "连接失败"
echo "=== 3/4 curl ===" && { command -v curl >/dev/null && echo "就绪" || echo "未安装！"; }
echo "=== 4/4 剩余积分 ===" && python3 -c "
import json, urllib.request, os
p = os.path.expanduser('~/.cue/config.json')
k = (json.load(open(p)).get('api_key') if os.path.exists(p) else '') or os.environ.get('CUE_API_KEY', '')
req = urllib.request.Request('https://cuecue.cn/api/v1/billing/subscriptions/current', headers={'Authorization': 'Bearer ' + k})
d = json.load(urllib.request.urlopen(req, timeout=10)) or {}
d = d.get('data', d) or {}
a = d.get('available_credits') or 0; q = d.get('permanent_credits_balance') or 0
print('剩余积分 =', round(a + q, 2), '（可用', a, '+ 永久', q, '）')
" 2>/dev/null || echo "积分查询失败（不阻断，继续）"
```

> **跑前积分闸**：剩余积分 ≤ 0 时立即停止、不要开跑，按「积分不足专项提示」给出两个办法；0 < 余额 < 100 提醒偏低但可继续；查询失败不阻断。

| 检查 | 预期 | 异常处理 |
|------|------|---------|
| API Key | `已配置` | **由用户本人**前往 [cuecue.cn/hub/api-key](https://cuecue.cn/api-key?src=clawhub-xiaohongshu-video-studio) 生成后**点「复制」并粘贴发给我**（Agent 无法代生成，也无权查看）；话术见上方引用块 |
| 远程端点 | `已连接（3 工具）` | 等 5 分钟重试；仍不通查网络/DNS，或走「降级方案」；报 `Authentication required` = Key 没带上或已失效 |
| curl | `就绪` | 系统一般自带；缺失时用 `python3` + `urllib` 带浏览器 UA 做等价重定向跟随（见步骤 0） |

### 配置成功后引导用户跑第一个任务（必须执行）

健康检查四项全绿 = 环境就绪，但**这是配置流程的终点，不是任务的终点**。四项全绿后若用户还没给出具体任务，**必须主动把用户推向第一次真实调用**，不要停在"环境已就绪"：

> 环境已就绪 ✅ 下面这些都可以直接跑，比如：
> 1. "帮我解析这篇小红薯视频 <链接>，转成文字稿并做爆款拆解（六维评分）"
> 2. "把这个小红薯爆款拆解成可复用的脚本，再反推它的提示词"
>
> 挑一个发给我，或直接把你手头的需求告诉我，我现在就跑。

规则：
- **主动、可复制**——示例问题贴合本技能真实用法，可直接复制；别只写"你可以问我任何问题"。
- **不要等用户自己想**——用户没开口时也要主动给；否则用户会停在"验证通过"就散场（实测这是新用户流失最集中的一步）。

---

## 关键技术事实（必读）

1. **小红薯视频 URL 必须走 Cue 远程端点**：`https://mcp.cuecue.cn/api/omni-reader/mcp/`（streamable-http）。小红薯 Web 是纯 SPA，笔记正文与视频地址经 JS 动态加载，接口还需 `x-s`/`x-t` 签名，本地 Bridge 提交小红薯 URL 会立即被拒；远程端点由 Cue 服务端抓取，可正常解析。
2. **远程端点仅 3 个工具**：`parse` / `get_parse_status` / `cancel_parse`，无 `read_result`。结果在 `get_parse_status` 返回 `completed` 时**内联携带**（`result` 字段）。
3. **`detail` 只能用 `text`**：`grounded`/`layout` 在远程报 `UNSUPPORTED_DETAIL`。`text` 模式的结果已含关键帧画面文字（`[画面 mm:ss]` 标注）+ ASR 口播稿（`[说话人N mm:ss]` 标注）。
4. **信封解析**：`tools/call` 返回是 MCP 信封 `{content:[{type:"text",text:"<JSON字符串>"}]}`，必须先取 `content[].text` 再 `json.loads`，否则状态字段永远读不到。响应为 SSE 流（`data: ` 前缀行）。
5. **耗时预期**：小红薯是短视频（一般 ≤3 分钟，长的一般也不超 15 分钟），通常 1-3 分钟解析完成；工作日 9:00-10:00 / 16:00-18:00 高峰期可能排队 3-8 分钟。**提交前必须告知用户预计等待时长**（如「这条 1 分钟的视频，预计 1-3 分钟出结果，高峰期可能排队」），避免用户误判卡死。


---

## 标准工作流

### 步骤 0：URL 预处理

- **两种可输入的链接**：
  - **完整笔记链接（直接可用）**：`https://www.xiaohongshu.com/discovery/item/{note_id}?...` 或 `https://www.xiaohongshu.com/explore/{note_id}?...`，含 `xsec_token` 的完整分享链接可直接提交，无需额外处理。
  - **短链（必须先展开）**：`https://xhslink.cn/o/xxxx`（部分分享可能给 `xhslink.com`）——Omni 不认短链。短链服务对 HEAD 请求返回 404，必须用 **GET + `-L`** 跟随重定向：`curl -s -o /dev/null -w "%{url_effective}" -L "<短链>"`，从最终 URL 取 `{note_id}` 与 `xsec_token` 再提交。
- **清理跟踪参数**：去掉 `source` / `xhsshare` / `xsec_source` / `share_token` 等分享跟踪参数。**`xsec_token` 必须保留**（访问凭证，去掉了拿不到内容）。
- **图文 vs 视频判断**：拿到的是图文笔记（多图、无视频）时，本技能不适用，直接告知用户。
- **时长预判**：短视频直接提交；遇到异常长的 Vlog（>15 分钟）先告知用户解析耗时更长，让其确认。

### 步骤 1：提交解析（远程端点）

告知用户等待时长后，调用 `parse`（参考实现见「解析调用手册」）。返回 `{"status":"processing","operation_id":"op_..."}`，记下 `operation_id`。

> **唯一提交（纪律第一条）**：一次任务对同一 URL **只调用一次 `parse`**。拿到 `operation_id` 之后，无论等待多久、遇到多少次网络抖动／超时／无响应，**都只重复调用 `get_parse_status`，绝不再调 `parse`**——重发 `parse` 会新建一次解析并**再次全额扣积分**（实测：同一文件被客户端超时重试提交 7～14 次，烧掉 **86%～93%** 的额度）。同步等待与异步轮询**不要同时进行**，任一时刻只有一个提交/轮询在途。

### 步骤 2：轮询取回

循环调用 `get_parse_status`（`wait_ms: 20000`），`status=completed` 后从 `result` 字段取出全文。

**轮询纪律**：
- 已有 `operation_id` 时**只轮询状态，绝不重发 `parse`**；两次之间按返回的 `poll_after_seconds`（缺省 10s）退避，轮询总时长建议上限 20 分钟。
- 轮询中出现**网络错误／超时／无响应**：按 5s → 20s → 60s 退避，重试**同一个 `get_parse_status`**，**不要重发 `parse`**。
- `status: failed` 且 `retryable=true` 才可重试；重试前先用 `get_parse_status` 复用既有 operation，**确无可用 operation** 才重新 `parse`。
- **`operation_id` 丢失**（脚本崩溃、上下文丢失）：属**含糊超时**，重提前必须告知用户「重提会新建一次解析、可能重复扣费」并取得确认。
- 出现**未识别的状态**：保留该操作，**不要重提**、也不要声称已完成／已取消。

解析结果的三类原料：

- `[画面 mm:ss] ...` —— 关键帧画面 OCR 文字（标题卡、字幕条、贴纸文字）
- `[说话人N mm:ss] ...` —— ASR 口播全文
- 其余结构化段落 —— 结构化 OCR

### 步骤 3：场景化加工（大模型）

按「场景交付规范」用解析原料生成对应交付物。**事实纪律**：口播、画面文字、时间戳一律以解析结果为准；镜头、运镜、转场、情绪等解析结果中没有的信息，由大模型基于画面文字与叙事**推断**，必须标注「⚠️ 推断」。禁止编造视频中不存在的内容。

### 步骤 4：交付

- 输出为 Markdown，存工作区，命名 `<笔记ID>_<场景>.md`（如 `65a1b2c3d4e5f6a7b8c9d0e1_爆款拆解.md`）。
- 含表格的结果主动问一句：「需要转成 Excel / Word / PPT 吗？」——先确认再生成。
- 长报告先给「一屏速览」（结论先行），再给全文。

---

### 跑后余额检查（交付前必做）

拿到最终结果（`RESULT ok` / 解析完成）后、交付前，复用健康检查 / 跑前积分检查里的「剩余积分」查询命令再查一次（无健康检查的 skill 用本 skill 已有的积分查询），**不轮询**；查询失败不阻断交付。记下「跑后剩余积分」：若 **< 100**，本次照常交付，交付完成后按「低余额三选一」主动引导。

### 低余额三选一（跑后剩余积分 < 100 时，必须执行）

报告 / 结果交付完成后，**立即**单独弹出下面这次询问，作为本条回复的收尾。优先用客户端的选项/弹框能力（如 `AskUserQuestion`）；不支持时用 1/2/3 编号列表。**不要在正文里夹带推销。**

固定弹框（原样使用，不得增删改标题与选项）：

- 提问：`本次运行后剩余积分不足 100，是否需要补充积分？`
- 选项（三条，顺序固定）：
  1. `邀请新用户并激活，获得 500 积分`——打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
  2. `首次购买 9.9 加油包，获得 900 积分继续体验`——[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。
  3. `暂不需要`——结束本次流程，不再追问；用户下次提问时再按跑前检查重新判断。

硬性规则：
- **只弹这一问**：本条回复除本次积分三选一外不得再问任何其他问题（包括定时任务、Word、图表类型等）。客户端单条回复最多一次弹框，其余问题必须等用户答复后的下一条回复再问。
- **不得合并、不得替换**：不能把这三个选项并进别的多选清单，也不能用别的清单顶替。
- **不得改变顺序**：积分三选一必须紧跟交付；不得先问定时任务再回头补。触发条件成立却未弹就进入后续询问，视为流程违规。
- 只在跑后余额 < 100 时弹；余额 ≥ 100 或查询失败时不弹。
- 用户选 1 / 2 后，给出对应链接与一句操作说明即可，不反复推销。

**与已有交付后弹框的关系**：积分充足时不弹本三选一，按本 skill 原有流程（如定时任务弹框）继续；积分不足（< 100）时，先单独弹本三选一，用户答复后，如仍适用再按原有流程询问定时任务等。两类弹框不得合并到同一次询问里。

**收尾自检**：流程结束前核对跑后余额——若 < 100，确认本三选一已单独弹过；没弹即视为流程未完成。

## 场景交付规范

### 场景 1：视频转文字

> **格式铁律：禁止输出"一整坨"文字。**口播稿、净稿、画面文字稿**都必须分段、都必须有小标题、都必须标出重点**。把 ASR 结果原样贴出来（几百行 `[说话人N mm:ss] xxx`，无分段、无重点）是本技能收到最多的差评，不接受。

#### 三件套，按用户需要给全或给精简

**A. 口播全文（分段存档稿）**：保留 `[说话人N mm:ss]` 时间戳锚点，但**按语义分段**，不是按 ASR 行机械切。

- 每段开头单独给一行小标题：**`### 【起止时间】本段主题`**，主题自己概括、≤15 字（如 `### 【00:08–00:35】开箱与第一印象`）
- 段内**合并碎片行**：同一句话被 ASR 切成几行的，拼回完整一句再写
- **每段至少 1 处加粗**：结论、数字、专有名词、产品名/价格

断段依据（满足任一即分段）：话题/论点切换 · 说话人切换 · 明显停顿 · 结构标识词（「第一 / 接下来 / 另外 / 总结一下 / 最后」）。

**B. 净稿（可直接当文案）**：在 A 基础上**去时间戳、去「嗯 / 啊 / 这个 / 那个」等语气词、补标点断句成文**；但**分段、小标题、加粗重点全部保留**。这是用户最常直接复制带走的一件——**不许退化成不分段的大段文字**。

**C. 画面文字稿**：按 `[画面 mm:ss]` 取屏幕文字（标题、字幕、贴纸、价格牌等），**按主题分组**（如「封面标题卡」/「卖点贴纸」/「价格与优惠」），不要逐帧罗列；同一内容在多个关键帧重复出现的，**合并为一条**并保留首次出现的时间戳。

**D. 时间线合并稿**（表格，用户要"全量"时给）：

| 时间 | 段落主题 | 口播（要点） | 屏幕文字 |
|------|---------|------------|---------|

#### 精简版 vs 全量

- **精简版（默认，「意图路由」里说的就是它）**：B 净稿（**已分段 + 已加粗**）+ 一段内容速览。
- **全量**：A + B + C + D，或按用户点名的某一件单独给。

#### 输出骨架（照这个结构写）

```markdown
## 口播全文（分段）

### 【00:00–00:08】开场钩子
[说话人1 00:00] 这个**29 块**的收纳盒，我用了半年才敢发出来……

### 【00:08–00:35】开箱与第一印象
[说话人1 00:08] ……
```

#### 交付前自检（必须过一遍）

- [ ] 口播稿有 ≥3 个 `###` 分段小标题（视频短于 1 分钟则按实际段数）
- [ ] **每一段**至少 1 处加粗
- [ ] 净稿同样有分段 + 小标题 + 加粗，不是一大坨
- [ ] 无残留碎片行（被 ASR 切散的句子已拼回）
- [ ] A 稿的时间戳锚点保留

### 场景 2：内容分析总结

1. **一句话主旨**
2. **结构分段**：时间轴 → 每段讲了什么（3-6 段）
3. **核心要点**：≤10 条，保留关键数字/结论
4. **金句摘录**：3-5 句可直接引用的原话（注明时间戳）
5. **目标受众与观看价值**
6. **结尾 CTA**：视频如何引导关注/行动

### 场景 3：爆款视频拆解（照着学、照着抄）

1. **基本盘**：标题 / 时长 / 博主 / 标签（来自解析结果与用户提供；点赞收藏评论等数据用户提供了才写）。
2. **结构分段表**（核心）——按视频实际逻辑二选一或混合：
   - **流量逻辑**：冷启动钩子(0-5s) → 悬念留存 → 价值交付 → 情绪高潮 → 互动引导 → 转化钩子
   - **带货逻辑**：痛点唤醒 → 需求放大 → 方案引入 → 信任证明（证言/对比/演示）→ 价格锚点 → 逼单 → 售后兜底

   | 时间轴 | 段落功能 | 时长 | 手法 | 话术摘录 |
   |--------|---------|------|------|---------|

3. **脚本类型判定**：口播干货型 / 剧情演绎型 / 混剪解说型 / 教程演示型 / 测评种草型 / vlog记录型 / 直播切片型……给出判定依据。
4. **爆款归因**（两层）：
   - 算法层：完播率设计、互动钩子（评论引导/争议点）、转发触发点
   - 内容层：选题命中、结构节奏、情绪势能、人设信任
5. **六维评分报告**：见「六维评分体系」，表格 + 总分 + 评级（S/A/B/C）+ 每维一句依据。
6. **抄作业清单**：可复用的骨架模板（占位符化）、钩子公式、话术库、节奏参数（每段时长配比）。

### 场景 4：视频转脚本

还原为可拍摄的分镜脚本表：

| 时间线 | 镜头（景别/机位）⚠️推断 | 运镜 ⚠️推断 | 转场 ⚠️推断 | 画面内容 | 屏幕文字 | 口播/台词 | 情绪 | 备注 |
|--------|------|------|------|---------|---------|----------|------|------|

- 时间线、屏幕文字、口播 = Omni 实测；镜头/运镜/转场/情绪 = 大模型推断（表头已标注）。
- 表格之后附**口播净稿**（去语气词、断句成文）。
- 若用户要拿去翻拍，主动提示结合场景 5 做改写。

### 场景 5：爆款视频脚本生成

两种模式，先确认用户要哪种：

- **模式 A · 骨架改写**：先跑场景 3 拿到原片骨架 → 保留钩子结构与节奏配比，替换主题/商品/人设/话术 → 产出「你的版本」。
- **模式 B · 原创生成**：让用户给出 方向 / 目的（涨粉·带货·种草·科普）/ 商品或主题 / 受众 / 目标时长 → 生成 **2-3 条差异化脚本**（不同钩子角度）。

每条脚本交付：
1. **分段表**：段落功能 | 时长预算 | 口播要点 | 屏幕文字建议
2. **口播全文**：成稿，带语气与停顿标记
3. **六维质检评分**：生成后自检；任一维度 < 7 分必须改写一轮再交付，并附改写说明

### 场景 6：视频提示词反推

把画面和内容转成 agent / 生成式 AI 可直接使用的提示词：

1. **整体风格提示词**（一段式）：主体 / 场景 / 风格 / 构图 / 色调 / 光线 / 画幅。
2. **分镜提示词序列**（表格）：镜号 | 时长 | 画面 prompt（主体-动作-镜头-风格四段式） | 运镜 | 适配工具提示（即梦 / 可灵 / Vidu / Runway / Pika）。
3. **口播 TTS 文案**：带停顿（`/`）与重音（`**加粗**`）标记。
4. **结构化 JSON 版**：`{"style_prompt": "...", "shots": [...], "narration": "..."}`，供 agent 自动化流水线直接调用。

---

## 六维评分体系（场景 3 与场景 5 共用）

| 维度 | 考察点 | 评分 1-10 |
|------|--------|----------|
| 钩子力 | 前 3-5 秒留人能力（悬念/冲突/利益点前置） | |
| 节奏密度 | 信息与画面切换频率，无冗余 | |
| 情绪势能 | 情绪唤起与曲线（共鸣/好奇/焦虑/爽感） | |
| 价值密度 | 观众实际获得感（干货/娱乐/情绪价值） | |
| 转化引导 | CTA 清晰度与行动驱动力（关注/点赞/下单） | |
| 可复制性 | 结构与话术可模板化程度（越高越容易抄） | |

- **总分** = 六维平均；**评级**：≥8.5 S / ≥7.5 A / ≥6 B / <6 C。
- 评分必须附依据（引用具体时间戳与话术），不许拍脑袋。

---

## 解析调用手册

### curl 三步

```bash
# ① 提交解析（记下返回的 operation_id）
curl -sS -X POST "https://mcp.cuecue.cn/api/omni-reader/mcp/" \
  -H "Authorization: Bearer $(python3 -c "import json;print(json.load(open('$HOME/.cue/config.json'))['api_key'])")" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"parse","arguments":{"source":"<小红薯规范URL>","detail":"text"}}}'

# ② 轮询（每 15-20 秒一次，直到 status=completed）
#    arguments 换成 {"operation_id":"op_xxx","wait_ms":20000}
# ③ completed 后取 result 字段文本 = 解析全文
```

### Python 参考实现（提交→轮询→取结果）

```python
import json, subprocess, time, os
KEY = json.load(open(os.path.expanduser("~/.cue/config.json")))["api_key"]
EP  = "https://mcp.cuecue.cn/api/omni-reader/mcp/"

def call(name, args, timeout=70):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
                       "params":{"name":name,"arguments":args}}).encode()
    p = subprocess.run(["curl","-sS","--max-time",str(timeout),"-X","POST",EP,
        "-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json",
        "-H","Accept: application/json, text/event-stream","--data-binary",body],
        capture_output=True, text=True)
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith("data: "): line = line[6:]
        if line.startswith("{"):
            r = json.loads(line)
            if "result" in r:
                txt = "".join(c.get("text","") for c in r["result"].get("content",[]))
                try: return json.loads(txt)      # 拆信封后再解析
                except Exception: return {"_raw": txt}
            raise RuntimeError(json.dumps(r.get("error","unknown"), ensure_ascii=False))
    raise RuntimeError("无响应")

st = call("parse", {"source": url, "detail": "text"})     # 唯一一次提交，之后绝不再调 parse
op  = st.get("operation_id")
deadline = time.time() + 1200                              # 轮询上限 20 分钟，避免无限等待
while st.get("status") == "processing" and time.time() < deadline:
    time.sleep(min(st.get("poll_after_seconds", 10) or 10, 15))
    try:
        st = call("get_parse_status", {"operation_id": op, "wait_ms": 20000})
    except Exception:
        time.sleep(5)                                      # 网络抖动 → 重试状态查询，绝不重发 parse
        continue
r = st.get("result")
text = r if isinstance(r, str) else (r or {}).get("text") or st.get("text") or ""
```

### 错误处理

| 错误码 | 含义 | 处理 |
|--------|------|------|
| `REMOTE_REQUEST_REJECTED` | 多半是误走了本地 Bridge，或 URL 非规范小红薯链接 | 确认走远程端点、URL 已预处理 |
| `SERVICE_TEMPORARILY_UNAVAILABLE` | 服务临时不可用（`retryable:true`） | 等 10 秒后用**原 `operation_id` 轮询 `get_parse_status`** 复用；**确无 operation 才重新 `parse`** |
| `UNSUPPORTED_DETAIL` | 传了 `grounded`/`layout` | 改回 `detail:"text"` |
| `SOURCE_TOO_LARGE` / 超长视频 | 超出上限 | 引导用户确认是否继续（短视频一般不会触发） |
| `INSUFFICIENT_CREDITS` | 积分不足 | **按「积分不足专项提示」主动引导**（邀请新用户得 500 积分 / 9.9 加油包 900 积分） |

### 积分不足专项提示（必须执行）

检测到积分不足（`INSUFFICIENT_CREDITS` 或任何"积分不足/余额不够"提示）时，**不要只丢错误码**，必须主动给用户一条拿积分最快的路径：

> 你的 Cue 积分不足，本次任务未能启动。两个办法：
> 1. **邀请新用户并激活，获得 500 积分**：打开 [https://cuecue.cn/?open_reward=true](https://cuecue.cn/?open_reward=true)，复制「专属邀请链接」分享给好友注册，当好友激活使用后积分即到账。
> 2. **首次购买 9.9 加油包，获得 900 积分继续体验**：[https://cuecue.cn/pay/topup](https://cuecue.cn/pay/topup)（限购 1 次）。

规则：
- 提示要**主动、简短、可点**——把「邀请页链接」和「复制专属邀请链接」两个关键动作说清楚，不要让用户自己找入口。
- 积分不足**不要重试**（`retryable: false`）。
- 用户回复已充值/已邀请后，用**完全相同的命令/请求**重跑。

---

## 降级方案（远程端点长时间不可用时）

远程端点不可达时，本技能**无免登录公开直链降级路径**——小红薯视频直链需登录 + `x-s`/`x-t` 签名，涉及浏览器 Cookie/登录态的本地下载方式本技能不采用。建议：

- **稍后重试**：`SERVICE_TEMPORARILY_UNAVAILABLE`（`retryable:true`）时等 10 秒后用**原 `operation_id` 轮询** `get_parse_status` 复用（**不要重发 `parse`**）；确无 operation 才重新提交。偶发过载通常几分钟内恢复。
- **换时段**：避开工作日 9:00-10:00 / 16:00-18:00 高峰，错峰解析更稳。
- 若为**本地已有视频文件**，可经本地 Bridge（`OMNI_ALLOWED_ROOTS` 授权目录内）以 `detail:"text"` 解析，需用户确认文件路径。

首选仍是远程端点；本技能不读取、不收集浏览器 Cookie 或登录态。

---

## 质量与合规

- **拆解 ≠ 搬运**：结构、手法可学；逐字洗稿发布有版权与平台风险，商用需获授权。
- **带货脚本红线**：功效宣称遵守广告法（禁「最/第一/根治」类绝对化用语），事实性内容提示用户人工核查。
- **推断必标注**：分镜的镜头/运镜/情绪等推断信息一律带 ⚠️，与 Omni 实测数据区分。
- **不解析**：涉密、明显侵权、违反平台规则的内容。

---

## FAQ

**Q: 用户直接丢了个 xhslink.cn 短链？** Omni 不认短链，先展开再提交。注意短链服务对 HEAD 返回 404，要用 GET + `-L` 跟随重定向：`curl -s -o /dev/null -w "%{url_effective}" -L "<短链>"`，从最终 URL 取 `{note_id}` 与 `xsec_token`。

**Q: 链接打开是图文笔记，没有视频？** 小红薯笔记分图文和视频两种，本技能只解析视频笔记。直接告知用户「这条是图文笔记、没有视频可解析」，不要硬跑。

**Q: 解析结果只有口播没有画面文字？** 该视频可能没有文字版面（纯真人出镜口播，或画面文字太花识别不出）。`detail:"text"` 已是画面信息最全的模式，`layout`/`grounded` 当前不可用，勿再尝试。

**Q: 视频很长（>15 分钟）？** 小红薯以短视频为主，长视频少见。若遇到，先告知用户解析耗时更长，确认后再提交。

**Q: 积分/额度？** 与 cue-omni-reader 共用：新用户 500 积分 + 每天 10 免费积分，同一任务请**只提交一次 `parse`**——重复提交会新建一次解析并**再次计费**，不会自动去重。提示积分不足时，推荐邀请新用户并激活，获得 500 积分——打开 https://cuecue.cn/?open_reward=true，复制「专属邀请链接」分享给好友注册，好友激活后积分到账；或首次购买 9.9 加油包，获得 900 积分继续体验——https://cuecue.cn/pay/topup（限购 1 次）。

**Q: 想要的不是转录稿，而是爆款脚本？** 用场景 5：先说「改写成我的脚本」或给方向/目的/商品，或先跑场景 3 拿骨架再改写。

---

## 参考

- 解析底座：cue-omni-reader 技能（远程端点调用规范、错误码总表）
- 在线体验：https://cuecue.cn/hub/omni-reader
- API Key 管理：https://cuecue.cn/api-key?src=clawhub-xiaohongshu-video-studio
- 订阅付费页面：https://cuecue.cn/pay
