#!/usr/bin/env python3
"""
test_sync.py - sync-obsidian-to-lexiang 单元测试 + 集成测试

测试层级:
  1. Unit: manifest.py 读写
  2. Unit: converter.py wikilink/图片解析
  3. Integration: sync.py 计划生成（全量/增量）
  4. E2E: 标记为 e2e，需手动触发（涉及真实乐享 MCP 调用）

运行:
  python3 test_sync.py              # 运行全部单元测试和集成测试
  python3 test_sync.py -v           # 详细输出
  python3 test_sync.py TestManifest # 只运行 manifest 测试
"""

import json
import io
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from unittest import mock

# 将 scripts 目录加入 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manifest import (
    load_config,
    save_config,
    load_manifest,
    save_manifest,
    new_manifest,
    compute_content_hash,
    get_file_mtime,
    now_iso,
    get_entry,
    set_entry,
    remove_entry,
    list_entries,
    ensure_plugin_dir,
    PLUGIN_DIR,
    acquire_lock,
    release_lock,
    sync_lock,
    SyncLockError,
    _pid_alive,
    _read_lock_info,
    get_plugin_dir,
    LOCK_FILE,
    LOCK_STALE_SECONDS,
)
from converter import (
    convert_wikilinks,
    extract_attachments,
    convert_file,
    resolve_obsidian_path,
    is_image_file,
    is_attachment_file,
    get_obsidian_attachment_folder,
    split_into_segments,
    has_local_images,
    RE_WIKI_IMAGE,
    RE_WIKI_LINK,
    RE_MD_IMAGE,
)
from sync import (
    _build_background_argv,
    _build_markdown_uploader_command,
    detect_vault_path,
    build_argument_parser,
    should_exclude,
    scan_vault,
    do_sync,
    _iso_to_ts,
)
from report import (
    SyncReport,
    cleanup_old_reports,
    generate_report_filename,
    get_reports_dir,
)
from lexiang_api import (
    DEFAULT_PERSONAL_CREDENTIALS,
    PERSONAL_PROFILE_DIR,
    LexiangConnector,
    discover_token,
    load_personal_credential,
    resolve_personal_credential_selector,
    _decode_jwt_exp,
    LexiangError,
)


