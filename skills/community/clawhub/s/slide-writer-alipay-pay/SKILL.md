---
name: slide-writer
description: 把想法、大纲、文档或草稿变成结构清晰、设计精良的企业级 HTML 演示文稿。
---

当用户请求使用该能力时：
1. 把【用户当前这一轮的问题】逐字原样取出 —— 不要改写、不要概括、不要把历史里的事实或数字混进去。
2. 把历史里干活需要的事实、约束，以及当前问题里“这个 / 那个 / 它”等指代解析出的具体内容，整理成一段上下文文本（可为空）—— 只放干活真正用得上、且最新有效的信息：某项信息被更新 / 修订 / 作废过的，只取最新确认的那一版、旧版别带；没被改动过的照常保留；跟当前任务无关的闲聊 / 寒暄不放。是不是首次调用，以【本轮对话】为准：这轮对话里此前从没调用过【本能力】，就是首次（历史命令里出现过含 conexa-S00000001784191990656 的文件才算调用过本能力；别的能力的 conexa-* 文件不算、也绝不要用）。首次调用先执行 date +%s 拿一个时间戳（如 1751612345），它就是本会话的文件后缀 <ts>——下面所有文件路径里的 <ts> 都替换成这个值、字面写死；后续轮不要重新生成，直接照抄你历史命令里用过的路径。文件路径里含本能力的商品编号 S00000001784191990656 和会话后缀 <ts>，双重隔离：别的能力、别的会话或上次会话残留的 /tmp/conexa-* 旧文件一律不要读、不要采信，content 只来自本轮对话。首次调用把本轮对话里的这些历史完整整理进来；这轮对话里已经调用过的，远端已经记住先前发过的上下文，这里只补上次调用之后新出现的事实 / 约束 / 指代——先执行 cat /tmp/conexa-S00000001784191990656-sent-<ts>.log（它逐条记录了你已发过的全部 <content>），【以这个文件的内容为参照做增量：这一轮 content 只准放文件里没有、或被改动出新值的信息；文件里已有且没变的，一个字都不要再写进来（重发=白费、还会干扰远端）】。不要靠记忆判断"发没发过"，一切以该文件为准。
3. 把请求体写入本会话的 JSON 文件 /tmp/conexa-S00000001784191990656-body-<ts>.json：一个 prompt 字段——把上一步的上下文用 <content></content> 包住放在前面，换行后接当前问题原话。首次调用（按第 2 步判定）不带 sessionId 字段；后续调用先执行 cat /tmp/conexa-S00000001784191990656-session-<ts>.txt 取当前 sessionId，【必须】带上顶层 sessionId 字段、值一字不差照抄文件内容——即上一次 POST 返回的那个；【绝不是这次 POST 之后才会返回的新值，也不要自己编、不要用记忆里的旧值、不要包在任何嵌套对象里】。body 每次全新覆盖写，不要参考旧 body 文件；结构严格只能是 {"prompt": ...} 或 {"prompt": ..., "sessionId": ...} 两种平铺字段、不要多字段：

首次调用：{"prompt": "<content><压缩后的历史事实与指代解析></content> /n <用户当前问题原话>"}
后续调用：{"prompt": "<content><本轮新增的事实与指代解析></content> /n <用户当前问题原话>", "sessionId": "<照抄 /tmp/conexa-S00000001784191990656-session-<ts>.txt 的内容>"}

4. 用 bash 提交任务（-d @ 读取该文件，规避命令行转义/引号问题）：

alipay-bot curl-proxy -- -X POST 'https://agentpay.alipay.com/ai-pay/proxy/2088902259764064/S00000001784191990656' -H 'Content-Type: application/json' -d @/tmp/conexa-S00000001784191990656-body-<ts>.json

看 POST 返回里的【顶层】字段：
- 正常：返回里带一个 sessionId（形如 ses_xxx）。【注意：sessionId 不是固定复用的，每轮 POST 都会返回一个新的、和上一轮不同】——拿到后立刻执行下面命令把它覆盖保存进本会话的文件（旧值随即作废，之后任何请求都只认这个文件、不要用记忆里的旧值）：

printf '%s' '<返回里的 sessionId>' > /tmp/conexa-S00000001784191990656-session-<ts>.txt
printf '%s
' '<本次 <content> 里发送的文本>' >> /tmp/conexa-S00000001784191990656-sent-<ts>.log

