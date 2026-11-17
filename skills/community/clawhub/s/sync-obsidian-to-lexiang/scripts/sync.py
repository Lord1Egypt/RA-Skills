#!/usr/bin/env python3
"""
sync.py - Obsidian → 乐享知识库 同步执行器

设计原则：
  Markdown 页面统一调用 upload-markdown-to-lexiang；目录和独立附件沿用连接器。
  LLM 只负责：1) 唤起 skill 2) 明确输入参数。脚本拿到参数后自主执行全部工作。

使用方式:
  python3 sync.py --mode full \
      --target-space-id <SPACE_ID> [--target-folder-id <FOLDER_ID>] \
      [--vault-path <PATH>] [--source-dirs A B] \
      [--conflict-strategy lexiang_wins|obsidian_wins] [--dry-run]

  python3 sync.py --mode incremental --target-space-id <SPACE_ID> ...

  # 大批量同步：后台运行，立即返回，进度写 progress.json（Agent 轮询，不阻塞）
  python3 sync.py --mode incremental --target-space-id <ID> --background

  # 查询后台同步进度
  python3 sync.py --status [--vault-path <PATH>]

  python3 sync.py --init --target-space-id <SPACE_ID> [--target-folder-id <ID>]

输出：仅向 stdout 打印一行 JSON 摘要 + 报告路径。文档内容不输出。

Markdown 鉴权：使用 https://lexiangla.com/ai/claw 获取的个人凭证。
"""

import argparse
import fnmatch
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manifest import (
    load_config, save_config, load_manifest, save_manifest, new_manifest,
    compute_content_hash, get_file_mtime, now_iso, set_entry, remove_entry,
    DEFAULT_CONFIG, sync_lock, SyncLockError,
)
from converter import (
    get_obsidian_attachment_folder,
    split_into_segments, convert_wikilinks,
)
from lexiang_api import (
    LexiangConnector,
    LexiangError,
    resolve_personal_credential_selector,
)
from report import SyncReport
from progress import ProgressWriter, read_progress, get_progress_path


def log(msg):
    """进度输出到 stderr，不污染 stdout 的 JSON 摘要"""
    print(msg, file=sys.stderr, flush=True)


# ── vault 扫描 ────────────────────────────────────────────────

def detect_vault_path():
    """从 Obsidian 配置自动检测 vault 路径"""
    cfg = os.path.expanduser("~/Library/Application Support/obsidian/obsidian.json")
    if not os.path.exists(cfg):
        return None
    try:
        with open(cfg, "r", encoding="utf-8") as f:
            data = json.load(f)
        vaults = data.get("vaults", {})
        for _, info in vaults.items():
            if info.get("open"):
                return info.get("path")
        for _, info in vaults.items():
            return info.get("path")
    except (json.JSONDecodeError, IOError):
        pass
    return None


def should_exclude(rel_path, exclude_patterns):
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        # 对于 "dir/**" 模式，也排除目录本身
        if pattern.endswith("/**") and fnmatch.fnmatch(rel_path, pattern[:-3]):
            return True
        parts = rel_path.split(os.sep)
        for i in range(len(parts)):
            partial = os.sep.join(parts[: i + 1])
            if fnmatch.fnmatch(partial, pattern):
                return True
            # "dir/**" 也匹配 dir 本身
            if pattern.endswith("/**") and fnmatch.fnmatch(partial, pattern[:-3]):
                return True
    return rel_path.startswith(".obsidian")


# 不作为独立文件上传的扩展名（Obsidian 内部/系统文件）
SKIP_EXTENSIONS = {".canvas", ".ds_store"}
# 不作为独立文件同步的文件名（系统隐藏文件）
SKIP_FILENAMES = {".DS_Store", "Thumbs.db", ".gitignore"}


