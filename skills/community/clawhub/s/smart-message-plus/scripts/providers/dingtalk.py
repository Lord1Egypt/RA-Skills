#!/usr/bin/env python3
"""smart-message-plus: DingTalk adapter (enterprise internal app + robot).

Verified endpoints (e2e tested 2026-07-14):
  token      POST https://api.dingtalk.com/v1.0/oauth2/accessToken
  p2p send   POST https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend
  group send POST https://api.dingtalk.com/v1.0/robot/groupMessages/send
  p2p recall POST https://api.dingtalk.com/v1.0/robot/otoMessages/batchRecall
  grp recall POST https://api.dingtalk.com/v1.0/robot/groupMessages/recall
  media      POST https://oapi.dingtalk.com/media/upload
  by mobile  POST https://oapi.dingtalk.com/topapi/v2/user/getbymobile
  dept list  POST https://oapi.dingtalk.com/topapi/v2/department/listsub
  dept users POST https://oapi.dingtalk.com/topapi/user/listid
"""
from __future__ import annotations

import json
import mimetypes
import os
import re

from core import accounts as A
from core.http import request, multipart_upload

from .base import Provider, SendResult, NotSupported

API = "https://api.dingtalk.com"
OAPI = "https://oapi.dingtalk.com"

_BATCH = 20  # oToMessages/batchSend userIds limit


