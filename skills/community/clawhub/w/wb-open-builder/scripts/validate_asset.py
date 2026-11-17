#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wb-open-builder 资产包规范校验脚本
校验 WorkBuddy 开放平台四类资产包（skill / connector / expert / team）的结构与字段规范。

用法:
    python scripts/validate_asset.py <资产包目录> --type <skill|connector|expert|team>

输出: 逐项 [PASS]/[FAIL]/[WARN] + 汇总；存在 FAIL 时退出码为 1，否则 0。
依赖: 仅 Python 3.8+ 标准库。
说明: FAIL 为必须修复项；WARN 为建议核对项（部分对应官方示例自身未满足的软性规则）。
Buddy 应用为网页端配置，不走本脚本，按 templates/buddy-app-config-checklist.md 人工核对。
"""
import argparse
import json
import re
import sys
from pathlib import Path

EXPERT_CATEGORIES = {
    "01-ProductDesign", "02-Engineering", "03-GameSpatial", "04-DataAI",
    "05-MarketingGrowth", "06-ContentCreative", "07-SalesCommerce",
    "08-FinanceInvestment", "09-OperationsHR", "10-ProjectQuality",
    "11-SecurityCompliance", "12-IndustryConsultant", "13-TencentZone",
    "14-WorldWise", "15-Education",
}

SECRET_PATTERNS = [
    (r"Bearer\s+[A-Za-z0-9\-_.]{25,}", "疑似硬编码 Bearer Token"),
    (r"sk-[A-Za-z0-9]{16,}", "疑似 API Key（sk- 前缀）"),
    (r"ghp_[A-Za-z0-9]{20,}", "疑似 GitHub Token"),
    (r"AKIA[0-9A-Z]{16}", "疑似 AWS Access Key"),
    (r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}", "疑似 JWT"),
]

results = []  # (level, name, detail)


def add(level, name, detail=""):
    results.append((level, name, detail))


def load_json(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        add("FAIL", f"{path.name} 可读性", f"无法以 UTF-8 读取: {e}")
        return None
    try:
        return json.loads(text)
    except Exception:
        stripped = re.sub(r"^\s*//.*$", "", text, flags=re.M)
        stripped = re.sub(r",(\s*[}\]])", r"\1", stripped)
        try:
            add("WARN", f"{path.name} 格式", "存在注释或尾逗号，已容错解析；建议输出严格 JSON")
            return json.loads(stripped)
        except Exception as e:
            add("FAIL", f"{path.name} JSON 合法性", f"解析失败: {e}")
            return None


def parse_frontmatter(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        add("FAIL", "SKILL.md 可读性", f"无法以 UTF-8 读取: {e}")
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        add("FAIL", "SKILL.md frontmatter", "未找到 YAML frontmatter（需以 --- 开头结尾）")
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith(("'", '"')):
            fm[key.strip().strip("'\"")] = val[1:-1] if len(val) >= 2 and val.endswith(val[0]) else val.strip("'\"")
        else:
            fm[key.strip().strip("'\"")] = re.sub(r"\s+#.*$", "", val).strip()
    return fm


def check_security(root: Path):
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix in {".png", ".jpg", ".svg", ".ico", ".zip"}:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        text = re.sub(r"\$\{[A-Za-z0-9_]+\}", "PLACEHOLDER", text)
        text = re.sub(r"\{\{[A-Za-z0-9_]+\}\}", "PLACEHOLDER", text)
        for pattern, label in SECRET_PATTERNS:
            m = re.search(pattern, text)
            if m:
                add("FAIL", f"安全扫描: {f.relative_to(root)}", f"{label}，请改为 ${{VAR}} 占位符")


def check_skill(root: Path):
    skill_md = None
    for cand in [root / "SKILL.md", root / f"{root.name}" / "SKILL.md"]:
        if cand.is_file():
            skill_md = cand
            break
    if skill_md is None:
        md_files = list(root.rglob("SKILL.md"))
        if md_files:
            skill_md = md_files[0]
            add("WARN", "SKILL.md 位置", f"位于子目录 {skill_md.parent.name}/，确认 zip 根层为技能目录")
    if skill_md is None:
        add("FAIL", "SKILL.md 存在性", "未找到 SKILL.md（技能包唯一必须文件）")
        return
    fm = parse_frontmatter(skill_md)
    if fm is None:
        return
    for field in ["description", "description_zh", "description_en", "version", "author"]:
        if not fm.get(field):
            add("FAIL", f"frontmatter 必填字段 {field}", "缺失或为空")
        else:
            add("PASS", f"frontmatter 必填字段 {field}")
    if fm.get("name") and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", fm["name"]):
        add("WARN", "frontmatter name", "建议 kebab-case（小写字母/数字/连字符）")
    if fm.get("version") and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.]+)?", fm["version"]):
        add("WARN", "frontmatter version", f"{fm['version']} 非语义化版本（建议 x.y.z）")
    for bfield in ("disable-model-invocation", "user-invocable"):
        bv = fm.get(bfield)
        if bv and str(bv).lower() not in ("true", "false"):
            add("WARN", f"frontmatter {bfield}", f"取值 {bv!r} 无效，仅接受 true/false")
    if fm.get("category"):
        add("PASS", "frontmatter category", f"{fm['category']}（须为平台分类之一，以开放平台创建页为准）")
    if fm.get("allowed-tools"):
        add("PASS", "frontmatter allowed-tools", "已声明工具白名单（逗号分隔）")
    body = skill_md.read_text(encoding="utf-8")
    for ref in re.findall(r"@references/[\w./-]+", body):
        p = ref.lstrip("@").rstrip("./")
        if not p or "*" in p:
            continue
        if not (skill_md.parent / p).exists():
            add("FAIL", "子资源引用", f"SKILL.md 以 @references/ 引用的 {p} 不存在")
    pkg_root = skill_md.parent
    for f in pkg_root.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(pkg_root)
        if any(p in {".git", "__pycache__", "node_modules"} for p in rel.parts[:-1]):
            continue
        if len(rel.parts) > 2:
            add("FAIL", "目录层级超限", f"{rel.as_posix()} 超过两级（根目录/二级目录/文件），请移除子目录嵌套")
    subdirs = [d.name for d in pkg_root.iterdir() if d.is_dir()]
    add("PASS", "技能目录子资源", f"子目录: {', '.join(subdirs) if subdirs else '无（允许）'}")


def _localized(v):
    if isinstance(v, dict):
        return v.get("zh"), v.get("en")
    return v, v


def _check_expert_common(root: Path, data: dict, is_team: bool):
    label = "专家团" if is_team else "专家"
    for field in ["name", "expertType", "version", "description", "author", "agents", "agentName"]:
        if field not in data or data[field] in (None, "", [], {}):
            add("FAIL", f"plugin.json 必填字段 {field}", "缺失或为空")
        else:
            add("PASS", f"plugin.json 必填字段 {field}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(data.get("name", ""))):
        add("FAIL", "plugin.json name", "必须为小写字母+连字符")
    expected_type = "team" if is_team else "agent"
    if data.get("expertType") != expected_type:
        add("FAIL", "plugin.json expertType", f'应为 "{expected_type}"，实际 {data.get("expertType")!r}')
    agents = data.get("agents") or []
    agent_files = []
    for p in agents:
        f = root / str(p).lstrip("./")
        if f.is_file():
            agent_files.append(f.name[:-3])
        else:
            add("FAIL", "agents 路径", f"{p} 不存在")
    agent_name = data.get("agentName")
    if agent_name and agent_name not in agent_files:
        add("FAIL", "agentName 一致性", f"{agent_name} 不在 agents 文件名列表 {agent_files} 中")
    for field in ["displayName", "profession", "displayDescription", "defaultInitPrompt"]:
        zh, en = _localized(data.get(field))
        if not zh or not en:
            add("FAIL", f"展示字段 {field}", "zh/en 不完整")
        else:
            add("PASS", f"展示字段 {field}")
    dd_zh = _localized(data.get("displayDescription"))[0] or ""
    if 40 <= len(dd_zh) <= 50:
        add("PASS", "displayDescription 字数", f"中文 {len(dd_zh)} 字（40~50 达标）")
    else:
        add("WARN", "displayDescription 字数", f"中文 {len(dd_zh)} 字，规范要求 40~50（个别官方示例亦超出，请尽量对齐）")
    tags = data.get("tags") or []
    if is_team:
        if not (3 <= len(tags) <= 4):
            add("WARN", "tags 数量", f"{len(tags)} 个；常规 3 个（官方团队示例存在 4 个）")
    elif len(tags) != 3:
        add("FAIL", "tags 数量", f"{len(tags)} 个，规范要求固定 3 个")
    else:
        add("PASS", "tags 数量", "3 个")
    qp = data.get("quickPrompts") or []
    if len(qp) != 3:
        add("FAIL", "quickPrompts 数量", f"{len(qp)} 个，规范要求固定 3 个")
    else:
        add("PASS", "quickPrompts 数量", "3 个")
    if data.get("plugin") != data.get("name"):
        add("FAIL", "plugin 字段", "必须与 name 一致")
    else:
        add("PASS", "plugin 字段", "与 name 一致")
    dip = _localized(data.get("defaultInitPrompt"))[0]
    qp0 = _localized(qp[0])[0] if qp else None
    if dip and qp0 and dip != qp0:
        add("WARN", "defaultInitPrompt 一致性", "规范要求与 quickPrompts 第一条一致（个别官方示例未满足，请尽量对齐）")
    elif dip and qp0:
        add("PASS", "defaultInitPrompt 一致性", "与 quickPrompts 第一条一致")
    cat = data.get("categoryId")
    if cat not in EXPERT_CATEGORIES:
        add("FAIL", "categoryId", f"{cat!r} 不在 15 个枚举值内")
    else:
        add("PASS", "categoryId", cat)
    avatar = data.get("avatar")
    if avatar and not (root / str(avatar)).is_file():
        add("FAIL", "avatar 文件", f"{avatar} 不存在（512×512 PNG，≤500KB）")
    elif avatar:
        add("PASS", "avatar 文件", str(avatar))
    for f in root.rglob("*"):
        if f.is_file() and f.suffix.lower() in {".png", ".jpg"}:
            if f.stat().st_size > 500 * 1024:
                add("WARN", "头像体积", f"{f.relative_to(root)} 超过 500KB")
    check_security(root)


def check_expert(root: Path):
    pj = root / ".codebuddy-plugin" / "plugin.json"
    if not pj.is_file():
        add("FAIL", "plugin.json 位置", "未找到 .codebuddy-plugin/plugin.json")
        return
    data = load_json(pj)
    if data is None:
        return
    _check_expert_common(root, data, is_team=False)


def check_team(root: Path):
    pj = root / ".codebuddy-plugin" / "plugin.json"
    if not pj.is_file():
        add("FAIL", "plugin.json 位置", "未找到 .codebuddy-plugin/plugin.json")
        return
    data = load_json(pj)
    if data is None:
        return
    _check_expert_common(root, data, is_team=True)
    team_info = data.get("teamInfo")
    if not isinstance(team_info, dict) or not team_info.get("leadAgent") or not team_info.get("memberAgents"):
        add("FAIL", "teamInfo", "缺失或缺少 leadAgent/memberAgents")
    else:
        add("PASS", "teamInfo 结构")
    members = data.get("members")
    if not isinstance(members, list) or not members:
        add("FAIL", "members", "缺失或为空")
        members = []
    else:
        add("PASS", "members 存在", f"{len(members)} 名成员")
    leads = [m for m in members if m.get("role") == "lead"]
    if len(leads) != 1:
        add("FAIL", "members 角色", f"role=lead 应恰好 1 个，实际 {len(leads)}")
    agent_names = {Path(str(p)).name[:-3] if str(p).endswith(".md") else Path(str(p)).name
                   for p in (data.get("agents") or [])}
    lead = data.get("teamInfo", {}).get("leadAgent") if isinstance(team_info, dict) else None
    if lead and lead not in agent_names:
        add("FAIL", "leadAgent 一致性", f"{lead} 不在 agents 文件中")
    if lead and lead == "team-lead":
        add("FAIL", "主理人命名", "不可使用通用 team-lead，须加专家团前缀")
    elif lead and data.get("name") and not lead.startswith(str(data.get("name")).split("-")[0]):
        add("WARN", "主理人命名", f"{lead} 建议包含团队名前缀")
    for m in members:
        mid = m.get("id")
        for field in ["name", "profession", "avatar", "role"]:
            if not m.get(field):
                add("FAIL", f"成员 {mid} 字段 {field}", "缺失或为空")
        if m.get("role") not in ("lead", "member"):
            add("FAIL", f"成员 {mid} role", '必须为 "lead" 或 "member"')
        if mid and mid not in agent_names:
            add("FAIL", f"成员 {mid} 对应 Agent", f"agents/ 中无同名文件")
        if m.get("avatar") and not (root / str(m["avatar"])).is_file():
            add("FAIL", f"成员 {mid} 头像", f"{m['avatar']} 不存在")
    if not (root / "settings.json").is_file():
        add("FAIL", "settings.json", "专家团必带 settings.json（设置主理人；字段以官方模板为准）")
    else:
        add("PASS", "settings.json 存在")


def check_connector(root: Path):
    meta = root / "connector-meta.json"
    if not meta.is_file():
        add("FAIL", "connector-meta.json", "缺失（连接器必须）")
        return
    data = load_json(meta)
    if data is None:
        return
    for field in ["name", "name_en", "description", "description_zh", "description_en", "source"]:
        if not data.get(field):
            add("FAIL", f"meta 必填字段 {field}", "缺失或为空")
        else:
            add("PASS", f"meta 必填字段 {field}")
    src = str(data.get("source", ""))
    if src and not re.fullmatch(r"[a-z0-9-]+", src):
        add("FAIL", "source 格式", "仅允许小写字母、数字、连字符（kebab-case，全局唯一）")
    ctype = data.get("type", "mcp")
    if ctype not in ("mcp", "cli", "skill-only"):
        add("FAIL", "type 取值", f"{ctype!r} 不在 mcp/cli/skill-only")
    for field in ["examples_zh", "examples_en"]:
        vals = data.get(field) or []
        if not (2 <= len(vals) <= 5):
            add("FAIL", field, f"{len(vals)} 条，规范要求 2~5 条")
        else:
            add("PASS", field, f"{len(vals)} 条")
    icon = next((f for f in ["icon.svg", "icon.png", "icon.jpg"] if (root / f).is_file()), None)
    if icon is None:
        add("FAIL", "icon", "未找到 icon.svg/icon.png/icon.jpg")
    else:
        add("PASS", "icon", icon)
    if ctype == "mcp":
        mcp = root / "mcp.json"
        if not mcp.is_file():
            add("FAIL", "mcp.json", "MCP 方案必须提供")
        else:
            cfg = load_json(mcp)
            if cfg is not None:
                servers = cfg.get("mcpServers") or {}
                if len(servers) != 1:
                    add("FAIL", "mcpServers 数量", f"{len(servers)} 个；一个连接器仅配置一个 MCP Server")
                else:
                    add("PASS", "mcpServers 数量", "1 个")
                for name, srv in servers.items():
                    if not isinstance(srv, dict):
                        add("FAIL", f"MCP Server {name}", "配置必须是对象")
                        continue
                    if srv.get("url"):
                        if not str(srv["url"]).startswith("https://"):
                            add("FAIL", f"远程 MCP 协议 {name}", "生产环境必须 HTTPS")
                        else:
                            add("PASS", f"远程 MCP 协议 {name}", "HTTPS")
                        if srv.get("type") not in ("sse", "streamableHttp", None):
                            add("WARN", "type 取值", f"{srv.get('type')!r}；远程建议 sse 或 streamableHttp")
                    elif srv.get("command"):
                        add("PASS", "stdio 本地进程", f"command={srv['command']}")
                    else:
                        add("FAIL", "MCP 连接方式", "既无 url 也无 command")
                    hdrs = srv.get("headers") or {}
                    env = srv.get("env") or {}
                    for k, v in list(hdrs.items()) + list(env.items()):
                        if isinstance(v, str) and "${" not in v and len(v) > 20 and re.search(r"[A-Za-z0-9]{20,}", v):
                            add("WARN", f"凭证占位 {name}.{k}", "疑似字面凭证，建议改为 ${VAR}")
    elif ctype == "cli":
        cli = root / "cli.json"
        if not cli.is_file():
            add("FAIL", "cli.json", "CLI 方案必须提供")
        else:
            cfg = load_json(cli)
            if cfg is not None:
                init = cfg.get("init") or {}
                for plat in ("darwin", "linux", "win32"):
                    if not init.get(plat):
                        add("FAIL", f"init.{plat}", "缺失安装命令")
                if (cfg.get("auth") or cfg.get("unAuth") or cfg.get("status")):
                    for field in ("unAuth", "status"):
                        if cfg.get("auth") and not (cfg.get(field) or {}).get("darwin"):
                            add("FAIL", f"{field} 命令", "有认证时三平台命令必填")
                    if not (cfg.get("statusMatch") or cfg.get("statusMatchJson")):
                        add("FAIL", "statusMatch", "statusMatch / statusMatchJson 二选一必填")
                add("WARN", "CLI 交叉验证", "请在 macOS/Linux/Windows 实测安装、认证、状态、登出全流程")
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        add("PASS", "配套 skills/ 目录", "已提供 AI 使用说明")
    elif ctype == "cli":
        add("WARN", "配套 skills/ 目录", "CLI 方案强烈推荐提供 SKILL.md 使用说明")
    else:
        add("WARN", "配套 skills/ 目录", "MCP 有标准工具描述时可选")
    check_security(root)


def main():
    ap = argparse.ArgumentParser(description="WorkBuddy 开放平台资产包规范校验")
    ap.add_argument("path", help="资产包目录")
    ap.add_argument("--type", required=True, choices=["skill", "connector", "expert", "team"])
    args = ap.parse_args()
    root = Path(args.path)
    if not root.is_dir():
        print(f"[FAIL] 资产包目录不存在: {root}")
        sys.exit(2)
    {"skill": check_skill, "connector": check_connector,
     "expert": check_expert, "team": check_team}[args.type](root)
    n_fail = sum(1 for lv, _, _ in results if lv == "FAIL")
    n_warn = sum(1 for lv, _, _ in results if lv == "WARN")
    n_pass = sum(1 for lv, _, _ in results if lv == "PASS")
    print(f"\n===== 校验报告: {root.name} (type={args.type}) =====")
    for lv, name, detail in results:
        mark = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️ "}[lv]
        line = f"{mark} [{lv}] {name}"
        if detail:
            line += f" — {detail}"
        print(line)
    print(f"----- 汇总: PASS={n_pass}  FAIL={n_fail}  WARN={n_warn} -----")
    if n_fail:
        print("结论: 未通过（存在 FAIL 项，修复后复检）")
        sys.exit(1)
    print("结论: 通过（WARN 项请逐条人工确认）")


if __name__ == "__main__":
    main()
