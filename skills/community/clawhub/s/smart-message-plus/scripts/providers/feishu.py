#!/usr/bin/env python3
"""smart-message-plus: Feishu (Lark) adapter (custom enterprise app, tenant token).

Verified endpoints (e2e tested 2026-07-14):
  token       POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
  send        POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=...
  recall      DELETE https://open.feishu.cn/open-apis/im/v1/messages/:message_id
  image up    POST https://open.feishu.cn/open-apis/im/v1/images
  file up     POST https://open.feishu.cn/open-apis/im/v1/files
  id lookup   POST https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id
  dept child  GET  https://open.feishu.cn/open-apis/contact/v3/departments/:id/children
  dept users  GET  https://open.feishu.cn/open-apis/contact/v3/users/find_by_department

Markdown note: Feishu 'post' rich text does NOT accept standard markdown.
We render --markdown through an interactive card (lark_md), which supports
bold / links / dividers etc.
"""
from __future__ import annotations

import json
import mimetypes
import os
import re

from core import accounts as A
from core.http import request, multipart_upload

from .base import Provider, SendResult

BASE = "https://open.feishu.cn/open-apis"


class FeishuProvider(Provider):
    name = "feishu"

    @classmethod
    def capabilities(cls) -> dict:
        caps = super().capabilities()
        caps.update(
            p2p_text=True, p2p_markdown=True,
            group_text=True, group_markdown=True,
            image=True, file=True,
            mention=True, mention_all=True,
            recall=True,
            resolve_by_mobile=True, resolve_by_email=True,
            org_lookup_builtin=True,
            card=True,
            create_group=True,
        )
        return caps

    # ---------- token ----------
    def get_token(self) -> str:
        tok = A.get_cached_token(self.slug)
        if tok:
            return tok
        st, r = request(
            f"{BASE}/auth/v3/tenant_access_token/internal",
            {"app_id": self.account["app_id"], "app_secret": self.account["app_secret"]},
            timeout=self.timeout,
        )
        if r.get("code") != 0:
            raise RuntimeError(f"飞书获取 tenant_access_token 失败: code={r.get('code')} {str(r.get('msg'))[:150]}")
        tok = r.get("tenant_access_token", "")
        A.store_token(self.slug, tok, int(r.get("expire", 7200)))
        return tok

    def _h(self):
        return {"Authorization": f"Bearer {self.get_token()}"}

    def _call(self, url, body=None, method=None, retry_on_auth=True) -> dict:
        st, r = request(url, body, self._h(), method=method, timeout=self.timeout)
        if retry_on_auth and r.get("code") in (99991663, 99991661, 99991668):  # token invalid/expired
            A.invalidate_token(self.slug)
            st, r = request(url, body, self._h(), method=method, timeout=self.timeout)
        r["_status"] = st
        return r

    def test(self) -> tuple[bool, str]:
        try:
            self.get_token()
            return True, "飞书凭证有效（tenant_access_token 获取成功）"
        except (RuntimeError, OSError) as e:
            return False, f"飞书凭证验证失败: {e}"

    # ---------- resolve ----------
    def resolve_user(self, raw: str) -> str:
        raw = raw.strip()
        if raw.startswith("ou_"):
            return raw
        body = None
        if "@" in raw:
            body = {"emails": [raw]}
        elif re.fullmatch(r"1\d{10}", raw):
            body = {"mobiles": [raw]}
        if body:
            r = self._call(f"{BASE}/contact/v3/users/batch_get_id?user_id_type=open_id", body)
            if r.get("code") != 0:
                raise ValueError(
                    f"飞书 ID 查询失败: code={r.get('code')} {str(r.get('msg'))[:120]}。"
                    f"可维护别名: --save-contact <名字> single \"feishu:<open_id>\""
                )
            for u in (r.get("data") or {}).get("user_list", []):
                if u.get("user_id"):
                    return u["user_id"]
            raise ValueError(
                f"「{raw}」在飞书租户内未匹配到用户（账号可能未绑定该邮箱/手机号）。"
                f"可维护别名: --save-contact <名字> single \"feishu:<open_id>\""
            )
        if not raw.isascii():
            raise ValueError(
                f"「{raw}」不在联系人别名中。请先保存: "
                f"--save-contact {raw} single \"feishu:<open_id>\"（或改用邮箱/手机号）"
            )
        return raw  # assume native id

    # ---------- send ----------
    @staticmethod
    def _md_card(text: str) -> str:
        card = {
            "config": {"wide_screen_mode": True},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": text}}],
        }
        return json.dumps(card, ensure_ascii=False)

    def _send(self, receive_id: str, id_type: str, msg_type: str, content: str) -> SendResult:
        r = self._call(
            f"{BASE}/im/v1/messages?receive_id_type={id_type}",
            {"receive_id": receive_id, "msg_type": msg_type, "content": content},
        )
        if r.get("code") == 0:
            return SendResult(True, (r.get("data") or {}).get("message_id", ""))
        return SendResult(False, "", f"code={r.get('code')} {str(r.get('msg'))[:200]}")

    def send_p2p(self, user_ids: list[str], text: str, markdown: bool = False) -> SendResult:
        results, first_id, fails = [], "", []
        for uid in user_ids:
            if markdown:
                res = self._send(uid, "open_id", "interactive", self._md_card(text))
            else:
                res = self._send(uid, "open_id", "text", json.dumps({"text": text}, ensure_ascii=False))
            results.append(res)
            if res.ok and not first_id:
                first_id = res.msg_id
            if not res.ok:
                fails.append(f"{uid}: {res.detail}")
        if fails:
            return SendResult(len(fails) < len(user_ids), first_id, "; ".join(fails)[:300])
        return SendResult(True, first_id)

    def send_group(self, chat_id: str, text: str, markdown: bool = False,
                   mention_ids=None, mention_all=False) -> SendResult:
        if mention_all or mention_ids:
            ats = ""
            if mention_all:
                ats += '<at user_id="all">所有人</at> '
            for uid in mention_ids or []:
                ats += f'<at user_id="{uid}"></at> '
            if markdown:
                # lark_md supports <at> in card content via at tag syntax
                text = f"{ats}\n{text}"
            else:
                text = f"{ats}{text}"
        if markdown:
            return self._send(chat_id, "chat_id", "interactive", self._md_card(text))
        return self._send(chat_id, "chat_id", "text", json.dumps({"text": text}, ensure_ascii=False))

    # ---------- card (v1.1) ----------
    @staticmethod
    def _rich_card(title: str, text: str, buttons) -> str:
        """Interactive card: header + lark_md body + optional url buttons."""
        card: dict = {
            "config": {"wide_screen_mode": True},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": text}}],
        }
        if title:
            card["header"] = {"title": {"tag": "plain_text", "content": title},
                              "template": "blue"}
        if buttons:
            card["elements"].append({
                "tag": "action",
                "actions": [
                    {"tag": "button", "text": {"tag": "plain_text", "content": label},
                     "url": url, "type": "primary" if i == 0 else "default"}
                    for i, (label, url) in enumerate(buttons)
                ],
            })
        return json.dumps(card, ensure_ascii=False)

    def send_card_p2p(self, user_ids, title, text, buttons=None) -> SendResult:
        content = self._rich_card(title, text, buttons)
        first_id, fails = "", []
        for uid in user_ids:
            res = self._send(uid, "open_id", "interactive", content)
            if res.ok and not first_id:
                first_id = res.msg_id
            if not res.ok:
                fails.append(f"{uid}: {res.detail}")
        if fails:
            return SendResult(len(fails) < len(user_ids), first_id, "; ".join(fails)[:300])
        return SendResult(True, first_id)

    def send_card_group(self, chat_id, title, text, buttons=None) -> SendResult:
        return self._send(chat_id, "chat_id", "interactive", self._rich_card(title, text, buttons))

    # ---------- group management (v2.0) ----------
    def create_group(self, name: str, owner_id: str, member_ids: list[str],
                     **kwargs) -> SendResult:
        if not name or not name.strip():
            return SendResult(False, "", "群名不能为空")
        body = {
            "name": name.strip(),
            "chat_mode": "group",
            "chat_type": "private",
            "id_list": list(dict.fromkeys(member_ids or [])),
        }
        if owner_id:
            body["owner_id"] = owner_id
        r = self._call(f"{BASE}/im/v1/chats?user_id_type=open_id&set_bot_manager=true", body)
        if r.get("code") == 0:
            data = r.get("data") or {}
            cid = data.get("chat_id", "")
            invalid = data.get("invalid_id_list") or []
            detail = f"未拉入的成员: {','.join(invalid)}" if invalid else ""
            return SendResult(True, cid, detail, {"chat_id": cid})
        return SendResult(False, "", f"code={r.get('code')} {str(r.get('msg'))[:200]}")

    def list_groups(self) -> list[dict]:
        groups, page_token = [], ""
        while True:
            url = f"{BASE}/im/v1/chats?page_size=100"
            if page_token:
                url += f"&page_token={page_token}"
            r = self._call(url, None, method="GET")
            if r.get("code") != 0:
                raise RuntimeError(f"群列表查询失败: code={r.get('code')} {str(r.get('msg'))[:150]}")
            data = r.get("data") or {}
            for it in data.get("items") or []:
                groups.append({"name": it.get("name") or "(未命名)", "chat_id": it.get("chat_id", "")})
            if not data.get("has_more"):
                break
            page_token = data.get("page_token", "")
        return groups

    # ---------- media ----------
    def _upload_image(self, path: str) -> str:
        size = os.path.getsize(path)
        if size > 10 * 1024 * 1024:
            raise ValueError(f"飞书图片上限 10MB，文件 {size / 1048576:.1f}MB 超限: {path}")
        mime = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as f:
            data = f.read()
        st, r = multipart_upload(
            f"{BASE}/im/v1/images", {"image_type": "message"},
            "image", os.path.basename(path), data, mime,
            headers={"Authorization": f"Bearer {self.get_token()}"}, timeout=60,
        )
        if r.get("code") == 0:
            return (r.get("data") or {}).get("image_key", "")
        raise RuntimeError(f"飞书图片上传失败: code={r.get('code')} {str(r.get('msg'))[:150]}")

    def _upload_file(self, path: str) -> str:
        size = os.path.getsize(path)
        if size > 30 * 1024 * 1024:
            raise ValueError(f"飞书文件上限 30MB，文件 {size / 1048576:.1f}MB 超限: {path}")
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        ftype = {"pdf": "pdf", "doc": "doc", "docx": "doc", "xls": "xls", "xlsx": "xls",
                 "ppt": "ppt", "pptx": "ppt", "mp4": "mp4", "opus": "opus"}.get(ext, "stream")
        with open(path, "rb") as f:
            data = f.read()
        st, r = multipart_upload(
            f"{BASE}/im/v1/files", {"file_type": ftype, "file_name": os.path.basename(path)},
            "file", os.path.basename(path), data, mime,
            headers={"Authorization": f"Bearer {self.get_token()}"}, timeout=120,
        )
        if r.get("code") == 0:
            return (r.get("data") or {}).get("file_key", "")
        raise RuntimeError(f"飞书文件上传失败: code={r.get('code')} {str(r.get('msg'))[:150]}")

    def send_image_p2p(self, user_ids, path) -> SendResult:
        key = self._upload_image(path)
        content = json.dumps({"image_key": key})
        first_id, fails = "", []
        for uid in user_ids:
            res = self._send(uid, "open_id", "image", content)
            if res.ok and not first_id:
                first_id = res.msg_id
            if not res.ok:
                fails.append(res.detail)
        return SendResult(not fails, first_id, "; ".join(fails)[:200])

    def send_image_group(self, chat_id, path) -> SendResult:
        key = self._upload_image(path)
        return self._send(chat_id, "chat_id", "image", json.dumps({"image_key": key}))

    def send_file_p2p(self, user_ids, path) -> SendResult:
        key = self._upload_file(path)
        content = json.dumps({"file_key": key})
        first_id, fails = "", []
        for uid in user_ids:
            res = self._send(uid, "open_id", "file", content)
            if res.ok and not first_id:
                first_id = res.msg_id
            if not res.ok:
                fails.append(res.detail)
        return SendResult(not fails, first_id, "; ".join(fails)[:200])

    def send_file_group(self, chat_id, path) -> SendResult:
        key = self._upload_file(path)
        return self._send(chat_id, "chat_id", "file", json.dumps({"file_key": key}))

    # ---------- recall ----------
    def recall(self, log_entry: dict) -> tuple[bool, str]:
        mid = log_entry.get("msg_id", "")
        r = self._call(f"{BASE}/im/v1/messages/{mid}", method="DELETE")
        if r.get("code") == 0:
            return True, "已撤回"
        if r.get("code") == 230020:
            return False, "撤回失败：超过飞书 24 小时撤回时限"
        return False, f"撤回失败: code={r.get('code')} {str(r.get('msg'))[:150]}"

    # ---------- org ----------
    def org_resolve_department(self, dept_name: str) -> dict:
        dept_id = self._find_dept(dept_name, "0", 0)
        if not dept_id:
            raise ValueError(f"未找到飞书部门「{dept_name}」（需要通讯录读权限，部门名需完全匹配）")
        member_ids = self._dept_members(dept_id)
        return {"dept_id": dept_id, "dept_name": dept_name, "member_ids": member_ids}

    def _find_dept(self, name: str, parent: str, depth: int):
        if depth > 4:
            return None
        r = self._call(
            f"{BASE}/contact/v3/departments/{parent}/children"
            f"?department_id_type=open_department_id&page_size=50"
        )
        for d in (r.get("data") or {}).get("items", []) or []:
            if d.get("name") == name:
                return d.get("open_department_id")
            found = self._find_dept(name, d.get("open_department_id"), depth + 1)
            if found:
                return found
        return None

    def _dept_members(self, dept_id: str) -> list[str]:
        out, token = [], ""
        while True:
            url = (f"{BASE}/contact/v3/users/find_by_department?department_id={dept_id}"
                   f"&department_id_type=open_department_id&page_size=50")
            if token:
                url += f"&page_token={token}"
            r = self._call(url)
            data = r.get("data") or {}
            out.extend(u.get("open_id", "") for u in data.get("items", []) or [])
            if not data.get("has_more"):
                break
            token = data.get("page_token", "")
        return [x for x in dict.fromkeys(out) if x]
