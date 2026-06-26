#!/usr/bin/env python3
"""
通用内容审核 Skill — 配置驱动，适用于所有 d.php 后台站点

审核判断优先级：
  1. 本地规则（rules.json）— 默认，无需外部依赖
  2. 技术部 API（可选增强）— 配置了 api_key 时启用

用法：
    # 标准用法：本地规则自动审核
    python review.py --config config.json

    # 可选：配合技术部 API 双重审核
    python review.py --config config.json  （config 中填了 api_key）

    # dry-run（只看不提交）
    python review.py --config config.json --dry-run

    # 只拉取待审列表（不判断不提交）
    python review.py --config config.json --fetch-only

    # 提交外部审核决定
    python review.py --config config.json --decisions decisions.json
"""
import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode


SCRIPT_DIR = Path(__file__).resolve().parent


# ─── 日志 ───

def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


# ─── TOTP ───

def totp(seed: str) -> str:
    """生成6位TOTP验证码（HMAC-SHA1, 30秒窗口）"""
    secret = base64.b32decode(seed, casefold=True)
    counter = int(time.time() // 30)
    msg = struct.pack(">Q", counter)
    digest = hmac.new(secret, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


# ─── HTTP 客户端（curl + VPN） ───

class SiteClient:
    """通过 curl 访问后台，走 VPN 接口并维护 cookie 会话"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = config["site"]["base_url"].rstrip("/")
        self.module = config["site"]["module"]
        self.vpn_iface = config["site"].get("vpn_interface", "ppp0")
        self.endpoints = config["site"]["endpoints"]
        self._cookie_file = tempfile.NamedTemporaryFile(
            prefix="review_cookies_", suffix=".txt", delete=False
        )
        self.cookie_jar = self._cookie_file.name
        self._cookie_file.close()

    def _resolve_endpoint(self, key: str) -> str:
        ep = self.endpoints[key].replace("{module}", self.module)
        return f"{self.base_url}{ep}"

    def curl(self, url: str, method: str = "GET", data: Optional[Dict] = None) -> str:
        cmd = [
            "curl", "-sS",
            "--interface", self.vpn_iface, "-4",
            "-b", self.cookie_jar, "-c", self.cookie_jar,
            "-H", "X-Requested-With: XMLHttpRequest",
        ]
        if method == "POST" and data is not None:
            cmd += [
                "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
                "--data", urlencode(data, doseq=True),
            ]
        cmd.append(url)
        try:
            return subprocess.check_output(cmd, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"curl 超时: {url}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"curl 失败 (exit {e.returncode}): {url}")

    def curl_json(self, url: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        raw = self.curl(url, method, data)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise RuntimeError(f"非 JSON 响应: {raw[:200]}")

    def cleanup(self):
        try:
            os.unlink(self.cookie_jar)
        except OSError:
            pass


# ─── 登录 ───

def login(client: SiteClient, config: Dict[str, Any]):
    """TOTP 登录后台"""
    fields = config["site"]["login_fields"]
    auth = config["auth"]

    log("正在登录...")
    client.curl(client._resolve_endpoint("login_page"))

    data = {
        fields["username_field"]: auth["username"],
        fields["password_field"]: auth["password"],
        fields["totp_field"]: totp(auth["totp_seed"]),
    }
    resp = client.curl_json(client._resolve_endpoint("login_submit"), method="POST", data=data)
    if resp.get("code") != 0:
        raise RuntimeError(f"登录失败: {resp.get('msg', resp)}")
    log("登录成功")


# ─── 拉取待审列表 ───

def fetch_pending(client: SiteClient, config: Dict[str, Any], page: int = 1) -> Tuple[List[Dict], int]:
    """拉取待审核内容列表，返回 (items, total_count)"""
    fetch_cfg = config["fetch"]
    url = client._resolve_endpoint("fetch")
    params = {
        "where[status]": fetch_cfg["pending_status"],
        "page": str(page),
        "limit": str(fetch_cfg["page_size"]),
    }
    full_url = f"{url}?{urlencode(params)}"
    resp = client.curl_json(full_url)
    items = resp.get("data", [])
    total = resp.get("count", 0)
    return items, int(total) if total else 0


# ─── 本地规则引擎 ───

def load_rules(rules_path: Optional[str] = None) -> List[Dict]:
    """加载审核规则"""
    if rules_path:
        p = Path(rules_path)
    else:
        p = SCRIPT_DIR / "rules.json"
    if not p.exists():
        log(f"  规则文件不存在: {p}，跳过本地规则")
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    rules = [r for r in data.get("rules", []) if r.get("enabled", True)]
    return rules


def apply_rules(item: Dict, content_fields: List[str], rules: List[Dict]) -> Optional[Dict]:
    """
    对单条数据应用本地规则。
    返回 None 表示通过，返回 dict 表示命中规则（含 reason）。
    """
    # 预拼接全文本字段（供 _text 规则使用）
    full_text = "\n".join(
        str(item.get(f, "")) for f in content_fields if item.get(f)
    )

    for rule in rules:
        rule_type = rule.get("type", "regex")
        field = rule.get("field", "_text")

        # 取目标文本
        if field == "_text":
            target = full_text
        else:
            val = item.get(field, "")
            target = str(val) if val else ""

        if not target.strip():
            continue

        # 价格校验规则
        if rule_type == "price_check":
            try:
                price = int(float(target))
            except (ValueError, TypeError):
                continue
            min_p = rule.get("min_price", 0)
            max_p = rule.get("max_price", 999999)
            mult = rule.get("must_be_multiple_of", 1)
            if mult > 1 and price % mult != 0:
                return {"verdict": "rejected", "reason": rule["reason"], "rule_id": rule["id"]}
            if price < min_p or price > max_p:
                return {"verdict": "rejected", "reason": rule["reason"], "rule_id": rule["id"]}
            continue

        # 标题格式校验规则
        if rule_type == "title_format":
            pat = rule.get("pattern", "")
            if pat and not re.match(pat, target):
                return {"verdict": "rejected", "reason": rule["reason"], "rule_id": rule["id"]}
            continue

        # 默认：正则匹配
        for pat in rule.get("patterns", []):
            try:
                if re.search(pat, target):
                    return {"verdict": "rejected", "reason": rule["reason"], "rule_id": rule["id"]}
            except re.error:
                continue

    return None  # 全部通过


# ─── 审核 API（可选增强） ───

def has_moderation_api(config: Dict[str, Any]) -> bool:
    return bool(config.get("moderation", {}).get("api_key"))


def moderate_via_api(text: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """调用技术部统一审核 API（POST /v2/moderations）"""
    try:
        import requests as req
    except ImportError:
        raise RuntimeError("API 审核需要 requests 库: pip install requests")

    mod_cfg = config["moderation"]
    api_url = mod_cfg["api_url"].rstrip("/")
    payload = {
        "content": text,
        "type": mod_cfg.get("type", "post"),
        "model": "auto",
        "strictness": mod_cfg.get("strictness", "standard"),
    }
    headers = {
        "X-Project-Key": mod_cfg["api_key"],
        "Content-Type": "application/json",
    }

    last_err = None
    for attempt in range(3):
        try:
            resp = req.post(
                f"{api_url}/v2/moderations", json=payload, headers=headers, timeout=15
            )
            if resp.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", {}).get("result", {})
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2)
    raise RuntimeError(f"审核 API 失败（重试3次）: {last_err}")


# ─── 提交审核结果 ───

def submit_review(
    client: SiteClient, item_id: Any, approved: bool, reason: str, config: Dict[str, Any]
) -> Dict[str, str]:
    submit_cfg = config["submit"]
    url = client._resolve_endpoint("submit")
    status = submit_cfg["approve_status"] if approved else submit_cfg["reject_status"]
    data = {
        "id": str(item_id),
        "status": str(status),
        "reason": reason if not approved else "",
    }
    resp = client.curl_json(url, method="POST", data=data)

    if resp.get("code") == -9999 and "不允许" in str(resp.get("msg", "")):
        return {"status": "skipped", "reason": "已被其他人审核"}
    if resp.get("code") != 0:
        return {"status": "error", "reason": str(resp.get("msg", resp))}
    return {"status": "ok"}


# ─── 内容提取 ───

def extract_content(item: Dict, content_fields: List[str]) -> str:
    parts = []
    for field in content_fields:
        val = item.get(field)
        if val is None:
            continue
        if isinstance(val, list):
            parts.append(" ".join(str(v) for v in val))
        elif isinstance(val, dict):
            parts.append(json.dumps(val, ensure_ascii=False))
        else:
            parts.append(str(val))
    return "\n".join(p for p in parts if p.strip())


# ─── 主审核流程 ───

def run_review(config: Dict[str, Any], dry_run: bool = False, max_pages: int = 10,
               rules_path: Optional[str] = None):
    """主审核流程：拉取 → 本地规则判断（+ 可选 API）→ 提交"""
    client = SiteClient(config)
    content_fields = config.get("moderation", {}).get("content_fields", ["title", "content"])
    use_api = has_moderation_api(config)
    rules = load_rules(rules_path)

    if rules:
        enabled_count = len(rules)
        log(f"已加载 {enabled_count} 条审核规则")
    else:
        log("未加载本地规则")

    if use_api:
        log("已配置审核 API（本地规则 + API 双重审核）")

    stats = {"total": 0, "approved": 0, "rejected": 0, "flagged": 0, "skipped": 0, "error": 0}

    try:
        login(client, config)

        items, total = fetch_pending(client, config, page=1)
        if total == 0 and not items:
            log("无待审内容")
            return stats
        log(f"待审总量: {total} 条")

        page = 1
        while items and page <= max_pages:
            log(f"── 第 {page} 页（{len(items)} 条）──")

            for item in items:
                item_id = item.get("id", "?")
                stats["total"] += 1

                text = extract_content(item, content_fields)
                if not text.strip():
                    log(f"  [{item_id}] 无内容，跳过")
                    stats["skipped"] += 1
                    continue

                # 第一层：本地规则
                rule_hit = apply_rules(item, content_fields, rules) if rules else None

                if rule_hit:
                    reason = rule_hit["reason"]
                    rule_id = rule_hit.get("rule_id", "?")
                    if not dry_run:
                        submit_review(client, item_id, False, reason, config)
                    stats["rejected"] += 1
                    log(f"  [{item_id}] REJECT [{rule_id}]: {reason}")
                    continue

                # 第二层：API 审核（可选）
                if use_api:
                    try:
                        api_result = moderate_via_api(text, config)
                    except Exception as e:
                        log(f"  [{item_id}] API 异常: {e}")
                        stats["error"] += 1
                        continue

                    verdict = api_result.get("verdict", "flagged")
                    reason = api_result.get("reason", "")
                    confidence = api_result.get("confidence", 0)
                    model_used = api_result.get("model_used", "?")

                    if verdict == "rejected":
                        if not dry_run:
                            submit_review(client, item_id, False, reason, config)
                        stats["rejected"] += 1
                        log(f"  [{item_id}] REJECT: {reason} ({confidence:.0%}, {model_used})")
                        continue
                    elif verdict == "flagged":
                        stats["flagged"] += 1
                        log(f"  [{item_id}] FLAG: {reason} ({confidence:.0%}, {model_used})")
                        continue

                # 通过（本地规则通过 + API通过或未配置API）
                if not dry_run:
                    submit_review(client, item_id, True, "", config)
                stats["approved"] += 1
                log(f"  [{item_id}] PASS")

            page += 1
            items, _ = fetch_pending(client, config, page=1)

        mode = "[DRY RUN] " if dry_run else ""
        log(f"{mode}完成: 共{stats['total']}条 | 通过{stats['approved']} | "
            f"拒绝{stats['rejected']} | 待复审{stats['flagged']} | "
            f"跳过{stats['skipped']} | 异常{stats['error']}")
    finally:
        client.cleanup()

    return stats


# ─── 仅拉取模式 ───

def run_fetch(config: Dict[str, Any], output_path: str = "pending_review.json", max_pages: int = 10):
    """拉取待审内容，输出为 JSON"""
    client = SiteClient(config)
    content_fields = config.get("moderation", {}).get("content_fields", ["title", "content"])
    all_items = []

    try:
        login(client, config)
        items, total = fetch_pending(client, config, page=1)
        if total == 0 and not items:
            log("无待审内容")
            return []
        log(f"待审总量: {total} 条")

        page = 1
        while items and page <= max_pages:
            for item in items:
                item_id = item.get("id", "?")
                text = extract_content(item, content_fields)
                all_items.append({
                    "id": item_id,
                    "content": text,
                    "raw_fields": {f: item.get(f) for f in content_fields if item.get(f)},
                })
            page += 1
            if page <= max_pages:
                items, _ = fetch_pending(client, config, page=page)
            else:
                break
    finally:
        client.cleanup()

    Path(output_path).write_text(
        json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"已导出 {len(all_items)} 条待审内容 → {output_path}")
    return all_items


# ─── 提交决定模式 ───

def run_submit(config: Dict[str, Any], decisions_path: str, dry_run: bool = False):
    """读取 decisions.json，提交审核结果"""
    p = Path(decisions_path)
    if not p.exists():
        sys.exit(f"决定文件不存在: {p}")
    decisions = json.loads(p.read_text(encoding="utf-8"))
    if not decisions:
        log("决定文件为空")
        return

    client = SiteClient(config)
    stats = {"submitted": 0, "skipped": 0, "error": 0}

    try:
        login(client, config)
        log(f"提交 {len(decisions)} 条审核决定...")

        for d in decisions:
            item_id = d.get("id")
            verdict = d.get("verdict", "")
            reason = d.get("reason", "")
            if not item_id:
                continue

            if verdict == "approved":
                approved = True
            elif verdict == "rejected":
                approved = False
            else:
                log(f"  [{item_id}] 跳过（{verdict}）")
                stats["skipped"] += 1
                continue

            if dry_run:
                action = "PASS" if approved else f"REJECT: {reason}"
                log(f"  [{item_id}] [DRY RUN] {action}")
                stats["submitted"] += 1
                continue

            result = submit_review(client, item_id, approved, reason, config)
            if result["status"] == "ok":
                action = "PASS" if approved else f"REJECT: {reason}"
                log(f"  [{item_id}] {action}")
                stats["submitted"] += 1
            elif result["status"] == "skipped":
                log(f"  [{item_id}] 已被其他人审核")
                stats["skipped"] += 1
            else:
                log(f"  [{item_id}] 失败: {result.get('reason', '?')}")
                stats["error"] += 1

        mode = "[DRY RUN] " if dry_run else ""
        log(f"{mode}提交完成: 成功{stats['submitted']} | 跳过{stats['skipped']} | 失败{stats['error']}")
    finally:
        client.cleanup()


# ─── 配置加载 ───

def load_config(path: str) -> Dict[str, Any]:
    p = Path(path).resolve()
    if not p.exists():
        sys.exit(f"配置文件不存在: {p}")
    config = json.loads(p.read_text(encoding="utf-8"))

    required = [
        ("site.base_url", config.get("site", {}).get("base_url")),
        ("site.module", config.get("site", {}).get("module")),
        ("auth.username", config.get("auth", {}).get("username")),
        ("auth.password", config.get("auth", {}).get("password")),
        ("auth.totp_seed", config.get("auth", {}).get("totp_seed")),
    ]
    missing = [name for name, val in required if not val]
    if missing:
        sys.exit(f"配置缺少必填项: {', '.join(missing)}")

    return config


# ─── CLI ───

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="review",
        description="通用内容审核 — 配置驱动，适用于所有 d.php 后台站点",
    )
    parser.add_argument("--config", default="config.json", help="配置文件路径（默认: config.json）")
    parser.add_argument("--rules", default=None, help="规则文件路径（默认: 同目录下 rules.json）")
    parser.add_argument("--dry-run", action="store_true", help="只判断不提交结果")
    parser.add_argument("--max-pages", type=int, default=None, help="最大处理页数")
    parser.add_argument("--fetch-only", action="store_true", help="只拉取待审列表，不判断不提交")
    parser.add_argument("--output", default="pending_review.json", help="拉取模式输出路径")
    parser.add_argument("--decisions", metavar="FILE", help="提交审核决定文件")
    args = parser.parse_args()

    config = load_config(args.config)
    max_pages = args.max_pages or config.get("fetch", {}).get("max_pages", 10)
    site_name = config["site"].get("name", config["site"]["module"])

    if args.decisions:
        log(f"═══ 通用审核 [{site_name}] — 提交决定 ═══")
        run_submit(config, args.decisions, dry_run=args.dry_run)
        return 0

    if args.fetch_only:
        log(f"═══ 通用审核 [{site_name}] — 拉取待审 ═══")
        run_fetch(config, output_path=args.output, max_pages=max_pages)
        return 0

    mode = "DRY RUN" if args.dry_run else "LIVE"
    log(f"═══ 通用审核 [{site_name}] ({mode}) ═══")
    stats = run_review(config, dry_run=args.dry_run, max_pages=max_pages, rules_path=args.rules)
    return 0 if stats["error"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
