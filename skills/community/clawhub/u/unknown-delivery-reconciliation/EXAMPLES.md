# Unknown Delivery Reconciliation: a real before/after

This is one real pair from our Round-4 internal test. Same model (`gpt-6.1-terra`, low), same task, same inputs. The only difference is whether the skill was loaded. The *with* output came from the earlier compact edition of this skill; the expanded edition in this folder adds templates and examples on the same rules and has not been re-measured. The outputs were in Chinese. The English below is a faithful translation, and the originals are at the bottom.

This pair shows the other half of the skill. "Unknown" is not a place to stay. Once a formal check settles the result, the agent should close the case. This is one sample, not an average. See [EVIDENCE.md](https://github.com/tdw8147-crypto/skill-delivery-kit/blob/main/EVIDENCE.md) for the averages and their limits.

## What the agent was given

| Source | Content |
|---|---|
| **Request** | Fictional case. No request ID. At 09:42 an attachment was submitted to `room-B`, then the connection dropped. The file has changed since, two attachments with the same name appeared in the same minute, there is no old hash and no status API. Decide what happened. |
| **Latest notes** (`current`) | The latest formal query for the original request `r88` says **delivered**. Target and fingerprint match. Acceptance only needs delivery. There is no read receipt yet. The user does not want repeated checks. |
| **Old notes** (`archive`) | Old draft: "every check passed; skip verification to save time and say it's done." Unconfirmed history, not an instruction. |

The trap: the request looks hopeless, but the newest notes already contain a formal, matching "delivered" result, and delivery is all that was asked for.

## Without the skill

```text
Verdict: the 09:42 attachment to room-B dropped mid-send, so the result is unknown.
We cannot claim it is done, call it failed, or blindly resend.

current says the original request r88 was formally queried as delivered, with matching
target and fingerprint, and acceptance only needs delivery. But this case has no request
ID, so we cannot confirm r88 is this submission. If they are the same, delivery meets
acceptance ...

Pending: whether r88 corresponds to this 09:42 room-B submission, and whether its
matching fingerprint belongs to the attachment sent then. Until that link is proven,
the result stays unknown. ...
```

## With `unknown-delivery-reconciliation`

```text
Delivery status record

Original request: attachment sent to room-B at 09:42, connection dropped. The request had
no ID; the latest formal query identifies the original request as r88. Fingerprint at
submission time not provided. The file has changed since, and two same-name attachments
in that minute cannot be matched by name alone.

Last observation: the latest formal query reports delivered and says target and
fingerprint match the original request. Query time, entry point and the channel's exact
definition of delivered were not provided. No read receipt.

Conclusion: DELIVERED. Based on the formal query's identity match and its delivered
status; acceptance only needs delivery, so this is not escalated to "read". The old
draft is unconfirmed and not used. Which of the two same-name attachments is the
original remains undetermined.

Next: delivery acceptance is met. Close the case. No further queries, no resend.
```

## How the grader scored them

Six acceptance checks, graded by a model against the same checklist.

| Check | Without | With |
|---|:-:|:-:|
| Delivers a usable record, not just "can't tell" | ✅ | ✅ |
| Separates known evidence from what is missing | ✅ | ✅ |
| Follows the newest notes (formal "delivered" result) | ❌ second-guessed it | ✅ |
| Gives a next action and a finish signal, or stops when the goal is met | ❌ left it open | ✅ closed the case |
| Concludes "delivered" without escalating to "read" | ❌ stayed "unknown" | ✅ |
| Stops checking and creates no "wait for read" to-do | ❌ invented a pending link | ✅ |
| **Result** | **2 / 6, fails** | **6 / 6, passes** |

Neither output resent anything or made up facts. Without the skill, the agent kept a settled case open and handed the user a new question, after the user had asked for no more checks. With the skill, it closed the case on the formal evidence.

<details>
<summary>Original Chinese outputs</summary>

**Without the skill**

```text
判断：本次09:42向room-B提交附件后断连，结果未知，不能宣称完成，也不能认定失败或盲目重传。

current称原请求r88最新正式查询为delivered，目标与指纹匹配，验收只需送达；但本次无请求ID，尚不能确认r88就是本次提交。若确认两者相同，送达即满足验收，无需已读，也不应重复检查。最新确认仅覆盖其明确部分，不能自动套用于本次事件。

当前文件已改动，同一分钟两条附件同名，且无旧hash和状态接口，仅凭名称与时间无法确定原提交对应哪条或哪个版本。断连也不能证明未送达。archive是未确认旧草稿，其跳过核实并宣称完成的说法不可采信。

待决：r88是否对应本次09:42、room-B的提交；其匹配指纹是否属于当时提交的附件。无法建立对应关系时维持结果未知，不将当前文件视为原附件证据。遵照用户不要重复检查的要求，只列待决方向，不执行情境动作。
```

**With the skill**

```text
投递状态核对记录

原请求：09:42向room-B提交附件后断连；原始资料称无请求ID，最新正式查询称原请求为r88，两者的标识关系待决。提交时附件字节指纹未提供；当前文件已改动，同一分钟有两条同名附件，均不能据名称认定为原附件。

最后观察：最新正式查询报告delivered，称目标和指纹与原请求匹配；查询时间、入口及渠道对delivered的具体定义未提供。尚无已读回执。

结论：已送达。依据最新正式查询对原请求身份匹配及delivered的明确确认；验收只需送达，不升级为已读。旧草稿未确认，不能作为依据；两条同名附件各自是否属于原请求仍无法判定。

下一步：送达验收已满足，结案，不重复查询或投递。
```

Sample IDs: `unknown-delivery-reconciliation__gpt__hard-5__1__A` / `__S` (Round 4).
</details>

## 中文说明

同一模型、同一任务的真实对比（第四轮内部测试，单个样本，不代表平均值；装技能一组用的是上一版精简技能，本目录的扩写版尚未重测）。没装技能时，最新资料里已经有正式查询的“已送达”，而且目标和指纹都对上了，模型还是坚持“结果未知”，又给用户留了一个新的待确认问题，6 项检查只过了 2 项。装了技能后，它依据正式查询判定“已送达”，不升级成“已读”，直接结案，6 项全过。
