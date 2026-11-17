#!/usr/bin/env python3
"""去敏复核 —— 验证发布物不含必须剥离的内部信息（离线，仅标准库）。

检查项：
  - 内部绝对路径（D:/ C:/ /Users/ /home/）
  - 内部项目代号 / 工作区路径片段
  - 明显的内部服务器名 (.internal / .local / .corp)
  - 客户/真实姓名占位（可由 --names 传入额外名单）

用法：
  python desens_check.py --path ./to_publish [--names 张三,李四]
退出码：0=通过，1=发现需去敏项，2=错误
"""
import argparse
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".vault", "venv"}
# 扫描器自身的源文件不参与自审（避免模式字符串自指命中）
SELF_SKIP = {"secret_scan.py", "desens_check.py"}
SCAN_EXT = {".md", ".py", ".js", ".ts", ".json", ".txt", ".yaml", ".yml", ".toml", ".sh", ".bat",
            ".html", ".htm", ".css", ".xml", ".csv", ".ini", ".cfg"}  # noqa: 发布物常见格式，漏了会误判为「无可扫描文件」

# 仅匹配"真实内部路径形态"，避免裸 /c/ /d/ 误命中 URL 或无关文本
PATTERNS = {
    # 左边界 (?<![A-Za-z0-9]) 必不可少：否则 https:// 里的 s:/ 会被当成盘符，
    # 任何含官网/徽章/文档链接的正常发布物都会被误 BLOCK（实测全仓 490 个文件受影响）。
    "绝对路径": re.compile(
        r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/][^\n\r]+|\\\\[\w.$-]+\\[\w.$-]+|/(?:Users|home|root)/[\w.-]+)"),
    # 左边界排除 . 与 -：否则 CSS 复合类选择器（.btn.local / .logo.corp）会被当成内网域名。
    # 必须用 (?:[\w-]+\.)+ 支持多级子域（svc.prod.corp / x.y.z.internal）。
    # 不能用 \b 收尾：Python3 的 \w 含中文，「svc.prod.corp的」不成边界会整体漏检（实测放行过门禁）。
    # 也不能简单排除句点：句末的「svc.prod.corp.」和 CSV 里的「svc.prod.corp.,8080」会漏。
    # 故右侧用两层否定：后面不能紧跟主机名字符，且不能是「点号+主机名字符」。
    "内网域名": re.compile(
        r"(?<![A-Za-z0-9_.-])(?:[A-Za-z0-9-]+\.)+(?:internal|local|corp|lan|intranet|intra|private)"
        r"(?![A-Za-z0-9_-])(?!\.[A-Za-z0-9])",
        re.I),
    # 内网 IP 段：只覆盖 RFC1918 私网与回环，不误伤公网地址
    "内网IP": re.compile(
        r"(?<![\d.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}"
        r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|127\.0\.0\.1)(?![\d.])"),
    "工作区片段": re.compile(r"2026-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}"),
}


