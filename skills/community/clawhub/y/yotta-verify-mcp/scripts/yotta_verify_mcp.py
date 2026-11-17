#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_verify_mcp.py — 元信 MCP server（yotta-verify-mcp）。

stdio MCP server（JSON-RPC 2.0，换行分隔），把 yotta-verify（元信）装前安全扫描
暴露为 MCP 工具：scan_skill / generate_badge / gate_check / get_report。

复用 yotta_verify.py 内核（同一规则表 verify_rules.py 单源），本地离线静态扫描；
不上传被测内容、不执行被测代码、不联网（目录扫描完全离线；npm 包扫描仅下载公开包）。

运行：python scripts/yotta_verify_mcp.py
MCP 客户端配置：
  {"mcpServers":{"yotta-verify-mcp":{"command":"python",
    "args":["<绝对路径>/scripts/yotta_verify_mcp.py"]}}}
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import yotta_verify as yv  # noqa: E402

VERSION = "0.4.7"
TOOL_NAME = "yotta-verify-mcp"
CN_NAME = "元信"
MCP_PROTOCOL_MODERN = "2026-07-28"
MCP_PROTOCOL_LEGACY = "2025-11-25"
SERVER_INFO = {"name": TOOL_NAME, "version": VERSION}
SERVERS = {TOOL_NAME: {"name": TOOL_NAME, "cn": CN_NAME, "version": VERSION}}


def _tool_error(message, extra=None):
    """构造工具调用错误结果（isError=true）。"""
    payload = {"error": message}
    if extra:
        payload.update(extra)
    return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
            "isError": True}


def _resolve_target(target, tmp_dirs):
    """把 target 解析为本地路径/压缩包路径；npm 包名则 npm pack 到临时目录。"""
    p = Path(target)
    if p.exists():
        return str(p)
    # 非本地路径：尝试当作 npm 包名下载后本地扫描（仅下载公开包，不上传被测内容）
    tmp = tempfile.mkdtemp(prefix="yottamcp-")
    tmp_dirs.append(tmp)
    try:
        r = subprocess.run(
            ["npm", "pack", target, "--pack-destination", tmp],
            capture_output=True, text=True, timeout=120)
    except Exception as e:  # noqa: BLE001
        raise ValueError("npm pack 调用失败：%s" % e)
    if r.returncode != 0:
        err = (r.stderr or r.stdout or "").strip()[:300]
        raise ValueError("无法解析目标 %s（不是本地路径，且 npm pack 失败）：%s" % (target, err))
    tarballs = [f for f in os.listdir(tmp) if f.endswith(".tgz")]
    if not tarballs:
        raise ValueError("npm pack 未产出 tarball：%s" % target)
    return os.path.join(tmp, tarballs[0])


def _scan(target):
    """扫描 target，返回 (findings, counts, verdict, meta, error)。"""
    tmp_dirs = []
    try:
        path = _resolve_target(target, tmp_dirs)
        findings, counts, verdict, meta = yv.scan_core(path, auto_name_hint=True)
        return findings, counts, verdict, meta, None
    except SystemExit as e:
        return None, None, None, None, str(e)
    except Exception as e:  # noqa: BLE001
        return None, None, None, None, str(e)
    finally:
        for d in tmp_dirs:
            shutil.rmtree(d, ignore_errors=True)


def _tool_scan_skill(params):
    target = params.get("target")
    if not target:
        return _tool_error("scan_skill 需要 target 参数")
    findings, counts, verdict, meta, err = _scan(target)
    if err:
        return _tool_error("扫描失败：%s" % err, {"verdict": None, "meta": {"target": target}})
    text = yv.render_json(findings, counts, verdict, meta)
    return {"content": [{"type": "text", "text": text}], "isError": False}


def _tool_generate_badge(params):
    target = params.get("target")
    verdict = params.get("verdict")
    if not verdict and target:
        findings, counts, v, meta, err = _scan(target)
        if err:
            return _tool_error("扫描失败：%s" % err, {"meta": {"target": target}})
        verdict = v
    if not verdict:
        verdict = yv.VERDICT_SAFE
    validate = params.get("validate")
    if validate is not None:
        validate = str(validate).upper()
        if validate not in ("PASS", "FAIL"):
            validate = None
    extra = {
        "validate": validate,
        "vetter": params.get("vetter"),
        "audit": params.get("audit"),
        "version": params.get("version") or yv.VERSION,
        "tests": params.get("tests"),
    }
    svg, url = yv.build_badges(verdict, extra)
    result = {"verdict": verdict, "svg": svg, "url": url}
    out = params.get("out")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(svg, encoding="utf-8")
        result["file"] = str(out)
    return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
            "isError": False}


