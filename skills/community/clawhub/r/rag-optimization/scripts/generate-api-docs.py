#!/usr/bin/env python3
"""
generate-api-docs.py — 从源码自动生成 API 文档
用法：
    python scripts/generate-api-docs.py <输出目录>
示例：
    python scripts/generate-api-docs.py references
    # → [OK] 已生成 api_reference.md（完整 API 参考，含签名与 docstring）
    # → [OK] 已生成 api_class_reference.md（类名速查表，符号→真实模块）
    # → [OK] 已生成 api_enums.md（枚举类型汇总）

原理：
    以代码为唯一真相源，通过 import + inspect 反射提取
    类、函数、枚举的签名和 docstring，生成 Markdown 格式 API 文档。
    模块收集规则：优先取模块 __all__ 声明；未声明 __all__ 的模块
    回退为提取"本模块定义的公开类/函数"（排除 re-export 的外来符号）。
"""
import enum
import importlib
import inspect
import pkgutil
import sys
from pathlib import Path
from typing import Any


def _indent(text: str, spaces: int = 2) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in text.split("\n"))


def _format_default(value: Any) -> str:
    if value is inspect.Parameter.empty:
        return ""
    if isinstance(value, str):
        return f' = {value!r}'
    return f" = {value!r}"


def _format_signature(func: Any) -> str:
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return "(签名不可获取)"
    parts = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        annotation = ""
        if param.annotation != inspect.Parameter.empty:
            ann = param.annotation
            ann_str = str(ann)
            if hasattr(ann, "__origin__"):
                ann_str = str(ann).replace("typing.", "")
            annotation = f": {ann_str}"
        default = _format_default(param.default)
        parts.append(f"{name}{annotation}{default}")
    return_annotation = ""
    if sig.return_annotation != inspect.Signature.empty:
        ret = sig.return_annotation
        ret_str = str(ret).replace("typing.", "")
        return_annotation = f" -> {ret_str}"
    return f"({', '.join(parts)}){return_annotation}"


def _extract_class(obj: type) -> list[str]:
    lines = [f"### `{obj.__name__}`", ""]
    doc = inspect.getdoc(obj)
    if doc:
        lines.append(f"*{doc.strip()}*")
        lines.append("")

    # 构造方法
    try:
        sig = inspect.signature(obj.__init__)
        params = [p for p in sig.parameters.values() if p.name != "self"]
        param_parts = []
        for p in params:
            ann = f": {p.annotation}" if p.annotation != inspect.Parameter.empty else ""
            dft = _format_default(p.default)
            param_parts.append(f"{p.name}{ann}{dft}")
        return_type = ""
        if sig.return_annotation != inspect.Signature.empty:
            return_type = f" -> {sig.return_annotation}"
        lines.append(f"- 构造: `{obj.__name__}({', '.join(param_parts)}){return_type}`")
    except (ValueError, TypeError):
        lines.append(f"- 构造: `{obj.__name__}(...)`")

    # 公开方法
    methods = [
        m for m in dir(obj)
        if not m.startswith("_") and callable(getattr(obj, m, None))
    ]
    if methods:
        lines.append("- 方法:")
        for m in methods:
            method = getattr(obj, m)
            try:
                sig = inspect.signature(method)
                params = [p for p in sig.parameters.values() if p.name != "self"]
                param_parts = []
                for p in params:
                    ann = f": {p.annotation}" if p.annotation != inspect.Parameter.empty else ""
                    dft = _format_default(p.default)
                    param_parts.append(f"{p.name}{ann}{dft}")
                ret = ""
                if sig.return_annotation != inspect.Signature.empty:
                    ret = f" -> {sig.return_annotation}"
                lines.append(f"  - `{m}({', '.join(param_parts)}){ret}`")
            except (ValueError, TypeError):
                lines.append(f"  - `{m}(...)`")
    lines.append("")
    return lines


def _extract_enum(obj: type[enum.Enum]) -> list[str]:
    lines = [f"### `{obj.__name__}`", ""]
    doc = inspect.getdoc(obj)
    if doc:
        lines.append(f"*{doc.strip()}*")
        lines.append("")
    members = [(m.name, m.value) for m in obj]
    lines.append(f"成员：{'，'.join(f'`{name} = {value!r}`' for name, value in members)}")
    lines.append("")
    return lines


def _extract_function(obj) -> list[str]:
    lines = [f"### `{obj.__name__}`", ""]
    doc = inspect.getdoc(obj)
    if doc:
        lines.append(f"*{doc.strip()}*")
        lines.append("")
    lines.append(f"- 签名: `{obj.__name__}{_format_signature(obj)}`")
    lines.append("")
    return lines


def _public_names(mod) -> list[str]:
    """返回模块对外公开的符号名。

    规则：声明了 __all__ 的模块以 __all__ 为准；
    未声明 __all__ 的模块回退为提取"本模块定义的公开类/函数"，
    通过 __module__ 比对排除 re-export 的外来符号。
    """
    if hasattr(mod, "__all__"):
        return list(mod.__all__)
    names = []
    for name, obj in vars(mod).items():
        if name.startswith("_"):
            continue
        if not (inspect.isclass(obj) or inspect.isfunction(obj)):
            continue
        if getattr(obj, "__module__", None) != mod.__name__:
            continue
        names.append(name)
    return names


