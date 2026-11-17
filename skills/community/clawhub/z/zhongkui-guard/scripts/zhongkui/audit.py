from __future__ import annotations

import json
import os
import ipaddress
import socket
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

TASKS = [
    {"id":"math-1", "kind":"logic", "prompt":"只输出 JSON：计算 17*3+2 的结果，键为 answer。", "expected":"53"},
    {"id":"json-1", "kind":"structure", "prompt":"只输出 JSON 对象 {\"status\":\"ok\",\"items\":[1,2]}。", "expected":"status"},
    {"id":"context-1", "kind":"context", "prompt":"记录：A=青，B=红，C=绿。只输出 JSON：B 的颜色，键为 answer。", "expected":"红"},
    {"id":"logic-1", "kind":"logic", "prompt":"只输出 JSON：如果所有猫是动物，咪咪是猫，咪咪是否是动物？键为 answer。", "expected":"true"},
]

@dataclass
class Endpoint:
    name: str; base_url: str; protocol: str; model: str; key_env: str; local_mode: bool

def _load(name: str, config: dict) -> Endpoint:
    value = config.get("endpoints", {}).get(name)
    if not value: raise ValueError("未找到目标端点别名")
    url = value.get("base_url", "")
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password: raise ValueError("端点必须是明确的 HTTPS URL")
    return Endpoint(name, url.rstrip("/"), value.get("protocol", ""), value.get("model", ""), value.get("api_key_env", ""), bool(value.get("local_mode", False)))

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): raise urllib.error.HTTPError(req.full_url, code, "不允许重定向", headers, fp)

def _payload(endpoint: Endpoint, prompt: str, limit: int) -> tuple[str, dict]:
    if endpoint.protocol == "openai-chat": return "/chat/completions", {"model":endpoint.model,"messages":[{"role":"user","content":prompt}],"max_tokens":limit,"temperature":0}
    if endpoint.protocol == "openai-responses": return "/responses", {"model":endpoint.model,"input":prompt,"max_output_tokens":limit}
    if endpoint.protocol == "anthropic-messages": return "/messages", {"model":endpoint.model,"messages":[{"role":"user","content":prompt}],"max_tokens":limit}
    raise ValueError("不支持的协议")

def _content(protocol: str, value: dict) -> str:
    if protocol == "openai-chat": return value["choices"][0]["message"]["content"]
    if protocol == "openai-responses": return value["output"][0]["content"][0]["text"]
    return value["content"][0]["text"]

def _request(endpoint: Endpoint, prompt: str, limit: int) -> str:
    key = os.environ.get(endpoint.key_env)
    if not key: raise ValueError(f"缺少端点凭据环境变量：{endpoint.key_env}")
    hostname = urllib.parse.urlparse(endpoint.base_url).hostname
    addresses = {record[4][0] for record in socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)}
    if not endpoint.local_mode and any(ipaddress.ip_address(address).is_private or ipaddress.ip_address(address).is_loopback or ipaddress.ip_address(address).is_link_local for address in addresses):
        raise ValueError("公网端点解析到本地或内网地址，已拒绝发送凭据")
    suffix, body = _payload(endpoint, prompt, limit)
    headers = {"Content-Type":"application/json"}
    if endpoint.protocol == "anthropic-messages": headers.update({"anthropic-version":"2023-06-01", "x-api-key":key})
    else: headers["Authorization"] = f"Bearer {key}"
    request = urllib.request.Request(endpoint.base_url + suffix, data=json.dumps(body).encode(), headers=headers, method="POST")
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl.create_default_context()), NoRedirect())
    with opener.open(request, timeout=30) as response:
        return _content(endpoint.protocol, json.loads(response.read(1_000_000).decode("utf-8")))

def _score(answer: str, expected: str) -> bool:
    return expected.lower() in answer.lower()

def audit(args: Any) -> dict:
    config = json.loads(open(args.config, encoding="utf-8").read())
    target = _load(args.target, config); reference = _load(args.reference, config) if args.reference else None
    budget = config.get("budget", {}); maximum = min(args.max_requests or budget.get("max_requests", 24), 60)
    tokens = min(args.max_output_tokens or budget.get("max_output_tokens_per_request", 512), 1024)
    planned = {"schema_version":"1.0", "operation":"audit", "status":"planned", "target":target.name, "reference":reference.name if reference else None, "requests_max":min(maximum, len(TASKS) * (2 if reference else 1)), "max_output_tokens":tokens, "task_categories":sorted({t["kind"] for t in TASKS}), "network_request_sent":False, "limitations":["合成题初筛，非模型身份认证", "未知服务价格时费用未知"], "summary":"体检计划已生成，未发送网络请求"}
    if args.plan: return planned
    results=[]; started=time.monotonic(); calls=0
    for task in TASKS:
        if calls >= maximum: break
        try:
            answer = _request(target, task["prompt"], tokens); calls += 1
            results.append({"id":task["id"],"kind":task["kind"],"target_pass":_score(answer, task["expected"])})
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError, TimeoutError) as exc:
            results.append({"id":task["id"],"kind":task["kind"],"error":type(exc).__name__})
    valid=[r for r in results if "target_pass" in r]
    passed=sum(r["target_pass"] for r in valid)
    return {"schema_version":"1.0", "operation":"audit", "status":"completed" if len(results)==len(TASKS) else "partial", "target":target.name, "quality":{"valid_samples":len(valid),"passed":passed,"coverage":len(valid)/len(TASKS),"failures":[r for r in results if "error" in r]}, "consistency":{"status":"not_evaluated" if not reference else "not_implemented_v0_1"}, "conclusion":"capability_only" if not reference else "insufficient_evidence", "requests_sent":calls, "elapsed_seconds":round(time.monotonic()-started,2), "limitations":["题库规模有限，不能证明模型身份或长期稳定性"], "summary":"模型体检完成"}