def _tool_gate_check(params):
    target = params.get("target")
    if not target:
        return _tool_error("gate_check 需要 target 参数")
    findings, counts, verdict, meta, err = _scan(target)
    if err:
        return _tool_error("扫描失败：%s" % err, {"meta": {"target": target}})
    limit_sev = (params.get("max_severity") or "medium").lower()
    limit = yv._SEVERITY_VALUE.get(limit_sev, 1)
    worst = yv.verdict_worst(findings)
    worst_val = yv._SEVERITY_VALUE.get(worst, 0)
    code = yv.exit_code_of(verdict)
    passed = worst_val <= limit
    result = {
        "verdict": verdict,
        "worst": worst,
        "max_severity": limit_sev,
        "pass": passed,
        "code": code if passed else max(code, 1),
    }
    return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
            "isError": False}


def _tool_get_report(params):
    target = params.get("target")
    if not target:
        return _tool_error("get_report 需要 target 参数")
    fmt = (params.get("format") or "markdown").lower()
    if fmt not in ("json", "markdown"):
        return _tool_error("get_report 的 format 只能为 json 或 markdown")
    findings, counts, verdict, meta, err = _scan(target)
    if err:
        return _tool_error("扫描失败：%s" % err, {"meta": {"target": target}})
    if fmt == "json":
        text = yv.render_json(findings, counts, verdict, meta)
    else:
        text = yv.render_markdown(findings, counts, verdict, meta)
    out = params.get("out")
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return {"content": [{"type": "text", "text": text}], "isError": False}


TOOL_HANDLERS = {
    "scan_skill": _tool_scan_skill,
    "generate_badge": _tool_generate_badge,
    "gate_check": _tool_gate_check,
    "get_report": _tool_get_report,
}


def mcp_tools():
    """返回 MCP tools 列表（name / description / inputSchema）。"""
    return [
        {
            "name": "scan_skill",
            "description": (
                "装前安全扫描（元信 yotta-verify）。扫描一个技能目录、.tgz 压缩包或 npm 包，"
                "返回 verdict（SAFE TO INSTALL / INSTALL WITH CAUTION / REVIEW REQUIRED / "
                "DO NOT INSTALL）+ 按严重级统计 + 发现列表（提示注入/危险模式/SKILL 完整性）。"
                "本地离线静态扫描，不上传被测内容、不执行被测代码。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string",
                               "description": "技能目录路径、.tgz/.tar.gz 路径，或 npm 包名（自动 npm pack 下载后本地扫描）"}
                },
                "required": ["target"],
            },
        },
        {
            "name": "generate_badge",
            "description": (
                "生成 audited 徽章（本地 SVG + shields.io URL）。可给 target 自动扫描取得 verdict，"
                "或直接给 verdict，并可附加 validate/vetter/audit/version/tests 分段。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "可选：目录/包，用于自动扫描取得 verdict"},
                    "verdict": {"type": "string", "description": "可选：直接指定 verdict"},
                    "validate": {"type": "string", "enum": ["pass", "fail"], "description": "validate-skill 结果"},
                    "vetter": {"type": "string", "description": "vetter 结论"},
                    "audit": {"type": "string", "description": "audit 结论"},
                    "version": {"type": "string", "description": "版本标签"},
                    "tests": {"type": "integer", "description": "测试数"},
                    "out": {"type": "string", "description": "可选：将 SVG 写入该路径"}
                },
            },
        },
        {
            "name": "gate_check",
            "description": (
                "CI 闸门。扫描 target，判断最严重级是否超过 max_severity 阈值（默认 medium）；"
                "返回 pass/verdict/worst/exit code。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "目录/包路径"},
                    "max_severity": {"type": "string", "enum": ["info", "low", "medium", "high", "critical"],
                                     "description": "允许的最大严重级（默认 medium）"}
                },
                "required": ["target"],
            },
        },
        {
            "name": "get_report",
            "description": (
                "生成验证报告。扫描 target 并按 format 返回 Markdown 或 JSON 报告；"
                "可写 out 路径。报告与 CLI 同一格式（verify_rules.py 单源）。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "目录/包路径"},
                    "format": {"type": "string", "enum": ["json", "markdown"], "description": "报告格式（默认 markdown）"},
                    "out": {"type": "string", "description": "可选：将报告写入该路径"}
                },
                "required": ["target"],
            },
        },
    ]


