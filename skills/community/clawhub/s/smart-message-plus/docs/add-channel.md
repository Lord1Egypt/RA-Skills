# 如何新增一个消息渠道（Channel / Provider）

> 本文说明如何为 smart-message-plus 接入一个新的 IM 平台（例如企业微信 WeCom、Slack、Telegram 等）。
> 阅读前建议先看 [`design.md`](./design.md) 了解整体分层架构。

## 总体思路

新增渠道 = **写一个新的 Provider 适配器**，让它继承 `providers/base.py` 的抽象基类并实现平台特有逻辑，然后在主入口注册。**你不需要改 `send.py` 的任何发送流程**——主流程只跟抽象接口打交道。

整个过程分 5 步：

1. 探测平台 API 能力（先做，别跳过）
2. 新建 `providers/<name>.py` 继承 `Provider`
3. 实现 token / 解析 / 发送 / 撤回等方法 + 声明能力矩阵
4. 在 `send.py` 的 `PROVIDERS` 注册表登记
5. 联系人别名 / 群 ID 前缀 / 文档更新

---

## Step 0：先探测平台 API 能力（关键前置）

**不要凭直觉写适配器。** 每个 IM 平台的坑都不一样，动手前用真实凭证把下面这些问清楚，否则设计会返工：

- **鉴权模型**：拿什么 token？应用身份 token 还是用户身份 token？有效期多久？（钉钉是 accessToken，飞书是 tenant_access_token）
- **单聊接口**：一次能发几个人？要不要先把手机号/邮箱换成用户 ID？换 ID 的接口有没有？（钉钉没有邮箱→userId 接口）
- **群聊前提**：机器人要不要先进群？能不能通过 API 建群 / 把机器人加进群？
- **Markdown**：原生支持还是要走卡片渲染？（飞书要走 interactive 卡片 lark_md）
- **撤回**：有没有时限？p2p 和 group 是不是分两个接口？
- **媒体上传**：图片 / 文件分不分接口？大小上限？
- **权限**：通讯录读、发消息、建群各要什么权限？改权限后要不要重新发版才生效？

把结论整理成一张能力表，作为适配器实现和 `capabilities()` 的依据。

---

## Step 1：新建适配器文件

在 `scripts/providers/` 下新建 `<name>.py`（如 `wecom.py`），骨架如下：

```python
#!/usr/bin/env python3
"""smart-message-plus: <平台> adapter."""
from __future__ import annotations

import json
from core import accounts as A
from core.http import request, multipart_upload
from .base import Provider, SendResult, NotSupported

BASE = "https://<平台 API 域名>"


class WeComProvider(Provider):
    name = "wecom"     # 全局唯一的 provider 名，命令行 --provider 用它

    @classmethod
    def capabilities(cls) -> dict:
        caps = super().capabilities()
        caps.update(
            p2p_text=True, p2p_markdown=True,
            group_text=True, group_markdown=True,
            image=True, file=True,
            mention=True, mention_all=True,
            recall=False,                 # 按平台真实能力如实声明
            resolve_by_mobile=True, resolve_by_email=False,
            org_lookup_builtin=True,
            card=True, create_group=False,
        )
        return caps
```

> ⚠️ `capabilities()` 一定要**如实**声明。主流程会据此在发送前拦截不支持的操作，声明错了会导致要么误报、要么发出去才失败。

---

## Step 2：实现必需方法

下面按"必须"和"可选"列出。**必须**的不实现，对应功能就用不了；**可选**的不实现会自动抛 `NotSupported`（对用户是友好报错，不会崩）。

### 2.1 凭证与连通性（必须）

```python
def get_token(self) -> str:
    tok = A.get_cached_token(self.slug)      # 先查缓存
    if tok:
        return tok
    st, r = request(f"{BASE}/gettoken",
                    {"corpid": self.account["app_key"],
                     "corpsecret": self.account["app_secret"]},
                    timeout=self.timeout)
    tok = r.get("access_token", "")
    if not tok:
        raise RuntimeError(f"获取 token 失败: {r}")
    A.store_token(self.slug, tok, int(r.get("expires_in", 7200)))  # 写缓存
    return tok

def test(self) -> tuple[bool, str]:
    try:
        self.get_token()
        return True, "凭证有效"
    except (RuntimeError, OSError) as e:
        return False, f"凭证验证失败: {e}"
```

- token 缓存交给 `core/accounts.py`，会自动提前 5 分钟刷新，你只管存和取。
- token 失效时（401 或平台特定错误码），在 `_call` 里 `A.invalidate_token(self.slug)` 后重试一次。

