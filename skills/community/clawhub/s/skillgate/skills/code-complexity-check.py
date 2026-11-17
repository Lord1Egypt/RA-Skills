#!/usr/bin/env python3
"""
code-complexity-check — 代码复杂度检查 skill。
检查 Python 代码的复杂度——函数太长、嵌套太深等。
"""
import ast
import sys
from pathlib import Path


def check_complexity(filepath: str) -> list:
    """检查 Python 代码复杂度。"""
    findings = []

    content = Path(filepath).read_text(encoding="utf-8")
    tree = ast.parse(content)

    for node in ast.walk(tree):
        # 检查函数长度
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 数一下这个函数有多少行
            if hasattr(node, 'end_lineno') and node.lineno:
                length = node.end_lineno - node.lineno
                if length > 50:
                    findings.append({
                        "line": node.lineno,
                        "severity": "MEDIUM",
                        "message": f"函数 {node.name} 太长了——{length} 行（建议 <50 行）"
                    })

        # 检查嵌套深度
        if isinstance(node, ast.If):
            # 数一下这个 if 里面有多少层嵌套
            depth = 0
            current = node
            while hasattr(current, 'body') and current.body:
                depth += 1
                current = current.body[0] if current.body else None

            if depth > 3:
                findings.append({
                    "line": node.lineno,
                    "severity": "LOW",
                    "message": f"嵌套太深了——{depth} 层（建议 <3 层）"
                })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python code_complexity_check.py <python文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_complexity(filepath)

    if not findings:
        print("✅ 代码复杂度没问题")
        sys.exit(0)

    print(f"发现 {len(findings)} 个问题：")
    for f in findings:
        print(f"  [{f['severity']}] 行 {f['line']}: {f['message']}")

    sys.exit(1 if any(f["severity"] == "HIGH" for f in findings) else 0)


if __name__ == "__main__":
    main()