def _req_version(params):
    """取请求声明的最新协议版本（modern _meta 字段）；无 = legacy。"""
    meta = (params or {}).get("_meta") or {}
    return meta.get("io.modelcontextprotocol/protocolVersion")


def _modern_ok(payload, cache=None):
    """modern 结果包装：resultType + _meta.serverInfo（list/discover 加 ttlMs/cacheScope）。"""
    out = {"resultType": "complete"}
    out.update(payload)
    out["_meta"] = {"io.modelcontextprotocol/serverInfo": dict(SERVER_INFO)}
    if cache:
        out["ttlMs"] = cache[0]
        out["cacheScope"] = cache[1]
    return out


def _unsupported_version(rid, pv):
    return {
        "jsonrpc": "2.0", "id": rid,
        "error": {
            "code": -32022,
            "message": "Unsupported protocol version",
            "data": {"supported": [MCP_PROTOCOL_MODERN], "requested": pv},
        },
    }


def handle_message(msg):
    """处理一行 JSON-RPC 消息，返回响应 dict；通知返回 None。

    双时代（dual-era）：请求 _meta 带 io.modelcontextprotocol/protocolVersion =
    modern（2026-07-28 无状态，server/discover 取代握手）；无该字段 = legacy
    （2025-11-25 及更早，initialize 握手），响应保持旧形状。
    """
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
        rid = msg.get("id") if isinstance(msg, dict) else None
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "invalid request"}}
    method = msg.get("method")
    rid = msg.get("id")
    if rid is None:  # JSON-RPC 通知（无 id）不响应
        return None
    if method is None:
        return None
    params = msg.get("params") or {}
    pv = _req_version(params)

    if pv is not None:
        # ---- modern（2026-07-28 无状态）----
        if pv != MCP_PROTOCOL_MODERN:
            return _unsupported_version(rid, pv)
        if method == "server/discover":
            return {
                "jsonrpc": "2.0", "id": rid,
                "result": _modern_ok({
                    "supportedVersions": [MCP_PROTOCOL_MODERN],
                    "capabilities": {"tools": {}},
                    "instructions": (
                        "元信 MCP（基于 MCP 最新协议 2026-07-28，向后兼容 2025-11-25 及更早握手）："
                        "装前安全扫描 scan_skill / generate_badge / gate_check / get_report；"
                        "本地离线静态扫描，数据不出本机。"
                    ),
                }, (3600000, "public")),
            }
        if method == "tools/list":
            return {
                "jsonrpc": "2.0", "id": rid,
                "result": _modern_ok({"tools": mcp_tools()}, (300000, "public")),
            }
        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}
            handler = TOOL_HANDLERS.get(name)
            if not handler:
                return {
                    "jsonrpc": "2.0", "id": rid,
                    "result": _modern_ok({"content": [{"type": "text", "text": "未知工具: %s" % name}], "isError": True}),
                }
            try:
                return {"jsonrpc": "2.0", "id": rid, "result": _modern_ok(handler(arguments))}
            except Exception as e:  # noqa: BLE001
                return {
                    "jsonrpc": "2.0", "id": rid,
                    "result": _modern_ok({"content": [{"type": "text", "text": "工具执行异常：%s" % e}], "isError": True}),
                }
        if method == "initialize":
            return {
                "jsonrpc": "2.0", "id": rid,
                "error": {
                    "code": -32601,
                    "message": "initialize removed in MCP 2026-07-28; use server/discover. supported: ['2026-07-28']",
                },
            }
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found: " + str(method)}}

    # ---- legacy（<=2025-11-25，initialize 握手；响应保持旧形状）----
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": rid,
            "result": {
                "protocolVersion": MCP_PROTOCOL_LEGACY,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": mcp_tools()}}
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        handler = TOOL_HANDLERS.get(name)
        if not handler:
            return {
                "jsonrpc": "2.0", "id": rid,
                "result": {"content": [{"type": "text", "text": "未知工具: %s" % name}], "isError": True},
            }
        try:
            return {
                "jsonrpc": "2.0", "id": rid,
                "result": handler(arguments),
            }
        except Exception as e:  # noqa: BLE001
            return {
                "jsonrpc": "2.0", "id": rid,
                "result": {"content": [{"type": "text", "text": "工具执行异常：%s" % e}], "isError": True},
            }
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found: " + str(method)}}

def main():
    """stdio 主循环：读行 -> JSON-RPC -> 响应行。"""
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps(
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}},
                ensure_ascii=False) + "\n")
            sys.stdout.flush()
            continue
        resp = handle_message(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