class TestManifest(unittest.TestCase):
    """manifest.py 单元测试"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_vault_")
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_new_manifest(self):
        m = new_manifest()
        self.assertEqual(m["version"], 1)
        self.assertEqual(m["entries"], {})
        self.assertIn("space_id", m)

    def test_save_and_load_manifest(self):
        m = new_manifest()
        m["space_id"] = "test_space"
        set_entry(m, "dir1/note.md", "page", "entry_123", "sha256:abc", 1000.0)
        save_manifest(self.tmpdir, m)

        loaded = load_manifest(self.tmpdir)
        self.assertEqual(loaded["space_id"], "test_space")
        entry = get_entry(loaded, "dir1/note.md")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["entry_id"], "entry_123")
        self.assertEqual(entry["type"], "page")
        self.assertEqual(entry["content_hash"], "sha256:abc")

    def test_save_and_load_config(self):
        config = {"target_space_id": "sp_123", "conflict_strategy": "obsidian_wins"}
        save_config(self.tmpdir, config)

        loaded = load_config(self.tmpdir)
        self.assertEqual(loaded["target_space_id"], "sp_123")
        self.assertEqual(loaded["conflict_strategy"], "obsidian_wins")

    def test_set_and_remove_entry(self):
        m = new_manifest()
        set_entry(m, "test.md", "page", "e1", "sha256:x", 100.0)
        self.assertIsNotNone(get_entry(m, "test.md"))

        removed = remove_entry(m, "test.md")
        self.assertIsNotNone(removed)
        self.assertIsNone(get_entry(m, "test.md"))

    def test_list_entries_filter(self):
        m = new_manifest()
        set_entry(m, "dir1", "folder", "f1")
        set_entry(m, "dir1/a.md", "page", "p1", "sha256:a", 100.0)
        set_entry(m, "dir1/b.md", "page", "p2", "sha256:b", 200.0)

        folders = list_entries(m, "folder")
        self.assertEqual(len(folders), 1)

        pages = list_entries(m, "page")
        self.assertEqual(len(pages), 2)

        all_entries = list_entries(m)
        self.assertEqual(len(all_entries), 3)

    def test_compute_content_hash(self):
        test_file = os.path.join(self.tmpdir, "test.md")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Hello World")
        h1 = compute_content_hash(test_file)
        self.assertTrue(h1.startswith("sha256:"))

        # 同样内容应该得到相同 hash
        test_file2 = os.path.join(self.tmpdir, "test2.md")
        with open(test_file2, "w", encoding="utf-8") as f:
            f.write("Hello World")
        h2 = compute_content_hash(test_file2)
        self.assertEqual(h1, h2)

        # 不同内容应该得到不同 hash
        with open(test_file2, "w", encoding="utf-8") as f:
            f.write("Different content")
        h3 = compute_content_hash(test_file2)
        self.assertNotEqual(h1, h3)

    def test_now_iso(self):
        ts = now_iso()
        self.assertIsInstance(ts, str)
        # 应该是合法的 ISO 格式
        self.assertIn("T", ts)

    def test_plugin_dir_creation(self):
        plugin_dir = ensure_plugin_dir(self.tmpdir)
        self.assertTrue(os.path.isdir(plugin_dir))
        self.assertTrue(plugin_dir.endswith(PLUGIN_DIR))


class TestConverter(unittest.TestCase):
    """converter.py 单元测试"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_vault_")
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"), exist_ok=True)
        os.makedirs(os.path.join(self.tmpdir, "attachments"), exist_ok=True)
        os.makedirs(os.path.join(self.tmpdir, "notes"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_is_image_file(self):
        self.assertTrue(is_image_file("photo.png"))
        self.assertTrue(is_image_file("PHOTO.JPG"))
        self.assertTrue(is_image_file("icon.svg"))
        self.assertFalse(is_image_file("doc.pdf"))
        self.assertFalse(is_image_file("note.md"))

    def test_is_attachment_file(self):
        self.assertTrue(is_attachment_file("photo.png"))
        self.assertTrue(is_attachment_file("doc.pdf"))
        self.assertTrue(is_attachment_file("data.xlsx"))
        self.assertFalse(is_attachment_file("note.md"))
        self.assertFalse(is_attachment_file("style.css"))

    # --- Wikilink 图片正则 ---
    def test_wiki_image_regex(self):
        cases = [
            ("![[image.png]]", "image.png", None),
            ("![[photo.jpg|alt text]]", "photo.jpg", "alt text"),
            ("![[dir/image.png]]", "dir/image.png", None),
            ("![[截图 2024.png]]", "截图 2024.png", None),
        ]
        for text, expected_name, expected_alt in cases:
            match = RE_WIKI_IMAGE.search(text)
            self.assertIsNotNone(match, f"Failed to match: {text}")
            self.assertEqual(match.group(1), expected_name)
            if expected_alt:
                self.assertEqual(match.group(2), expected_alt)

    # --- Wikilink 文档链接正则 ---
    def test_wiki_link_regex(self):
        cases = [
            ("[[note]]", "note", None, None),
            ("[[note|display]]", "note", None, "display"),
            ("[[note#heading]]", "note", "heading", None),
            ("[[note#heading|display]]", "note", "heading", "display"),
        ]
        for text, expected_name, expected_heading, expected_display in cases:
            match = RE_WIKI_LINK.search(text)
            self.assertIsNotNone(match, f"Failed to match: {text}")
            self.assertEqual(match.group(1), expected_name)
            if expected_heading:
                self.assertEqual(match.group(2), expected_heading)
            if expected_display:
                self.assertEqual(match.group(3), expected_display)

    def test_wiki_image_not_match_wiki_link(self):
        """![[image]] 不应被 wiki_link 正则匹配"""
        text = "![[image.png]]"
        match = RE_WIKI_LINK.search(text)
        self.assertIsNone(match)

    # --- Wikilink 转换 ---
    def test_convert_wikilinks_basic(self):
        content = "See [[my note]] for details."
        result = convert_wikilinks(content)
        self.assertIn("[my note]", result)
        self.assertNotIn("[[", result)

    def test_convert_wikilinks_with_heading(self):
        content = "See [[note#section]] for details."
        result = convert_wikilinks(content)
        self.assertIn("note > section", result)
        self.assertIn("note#section", result)

    def test_convert_wikilinks_with_display(self):
        content = "See [[note|click here]] for details."
        result = convert_wikilinks(content)
        self.assertIn("[click here]", result)

    def test_convert_wiki_image(self):
        content = "Here is ![[photo.png]] in text."
        result = convert_wikilinks(content)
        self.assertIn("![photo.png](photo.png)", result)
        self.assertNotIn("![[", result)

    def test_convert_wiki_image_with_alt(self):
        content = "Here is ![[photo.png|my photo]] in text."
        result = convert_wikilinks(content)
        self.assertIn("![my photo](photo.png)", result)

    def test_convert_wiki_image_with_attachment_map(self):
        content = "Here is ![[photo.png]] in text."
        att_map = {"photo.png": "/assets/uploaded_123"}
        result = convert_wikilinks(content, att_map)
        self.assertIn("![photo.png](/assets/uploaded_123)", result)

    def test_convert_md_image_with_attachment_map(self):
        content = "Here is ![alt](images/photo.png) in text."
        att_map = {"photo.png": "/assets/uploaded_456"}
        result = convert_wikilinks(content, att_map)
        self.assertIn("![alt](/assets/uploaded_456)", result)

    def test_convert_md_image_http_untouched(self):
        content = "Here is ![alt](https://example.com/img.png) in text."
        result = convert_wikilinks(content)
        self.assertIn("https://example.com/img.png", result)

    # --- 附件解析 ---
    def test_extract_attachments_wikilink(self):
        # 创建测试文件
        img_path = os.path.join(self.tmpdir, "attachments", "photo.png")
        with open(img_path, "wb") as f:
            f.write(b"\x89PNG\r\n")

        note_path = os.path.join(self.tmpdir, "notes", "test.md")
        with open(note_path, "w", encoding="utf-8") as f:
            f.write("Hello ![[photo.png]] world")

        attachments = extract_attachments(
            "Hello ![[photo.png]] world",
            note_path,
            self.tmpdir,
        )
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].file_name, "photo.png")
        self.assertTrue(attachments[0].is_image)

    def test_extract_attachments_md_image(self):
        img_path = os.path.join(self.tmpdir, "notes", "img.jpg")
        with open(img_path, "wb") as f:
            f.write(b"\xff\xd8\xff")

        note_path = os.path.join(self.tmpdir, "notes", "test.md")
        content = "![desc](img.jpg)"

        attachments = extract_attachments(content, note_path, self.tmpdir)
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].file_name, "img.jpg")
        self.assertTrue(attachments[0].is_image)

    def test_extract_attachments_dedup(self):
        """同一文件多次引用只提取一次"""
        img_path = os.path.join(self.tmpdir, "attachments", "dup.png")
        with open(img_path, "wb") as f:
            f.write(b"\x89PNG")

        note_path = os.path.join(self.tmpdir, "notes", "test.md")
        content = "![[dup.png]] and again ![[dup.png]]"

        attachments = extract_attachments(content, note_path, self.tmpdir)
        self.assertEqual(len(attachments), 1)

    def test_extract_attachments_missing_file(self):
        """引用的文件不存在时不报错，只是不加入列表"""
        note_path = os.path.join(self.tmpdir, "notes", "test.md")
        with open(note_path, "w", encoding="utf-8") as f:
            f.write("content")

        attachments = extract_attachments(
            "![[nonexistent.png]]", note_path, self.tmpdir
        )
        self.assertEqual(len(attachments), 0)

    # --- resolve_obsidian_path ---
    def test_resolve_obsidian_path_in_attachment_folder(self):
        img_path = os.path.join(self.tmpdir, "attachments", "found.png")
        with open(img_path, "wb") as f:
            f.write(b"\x89PNG")

        result = resolve_obsidian_path(
            "found.png",
            os.path.join(self.tmpdir, "notes"),
            self.tmpdir,
            "attachments",
        )
        self.assertEqual(result, img_path)

    def test_resolve_obsidian_path_in_current_dir(self):
        img_path = os.path.join(self.tmpdir, "notes", "local.png")
        with open(img_path, "wb") as f:
            f.write(b"\x89PNG")

        result = resolve_obsidian_path(
            "local.png",
            os.path.join(self.tmpdir, "notes"),
            self.tmpdir,
        )
        self.assertEqual(result, img_path)

    def test_resolve_obsidian_path_global_search(self):
        deep_dir = os.path.join(self.tmpdir, "deep", "nested")
        os.makedirs(deep_dir, exist_ok=True)
        img_path = os.path.join(deep_dir, "global.png")
        with open(img_path, "wb") as f:
            f.write(b"\x89PNG")

        result = resolve_obsidian_path(
            "global.png",
            os.path.join(self.tmpdir, "notes"),
            self.tmpdir,
        )
        self.assertEqual(result, img_path)

    # --- convert_file ---
    def test_convert_file_full(self):
        img_path = os.path.join(self.tmpdir, "attachments", "pic.png")
        with open(img_path, "wb") as f:
            f.write(b"\x89PNG")

        note_path = os.path.join(self.tmpdir, "notes", "full_test.md")
        with open(note_path, "w", encoding="utf-8") as f:
            f.write("# Title\n\n![[pic.png]]\n\nSee [[other note]] for more.\n")

        result = convert_file(note_path, self.tmpdir)
        self.assertNotIn("![[", result.content)
        self.assertNotIn("[[other note]]", result.content)
        self.assertIn("![pic.png]", result.content)
        self.assertIn("[other note]", result.content)
        self.assertEqual(len(result.attachments), 1)

    def test_get_obsidian_attachment_folder(self):
        # 没有 app.json 时返回空
        folder = get_obsidian_attachment_folder(self.tmpdir)
        self.assertEqual(folder, "")

        # 有 app.json 时返回配置值
        app_json = os.path.join(self.tmpdir, ".obsidian", "app.json")
        with open(app_json, "w") as f:
            json.dump({"attachmentFolderPath": "assets"}, f)
        folder = get_obsidian_attachment_folder(self.tmpdir)
        self.assertEqual(folder, "assets")


