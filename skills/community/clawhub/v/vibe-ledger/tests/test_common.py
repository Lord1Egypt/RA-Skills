from pathlib import Path

import common


def test_norm_ws_collapses_and_nfc():
    assert common.norm_ws("  a\n\t b  ") == "a b"
    assert common.norm_ws("é") == "é"
    assert common.norm_ws(None) == ""


def test_project_id_is_stable_and_path_specific(tmp_path):
    a = tmp_path / "我的 应用"
    a.mkdir()
    b = tmp_path / "other" / "我的 应用"
    b.mkdir(parents=True)
    assert common.project_id(a) == common.project_id(a)
    assert common.project_id(a) != common.project_id(b)
    assert common.project_id(a).startswith("我的-应用-")


def test_workdir_honours_env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    app = tmp_path / "app"
    app.mkdir()
    assert common.project_workdir(app) == tmp_path / "home" / "projects" / common.project_id(app)


def test_is_within(tmp_path):
    root = tmp_path / "app"
    (root / "src").mkdir(parents=True)
    assert common.is_within(root / "src" / "x.ts", root)
    assert common.is_within(root, root)
    assert not common.is_within(tmp_path / "app2" / "x.ts", root)
    assert not common.is_within(tmp_path, root)
    assert not common.is_within("", root)


def test_is_within_follows_symlinks(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real)
    assert common.is_within(link / "a.ts", real)
    assert common.is_within(real / "a.ts", link)


def test_rel_is_posix_relative(tmp_path):
    (tmp_path / "a" / "b").mkdir(parents=True)
    assert common.rel(tmp_path / "a" / "b" / "c.ts", tmp_path) == "a/b/c.ts"


def test_read_jsonl_reports_bad_lines(tmp_path):
    f = tmp_path / "x.jsonl"
    f.write_text('{"a": 1}\nnot json\n\n[1, 2]\n{"b": 2}\n', encoding="utf-8")
    assert list(common.read_jsonl(f)) == [(1, {"a": 1}), (2, None), (4, None), (5, {"b": 2})]


def test_iter_files_skips_dependency_dirs_and_big_files(tmp_path):
    (tmp_path / "node_modules" / "x").mkdir(parents=True)
    (tmp_path / "node_modules" / "x" / "a.js").write_text("x")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "b.ts").write_text("ok")
    (tmp_path / "src" / "big.js").write_bytes(b"a" * (common.MAX_FILE_BYTES + 1))
    assert [p.name for p in common.iter_files(tmp_path, {".js", ".ts"})] == ["b.ts"]


def test_iter_files_skips_nested_checkouts_but_not_the_root(tmp_path):
    # the project root is itself a git repo; a worktree inside it has a `.git` FILE,
    # a nested clone a `.git` FOLDER — both are copies of other code, not this project
    (tmp_path / ".git").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x")
    wt = tmp_path / ".worktrees" / "feature"
    wt.mkdir(parents=True)
    (wt / ".git").write_text("gitdir: /elsewhere/.git/worktrees/feature\n")
    (wt / "a.py").write_text("x")
    clone = tmp_path / "third_party" / "lib"
    clone.mkdir(parents=True)
    (clone / ".git").mkdir()
    (clone / "b.py").write_text("x")
    got = [p.relative_to(tmp_path).as_posix() for p in common.iter_files(tmp_path, {".py"})]
    assert got == ["src/a.py"]


def test_detect_lang_votes_per_message():
    zh = ["帮我做一个记账应用", "只有我自己能看到",
          "Error: permission denied for table notes at line 3 of the migration"]
    assert common.detect_lang(zh) == "zh"
    assert common.detect_lang(["make me a habit tracker", "only I should see my data"]) == "en"
    assert common.detect_lang([]) == "en"
    # short commands do not vote: a Chinese conversation full of "push" stays Chinese
    assert common.detect_lang(["帮我加一个导出按钮", "push", "push", "ok", "push", "再改一下颜色吧"]) == "zh"
    assert common.detect_lang(["push", "ok"]) == "en"


def test_git_ls_files_returns_none_outside_git(tmp_path):
    assert common.git_ls_files(tmp_path) is None


def test_error_patterns():
    assert common.ERROR_LINE.search("ready\nError: permission denied for table notes")
    assert common.ERROR_LINE.search("new row violates row-level security policy")
    assert not common.ERROR_LINE.search("compiled successfully in 2s")
    assert common.USER_ERROR.search("保存的时候报错了")
    assert common.USER_ERROR.search("Access to fetch has been blocked by CORS policy")
    assert not common.USER_ERROR.search("make the button blue")


def test_tool_caches_are_not_project_files(tmp_path):
    (tmp_path / ".remotion" / "chrome" / "res").mkdir(parents=True)
    (tmp_path / ".remotion" / "chrome" / "res" / "content.js").write_text("x", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.ts").write_text("x", encoding="utf-8")
    assert [p.relative_to(tmp_path).as_posix() for p in common.iter_files(tmp_path)] == ["src/a.ts"]
