# -*- coding: utf-8 -*-
"""
静态未定义名检查器 (零依赖, AST 实现)
===================================================================
背景 / 为什么必须有它
-------------------------------------------------------------------
py_compile 与 ast.parse 只做**语法**检查, 对下面这种代码完全放行:

    def f():
        return glob.glob("*")     # 模块顶层没有 import glob -> 运行时才 NameError

2026-08-04 就因为这个: ssq_smart.py 新增 sync_products_to_peers() 里用了
glob, 而 ssq_smart.py 的 `import glob` 其实写在**另一个函数内部**(局部作用域),
语法检查全绿, 直到真实排程跑到那一行才抛 NameError, 把整条流水线拖成退出码 1。

本检查器在**不执行代码**的前提下把这类问题拦在交付前。

设计原则: 宁可漏报, 不可误报 (conservative)
-------------------------------------------------------------------
- 遇到 `from x import *` / `global` / `nonlocal` / `exec/eval` 等无法静态确定
  作用域的情况 -> 直接放弃该模块(标记 skipped), 而不是瞎报。
- 只报告"确定性"未绑定: 该名字不在 内置 / 模块顶层 / 任何外层函数作用域 /
  当前函数局部 / 参数 / 推导式目标 / except as / with as / 类名 中。
- 类体作用域按 Python 真实规则处理(类属性不参与嵌套函数的名字解析)。

用法:
    python check_undefined_names.py            # 检查当前目录 ssq_*.py + run_ssq.py
    python check_undefined_names.py a.py b.py  # 检查指定文件
退出码: 0=全绿, 1=发现确定性未定义名
"""
import ast
import builtins
import os
import sys
import glob as _glob

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BUILTINS = set(dir(builtins)) | {
    '__file__', '__name__', '__doc__', '__spec__', '__package__',
    '__loader__', '__builtins__', '__debug__', '__annotations__',
}


class ScopeCollector(ast.NodeVisitor):
    """收集一个作用域内所有被绑定(赋值/导入/定义)的名字, 不递归进子函数体。"""

    def __init__(self):
        self.bound = set()
        self.unsafe = False          # 遇到 import * / global / nonlocal 等

    # ---- 绑定型语句 ----
    def visit_Assign(self, node):
        for t in node.targets:
            self._bind_target(t)
        self.visit(node.value)

    def visit_AnnAssign(self, node):
        self._bind_target(node.target)
        if node.value:
            self.visit(node.value)

    def visit_AugAssign(self, node):
        self._bind_target(node.target)
        self.visit(node.value)

    def visit_NamedExpr(self, node):        # walrus :=
        self._bind_target(node.target)
        self.visit(node.value)

    def visit_For(self, node):
        self._bind_target(node.target)
        self.generic_visit(node)

    visit_AsyncFor = visit_For

    def visit_With(self, node):
        for item in node.items:
            if item.optional_vars is not None:
                self._bind_target(item.optional_vars)
        self.generic_visit(node)

    visit_AsyncWith = visit_With

    def visit_Import(self, node):
        for a in node.names:
            self.bound.add((a.asname or a.name).split('.')[0])

    def visit_ImportFrom(self, node):
        for a in node.names:
            if a.name == '*':
                self.unsafe = True      # 无法静态确定引入了什么
            else:
                self.bound.add(a.asname or a.name)

    def visit_Global(self, node):
        self.unsafe = True

    def visit_Nonlocal(self, node):
        self.unsafe = True

    def visit_ExceptHandler(self, node):
        if node.name:
            self.bound.add(node.name)
        self.generic_visit(node)

    def visit_Match(self, node):            # py3.10+ 结构化模式匹配, 绑定规则复杂
        self.unsafe = True

    # ---- 定义型: 记名字, 但不进入其体(子作用域另行处理) ----
    def visit_FunctionDef(self, node):
        self.bound.add(node.name)
        for d in node.decorator_list:
            self.visit(d)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.bound.add(node.name)
        for d in node.decorator_list:
            self.visit(d)
        for b in node.bases:
            self.visit(b)

    def visit_Lambda(self, node):
        pass                                 # 子作用域

    def _bind_target(self, t):
        if isinstance(t, ast.Name):
            self.bound.add(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            for e in t.elts:
                self._bind_target(e)
        elif isinstance(t, ast.Starred):
            self._bind_target(t.value)
        # Attribute / Subscript 目标不新增名字


def collect_scope(body_nodes):
    c = ScopeCollector()
    for n in body_nodes:
        c.visit(n)
    return c.bound, c.unsafe


def params_of(node):
    a = node.args
    names = set()
    for x in list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs):
        names.add(x.arg)
    if a.vararg:
        names.add(a.vararg.arg)
    if a.kwarg:
        names.add(a.kwarg.arg)
    return names


