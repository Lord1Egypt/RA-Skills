#!/usr/bin/env python3
"""
Web Content → Markdown → Obsidian/Feishu/IMA

Convert any web URL or local file to Markdown, then:
1. Save to Obsidian Vault (configurable via OBSIDIAN_VAULT_PATH)
2. Save to Feishu Cloud Document (optional)
3. Save to Tencent IMA Note (optional)

Usage:
  python3 web_to_all.py --url <url_or_path>
  python3 web_to_all.py --url <url_or_path> --title "Custom Title"
  python3 web_to_all.py --url <url_or_path> --no-feishu --no-ima
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from web_to_md import convert as convert_to_md
from web_to_md import extract_original_url
from ima_client import IMAClient

# v3.6.0: feishu_client.FeishuClient 已废弃，不再 import
# 飞书存储改用 lark-cli drive +upload（用户身份上传 .md 原文件到云盘）


def get_obsidian_vault_path() -> Path:
    r"""
    Get Obsidian Vault path from environment variable or use default.
    
    Environment variable: OBSIDIAN_VAULT_PATH

    Defaults:
    - Windows: E:\Obsidian-Vault\00-Inbox
    - macOS/Linux: ~/Obsidian-Vault/00-Inbox
    """
    env_path = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_path:
        return Path(env_path).expanduser()

    # Default paths by OS
    if sys.platform.startswith("win"):
        return Path(r"E:\Obsidian-Vault\00-Inbox")
    else:
        return Path.home() / "Obsidian-Vault" / "00-Inbox"


OBSIDIAN_VAULT = get_obsidian_vault_path()


def _extract_source_name(url: str) -> str:
    """从 URL 提取来源标识用于文件命名（v3.2.0）"""
    if not url:
        return "local"
    lower = url.lower()
    if "waytoagi" in lower:
        return "waytoagi"
    if "feishu.cn" in lower or "larkoffice" in lower:
        return "feishu"
    if "x.com" in lower or "twitter.com" in lower:
        return "x"
    if "mp.weixin.qq.com" in lower:
        return "wechat"
    if "weibo.com" in lower:
        return "weibo"
    if "xiaohongshu.com" in lower or "xhslink.com" in lower:
        return "xiaohongshu"
    if "github.com" in lower:
        return "github"
    if "youtube.com" in lower or "youtu.be" in lower:
        return "youtube"
    from urllib.parse import urlparse
    try:
        netloc = urlparse(url).netloc
        parts = netloc.split(".")
        return parts[-2] if len(parts) >= 2 else netloc
    except Exception:
        return "webpage"


def save_to_obsidian(content: str, title: str, url: str = None, keywords: str = None) -> str:
    """Save Markdown to Obsidian Vault

    文件名规则（v3.5.0）：YYYYMMDD-标题-关键信息.md
    - 关键信息：2-4 个关键词，用顿号"、"分隔（如 "数字人、口播、heygen"）
    - 由调用方（AI）从标题和内容提取
    - 未提供 keywords 时 fallback 到来源（waytoagi/wechat/x/github）
    """
    vault_path = Path(OBSIDIAN_VAULT)
    vault_path.mkdir(parents=True, exist_ok=True)

    import re
    date_str = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 保留用于 fallback
    source = _extract_source_name(url)
    # Windows 禁止字符替换为下划线，中文标点（含：、）保留
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title).strip()
    safe_title = re.sub(r'_+', '_', safe_title).strip("_ ").strip()
    safe_title = safe_title.rstrip(".")
    # 限制标题长度，避免文件名过长
    if len(safe_title) > 60:
        safe_title = safe_title[:60].strip("_ ").strip()

    # v3.5.0: 关键信息优先，fallback 到来源
    if keywords and keywords.strip():
        # 清理关键词：去掉 Windows 禁止字符，保留顿号"、"和英文逗号
        safe_kw = re.sub(r'[\\/:*?"<>|]', '_', keywords).strip()
        safe_kw = safe_kw.strip("_ ").strip()
        # 长度限制：关键词部分 ≤ 40 字符
        if len(safe_kw) > 40:
            safe_kw = safe_kw[:40].strip("_ ").strip()
        suffix = safe_kw
    else:
        suffix = source
    filename = f"{date_str}-{safe_title}-{suffix}.md"
    filepath = vault_path / filename

    frontmatter = []
    frontmatter.append("---")
    frontmatter.append(f"title: {title}")
    frontmatter.append(f"date: {datetime.now().isoformat()}")
    if url:
        frontmatter.append(f"source: {url}")
        # 根据 URL 来源自动生成 tags
        lower_url = url.lower()
        if "x.com" in lower_url or "twitter.com" in lower_url:
            tags = "web-to-fim, x-twitter"
        elif "mp.weixin.qq.com" in lower_url:
            tags = "web-to-fim, wechat"
        elif "weibo.com" in lower_url:
            tags = "web-to-fim, weibo"
        elif "xiaohongshu.com" in lower_url or "xhslink.com" in lower_url:
            tags = "web-to-fim, xiaohongshu"
        elif "github.com" in lower_url:
            tags = "web-to-fim, github"
        elif "youtube.com" in lower_url or "youtu.be" in lower_url:
            tags = "web-to-fim, youtube"
        else:
            tags = "web-to-fim, webpage"
    else:
        tags = "web-to-fim, local-file"
    frontmatter.append(f"tags: [{tags}]")
    frontmatter.append("---")
    frontmatter_str = "\n".join(frontmatter)

    full_content = f"{frontmatter_str}\n\n{content}"

    for attempt in range(3):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_content)
            break
        except PermissionError:
            if attempt < 2:
                time.sleep(1)
            else:
                # Fallback: use ASCII-only filename
                ascii_filename = f"note_{timestamp}.md"
                ascii_filepath = vault_path / ascii_filename
                try:
                    with open(ascii_filepath, "w", encoding="utf-8") as f:
                        f.write(full_content)
                    filepath = ascii_filepath
                    break
                except PermissionError:
                    # Last resort: save to script directory
                    fallback_path = Path(__file__).parent.parent / "saved" / ascii_filename
                    fallback_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(fallback_path, "w", encoding="utf-8") as f:
                        f.write(full_content)
                    filepath = fallback_path
                    break

    print(f"✅ Obsidian: {filepath}")
    return str(filepath)


def save_to_feishu(md_file_path: str, title: str = None) -> dict:
    """Save to Feishu Cloud Drive via lark-cli (v3.6.0)

    上传 .md 原文件到用户飞书云盘根目录。
    用户在飞书"我的空间 > 云盘"立即可见。

    v3.6.0 变更：
    - 从 FeishuClient.create_document（tenant_access_token，应用身份，用户不可见）
      改为 lark-cli drive +upload（user_access_token，用户身份，立即可见）
    - 旧 feishu_client.py 标记为废弃

    Args:
        md_file_path: 本地 .md 文件路径（通常是 Obsidian 保存后的路径）
        title: 文档标题（用于云盘中的文件名，可选；未提供时用原文件名）

    Returns:
        dict: {"url": ..., "file_token": ..., "file_name": ...}

    Raises:
        FileNotFoundError: md_file_path 不存在
        RuntimeError: lark-cli 未安装/未登录/上传失败
    """
    import shutil
    import subprocess

    src = Path(md_file_path).resolve()
    if not src.exists():
        raise FileNotFoundError(f"MD file not found: {src}")

    # lark-cli --file 必须是 cwd 下的相对路径，复制到 scripts 目录
    scripts_dir = Path(__file__).parent
    if title:
        import re
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title).strip().rstrip(".")
        if len(safe_title) > 80:
            safe_title = safe_title[:80].strip()
        upload_name = f"{safe_title}.md"
    else:
        upload_name = src.name

    tmp_path = scripts_dir / upload_name
    shutil.copy2(src, tmp_path)

    try:
        lark_cli = shutil.which("lark-cli")
        if not lark_cli:
            raise RuntimeError("lark-cli not found in PATH. Install via npm i -g @larksuiteoapi/lark-cli and run lark-cli auth login.")

        result = subprocess.run(
            [lark_cli, "drive", "+upload", "--file", f"./{upload_name}", "--name", upload_name],
            capture_output=True,
            text=True,
            cwd=str(scripts_dir),
            timeout=60,
            encoding="utf-8",
        )
        if result.returncode != 0:
            raise RuntimeError(f"lark-cli exit {result.returncode}: {result.stderr.strip() or result.stdout.strip()}")

        # 输出包含一行 "Uploading: ..." 和多行 JSON，提取从第一个 { 到最后一个 } 的内容
        stdout = result.stdout
        start = stdout.find("{")
        end = stdout.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise RuntimeError(f"lark-cli output missing JSON: {stdout}")

        json_str = stdout[start:end + 1]
        data = json.loads(json_str)
        if not data.get("ok"):
            err = data.get("error", {}).get("message", "unknown")
            raise RuntimeError(f"lark-cli upload failed: {err}")

        file_data = data.get("data", {})
        url = file_data.get("url", "N/A")
        print(f"✅ Feishu (Drive): {url}")
        return {
            "url": url,
            "file_token": file_data.get("file_token", ""),
            "file_name": file_data.get("file_name", upload_name),
        }
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass


def save_to_ima(content: str, title: str, knowledge_base: str = None, source_url: str = None) -> dict:
    """Save to Tencent IMA knowledge base.

    Two strategies based on source_url:
    - Has URL (公众号/网页): use import_urls → IMA server-side fetch (preserves images/layout)
    - No URL (飞书转录/手动内容): use create_note + add_knowledge (plain text note)

    IMA has two separate API systems:
    - Notes API (/openapi/note/v1/): creates notes, manages notebooks
    - Knowledge Base API (/openapi/wiki/v1/): manages knowledge bases, adds content

    Args:
        content: Markdown content (used when source_url is None)
        title: Note title
        knowledge_base: Target knowledge base name. If None, reads from IMA_KB_NAME env var,
                        defaults to "FIM知识库".
        source_url: Original article URL. If it's a 公众号/网页 URL, use import_urls
                    for server-side fetch (preserves images). None for plain text note.
    """
    # 优先用传入参数，其次环境变量 IMA_KB_NAME，最后默认值
    if knowledge_base is None:
        knowledge_base = os.environ.get("IMA_KB_NAME", "FIM知识库")

    try:
        client = IMAClient()
        kb_id = client.find_knowledge_base_by_name(knowledge_base) if knowledge_base else None

        # Strategy 1: URL import (公众号/网页) — IMA server-side fetch, preserves images
        if source_url and _is_importable_url(source_url):
            results = client.import_urls(
                knowledge_base_id=kb_id,
                urls=[source_url],
            )
            if results and results[0].get("success"):
                print(f"✅ IMA (→ {knowledge_base}, URL导入): {source_url}")
                return {
                    "note_id": "",
                    "title": title,
                    "url": source_url,
                    "media_id": results[0].get("media_id", ""),
                    "method": "import_urls",
                }
            else:
                ret_code = results[0].get("ret_code", -1) if results else -1
                print(f"⚠️ IMA import_urls failed (ret_code={ret_code}), fallback to note", file=sys.stderr)

        # Strategy 2: Plain text note (飞书转录/手动内容/URL导入失败fallback)
        note_result = client.create_note(title=title, content=content)
        note_id = note_result.get("note_id", "")
        if not note_id:
            raise Exception("创建笔记失败：未返回 note_id")

        if kb_id:
            client.add_note_to_knowledge_base(
                note_id=note_id,
                title=title,
                knowledge_base_id=kb_id,
            )
            print(f"✅ IMA (→ {knowledge_base}): {note_result.get('url', 'N/A')}")
        else:
            print(f"✅ IMA: {note_result.get('url', 'N/A')}")

        return note_result
    except Exception as e:
        print(f"⚠️ IMA failed: {e}", file=sys.stderr)
        return None


def _is_importable_url(url: str) -> bool:
    """Check if URL is suitable for IMA import_urls (server-side fetch)（v3.3.0 精细化路由）.

    IMA import_urls 适用（返回 True）:
    - 微信公众号文章: mp.weixin.qq.com/s（IMA 自动识别，保留图片排版）
    - 普通网页: 除排除项外的 http(s):// URL

    IMA import_urls 不适用（返回 False）:
    - feishu wiki URLs: 需登录认证，IMA 服务端无法抓取
    - X/Twitter URLs: 必须逐字转录（web-to-fim 技能规则）
    - GitHub URLs: IMA 抓取 HTML 页面效果差，改为纯文本笔记（v3.3.0 新增）

    Rationale:
    - X/Twitter content must be 逐字转录 per SKILL.md rules.
    - GitHub HTML 页面不是 markdown 源码，IMA 抓取后内容混乱，改为纯文本笔记存转录 MD。
    """
    if not url:
        return False
    lower = url.lower()
    # 飞书 wiki 需要登录认证，IMA 服务端无法抓取
    if "feishu.cn" in lower or "larkoffice" in lower:
        return False
    # X/Twitter 必须逐字转录（web-to-fim 技能规则），不用 IMA 服务端抓取
    if "x.com" in lower or "twitter.com" in lower:
        return False
    # GitHub: IMA 抓取 HTML 页面效果差（非 markdown 源码），改为纯文本笔记（v3.3.0）
    if "github.com" in lower:
        return False
    # 公众号文章和普通网页都可以（IMA 自动识别）
    if lower.startswith("http://") or lower.startswith("https://"):
        return True
    return False


def _is_feishu_wiki(url: str) -> bool:
    """判断 URL 是否为飞书 wiki（v3.3.0 新增）"""
    if not url:
        return False
    lower = url.lower()
    return "feishu.cn/wiki" in lower or "larkoffice.com/wiki" in lower


def _fetch_feishu_wiki_via_webfetch(url: str) -> str:
    """通过 WebFetch 抓取飞书 wiki 内容（v3.3.0 新增）

    markitdown 无法处理飞书 wiki（需 JS 渲染 + 登录认证），
    需通过 WebFetch 工具抓取。本函数仅返回提示信息，实际抓取由 AI 调用 WebFetch 工具完成。

    在自动化流程中，AI 应该：
    1. 识别飞书 wiki URL
    2. 调用 WebFetch 抓取内容
    3. 用 extract_original_url() 检查原文链接
    4. 有可导入原文链接 → 抓取原文内容作为最终 MD
    5. 无原文链接 → 用飞书 wiki 内容
    """
    raise NotImplementedError(
        "飞书 wiki 需要通过 WebFetch 工具抓取，不能直接用 markitdown。"
        "请在 AI 流程中识别飞书 wiki URL 后调用 WebFetch。"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Web Content → Markdown → Obsidian/Feishu/IMA"
    )
    parser.add_argument("--url", help="URL or local file path to convert")
    parser.add_argument("--urls-file", help="File containing one URL per line (batch mode)")
    parser.add_argument("--title", help="Custom title for the document")
    parser.add_argument("--keywords", help="关键信息（2-4 个关键词用顿号分隔，如 '数字人、口播、heygen'），未指定时 fallback 到来源")
    parser.add_argument("--no-feishu", action="store_true", help="Skip Feishu")
    parser.add_argument("--no-ima", action="store_true", help="Skip IMA")
    parser.add_argument("--no-obsidian", action="store_true", help="Skip Obsidian")
    parser.add_argument("--dry-run", action="store_true", help="Only convert to Markdown, don't save anywhere")
    args = parser.parse_args()

    # Batch mode: read URLs from file
    if args.urls_file:
        with open(args.urls_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"📋 Batch mode: {len(urls)} URLs from {args.urls_file}\n")

        # 断点恢复：读取进度文件，跳过已完成的 URL
        progress_file = Path(args.urls_file).with_suffix(".progress.json")
        completed_urls = set()
        if progress_file.exists():
            with open(progress_file, "r", encoding="utf-8") as f:
                completed_urls = set(json.load(f))
            if completed_urls:
                print(f"♻️ Resuming: {len(completed_urls)} URLs already completed, skipping...\n")

        success, fail = 0, 0
        for i, url in enumerate(urls, 1):
            if url in completed_urls:
                print(f"--- [{i}/{len(urls)}] SKIP (already done) {url} ---")
                continue
            print(f"--- [{i}/{len(urls)}] {url} ---")
            try:
                _process_single(url, args)
                success += 1
                completed_urls.add(url)
                # 每条完成后立即写入进度（崩溃可恢复）
                with open(progress_file, "w", encoding="utf-8") as f:
                    json.dump(list(completed_urls), f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"❌ Failed: {e}", file=sys.stderr)
                fail += 1
        print(f"\n✅ Batch done: {success} success, {fail} failed")
        if fail == 0:
            # 全部成功，清理进度文件
            if progress_file.exists():
                progress_file.unlink()
        return 0 if fail == 0 else 1

    # Single mode
    if not args.url:
        parser.error("either --url or --urls-file is required")
    return _process_single(args.url, args)


def _process_single(url: str, args) -> int:
    """Process a single URL: convert → save to destinations."""
    print(f"🔍 Converting: {url}")
    try:
        markdown = convert_to_md(url)
    except Exception as e:
        print(f"❌ Conversion failed: {e}", file=sys.stderr)
        return 1

    # v3.4.0 全文完整性验证
    if len(markdown) < 500:
        print(f"⚠️ Warning: Content is short ({len(markdown)} chars), may be incomplete", file=sys.stderr)

    # v3.7.0 飞书 wiki 原文链接优先转录
    # v3.7.0: 飞书 wiki 内容已通过 lark-cli docs +fetch 完整获取（不再依赖 WebFetch）
    # 检测到原文链接时，尝试用 markitdown 或 x-tweet-fetcher 抓取原文，更长则覆盖
    original_url = None
    if _is_feishu_wiki(url):
        original_url = extract_original_url(markdown)
        if original_url:
            print(f"🔗 Found original URL: {original_url}")
            lower_orig = original_url.lower()
            # X / Twitter 原文：x-tweet-fetcher（convert_to_md 内部调用）
            if "x.com" in lower_orig or "twitter.com" in lower_orig:
                try:
                    orig_markdown = convert_to_md(original_url)
                    if len(orig_markdown) > len(markdown):
                        print(f"✅ X original fetched: {len(orig_markdown)} chars (was {len(markdown)})")
                        markdown = orig_markdown
                    else:
                        print(f"⚠️ X original shorter than feishu wiki, keeping feishu content")
                except Exception as e:
                    print(f"⚠️ X original fetch failed: {e}, using feishu wiki content (fallback)")
            # 公众号/普通网页原文：用 markitdown 转换（v3.7.0 改为自动抓取）
            elif "mp.weixin.qq.com" in lower_orig or lower_orig.startswith("http"):
                try:
                    orig_markdown = convert_to_md(original_url)
                    if len(orig_markdown) > len(markdown):
                        print(f"✅ Web original fetched: {len(orig_markdown)} chars (was {len(markdown)})")
                        markdown = orig_markdown
                    else:
                        print(f"⚠️ Web original shorter than feishu wiki, keeping feishu content")
                except Exception as e:
                    print(f"⚠️ Web original fetch failed: {e}, using feishu wiki content (fallback)")

    title = args.title
    if not title:
        lines = markdown.strip().split("\n")
        first_line = lines[0] if lines else ""
        if first_line.startswith("# "):
            title = first_line[2:].strip()
        elif first_line.startswith("title:"):
            title = first_line.split("title:", 1)[1].strip()
        else:
            # 尝试从 frontmatter 提取 title
            for line in lines[:10]:
                if line.strip().startswith("title:"):
                    title = line.split("title:", 1)[1].strip()
                    break
            else:
                # 从 URL 生成标题
                if url.startswith("http"):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    domain = parsed.netloc.replace("www.", "")
                    title = f"{domain} - {datetime.now().strftime('%Y-%m-%d')}"
                else:
                    title = f"Untitled - {datetime.now().strftime('%Y-%m-%d')}"

    print(f"\n📄 Title: {title}")
    print(f"📝 Markdown length: {len(markdown)} chars\n")

    if args.dry_run:
        print("🔇 Dry run — not saving anywhere")
        print(f"\n--- Markdown preview (first 500 chars) ---\n{markdown[:500]}")
        return 0

    results = {}

    if not args.no_obsidian:
        try:
            results["obsidian"] = save_to_obsidian(markdown, title, url, keywords=args.keywords)
        except Exception as e:
            print(f"⚠️ Obsidian failed: {e}", file=sys.stderr)

    # v3.6.0: 飞书改为上传 .md 文件到云盘，复用 Obsidian 保存的文件路径
    # 若 Obsidian 失败，则跳过飞书（需要源文件）
    if not args.no_feishu and results.get("obsidian"):
        try:
            results["feishu"] = save_to_feishu(results["obsidian"], title)
        except Exception as e:
            print(f"⚠️ Feishu failed: {e}", file=sys.stderr)
    elif not args.no_feishu and not results.get("obsidian"):
        print(f"⚠️ Feishu skipped: Obsidian file not available (required as upload source)", file=sys.stderr)

    if not args.no_ima:
        try:
            results["ima"] = save_to_ima(markdown, title, source_url=url)
        except Exception as e:
            print(f"⚠️ IMA failed: {e}", file=sys.stderr)

    print(f"\n✅ Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
