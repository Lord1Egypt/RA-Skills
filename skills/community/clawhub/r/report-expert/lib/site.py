"""小站维护模块 — 索引管理、首页重建、页面更新、资源同步、CF 部署

职责边界：
- 管理 dist/ 目录下的所有文件和索引
- 同步静态资源（templates → dist）
- 重建首页和索引
- 用最新模板+html_lint 管线更新所有报告页面
- 将 dist/ 部署到 Cloudflare Pages
- 添加/删除页面索引

不做的事：
- 不提取/校验 HTML 内容（交给 report + html_lint 模块）
- 不验证线上结果（交给 verify 模块）
"""

import re, sys, shutil, json, subprocess
from pathlib import Path
from datetime import date

from lib.config import (
    BASE_DIR, DIST_DIR, SITE_URL, SITE_NAME,
    load_index, save_index, strip_emoji, CATEGORIES, INDEX_FILE
)
from lib.page import generate_page_html
from lib.remote_deploy import deploy_to_cf


# 索引备份路径（dist 被清理时的恢复源）
INDEX_BACKUP = BASE_DIR / "index.json"


def sync_from_cf():
    """从 Cloudflare Pages 线上站点同步缺失文件到 dist/

    确保本地 dist/ 与线上站点保持一致：
    - 从线上 index.json 获取所有页面列表
    - 对比 dist/ 中缺失的文件
    - 逐个拉取并写入 dist/ 对应目录

    Returns:
        synced: 同步的文件数量
        missing: 仍缺失的文件列表
    """
    if not SITE_URL:
        print("⚠️ SITE_URL 未配置，无法从线上同步")
        return 0, []

    # 1. 从线上拉取 index.json
    remote_data = _restore_index_from_remote()
    if not remote_data or not remote_data.get("pages"):
        print("⚠️ 线上 index.json 为空或无法拉取")
        return 0, []

    # 2. 拉取线上静态资源（CSS/JS）
    asset_urls = [
        (f"{SITE_URL}/styles/base.css", DIST_DIR / "styles" / "base.css"),
        (f"{SITE_URL}/scripts/main.js", DIST_DIR / "scripts" / "main.js"),
    ]
    for url, dst in asset_urls:
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            _download_file(url, dst)

    # 3. 逐个检查页面文件
    synced = 0
    missing = []
    for page in remote_data["pages"]:
        if page.get("external") and not page.get("url"):
            continue  # External pages without URL — can't sync

        cat = page.get("category", "")
        fn = page.get("filename", "")
        if not cat or not fn:
            continue

        local_path = DIST_DIR / cat / fn
        if local_path.exists():
            continue  # Already in dist

        # Download from online
        page_url = page.get("url", f"/{cat}/{fn}")
        if not page_url.startswith("http"):
            page_url = f"{SITE_URL}{page_url}"

        local_path.parent.mkdir(parents=True, exist_ok=True)
        ok = _download_file(page_url, local_path)
        if ok:
            synced += 1
            print(f"  📥 同步: {cat}/{fn}")
        else:
            missing.append(f"{cat}/{fn}")
            print(f"  ❌ 无法拉取: {cat}/{fn}")

    # 4. 同步线上 index.json 到本地（合并）
    local_data = load_index_safe()
    # Add pages from remote that don't exist in local
    local_filenames = {p.get("filename", "") for p in local_data["pages"]}
    for rp in remote_data["pages"]:
        if rp.get("filename") not in local_filenames:
            local_data["pages"].append(rp)

    save_index(local_data)
    _backup_index(local_data)

    if synced:
        print(f"✅ 从线上同步了 {synced} 个文件")
    if missing:
        print(f"⚠️ {len(missing)} 个文件无法从线上拉取: {', '.join(missing[:5])}")

    return synced, missing