class Checker:
    def __init__(self, path):
        self.path = path
        self.problems = []
        self.unsafe = False

    def run(self, tree):
        mod_bound, mod_unsafe = collect_scope(tree.body)
        if mod_unsafe:
            self.unsafe = True
            return
        # 模块顶层的 Name 使用暂不检查(通常是直接可见的), 重点是函数体
        for node in tree.body:
            self._walk_defs(node, [mod_bound])

    def _walk_defs(self, node, scopes):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self._check_function(node, scopes)
        elif isinstance(node, ast.ClassDef):
            # 类体内的名字不参与嵌套函数解析(Python 真实规则)
            for sub in node.body:
                self._walk_defs(sub, scopes)
        else:
            for child in ast.iter_child_nodes(node):
                self._walk_defs(child, scopes)

    def _check_function(self, node, scopes):
        local, unsafe = collect_scope(node.body)
        if unsafe:
            return                       # 该函数放弃检查(保守)
        local |= params_of(node)
        # 推导式 / lambda 内部目标名: 统一收进 local, 避免误报
        for sub in ast.walk(node):
            if isinstance(sub, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for gen in sub.generators:
                    ScopeCollector()._bind_target  # noqa
                    c = ScopeCollector()
                    c._bind_target(gen.target)
                    local |= c.bound
            elif isinstance(sub, ast.Lambda):
                local |= params_of(sub)

        visible = set().union(*scopes) | local | BUILTINS

        # 检查本函数体内直接使用的 Name(Load), 跳过嵌套函数体(它们自己递归检查)
        nested = [n for n in node.body]
        for sub in self._iter_own_body(node):
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                if sub.id not in visible:
                    self.problems.append((sub.lineno, node.name, sub.id))

        # 递归嵌套函数
        for sub in node.body:
            self._walk_defs(sub, scopes + [local])

    def _iter_own_body(self, func):
        """遍历函数体, 但不进入嵌套的 FunctionDef/Lambda/ClassDef 体。"""
        stack = list(func.body)
        while stack:
            n = stack.pop()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                continue
            yield n
            stack.extend(ast.iter_child_nodes(n))


def check_file(path):
    try:
        src = open(path, encoding='utf-8').read()
    except Exception as e:
        return None, f"读取失败: {e}"
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        return None, f"语法错误 line {e.lineno}: {e.msg}"
    ck = Checker(path)
    ck.run(tree)
    if ck.unsafe:
        return 'skipped', None
    return ck.problems, None


def main(argv):
    files = argv[1:]
    if not files:
        here = os.path.dirname(os.path.abspath(__file__)) or '.'
        files = sorted(_glob.glob(os.path.join(here, 'ssq_*.py')))
        for extra in ('run_ssq.py',):
            p = os.path.join(here, extra)
            if os.path.exists(p):
                files.append(p)

    print("=" * 66)
    print("  静态未定义名检查 (AST, 零依赖) — 抓 py_compile 抓不到的 NameError")
    print("=" * 66)

    total_bad = 0
    skipped = []
    for f in files:
        res, err = check_file(f)
        name = os.path.basename(f)
        if err:
            print(f"  ⚠ {name}: {err}")
            continue
        if res == 'skipped':
            skipped.append(name)
            continue
        if res:
            total_bad += len(res)
            print(f"  ❌ {name}: {len(res)} 处疑似未定义")
            for lineno, fn, nm in sorted(res):
                print(f"       line {lineno:>5}  函数 {fn}()  ->  未定义名 '{nm}'")

    print("-" * 66)
    if skipped:
        print(f"  ℹ 跳过(含 import*/global/match 等无法静态判定): {', '.join(skipped)}")
    print(f"  检查文件: {len(files)}  |  确定性未定义名: {total_bad}")
    if total_bad == 0:
        print("  ✅ 未发现确定性未定义名")
    else:
        print("  ⛔ 发现未定义名, 会在运行时抛 NameError, 必须修复!")
    print("=" * 66)
    return 1 if total_bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
