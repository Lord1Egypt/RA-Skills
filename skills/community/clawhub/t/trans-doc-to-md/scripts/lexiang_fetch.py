#!/usr/bin/env python3
"""乐享文档链接 → 解析 markdown + 下载图片并填充到对应位置。

默认流程：
  1. entry_describe_ai_parse_content 获取 AI 解析 markdown（data.content）
  2. 从 [IMAGE] 块与行内 `![](/assets/{id})` 提取 asset_id
  3. GET https://lxapi.lexiangla.com/cgi-bin/v1/assets/{asset_id} 下载图片
  4. 按原文顺序替换为 ![title](images/img_NNN.ext)，并剔除 `<image_ocr>` 等元数据

用法：
    python3 lexiang_fetch.py <entry_id|lexiang_url> [--out-dir DIR] [--skip-images] [--download-pdf]

输出（默认 ./<safe_title>/）：
    parsed_raw.md           原始解析（含 [IMAGE] 块，备查）
    source.md               图片已填充，供后续清洗/翻译（主工作文件）
    images/                 img_000.png ...
    images.json             图片清单（含 downloaded 状态）
    meta.json               条目元信息
    paper.pdf               （--download-pdf 时）原 PDF，pymupdf 降级用

Token：~/.cursor/mcp.json → mcpServers.lexiang.headers.Authorization
company_from：mcp URL 查询参数，或环境变量 LEXIANG_COMPANY_FROM

本脚本仅负责「获取」；上传到乐享请用独立 Skill
upload-markdown-to-lexiang 的公共 CLI。
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

MCP_BASE = os.environ.get("MCP_BASE_URL", "https://mcp.lexiang-app.com")
ASSET_API = "https://lxapi.lexiangla.com/cgi-bin/v1/assets/{asset_id}"
ENTRY_URL_RE = re.compile(
    r"(?:https?://)?(?:[\w.-]+\.)?lexiangla\.com/pages/([a-f0-9]{32})",
    re.I,
)
ASSET_ID_RE = re.compile(r"/assets/([a-f0-9]+)", re.I)
IMAGE_OCR_RE = re.compile(r"<image_ocr>.*?</image_ocr>", re.IGNORECASE | re.DOTALL)
INLINE_ASSET_RE = re.compile(
    r"!\[([^\]]*)\]\(/assets/([a-f0-9]+)\)(?:<image_ocr>.*?</image_ocr>)?",
    re.IGNORECASE | re.DOTALL,
)


def load_mcp_config() -> tuple[str, str]:
    """返回 (authorization_header, company_from)。"""
    p = os.path.expanduser("~/.cursor/mcp.json")
    if not os.path.exists(p):
        raise SystemExit("ERROR: ~/.cursor/mcp.json 不存在，无法读取乐享 token")
    d = json.load(open(p))
    srv = d.get("mcpServers", {}).get("lexiang", {})
    auth = srv.get("headers", {}).get("Authorization", "")
    if not auth:
        raise SystemExit("ERROR: mcp.json 中未找到 lexiang Authorization")
    if not auth.lower().startswith("bearer "):
        auth = "Bearer " + auth

    company_from = os.environ.get("LEXIANG_COMPANY_FROM", "") or os.environ.get("COMPANY_FROM", "")
    url = srv.get("url", "")
    m = re.search(r"[?&]company_from=([^&]+)", url)
    if m:
        company_from = m.group(1)
    if not company_from:
        raise SystemExit("ERROR: company_from 未找到（检查 mcp.json URL 或 LEXIANG_COMPANY_FROM）")
    return auth, company_from


def mcp_call(name: str, arguments: dict, auth: str, company_from: str) -> dict:
    url = f"{MCP_BASE}/mcp?company_from={company_from}"
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": auth},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise SystemExit("ERROR: 乐享 token 已过期（401）")
        raise SystemExit(f"ERROR: MCP HTTP {e.code}")
    if "error" in result:
        raise SystemExit(f"MCP error: {result['error']}")
    inner = json.loads(result["result"]["content"][0]["text"])
    if inner.get("code", 0) != 0:
        raise SystemExit(f"MCP {name} failed: {inner.get('message', inner)}")
    return inner


def parse_entry_id(arg: str) -> str:
    arg = arg.strip()
    m = ENTRY_URL_RE.search(arg)
    if m:
        return m.group(1)
    if re.fullmatch(r"[a-f0-9]{32}", arg, re.I):
        return arg
    raise SystemExit(f"ERROR: 无法识别 entry_id: {arg}")


def ext_from_content_type(ctype: str, data: bytes) -> str:
    ctype = (ctype or "").lower()
    if "png" in ctype:
        return ".png"
    if "jpeg" in ctype or "jpg" in ctype:
        return ".jpg"
    if "webp" in ctype:
        return ".webp"
    if "gif" in ctype:
        return ".gif"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:2] == b"\xff\xd8":
        return ".jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return ".png"


def download_asset(asset_id: str, token: str, out_path_no_ext: str) -> tuple[str | None, str]:
    """下载 asset：先调 lxapi 拿签名 URL，再下载图片二进制。"""
    api_url = ASSET_API.format(asset_id=asset_id)
    req = urllib.request.Request(api_url, headers={"Authorization": token}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            ctype = resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, str(e.reason)

    if not body:
        return None, "empty body"

    # lxapi 返回 JSON：{"url": "...", "mime_type": "image/png"}
    download_url = ""
    mime = ""
    if "json" in ctype.lower() or body[:1] == b"{":
        try:
            meta = json.loads(body.decode())
            download_url = meta.get("url", "")
            mime = meta.get("mime_type", "")
            if not download_url:
                return None, meta.get("message", "missing url in asset response")
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            return None, f"invalid asset json: {e}"
        try:
            with urllib.request.urlopen(download_url, timeout=120) as resp:
                data = resp.read()
                if not mime:
                    mime = resp.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            return None, f"download HTTP {e.code}"
        except urllib.error.URLError as e:
            return None, f"download: {e.reason}"
    else:
        data = body
        mime = ctype

    if not data:
        return None, "empty image body"

    ext = ext_from_content_type(mime, data)
    local = out_path_no_ext + ext
    os.makedirs(os.path.dirname(local), exist_ok=True)
    with open(local, "wb") as f:
        f.write(data)
    rel = f"images/{os.path.basename(local)}"
    return rel.replace("\\", "/"), ""


def parse_image_block(lines: list[str], start: int) -> tuple[dict, int]:
    """解析 [IMAGE]...[/IMAGE]，返回字段 dict 与结束行 index（含 [/IMAGE]）。"""
    link = title = desc = ""
    j = start + 1
    n = len(lines)
    while j < n and lines[j].strip() != "[/IMAGE]":
        ln = lines[j]
        if ln.startswith("图片链接"):
            link = ln.split("：", 1)[-1].strip()
        elif ln.startswith("图片标题"):
            title = ln.split("：", 1)[-1].strip()
        elif ln.startswith("图片描述"):
            desc = ln.split("：", 1)[-1].strip()
        j += 1
    if j >= n:
        j = start
    asset_m = ASSET_ID_RE.search(link)
    return {
        "asset_link": link,
        "asset_id": asset_m.group(1) if asset_m else "",
        "title": title,
        "desc": desc,
    }, j


def strip_image_metadata(text: str) -> str:
    """移除图片提取元数据（OCR 标签等），不进入 source.md。"""
    text = IMAGE_OCR_RE.sub("", text)
    cleaned: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            cleaned.append(line)
            continue
        if stripped.startswith(("[IMAGE]", "[/IMAGE]")):
            continue
        if re.match(r"^图片(?:链接|标题|描述|OCR结果)\s*[：:]", stripped):
            continue
        cleaned.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned))


def _image_record(
    *,
    index: int,
    page: int,
    asset_id: str,
    title: str = "",
    desc: str = "",
    kind: str = "block",
    context: str = "",
) -> dict:
    return {
        "index": index,
        "page": page,
        "kind": kind,
        "asset_link": f"/assets/{asset_id}" if asset_id else "",
        "asset_id": asset_id,
        "title": title,
        "desc": desc,
        "context": context,
        "downloaded": False,
        "local_path": "",
        "error": "",
    }


def build_image_inventory(content: str) -> list[dict]:
    """按文档顺序收集 [IMAGE] 块与行内 /assets/ 引用。"""
    lines = content.split("\n")
    cur_page, imgs, i, n = 0, [], 0, len(lines)
    while i < n:
        m = re.search(r'page-number", "value": (\d+)', lines[i])
        if m:
            cur_page = int(m.group(1))
        if lines[i].strip() == "[IMAGE]":
            info, j = parse_image_block(lines, i)
            ctx = ""
            for k in range(j + 1, min(j + 6, n)):
                t = lines[k].strip()
                if t and t != "[IMAGE]":
                    ctx = t[:80]
                    break
            imgs.append(
                _image_record(
                    index=len(imgs),
                    page=cur_page,
                    asset_id=info["asset_id"],
                    title=info["title"],
                    desc=info["desc"],
                    kind="block",
                    context=ctx,
                )
            )
            i = j + 1
            continue
        for match in INLINE_ASSET_RE.finditer(lines[i]):
            imgs.append(
                _image_record(
                    index=len(imgs),
                    page=cur_page,
                    asset_id=match.group(2),
                    title=match.group(1),
                    kind="inline",
                    context=lines[i].strip()[:80],
                )
            )
        i += 1
    return imgs


def _download_image(
    rec: dict,
    img_idx: int,
    out_dir: str,
    token: str,
    skip_download: bool,
) -> None:
    rel_path = ""
    err = ""
    asset_id = rec.get("asset_id", "")
    if not skip_download and asset_id:
        base = os.path.join(out_dir, "images", f"img_{img_idx:03d}")
        rel_path, err = download_asset(asset_id, token, base)
    elif not asset_id:
        err = "missing asset_id"
    rec["downloaded"] = bool(rel_path)
    rec["local_path"] = rel_path or ""
    rec["error"] = err


def _image_markdown(rec: dict, img_idx: int) -> str | None:
    rel_path = rec.get("local_path", "")
    if not rel_path:
        return None
    alt = rec.get("title") or f"image_{img_idx}"
    alt = alt.replace("[", "").replace("]", "")
    return f"![{alt}]({rel_path})"


def fill_images(content: str, out_dir: str, token: str, skip_download: bool) -> tuple[str, list[dict]]:
    """将 [IMAGE] 块与行内 /assets/ 引用替换为本地图片，并剔除 OCR 元数据。"""
    lines = content.split("\n")
    out: list[str] = []
    imgs = build_image_inventory(content)
    img_map = {x["index"]: x for x in imgs}
    img_idx = 0
    i, n = 0, len(lines)
    os.makedirs(os.path.join(out_dir, "images"), exist_ok=True)

    while i < n:
        if lines[i].strip() == "[IMAGE]":
            info, j = parse_image_block(lines, i)
            rec = img_map[img_idx]
            _download_image(rec, img_idx, out_dir, token, skip_download)
            md = _image_markdown(rec, img_idx)
            if md:
                out.append(md)
            else:
                out.extend(lines[i : j + 1])
                if rec.get("error"):
                    out.append(f"<!-- asset download failed: {rec['error']} -->")
            img_idx += 1
            i = j + 1
            continue

        line = lines[i]
        if INLINE_ASSET_RE.search(line):
            def _replace_inline(match: re.Match[str]) -> str:
                nonlocal img_idx
                rec = img_map[img_idx]
                _download_image(rec, img_idx, out_dir, token, skip_download)
                md = _image_markdown(rec, img_idx)
                img_idx += 1
                return md or ""

            line = INLINE_ASSET_RE.sub(_replace_inline, line)
        out.append(line)
        i += 1

    return strip_image_metadata("\n".join(out)), list(img_map.values())


def safe_name(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip()[:80] or "lexiang_doc"


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help") else 1)

    entry_id = parse_entry_id(sys.argv[1])
    skip_images = "--skip-images" in sys.argv
    download_pdf = "--download-pdf" in sys.argv
    out_dir = None
    if "--out-dir" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--out-dir") + 1]

    auth, company_from = load_mcp_config()

    entry = mcp_call("entry_describe_entry", {"entry_id": entry_id}, auth, company_from)
    e = entry["data"]["entry"]
    title = e.get("name", entry_id)
    source_url = (
        sys.argv[1]
        if re.match(r"https?://", sys.argv[1])
        else f"https://lexiangla.com/pages/{entry_id}"
    )
    meta = {
        "entry_id": entry_id,
        "title": title,
        "source_url": source_url,
        "source_title": title,
        "source_type": "lexiang",
        "language": "unknown",
        "parent_id": e.get("parent_id"),
        "space_id": e.get("space_id"),
        "file_id": e.get("target_id"),
        "extension": e.get("extension"),
        "entry_type": e.get("entry_type"),
    }

    out_dir = out_dir or safe_name(title)
    os.makedirs(out_dir, exist_ok=True)

    parse = mcp_call(
        "entry_describe_ai_parse_content", {"entry_id": entry_id}, auth, company_from
    )
    raw = parse["data"]["content"]
    with open(os.path.join(out_dir, "parsed_raw.md"), "w", encoding="utf-8") as f:
        f.write(raw)

    source, imgs = fill_images(raw, out_dir, auth, skip_download=skip_images)
    with open(os.path.join(out_dir, "source.md"), "w", encoding="utf-8") as f:
        f.write(source)

    with open(os.path.join(out_dir, "images.json"), "w", encoding="utf-8") as f:
        json.dump(imgs, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    if download_pdf and meta.get("file_id"):
        dl = mcp_call(
            "file_download_file",
            {"file_id": meta["file_id"], "expire_seconds": 3600},
            auth,
            company_from,
        )
        pdf_path = os.path.join(out_dir, "paper.pdf")
        with urllib.request.urlopen(dl["data"]["url"], timeout=300) as r, open(
            pdf_path, "wb"
        ) as f:
            f.write(r.read())
        print(f"  PDF -> {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

    n_img = len(imgs)
    n_ok = sum(1 for x in imgs if x.get("downloaded"))
    n_md = source.count("![")
    print(f"Title       : {title}")
    print(f"Entry       : {entry_id}")
    print(f"Out dir     : {out_dir}")
    print(f"Parsed raw  : {len(raw)} chars -> parsed_raw.md")
    print(f"Source md   : {len(source)} chars -> source.md ({n_md} image refs)")
    print(f"Images      : {n_ok}/{n_img} downloaded -> {out_dir}/images/")
    if n_ok < n_img:
        failed = [x for x in imgs if not x.get("downloaded")]
        print(f"  Failed    : {len(failed)} (see images.json; try --download-pdf + pymupdf)")
    print("\n下一步：清洗/翻译 source.md；上传请调用 upload-markdown-to-lexiang 公共 CLI")


if __name__ == "__main__":
    main()