def _download_file(url, dst_path, timeout=30):
    """从 URL 下载文件到本地路径

    Args:
        url: 下载 URL
        dst_path: 目标本地路径
        timeout: 超时秒数

    Returns:
        True: 成功下载
        False: 失败
    """
    # Try curl first (more robust for various protocols)
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), "-o", str(dst_path), url],
            capture_output=True, text=True, timeout=timeout + 5
        )
        if result.returncode == 0 and dst_path.exists() and dst_path.stat().st_size > 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Fallback: urllib
    try:
        from urllib.request import urlopen
        from urllib.error import URLError
        with urlopen(url, timeout=timeout) as resp:
            if resp.status == 200:
                data = resp.read()
                dst_path.write_bytes(data)
                return len(data) > 0
    except (URLError, OSError):
        pass

    # Clean up failed download
    if dst_path.exists():
        try:
            dst_path.unlink()
        except OSError:
            pass

    return False


def copy_assets():
    """同步静态资源到 dist/（templates → dist/styles/scripts）"""
    asset_map = {
        BASE_DIR / "templates" / "base.css": DIST_DIR / "styles" / "base.css",
        BASE_DIR / "scripts" / "main.js": DIST_DIR / "scripts" / "main.js",
    }
    updated = 0
    for src, dst in asset_map.items():
        if not src.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or dst.read_bytes() != src.read_bytes():
            shutil.copy2(src, dst)
            updated += 1
    return updated


def _backup_index(data):
    """将索引备份到技能根目录，作为 dist 被清理时的恢复源"""
    INDEX_BACKUP.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), "utf-8"
    )


