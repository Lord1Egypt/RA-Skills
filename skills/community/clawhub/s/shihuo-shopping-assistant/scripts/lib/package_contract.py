"""识货购物助手 Skill 包的结构与资源契约校验。"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .frontmatter import FrontmatterError, load_frontmatter


REQUIRED_TOOLS = {
    "search_goods_by_keyword",
    "search_goods_by_image",
    "goods_styles",
    "search_sku",
    "goods_detail",
    "goods_notes",
    "goods_price_trend",
    "goods_sku_price_trend",
    "goods_sku_price_comparision",
    "link_parse",
    "goods_link_query",
    "link_convert",
}
PLATFORM_TOOLS = {"web_search", "mcp__node_repl__js", "Bash", "Read", "Write"}

# 每个场景包只允许三个文件：README 写边界与文件清单，workflow 写流程，output 写回复。
SCENARIO_FILES = ("README.md", "workflow.md", "output.md")
SCENARIOS = (
    "recommendation",
    "price-comparison",
    "link-price-comparison",
    "link-coupon",
)

# 骨架段界定标记。标记之间是逐字输出的用户可见文本，只允许出现语义占位符。
SKELETON_BEGIN = "<!-- 骨架开始 -->"
SKELETON_END = "<!-- 骨架结束 -->"

# 骨架段里不许出现的内部标识：识货工具名和运行时脚本名。
# Bash/Read/Write 是通用英文词，不参与骨架扫描，避免误报。
SKELETON_FORBIDDEN = sorted(
    REQUIRED_TOOLS | {"web_search", "mcp__node_repl__js", "shihuo_api.py"},
    key=len,
    reverse=True,
)

# ID 字段只用于工具调用，不进用户可见文本，因此也不许进骨架段。
ID_FIELDS = (
    "goods_id",
    "goods_style_id",
    "goods_sku_id",
    "style_id",
    "sku_id",
    "sh_goods_id",
    "sh_sku_id",
)

# 已上收到 SKILL.md 全局约束的句子，场景包里不许再写一遍。
UPSTREAMED_PHRASES = (
    "第一行必须以",
    "方括号占位符",
    "命中第一条即停",
    "临近尺码",
    "不写全网最低",
    "shihuo://",
    "质量、真伪",
    "禁止输出工具名",
)

# output.md 的模块标题与章节清单表。
MODULE_HEADING = re.compile(r"^##\s*模块：(.+?)\s*$")
MODULE_LIST_HEADING = "## 章节清单"


@dataclass
class Issue:
    code: str
    path: str
    message: str
    severity: str = "error"

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


@dataclass
class ContractReport:
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add_error(self, code: str, path: str, message: str) -> None:
        self.errors.append(Issue(code, path, message))

    def add_warning(self, code: str, path: str, message: str) -> None:
        self.warnings.append(Issue(code, path, message, "warning"))

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": [item.as_dict() for item in self.errors],
            "warnings": [item.as_dict() for item in self.warnings],
            "summary": self.summary,
        }


def _tool_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("tools", "result", "structuredContent", "data"):
        child = payload.get(key)
        if key == "tools" and isinstance(child, list):
            return [item for item in child if isinstance(item, dict)]
        if isinstance(child, dict):
            found = _tool_list(child)
            if found:
                return found
    return []


def load_tools(path: Path) -> list[dict[str, Any]]:
    try:
        return _tool_list(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError):
        return []


def _parameters(tool: dict[str, Any]) -> dict[str, Any]:
    value = tool.get("parameters")
    if isinstance(value, dict):
        return value
    value = tool.get("inputSchema")
    return value if isinstance(value, dict) else {}


def _tool_names(tools: Iterable[dict[str, Any]]) -> set[str]:
    return {str(item.get("name")) for item in tools if item.get("name")}


def _check_tools(root: Path, report: ContractReport, strict: bool, tools_list: Path | None) -> set[str]:
    path = root / "assets" / "tools.json"
    tools = load_tools(path)
    if not tools:
        report.add_error("invalid_tools_json", "assets/tools.json", "工具镜像缺少非空 tools 数组")
        return set()
    names = _tool_names(tools)
    missing = sorted(REQUIRED_TOOLS - names)
    for name in missing:
        report.add_error("missing_tool", "assets/tools.json", f"工具镜像缺少 Skill 必需工具：{name}")
    for index, tool in enumerate(tools):
        name = tool.get("name") or f"tools[{index}]"
        if not isinstance(tool.get("description"), str) or not tool.get("description"):
            report.add_error("tool_missing_description", f"assets/tools.json:{name}", "工具缺少 description")
        params = _parameters(tool)
        if params.get("type") != "object" or not isinstance(params.get("properties"), dict):
            report.add_error("tool_invalid_parameters", f"assets/tools.json:{name}", "工具参数必须是 object 且包含 properties")
    if tools_list is not None and strict:
        actual = load_tools(tools_list)
        if not actual:
            report.add_error("invalid_tools_list", str(tools_list), "--tools-list 不是可识别的 tools/list 快照")
        elif not names <= _tool_names(actual):
            report.add_error("tool_schema_drift", str(tools_list), "工具镜像包含服务端 tools/list 未提供的工具")
    return names


def _check_frontmatter(root: Path, report: ContractReport, names: set[str]) -> None:
    path = root / "SKILL.md"
    if not path.is_file():
        return
    try:
        data, _ = load_frontmatter(path)
    except FrontmatterError as exc:
        report.add_error("invalid_frontmatter", "SKILL.md", str(exc))
        return
    for key in ("name", "description", "skill_type", "scope", "allowed-tools"):
        if key not in data or data[key] in (None, "", []):
            report.add_error("frontmatter_required", "SKILL.md", f"frontmatter 缺少 {key}")
    if data.get("name") != root.name:
        report.add_error("frontmatter_name", "SKILL.md", "frontmatter.name 必须与目录名一致")
    if data.get("skill_type") != "mcp_interface":
        report.add_error("frontmatter_skill_type", "SKILL.md", "skill_type 必须为 mcp_interface")
    allowed = data.get("allowed-tools")
    if not isinstance(allowed, list):
        report.add_error("allowed_tools_drift", "SKILL.md", "allowed-tools 必须是列表")
    else:
        allowed_set = {str(item) for item in allowed}
        missing = sorted(REQUIRED_TOOLS - allowed_set)
        unknown = sorted(allowed_set - names - PLATFORM_TOOLS)
        if missing:
            report.add_error("allowed_tools_drift", "SKILL.md", f"allowed-tools 缺少 Skill 必需工具：{missing}")
        if unknown:
            report.add_error("allowed_tools_drift", "SKILL.md", f"allowed-tools 包含工具镜像不存在的名称：{unknown}")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("version"), str) or not metadata.get("version"):
        report.add_error("frontmatter_version", "SKILL.md", "metadata.version 必须存在")


def _check_structure(root: Path, report: ContractReport) -> None:
    for required in ("SKILL.md", "README.md", "assets", "references", "scripts/shihuo_api.py"):
        if not (root / required).exists():
            report.add_error("missing_file", required, f"缺少 {required}")
    secret = root / "assets" / "authorization.txt"
    if secret.is_file() and secret.read_text(encoding="utf-8", errors="replace").strip():
        report.add_error(
            "secret_in_package",
            "assets/authorization.txt",
            "包内不得携带 Access Secret，发布前清空或删除该文件",
        )
    for name in REQUIRED_TOOLS:
        if not (root / "references" / "tools" / f"{name}.md").is_file():
            report.add_error("missing_tool_doc", f"references/tools/{name}.md", f"缺少 Skill 必需工具文档 {name}.md")
    scenarios_dir = root / "references" / "scenarios"
    actual_scenarios = {item.name for item in scenarios_dir.iterdir() if item.is_dir()} if scenarios_dir.is_dir() else set()
    if actual_scenarios != set(SCENARIOS):
        report.add_error("scenario_drift", "references/scenarios", f"当前只允许 {sorted(SCENARIOS)}，实际为 {sorted(actual_scenarios)}")
    for scenario in SCENARIOS:
        directory = scenarios_dir / scenario
        relative = f"references/scenarios/{scenario}"
        for filename in SCENARIO_FILES:
            if not (directory / filename).is_file():
                report.add_error("missing_scenario_file", f"{relative}/{filename}", f"缺少场景文件 {filename}")
        if not directory.is_dir():
            continue
        extra = sorted(item.name for item in directory.iterdir() if item.name not in SCENARIO_FILES)
        if extra:
            report.add_error(
                "scenario_file_drift",
                relative,
                f"场景包只允许 {list(SCENARIO_FILES)}，多出：{extra}",
            )


def _table_first_column(lines: list[str]) -> list[str]:
    """取一段 Markdown 表格里每个数据行的第一列。分隔行之前的都是表头。"""
    pending: list[str] = []
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        if set(cells[0]) <= set("-: "):
            pending.clear()
            continue
        pending.append(cells[0])
        values.append(cells[0])
    # 表头行在分隔行之前，pending 清空前累积的那些不是数据行。
    return values[len(values) - len(pending):] if pending else values


def _check_output_modules(root: Path, report: ContractReport) -> None:
    """章节清单引用的模块必须存在，每个模块也必须被清单引用到。"""
    for scenario in SCENARIOS:
        path = root / "references" / "scenarios" / scenario / "output.md"
        if not path.is_file():
            continue
        relative = f"references/scenarios/{scenario}/output.md"
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        defined: list[str] = []
        listed_lines: list[str] = []
        in_list = False
        for line in lines:
            heading = MODULE_HEADING.match(line)
            if heading:
                defined.append(heading.group(1))
                in_list = False
                continue
            if line.strip() == MODULE_LIST_HEADING:
                in_list = True
                continue
            if in_list and line.startswith("## "):
                in_list = False
                continue
            if in_list:
                listed_lines.append(line)
        listed = _table_first_column(listed_lines)
        if not listed:
            report.add_error("missing_module_list", relative, f"缺少“{MODULE_LIST_HEADING}”表或表内没有数据行")
        if not defined:
            report.add_error("missing_module_section", relative, "没有任何“## 模块：<名称>”小节")
        for name in sorted(set(listed) - set(defined)):
            report.add_error("module_not_defined", relative, f"章节清单引用了不存在的模块：{name}")
        for name in sorted(set(defined) - set(listed)):
            report.add_error("module_not_listed", relative, f"模块未被章节清单引用：{name}")
        duplicates = sorted({name for name in defined if defined.count(name) > 1})
        if duplicates:
            report.add_error("module_duplicated", relative, f"模块小节重复定义：{duplicates}")


def _skeleton_spans(text: str) -> list[str]:
    return re.findall(
        re.escape(SKELETON_BEGIN) + r"(.*?)" + re.escape(SKELETON_END),
        text,
        re.DOTALL,
    )


def _check_skeletons(root: Path, report: ContractReport) -> None:
    """骨架段是用户可见文本，不许出现工具名、脚本名和 ID 字段名。"""
    for scenario in SCENARIOS:
        path = root / "references" / "scenarios" / scenario / "output.md"
        if not path.is_file():
            continue
        relative = f"references/scenarios/{scenario}/output.md"
        text = path.read_text(encoding="utf-8", errors="replace")
        spans = _skeleton_spans(text)
        if not spans:
            report.add_error("missing_skeleton_marker", relative, f"没有成对的 {SKELETON_BEGIN} / {SKELETON_END} 标记")
            continue
        if text.count(SKELETON_BEGIN) != text.count(SKELETON_END):
            report.add_error("unbalanced_skeleton_marker", relative, "骨架开始与结束标记数量不一致")
        for span in spans:
            for name in SKELETON_FORBIDDEN:
                if name in span:
                    report.add_error("tool_name_in_skeleton", relative, f"骨架段出现内部标识：{name}")
            for field_name in ID_FIELDS:
                if field_name in span:
                    report.add_error("id_field_in_skeleton", relative, f"骨架段出现 ID 字段名：{field_name}")


def _strip_skeletons(text: str) -> str:
    """去掉骨架段。骨架段是逐字保留的用户可见文案，不受“规则不许重复”约束。"""
    return re.sub(
        re.escape(SKELETON_BEGIN) + r".*?" + re.escape(SKELETON_END),
        "",
        text,
        flags=re.DOTALL,
    )


def _check_upstreamed(root: Path, report: ContractReport) -> None:
    """已上收到 SKILL.md 的句子不许在场景包里再出现。"""
    for scenario in SCENARIOS:
        directory = root / "references" / "scenarios" / scenario
        if not directory.is_dir():
            continue
        for filename in SCENARIO_FILES:
            path = directory / filename
            if not path.is_file():
                continue
            text = _strip_skeletons(path.read_text(encoding="utf-8", errors="replace"))
            relative = f"references/scenarios/{scenario}/{filename}"
            for phrase in UPSTREAMED_PHRASES:
                if phrase in text:
                    report.add_error("upstreamed_phrase", relative, f"该句已上收到 SKILL.md，场景包不再重复：{phrase}")


# 模板里表示“运行时填入真实地址”的链接占位符，不是仓库内的相对引用。
# 按特征匹配而不是穷举字样，避免新增模板文案时漏配白名单。
LINK_PLACEHOLDER = re.compile(r"^\[?(?:识货[^]]*链接|转链后[^]]*)\]?$")


def _is_link_placeholder(target: str) -> bool:
    return bool(LINK_PLACEHOLDER.match(target))


def _check_references(root: Path, report: ContractReport) -> None:
    """只检查 Markdown 相对引用是否存在，不按文案关键词推断流程正确性。"""
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = str(path.relative_to(root))
        for match in re.finditer(r"\]\(([^)]+)\)", text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "#")) or "{" in target or "}" in target:
                continue
            if _is_link_placeholder(target):
                continue
            if not (path.parent / target.split("#", 1)[0]).resolve().is_file():
                report.add_error("broken_reference", relative, f"相对引用不存在：{target}")


def validate_package(root: str | Path, *, strict: bool = False, tools_list: str | Path | None = None) -> ContractReport:
    root_path = Path(root).resolve()
    report = ContractReport()
    if not root_path.is_dir():
        report.add_error("invalid_skill_dir", str(root_path), "Skill 根目录不存在或不是目录")
        return report
    names = _check_tools(root_path, report, strict, Path(tools_list).resolve() if tools_list else None)
    _check_frontmatter(root_path, report, names)
    _check_structure(root_path, report)
    _check_references(root_path, report)
    _check_output_modules(root_path, report)
    _check_skeletons(root_path, report)
    _check_upstreamed(root_path, report)
    report.summary = {"scenarios": len(SCENARIOS), "tools": len(names)}
    return report


__all__ = ["ContractReport", "Issue", "REQUIRED_TOOLS", "SCENARIOS", "validate_package"]