class TestSegments(unittest.TestCase):
    """图文切片：split_into_segments / has_local_images"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_seg_")
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"), exist_ok=True)
        # 造一张真实存在的本地图片（1x1 PNG）
        png = bytes.fromhex(
            "89504e470d0a1a0a0000000d4948445200000001000000010802000000907753"
            "de0000000c4944415408d763f8cfc0f01f0005000186a0a4d6000000004945"
            "4e44ae426082")
        self.img = os.path.join(self.tmpdir, "pic.png")
        with open(self.img, "wb") as f:
            f.write(png)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _md(self, content, name="doc.md"):
        p = os.path.join(self.tmpdir, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        return p

    @staticmethod
    def _read(path):
        with open(path, encoding="utf-8") as handle:
            return handle.read()

    def test_no_image_single_text_segment(self):
        md = self._md("# 标题\n\n纯文字内容，无图片。")
        segs = split_into_segments(self._read(md), md, self.tmpdir, "")
        self.assertEqual(len(segs), 1)
        self.assertEqual(segs[0].kind, "text")
        self.assertFalse(has_local_images(self._read(md), md, self.tmpdir, ""))

    def test_wiki_local_image_split(self):
        md = self._md("前文\n\n![[pic.png]]\n\n后文")
        segs = split_into_segments(self._read(md), md, self.tmpdir, "")
        kinds = [s.kind for s in segs]
        self.assertEqual(kinds, ["text", "image", "text"])
        img = next(s for s in segs if s.kind == "image")
        self.assertEqual(os.path.basename(img.image_abs_path), "pic.png")
        self.assertTrue(has_local_images(self._read(md), md, self.tmpdir, ""))

    def test_md_local_image_split(self):
        md = self._md("段落\n\n![描述](pic.png)\n\n尾段")
        segs = split_into_segments(self._read(md), md, self.tmpdir, "")
        self.assertEqual([s.kind for s in segs], ["text", "image", "text"])
        img = next(s for s in segs if s.kind == "image")
        self.assertEqual(img.image_alt, "描述")

    def test_remote_image_stays_in_text(self):
        md = self._md("![x](https://example.com/a.png)\n\n文字")
        segs = split_into_segments(self._read(md), md, self.tmpdir, "")
        # 公网图不切分，整篇是一个 text 片段
        self.assertTrue(all(s.kind == "text" for s in segs))
        self.assertFalse(has_local_images(self._read(md), md, self.tmpdir, ""))

    def test_missing_local_image_not_split(self):
        # 引用了不存在的图片 → 不当作 image 片段（避免上传失败）
        md = self._md("文字\n\n![[notexist.png]]\n\n更多")
        segs = split_into_segments(self._read(md), md, self.tmpdir, "")
        self.assertTrue(all(s.kind == "text" for s in segs))

    def test_multiple_images_order(self):
        md = self._md("A\n\n![[pic.png]]\n\nB\n\n![](pic.png)\n\nC")
        segs = split_into_segments(self._read(md), md, self.tmpdir, "")
        self.assertEqual([s.kind for s in segs],
                         ["text", "image", "text", "image", "text"])


class TestSync(unittest.TestCase):
    """sync.py 集成测试"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_vault_")
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"), exist_ok=True)

        # 创建测试目录结构
        # vault/
        #   dir1/
        #     note_a.md
        #     note_b.md
        #   dir2/
        #     sub/
        #       deep.md
        #   root_note.md
        for d in ["dir1", "dir2", os.path.join("dir2", "sub")]:
            os.makedirs(os.path.join(self.tmpdir, d), exist_ok=True)

        files = {
            "root_note.md": "# Root\n\nRoot content.",
            os.path.join("dir1", "note_a.md"): "# A\n\nContent A with ![[img.png]]",
            os.path.join("dir1", "note_b.md"): "# B\n\nContent B",
            os.path.join("dir2", "sub", "deep.md"): "# Deep\n\nDeep content [[note_a]]",
        }
        for rel, content in files.items():
            with open(os.path.join(self.tmpdir, rel), "w", encoding="utf-8") as f:
                f.write(content)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_should_exclude(self):
        self.assertTrue(should_exclude(".obsidian/plugins/x", [".obsidian/**"]))
        self.assertTrue(should_exclude("test.canvas", ["*.canvas"]))
        self.assertFalse(should_exclude("dir1/note.md", [".obsidian/**", "*.canvas"]))

    def test_scan_vault_all(self):
        result = scan_vault(self.tmpdir, [], [".obsidian/**", "*.canvas"])
        self.assertEqual(len(result["folders"]), 3)  # dir1, dir2, dir2/sub
        self.assertEqual(len(result["files"]), 4)

        # 确保 folders 按深度排序
        folder_depths = [f.count(os.sep) for f in result["folders"]]
        self.assertEqual(folder_depths, sorted(folder_depths))

    def test_scan_vault_source_dirs(self):
        result = scan_vault(self.tmpdir, ["dir1"], [".obsidian/**"])
        self.assertEqual(len(result["folders"]), 1)  # 只有 dir1
        self.assertEqual(len(result["files"]), 2)  # note_a.md, note_b.md

    def test_scan_vault_hash_consistency(self):
        result = scan_vault(self.tmpdir, [], [".obsidian/**"])
        for f in result["files"]:
            self.assertTrue(f["hash"].startswith("sha256:"))
            self.assertGreater(f["mtime"], 0)

    def test_scan_vault_non_md_files(self):
        """非 .md 文件（PDF/图片等）应被扫描为 kind=file，递归生效"""
        # 在 dir1 放一个 PDF，在 dir2/sub 放一个 png
        with open(os.path.join(self.tmpdir, "dir1", "doc.pdf"), "wb") as f:
            f.write(b"%PDF-1.4 fake")
        with open(os.path.join(self.tmpdir, "dir2", "sub", "img.png"), "wb") as f:
            f.write(b"\x89PNG fake")
        result = scan_vault(self.tmpdir, [], [".obsidian/**", "*.canvas"])

        by_path = {f["rel_path"]: f for f in result["files"]}
        # PDF 与 PNG 都被纳入，kind=file
        self.assertIn(os.path.join("dir1", "doc.pdf"), by_path)
        self.assertEqual(by_path[os.path.join("dir1", "doc.pdf")]["kind"], "file")
        self.assertIn(os.path.join("dir2", "sub", "img.png"), by_path)
        self.assertEqual(by_path[os.path.join("dir2", "sub", "img.png")]["kind"], "file")
        # .md 仍为 page
        self.assertEqual(by_path["root_note.md"]["kind"], "page")

    def test_scan_vault_skips_system_files(self):
        """系统/隐藏文件（.DS_Store / .canvas）不应被纳入"""
        with open(os.path.join(self.tmpdir, ".DS_Store"), "wb") as f:
            f.write(b"junk")
        with open(os.path.join(self.tmpdir, "board.canvas"), "w") as f:
            f.write("{}")
        result = scan_vault(self.tmpdir, [], [".obsidian/**", "*.canvas"])
        paths = {f["rel_path"] for f in result["files"]}
        self.assertNotIn(".DS_Store", paths)
        self.assertNotIn("board.canvas", paths)