class DingTalkProvider(Provider):
    name = "dingtalk"

    @classmethod
    def capabilities(cls) -> dict:
        caps = super().capabilities()
        caps.update(
            p2p_text=True, p2p_markdown=True,
            group_text=True, group_markdown=True,
            image=True, file=True,
            mention=True, mention_all=True,
            recall=True,
            resolve_by_mobile=True, resolve_by_email=False,
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
            f"{API}/v1.0/oauth2/accessToken",
            {"appKey": self.account["app_key"], "appSecret": self.account["app_secret"]},
            timeout=self.timeout,
        )
        tok = r.get("accessToken", "")
        if not tok:
            raise RuntimeError(f"钉钉获取 accessToken 失败: HTTP {st} {json.dumps(r, ensure_ascii=False)[:150]}")
        A.store_token(self.slug, tok, int(r.get("expireIn", 7200)))
        return tok

    def _h(self):
        return {"x-acs-dingtalk-access-token": self.get_token()}

    def _call(self, url, body, headers=None, retry_on_auth=True) -> tuple[int, dict]:
        st, r = request(url, body, headers or self._h(), timeout=self.timeout)
        # token invalid -> refresh once
        if retry_on_auth and (st in (401,) or r.get("code") in ("InvalidAuthentication", "InvalidAccessToken")):
            A.invalidate_token(self.slug)
            st, r = request(url, body, self._h(), timeout=self.timeout)
        return st, r

    def _oapi(self, path, body) -> dict:
        st, r = request(f"{OAPI}{path}?access_token={self.get_token()}", body, timeout=self.timeout)
        if r.get("errcode") not in (0, None):
            # 88 = permission missing etc.
            raise RuntimeError(f"钉钉接口错误 [{path}]: errcode={r.get('errcode')} {str(r.get('errmsg'))[:200]}")
        return r

    def test(self) -> tuple[bool, str]:
        try:
            self.get_token()
            return True, "钉钉凭证有效（accessToken 获取成功）"
        except (RuntimeError, OSError) as e:
            return False, f"钉钉凭证验证失败: {e}"

    # ---------- resolve ----------
    def resolve_user(self, raw: str) -> str:
        raw = raw.strip()
        if re.fullmatch(r"1\d{10}", raw):  # CN mobile
            try:
                r = self._oapi("/topapi/v2/user/getbymobile", {"mobile": raw})
                uid = (r.get("result") or {}).get("userid", "")
                if uid:
                    return uid
                raise ValueError(f"手机号 {raw} 未匹配到企业成员")
            except RuntimeError as e:
                raise ValueError(f"手机号查询失败（{e}）。可改用 userId 或维护联系人别名") from e
        if "@" in raw:
            raise ValueError(
                f"钉钉不支持邮箱直发（{raw}）。请改用手机号/userId，"
                f"或维护别名: --save-contact <名字> single \"dingtalk:<userId>\""
            )
        if not raw.isascii():
            raise ValueError(
                f"「{raw}」不在联系人别名中。请先保存: "
                f"--save-contact {raw} single \"dingtalk:<userId>\"（或改用手机号）"
            )
        return raw  # assume native userId

    # ---------- send ----------
    def _robot_body(self, msg_key: str, msg_param: dict) -> dict:
        return {
            "robotCode": self.account.get("robot_code") or self.account["app_key"],
            "msgKey": msg_key,
            "msgParam": json.dumps(msg_param, ensure_ascii=False),
        }

    def send_p2p(self, user_ids: list[str], text: str, markdown: bool = False) -> SendResult:
        msg_key, param = ("sampleMarkdown", {"title": text[:20] or "消息", "text": text}) if markdown \
            else ("sampleText", {"content": text})
        ids_all, keys, failed = list(user_ids), [], []
        for i in range(0, len(ids_all), _BATCH):
            chunk = ids_all[i:i + _BATCH]
            body = self._robot_body(msg_key, param)
            body["userIds"] = chunk
            st, r = self._call(f"{API}/v1.0/robot/oToMessages/batchSend", body)
            if st == 200 and r.get("processQueryKey"):
                keys.append(r["processQueryKey"])
                bad = r.get("invalidStaffIdList") or []
                failed.extend(bad)
            else:
                failed.extend(chunk)
                return SendResult(False, "", f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}",
                                  {"sent_keys": keys, "failed": failed})
        detail = "" if not failed else f"无效用户: {','.join(failed)}"
        return SendResult(True, keys[0] if keys else "", detail, {"all_keys": keys, "failed": failed})

    def send_group(self, chat_id: str, text: str, markdown: bool = False,
                   mention_ids=None, mention_all=False) -> SendResult:
        # robot group send has no native at-field; embed @ in markdown text
        if mention_ids or mention_all:
            markdown = True
            at_txt = " ".join(f"<@{u}>" for u in (mention_ids or []))
            if mention_all:
                at_txt = "@所有人 " + at_txt  # dingtalk robot md has no reliable at-all; textual fallback
            text = f"{text}\n\n{at_txt}".strip()
        # chatXXX form (from --create-group): robot is not a member -> legacy app-message channel
        if chat_id.startswith("chat"):
            return self._chat_send(chat_id, text, markdown)
        msg_key, param = ("sampleMarkdown", {"title": text[:20] or "消息", "text": text}) if markdown \
            else ("sampleText", {"content": text})
        body = self._robot_body(msg_key, param)
        body["openConversationId"] = chat_id
        st, r = self._call(f"{API}/v1.0/robot/groupMessages/send", body)
        if st == 200 and r.get("processQueryKey"):
            return SendResult(True, r["processQueryKey"])
        detail = f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}"
        if r.get("code") == "resource.not.found":
            detail += "\n   机器人不在该群。群设置→智能群助手→添加机器人，或用 --create-group 产生的 chatId 别名（走应用消息通道）"
        return SendResult(False, "", detail)

    def _chat_send(self, chatid: str, text: str, markdown: bool = False,
                   media_id: str = "", mtype: str = "") -> SendResult:
        """Legacy app-message to a chat (no robot membership required).
        Note: these messages cannot be recalled."""
        if mtype == "image":
            msg = {"msgtype": "image", "image": {"media_id": media_id}}
        elif mtype == "file":
            msg = {"msgtype": "file", "file": {"media_id": media_id}}
        elif markdown:
            msg = {"msgtype": "markdown", "markdown": {"title": text[:20] or "消息", "text": text}}
        else:
            msg = {"msgtype": "text", "text": {"content": text}}
        st, r = request(f"{OAPI}/chat/send?access_token={self.get_token()}",
                        {"chatid": chatid, "msg": msg}, timeout=self.timeout)
        if r.get("errcode") == 0:
            return SendResult(True, r.get("messageId", ""), "（应用消息通道，不支持撤回）")
        return SendResult(False, "", f"errcode={r.get('errcode')} {str(r.get('errmsg'))[:150]}")

    # ---------- card (v1.1) ----------
    @staticmethod
    def _card_msg(title: str, text: str, buttons) -> tuple[str, dict]:
        """Map to robot ActionCard msgKeys.
        0 buttons -> markdown; 1 -> sampleActionCard (single jump);
        2..5 -> sampleActionCard2..5 (button list)."""
        buttons = buttons or []
        if len(buttons) > 5:
            raise ValueError(f"钉钉 ActionCard 最多 5 个按钮，当前 {len(buttons)} 个")
        body_md = f"### {title}\n\n{text}" if title else text
        if not buttons:
            return "sampleMarkdown", {"title": title or text[:20] or "消息", "text": body_md}
        if len(buttons) == 1:
            label, url = buttons[0]
            return "sampleActionCard", {
                "title": title or "消息", "text": body_md,
                "singleTitle": label, "singleURL": url,
            }
        param = {"title": title or "消息", "text": body_md}
        for i, (label, url) in enumerate(buttons, 1):
            param[f"actionTitle{i}"] = label
            param[f"actionURL{i}"] = url
        return f"sampleActionCard{len(buttons)}", param

    def send_card_p2p(self, user_ids, title, text, buttons=None) -> SendResult:
        msg_key, param = self._card_msg(title, text, buttons)
        ids_all, keys, failed = list(user_ids), [], []
        for i in range(0, len(ids_all), _BATCH):
            chunk = ids_all[i:i + _BATCH]
            body = self._robot_body(msg_key, param)
            body["userIds"] = chunk
            st, r = self._call(f"{API}/v1.0/robot/oToMessages/batchSend", body)
            if st == 200 and r.get("processQueryKey"):
                keys.append(r["processQueryKey"])
                failed.extend(r.get("invalidStaffIdList") or [])
            else:
                return SendResult(False, "", f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}")
        detail = "" if not failed else f"无效用户: {','.join(failed)}"
        return SendResult(True, keys[0] if keys else "", detail, {"all_keys": keys})

    def send_card_group(self, chat_id, title, text, buttons=None) -> SendResult:
        msg_key, param = self._card_msg(title, text, buttons)
        if chat_id.startswith("chat"):
            # app-message channel supports markdown but not ActionCard buttons
            if buttons:
                return SendResult(False, "", "该群走应用消息通道（机器人不在群内），不支持按钮卡片。"
                                             "请在群里手动添加机器人后用 cid 形式群ID重试")
            return self._chat_send(chat_id, param.get("text", text), markdown=True)
        body = self._robot_body(msg_key, param)
        body["openConversationId"] = chat_id
        st, r = self._call(f"{API}/v1.0/robot/groupMessages/send", body)
        if st == 200 and r.get("processQueryKey"):
            return SendResult(True, r["processQueryKey"])
        return SendResult(False, "", f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}")

    # ---------- group management (v2.0) ----------
    def create_group(self, name: str, owner_id: str, member_ids: list[str],
                     with_bot: bool = False, template_id: str = "") -> SendResult:
        if not name or not name.strip():
            return SendResult(False, "", "群名不能为空")
        owner = owner_id or (member_ids[0] if member_ids else "")
        if not owner:
            return SendResult(False, "", "钉钉建群需要群主: --owner <userId/别名> 或至少一个 --members 成员")
        ids = list(dict.fromkeys([owner] + (member_ids or [])))
        if with_bot:
            return self._create_scene_group(name.strip(), owner, ids, template_id)
        # Legacy chat/create: ordinary group, robot NOT inside (app-message channel)
        st, r = request(
            f"{OAPI}/chat/create?access_token={self.get_token()}",
            {"name": name.strip(), "owner": owner, "useridlist": ids},
            timeout=self.timeout,
        )
        if r.get("errcode") == 0 and r.get("chatid"):
            chat_id = r["chatid"]
            open_cid = r.get("openConversationId", "")
            return SendResult(True, chat_id, "",
                              {"chat_id": chat_id, "open_conversation_id": open_cid})
        err = f"errcode={r.get('errcode')} {str(r.get('errmsg'))[:150]}"
        if r.get("errcode") in (40014, 60011, 88) or st == 403:
            err += ("\n   可能缺少「群管理」权限 qyapi_chat_manage。申请地址: "
                    f"https://open-dev.dingtalk.com/appscope/apply?content={self.account['app_key']}%23qyapi_chat_manage"
                    "\n   开通后无需发版即可重试")
        return SendResult(False, "", err)

    def _create_scene_group(self, name: str, owner: str, ids: list[str],
                            template_id: str) -> SendResult:
        """Scene group with a console-configured template that has the robot
        bound — the only DingTalk path where the bot lands in the group via API
        (full robot channel: buttons/recall/@)."""
        if not template_id:
            return SendResult(False, "", (
                "加机器人建群需要「场景群模板」（钉钉平台限制：普通群无法通过 API 加机器人）。\n"
                "   一次性配置（约3分钟）: 开发者后台 → 开放能力 → 场景群 → 创建群模板 → "
                "在模板里添加本应用机器人 → 发布 → 复制模板ID\n"
                "   然后: --create-group <群名> --with-bot --scene-template <模板ID>\n"
                "   （模板ID会自动记住，下次不用再传）\n"
                "   或去掉 --with-bot 建普通群（应用消息通道: 文本/MD/图片/文件，无按钮卡片/撤回）"))
        st, r = self._call(f"{API}/v1.0/im/sceneGroups", {
            "groupName": name, "groupOwnerId": owner,
            "userIds": ",".join(ids), "templateId": template_id,
        })
        cid = (r or {}).get("openConversationId", "")
        if st == 200 and cid:
            return SendResult(True, cid, "机器人已在群内（场景群模板），全能力可用",
                              {"chat_id": cid, "scene": True})
        err = f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}"
        if (r or {}).get("code") == "groupTemplate.notFound":
            err += "\n   模板不存在或未发布。请检查模板ID，确认模板已在后台「发布」"
        return SendResult(False, "", err)

    # ---------- media ----------
    def _upload_media(self, path: str, mtype: str) -> str:
        size = os.path.getsize(path)
        if size > 20 * 1024 * 1024:
            raise ValueError(f"钉钉媒体上限 20MB，文件 {size / 1048576:.1f}MB 超限: {path}")
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            data = f.read()
        st, r = multipart_upload(
            f"{OAPI}/media/upload?access_token={self.get_token()}&type={mtype}",
            {}, "media", os.path.basename(path), data, mime, timeout=60,
        )
        if r.get("errcode") == 0 and r.get("media_id"):
            return r["media_id"]
        raise RuntimeError(f"钉钉媒体上传失败: {json.dumps(r, ensure_ascii=False)[:200]}")

    def send_image_p2p(self, user_ids, path) -> SendResult:
        media_id = self._upload_media(path, "image")
        param = {"photoURL": media_id}
        ids_all, keys = list(user_ids), []
        for i in range(0, len(ids_all), _BATCH):
            body = self._robot_body("sampleImageMsg", param)
            body["userIds"] = ids_all[i:i + _BATCH]
            st, r = self._call(f"{API}/v1.0/robot/oToMessages/batchSend", body)
            if not (st == 200 and r.get("processQueryKey")):
                return SendResult(False, "", f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}")
            keys.append(r["processQueryKey"])
        return SendResult(True, keys[0] if keys else "", "", {"all_keys": keys})

    def send_image_group(self, chat_id, path) -> SendResult:
        media_id = self._upload_media(path, "image")
        if chat_id.startswith("chat"):
            return self._chat_send(chat_id, "", media_id=media_id, mtype="image")
        body = self._robot_body("sampleImageMsg", {"photoURL": media_id})
        body["openConversationId"] = chat_id
        st, r = self._call(f"{API}/v1.0/robot/groupMessages/send", body)
        if st == 200 and r.get("processQueryKey"):
            return SendResult(True, r["processQueryKey"])
        return SendResult(False, "", f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}")

    def send_file_p2p(self, user_ids, path) -> SendResult:
        media_id = self._upload_media(path, "file")
        fname = os.path.basename(path)
        param = {"mediaId": media_id, "fileName": fname, "fileType": fname.rsplit(".", 1)[-1] if "." in fname else "file"}
        ids_all, keys = list(user_ids), []
        for i in range(0, len(ids_all), _BATCH):
            body = self._robot_body("sampleFile", param)
            body["userIds"] = ids_all[i:i + _BATCH]
            st, r = self._call(f"{API}/v1.0/robot/oToMessages/batchSend", body)
            if not (st == 200 and r.get("processQueryKey")):
                return SendResult(False, "", f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}")
            keys.append(r["processQueryKey"])
        return SendResult(True, keys[0] if keys else "", "", {"all_keys": keys})

    def send_file_group(self, chat_id, path) -> SendResult:
        media_id = self._upload_media(path, "file")
        fname = os.path.basename(path)
        if chat_id.startswith("chat"):
            return self._chat_send(chat_id, "", media_id=media_id, mtype="file")
        param = {"mediaId": media_id, "fileName": fname, "fileType": fname.rsplit(".", 1)[-1] if "." in fname else "file"}
        body = self._robot_body("sampleFile", param)
        body["openConversationId"] = chat_id
        st, r = self._call(f"{API}/v1.0/robot/groupMessages/send", body)
        if st == 200 and r.get("processQueryKey"):
            return SendResult(True, r["processQueryKey"])
        return SendResult(False, "", f"HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}")

    # ---------- recall ----------
    def recall(self, log_entry: dict) -> tuple[bool, str]:
        mode = log_entry.get("send_mode", "")
        key = log_entry.get("msg_id", "")
        robot = self.account.get("robot_code") or self.account["app_key"]
        if mode == "group":
            body = {"robotCode": robot, "openConversationId": log_entry.get("chat_id", ""),
                    "processQueryKeys": [key]}
            st, r = self._call(f"{API}/v1.0/robot/groupMessages/recall", body)
        else:
            body = {"robotCode": robot, "processQueryKeys": [key]}
            st, r = self._call(f"{API}/v1.0/robot/otoMessages/batchRecall", body)
        ok = st == 200 and key in (r.get("successResult") or [])
        if ok:
            return True, "已撤回"
        return False, f"撤回失败: HTTP {st} {json.dumps(r, ensure_ascii=False)[:200]}"

    # ---------- org ----------
    def org_resolve_department(self, dept_name: str) -> dict:
        """BFS the dept tree by name; collect member ids of matched dept (incl. sub-depts)."""
        matched = self._find_dept(dept_name)
        if not matched:
            raise ValueError(f"未找到部门「{dept_name}」（需要通讯录读权限，且部门名需完全匹配）")
        dept_id, full_name = matched
        member_ids = self._collect_members(dept_id)
        return {"dept_id": str(dept_id), "dept_name": full_name, "member_ids": member_ids}

    def _find_dept(self, name: str, root: int = 1, depth: int = 0):
        if depth > 4:
            return None
        r = self._oapi("/topapi/v2/department/listsub", {"dept_id": root})
        for d in r.get("result") or []:
            if d.get("name") == name:
                return d["dept_id"], d["name"]
            found = self._find_dept(name, d["dept_id"], depth + 1)
            if found:
                return found
        return None

    def _collect_members(self, dept_id: int, depth: int = 0) -> list[str]:
        if depth > 4:
            return []
        ids = list((self._oapi("/topapi/user/listid", {"dept_id": dept_id}).get("result") or {}).get("userid_list") or [])
        r = self._oapi("/topapi/v2/department/listsub", {"dept_id": dept_id})
        for d in r.get("result") or []:
            ids.extend(self._collect_members(d["dept_id"], depth + 1))
        return list(dict.fromkeys(ids))
