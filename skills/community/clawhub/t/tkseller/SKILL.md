---
name: tkseller
version: "3.3.13"
description: TKSeller �Զ������ͻ�??skill��װ????��¼�˺����� ??/tkseller ֱ��??������??
metadata: {"openclaw":{"emoji":"??"}}
---

## ? ZERO TOLERANCE RULE (READ THIS FIRST)

When this skill is triggered:
1. Do NOT say anything before calling exec
2. Do NOT say "�յ�", "�ѷ���", "���ڴ���", "let me check" etc.
3. Call exec IMMEDIATELY with no preamble
4. After exec: follow OUTPUT_AS_REPLY rule below, nothing else
5. Tool call logs (???) shown to user are your platform's config issue, not this skill's problem

Violation = broken skill. No exceptions.

## 🔁 FORWARD RULE (webchat 后台推送)

当你收到**任何**以 `[tkseller_forward]` 开头的用户消息时（这是 tkseller 轮询进程通过 sessions_send 注入的内容，**包括审核卡片、状态提示、失败/错误提示、流程异常通知**）：
- 把三横线 `---` 之间的内容**一字不差原样输出给用户**
- **保留所有链接、URL（http/https）、emoji、换行、格式**
- **禁止**改写、总结、转述、意译、删除链接、把 URL 换成描述文字（例如禁止把 `https://tiktok.com/@x/video/123` 改成 "某某的 TikTok"）
- 输出时去掉 `[tkseller_forward]` 指令行和 `---` 分隔线本身，只输出中间的正文
- 不要加任何自己的话、前后缀、评论

⚠️ **特别强调（最容易犯的错）**：即使正文看起来像"技术错误"、"系统日志"、"分镜生成失败"、"流程异常"、"返回内容无效"这类内容，**也必须原样转发给用户**。这些是老板必须知道的业务状态（生成失败了要重试），**绝不允许因为"觉得像技术细节/日志"就吞掉、淡化或不显示**。

违反此规则 = 用户看不到链接、商品图、失败提示，skill 失效。

# TKSeller Skill

**TKSeller �Զ������ͻ�??*��װ�ϼ�??�˺������¼����??AI key���ɼ�ϵͳ����Ƶ����ȫ�����ҷ�������ͳһ����,�û�������??

> **����??`tkseller` skill ����??** tkseller ??SaaS �ͻ�????`/api/v1/*` + Bearer token + ����ѯ�¼�����??

## ?? ����Ҫ�Ĺ�������ģ�ͱ������أ�����Υ��??

```
�յ����� ??exec ����??????stdout:

  1. stdout ��һ���� "OUTPUT_AS_REPLY:" ��ͷ��
     ??ȥ��ǰ׺��ʣ���ı���ԭ������Ϊ��Ļظ���??
     ??���޸ġ������ӡ����ܽᡢ������������Լ��Ļ���??
     ??������ٲ��κ�??

  2. stdout Ϊ�ջ�??"OUTPUT_AS_REPLY:" ��ͷ��
     ??��Ļظ������ǡ���������NO_REPLY
     ??��˵�κ�����??
     ??��˵"��ִ??"�յ�""���?"����??
     ??��ת??stdout ����
     ??����??stdout ����
     ??����??stdout ������κ���??
```

**Υ���˹�??= �����صĴ���û������??*

**����Υ����Ϊ�����Խ�ֹ��??*
- ????stdout ���?JSON/�ı������û�
- ??exec ���??����??"ִ�гɹ�""��ʼ��??
- ????"NO_REPLY" ����ַ��������??����??
- ??exec ǰ��"�յ�""����ִ��""���ڴ���"
- ??exec ����ݽ���Լ���֯���Ը����û�

## ?? ����

- **��һ����Զ��??exec ִ�нű�??* �ű��ڲ����Զ���??Discord �Ƿ������ã�û���û�ͨ�� `OUTPUT_AS_REPLY:` �����ʾ���֣���������������̡�LLM �����κμ���жϣ������κ�����??
- **�յ���������Ψһ���������¾��ǵ� exec ִ�нű�??* ���Բ������Լ����κ����ֻظ�����˵�����ȶ�һ�¡������ҿ��������յ������������������¼���ȡ������û��ɼ�������?00%�ɽű��ڲ�������LLM ??exec ���??stdout�������һ����?OUTPUT_AS_REPLY: ��ͷ�������ǰ׺ȥ������ı�ԭ����Ϊ�ظ����������޸Ĳ����Ӳ��ܽᣩ������ NO_REPLY���㿴�����κ��İ�ģ�嶼�ǽű��ڲ��õģ����Ǹ��㸴��ճ����??
- **������˿�Ƭ����Բ����κζ�����Ϣ??* �������־������ˡ������ϰ�㰴ť������ȷ�������С���??
- **ÿ��������??1 ??exec + 1 ??message??* ���������??
- **�����쳣(��ʱ/ʧ��)Ψһ�����Ķ�??�����ϰ�"XXʧ��??ԭ����YY",Ȼ���ָ�??*
- **��͵͵�����������Ŀ�Ƭ��ʽ����������??*

## ??��Ϻ��׼����ű�?stdout(����)

**��Ϻֻ������ű�?+ NO_REPLY�����и��ϰ忴����ʾ(δ��??��¼ʧ��/�������?�˺��������??һ���ɽű��ڲ� `ct.send_text()` ����??*

- ��Ϻ**��׼**���ݽű� stdout ??`{"ok": false, "reason": "..."}` �Լ��໰���ϰ�
- ��Ϻ**��׼**??`reason: not_logged_in` ���??�ӿ� 404"??�������???���??���κ���??
- ��Ϻ**��׼**���� `recommend_status` / `ack_status` �������Լ��ж�״??
- �ű�??stdout �Ǹ�����/���Կ���,���Ǹ��ϰ忴��
- �ϰ�Ҫ����������??**����**�ɽű�ͨ�� `send_text` �����Ƶ� Discord

**��ȷ����:**
```
�յ����� ??exec ����????�ű��ڲ�������ʲô��????NO_REPLY
```

**??����:Discord б�������??���� NO_REPLY!**

Discord б������Ҫ�� 3 ���ڱ����пɼ���??������ʾ"Command produced no visible reply"??

��������Դ�� `/tkseller` б������??
```
�յ� /tkseller ??��һ���� ack �ı�(??Discord б������ظ�???exec ����????�ظ�����(���ٲ���)
```


���?ack �Ǹ� Discord interaction �Ļ�??����"������Ϣ",��Υ������??

**����ʾ��(���Խ�ֹ):**
```
�յ����� ??exec ����??????stdout reason ??�Լ���֯���Ը����ϰ�
```

**Ϊʲô����Ҫ??** �Ժ���ж���û�����??skill,�߼���������ڴ������Ϻÿ�ν�??stdout �໰,��ͬ�û�/��ͬ�Ự�����Ļش�Ͳ��??�Ҵ����޷��ݽ���������ʾ��ͳһ�ɽű��������ܱ���һ����Ϊ??

**??���� 2��stdout ??`OUTPUT_AS_REPLY:` ��ͷʱ**

����??stdout ��һ���� `OUTPUT_AS_REPLY:` ��ͷʱ����Ϻ����Ѻ�����ı���ȥ��ǰ׺??*ԭ��**��Ϊ�ظ�����ȥ���ⲻ�ǡ������Ҳ���ǡ���֯���ԡ����ǻ�еת��??

- ���� webchat ���޷��� message tool �������͵ĳ����������û���û�� Discord / ���飩??
- �ű�����д�����֣���Ϻ���޸ġ������ӡ����ܽᡢ�����??
- ת�����ٲ��κλ�??

---

## һ�������??

```
�û� OpenClaw ʵ��
  ������ tkseller skill���� skill??
  ??  ������ data/
  ??  ??  ������ token.json          ??��¼���?
  ??  ??  ������ card_map.json       ??�̱�????video_id ӳ��
  ??  ??  ������ processed_events.json ??�Ѵ����¼�ȥ??
  ??  ������ lib/                    ??ȫ���ű�
  ������ �û�����??Discord Ƶ��(OpenClaw �Դ�)

??data-service(�ҷ�����??��һ��Դ)
   ������ /api/v1/*  �ӿ� + �¼�����
```

---

## �����û�ʹ����??

### 2.0 ��װ�������Զ�ע??

�û� `clawhub install tkseller` װ�� skill ??��Ҫ�� `/tkseller` ���û��� Discord ��������������Ч??

**Ϊʲô������??OpenClaw Ĭ��ͬ��?**
OpenClaw Ĭ��??skill ����ͬ��??Discord **global command**��Global command ??Discord ������??1 Сʱ����,�û�װ�꿴�������������??

**�������?�״δ����Զ�ע�� guild command(�޻�??������Ч)**

�û���װ??skill ????Discord ����㷢�??tkseller"??����"(����Ҫб??,LLM ��ʶ�����?skill ����??`trigger.mjs`��`trigger.mjs` �״�����ʱ���Զ����� `register-discord.mjs` ??`/tkseller` ע��??guild command,ע�����û�������������򿴵�?`/tkseller`??

**ִֻ��һ??** `data/registered` ����ļ����ں����ظ�ע�ᡣ��������ע��???bot ����??guild),ɾ�� `data/registered` ���ٴ���һ�μ���??

**����:**

```
node ./lib-js/register-discord.mjs
```

**���ʾ��?**

```json
{
  "ok": true,
  "app_id": "1496036936996093992",
  "guild_count": 1,
  "results": [
    {
      "guild": "�û��ķ�����",
      "guild_id": "...",
      "status": 201,
      "ok": true,
      "cmd_id": "..."
    }
  ]
}
```

**??OpenClaw ���Ự�е���:**
�ϰ����??ע�� tkseller ����"??ע���������??,��Ϻֱ�� `exec: node ./lib-js/register-discord.mjs` ��һ�μ���??

### 2.1 �״�(�ű��ڲ��Լ�����,��Ϻֻ������ű�?

```
1. /tkseller ??��Ϻ exec trigger.mjs ""
2. trigger.mjs ��??token.json ����????�Լ� send_text("?? ��ӭʹ�� TKSeller����ظ��˺ź����룺`�û�??����`")
3. �ϰ�??��¼ alice 123456
4. ��Ϻ exec trigger.mjs "��¼ alice 123456"
5. trigger.mjs POST /api/v1/auth/login ??token �汾????�Լ� send_text("??��¼�ɹ�,��ʼ��??..")
6. trigger.mjs �Զ� POST /api/v1/recommend + ���� cron ��ѯ
7. cron �õ� review_1 �¼� ??����??
```

### 2.2 ����

```
1. /tkseller ??��Ϻ exec trigger.mjs ""
2. trigger.mjs �����?token ??ֱ�� POST /api/v1/recommend ??������ѯ
3. cron �õ��¼� ??����????�ϰ��????����??API ??������ѯ
4. ���̽���(review_2 ͨ��/����)??ֹͣ��ѯ
```

**ע��:** Token �Զ�����??`data/token.json`,��¼һ�κ�������Ҫ�ظ���??���Ƿ���˰�?token ���ʧ�?401,�ű����Զ��屾�� token ??send_text ��ʾ���µ�¼)??