class TestDoSyncDryRun(unittest.TestCase):
    """do_sync(dry_run=True) 测试 —— 不触发任何乐享 API 调用，无需凭证"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_vault_")
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"), exist_ok=True)

        # vault 结构：3 个目录 + 4 篇文档
        for d in ["dir1", "dir2", os.path.join("dir2", "sub")]:
            os.makedirs(os.path.join(self.tmpdir, d), exist_ok=True)

        files = {
            "root_note.md": "# Root\n\nRoot content.",
            os.path.join("dir1", "note_a.md"): "# A\n\nContent A",
            os.path.join("dir1", "note_b.md"): "# B\n\nContent B",
            os.path.join("dir2", "sub", "deep.md"): "# Deep\n\nDeep content",
        }
        for rel, content in files.items():
            with open(os.path.join(self.tmpdir, rel), "w", encoding="utf-8") as f:
                f.write(content)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_dry_run_returns_report_and_manifest(self):
        config = {
            "target_space_id": "test_space",
            "target_folder_entry_id": "test_folder",
            "exclude_patterns": [".obsidian/**", "*.canvas"],
        }
        report, manifest = do_sync(
            self.tmpdir, config, mode="full", source_dirs=[], dry_run=True
        )

        # 返回值类型
        self.assertIsInstance(report, SyncReport)
        self.assertIsInstance(manifest, dict)
        self.assertTrue(report.dry_run)
        self.assertEqual(report.mode, "full")

    def test_dry_run_stats_counts(self):
        config = {
            "target_space_id": "test_space",
            "target_folder_entry_id": "",
            "exclude_patterns": [".obsidian/**", "*.canvas"],
        }
        report, _ = do_sync(
            self.tmpdir, config, mode="full", source_dirs=[], dry_run=True
        )
        # 3 个目录、4 篇文档
        self.assertEqual(report.stats["folders_created"], 3)
        self.assertEqual(report.stats["pages_created"], 4)
        self.assertEqual(report.stats["errors"], 0)

    def test_dry_run_no_api_calls(self):
        """dry_run 应在创建 LexiangAPI 之前短路，即使没有凭证也不报错"""
        # 确保不会因为缺少环境变量凭证而失败
        config = {
            "target_space_id": "test_space",
            "target_folder_entry_id": "",
            "exclude_patterns": [".obsidian/**"],
        }
        # 不抛异常即证明未真正实例化 LexiangAPI / 未发起网络请求
        report, _ = do_sync(
            self.tmpdir, config, mode="full", source_dirs=[], dry_run=True
        )
        # 所有动作状态均为 success（dry-run），无 error
        for a in report.actions:
            self.assertEqual(a["status"], "success")

    def test_dry_run_source_dirs(self):
        config = {
            "target_space_id": "test_space",
            "target_folder_entry_id": "",
            "exclude_patterns": [".obsidian/**"],
        }
        report, _ = do_sync(
            self.tmpdir, config, mode="full", source_dirs=["dir1"], dry_run=True
        )
        self.assertEqual(report.stats["folders_created"], 1)  # 只有 dir1
        self.assertEqual(report.stats["pages_created"], 2)    # note_a, note_b


class FakeConnector:
    """模拟 LexiangConnector，用于测试 do_sync 的非 dry-run 异常处理逻辑（不发网络）"""

    def __init__(self, deleted_ids=None, parent_overrides=None, edited_overrides=None,
                 children_map=None):
        self._seq = 0
        self.created_pages = []          # [(name, parent_id)]
        self.created_folders = []        # [(name, parent_id)]
        self.updated_pages = []          # [entry_id]
        self.uploaded_files = []         # [(filename, parent_id)]
        self.deleted_ids = set(deleted_ids or [])      # 视为已删除的 entry
        self.parent_overrides = parent_overrides or {}  # {entry_id: actual_parent}
        self.edited_overrides = edited_overrides or {}  # {entry_id: edited_ts}
        # {parent_id: [entry_dict, ...]}，用于模拟乐享侧已有子项（查重测试）
        self.children_map = children_map or {}

    def _next(self, prefix):
        self._seq += 1
        return f"{prefix}_{self._seq}"

    def create_folder(self, space_id, name, parent_id=None):
        eid = self._next("folder")
        self.created_folders.append((name, parent_id))
        return eid

    def upload_attachment(self, file_path, parent_entry_id):
        return ""

    def upload_file_entry(self, file_path, parent_entry_id):
        eid = self._next("file")
        self.uploaded_files.append((os.path.basename(file_path), parent_entry_id))
        return eid

    def get_entry_edited_at(self, entry_id):
        return self.edited_overrides.get(entry_id, 0)

    def probe_entry(self, entry_id):
        if entry_id in self.deleted_ids:
            return {"exists": False, "parent_id": "", "edited_at": 0}
        return {
            "exists": True,
            "parent_id": self.parent_overrides.get(entry_id, ""),
            "edited_at": self.edited_overrides.get(entry_id, 0),
        }

    def list_children(self, parent_id, limit=100):
        """返回模拟的乐享侧子项列表（供查重测试）"""
        return list(self.children_map.get(parent_id, []))


class TestDoSyncHardening(unittest.TestCase):
    """中断恢复 / entry 失效重建 / 移动检测（注入 FakeConnector，无网络）"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_vault_")
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"), exist_ok=True)
        os.makedirs(os.path.join(self.tmpdir, "dir1"), exist_ok=True)
        files = {
            os.path.join("dir1", "a.md"): "# A\n\nContent A",
            os.path.join("dir1", "b.md"): "# B\n\nContent B",
        }
        for rel, content in files.items():
            with open(os.path.join(self.tmpdir, rel), "w", encoding="utf-8") as f:
                f.write(content)
        self.config = {
            "target_space_id": "sp",
            "target_folder_entry_id": "TARGET",
            "conflict_strategy": "lexiang_wins",
            "exclude_patterns": [".obsidian/**"],
            "sync_attachments": False,
            "respect_move": True,
        }

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _patch_api(self, fake):
        """让 do_sync 使用 FakeConnector 和假公共上传器，不发网络请求。"""
        import sync as sync_mod
        self._orig = sync_mod.LexiangConnector
        self._orig_uploader = sync_mod._run_markdown_uploader
        sync_mod.LexiangConnector = lambda *a, **k: fake

        def fake_uploader(source_path, vault_path, attachment_folder, *,
                          parent_id=None, entry_id=None, name=None, include_images=True,
                          credential_selector=None):
            with tempfile.TemporaryDirectory(prefix="test-uploader-") as package_dir:
                _, image_count = sync_mod._prepare_markdown_package(
                    source_path,
                    vault_path,
                    attachment_folder,
                    package_dir,
                    include_images=include_images,
                )
            if entry_id:
                fake.updated_pages.append(entry_id)
                result_id = entry_id
            else:
                result_id = fake._next("page")
                fake.created_pages.append((name, parent_id))
            fake.embedded_images = getattr(fake, "embedded_images", 0) + image_count
            return {
                "ok": True,
                "entry_id": result_id,
                "local_images": image_count,
                "remote_images": image_count,
                "verified": True,
            }

        sync_mod._run_markdown_uploader = fake_uploader

    def _unpatch(self):
        import sync as sync_mod
        sync_mod.LexiangConnector = self._orig
        sync_mod._run_markdown_uploader = self._orig_uploader

    def test_idempotent_resume_after_interrupt(self):
        """模拟中断后重跑：manifest 已有部分记录，已同步项跳过，不重复创建"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            # 第一次：全量同步（manifest 为空 → 全部新建）
            saved = {}
            def persist(m):
                saved["m"] = json.loads(json.dumps(m))  # 深拷贝模拟落盘
            report1, m1 = do_sync(self.tmpdir, self.config, "full", [], False, persist=persist)
            save_manifest(self.tmpdir, m1)
            self.assertEqual(report1.stats["pages_created"], 2)
            self.assertEqual(len(fake.created_pages), 2)

            # 第二次：用同一 manifest 重跑（模拟中断后续传）→ 应全部跳过
            fake2 = FakeConnector()
            self._unpatch(); self._patch_api(fake2)
            report2, _ = do_sync(self.tmpdir, self.config, "incremental", [], False)
            self.assertEqual(report2.stats["pages_created"], 0)
            self.assertEqual(report2.stats["pages_skipped_no_change"], 2)
            self.assertEqual(len(fake2.created_pages), 0)  # 没有重复创建
        finally:
            self._unpatch()

    def test_persist_called_per_item(self):
        """每个写操作都触发 persist（增量落盘）"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            calls = {"n": 0}
            def persist(m):
                calls["n"] += 1
            do_sync(self.tmpdir, self.config, "full", [], False, persist=persist)
            # 1 目录 + 2 文档 + 末尾时间戳 → 至少 3 次以上
            self.assertGreaterEqual(calls["n"], 3)
        finally:
            self._unpatch()

    def test_deleted_entry_rebuilt(self):
        """乐享侧 entry 被删除 → 重跑时探活失败 → 重新创建"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            # 找到 a.md 的 entry_id，标记为已删除
            a_eid = m1["entries"][os.path.join("dir1", "a.md")]["entry_id"]

            fake2 = FakeConnector(deleted_ids=[a_eid])
            self._unpatch(); self._patch_api(fake2)
            report2, _ = do_sync(self.tmpdir, self.config, "incremental", [], False)
            # a.md 重建（1 篇 created），b.md 跳过
            self.assertEqual(report2.stats["pages_created"], 1)
            self.assertEqual(report2.stats["pages_skipped_no_change"], 1)
        finally:
            self._unpatch()

    def test_manifest_lost_mapping_dedup(self):
        """manifest 丢失映射但乐享侧已有同名 entry → 查重复用，不重复创建"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            dir1_eid = m1["entries"]["dir1"]["entry_id"]
            # 模拟 manifest 丢失 a.md 映射（如断连重建失败冲映射）
            del m1["entries"][os.path.join("dir1", "a.md")]
            save_manifest(self.tmpdir, m1)

            # 第二次增量：乐享侧 dir1 下已有同名 "a" 的 page
            fake2 = FakeConnector(children_map={
                dir1_eid: [{"id": "EXISTING_A", "name": "a", "entry_type": "page"}]
            })
            self._unpatch(); self._patch_api(fake2)
            report2, m2 = do_sync(self.tmpdir, self.config, "incremental", [], False)

            # a.md 复用 EXISTING_A（不创建新），b.md 跳过
            self.assertEqual(report2.stats["pages_created"], 0)
            self.assertEqual(len(fake2.created_pages), 0)
            a_entry = m2["entries"][os.path.join("dir1", "a.md")]
            self.assertEqual(a_entry["entry_id"], "EXISTING_A")
        finally:
            self._unpatch()

    def test_probe_exception_no_wipe(self):
        """probe 抛异常 → 跳过且保留 manifest 映射，不中断不冲映射"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            a_eid = m1["entries"][os.path.join("dir1", "a.md")]["entry_id"]

            # 第二次：probe a 抛异常（模拟代理模式异常）
            fake2 = FakeConnector()
            def boom(entry_id):
                if entry_id == a_eid:
                    raise LexiangError("MCP 网络错误 tools/call: timeout")
                return fake2.__class__.probe_entry(fake2, entry_id)
            fake2.probe_entry = boom
            self._unpatch(); self._patch_api(fake2)
            report2, m2 = do_sync(self.tmpdir, self.config, "incremental", [], False)

            # a.md 报错跳过，b.md 正常跳过；不中断整个同步
            self.assertEqual(report2.stats["errors"], 1)
            self.assertEqual(report2.stats["pages_created"], 0)
            # manifest 仍保留 a.md 的映射（未被冲掉）
            self.assertIn(os.path.join("dir1", "a.md"), m2["entries"])
            self.assertEqual(
                m2["entries"][os.path.join("dir1", "a.md")]["entry_id"], a_eid)
        finally:
            self._unpatch()

    def test_moved_respect_true_no_rebuild(self):
        """respect_move=true：文档被移动后修改内容 → 仍更新原 entry，不重建"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            a_eid = m1["entries"][os.path.join("dir1", "a.md")]["entry_id"]
            # 修改 a.md 内容（触发 update 分支）
            with open(os.path.join(self.tmpdir, "dir1", "a.md"), "w", encoding="utf-8") as f:
                f.write("# A changed\n\nNew content")
            # a 被移动到别处（parent != 预期）
            fake2 = FakeConnector(parent_overrides={a_eid: "SOMEWHERE_ELSE"})
            self._unpatch(); self._patch_api(fake2)
            report2, _ = do_sync(self.tmpdir, self.config, "incremental", [], False)
            # respect_move=true → 不重建，走更新
            self.assertEqual(report2.stats["pages_created"], 0)
            self.assertEqual(report2.stats["pages_updated"], 1)
            self.assertIn(a_eid, fake2.updated_pages)
        finally:
            self._unpatch()

    def test_moved_respect_false_rebuild(self):
        """respect_move=false：文档被移动 → 在目标目录重建一份"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            a_eid = m1["entries"][os.path.join("dir1", "a.md")]["entry_id"]
            with open(os.path.join(self.tmpdir, "dir1", "a.md"), "w", encoding="utf-8") as f:
                f.write("# A changed\n\nNew content")

            cfg = dict(self.config, respect_move=False)
            fake2 = FakeConnector(parent_overrides={a_eid: "SOMEWHERE_ELSE"})
            self._unpatch(); self._patch_api(fake2)
            report2, _ = do_sync(self.tmpdir, cfg, "incremental", [], False)
            # respect_move=false → 重建
            self.assertEqual(report2.stats["pages_created"], 1)
            self.assertEqual(len(fake2.created_pages), 1)
        finally:
            self._unpatch()

    def test_lexiang_wins_skip_when_remote_newer(self):
        """lexiang_wins：乐享侧 edited_at 晚于 last_sync → 跳过覆盖"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            a_eid = m1["entries"][os.path.join("dir1", "a.md")]["entry_id"]
            with open(os.path.join(self.tmpdir, "dir1", "a.md"), "w", encoding="utf-8") as f:
                f.write("# A changed\n\nNew content")
            # 乐享侧 edited_at = 远未来 → 视为有独立更新
            import time as _t
            fake2 = FakeConnector(edited_overrides={a_eid: int(_t.time()) + 99999})
            self._unpatch(); self._patch_api(fake2)
            report2, _ = do_sync(self.tmpdir, self.config, "incremental", [], False)
            self.assertEqual(report2.stats["pages_skipped_conflict"], 1)
            self.assertNotIn(a_eid, fake2.updated_pages)
        finally:
            self._unpatch()

    def test_new_non_md_file_uploaded(self):
        """新增 PDF/图片等非 md 文件 → 增量同步检测到并作为 file 上传"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            # 首次全量：2 篇 md
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            self.assertEqual(len(fake.uploaded_files), 0)

            # 新增一个 PDF
            with open(os.path.join(self.tmpdir, "dir1", "report.pdf"), "wb") as f:
                f.write(b"%PDF-1.4 fake content")

            fake2 = FakeConnector()
            self._unpatch(); self._patch_api(fake2)
            report2, _ = do_sync(self.tmpdir, self.config, "incremental", [], False)
            # PDF 被作为 file 上传，md 跳过
            self.assertEqual(report2.stats["files_created"], 1)
            self.assertEqual(report2.stats["pages_created"], 0)
            self.assertEqual(report2.stats["pages_skipped_no_change"], 2)
            self.assertEqual(len(fake2.uploaded_files), 1)
            self.assertEqual(fake2.uploaded_files[0][0], "report.pdf")
        finally:
            self._unpatch()

    def test_changed_non_md_file_reuploaded(self):
        """非 md 文件内容变化 → 重新上传（删旧映射建新）"""
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            with open(os.path.join(self.tmpdir, "dir1", "report.pdf"), "wb") as f:
                f.write(b"%PDF v1")
            _, m1 = do_sync(self.tmpdir, self.config, "full", [], False)
            save_manifest(self.tmpdir, m1)
            self.assertEqual(len(fake.uploaded_files), 1)

            # 修改 PDF 内容
            with open(os.path.join(self.tmpdir, "dir1", "report.pdf"), "wb") as f:
                f.write(b"%PDF v2 changed bigger content")

            fake2 = FakeConnector()
            self._unpatch(); self._patch_api(fake2)
            report2, _ = do_sync(self.tmpdir, self.config, "incremental", [], False)
            self.assertEqual(report2.stats["files_created"], 1)  # 重新上传
            self.assertEqual(len(fake2.uploaded_files), 1)
        finally:
            self._unpatch()

    def test_local_image_md_uses_segment_path(self):
        """含本地图片的 md → 临时工作包交给公共上传器内嵌图片"""
        # 造一张真实图片
        png = bytes.fromhex(
            "89504e470d0a1a0a0000000d4948445200000001000000010802000000907753"
            "de0000000c4944415408d763f8cfc0f01f0005000186a0a4d6000000004945"
            "4e44ae426082")
        with open(os.path.join(self.tmpdir, "dir1", "pic.png"), "wb") as f:
            f.write(png)
        with open(os.path.join(self.tmpdir, "dir1", "img.md"), "w", encoding="utf-8") as f:
            f.write("正文\n\n![[pic.png]]\n\n结尾")

        cfg = dict(self.config, sync_attachments=True)  # 图文混排需开启附件同步
        fake = FakeConnector()
        self._patch_api(fake)
        try:
            report, _ = do_sync(self.tmpdir, cfg, "full", [], False)
            # img.md 走图文分支，内嵌 1 张图；pic.png 作为独立 file 上传
            self.assertEqual(getattr(fake, "embedded_images", 0), 1)
            self.assertGreaterEqual(report.stats["pages_created"], 1)
        finally:
            self._unpatch()


class TestSyncLock(unittest.TestCase):
    """文件锁：防止跨会话/多进程并发同步同一 vault"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"))
        self.lock_path = os.path.join(get_plugin_dir(self.tmpdir), LOCK_FILE)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_acquire_and_release(self):
        lock = acquire_lock(self.tmpdir)
        self.assertTrue(os.path.exists(lock))
        info = _read_lock_info(lock)
        self.assertEqual(info["pid"], os.getpid())
        release_lock(lock)
        self.assertFalse(os.path.exists(lock))

    def test_double_acquire_rejected(self):
        lock = acquire_lock(self.tmpdir)
        try:
            with self.assertRaises(SyncLockError):
                acquire_lock(self.tmpdir)
        finally:
            release_lock(lock)

    def test_reacquire_after_release(self):
        lock = acquire_lock(self.tmpdir)
        release_lock(lock)
        lock2 = acquire_lock(self.tmpdir)  # 不应抛异常
        self.assertTrue(os.path.exists(lock2))
        release_lock(lock2)

    def test_stale_lock_dead_pid_takeover(self):
        # 伪造一个死进程的锁（同机 + 不存在的 pid）
        os.makedirs(get_plugin_dir(self.tmpdir), exist_ok=True)
        with open(self.lock_path, "w", encoding="utf-8") as f:
            json.dump({"pid": 999999, "host": __import__("socket").gethostname(),
                       "acquired_at": "x", "acquired_ts": time.time()}, f)
        self.assertFalse(_pid_alive(999999))
        lock = acquire_lock(self.tmpdir)  # 应接管
        self.assertEqual(_read_lock_info(lock)["pid"], os.getpid())
        release_lock(lock)

    def test_stale_lock_timeout_takeover(self):
        # 别的机器 + 超时时间戳 → 接管
        os.makedirs(get_plugin_dir(self.tmpdir), exist_ok=True)
        with open(self.lock_path, "w", encoding="utf-8") as f:
            json.dump({"pid": 1, "host": "other-machine", "acquired_at": "x",
                       "acquired_ts": time.time() - LOCK_STALE_SECONDS - 10}, f)
        lock = acquire_lock(self.tmpdir)
        self.assertEqual(_read_lock_info(lock)["pid"], os.getpid())
        release_lock(lock)

    def test_fresh_lock_other_host_rejected(self):
        # 别的机器 + 未超时 → 不接管，拒绝
        os.makedirs(get_plugin_dir(self.tmpdir), exist_ok=True)
        with open(self.lock_path, "w", encoding="utf-8") as f:
            json.dump({"pid": 1, "host": "other-machine", "acquired_at": "x",
                       "acquired_ts": time.time()}, f)
        with self.assertRaises(SyncLockError):
            acquire_lock(self.tmpdir)
        os.remove(self.lock_path)

    def test_corrupt_lock_takeover(self):
        # 锁文件损坏（非 JSON）→ 视为陈旧，接管
        os.makedirs(get_plugin_dir(self.tmpdir), exist_ok=True)
        with open(self.lock_path, "w", encoding="utf-8") as f:
            f.write("not-a-json {{{")
        lock = acquire_lock(self.tmpdir)
        self.assertEqual(_read_lock_info(lock)["pid"], os.getpid())
        release_lock(lock)

    def test_context_manager_releases_on_exception(self):
        with self.assertRaises(RuntimeError):
            with sync_lock(self.tmpdir):
                self.assertTrue(os.path.exists(self.lock_path))
                raise RuntimeError("模拟崩溃")
        self.assertFalse(os.path.exists(self.lock_path))

    def test_release_does_not_delete_others_lock(self):
        # release 只删属于本进程的锁，不误删接管者的锁
        os.makedirs(get_plugin_dir(self.tmpdir), exist_ok=True)
        with open(self.lock_path, "w", encoding="utf-8") as f:
            json.dump({"pid": 888888, "host": "x", "acquired_at": "x",
                       "acquired_ts": time.time()}, f)
        release_lock(self.lock_path)  # pid 不匹配，不应删除
        self.assertTrue(os.path.exists(self.lock_path))
        os.remove(self.lock_path)