def scan_vault(vault_path, source_dirs, exclude_patterns):
    """
    递归扫描 vault，返回：
      {
        "folders": [rel_path, ...],
        "files":   [{rel_path, abs_path, mtime, hash, kind}],  # kind=page(.md) / file(其他)
      }
    .md → page（解析正文）；其他文件（PDF/Office/图片等）→ file（作为文件型 entry 上传）。
    """
    folders, files = [], []
    for root, dirs, filenames in os.walk(vault_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        rel_root = os.path.relpath(root, vault_path)
        if rel_root == ".":
            rel_root = ""
        if source_dirs:
            if rel_root == "":
                dirs[:] = [d for d in dirs if any(
                    d == sd or sd.startswith(d + os.sep) for sd in source_dirs
                )]
                continue
            if not any(rel_root == sd or rel_root.startswith(sd + os.sep) for sd in source_dirs):
                continue
        if rel_root and not should_exclude(rel_root, exclude_patterns):
            folders.append(rel_root)
        for fname in sorted(filenames):
            # 跳过系统/隐藏文件
            if fname in SKIP_FILENAMES or fname.startswith("."):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext in SKIP_EXTENSIONS:
                continue
            rel_path = os.path.join(rel_root, fname) if rel_root else fname
            if should_exclude(rel_path, exclude_patterns):
                continue
            abs_path = os.path.join(root, fname)
            kind = "page" if ext == ".md" else "file"
            files.append({
                "rel_path": rel_path,
                "abs_path": abs_path,
                "mtime": get_file_mtime(abs_path),
                "hash": compute_content_hash(abs_path),
                "kind": kind,
            })
    folders.sort(key=lambda x: x.count(os.sep))
    files.sort(key=lambda x: x["rel_path"])
    return {"folders": folders, "files": files}


# ── 同步执行 ──────────────────────────────────────────────────

def resolve_parent_id(rel_parent, folder_id_map, target_folder_id):
    """根据相对父路径查映射到的乐享 entry_id"""
    if not rel_parent:
        return target_folder_id or None
    return folder_id_map.get(rel_parent)


def upload_attachments_for(attachments, api, sync_attachments, parent_id, report, dry_run):
    """上传文档引用的附件，返回 {file_name: lexiang_url}"""
    att_map = {}
    if not sync_attachments:
        return att_map
    for att in attachments:
        if dry_run:
            report.record_action("upload_attachment", att.rel_path, "success", "", "dry-run")
            continue
        try:
            url = api.upload_attachment(att.abs_path, parent_id)
            if url:
                att_map[att.file_name] = url
            report.record_action("upload_attachment", att.rel_path, "success", "", "")
        except LexiangError as e:
            # 附件上传失败不阻断文档同步，保留原始引用
            report.record_action("upload_attachment", att.rel_path, "error", "", str(e)[:120])
    return att_map


def do_sync(vault_path, config, mode, source_dirs, dry_run, persist=None, progress=None):
    """
    执行同步主流程，返回 (report, manifest)。

    persist: 可选回调 persist(manifest)，用于增量落盘 manifest（中断安全）。
             每完成一个写操作就调用一次，保证中断后重跑不重不漏。
    progress: 可选 ProgressWriter，实时写 progress.json，供 Agent 后台轮询进度。
    """
    space_id = config["target_space_id"]
    target_folder_id = config.get("target_folder_entry_id", "")
    conflict_strategy = config.get("conflict_strategy", "lexiang_wins")
    sync_attachments = config.get("sync_attachments", True)
    respect_move = config.get("respect_move", True)
    exclude = config.get("exclude_patterns", DEFAULT_CONFIG["exclude_patterns"])
    attachment_folder = get_obsidian_attachment_folder(vault_path)
    credential_selector = resolve_personal_credential_selector(
        config.get("lexiang_profile") or None,
        config.get("lexiang_credential_file") or None,
    )

    report = SyncReport(
        mode=mode, vault_path=vault_path, target_space_id=space_id,
        target_folder_id=target_folder_id, conflict_strategy=conflict_strategy,
        dry_run=dry_run,
    )
    # 失败时同步写入 progress.json，便于 Agent 后台查看具体失败文档
    if progress:
        report.on_error = lambda rel_path, detail: progress.record_error(rel_path, detail)

    api = None
    if not dry_run:
        api = LexiangConnector(
            personal_credential_file=(
                credential_selector.path if credential_selector else None
            )
        )

    # target_folder_id 为空时，自动获取知识库根目录的 root_entry_id
    if not dry_run and not target_folder_id:
        try:
            root_id = api.resolve_root_entry_id(space_id)
            if root_id:
                target_folder_id = root_id
                config["target_folder_entry_id"] = target_folder_id
                log(f"  [配置] 未指定 --target-folder-id，自动获取知识库根目录: {root_id}")
            else:
                log(f"  [警告] 无法获取知识库根目录 ID，部分操作可能失败")
        except LexiangError as e:
            log(f"  [警告] 获取知识库根目录失败: {e}")

    # 关键：即便是 full 模式，也加载已有 manifest 作为「断点续传」基础，
    # 这样中途中断后重跑（无论 full/incremental）都能跳过已完成项。
    manifest = load_manifest(vault_path)
    manifest["space_id"] = space_id
    manifest["target_folder_entry_id"] = target_folder_id
    entries = manifest.setdefault("entries", {})

    # entry 探活缓存：{entry_id: probe_result}，避免对同一 entry 重复 describe
    probe_cache = {}

    def probe(entry_id):
        if dry_run or not entry_id:
            return {"exists": True, "parent_id": "", "edited_at": 0}
        if entry_id not in probe_cache:
            probe_cache[entry_id] = api.probe_entry(entry_id)
        return probe_cache[entry_id]

    # 乐享侧目录子项缓存：{parent_id: {(name, entry_type): entry_dict}}
    # 用于「manifest 丢失映射」时防重复创建——先查目标目录是否已有同名 entry，命中则复用。
    lexiang_children_cache = {}

    def find_lexiang_entry(parent_id, match_name, entry_type):
        """在乐享目标父目录下查找同名同类型 entry，返回 entry dict 或 None。
        按 parent_id 缓存，同一目录只 list 一次。dry_run 下不查（无网络）。"""
        if dry_run or not parent_id or not match_name:
            return None
        if parent_id not in lexiang_children_cache:
            try:
                children = api.list_children(parent_id, limit=200)
                cache = {}
                for ch in children:
                    cache[(ch.get("name", ""), ch.get("entry_type", ""))] = ch
                lexiang_children_cache[parent_id] = cache
            except LexiangError as e:
                log(f"  [查重] 列目录失败，跳过查重: {e}")
                lexiang_children_cache[parent_id] = {}
        return lexiang_children_cache[parent_id].get((match_name, entry_type))

    def save():
        if persist and not dry_run:
            persist(manifest)

    scan = scan_vault(vault_path, source_dirs, exclude)
    log(f"扫描完成：{len(scan['folders'])} 个目录，{len(scan['files'])} 篇文档")
    if progress:
        progress.set_total(len(scan["files"]))
        progress.note(message=f"开始同步：{len(scan['folders'])} 个目录，{len(scan['files'])} 篇文档")

    folder_id_map = {
        path: info["entry_id"]
        for path, info in entries.items() if info.get("type") == "folder"
    }

    # ── 1. 处理目录 ──
    for folder_path in scan["folders"]:
        existing = entries.get(folder_path)
        if existing and existing.get("type") == "folder":
            eid = existing["entry_id"]
            info = probe(eid)
            if info["exists"]:
                # 存在 → 复用（移动检测：被移走且不尊重移动则重建）
                moved = (not dry_run and target_folder_id and info["parent_id"]
                         and not _is_under_target(folder_path, info["parent_id"],
                                                  folder_id_map, target_folder_id))
                if moved and not respect_move:
                    log(f"  [目录] {folder_path} 被移动，按策略重建")
                else:
                    folder_id_map[folder_path] = eid
                    continue
            else:
                # entry 已被删除 → 清掉旧映射，下面重建
                log(f"  [目录] {folder_path} 原 entry 已失效，重建")
                remove_entry(manifest, folder_path)

        parent_id = resolve_parent_id(
            os.path.dirname(folder_path), folder_id_map, target_folder_id
        )
        name = os.path.basename(folder_path)
        if dry_run:
            report.record_action("create_folder", folder_path, "success", "", "dry-run")
            folder_id_map[folder_path] = f"DRYRUN_{folder_path}"
            continue
        try:
            fid = api.create_folder(space_id, name, parent_id)
            folder_id_map[folder_path] = fid
            set_entry(manifest, folder_path, "folder", fid)
            save()  # 每建一个目录立即落盘
            report.record_action("create_folder", folder_path, "success", fid, "")
            log(f"  [目录] {folder_path} ✓")
        except LexiangError as e:
            report.record_action("create_folder", folder_path, "error", "", str(e)[:120])
            log(f"  [目录] {folder_path} ✗ {e}")

    # ── 2. 处理文档与文件 ──
    # .md → page（解析正文）；其他类型（PDF/Office/图片等）→ file（文件型 entry 上传）
    for _idx, fi in enumerate(scan["files"]):
        rel_path = fi["rel_path"]
        kind = fi.get("kind", "page")          # page / file
        if progress:
            # done=_idx 表示「前 _idx 篇已处理完，现在开始第 _idx+1 篇」
            progress.state["done"] = _idx
            progress.note(current=rel_path, stats=report.stats,
                          message=f"处理中 {_idx + 1}/{len(scan['files'])}：{rel_path}")
        manifest_type = "page" if kind == "page" else "file"
        existing = entries.get(rel_path)
        parent_id = resolve_parent_id(
            os.path.dirname(rel_path), folder_id_map, target_folder_id
        )
        name = os.path.splitext(os.path.basename(rel_path))[0]

        # 新增（manifest 无记录，或类型不匹配）
        if not existing or existing.get("type") != manifest_type:
            # ⚠️ 防重复创建：manifest 丢失映射时（如断连重建失败冲映射），
            # 先查乐享目标目录是否已有同名 entry，命中则复用走更新，避免创建重复文档。
            match_name = name if manifest_type == "page" else os.path.basename(rel_path)
            found = find_lexiang_entry(parent_id, match_name, manifest_type)
            if found and found.get("id"):
                found_id = found["id"]
                log(f"  [{kind}] {rel_path} manifest 无映射，乐享已有同名 entry，复用 {found_id[:12]}…")
                set_entry(manifest, rel_path, manifest_type, found_id, "", fi.get("mtime", 0))
                save()  # 立即落盘，即使后续更新失败也不再重复创建
                existing = entries.get(rel_path)
                # 不 continue，继续走下面的 probe → 更新/跳过逻辑
            else:
                _sync_new(api, space_id, parent_id, name, rel_path, fi, vault_path,
                          attachment_folder, sync_attachments, report, manifest,
                          dry_run, save, credential_selector)
                continue

        entry_id = existing["entry_id"]
        try:
            info = probe(entry_id)
        except LexiangError as e:
            # 探活失败（如代理模式返回异常）→ 跳过，不 remove_entry，保留映射待下次重试。
            # 避免因 probe 抛异常而中断整个同步或冲掉映射导致后续重复创建。
            report.record_action("update_page", rel_path, "error", entry_id,
                                 f"探活失败: {e}")
            log(f"  [{kind}] {rel_path} ⚠ 探活失败，跳过（保留映射）: {e}")
            continue

        # entry 已被删除 → 当作新增重建
        if not info["exists"]:
            log(f"  [{kind}] {rel_path} 原 entry 已失效，重建")
            remove_entry(manifest, rel_path)
            _sync_new(api, space_id, parent_id, name, rel_path, fi, vault_path,
                      attachment_folder, sync_attachments, report, manifest,
                      dry_run, save, credential_selector)
            continue

        # 移动检测
        moved = (not dry_run and target_folder_id and info["parent_id"]
                 and parent_id and info["parent_id"] != parent_id)
        if moved and not respect_move:
            log(f"  [{kind}] {rel_path} 被移动，按策略在目标目录重建")
            remove_entry(manifest, rel_path)
            _sync_new(api, space_id, parent_id, name, rel_path, fi, vault_path,
                      attachment_folder, sync_attachments, report, manifest,
                      dry_run, save, credential_selector)
            continue

        # 内容未变 → 跳过
        if existing.get("content_hash") == fi["hash"]:
            report.record_action("update_page", rel_path, "skipped_no_change",
                                 entry_id, "无变化")
            continue

        # ── 内容有变 ──
        if kind == "file":
            # 文件型 entry 无法原地覆盖内容：删旧映射，重新上传一份新文件
            log(f"  [file] {rel_path} 内容变化，重新上传")
            remove_entry(manifest, rel_path)
            _sync_new(api, space_id, parent_id, name, rel_path, fi, vault_path,
                      attachment_folder, sync_attachments, report, manifest,
                      dry_run, save, credential_selector)
            continue

        # page 内容有变 → 冲突策略
        if conflict_strategy == "lexiang_wins" and not dry_run:
            last_sync_ts = _iso_to_ts(existing.get("last_sync_at", ""))
            lx_ts = info["edited_at"]
            if lx_ts and last_sync_ts and lx_ts > last_sync_ts + 5:
                report.record_action("update_page", rel_path, "skipped_conflict",
                                     entry_id, "乐享侧有独立更新，按策略跳过")
                log(f"  [page] {rel_path} ⚠ 乐享侧有更新，跳过")
                continue

        _update_page(api, entry_id, rel_path, fi, vault_path, attachment_folder,
                     sync_attachments, parent_id, space_id, report, manifest,
                     dry_run, save, credential_selector)

    if progress:
        progress.state["done"] = len(scan["files"])
        progress.note(current="", stats=report.stats, message="文档处理完成，正在收尾")

    # ── 3. 统计源端删除（manifest 有，本地无）──
    scanned_folders = set(scan["folders"])
    scanned_files = {f["rel_path"] for f in scan["files"]}
    deleted = 0
    for path, info in list(entries.items()):
        # 仅统计在本次同步范围内（source_dirs）的删除
        if source_dirs and not any(
            path == sd or path.startswith(sd + os.sep) for sd in source_dirs
        ):
            continue
        if info.get("type") == "folder" and path not in scanned_folders:
            deleted += 1
        elif info.get("type") in ("page", "file") and path not in scanned_files:
            deleted += 1
    report.set_source_deleted_ignored(deleted)

    # ── 4. 更新时间戳 ──
    if mode == "full":
        manifest["last_full_sync_at"] = now_iso()
    else:
        manifest["last_incremental_sync_at"] = now_iso()
    save()

    return report, manifest


def _is_under_target(folder_path, actual_parent_id, folder_id_map, target_folder_id):
    """判断 folder 的实际 parent 是否仍是其在目标树中预期的 parent"""
    expected = resolve_parent_id(
        os.path.dirname(folder_path), folder_id_map, target_folder_id
    )
    return actual_parent_id == expected


def _sync_new(api, space_id, parent_id, name, rel_path, fi, vault_path,
              attachment_folder, sync_attachments, report, manifest, dry_run, save,
              credential_selector=None):
    """根据 kind 分派：.md → 创建 page；其他 → 上传文件型 entry"""
    if fi.get("kind") == "file":
        _create_file(api, parent_id, rel_path, fi, space_id, report, manifest,
                     dry_run, save)
    else:
        _create_page(api, space_id, parent_id, name, rel_path, fi, vault_path,
                     attachment_folder, sync_attachments, report, manifest,
                     dry_run, save, credential_selector)


def _create_file(api, parent_id, rel_path, fi, space_id, report, manifest, dry_run, save):
    """上传独立文件（PDF/Office/图片等）为乐享文件型 entry"""
    if dry_run:
        report.record_action("create_file", rel_path, "success", "", "dry-run")
        return
    try:
        entry_id = api.upload_file_entry(fi["abs_path"], parent_id or space_id)
        set_entry(manifest, rel_path, "file", entry_id, fi["hash"], fi["mtime"])
        save()
        report.record_action("create_file", rel_path, "success", entry_id, "")
        log(f"  [文件] {rel_path} ✓")
    except LexiangError as e:
        report.record_action("create_file", rel_path, "error", "", str(e)[:120])
        log(f"  [文件] {rel_path} ✗ {e}")


def _read_text(abs_path):
    """读取 markdown 原文（容错编码）"""
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()


def _find_markdown_uploader():
    """Locate the shared uploader without assuming an Agent-specific home."""
    override = os.environ.get("LEXIANG_UPLOADER_HOME", "").strip()
    roots = [Path(override).expanduser()] if override else []
    skill_root = Path(__file__).resolve().parents[1]
    roots.append(skill_root.parent / "upload-markdown-to-lexiang")
    for root in roots:
        script = root / "scripts" / "lexiang_upload.py"
        if script.is_file():
            return script
    raise LexiangError(
        "未找到 upload-markdown-to-lexiang。请安装到当前 skills 根目录，"
        "或设置 LEXIANG_UPLOADER_HOME。"
    )


def _prepare_markdown_package(
        source_path, vault_path, attachment_folder, package_dir, include_images=True):
    """Convert Obsidian syntax and stage local images beside a temporary Markdown."""
    source = _read_text(source_path)
    segments = split_into_segments(source, source_path, vault_path, attachment_folder)
    image_dir = Path(package_dir) / "images"
    output = []
    image_count = 0
    for segment in segments:
        if segment.kind == "text":
            output.append(convert_wikilinks(segment.text))
            continue
        if not include_images:
            output.append(f"[本地图片未同步：{segment.image_alt}]")
            continue
        image_count += 1
        source_image = Path(segment.image_abs_path)
        safe_name = f"{image_count:04d}_{source_image.name}"
        image_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image, image_dir / safe_name)
        output.append(f"![{segment.image_alt}](images/{safe_name})")
    staged = Path(package_dir) / Path(source_path).name
    staged.write_text("\n\n".join(output), encoding="utf-8")
    return staged, image_count