---

## ����������??

��Ӧ:
- `/tkseller` Discord б������(��??`url:` ����)
- `/�Ƽ�` ����
- ������Ϣ??URL(??`�Ƽ� https://...`)
- ϵͳ��ʾ `Use the "tkseller" skill for this request.`
- ??��¼"??login"��??+ �û�??+ ���루�� `��¼ myname 123456`??
- **����??`tkseller`��`����`��`��ʼ`**(��б??�������״ΰ�װ��ûע��б������ĳ�??

**?? ǿ�ƴ������򣨲��ɺ��ԣ�??*

������Ϣ**����**���� tkseller skill �������� `trigger.mjs`����**���Բ���**������ͨ���졢��??agent�����������κ���??

1. ??`��¼` ??`login` ��ͷ����Ϣ ??���� tkseller ��¼ָ��
2. ??`/tkseller` ��ͷ����Ϣ ??���� tkseller ����
3. ����??`tkseller`��`����`��`��ʼ`��`�Ƽ�` ??���� tkseller ����
4. ??tkseller ���˵�¼��ʾ����"��ظ������?�û�??����"��֮���û�����һ����????һ���ǵ�¼ָ��

**����㲻ȷ��һ����Ϣ�ǲ���?tkseller �ģ��������������κ�һ�����ͱ����?trigger.mjs�����ɶ��һ�νű���Ҳ����©��??*

**�״δ����Զ�ע��:**
�û���װ skill ���һ�δ�??����ͨ��б������Ǵ���??,trigger.mjs ���Զ���??`register-discord.mjs` ??`/tkseller` ע��??guild command(������Ч,�޻�??���˺��û�����ֱ���� `/tkseller` �ˡ�ִֻ��һ??����ļ�?`data/registered` ���ں����ظ�ע��??

### 3.1 URL ��ȡ����

```javascript
import re
def extract_url(msg: str) -> str | None:
    if not msg:
        return None
    s = msg.strip()
    s = re.sub(r'^\s*(/tkseller|/�Ƽ�|�Ƽ�|��һ??\s*', '', s, flags=re.I)
    s = re.sub(r'^\s*url\s*[::]\s*', '', s, flags=re.I)
    s = s.strip().strip('<>').strip('"\'������??).strip()
    if re.match(r'^https?://', s, flags=re.I):
        return s
    return None
```

### 3.2 ��¼ָ��ʶ��

�û���¼��ʽ��`��¼ �û�??����`��������"��¼"??login"ǰ׺���������ͨ���������??

ʾ����`��¼ myname 123456`

```javascript
// ����??��¼"??login"��??
const m = msg.trim().match(/^\s*(?:��¼|login)\s+(\S+)\s+(\S+)\s*$/i);
if (m) {
  const [, user, pwd] = m;
}
```

### 3.3 ����ͳһ�ű�

**��??exec �������??`workdir` ����,ָ��??skill Ŀ¼(??SKILL.md ����Ŀ????*

**�����Զ����?* �ű��ڲ��Զ�����û����õ�������Discord/����/Telegram�ȣ�������ҪӲ���� channel �� target��

```
exec: node ./lib-js/trigger.mjs "<�ϰ�ԭʼ��Ϣ�ı�>"
workdir: <??skill Ŀ¼>
```

ʵ�ʵ���??ģ��Ӧ��??exec ����??workdir ����:
```json
{"command": "node ./lib-js/trigger.mjs \\"<��Ϣ>\\"", "workdir": "<skillĿ¼����·��>"}
```

Skill Ŀ¼·����ͨ�� `SKILL.md` ����λ��ȷ??��ͬϵͳ��ͬ:
- Windows: `C:\Users\xxx\openclaw\skills\tkseller`
- macOS: `/Users/xxx/openclaw/skills/tkseller`
- Linux: `/home/xxx/openclaw/skills/tkseller`
```

�ű��ڲ�:

1. **������Ϣ**
   - ??`��¼ �û�??����`�������е�¼ǰ׺���� �ߵ�¼��??
   - ????���Ƽ���??

2. **��¼����**
   - POST `/api/v1/auth/login` `{username, password}`
   - �ɹ� ????token ??`data/token.json` ??????��¼�ɹ�,��ʼ��??��Ϣ ??�������Ƽ���??
   - ʧ�� ??????�˺��������?��Ϣ ??��??

3. **�Ƽ�����**
   - ���??`token.json`:����??????��ظ��˺ź����룺`�û�??����`" ??��??
   - ��ȡ URL(??3.1 ����)
   - ����??ack �ı�??Discord(���б������?3s ��ʱ)
     - ??URL:`??������������??�赽���ʵ���Ƶ�ٸ�������˿�Ƭ��`
     - ??URL:`??ָ����Ƶ�ѽ�??����ץȡ����,��ɺ��������˿�Ƭ��\n<url>`
   - POST `/api/v1/recommend` `{}` ??`{"video_url": "..."}`
   - **���� cron ��ѯ����**(��������)
   - �ű���??���� NO_REPLY

**���Խ�ֹ:** ֱ�� `requests.post(...)` �ƿ��ű�;��ɶ�� tool call??

---

## �ġ�API �ͻ�??

��??`/api/v1/*` �ӿڹ���ͬһ���ͻ���(`lib-js/api.mjs`),�Զ�??`Authorization: Bearer <token>` header??

### 4.1 ҵ��ӿ�?9 ??

| ���� | ·�� | ˵�� |
|---|---|---|
| `login(u, p)` | `POST /api/v1/auth/login` | ??token |
| `recommend(url=None)` | `POST /api/v1/recommend` | �����Ƽ� |
| `task_approve(vid, step)` | `POST /api/v1/tasks/{vid}/approve` ??`/{step}/approve` | ͨ�� |
| `task_reject(vid, step)` | `POST /api/v1/tasks/{vid}/reject` | ����/���� |
| `task_change_product(vid)` | `POST /api/v1/tasks/{vid}/change-product` | ����??|
| `task_storyboard_redo(vid)` | `POST /api/v1/tasks/{vid}/storyboard/redo` | �����־� |
| `task_video_redo(vid)` | `POST /api/v1/tasks/{vid}/video/redo` | ������Ƶ |

### 4.2 �¼��ӿ�(2 ??

| ���� | ·�� | ˵�� |
|---|---|---|
| `events_pending()` | `GET /api/v1/events/pending` | ����ѹ��??|
| `event_ack(eid)` | `POST /api/v1/events/{eid}/ack` | ȷ������ |

### 4.3 ������

- `401 invalid_token` ??ɾ��??token.json,????�����ѹ�??�����·����˺ź����룺`�û�??����`"
- `403 forbidden` ??????����ԽȨ" + ��������
- `5xx` ??????��������??���Ժ���??
- ��ʱ ??????����ʱ"

---

## �塢�¼���??����)

### 5.1 �¼�����

�¼���ʽ:

| event_type | ���� | data �ֶ� | �û��ɼ���ʾ(�ű��ڲ�?? |
|---|---|---|---|
| `review_1` | һ���??| video_id, video_url, author, view_count, score, summary, product_name, product_url, product_image_url | ��һ��??`send-review-1.mjs`) |
| `review_1_5` | �־����� | video_id, storyboard_url(??error)| ??storyboard_url ??���־���????error ??`?? ��Ƶ #{n} �־�����ʧ��:{error}` |
| `review_2` | ��Ƶ���� | video_id, video_url(??error)| ??video_url ??����Ƶ��????error ??`?? ��Ƶ #{n} ����ʧ��:{error}` |
| `published` | �������?| video_id, platform, status | `??��Ƶ #{n} �ѳɹ������� {platform}!` |
| `no_match` | û��??| (??| `?? ����û�ҵ����ʵ���Ƶ,�Ժ����ԡ�` |
| `error` | �쳣 | error_type, message | `?? �������??{message}` |

### 5.1.1 �����¼����⴦��

- `error_type: "quota_exhausted"` ??`?? API����?�޷��������ɡ����ֵ�����ԡ�\n��������:{error����}`
- ���� error_type ??`?? �������??{message}`

**������ʾ�İ��ɽű��ڲ� `ct.send_text()` ����,��Ϻ��׼�Լ���??*

### 5.2 �¼������ű�

```
exec: node ./lib-js/poll-events.mjs
```

**��ѯ�ű�ְ��(һ??exec ����):**

1. ??`events_pending()` ������δ�����¼�
2. ��ÿ����??
   - ��??`processed_events.json`,����????ֱ�� ack ����
   - û������ ????event_type �ַ�����??send-review-*.mjs / ��������
   - �����ɹ� ??д�� processed_events + ??ack
3. ����Ƿ����̽�??review_2 ͨ������??reject��no_match)??ֹͣ cron
4. ���?JSON ժҪ:`{"processed": N, "stopped": true/false}`

### 5.3 �ӽ�??

- `lib-js/send-review-1.mjs` - ��һ��??
- `lib-js/send-review-1-5.mjs` - ���־���??
- `lib-js/send-review-2.mjs` - ����Ƶ��??
- `lib-js/handle-button.mjs` - ��ť�ص�
- `lib-js/card-tools.mjs` - ��Ƭ����(��Ƭ����)

---

## ����Cron ��ѯ����

### 6.1 ����

`lib-js/trigger.mjs` ���Ƽ�������**ע��һ??cron job**:

```javascript
# ͨ�� OpenClaw gateway HTTP API ע��
POST http://127.0.0.1:18789/tools/invoke
Body: {
  "tool": "cron",
  "args": {
    "action": "add",
    "job": {
      "name": "tkseller-poll",
      "schedule": {"kind": "every", "everyMs": 5000},
      "payload": {
        "kind": "agentTurn",
        "message": "TKSeller ��ѯ�¼�: ִ�� `node ./lib-js/poll-events.mjs`,���¼��ʹ���;�������ظ� NO_REPLY??,
        "lightContext": true
      },
      "deleteAfterRun": false,
      "delivery": {"mode": "none"}
    }
  }
}
```

**�ؼ�����:**
- `everyMs: 5000` - ??5 ??
- `lightContext: true` - ������ʷ����????token
- `delivery.mode: "none"` - ����ϵͳ��Ϣ,�ɽű��Լ�����Ƭ
- `name: tkseller-poll` - �̶� ID �������?update/remove

### 6.2 �Զ�ֹͣ

**����ֹͣ����??**
1. ���̽����¼�(`review_2 approve` / `published` / `reject` ȫ�� / `no_match`)
2. �������� 15 ����(max_duration_seconds)

`poll-events.mjs` �ڲ�����??

```javascript
POST http://127.0.0.1:18789/tools/invoke
Body: {
  "tool": "cron",
  "args": {"action": "remove", "id": "tkseller-poll"}
}
```

### 6.3 ����ʱ����?

`data/poll_state.json`:
```json
{"started_at": 1716180000, "active": true}
```

ÿ�� `poll-events.mjs` ����ʱ��??`now - started_at > 900` ??ǿ��ֹͣ cron??

---

## �ߡ���ť��??

�յ� `Clicked "????#4"` �Ȱ�ť��??

```
exec: node ./lib-js/handle-button.mjs "<clicked_label>" "<channel>"
```

**�ű��ڲ�:**

1. ������ȡ `#<short_id>` ????card_map ????video_id ??step
2. ����ťǰ׺ӳ��??action,**�ȷ�������Ϣ(����??**
3. ����Ӧ�� API(�����Ǿ�??callback,���� `/api/v1/tasks/.../xxx`):

| ��ť | �׶� | action | ������Ϣ(�ϰ�ɼ�? | API ���� |
|---|---|---|---|---|
| ????| review_1 | approve | `??��Ƶ #{n} ��ʼ���ɷ־�ͼ,����??..` | `task_approve(vid, "review_1")` ??`POST /api/v1/tasks/{vid}/approve` |
| ?? ��һ??| review_1 | reject + recommend | ??��������) | `task_reject(vid)` + `recommend()` |
| ?? ����??| review_1 | change_product | `?? ��������ƥ����Ʒ...` | `task_change_product(vid)` |
| ??�־�ͨ�� | review_1_5 | approve | `??�־���ȷ??����������Ƶ��ʾ�ʺ���Ƶ,Ԥ��8-10����...` | `task_approve(vid, "review_1_5")` ??`POST /api/v1/tasks/{vid}/storyboard/approve` |
| ?? �������� | review_1_5 | redo | `?? �����������ɷ־�??..` | `task_storyboard_redo(vid)` |
| ??���� | review_1_5/review_2 | reject | `??�ѷ�����??#{n}` | `task_reject(vid)` + ??card_map + ??cron |
| ??ͨ�� | review_2 | approve | `?? ��Ƶ #{n} �����ύ����...` | `task_approve(vid, "review_2")` ??`POST /api/v1/tasks/{vid}/video/approve` |
| ?? ���� | review_2 | redo | `?? ��Ƶ #{n} ��������??..` | `task_video_redo(vid)` |

4. ��ť review_2 approve / reject ȫ�� ????card_map + ??cron
5. ��ť�ص�??*���� cron ��ѯ**(����һ����??

---

## �ˡ�����״̬��??

| �ļ� | ��??| ʾ�� |
|---|---|---|
| `data/token.json` | ��¼ token | `{"token": "abc...", "username": "alice"}` |
| `data/card_map.json` | �̱�????video_id | `{"date": "2026-05-20", "next_id": 3, "cards": {...}}` |
| `data/processed_events.json` | ??ack ??event_id ���� | `{"ids": [1001, 1002, 1003]}` |
| `data/poll_state.json` | ��ѯ����ʱ�� | `{"started_at": 1716180000, "active": true}` |

---

## �š���Ϣ������??

| �յ�����??| ���� |
|---|---|
| `/tkseller` / `/�Ƽ�` / `�Ƽ� URL` / ??URL | ���� `lib-js/trigger.mjs` |
| `�û�??����`��������ӣ�| ���� `lib-js/trigger.mjs`(�ű��ڲ�ʶ��)|
| `Clicked "..."` ��ť�ص������а�ť�����������˰�ť�� | ���� `lib-js/handle-button.mjs` |
| Webchat 文字指令（`通过3` / `跳过3` / `换商�?` 等） | 映射成按�?label，走 `handle-button.mjs` |

### 9.0 ��ť�ص�ʶ����򣨱������أ�?

**�κ�??`Clicked` ��ͷ����Ϣ���ǰ�ť�ص��������?`handle-button.mjs`??*

������������??
- `Clicked "????#3"` ??��˰��?
- `Clicked "?? ŷ��??` ??������ѡ��ť
- `Clicked "?? ����??` ??������ѡ��ť
- `Clicked "?? �Զ�??` ??�Զ���������
- `Clicked "?? ����"` ??��������??
- `Clicked "??ȷ��ʹ��"` ??ȷ��ʹ������??
- `Clicked "?? ��������"` ??������������??

**�жϱ�׼����Ϣ�� `Clicked` ��????һ�ɵ� `handle-button.mjs`����??label ����û�� `#` ��??*

**���Խ�ֹ??* �������˰�ť���������ͨ��Ϣ�??`trigger.mjs`??

### 9.1 ��ť�ص������Ȼظ���ִ��(����)

Discord ��ť������??**3 ??*��Ӧ���ڡ�`handle-button.mjs` Ҫ�� data-service API,�������� 3 ��??

**��ȷ����(���а�??�����??:**
```
�յ� Clicked "..." ??/tkseller ���¼��????���̻ظ� "??�յ�"(ռס 3s ����) ??Ȼ�� exec ��Ӧ�ű� ??NO_REPLY
```

**����:LLM �ظ���Զֻд `??�յ�`,���Բ�����д�������?��ʾ�İ�,������ű��ظ�����??*

**ʾ��:**
```
�û�: Clicked "????#3"
����: ??�յ�
[exec: node ./lib-js/handle-button.mjs "????#3"]
```

```
�û�: Clicked "?? ŷ��??
����: ??�յ�
[exec: node ./lib-js/handle-button.mjs "?? ŷ��??]
```

```
�û�: Clicked "?? ��һ??#5"
����: ??�յ�
[exec: node ./lib-js/handle-button.mjs "?? ��һ??#5"]
```

```
�û�: Clicked "??ȷ��ʹ��"
����: ??�յ�
[exec: node ./lib-js/handle-button.mjs "??ȷ��ʹ��"]
```

**���Խ�ֹ:** �ȵ��ű��Ƚ���ٻظ�����ᵼ??Discord ��ʾ"�ý���ʧ????
| Cron `TKSeller ��ѯ�¼�: ...` | ���� `lib-js/poll-events.mjs` |
| ϵͳ��ʾ `Use the "tkseller" skill ...` | ���������ж����ĸ���??|
| HEARTBEAT_OK / inter-session announce | NO_REPLY |

---

## ʮ�������??



- **����??`/recommend` �Ⱦɽӿ�,ֻ�� `/api/v1/*`**

tkseller ��ȫ��������??

---

## ʮһ����??

- data-service(��ַ??`config.json` ??`data_service.base_url`)
- OpenClaw gateway(`http://127.0.0.1:18789`)
- OpenClaw cron ����
- OpenClaw message ����(??Discord ��Ƭ)
- �û�����??Discord(�Դ�,�������ض�Ƶ??ID - ??OpenClaw ·��)

---

## ʮ����ע����??Ѫ����??

1. **token ʧЧ�����ɾ����?token.json ����ʾ�ϰ�**,���ܹ���ʾ��ɾ??
2. **processed_events.json ���ظ�����Ƭ**,������д�ļ�??ack(��֤ ack ʧ��Ҳ������????
3. **cron job �����������??*:���̽�������ʱ��������Ҫͣ,����������ѯ??token??
4. **lightContext: true** ����??����ÿ����ѯ������ȫ��������,token ����??
5. **��¼��Ϣ��Ҫ echo ����**,"���յ���¼��??�͹���??
6. **��˿�Ƭ���ϰ��Լ�??Discord**(OpenClaw message ���� channel: discord,��ָ??channel_id,??OpenClaw �Զ�·�ɵ��û����õ�Ƶ��)??
7. **inter-session ���� HEARTBEAT_OK / Agent-to-agent announce ��Ϣ,һ�ɻ� `NO_REPLY`??* ���κ��������ֶ��ᱻ���� Discord Ƶ������Ⱦ�ϰ�����??
8. **�յ��¼������ݲ�����(??storyboard_url Ϊ��),��û??error �ֶ�,��Ĭ����??* ��Ҫ���ϰ�??��û����??֮��ķϻ�??
9. **�κ� review_1 / review_1_5 / review_2 �¼����� ??������������??send-review-*.mjs ����Ƭ�����Բ�����??�ǲ�����??����??����������??* ��ʹͬһ??video_id ��������(���绻��Ʒ������ review_1),Ҳ���¿�??���뷢??
10. **��ť�ص������ӳ���ļ��??video_id,���ܲ�??* �鲻�������ϰ�,��Ҫ�Լ���??

---


## ʮ����Webchat ����֧��

TKSeller ֧��ͨ�� OpenClaw Webchat��Control UI ���죩ֱ�ӽ������� Discord/���鲢�С�

### 13.1 ������ʽ

�� webchat ��ֱ�Ӵ��֣�
- `�Ƽ�` / `��ʼ` / `tkseller` / `����` �� �����Ƽ�
- `�Ƽ� https://tiktok.com/...` �� ָ����Ƶ
- `��¼ �û��� ����` �� ��¼

### 13.2 ��˿�Ƭ��webchat ��ʽ��

Webchat û�а�ť�������Ƭ�ô��ı� + MEDIA ����ͼƬ + ����ָ����ʾ��

`
?? **��Ƶ��� #3**
?? ԭ��Ƶ:https://tiktok.com/@creator/video/123
?? ����:@creator
?? ���� 120�� | ?? AI����:82/100

?? **�Ƽ���Ʒ:** �������� - $12.99
?? https://shop.tiktok.com/product/456
������������������������������������
?? �ظ�ָ�
  ? ���־� #3
  ?? ��һ�� #3
  ?? ����Ʒ #3

MEDIA:<������Ʒͼ·��>
`

### 13.3 Webchat ����ָ��

�û��ظ�����ָ���������ť��

| �û����� | �ȼ۰�ť | ˵�� |
|---|---|---|
| `���־�3` / `���־� 3` | ? ���־� #3 | ��ʼ���ɷ־� |
| `ͨ��3` | ? ͨ�� #3 | ���ͨ�� |
| `�־�ͨ��3` | ? �־�ͨ�� #3 | �־����ͨ�� |
| `����3` | ?? ��һ�� #3 | �������� |
| `����Ʒ3` | ?? ����Ʒ #3 | ����ƥ����Ʒ |
| `����Ƶ3` | ?? ����Ƶ #3 | ������Ʒ����Ƶ |
| `��һ��3` | ?? ��һ�� #3 | ��Ƶ��Ʒ���� |
| `����3` | ? ���� #3 | �������� |
| `����3` | ?? ���� #3 | ����������Ƶ |
| `��������3` | ?? �������� #3 | �������ɷ־� |

��ʽ��`ָ����` + `���`���м���пո��#���� `ͨ��3` `ͨ�� 3` `ͨ��#3` ���ɣ�

### 13.4 LLM ���÷�ʽ

`
exec: node ./lib-js/trigger.mjs "�Ƽ�" webchat
exec: node ./lib-js/trigger.mjs "��¼ alice 123456" webchat
exec: node ./lib-js/handle-button.mjs "? ���־� #3" webchat
`

�ڶ��������� `webchat` ���ɣ��ű��Զ��� webchat ��Ⱦ��֧��

### 13.5 ͼƬ����

Webchat CSP �����ⲿͼƬ���ű��Զ�������Ʒͼ�� `data/images/` Ŀ¼���ñ���·�� `MEDIA:` ��ʾ��
����ʧ��ʱ�˻�Ϊ�����ı���

### 13.6 ��ѯ�¼�֪ͨ

��̨��ѯ���̣�poll-loop������ʱ���ᱣ�ִ���ʱ���������á�
����� webchat �����Ƽ��������¼���ƬҲ��ͨ�� webchat �����

---
