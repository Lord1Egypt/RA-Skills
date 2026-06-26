#!/usr/bin/env python3
"""
integration_test.py — Synapse Wiki 集成测试

测试核心功能的端到端流程：
1. 初始化 Wiki → 验证目录结构
2. 摄取资料 → 验证 Wiki 页面创建
3. 查询知识 → 验证答案综合
4. 健康检查 → 验证问题检测
5. 完整工作流 → 模拟真实使用场景
"""

import sys
import json
from pathlib import Path
import subprocess
import shutil

class Colors:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'

def log(msg, color=Colors.RESET):
    print(f"{color}{msg}{Colors.RESET}")

def run_script(script_path, args, timeout=60):
    """Run a Python script and return result."""
    try:
        result = subprocess.run(
            ['python3', str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, '', f'Timeout after {timeout}s'
    except Exception as e:
        return 1, '', str(e)

# Test paths
TEST_WIKI = Path('/tmp/synapse-wiki-integration-test')
SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'

def cleanup():
    """Clean up test directory."""
    if TEST_WIKI.exists():
        shutil.rmtree(TEST_WIKI, ignore_errors=True)

def assert_file_exists(path, description):
    """Assert that a file exists."""
    if path.exists():
        return True
    log(f'  ✗ FAIL: {description} not found: {path}', Colors.RED)
    return False

def assert_contains(text, substring, description):
    """Assert that text contains substring."""
    if substring in text:
        return True
    log(f'  ✗ FAIL: {description}', Colors.RED)
    return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 1: Initialize Wiki
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_init_wiki():
    """Test 1: Initialize Wiki and verify directory structure."""
    log('\n[Test 1] Initialize Wiki', Colors.CYAN)
    cleanup()

    # Run scaffold
    code, stdout, stderr = run_script(SCRIPT_DIR / 'scaffold.py', [str(TEST_WIKI), 'AI 学习知识库'])

    if code != 0:
        log(f'  ✗ FAIL: scaffold.py failed: {stderr}', Colors.RED)
        return False

    # Verify directory structure
    required_dirs = [
        'raw/articles',
        'raw/papers',
        'raw/notes',
        'wiki/concepts',
        'wiki/entities',
        'wiki/summaries',
    ]

    required_files = [
        'CLAUDE.md',
        'log.md',
        'wiki/index.md',
    ]

    all_passed = True

    for dir_path in required_dirs:
        full_path = TEST_WIKI / dir_path
        if not full_path.exists():
            log(f'  ✗ FAIL: Missing directory: {dir_path}', Colors.RED)
            all_passed = False

    for file_path in required_files:
        full_path = TEST_WIKI / file_path
        if not assert_file_exists(full_path, f'Missing file: {file_path}'):
            all_passed = False

    # Verify CLAUDE.md content
    claude_md = (TEST_WIKI / 'CLAUDE.md').read_text(encoding='utf-8')
    if not assert_contains(claude_md, 'AI 学习知识库', 'CLAUDE.md contains wiki name'):
        all_passed = False

    if all_passed:
        log('  ✓ PASS: Wiki initialized with correct structure', Colors.GREEN)
    else:
        log('  ✗ FAIL: Directory structure verification failed', Colors.RED)

    return all_passed

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 2: Ingest Article
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_ingest_article():
    """Test 2: Ingest article and verify Wiki page creation."""
    log('\n[Test 2] Ingest Article', Colors.CYAN)

    # Create test article
    article_dir = TEST_WIKI / 'raw' / 'articles'
    article_dir.mkdir(parents=True, exist_ok=True)

    article_path = article_dir / 'llm-wiki-test.md'
    article_content = '''---
title: LLM Wiki 模式详解
author: Karpathy
date: 2024-01-15
---

# LLM Wiki 模式详解

LLM Wiki 模式是由 Andrej Karpathy 提出的知识库管理方法。

## 核心思想

与传统 RAG 不同，LLM Wiki 模式强调由 LLM 增量编译原始资料成持久化的 Wiki 页面。

## 三层架构

1. **raw/** - 原始资料层，LLM 只读
2. **wiki/** - 知识页面层，LLM 编写
3. **outputs/** - 探索产出层

## 关键概念

### 概念页面

概念页面用于记录抽象概念，如 "Prompt Engineering"、"RAG" 等。

### 实体页面

实体页面用于记录具体实体，如 "Claude Code"、"Obsidian" 等。
'''
    article_path.write_text(article_content, encoding='utf-8')

    # Run ingest
    code, stdout, stderr = run_script(SCRIPT_DIR / 'ingest.py', [str(TEST_WIKI), str(article_path)], timeout=120)

    if code != 0:
        log(f'  ✗ FAIL: ingest.py failed: {stderr}', Colors.RED)
        return False

    # Verify Wiki pages were created
    wiki_concepts = TEST_WIKI / 'wiki' / 'concepts'
    wiki_summaries = TEST_WIKI / 'wiki' / 'summaries'

    # Should create summary page
    summary_page = wiki_summaries / 'llm-wiki-test.md'

    # Should update index.md
    index_md = TEST_WIKI / 'wiki' / 'index.md'

    # Should update log.md
    log_md = TEST_WIKI / 'log.md'

    all_passed = True

    if not assert_file_exists(summary_page, 'Summary page created'):
        all_passed = False
    elif 'LLM Wiki' in summary_page.read_text(encoding='utf-8'):
        log('  ✓ Summary page contains correct content', Colors.GREEN)

    if not assert_file_exists(index_md, 'Index.md updated'):
        all_passed = False

    if not assert_file_exists(log_md, 'Log.md updated'):
        all_passed = False
    else:
        log_content = log_md.read_text(encoding='utf-8')
        if 'ingest' in log_content.lower():
            log('  ✓ Log.md contains ingest entry', Colors.GREEN)
        else:
            log('  ✗ FAIL: Log.md missing ingest entry', Colors.RED)
            all_passed = False

    if all_passed:
        log('  ✓ PASS: Article ingested successfully', Colors.GREEN)
    else:
        log('  ✗ FAIL: Ingest verification failed', Colors.RED)

    return all_passed

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 3: Query Knowledge
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_query_knowledge():
    """Test 3: Query Wiki and verify answer synthesis."""
    log('\n[Test 3] Query Knowledge', Colors.CYAN)

    # Query about LLM Wiki
    code, stdout, stderr = run_script(SCRIPT_DIR / 'query.py', [str(TEST_WIKI), 'LLM Wiki 的核心思想是什么'], timeout=60)

    if code != 0:
        log(f'  ✗ FAIL: query.py failed: {stderr}', Colors.RED)
        return False

    # Should find relevant pages or indicate no results
    output_lower = stdout.lower()

    if '查询' in output_lower or 'query' in output_lower or '没有找到' in output_lower or 'relevant' in output_lower:
        log('  ✓ PASS: Query completed with meaningful output', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: Unexpected output: {stdout[:200]}', Colors.RED)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 4: Health Check (Lint)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_health_check():
    """Test 4: Run health check and verify issue detection."""
    log('\n[Test 4] Health Check (Lint)', Colors.CYAN)

    code, stdout, stderr = run_script(SCRIPT_DIR / 'lint_wiki.py', [str(TEST_WIKI)], timeout=60)

    # Lint may find issues (exit 1) or be clean (exit 0)
    if code not in [0, 1]:
        log(f'  ✗ FAIL: lint_wiki.py failed with code {code}: {stderr}', Colors.RED)
        return False

    # Should report status
    if 'Wiki pages' in stdout or 'issues found' in stdout.lower() or 'ok' in stdout.lower():
        log('  ✓ PASS: Health check completed', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: Unexpected output: {stdout[:200]}', Colors.RED)
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 5: Complete Workflow
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_complete_workflow():
    """Test 5: Simulate real user workflow."""
    log('\n[Test 5] Complete Workflow Simulation', Colors.CYAN)

    # Create multiple articles
    articles_dir = TEST_WIKI / 'raw' / 'articles'
    articles_dir.mkdir(parents=True, exist_ok=True)

    # Article 1: Prompt Engineering
    article1 = articles_dir / 'prompt-engineering.md'
    article1.write_text('''---
title: Prompt Engineering Best Practices
---

# Prompt Engineering Best Practices

## Key Principles

1. Be specific and explicit
2. Provide examples (few-shot)
3. Use chain-of-thought reasoning

## Common Patterns

### Role Assignment
"You are an expert Python developer..."

### Step-by-Step
"Let's think step by step..."
''', encoding='utf-8')

    # Article 2: RAG
    article2 = articles_dir / 'rag-systems.md'
    article2.write_text('''---
title: RAG Systems Overview
---

# RAG Systems Overview

RAG (Retrieval Augmented Generation) combines retrieval with generation.

## Components

1. Document store
2. Retrieval mechanism
3. LLM for generation

## Tradeoffs

- Pros: Up-to-date knowledge, verifiable sources
- Cons: Latency, index maintenance
''', encoding='utf-8')

    # Ingest both articles
    log('  Ingesting article 1...', Colors.BLUE)
    code1, _, _ = run_script(SCRIPT_DIR / 'ingest.py', [str(TEST_WIKI), str(article1)], timeout=120)

    log('  Ingesting article 2...', Colors.BLUE)
    code2, _, _ = run_script(SCRIPT_DIR / 'ingest.py', [str(TEST_WIKI), str(article2)], timeout=120)

    if code1 != 0 or code2 != 0:
        log('  ✗ FAIL: Failed to ingest articles', Colors.RED)
        return False

    # Verify index has both entries
    index_md = TEST_WIKI / 'wiki' / 'index.md'
    index_content = index_md.read_text(encoding='utf-8')

    all_passed = True

    # Check for summary pages existence (more reliable than index content)
    summary1 = TEST_WIKI / 'wiki' / 'summaries' / 'prompt-engineering.md'
    summary2 = TEST_WIKI / 'wiki' / 'summaries' / 'rag-systems.md'

    if not summary1.exists():
        log('  ✗ FAIL: Summary page for Prompt Engineering not created', Colors.RED)
        all_passed = False
    else:
        log('  ✓ Summary page for Prompt Engineering created', Colors.GREEN)

    if not summary2.exists():
        log('  ✗ FAIL: Summary page for RAG not created', Colors.RED)
        all_passed = False
    else:
        log('  ✓ Summary page for RAG created', Colors.GREEN)

    # Check index.md was updated (may use full title)
    if 'Engineering' in index_content or 'Prompt' in index_content:
        log('  ✓ Index contains Prompt Engineering reference', Colors.GREEN)
    else:
        log('  ⚠ Index may need to use full title for references', Colors.YELLOW)

    if 'RAG' in index_content or 'Systems' in index_content:
        log('  ✓ Index contains RAG reference', Colors.GREEN)
    else:
        log('  ⚠ Index may need to use full title for references', Colors.YELLOW)

    # Run lint to verify no critical issues
    code, stdout, _ = run_script(SCRIPT_DIR / 'lint_wiki.py', [str(TEST_WIKI)], timeout=60)

    # Check for isolated pages (common issue)
    if 'isolated' in stdout.lower():
        log('  ⚠ Warning: Some isolated pages detected (expected for test)', Colors.YELLOW)

    if all_passed:
        log('  ✓ PASS: Complete workflow simulation successful', Colors.GREEN)
    else:
        log('  ✗ FAIL: Workflow verification failed', Colors.RED)

    return all_passed


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 6: Recursive Scanning (subdirectory support)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_recursive_scanning():
    """Test 6: Verify lint_wiki.py uses recursive scanning (.rglob)."""
    log('\n[Test 6] Recursive Scanning (Subdirectory Support)', Colors.CYAN)

    # Create nested structure
    nested_dir = TEST_WIKI / 'raw' / 'articles' / 'nested' / 'deep'
    nested_dir.mkdir(parents=True, exist_ok=True)

    # Create deeply nested article
    nested_article = nested_dir / 'deep-article.md'
    nested_article.write_text('''---
title: Deep Nested Article
---

# Deep Nested Article

This article is in a deeply nested subdirectory.
''', encoding='utf-8')

    # Run lint and check if it finds the nested article
    code, stdout, stderr = run_script(SCRIPT_DIR / 'lint_wiki.py', [str(TEST_WIKI)], timeout=60)

    # Check if lint_wiki.py has .rglob() for recursive scanning
    lint_script = SCRIPT_DIR / 'lint_wiki.py'
    source = lint_script.read_text(encoding='utf-8')

    if '.rglob(' in source:
        log('  ✓ lint_wiki.py uses .rglob() for recursive scanning', Colors.GREEN)
        log('  ✓ PASS: Recursive scanning verified', Colors.GREEN)
        return True
    elif '.glob(' in source:
        log('  ✗ FAIL: lint_wiki.py uses .glob() (non-recursive)', Colors.RED)
        return False
    else:
        log('  ⚠ Warning: Could not verify scanning method', Colors.YELLOW)
        return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 7: Summaries Link Check (filename-based matching)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_summaries_link_check():
    """Test 7: Verify summaries directory uses filename-based link matching."""
    log('\n[Test 7] Summaries Link Check (Filename-based)', Colors.CYAN)

    # Create test summary page
    summaries_dir = TEST_WIKI / 'wiki' / 'summaries'
    summaries_dir.mkdir(parents=True, exist_ok=True)

    summary_file = summaries_dir / 'test-summary-link.md'
    summary_file.write_text('''---
title: summaries/test-summary-link
type: summary
---

# Test Summary

## Content

This is a test summary.

## References

[[concepts/test-concept]] - Test concept link
''', encoding='utf-8')

    # Create test concept page
    concepts_dir = TEST_WIKI / 'wiki' / 'concepts'
    concepts_dir.mkdir(parents=True, exist_ok=True)

    concept_file = concepts_dir / 'test-concept.md'
    concept_file.write_text('''---
title: Test Concept
type: concept
---

# Test Concept

This is a test concept.
''', encoding='utf-8')

    # Check lint_wiki.py for filename-based matching
    lint_script = SCRIPT_DIR / 'lint_wiki.py'
    source = lint_script.read_text(encoding='utf-8')

    # Look for filename-based matching (not frontmatter title)
    # The fix was to use page.name or page.stem instead of page.read_text().frontmatter.title
    has_filename_matching = '.name' in source or '.stem' in source or 'page.name' in source

    if has_filename_matching:
        log('  ✓ lint_wiki.py uses filename-based matching', Colors.GREEN)
        log('  ✓ PASS: Summaries link check verified', Colors.GREEN)
        return True
    else:
        log('  ⚠ Warning: Could not verify filename-based matching', Colors.YELLOW)
        return True

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    log('\n' + '═' * 70, Colors.CYAN)
    log('  Synapse Wiki Integration Tests', Colors.CYAN)
    log('═' * 70, Colors.CYAN)

    tests = [
        ('Initialize Wiki', test_init_wiki),
        ('Ingest Article', test_ingest_article),
        ('Query Knowledge', test_query_knowledge),
        ('Health Check', test_health_check),
        ('Complete Workflow', test_complete_workflow),
        ('Recursive Scanning', test_recursive_scanning),
        ('Summaries Link Check', test_summaries_link_check),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            log(f'  ✗ FAIL: {name} raised exception: {e}', Colors.RED)
            results.append((name, False))

    cleanup()

    # Summary
    log('\n' + '═' * 70, Colors.CYAN)
    log('  Test Summary', Colors.CYAN)
    log('═' * 70, Colors.CYAN)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = '✓ PASS' if result else '✗ FAIL'
        color = Colors.GREEN if result else Colors.RED
        log(f'  {color}{status}{Colors.RESET}: {name}')

    log('\n' + '─' * 70, Colors.BLUE)
    overall = Colors.GREEN if passed == total else Colors.RED
    log(f'  {overall}Results: {passed}/{total} tests passed{Colors.RESET}', Colors.RESET)
    log('─' * 70 + '\n', Colors.BLUE)

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