def _build_markdown_uploader_command(
        uploader, staged, *, parent_id=None, entry_id=None, name=None,
        credential_selector=None):
    """构造公共 uploader 命令；返回值不含任何凭证内容。"""
    command = [sys.executable, str(uploader), "upload", str(staged), "--json"]
    if entry_id:
        command += ["--entry-id", entry_id]
    else:
        command += ["--parent-id", parent_id, "--name", name]
    if credential_selector:
        if credential_selector.profile:
            command += ["--profile", credential_selector.profile]
        else:
            command += ["--credential-file", str(credential_selector.path)]
    return command


def _run_markdown_uploader(source_path, vault_path, attachment_folder, *,
                           parent_id=None, entry_id=None, name=None, include_images=True,
                           credential_selector=None):
    uploader = _find_markdown_uploader()
    with tempfile.TemporaryDirectory(prefix="obsidian-lexiang-") as package_dir:
        staged, image_count = _prepare_markdown_package(
            source_path,
            vault_path,
            attachment_folder,
            package_dir,
            include_images=include_images,
        )
        command = _build_markdown_uploader_command(
            uploader,
            staged,
            parent_id=parent_id,
            entry_id=entry_id,
            name=name,
            credential_selector=credential_selector,
        )
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0:
            raise LexiangError(process.stderr.strip() or "公共 Markdown 上传器执行失败")
        try:
            result = json.loads(process.stdout)
        except json.JSONDecodeError as error:
            raise LexiangError(f"公共上传器返回非 JSON：{process.stdout[:200]}") from error
        if not result.get("verified"):
            raise LexiangError("公共上传器未通过线上对账")
        result["staged_images"] = image_count
        return result