class TestLexiangConnector(unittest.TestCase):
    """lexiang_api 连接器：token 发现 / JWT 解析（离线，不发网络请求）"""

    def test_decode_jwt_exp(self):
        import base64, json as _json
        payload = base64.urlsafe_b64encode(
            _json.dumps({"exp": 1782289014}).encode()
        ).decode().rstrip("=")
        fake_jwt = f"header.{payload}.sig"
        self.assertEqual(_decode_jwt_exp(fake_jwt), 1782289014)

    def test_decode_jwt_exp_invalid(self):
        self.assertEqual(_decode_jwt_exp("not-a-jwt"), 0)
        self.assertEqual(_decode_jwt_exp(""), 0)

    def test_discover_token_env_override(self):
        import os as _os
        old = _os.environ.get("LEXIANG_ONEID_TOKEN")
        _os.environ["LEXIANG_ONEID_TOKEN"] = "x" * 40
        try:
            tok, src = discover_token()
            self.assertEqual(tok, "x" * 40)
            self.assertEqual(src, "env:LEXIANG_ONEID_TOKEN")
        finally:
            if old is None:
                _os.environ.pop("LEXIANG_ONEID_TOKEN", None)
            else:
                _os.environ["LEXIANG_ONEID_TOKEN"] = old


class TestPersonalCredentials(unittest.TestCase):
    """个人凭证选择与 MCP 鉴权（离线）。"""

    TOKEN = "lxmcp_super_secret_test_token"

    def test_profile_path_resolution(self):
        default = resolve_personal_credential_selector(
            profile="default", environ={}
        )
        self.assertEqual(default.path, DEFAULT_PERSONAL_CREDENTIALS)
        named = resolve_personal_credential_selector(
            profile="obsidian-sync", environ={}
        )
        self.assertEqual(
            named.path, PERSONAL_PROFILE_DIR / "obsidian-sync.json"
        )

    def test_environment_and_explicit_precedence(self):
        selected = resolve_personal_credential_selector(
            profile="explicit",
            environ={
                "LEXIANG_UPLOAD_CREDENTIALS": "/tmp/environment.json",
                "LEXIANG_UPLOAD_PROFILE": "environment",
            },
        )
        self.assertEqual(selected.profile, "explicit")
        selected = resolve_personal_credential_selector(
            environ={
                "LEXIANG_UPLOAD_CREDENTIALS": "/tmp/environment.json",
                "LEXIANG_UPLOAD_PROFILE": "environment",
            }
        )
        self.assertEqual(selected.path, __import__("pathlib").Path("/tmp/environment.json"))
        self.assertEqual(selected.profile, "")
        self.assertIsNone(resolve_personal_credential_selector(environ={}))

    def test_rejects_unsafe_and_conflicting_selectors(self):
        for profile in ("../escape", "nested/profile", "white space", ""):
            with self.subTest(profile=profile), self.assertRaises(LexiangError):
                resolve_personal_credential_selector(profile=profile, environ={})
        with self.assertRaises(LexiangError):
            resolve_personal_credential_selector(
                profile="one", credential_file="/tmp/two.json", environ={}
            )

    def test_loads_nested_uploader_compatible_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "credential.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump({
                    "auth": {
                        "access_token": self.TOKEN,
                        "mcp_company_from": "company-test",
                    }
                }, handle)
            credential = load_personal_credential(path)
        self.assertEqual(credential["mcp_token"], self.TOKEN)
        self.assertEqual(credential["company_from"], "company-test")

    def test_personal_mode_uses_bearer_header_and_company_url(self):
        connector = LexiangConnector(credential={
            "mcp_token": self.TOKEN,
            "company_from": "company test",
        })

        class Response:
            headers = {}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b"{}"

        with mock.patch(
            "lexiang_api.urllib.request.urlopen", return_value=Response()
        ) as urlopen:
            connector._post_once("ping")
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.get_header("Authorization"), f"Bearer {self.TOKEN}"
        )
        self.assertEqual(
            request.full_url,
            "https://mcp.lexiang-app.com/mcp?company_from=company%20test",
        )
        self.assertIsNone(request.get_header("X-oneid-access-token"))

    def test_personal_token_not_exposed_by_errors(self):
        connector = LexiangConnector(credential={
            "mcp_token": self.TOKEN,
            "company_from": "company",
        })
        error = __import__("urllib.error", fromlist=["HTTPError"]).HTTPError(
            connector.mcp_url, 401, "unauthorized", {}, io.BytesIO(b"unauthorized")
        )
        with mock.patch(
            "lexiang_api.urllib.request.urlopen", side_effect=error
        ), self.assertRaises(LexiangError) as raised:
            connector._post_once("ping")
        self.assertNotIn(self.TOKEN, str(raised.exception))