def _iter_package_modules(package_name: str):
    """遍历包及其全部子模块，返回 (模块键, 模块对象) 列表。"""
    pkg = importlib.import_module(package_name)
    modules = [(package_name, pkg)]
    for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__, prefix=f"{package_name}."):
        try:
            modules.append((name, importlib.import_module(name)))
        except ImportError as e:
            print(f"[WARN] 跳过无法导入的模块 {name}: {e}", file=sys.stderr)
    return modules


def _generate_reference(package_name: str) -> str:
    module_paths = []

    for mod_key, mod in _iter_package_modules(package_name):
        for name in _public_names(mod):
            obj = getattr(mod, name, None)
            if obj is None:
                continue
            module_paths.append((mod_key, name, obj))

    # 按模块分组
    from collections import OrderedDict
    grouped: dict[str, list[tuple[str, Any]]] = OrderedDict()
    for mod_key, name, obj in module_paths:
        grouped.setdefault(mod_key, []).append((name, obj))

    lines = [
        f"# {package_name} API 参考文档（自动生成）",
        "",
        "> **本文档由 `scripts/generate-api-docs.py` 自动生成，以代码为唯一真相源**，"
        "人工修改会被下次生成覆盖。",
        "> 若需更新 API 描述，请修改代码 docstring 后重新生成。",
        "",
        "---",
        "",
    ]

    for module_name, items in grouped.items():
        lines.append(f"## `{module_name}`")
        lines.append("")
        for name, obj in sorted(items, key=lambda x: x[0]):
            if isinstance(obj, type) and issubclass(obj, enum.Enum):
                lines.extend(_extract_enum(obj))
            elif isinstance(obj, type):
                lines.extend(_extract_class(obj))
            elif callable(obj):
                lines.extend(_extract_function(obj))
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _generate_class_index(package_name: str) -> str:
    lines = [
        f"# {package_name} 类名速查表（自动生成）",
        "",
        "> **本文档由 `scripts/generate-api-docs.py` 自动生成**，以代码为唯一真相源。",
        "> 列出全部可导入类、枚举与函数及其真实所在模块。",
        "",
        "## 导出符号总表",
        "",
        "| 符号 | 类型 | 真实模块 | 职责/说明 |",
        "|------|------|----------|-----------|",
    ]

    seen_modules = set()

    for mod_key, mod in _iter_package_modules(package_name):
        if mod in seen_modules:
            continue
        seen_modules.add(mod)
        for name in _public_names(mod):
            member = getattr(mod, name, None)
            if member is None:
                continue
            definition_mod = inspect.getmodule(member)
            mod_path = f"{definition_mod.__name__}" if definition_mod else "unknown"
            doc = ""
            if hasattr(member, "__doc__") and member.__doc__:
                doc = str(member.__doc__).strip().split("\n")[0][:60]
            elif inspect.isclass(member):
                doc = member.__name__
            else:
                doc = "-"
            if inspect.isclass(member) and issubclass(member, enum.Enum):
                sym_type = "枚举"
            elif inspect.isclass(member):
                sym_type = "类"
            elif inspect.isfunction(member) or inspect.ismethod(member):
                sym_type = "函数"
            elif isinstance(member, (int, float, str, bool, type(None))):
                sym_type = "常量"
            else:
                sym_type = "-"
            lines.append(f"| `{name}` | {sym_type} | `{mod_path}` | {doc} |")

    return "\n".join(lines)


def _generate_enums(package_name: str) -> str:
    lines = [
        f"# {package_name} 枚举类型汇总（自动生成）",
        "",
        "> **本文档由 `scripts/generate-api-docs.py` 自动生成**，以代码为唯一真相源。",
        "> 枚举与类型定义属于 API 契约，改动枚举值属于破坏性变更。",
        "",
    ]

    found = False
    for mod_key, mod in _iter_package_modules(package_name):
        enums = []
        for name in _public_names(mod):
            obj = getattr(mod, name, None)
            if isinstance(obj, type) and issubclass(obj, enum.Enum):
                enums.append(obj)
        if not enums:
            continue
        found = True
        lines.append(f"## `{mod_key}`")
        lines.append("")
        for e in sorted(enums, key=lambda x: x.__name__):
            lines.extend(_extract_enum(e))
        lines.append("---")
        lines.append("")

    if not found:
        lines.append("（未发现枚举类型）")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/generate-api-docs.py <输出目录>")
        sys.exit(1)
    output_dir = Path(sys.argv[1])
    output_dir.mkdir(parents=True, exist_ok=True)

    # 将技能根目录与 scripts/ 目录均加入 sys.path：
    # - 根目录在 path 中使 `import scripts` 包可导入
    # - scripts/ 目录在 path 中使子模块内部 `from llm_client import ...` 等平铺导入成功
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    for p in (str(project_root), str(script_dir)):
        if p not in sys.path:
            sys.path.insert(0, p)

    # 生成前先确保 scripts 包可导入
    importlib.invalidate_caches()

    ref_doc = _generate_reference("scripts")
    (output_dir / "api_reference.md").write_text(ref_doc, encoding="utf-8")
    print(f"[OK] 已生成 api_reference.md ({len(ref_doc)} 字符)")

    index_doc = _generate_class_index("scripts")
    (output_dir / "api_class_reference.md").write_text(index_doc, encoding="utf-8")
    print(f"[OK] 已生成 api_class_reference.md ({len(index_doc)} 字符)")

    enums_doc = _generate_enums("scripts")
    (output_dir / "api_enums.md").write_text(enums_doc, encoding="utf-8")
    print(f"[OK] 已生成 api_enums.md ({len(enums_doc)} 字符)")


if __name__ == "__main__":
    main()