（第二条是把本次发送内容追加进发送记录，下一轮增量就以它为参照。）

- 若返回的【顶层 code 字段 == SESSION_EXPIRED】（形如 {"error": "Session not found or expired", "code": "SESSION_EXPIRED"}）：说明远端沙箱已过期、文件里这个 sessionId 作废了。先执行 rm -f /tmp/conexa-S00000001784191990656-session-<ts>.txt /tmp/conexa-S00000001784191990656-sent-<ts>.log 清掉它们（远端已全忘，发送记录一并作废；后缀 <ts> 沿用本会话的、不要新生成），然后把这一轮【当首轮重打一次】：回到第 2 步改用【完整压缩】重整上下文——此时发送记录已清空、没有增量参照可言，把整段对话里当前仍有效的事实 / 约束 / 指代全部重压一遍（不是增量），重写 body 且【不带 sessionId 字段】，再 POST 一次；这次返回会给一个新的 sessionId，照常写入文件后继续后面的查询和后续轮。（首轮 POST 本就不带 sessionId、不会过期；整个重试对用户无感。）
5. 查询结果：查询地址带 userId、mode=text、sessionId 三个参数（userId 和 mode 固定、前缀照抄；sessionId 直接用 $(cat /tmp/conexa-S00000001784191990656-session-<ts>.txt) 从文件读，不要手填）：这是个 SSE 流式接口，**直接用 curl 请求**（不走 alipay-bot、直连）。每条 data: 行是一个 JSON `{"text":"..."}`，把里面的 text 字段依次拼起来就是回答正文。用下面这段 bash 一边收一边流式输出：

curl -sN "https://aipaymerchantorder-pre.alipay.com/test/agent/query?userId=2088902259764064&mode=text&sessionId=$(cat /tmp/conexa-S00000001784191990656-session-<ts>.txt)"   | python3 -c '
import sys, json
for line in iter(sys.stdin.readline, ""):
    p = line.strip()
    if not p.startswith("data:"): continue
    p = p[5:].strip()
    if not p or p == "[DONE]": continue
    try: o = json.loads(p)
    except Exception: continue
    sys.stdout.write(o.get("text", "")); sys.stdout.flush()
print()
'

6. 上面命令已把回答正文逐块流式打印出来，直接呈现给用户即可。

关键：<content> 里只放压缩后、最新有效的历史（被更新 / 作废的旧值只留最新版、无关闲聊不带）；当前问题原话一字不改地接在 </content> 后面，不要改写、不要和历史混在一起。sessionId 用法：【它每轮都会变，不是拿到一个就一直复用】，唯一可信来源是本会话的文件 /tmp/conexa-S00000001784191990656-session-<ts>.txt——每次 POST 返回后立刻覆盖写入，写 body（cat 出来填顶层 sessionId 字段）和拼查询地址（$(cat ...)）都从文件读，不要靠上下文记忆、不要自己编。文件后缀 <ts> 在首次调用时用 date +%s 生成一次、整个会话不变、写死在每条命令里，后续轮照抄历史命令的路径、不要新生成；路径里的 S00000001784191990656 是本能力专属——每个能力各用自己的文件，绝不读别的能力 / 别的会话 / 上次会话的 /tmp/conexa-* 旧文件。首次调用以【本轮对话此前没调用过本能力】为准（不是看文件）：生成 <ts>、POST 不带 sessionId、content 只来自本轮对话；每次 POST 返回新值并写入后，旧值立刻作废（一次对话里可能切换多个远端 agent、sessionId 必然更换）。再强调两点：① 后续轮 content 只发增量——以 cat /tmp/conexa-S00000001784191990656-sent-<ts>.log 的内容为参照，文件里已有且没变的别重发，不靠记忆；② 后续轮 body 必须带顶层 sessionId 字段=文件里的当前值，平铺在 prompt 旁边、不要包进任何嵌套对象、结构别飘。若某次 POST 返回顶层 code == SESSION_EXPIRED：把上下文【完整重压】、且【不带 sessionId 字段】重发一次 POST，用新返回的 sessionId 再查询，全程对用户无感。**第 5 步查询用普通 curl 直连、不要走 alipay-bot**。
本能力仅支持纯文本输入；不接受用户提供的图片、附件、文档等文件，若任务依赖这类输入，请告知用户暂不支持。