def _create_page(api, space_id, parent_id, name, rel_path, fi, vault_path,
                 attachment_folder, sync_attachments, report, manifest, dry_run, save,
                 credential_selector=None):
    if dry_run:
        report.record_action("create_page", rel_path, "success", "", "dry-run")
        return
    try:
        result = _run_markdown_uploader(
            fi["abs_path"],
            vault_path,
            attachment_folder,
            parent_id=parent_id,
            name=name,
            include_images=sync_attachments,
            credential_selector=credential_selector,
        )
        entry_id = result["entry_id"]
        set_entry(manifest, rel_path, "page", entry_id, fi["hash"], fi["mtime"])
        save()
        image_count = result.get("local_images", 0)
        note = f"公共上传器 verified=true，图片 {image_count}"
        report.record_action("create_page", rel_path, "success", entry_id, note)
        log(f"  [文档] {rel_path} ✓ (图片 {image_count})")
    except LexiangError as e:
        report.record_action("create_page", rel_path, "error", "", str(e)[:120])
        log(f"  [文档] {rel_path} ✗ {e}")


def _update_page(api, entry_id, rel_path, fi, vault_path, attachment_folder,
                 sync_attachments, parent_id, space_id, report, manifest, dry_run, save,
                 credential_selector=None):
    if dry_run:
        report.record_action("update_page", rel_path, "success", entry_id, "dry-run 覆盖")
        return
    try:
        result = _run_markdown_uploader(
            fi["abs_path"],
            vault_path,
            attachment_folder,
            entry_id=entry_id,
            include_images=sync_attachments,
            credential_selector=credential_selector,
        )
        set_entry(manifest, rel_path, "page", entry_id, fi["hash"], fi["mtime"])
        save()
        image_count = result.get("local_images", 0)
        report.record_action(
            "update_page",
            rel_path,
            "success",
            entry_id,
            f"公共上传器 verified=true，图片 {image_count}",
        )
        log(f"  [文档] {rel_path} ↻ 已更新 (图片 {image_count})")
    except LexiangError as e:
        report.record_action("update_page", rel_path, "error", entry_id, str(e)[:120])
        log(f"  [文档] {rel_path} ✗ {e}")


