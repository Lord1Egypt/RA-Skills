#!/usr/bin/env python3
"""
test_outline_parser.py - 目录解析器单元测试

⚠️ 隐私警告：docx 样本含学生姓名/学号/研究方向，严禁上传到 GitHub。
默认使用 mock 文本样本。如需验证真实 docx，设置环境变量
MBA_REAL_SAMPLES_DIR 指向本地样本目录，样本自动匿名发现。
详见 tests/REAL_SAMPLES_README.md。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from outline_parser import (
    outline_parse, validate_manual_input,
    extract_outline_from_docx,
    MANUAL_INPUT_TEMPLATE
)


def _discover_real_samples():
    """
    从环境变量 MBA_REAL_SAMPLES_DIR 指定的目录中发现 docx 文件。
    返回 [(idx, full_path), ...]，idx 从 1 开始。
    若环境变量未设置或目录不存在，返回空列表。
    """
    samples_dir = os.environ.get("MBA_REAL_SAMPLES_DIR")
    if not samples_dir or not os.path.isdir(samples_dir):
        return []
    docx_files = sorted(
        f for f in os.listdir(samples_dir)
        if f.lower().endswith(".docx") and not f.startswith("~")
    )
    return [(i + 1, os.path.join(samples_dir, f)) for i, f in enumerate(docx_files)]


# 隐私保护：SAMPLES 列表由环境变量动态发现，默认空。
# 变量名保留 SAMPLES 以兼容既有调用，仅内容为匿名索引。
SAMPLES = _discover_real_samples()


def _run_docx_samples():
    """测试所有 docx 样本"""
    print("=" * 60)
    print("测试 docx 样本解析")
    print("=" * 60)
    
    results = []
    
    for name, path in SAMPLES:
        if not os.path.exists(path):
            print(f"⏭️  跳过 {name}（文件不存在）")
            continue
        
        print(f"\n📄 测试: {name}")
        print(f"   文件: {os.path.basename(path)}（{os.path.getsize(path)//1024} KB）")
        
        tree, issues = extract_outline_from_docx(path)
        
        if not tree:
            print(f"   ❌ 失败: {issues}")
            results.append((name, False, "未解析到章节"))
            continue
        
        l1 = len(tree)
        l2 = sum(len(c["children"]) for c in tree)
        l3 = sum(len(c2["children"]) for c in tree for c2 in c["children"])
        
        # 关键校验：必须7章
        chapter_ok = l1 == 7
        issue_str = ""
        if issues:
            critical = [i for i in issues if i.get("type") in ["L2_duplicate", "no_anchor"]]
            if critical:
                issue_str = f"  ⚠️ 问题: {[i['message'] for i in critical]}"
        
        status = "✅" if chapter_ok else "❌"
        print(f"   {status} 章节数: L1={l1} L2={l2} L3={l3} (期望L1=7)")
        if issue_str:
            print(f"   {issue_str}")
        
        results.append((name, chapter_ok, l1))
    
    return results


def _run_manual_input_validation():
    """测试手动输入验证"""
    print("\n" + "=" * 60)
    print("测试手动输入验证")
    print("=" * 60)
    
    test_cases = [
        # 正确格式
        (
            "正确格式",
            """第1章 绪论
1.1 研究背景
1.1.1 行业背景
1.1.2 研究意义
1.2 研究内容
第2章 理论基础与文献综述
2.1 战略管理理论
2.1.1 企业战略概念
2.1.2 竞争战略理论
2.2 文献综述
第3章 外部环境分析
3.1 PESTEL分析
3.1.1 政治环境
3.1.2 经济环境
3.2 五力模型分析
第4章 内部环境分析
4.1 资源分析
4.2 能力分析
第5章 竞争战略选择""",
            True
        ),
        # 格式错误：章节太少
        (
            "章节太少",
            """第1章 绪论
1.1 研究背景
第2章 理论基础""",
            False
        ),
        # 空输入
        (
            "空输入",
            "",
            False
        ),
        # 格式错误：无编号
        (
            "无编号",
            """这是一些文字
不是目录格式""",
            False
        ),
    ]
    
    results = []
    for name, text, expected_ok in test_cases:
        result = validate_manual_input(text)
        ok = result["ok"] == expected_ok
        status = "✅" if ok else "❌"
        print(f"\n{status} {name}")
        print(f"   输入: {text[:50]}...")
        print(f"   期望: {'成功' if expected_ok else '失败'}")
        print(f"   实际: {'成功' if result['ok'] else '失败 - ' + result.get('error', '')[:40]}")
        results.append((name, ok))
    
    return results


def test_docx_samples():
    """pytest 测试入口：调用 _run_docx_samples"""
    results = _run_docx_samples()
    # 至少跑过
    assert results is not None
    # 至少有一个样本且全部通过（如果有样本的话）
    if results:
        failed = [name for name, ok, *_ in results if not ok]
        assert not failed, f"失败样本: {failed}"


def test_manual_input_validation():
    """pytest 测试入口：调用 _run_manual_input_validation"""
    results = _run_manual_input_validation()
    assert results is not None
    if results:
        failed = [name for name, ok in results if not ok]
        assert not failed, f"失败用例: {failed}"


def test_manual_template():
    """验证手动输入示例模板"""
    print("\n" + "=" * 60)
    print("手动输入模板内容预览")
    print("=" * 60)
    print(MANUAL_INPUT_TEMPLATE[:500] + "...")


def main():
    print("\n🏁 开始目录解析器测试")
    print("")
    
    # 测试 docx 样本
    docx_results = _run_docx_samples()

    # 测试手动输入验证
    manual_results = _run_manual_input_validation()
    
    # 统计
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    docx_pass = sum(1 for _, ok, *_ in docx_results if ok)
    docx_total = len(docx_results)
    print(f"docx样本: {docx_pass}/{docx_total} 通过")
    
    for name, ok, l1 in docx_results:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}: L1={l1}")
    
    manual_pass = sum(1 for _, ok in manual_results if ok)
    manual_total = len(manual_results)
    print(f"\n手动输入验证: {manual_pass}/{manual_total} 通过")
    for name, ok in manual_results:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")
    
    all_pass = docx_pass == docx_total and manual_pass == manual_total
    print(f"\n{'🎉 全部测试通过' if all_pass else '⚠️ 部分测试失败'}")
    
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