class TestCredentialCommandLine(unittest.TestCase):
    """CLI、uploader 和后台命令的凭证参数透传。"""

    def test_cli_selectors_are_mutually_exclusive(self):
        parser = build_argument_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--lexiang-profile", "one",
                "--lexiang-credential-file", "/tmp/two.json",
            ])

    def test_uploader_command_for_profile_and_file(self):
        profile = resolve_personal_credential_selector(
            profile="obsidian-sync", environ={}
        )
        command = _build_markdown_uploader_command(
            "/skill/lexiang_upload.py", "/tmp/note.md",
            parent_id="parent", name="note", credential_selector=profile,
        )
        self.assertEqual(command[-2:], ["--profile", "obsidian-sync"])

        file_selector = resolve_personal_credential_selector(
            credential_file="~/private/lexiang.json", environ={}
        )
        command = _build_markdown_uploader_command(
            "/skill/lexiang_upload.py", "/tmp/note.md",
            entry_id="entry", credential_selector=file_selector,
        )
        self.assertEqual(command[-2], "--credential-file")
        self.assertEqual(command[-1], str(file_selector.path))

    def test_background_argv_preserves_selector(self):
        original = [
            "--mode", "incremental",
            "--lexiang-profile", "obsidian-sync",
            "--background",
        ]
        child = _build_background_argv(original, "/skill/sync.py", "/vault")
        self.assertNotIn("--background", child)
        self.assertIn("--_bg-child", child)
        index = child.index("--lexiang-profile")
        self.assertEqual(child[index + 1], "obsidian-sync")
        self.assertEqual(child[-2:], ["--vault-path", "/vault"])

    def test_init_persists_selector_without_token(self):
        with tempfile.TemporaryDirectory() as vault:
            os.makedirs(os.path.join(vault, ".obsidian"))
            result = subprocess.run([
                sys.executable,
                os.path.join(os.path.dirname(__file__), "sync.py"),
                "--init",
                "--vault-path", vault,
                "--target-space-id", "space",
                "--lexiang-profile", "obsidian-sync",
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            config = load_config(vault)
            serialized = json.dumps(config)
            self.assertEqual(config["lexiang_profile"], "obsidian-sync")
            self.assertEqual(config["lexiang_credential_file"], "")
            self.assertNotIn("lxmcp_", serialized)


class TestIsoToTs(unittest.TestCase):
    """_iso_to_ts 测试"""

    def test_valid_iso(self):
        ts = _iso_to_ts("2026-06-24T12:00:00+08:00")
        self.assertIsInstance(ts, int)
        self.assertGreater(ts, 0)

    def test_valid_iso_naive(self):
        ts = _iso_to_ts("2026-06-24T12:00:00")
        self.assertIsInstance(ts, int)
        self.assertGreater(ts, 0)

    def test_empty_string(self):
        self.assertEqual(_iso_to_ts(""), 0)

    def test_garbage(self):
        self.assertEqual(_iso_to_ts("not-a-date"), 0)
        self.assertEqual(_iso_to_ts("2026/06/24"), 0)


class TestReport(unittest.TestCase):
    """report.py 单元测试"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_vault_")
        os.makedirs(os.path.join(self.tmpdir, ".obsidian"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_report_filename_format(self):
        filename = generate_report_filename()
        self.assertTrue(filename.startswith("sync_report_"))
        self.assertTrue(filename.endswith(".md"))

    def test_sync_report_basic(self):
        """测试基本报告生成"""
        report = SyncReport(
            mode="full",
            vault_path=self.tmpdir,
            target_space_id="sp_123",
            target_folder_id="f_456",
        )
        report.record_action("create_folder", "dir1", "success", "e_dir1")
        report.record_action("create_page", "dir1/note.md", "success", "e_note1")
        report.record_action("create_page", "dir1/note2.md", "success", "e_note2")

        md = report.to_markdown()
        self.assertIn("全量同步", md)
        self.assertIn("sp_123", md)
        self.assertIn("dir1", md)
        self.assertIn("dir1/note.md", md)
        self.assertIn("✅", md)
        self.assertEqual(report.stats["folders_created"], 1)
        self.assertEqual(report.stats["pages_created"], 2)

    def test_sync_report_incremental_with_skips(self):
        """测试增量报告含跳过和冲突"""
        report = SyncReport(
            mode="incremental",
            vault_path=self.tmpdir,
            target_space_id="sp_123",
            conflict_strategy="lexiang_wins",
        )
        report.record_action("update_page", "note1.md", "success", "e1")
        report.record_action("create_page", "new.md", "success", "e2", "新增文档")
        report.record_action("update_page", "note2.md", "skipped_no_change", "e3")
        report.record_action("update_page", "note3.md", "skipped_conflict", "e4", "乐享侧有更新")
        report.set_source_deleted_ignored(2)

        md = report.to_markdown()
        self.assertIn("增量同步", md)
        self.assertIn("乐享优先", md)
        self.assertIn("⏭️", md)
        self.assertIn("⚠️", md)
        self.assertEqual(report.stats["pages_updated"], 1)
        self.assertEqual(report.stats["pages_created"], 1)
        self.assertEqual(report.stats["pages_skipped_no_change"], 1)
        self.assertEqual(report.stats["pages_skipped_conflict"], 1)
        self.assertEqual(report.stats["source_deleted_ignored"], 2)

    def test_sync_report_with_errors(self):
        """测试含错误的报告"""
        report = SyncReport(
            mode="full",
            vault_path=self.tmpdir,
            target_space_id="sp_123",
        )
        report.record_action("create_folder", "dir1", "success", "e1")
        report.record_action("create_page", "bad.md", "error", "", "MCP 调用失败: 403")
        report.record_action("create_page", "good.md", "success", "e2")

        md = report.to_markdown()
        self.assertIn("错误记录", md)
        self.assertIn("❌", md)
        self.assertIn("MCP 调用失败", md)
        self.assertEqual(report.stats["errors"], 1)
        self.assertEqual(report.stats["pages_created"], 1)

    def test_sync_report_dry_run(self):
        """预览模式报告标记"""
        report = SyncReport(
            mode="full",
            vault_path=self.tmpdir,
            target_space_id="sp_123",
            dry_run=True,
        )
        md = report.to_markdown()
        self.assertIn("预览模式", md)

    def test_save_report(self):
        """测试报告保存到文件"""
        report = SyncReport(
            mode="full",
            vault_path=self.tmpdir,
            target_space_id="sp_123",
        )
        report.record_action("create_folder", "dir1", "success", "e1")
        report.record_action("create_page", "note.md", "success", "e2")

        path = report.save(self.tmpdir)
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(path.endswith(".md"))

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("全量同步", content)
        self.assertIn("dir1", content)

    def test_cleanup_old_reports(self):
        """测试旧报告清理"""
        reports_dir = get_reports_dir(self.tmpdir)
        os.makedirs(reports_dir, exist_ok=True)

        # 创建 15 份报告
        for i in range(15):
            fname = f"sync_report_20260601_{i:06d}.md"
            with open(os.path.join(reports_dir, fname), "w") as f:
                f.write(f"report {i}")

        removed = cleanup_old_reports(self.tmpdir, keep=10)
        self.assertEqual(len(removed), 5)

        remaining = [f for f in os.listdir(reports_dir) if f.startswith("sync_report_")]
        self.assertEqual(len(remaining), 10)

    def test_report_attachment_stats(self):
        """测试附件上传统计"""
        report = SyncReport(
            mode="full",
            vault_path=self.tmpdir,
            target_space_id="sp_123",
        )
        report.record_action("upload_attachment", "img/photo.png", "success", "att_1")
        report.record_action("upload_attachment", "img/logo.svg", "success", "att_2")

        md = report.to_markdown()
        self.assertIn("上传附件", md)
        self.assertEqual(report.stats["attachments_uploaded"], 2)


class TestDetectVault(unittest.TestCase):
    """detect_vault_path 测试"""

    def test_detect_vault_path(self):
        """验证能检测到 vault（真实环境测试）"""
        vault_path = detect_vault_path()
        # 在真实环境中应该能检测到
        if vault_path:
            self.assertTrue(os.path.isdir(vault_path))


class TestRealVault(unittest.TestCase):
    """对真实 vault 凡哥杂谈 的集成测试"""

    VAULT_PATH = "/Users/ajaxhe/Obsidian/凡哥杂谈"
    TARGET_SPACE_ID = "cc9dc48a4a8845ff83c3d403840ae189"
    TARGET_FOLDER_ID = "303b0714d2c94735ae1fdaaac4c4f77b"

    def setUp(self):
        if not os.path.isdir(self.VAULT_PATH):
            self.skipTest("Vault not found, skip real vault test")

    def test_scan_real_vault(self):
        """扫描真实 vault，验证结果合理"""
        result = scan_vault(self.VAULT_PATH, [], [".obsidian/**", "*.canvas"])
        self.assertGreater(len(result["folders"]), 0)
        self.assertGreater(len(result["files"]), 0)

        # 每个文件都应该有合法的 hash、mtime 和 kind
        for f in result["files"]:
            self.assertTrue(f["hash"].startswith("sha256:"))
            self.assertGreater(f["mtime"], 0)
            self.assertIn(f["kind"], ("page", "file"))
            if f["rel_path"].endswith(".md"):
                self.assertEqual(f["kind"], "page")
            else:
                self.assertEqual(f["kind"], "file")

    def test_plan_full_sync_real_vault(self):
        """对真实 vault 执行全量同步预览（dry_run，不调用 API）"""
        config = {
            "target_space_id": self.TARGET_SPACE_ID,
            "target_folder_entry_id": self.TARGET_FOLDER_ID,
            "exclude_patterns": [".obsidian/**", "*.canvas"],
        }
        report, manifest = do_sync(
            self.VAULT_PATH, config, mode="full", source_dirs=[], dry_run=True
        )

        self.assertEqual(report.mode, "full")
        self.assertTrue(report.dry_run)
        self.assertEqual(report.target_space_id, self.TARGET_SPACE_ID)
        # 真实 vault 应有文档
        self.assertGreater(report.stats["pages_created"], 0)
        self.assertEqual(report.stats["errors"], 0)

        # 输出摘要供人工查看
        print(f"\n=== Real Vault Full Sync (dry-run) ===")
        print(f"  Folders: {report.stats['folders_created']}")
        print(f"  Pages:   {report.stats['pages_created']}")

    def test_converter_on_real_files(self):
        """对真实 vault 中的文件测试 converter"""
        att_folder = get_obsidian_attachment_folder(self.VAULT_PATH)
        errors = []

        scan_result = scan_vault(self.VAULT_PATH, [], [".obsidian/**", "*.canvas"])
        # converter 仅作用于 markdown（kind=="page"）；二进制文件（kind=="file"，
        # 如图片/PDF）走文件上传通道，不应被当文本读取
        md_files = [f for f in scan_result["files"] if f.get("kind", "page") == "page"]
        for f in md_files[:10]:  # 只测前 10 个 markdown 文件
            try:
                result = convert_file(f["abs_path"], self.VAULT_PATH, att_folder)
                # 转换后不应包含 wikilink
                if "![[" in result.content:
                    errors.append(f"{f['rel_path']}: still contains ![[...]]")
            except Exception as e:
                errors.append(f"{f['rel_path']}: {e}")

        if errors:
            self.fail(f"Converter errors:\n" + "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