# ── 冲突检测辅助 ──────────────────────────────────────────────

def _iso_to_ts(iso_str):
    """ISO 8601 → unix 秒，失败返回 0"""
    if not iso_str:
        return 0
    try:
        import datetime as dt
        d = dt.datetime.fromisoformat(iso_str)
        return int(d.timestamp())
    except (ValueError, TypeError):
        return 0


# ── 主入口 ────────────────────────────────────────────────────


def build_argument_parser():
    p = argparse.ArgumentParser(description="Obsidian → 乐享知识库 同步执行器")
    p.add_argument("--mode", choices=["full", "incremental"], help="同步模式")
    p.add_argument("--vault-path", help="Obsidian vault 路径（默认自动检测）")
    p.add_argument("--source-dirs", nargs="*", default=[], help="要同步的目录（空=全部）")
    p.add_argument("--target-space-id", help="目标乐享知识库 space_id")
    p.add_argument("--target-folder-id", default="", help="目标目录 entry_id")
    credential_group = p.add_mutually_exclusive_group()
    credential_group.add_argument(
        "--lexiang-profile",
        metavar="NAME",
        help="使用命名乐享个人凭证；default 对应旧 credentials.json",
    )
    credential_group.add_argument(
        "--lexiang-credential-file",
        metavar="PATH",
        help="使用指定的乐享个人凭证 JSON 文件",
    )
    p.add_argument("--conflict-strategy", choices=["lexiang_wins", "obsidian_wins"], default=None)
    p.add_argument("--respect-move", dest="respect_move", action="store_true", default=None,
                   help="尊重目的端移动：被移走的条目仍更新原 entry，不在目标目录重建（默认）")
    p.add_argument("--no-respect-move", dest="respect_move", action="store_false",
                   help="不尊重移动：被移走的条目在目标目录重新创建一份")
    p.add_argument("--exclude", nargs="*", default=None, help="排除 glob 模式")
    p.add_argument("--dry-run", action="store_true", help="仅预览，不实际写入")
    p.add_argument("--init", action="store_true", help="仅初始化配置")
    p.add_argument("--background", action="store_true",
                   help="后台运行：立即返回 task 信息，进度写 progress.json（推荐大批量同步）")
    p.add_argument("--status", action="store_true",
                   help="查询后台同步进度（读取 progress.json）")
    p.add_argument("--no-progress", action="store_true", help="不写进度文件")
    p.add_argument("--_bg-child", dest="bg_child", action="store_true",
                   help=argparse.SUPPRESS)  # 内部：标记当前是后台子进程
    return p