def _restore_index_from_backup():
    """从备份恢复索引（dist 被清理时使用）"""
    if INDEX_BACKUP.exists():
        with open(INDEX_BACKUP, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _restore_index_from_remote():
    """从线上站点拉取 index.json 恢复索引（终极恢复）"""
    if not SITE_URL:
        return None
    # Try curl first, fall back to urllib
    try:
        result = subprocess.run(
            ["curl", "-sL", f"{SITE_URL}/index.json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass

    # Fallback: use urllib (always available in Python)
    try:
        from urllib.request import urlopen
        from urllib.error import URLError
        with urlopen(f"{SITE_URL}/index.json", timeout=15) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except (URLError, json.JSONDecodeError, OSError):
        pass

    return None


def load_index_safe():
    """安全加载索引：dist → 备份 → 线上，确保索引不丢失。

    优先级：
    1. dist/index.json（正常路径）
    2. 技能根目录 index.json（dist 被清理时的备份）
    3. 线上 {SITE_URL}/index.json（终极恢复）
    """
    # 1. 先尝试从 dist 加载
    data = load_index()
    if data.get("pages") or INDEX_FILE.exists():
        # dist/index.json exists (even if empty) — trust it
        if not data.get("pages") and INDEX_FILE.exists():
            print(f"⚠️ dist/index.json 存在但 pages 为空 — 如非预期，请检查备份或执行 rebuild_index")
        return data

    # 2. 从备份恢复
    backup = _restore_index_from_backup()
    if backup and backup.get("pages"):
        print(f"📦 从本地备份恢复索引（{len(backup['pages'])} 篇）")
        # 写回 dist
        DIST_DIR.mkdir(parents=True, exist_ok=True)
        save_index(backup)
        return backup

    # 3. 从线上恢复
    remote = _restore_index_from_remote()
    if remote and remote.get("pages"):
        print(f"🌐 从线上站点恢复索引（{len(remote['pages'])} 篇）")
        DIST_DIR.mkdir(parents=True, exist_ok=True)
        save_index(remote)
        _backup_index(remote)
        return remote

    # 全部为空，返回空索引
    return data


def add_to_index(filename, title, desc, category, url=None):
    """将外部页面添加到索引"""
    if category not in CATEGORIES:
        print(f"⚠️ 分类 '{category}' 不在预定义分类中，仍将添加（可用的: {', '.join(CATEGORIES.keys())}）")
    data = load_index_safe()

    # Check for duplicate filename — replace existing entry
    for i, p in enumerate(data["pages"]):
        if p.get("filename") == filename and p.get("category") == category:
            # Replace existing entry with updated info
            data["pages"][i] = {
                "filename": filename,
                "title": title,
                "desc": desc or "",
                "date": p.get("date", date.today().isoformat()),
                "category": category,
                "external": True,
            }
            if url:
                data["pages"][i]["url"] = url
            save_index(data)
            _backup_index(data)
            print(f"✅ 已更新索引条目: {title}")
            return

    today = date.today().isoformat()
    entry = {
        "filename": filename,
        "title": title,
        "desc": desc or "",
        "date": today,
        "category": category,
        "external": True,
    }
    if url:
        entry["url"] = url
    data["pages"].append(entry)
    save_index(data)
    _backup_index(data)
    print(f"✅ 已添加到索引: {title}")


def remove_from_index(filename):
    """从索引中删除指定页面，并删除 dist 中对应文件。

    Args:
        filename: 文件名（如 "2026-06-17-test-report.html"）
                 也可以是 "category/filename" 格式

    Returns:
        True: 成功删除
        False: 未找到该条目
    """
    data = load_index_safe()

    # 在索引中查找并删除
    target = None
    for i, p in enumerate(data["pages"]):
        # Exact filename match
        if p.get("filename") == filename:
            target = i
            break

    if target is None:
        # Try path format: category/filename
        for i, p in enumerate(data["pages"]):
            page_path = f"{p.get('category','')}/{p.get('filename','')}"
            if filename == page_path:
                target = i
                break

    if target is None:
        print(f"⚠️ 索引中未找到: {filename}")
        return False

    removed = data["pages"].pop(target)
    removed_title = removed.get("title", filename)
    removed_cat = removed.get("category", "")
    removed_file = removed.get("filename", "")

    # 删除 dist 中的实际文件
    if removed_cat and removed_file:
        file_path = DIST_DIR / removed_cat / removed_file
        if file_path.exists():
            file_path.unlink()
            print(f"🗑️  已删除文件: dist/{removed_cat}/{removed_file}")
            # Clean up empty category directory
            cat_dir = DIST_DIR / removed_cat
            if cat_dir.is_dir() and not any(cat_dir.iterdir()):
                cat_dir.rmdir()
                print(f"🗑️  已清理空目录: dist/{removed_cat}")

    save_index(data)
    _backup_index(data)
    print(f"✅ 已从索引删除: {removed_title}")
    return True


def rebuild_index():
    """重建索引 + 刷新首页

    Also scans dist/ for HTML files not in the index and adds them.
    This handles the case where index.json is lost/corrupted but dist files remain.
    """
    data = load_index_safe()
    copy_assets()

    # Scan dist/ for HTML files not in index (recovery scenario)
    existing_filenames = {p.get("filename", "") for p in data["pages"]}
    for html_file in sorted(DIST_DIR.rglob("*.html")):
        if html_file.name == "index.html":
            continue
        rel = html_file.relative_to(DIST_DIR)
        cat = str(rel.parent)
        if cat == '.':
            cat = 'other'
        filename = rel.name

        if filename not in existing_filenames:
            # Recover this file into the index
            html = html_file.read_text("utf-8")
            title_m = re.search(r'<title>(.*?)</title>', html)
            title = title_m.group(1).strip() if title_m else html_file.stem
            date_m = re.match(r'(\d{4}-\d{2}-\d{2})', html_file.stem)
            date_str = date_m.group(1) if date_m else date.today().isoformat()
            entry = {
                "filename": filename,
                "title": title,
                "desc": "",
                "date": date_str,
                "category": cat,
                "url": f"/{cat}/{filename}",
            }
            data["pages"].append(entry)
            existing_filenames.add(filename)
            print(f"  📎 恢复索引条目: {cat}/{filename}")

    # Remove index entries whose files don't exist in dist (and aren't external)
    missing_pages = []
    for p in data["pages"]:
        if p.get("external"):
            continue  # External pages don't have files in dist
        cat = p.get("category", "")
        fn = p.get("filename", "")
        if cat and fn:
            file_path = DIST_DIR / cat / fn
            if not file_path.exists():
                missing_pages.append(p)
    if missing_pages:
        print(f"  ⚠️ 发现 {len(missing_pages)} 个索引条目的文件不存在于 dist 中:")
        for p in missing_pages:
            print(f"     - {p.get('category','')}/{p.get('filename','')} ({p.get('title','')})")
        print(f"  这些条目将被移除。如需恢复，请重新 produce 或从线上站点拉取。")
        data["pages"] = [p for p in data["pages"] if p not in missing_pages]

    # Generate index page from template
    tpl = BASE_DIR / "templates" / "index.html"
    if tpl.exists():
        html = tpl.read_text("utf-8")
        html = html.replace("{{SITE_NAME}}", SITE_NAME)
        (DIST_DIR / "index.html").write_text(html, "utf-8")
    else:
        print("⚠️ templates/index.html 不存在，跳过首页生成")

    save_index(data)
    _backup_index(data)
    print(f"✅ 索引已刷新，共 {len(data['pages'])} 篇内容")


def update_pages():
    """用最新模板重新包裹所有报告页面

    使用 report 模块的 extract_body 进行内容提取，
    确保与 produce 使用的提取逻辑一致，避免 regex 不匹配。
    """
    from lib.report import extract_body

    dist = DIST_DIR
    if not dist.exists():
        print(f"❌ dist 目录不存在: {dist}")
        sys.exit(1)

    html_files = sorted(dist.rglob("*.html"))
    html_files = [f for f in html_files if f.name != "index.html"]

    if not html_files:
        print("⚠️ 未找到任何 HTML 页面")
        return

    print(f"🔄 更新 {len(html_files)} 个页面...")
    updated = 0
    skipped = 0

    for fpath in html_files:
        rel = fpath.relative_to(dist)
        category = str(rel.parent)
        if category == '.':
            category = 'other'
        html = fpath.read_text("utf-8")

        title_m = re.search(r'<title>(.*?)</title>', html)
        title = title_m.group(1).strip() if title_m else fpath.stem

        date_m = re.match(r'(\d{4}-\d{2}-\d{2})', fpath.stem)
        date_str = date_m.group(1) if date_m else date.today().isoformat()

        # Use extract_body from report module (same logic as produce)
        body, page_style = extract_body(html)

        # Body lint + fix pipeline (unified check + auto-fix)
        from lib.html_lint import lint_body
        body, body_failed = lint_body(body, label=str(rel), dist_dir=DIST_DIR)

        # Skip if content is empty (can't be auto-fixed)
        empty_result = [r for r in body_failed if r.rule.name == "body_not_empty"]
        if empty_result:
            print(f"  ⏭️  {rel} — 提取内容为空，跳过更新")
            skipped += 1
            continue

        desc = ""
        desc_m = re.search(r'<p class="report-header__desc">(.*?)</p>', html, re.DOTALL)
        if desc_m:
            desc_raw = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip()
            import html as html_module
            desc = html_module.unescape(desc_raw)

        page_info = {
            "title": title,
            "desc": desc,
            "date": date_str,
            "category": category,
            "body": body,
            "style": page_style,
        }
        page_html = generate_page_html(page_info, SITE_URL)

        # Page lint + fix pipeline
        from lib.html_lint import lint_page
        page_html, page_failed = lint_page(page_html, label=str(rel), dist_dir=DIST_DIR)
        for r in page_failed:
            print(f"  ⚠️ {rel} — Page lint: {r}")

        fpath.write_text(page_html, "utf-8")
        updated += 1
        print(f"  ✅ {rel} — {title}")

    if skipped:
        print(f"\n⚠️ {skipped} 个页面因内容校验失败被跳过（可能是旧格式或结构异常）")
    print(f"\n✅ 更新完成: {updated}/{len(html_files)} 个页面已重新生成")


def publish():
    """将 dist/ 部署到 Cloudflare Pages（小站维护的最终推送步骤）"""
    copy_assets()
    return deploy_to_cf()


def full_deploy(category, html_file, title=None, desc=None):
    """完整部署流程：生产 → 同步 → 部署 → 验证

    组合 report + site + verify 三个模块的能力。
    """
    from lib.config import check_config
    from lib.report import produce
    from lib.verify import verify_deployment

    check_config()

    # ── 1. 报告生产 ──
    filename, cat = produce(category, html_file, title, desc)

    # ── 2. 资源同步 + 索引备份 ──
    copy_assets()
    data = load_index_safe()
    _backup_index(data)

    # ── 3. 部署到 CF ──
    success = deploy_to_cf()
    if not success:
        return False

    # ── 4. 验证 ──
    verify_deployment(cat, filename)
    # Note: verify_deployment only outputs a verification plan.
    # The agent should use web_fetch to actually verify and act on results.
    print("📝 验证计划已输出，请用 web_fetch 逐项验证")
    return True