def check(text, extra_names):
    hits = []
    for label, pat in PATTERNS.items():
        for m in pat.finditer(text):
            hits.append((label, m.group(0)))
    for name in extra_names:
        if name and name in text:
            hits.append(("真实姓名", name))
    return hits


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path", required=True)
    p.add_argument("--names", default="", help="额外需剥离的真实姓名，逗号分隔")
    a = p.parse_args()
    extra = [n.strip() for n in a.names.split(",") if n.strip()]
    if not os.path.exists(a.path):
        print(f"[BLOCK] 扫描目标不存在：{a.path}，按 fail-closed 处理。")
        sys.exit(2)
    results = []
    errors = []
    root = a.path if os.path.isdir(a.path) else os.path.dirname(os.path.abspath(a.path))
    if os.path.isfile(a.path):
        targets = [a.path]
    else:
        targets = []
        visited = set()

        def _on_walk_error(e):
            # os.walk 默认静默吞掉遍历错误；这里必须记下来，否则漏扫目录会让结论假装通过
            errors.append((getattr(e, 'filename', a.path), "目录遍历失败：%s" % e))

        for r, dirs, files in os.walk(a.path, followlinks=True, onerror=_on_walk_error):
            # followlinks=True 后可能出现回环（sub/loop -> 根），必须按真实路径去重
            rp = os.path.realpath(r)
            if rp in visited:
                dirs[:] = []
                continue
            visited.add(rp)
            # 目录级符号链接：指向扫描根内则正常跟随；指向根外则不跟随并记入未检查项
            # （只对越界链接告警，避免发布目录里一个无害软链就让门禁永久红灯）
            for d in list(dirs):
                full = os.path.join(r, d)
                if not os.path.islink(full):
                    continue
                try:
                    inside = os.path.commonpath([os.path.realpath(full), os.path.realpath(root)]) == os.path.realpath(root)
                except (ValueError, OSError):
                    inside = False
                if not inside:
                    errors.append((full, "目录符号链接指向扫描根之外，未跟随"))
                    dirs.remove(d)
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                fp_full = os.path.join(r, f)
                if os.path.basename(fp_full) in SELF_SKIP:
                    continue
                if os.path.islink(fp_full):
                    # 不跟随符号链接：避免借链接读到扫描目标之外的内部路径
                    errors.append((fp_full, "符号链接，已跳过"))
                    continue
                try:
                    if os.path.commonpath([os.path.realpath(fp_full), os.path.realpath(root)]) != os.path.realpath(root):
                        errors.append((fp_full, "越出扫描根目录"))
                        continue
                except (ValueError, OSError):
                    errors.append((fp_full, "路径解析失败"))
                    continue
                if os.path.splitext(f)[1].lower() in SCAN_EXT:
                    targets.append(fp_full)
        if not targets:
            print("[BLOCK] 去敏复核未能枚举到任何目标文件（路径可能不存在或不含受检扩展名），按 fail-closed 处理。")
            sys.exit(2)
    for fp in targets:
        try:
            # 按字节读再解码：记事本「Unicode」存的是带 BOM 的 UTF-16，
            # 直接用 utf-8 读会得到夹 NUL 的乱码，正则全部失效 → 假 PASS。
            _raw = open(fp, "rb").read()
            if _raw.startswith((b"\xff\xfe", b"\xfe\xff")):
                content = _raw.decode("utf-16", "replace")
            elif _raw.startswith(b"\xef\xbb\xbf"):
                content = _raw.decode("utf-8-sig", "replace")
            else:
                content = _raw.decode("utf-8", "replace")
                if "\x00" in content:
                    # 无 BOM 的 UTF-16：utf-8 能解但不报错，正文被 NUL 拆散，三条正则全部失效
                    # → 会静默判 PASS。无 BOM 时无法可靠判定字节序，两种都解、取命中并集：
                    # 只要任一字节序能命中就拦；都命不中则记为「无法判定」fail-closed，
                    # 绝不能在猜错字节序时对外输出 PASS。
                    cands = []
                    for _enc in ("utf-16-le", "utf-16-be"):
                        try:
                            cand = _raw.decode(_enc, "replace")
                        except (UnicodeDecodeError, ValueError):
                            continue
                        if "\x00" not in cand:
                            cands.append(cand)
                    if cands:
                        content = "\n".join(cands)
                    else:
                        errors.append((fp, "疑似二进制或未知编码，无法判定是否含敏感信息"))
                        continue
        except OSError as e:
            errors.append((fp, "读取失败：%s" % e))
            continue
        for label, snip in check(content, extra):
            results.append((fp, label, snip))
    if errors:
        print(f"[WARN] {len(errors)} 个文件未能检查，本次结论不完整：")
        for fp, why in errors[:10]:
            print(f"  - {fp}  [{why}]")
    if not results:
        if errors:
            print("[BLOCK] 已扫描文件未发现需去敏项，但存在未检查文件，不能判定为可放行。")
            sys.exit(1)
        print("[PASS] 去敏复核通过：未检出内部路径/内网域名/工作区片段/指定姓名。")
        sys.exit(0)
    print(f"[BLOCK] 去敏复核发现 {len(results)} 处需处理：")
    for fp, label, snip in results:
        print(f"  - {fp}  [{label}]  {snip}")
    sys.exit(1)


if __name__ == "__main__":
    main()