def _build_background_argv(original_args, script_path, vault_path):
    """保留原始参数启动后台子进程，仅替换 background 标记。"""
    original = list(original_args)
    child = [sys.executable, os.path.abspath(script_path)]
    child.extend(arg for arg in original if arg != "--background")
    child.append("--_bg-child")
    has_vault = any(
        arg == "--vault-path" or arg.startswith("--vault-path=")
        for arg in original
    )
    if not has_vault:
        child += ["--vault-path", vault_path]
    return child


def main():
    p = build_argument_parser()
    args = p.parse_args()

    vault_path = args.vault_path or detect_vault_path()
    if not vault_path or not os.path.isdir(vault_path):
        print(json.dumps({"error": f"无效 vault 路径: {vault_path}"}, ensure_ascii=False))
        sys.exit(1)

    # ── --status：查询后台同步进度，立即返回 ──
    if args.status:
        prog = read_progress(vault_path)
        if prog is None:
            print(json.dumps({"status": "no_progress",
                              "message": "无进度记录（尚未运行过同步，或进度文件已清理）"},
                             ensure_ascii=False))
            return
        total = prog.get("total", 0)
        done = prog.get("done", 0)
        prog["percent"] = round(done / total * 100, 1) if total else 0
        print(json.dumps(prog, ensure_ascii=False, indent=2))
        return

    config = load_config(vault_path)
    if args.target_space_id:
        config["target_space_id"] = args.target_space_id
    if args.target_folder_id:
        config["target_folder_entry_id"] = args.target_folder_id
    if args.lexiang_profile is not None:
        # 选择器互斥；切换时清掉另一种旧配置。
        config["lexiang_profile"] = args.lexiang_profile
        config["lexiang_credential_file"] = ""
    elif args.lexiang_credential_file is not None:
        config["lexiang_credential_file"] = args.lexiang_credential_file
        config["lexiang_profile"] = ""
    if args.conflict_strategy:
        config["conflict_strategy"] = args.conflict_strategy
    if args.respect_move is not None:
        config["respect_move"] = args.respect_move
    if args.exclude is not None:
        config["exclude_patterns"] = args.exclude

    try:
        # 只解析位置并校验选择器，不读取凭证，更不会把 token 写入配置。
        resolve_personal_credential_selector(
            config.get("lexiang_profile") or None,
            config.get("lexiang_credential_file") or None,
        )
    except LexiangError as error:
        p.error(str(error))

    if args.init:
        path = save_config(vault_path, config)
        print(json.dumps({"status": "initialized", "config_path": path, "config": config},
                         ensure_ascii=False, indent=2))
        return

    if not config.get("target_space_id"):
        print(json.dumps({"error": "缺少 target_space_id"}, ensure_ascii=False))
        sys.exit(1)
    if not args.mode:
        print(json.dumps({"error": "缺少 --mode (full|incremental)"}, ensure_ascii=False))
        sys.exit(1)

    save_config(vault_path, config)

    # ── --background：把自身 re-spawn 到后台，立即返回 task 信息 ──
    # dry-run 很快，不需要后台。
    if args.background and not args.bg_child and not args.dry_run:
        import subprocess
        orig = sys.argv[1:]
        child_argv = _build_background_argv(orig, __file__, vault_path)
        # detach：新会话、脱离父进程，stdout/stderr 重定向到日志
        log_path = os.path.join(get_progress_path(vault_path) + ".log")
        try:
            logf = open(log_path, "a", encoding="utf-8")
        except OSError:
            logf = subprocess.DEVNULL
        proc = subprocess.Popen(
            child_argv, stdout=logf, stderr=logf,
            stdin=subprocess.DEVNULL, start_new_session=True,
        )
        # 初始化一份 progress，避免紧接着 --status 读到空
        try:
            ProgressWriter(vault_path, args.mode, total=0,
                           enabled=not args.no_progress).note(
                message=f"后台同步已启动（pid={proc.pid}），正在扫描…")
        except Exception:
            pass
        print(json.dumps({
            "status": "started",
            "background": True,
            "pid": proc.pid,
            "mode": args.mode,
            "progress_path": get_progress_path(vault_path),
            "log_path": log_path,
            "hint": "用 `--status` 轮询进度；完成后 status=completed。请勿前台阻塞等待。",
        }, ensure_ascii=False, indent=2))
        return

    # 进度写入器（前台/后台子进程都写，便于 --status 查询）
    prog_writer = None
    if not args.dry_run and not args.no_progress:
        prog_writer = ProgressWriter(vault_path, args.mode, total=0)

    # 增量落盘回调：每个写操作成功后立即保存 manifest（中断安全）
    def persist(manifest):
        save_manifest(vault_path, manifest)

    def _run():
        """执行同步主体，返回 (report, manifest, interrupted, error_msg)"""
        _interrupted = False
        _error_msg = None
        _report = _manifest = None
        try:
            _report, _manifest = do_sync(
                vault_path, config, args.mode, args.source_dirs, args.dry_run,
                persist=persist, progress=prog_writer,
            )
        except KeyboardInterrupt:
            _interrupted = True
            _error_msg = "用户中断（manifest 已逐步落盘，可重跑增量同步续传）"
        except LexiangError as e:
            _error_msg = f"乐享 API 错误: {e}（manifest 已逐步落盘，可重跑续传）"
        finally:
            # do_sync 内部已逐项落盘；这里兜底再保存一次最终状态
            if _manifest is not None and not args.dry_run:
                try:
                    save_manifest(vault_path, _manifest)
                except Exception:
                    pass
            # 收尾进度状态
            if prog_writer is not None:
                if _interrupted:
                    prog_writer.finish("interrupted",
                                       stats=_report.stats if _report else None,
                                       message=_error_msg or "已中断，可重跑续传")
                elif _error_msg:
                    prog_writer.finish("error",
                                       stats=_report.stats if _report else None,
                                       message=_error_msg)
                else:
                    prog_writer.finish("completed",
                                       stats=_report.stats if _report else None,
                                       message="同步完成")
        return _report, _manifest, _interrupted, _error_msg

    # dry-run 不写状态，无需加锁；实际写入时用文件锁防止跨会话并发同步
    if args.dry_run:
        report, manifest, interrupted, error_msg = _run()
    else:
        try:
            with sync_lock(vault_path):
                report, manifest, interrupted, error_msg = _run()
        except SyncLockError as e:
            print(json.dumps({"status": "locked", "error": str(e)}, ensure_ascii=False))
            sys.exit(2)

    if error_msg:
        out = {"status": "interrupted" if interrupted else "error", "error": error_msg}
        if report is not None:
            out["stats"] = report.stats
            try:
                out["report_path"] = report.save(vault_path)
            except Exception:
                pass
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(130 if interrupted else 1)

    report_path = report.save(vault_path)
    summary = {
        "status": "completed",
        "mode": args.mode,
        "dry_run": args.dry_run,
        "stats": report.stats,
        "report_path": report_path,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