### 2.2 收件人解析（必须）

```python
def resolve_user(self, raw: str) -> str:
    raw = raw.strip()
    # 手机号 / 邮箱 → 平台用户 ID
    # 已经是原生 ID → 原样返回
    # 中文昵称等无法解析 → 抛 ValueError，提示用别名
    if not raw.isascii():
        raise ValueError(
            f"「{raw}」不在联系人别名中。请先保存: "
            f'--save-contact {raw} single "{self.name}:<用户ID>"')
    return raw
```

**约定**：解析失败一律抛 `ValueError`，消息里要带**可复制的修复命令**，不要抛裸异常。

### 2.3 发送（必须）

所有发送方法返回 `SendResult(ok, msg_id, detail, extra)`：

```python
def send_p2p(self, user_ids: list[str], text: str, markdown: bool = False) -> SendResult:
    ...
    if success:
        return SendResult(True, message_id)
    return SendResult(False, "", f"失败原因: {...}")

def send_group(self, chat_id: str, text: str, markdown: bool = False,
               mention_ids=None, mention_all=False) -> SendResult:
    ...
```

- `msg_id` 用于后续撤回，务必返回平台真实消息 ID。
- 批量单聊如果平台有上限（如钉钉 20/批），在这里分批循环。
- 需要 @人时，按平台语法拼接（钉钉在 markdown 里嵌 `<@userid>`，飞书用 `<at>` 标签）。

### 2.4 可选方法

按平台能力选实现，不实现则继承基类的 `NotSupported`：

- `send_card_p2p` / `send_card_group`：卡片消息（标题 + 正文 + 跳转按钮）
- `send_image_p2p` / `send_image_group` / `send_file_p2p` / `send_file_group`：媒体，用 `multipart_upload` 上传拿 media_id 再发
- `recall(log_entry)`：撤回，从日志条目取 msg_id / chat_id
- `create_group` / `list_groups`：建群 / 群列表
- `org_resolve_department(dept_name)`：部门查询，返回 `{"dept_id", "dept_name", "member_ids"[...]}`

---

## Step 3：在主入口注册

编辑 `scripts/send.py`，两处改动：

```python
from providers.wecom import WeComProvider          # 1. 导入

PROVIDERS: dict[str, type[Provider]] = {
    "dingtalk": DingTalkProvider,
    "feishu": FeishuProvider,
    "wecom": WeComProvider,                          # 2. 登记
}
```

同时在 `cmd_save_account` 里处理该平台的凭证字段映射（哪些字段是必需的），并在 `contacts.py` 的 `save_contact` 校验里把新 provider 名加入白名单（当前是 `("dingtalk", "feishu")`）。

---

## Step 4：群 ID 前缀（如涉及群聊）

`core/contacts.py` 的 `resolve_group()` 会根据前缀识别"这是原生群 ID 还是别名"。如果你的平台群 ID 有固定前缀（钉钉是 `cid` / `chat`，飞书是 `oc_`），在这里加一条放行规则，让用户可以直接传原生群 ID 而不必先存别名。

---

## Step 5：验证与文档

### 端到端验证（务必用真实凭证跑）

至少覆盖这些场景：

- [ ] `--test-account` 凭证验证通过
- [ ] 单聊文本 / Markdown
- [ ] 群聊文本 / Markdown / @人 / @所有人
- [ ] 图片 / 文件
- [ ] 卡片（如支持）
- [ ] 撤回（如支持）
- [ ] 收件人别名解析 + 解析失败的报错指引
- [ ] `--dry-run` 预览
- [ ] 部门广播（如支持）

> `--dry-run` 只走参数解析和收件人解析、不真发，适合先自查逻辑；但**最终必须用真凭证真发一轮**，`--dry-run` 全过不代表线上能用。

### 更新文档

- `SKILL.md`：平台差异速查表、能力矩阵、账号字段说明
- `references/provider-matrix.md`：补一列新平台
- `references/console-setup.md`：新平台的后台配置 + 权限清单
- `docs/design.md`：如果新平台带来新的架构考量

---

## 常见坑提醒

- **能力如实声明**：`capabilities()` 写错比不写更糟。
- **所有网络调用走 `core/http.py`**：自带超时和重试，别自己写裸 `urllib`。
- **凭证只走 `core/accounts.py`**：不要把 secret 硬编码或落到 skill 目录。
- **报错要可操作**：解析 / 权限 / 建群失败时，把"缺什么权限、去哪申请、怎么改"写进 detail。
- **改权限后可能要重新发版**：部分平台（如飞书）权限变更后需重新发布应用才生效，探测阶段就要确认。
