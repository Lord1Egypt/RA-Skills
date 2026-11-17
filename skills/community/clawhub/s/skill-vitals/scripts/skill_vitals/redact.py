"""Pure path and optional identifier redaction."""

import os
import re


SKILL_NAME_KEYS = frozenset({"name", "dir_name", "skill", "at_risk_skills"})
PLUGIN_NAME_KEYS = frozenset({"namespace"})
PLUGIN_KEY_KEYS = frozenset({"plugin_key", "enabled_plugins"})
# 宿主实例名。instance_id = Path(instance_root).name —— 用户机器上的目录名，
# 常常就是工作区或客户项目的名字，与 skill 名同一性质。
# 收集它之后，instance_root / config_path / conflict_domain 里嵌着的同一串
# 会被后面的单遍替换一起清掉，不必逐个字段列举。
INSTANCE_NAME_KEYS = frozenset({"instance_id"})


def redact(obj, names=False, name_map=None, home_n="", cwd_n=""):
    """把输出里的可识别信息去掉，让用户能安全地把报告贴到 issue / 群里。

    体检结果最自然的用途就是拿去问人，所以必须提供一个能安全外发的形态。
    - 路径：home 目录 -> `~`，当前目录 -> `.`，兜底再抹一次用户名
    - 名称（可选）：skill 名往往泄露业务上下文（客户名、项目代号、研究方向），
      换成稳定编号后报告结构仍可读，但不再暴露你在做什么
    """
    user = os.path.basename(home_n.rstrip("/")) or ""

    def fix_str(s):
        for src, dst in ((home_n, "~"), (cwd_n, ".")):
            if src:
                s = s.replace(src, dst).replace(src.replace("/", "\\"), dst)
        if user:
            s = re.sub(r"(?i)(?<=[/\\])" + re.escape(user) + r"(?=[/\\]|$)", "<user>", s)
        return s

    # 第一遍：收集所有名字，建立稳定映射。
    # 必须先收集完再替换 —— 名字会同时出现在 name 字段和 path 字段里，
    # 只改字段不改路径等于没脱敏（`~/.claude/skills/<真名>` 照样泄露）。
    if names and name_map is not None:
        def alias(prefix):
            n = sum(1 for v in name_map.values() if v.startswith(prefix)) + 1
            return "%s-%03d" % (prefix, n)

        def collect(o, key=None):
            if isinstance(o, dict):
                for k, v in o.items():
                    collect(v, k)
            elif isinstance(o, list):
                # 列表元素继承父键：removed_skills 里是一串裸名字符串
                for v in o:
                    collect(v, key)
            elif isinstance(o, str) and o:
                if key in SKILL_NAME_KEYS:
                    name_map.setdefault(o, alias("skill"))
                elif key in PLUGIN_NAME_KEYS:
                    name_map.setdefault(o, alias("plugin"))
                elif key in INSTANCE_NAME_KEYS:
                    name_map.setdefault(o, alias("instance"))
                elif key in PLUGIN_KEY_KEYS and "@" in o:
                    # `<plugin>@<marketplace>` —— 两段都要脱敏。
                    # marketplace 常常直接就是公司名或团队名。
                    plug, _, mkt = o.partition("@")
                    if plug:
                        name_map.setdefault(plug, alias("plugin"))
                    if mkt:
                        name_map.setdefault(mkt, alias("market"))
        collect(obj)
        # 长名优先，避免短名先命中造成部分替换
        ordered = sorted(name_map.items(), key=lambda kv: -len(kv[0]))
    else:
        ordered = []

    # 一次扫过、不回头：用交替正则一遍替换完，替换产生的别名不会再被后续
    # 规则命中。曾经是 for real, alias: s = s.replace(...) 的顺序替换 ——
    # 只要有一个真名是别名的子串（比如 skill 名叫 "in"，别名 "plugin-001"），
    # 就会把已经脱敏好的部分再改一次，结果既错又不可预测。
    # 交替顺序即 ordered 的顺序（长名在前），Python 的交替是最左优先。
    name_re = re.compile("|".join(re.escape(r) for r, _ in ordered)) if ordered else None
    alias_of = dict(ordered)

    def walk(o, key=None):
        if isinstance(o, dict):
            return {k: walk(v, k) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v, key) for v in o]
        if isinstance(o, str):
            # description 是自由文本，可能含真名、雇主、客户名、项目代号。
            # 这类内容无法靠模式匹配清除，只能整体丢弃。
            # 预算数字在脱敏前就算好了，丢正文不影响任何统计。
            if names and key == "description":
                return "<redacted: %d chars>" % len(o)
            s = fix_str(o)
            if name_re is not None:
                s = name_re.sub(lambda m: alias_of[m.group(0)], s)
            return s
        return o

    return walk(obj)
