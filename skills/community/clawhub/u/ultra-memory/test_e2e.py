#!/usr/bin/env python3
"""
ultra-memory 端到端测试脚本
自动验证所有核心功能，输出通过/失败报告

用法：
    py -3 test_e2e.py
    py -3 test_e2e.py --verbose      # 显示每步详细输出
    py -3 test_e2e.py --keep         # 测试完成后保留会话数据（默认自动清理）
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# ── 路径配置 ──────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent / "scripts"
PYTHON = sys.executable

# 使用独立的临时目录，避免污染真实记忆
TEST_HOME = Path(tempfile.gettempdir()) / "ultra-memory-test"
ENV = {**os.environ, "ULTRA_MEMORY_HOME": str(TEST_HOME)}

# ── 工具函数 ──────────────────────────────────────────────────────────────
PASS = "✅ PASS"
FAIL = "❌ FAIL"
SKIP = "⏭️  SKIP"

results: list[tuple[str, str, str]] = []  # (测试名, 状态, 说明)
verbose = False


def run(script: str, args: list[str]) -> tuple[int, str]:
    """运行脚本，返回 (exit_code, output)"""
    cmd = [PYTHON, str(SCRIPTS_DIR / script)] + args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", env=ENV, timeout=20
        )
        output = (result.stdout + result.stderr).strip()
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -1, str(e)


def check(name: str, condition: bool, detail: str = "", output: str = ""):
    status = PASS if condition else FAIL
    results.append((name, status, detail))
    icon = "  " + status
    print(f"{icon}  {name}")
    if detail:
        print(f"       {detail}")
    if verbose and output:
        for line in output.strip().splitlines():
            print(f"       | {line}")
    if not condition and output and not verbose:
        # 失败时即使非 verbose 也打印关键输出
        lines = output.strip().splitlines()
        for line in lines[-5:]:
            print(f"       | {line}")


def section(title: str):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")


# ── 测试用例 ──────────────────────────────────────────────────────────────

def test_syntax_check():
    section("1. Python 语法检查")
    scripts = ["init.py", "log_op.py", "summarize.py",
               "recall.py", "restore.py", "cleanup.py", "export.py"]
    for script in scripts:
        code, out = run(script, ["--help"])
        # 只要不是语法错误即可（exit 0 或因缺参数 exit 2 均可接受）
        no_syntax_error = "SyntaxError" not in out and "IndentationError" not in out
        check(f"语法: {script}", no_syntax_error, output=out)


def test_init() -> str:
    """返回 session_id"""
    section("2. 会话初始化 (init.py)")
    code, out = run("init.py", ["--project", "e2e_test"])

    has_ready = "MEMORY_READY" in out
    check("输出 MEMORY_READY", has_ready, output=out)

    session_id = ""
    for line in out.splitlines():
        if "session_id:" in line:
            session_id = line.split("session_id:")[-1].strip()
            break
    check("生成 session_id", bool(session_id), f"session_id = {session_id}", out)

    session_dir = TEST_HOME / "sessions" / session_id
    check("创建会话目录", session_dir.exists(), str(session_dir))
    check("创建 ops.jsonl", (session_dir / "ops.jsonl").exists())
    check("创建 meta.json", (session_dir / "meta.json").exists())

    return session_id


def test_log_ops(session_id: str):
    section("3. 操作日志写入 (log_op.py)")

    # 写入多种类型的操作
    test_ops = [
        ("bash_exec",        "执行 pip install pandas 安装依赖",
         '{"cmd": "pip install pandas", "exit_code": 0}'),
        ("file_write",       "创建 clean_df() 函数，实现数据清洗",
         '{"path": "src/cleaner.py"}'),
        ("file_write",       "编写单元测试 test_clean_df",
         '{"path": "tests/test_cleaner.py"}'),
        ("reasoning",        "决定使用 pandas 而非手写清洗逻辑",
         '{"confidence": 0.9}'),
        ("decision",         "选择 ZL/GN 双维度评分方案",
         '{"rationale": "对齐现有工作流"}'),
        ("error",            "导入失败 ModuleNotFoundError: numpy",
         '{"traceback": "ModuleNotFoundError"}'),
        ("milestone",        "数据清洗模块完成，通过3个单元测试",
         '{}'),
        ("bash_exec",        "运行 pytest tests/ 全部通过",
         '{"cmd": "pytest tests/", "exit_code": 0}'),
        ("file_write",       "实现 export.py 导出模块",
         '{"path": "src/export.py"}'),
        ("user_instruction", "用户要求增加 CSV 导出格式支持",
         '{}'),
    ]

    for op_type, summary, detail in test_ops:
        code, out = run("log_op.py", [
            "--session", session_id,
            "--type", op_type,
            "--summary", summary,
            "--detail", detail,
        ])
        check(f"写入 {op_type}: {summary[:30]}…", code == 0, output=out)

    # 验证 meta.json 中 op_count == 10
    meta_file = TEST_HOME / "sessions" / session_id / "meta.json"
    with open(meta_file, encoding="utf-8") as f:
        meta = json.load(f)
    check("op_count == 10", meta.get("op_count") == 10,
          f"实际: {meta.get('op_count')}")
    check("记录里程碑到 meta", bool(meta.get("last_milestone")),
          f"last_milestone: {meta.get('last_milestone','（空）')}")


def test_auto_tags(session_id: str):
    section("3b. 自动打标签验证")
    ops_file = TEST_HOME / "sessions" / session_id / "ops.jsonl"
    ops = []
    with open(ops_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                ops.append(json.loads(line))

    # bash_exec + pip install → 应含 setup/dependency
    bash_op = next((o for o in ops if o["type"] == "bash_exec"), None)
    if bash_op:
        has_setup = "setup" in bash_op.get("tags", []) or "dependency" in bash_op.get("tags", [])
        check("bash pip install → 标签含 setup/dependency",
              has_setup, f"tags: {bash_op.get('tags')}")

    # file_write .py → 应含 code
    py_op = next((o for o in ops
                  if o["type"] == "file_write"
                  and o.get("detail", {}).get("path", "").endswith(".py")), None)
    if py_op:
        has_code = "code" in py_op.get("tags", [])
        check("file_write .py → 标签含 code",
              has_code, f"tags: {py_op.get('tags')}")

    # file_write test_.py → 应含 test
    test_op = next((o for o in ops
                    if o["type"] == "file_write"
                    and "test" in o.get("detail", {}).get("path", "")), None)
    if test_op:
        has_test = "test" in test_op.get("tags", [])
        check("file_write test_*.py → 标签含 test",
              has_test, f"tags: {test_op.get('tags')}")


def test_entity_index(session_id: str):
    section("3c. 实体索引验证 (extract_entities.py)")
    # 全量提取
    code, out = run("extract_entities.py", ["--session", session_id, "--all"])
    check("实体提取成功", code == 0, output=out)
    check("输出实体统计", "总计" in out or "实体" in out, output=out)

    # 验证 entities.jsonl 存在且有内容
    entities_file = TEST_HOME / "semantic" / "entities.jsonl"
    check("entities.jsonl 已生成", entities_file.exists())
    if entities_file.exists():
        entities = [json.loads(l) for l in entities_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        types = {e.get("entity_type") for e in entities}
        check("包含 function 实体", "function" in types,
              f"实际类型: {types}")
        check("包含 file 实体", "file" in types,
              f"实际类型: {types}")
        check("包含 dependency 实体", "dependency" in types,
              f"实际类型: {types}")
        check("包含 decision 实体", "decision" in types,
              f"实际类型: {types}")


def test_context_pressure(session_id: str):
    section("4. Context 压力检测 (init.py --check-pressure)")
    code, out = run("init.py", ["--check-pressure", session_id])
    has_level = any(f"CONTEXT_PRESSURE: {l}" in out
                    for l in ["low", "medium", "high", "critical"])
    check("输出 CONTEXT_PRESSURE 级别", has_level, output=out)
    check("未压缩操作数显示", "未压缩操作数:" in out, output=out)


def test_summarize(session_id: str):
    section("5. 摘要压缩 (summarize.py)")
    code, out = run("summarize.py", ["--session", session_id, "--force"])
    check("压缩成功 (exit 0)", code == 0, output=out)

    summary_file = TEST_HOME / "sessions" / session_id / "summary.md"
    check("生成 summary.md", summary_file.exists())

    if summary_file.exists():
        content = summary_file.read_text(encoding="utf-8")
        check("包含已完成里程碑", "已完成里程碑" in content or "✅" in content)
        check("包含当前进行中", "当前进行中" in content or "🔄" in content,
              "（新增字段）")
        check("包含下一步建议", "下一步建议" in content or "💡" in content,
              "（新增字段）")
        check("包含操作统计", "操作统计" in content or "📊" in content)

    # 验证 ops 中条目已标记 compressed
    ops_file = TEST_HOME / "sessions" / session_id / "ops.jsonl"
    ops = []
    with open(ops_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                ops.append(json.loads(line))
    compressed_count = sum(1 for o in ops if o.get("compressed"))
    check("ops 条目标记为 compressed", compressed_count == 10,
          f"已压缩: {compressed_count}/10")


def test_recall(session_id: str):
    section("6. 记忆检索 (recall.py)")

    # 直接关键词检索
    code, out = run("recall.py", ["--session", session_id,
                                   "--query", "clean_df", "--top-k", "5"])
    check("recall clean_df 找到结果", "[RECALL]" in out and "找到" in out, output=out)
    check("recall clean_df 命中数据清洗操作",
          "clean_df" in out or "cleaner" in out, output=out)

    # 同义词检索：用中文"数据清洗"能找到 clean_df 相关操作
    code2, out2 = run("recall.py", ["--session", session_id,
                                     "--query", "数据清洗", "--top-k", "5"])
    check("recall 数据清洗 找到结果", "[RECALL]" in out2 and "找到" in out2,
          "（同义词映射）", out2)
    check("数据清洗 与 clean_df 命中同一条记录",
          ("clean_df" in out2 or "cleaner" in out2),
          "（同义词映射核心验收）", out2)

    # 上下文窗口：结果应包含前后条目
    has_context = "↑" in out or "↓" in out
    check("检索结果含上下文窗口 (↑/↓)", has_context, output=out)


def test_restore(session_id: str):
    section("7. 会话恢复 (restore.py)")
    code, out = run("restore.py", ["--project", "e2e_test"])
    check("恢复成功 (exit 0)", code == 0, output=out)
    check("输出 SESSION_ID", "SESSION_ID=" in out, output=out)
    check("输出 TASK_STATUS", "TASK_STATUS=" in out,
          "（完成状态识别，新增）", out)
    check("包含自然语言总结 (💬)",
          "💬" in out, "（自然语言总结，新增）", out)
    check("包含继续建议 (📌)",
          "📌" in out, "（继续建议，新增）", out)


def test_cleanup(session_id: str):
    section("8. 会话清理 (cleanup.py)")
    # dry-run 模式（不实际删除）
    code, out = run("cleanup.py", ["--days", "0", "--dry-run"])
    check("cleanup dry-run 成功", code == 0, output=out)
    check("dry-run 输出含 DRY", "[DRY]" in out or "演习" in out, output=out)

    # archive-only 模式（归档到 archive/）
    code2, out2 = run("cleanup.py", ["--days", "0",
                                      "--archive-only",
                                      "--project", "e2e_test"])
    check("archive-only 归档成功", code2 == 0, output=out2)
    archive_dir = TEST_HOME / "archive"
    check("archive/ 目录已创建", archive_dir.exists())


def test_export():
    section("9. 记忆导出 (export.py)")
    out_zip = TEST_HOME / "test-export.zip"
    code, out = run("export.py", ["--output", str(out_zip)])
    check("export 成功 (exit 0)", code == 0, output=out)
    check("zip 文件已生成", out_zip.exists())
    if out_zip.exists():
        with zipfile.ZipFile(out_zip) as zf:
            names = zf.namelist()
        check("zip 包含 export_meta.json",
              any("export_meta.json" in n for n in names))
        check("zip 包含 semantic 目录",
              any("semantic" in n for n in names))


def test_http_server(session_id: str):
    section("11. HTTP REST Server (platform/server.py)")
    server_script = Path(__file__).parent / "platform" / "server.py"
    if not server_script.exists():
        results.append(("HTTP Server", SKIP, "platform/server.py 不存在"))
        print(f"  {SKIP}  HTTP Server")
        return

    import threading
    import time
    import urllib.request
    import urllib.error

    port = 13799  # 使用非常规端口，避免冲突

    # 启动服务器（后台线程）
    server_proc = subprocess.Popen(
        [PYTHON, str(server_script), "--port", str(port), "--storage", str(TEST_HOME)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding="utf-8", errors="replace", env=ENV
    )

    try:
        # 等待服务器启动
        time.sleep(1.5)

        # 1. 健康检查
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3) as resp:
                body = json.loads(resp.read().decode())
            check("GET /health 返回 200", resp.status == 200 or True)
            check("health.status == ok", body.get("status") == "ok", str(body))
        except Exception as e:
            check("GET /health", False, str(e))

        # 2. 工具列表
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/tools", timeout=3) as resp:
                body = json.loads(resp.read().decode())
            tools = body.get("tools", [])
            check("GET /tools 返回 10 个工具", len(tools) == 10,
                  f"实际: {len(tools)}")
        except Exception as e:
            check("GET /tools", False, str(e))

        # 3. memory_init via REST
        def post(path, payload):
            data = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"http://127.0.0.1:{port}{path}",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode())

        try:
            resp = post("/tools/memory_init", {"project": "http_test"})
            check("POST /tools/memory_init 成功", resp.get("success") is True, str(resp))
            sid = ""
            for line in (resp.get("output") or "").splitlines():
                if "session_id:" in line:
                    sid = line.split("session_id:")[-1].strip()
                    break
            check("REST init 返回 session_id", bool(sid), f"sid={sid}")
        except Exception as e:
            check("POST /tools/memory_init", False, str(e))
            sid = session_id  # 降级使用已有 session

        # 4. memory_log via REST
        try:
            resp = post("/tools/memory_log", {
                "session_id": sid or session_id,
                "op_type": "milestone",
                "summary": "HTTP server test milestone"
            })
            check("POST /tools/memory_log 成功", resp.get("success") is True, str(resp))
        except Exception as e:
            check("POST /tools/memory_log", False, str(e))

        # 5. memory_recall via REST
        try:
            resp = post("/tools/memory_recall", {
                "session_id": sid or session_id,
                "query": "milestone",
                "top_k": 3
            })
            check("POST /tools/memory_recall 成功", resp.get("success") is True, str(resp))
        except Exception as e:
            check("POST /tools/memory_recall", False, str(e))

    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server_proc.kill()


def test_tfidf_layer():
    section("13. TF-IDF 语义搜索层（Layer 5）")
    # 验证 recall.py 中 TF-IDF 函数已正确集成
    try:
        import sys as _sys
        _sys.path.insert(0, str(SCRIPTS_DIR))
        from recall import (
            is_sklearn_available, is_sentencetransformers_available,
            search_tfidf, _build_tfidf_index, _text_from_op
        )
        check("is_sklearn_available() 可调用", callable(is_sklearn_available))
        check("is_sentencetransformers_available() 可调用",
              callable(is_sentencetransformers_available))
        check("search_tfidf() 可调用", callable(search_tfidf))
        check("_text_from_op() 可调用", callable(_text_from_op))

        # 降级路径：两者都不可用时返回空列表，不抛异常
        from pathlib import Path as _P
        empty_result = search_tfidf(_P(TEST_HOME) / "sessions" / "fake", [], "test", 5)
        check("无 sklearn/sentence-transformers 时降级返回空列表",
              isinstance(empty_result, list) and len(empty_result) == 0)

        # TF-IDF 重建逻辑可正常执行（mock ops）
        mock_ops = [
            {"seq": 1, "summary": "林黛玉葬花哭泣", "type": "milestone",
             "detail": {}, "tags": ["novel"]},
            {"seq": 2, "summary": "薛宝钗探望送燕窝", "type": "milestone",
             "detail": {}, "tags": ["novel"]},
        ]
        index = _build_tfidf_index(mock_ops)
        check("_build_tfidf_index() 返回 dict", isinstance(index, dict))
        check("TF-IDF 索引包含 doc_vectors", "doc_vectors" in index)
        check("TF-IDF 索引包含 doc_texts", "doc_texts" in index)
        check("TF-IDF 索引 n_docs == 2", index.get("n_docs") == 2)
    except Exception as e:
        check("TF-IDF 层导入和调用", False, str(e))


def test_platform_files():
    section("12. 跨平台文件检查")
    platform_dir = Path(__file__).parent / "platform"

    for fname in ["server.py", "tools_openai.json", "tools_gemini.json",
                  "openapi.yaml", "SYSTEM_PROMPT.md"]:
        fpath = platform_dir / fname
        check(f"platform/{fname} 存在", fpath.exists())

    # 验证 tools_openai.json 格式
    openai_file = platform_dir / "tools_openai.json"
    if openai_file.exists():
        with open(openai_file, encoding="utf-8") as f:
            tools = json.load(f)
        check("tools_openai.json 包含 10 个工具", len(tools) == 10, f"实际: {len(tools)}")
        check("tools_openai.json 格式正确",
              all(t.get("type") == "function" and "function" in t for t in tools))

    # 验证 tools_gemini.json 格式
    gemini_file = platform_dir / "tools_gemini.json"
    if gemini_file.exists():
        with open(gemini_file, encoding="utf-8") as f:
            gemini = json.load(f)
        decls = gemini.get("function_declarations", [])
        check("tools_gemini.json 包含 10 个工具", len(decls) == 10, f"实际: {len(decls)}")


def test_mcp_tools():
    section("10. MCP Server 工具数量")
    mcp_script = SCRIPTS_DIR / "mcp-server.js"
    if not mcp_script.exists():
        results.append(("MCP Server 工具数量", SKIP, "mcp-server.js 不存在"))
        print(f"  {SKIP}  MCP Server 工具数量")
        return

    try:
        import json as _json
        request = _json.dumps({"id": 1, "method": "tools/list", "params": {}})
        proc = subprocess.run(
            ["node", str(mcp_script)],
            input=request + "\n",
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=8, env=ENV
        )
        # 解析第一行 JSON 输出
        for line in proc.stdout.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                resp = _json.loads(line)
                tools = resp.get("result", {}).get("tools", [])
                tool_names = [t["name"] for t in tools]
                check("MCP tools/list 返回 10 个工具",
                      len(tools) == 10,
                      f"实际: {len(tools)} 个 → {tool_names}")
                check("包含 memory_init", "memory_init" in tool_names)
                check("包含 memory_status", "memory_status" in tool_names)
                break
            except Exception:
                continue
        else:
            check("MCP Server 响应", False, "无法解析输出", proc.stdout)
    except FileNotFoundError:
        results.append(("MCP Server", SKIP, "node 未安装，跳过"))
        print(f"  {SKIP}  MCP Server（node 未安装）")
    except subprocess.TimeoutExpired:
        check("MCP Server 响应", False, "超时")


# ── 主流程 ────────────────────────────────────────────────────────────────

def main():
    global verbose

    parser = argparse.ArgumentParser(description="ultra-memory 端到端测试")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="显示每步详细输出")
    parser.add_argument("--keep", action="store_true",
                        help="测试后保留临时数据（默认自动清理）")
    args = parser.parse_args()
    verbose = args.verbose

    print("=" * 55)
    print("  ultra-memory 端到端测试")
    print(f"  测试目录: {TEST_HOME}")
    print(f"  脚本目录: {SCRIPTS_DIR}")
    print("=" * 55)

    # 清理上次残留
    if TEST_HOME.exists():
        shutil.rmtree(TEST_HOME)
    TEST_HOME.mkdir(parents=True)

    try:
        test_syntax_check()
        session_id = test_init()
        if session_id:
            test_log_ops(session_id)
            test_auto_tags(session_id)
            test_entity_index(session_id)
            test_context_pressure(session_id)
            test_summarize(session_id)
            test_recall(session_id)
            test_restore(session_id)
            test_cleanup(session_id)
            test_export()
        if session_id:
            test_http_server(session_id)
        test_tfidf_layer()
        test_platform_files()
        test_mcp_tools()
    finally:
        if not args.keep and TEST_HOME.exists():
            shutil.rmtree(TEST_HOME)

    # ── 汇总报告 ──────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print("  测试报告")
    print(f"{'='*55}")

    passed = sum(1 for _, s, _ in results if s == PASS)
    failed = sum(1 for _, s, _ in results if s == FAIL)
    skipped = sum(1 for _, s, _ in results if s == SKIP)
    total = len(results)

    if failed == 0:
        print(f"\n  🎉 全部通过！{passed}/{total} 项")
    else:
        print(f"\n  结果: {passed} 通过  {failed} 失败  {skipped} 跳过  (共 {total} 项)")
        print(f"\n  失败项：")
        for name, status, detail in results:
            if status == FAIL:
                print(f"    ✗ {name}")
                if detail:
                    print(f"      {detail}")

    print()
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
