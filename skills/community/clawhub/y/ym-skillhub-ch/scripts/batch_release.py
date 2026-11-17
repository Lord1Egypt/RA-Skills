#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量上架：发布 SkillHub + 同步 GitHub + 双项校验。

把「一批技能从本地目录推到线上」整条链路固化下来。两处平台节流都已内建：
  - SkillHub 发布有频率限制，**每个之间固定 GAP 秒**（默认 40），失败按 30/60/90 退避重试；
  - GitHub 连推十几个仓库会返回 422（次级限流），走 push_via_api 的重试通道。

用法：
    python batch_release.py <技能目录> [<技能目录> ...] [选项]
    python batch_release.py --from-list list.txt [选项]

选项：
    --stage publish|github|all   只做某一段，默认 all
    --gap 40                     SkillHub 发布间隔秒数
    --changelog "说明"            统一 changelog（不传则用 SKILL.md 的 summary 字段）
    --branch main                推送分支
    --owner <你的GitHub账号>      GitHub 账号（不传则取 gh 当前登录用户）
    --email <提交邮箱>            git 提交邮箱（不传则用 <owner>@users.noreply.github.com）
    --skills-root <目录>         技能根目录，默认 ~/.workbuddy/skills
    --dry-run                    只打印计划

退出码：0 全部成功 / 1 有失败项 / 2 参数错。
"""
import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# 解释器用「当前跑这个脚本的 python」，不写死个人路径（否则换机就废）。
PY = os.environ.get("SKILLHUB_PY") or sys.executable
CLI = Path.home() / ".skillhub" / "skills_store_cli.py"
PUSHER = Path.home() / ".workbuddy" / "tools" / "push_via_api.py"


def run(cmd, cwd=None, env=None):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()


def read_summary(skill_dir: Path) -> str:
    """从 SKILL.md frontmatter 的 summary / description 取一句话当 changelog。"""
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return ""
    m = re.match(r"^---\r?\n(.*?)\r?\n---", md.read_text(encoding="utf-8"), re.S)
    if not m:
        return ""
    for key in ("summary", "description"):
        for line in m.group(1).splitlines():
            if line.startswith(key + ":"):
                v = line.split(":", 1)[1].strip().strip('"')
                return v[:120]
    return ""


def publish(skill_dir: Path, changelog: str, env, tries=3) -> bool:
    for i in range(tries):
        rc, out = run([PY, str(CLI), "publish", str(skill_dir),
                       "--changelog", changelog], env=env)
        first = out.replace("\n", " | ")[:120]
        if rc == 0:
            print("  发布 OK   %s" % first, flush=True)
            return True
        wait = 30 * (i + 1)
        print("  发布 重试 %d/3  rc=%d  %s  -> %ds 后重试"
              % (i + 1, rc, first, wait), flush=True)
        if i < tries - 1:
            time.sleep(wait)
    return False


def push_github(skill_dir: Path, owner: str, branch: str, email: str = "") -> bool:
    name = skill_dir.name
    if not (skill_dir / ".git").exists():
        run(["git", "init", "-q"], cwd=str(skill_dir))
    run(["git", "add", "-A"], cwd=str(skill_dir))
    # 提交邮箱不写死：优先 --email / 环境变量，兜底用 GitHub 官方 noreply 地址
    email = email or os.environ.get("GIT_AUTHOR_EMAIL") or ("%s@users.noreply.github.com" % owner)
    run(["git", "-c", "user.name=" + owner, "-c", "user.email=" + email,
         "commit", "-m", "feat: 技能更新"], cwd=str(skill_dir))

    rc, _ = run(["gh", "repo", "view", "%s/%s" % (owner, name)])
    if rc != 0:
        rc, out = run(["gh", "repo", "create", name, "--public",
                       "--source=.", "--remote=origin"], cwd=str(skill_dir))
        print("  建仓 %s" % ("OK" if rc == 0 else "失败 " + out[-80:]), flush=True)
    else:
        rc, _ = run(["git", "remote", "get-url", "origin"], cwd=str(skill_dir))
        if rc != 0:
            run(["git", "remote", "add", "origin",
                 "https://github.com/%s/%s.git" % (owner, name)], cwd=str(skill_dir))

    rc, out = run([PY, str(PUSHER), str(skill_dir), "--branch", branch])
    line = [l for l in out.splitlines() if "tree" in l]
    print("  推送 %s  %s" % ("OK" if rc == 0 else "失败",
                            line[-1][:100] if line else out[-100:]), flush=True)
    return rc == 0


def verify_skillhub(skill_dir: Path) -> bool:
    """判据：版本列表里出现 SKILL.md 中声明的版本号 = 已过审上线。"""
    md = skill_dir / "SKILL.md"
    m = re.search(r"^version:\s*([\d.]+)", md.read_text(encoding="utf-8"), re.M)
    ver = m.group(1) if m else "0.1.0"
    slug = skill_dir.name
    import json
    import urllib.request
    URL = "https://api.skillhub.cn/api/v1/skills/%s/versions" % slug
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "batch-release/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001
        print("  校验 取不到线上数据：%s" % e, flush=True)
        return False
    items = []
    if isinstance(data, dict):
        items = data.get("data") or data.get("versions") or []
    elif isinstance(data, list):
        items = data
    vers = [i.get("version") if isinstance(i, dict) else str(i) for i in items]
    on = ver in vers
    print("  校验 %s  线上版本=%s  %s"
          % ("OK" if on else "待审核", vers or "(空)",
             "已上线" if on else "稍后复查（受理不等于上线）"), flush=True)
    return on


def main() -> int:
    ap = argparse.ArgumentParser(description="批量发布 SkillHub 并同步 GitHub")
    ap.add_argument("dirs", nargs="*", help="技能目录")
    ap.add_argument("--from-list", help="从文件读技能目录，每行一个")
    ap.add_argument("--stage", choices=["publish", "github", "all"], default="all")
    ap.add_argument("--gap", type=int, default=40)
    ap.add_argument("--changelog", default="")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--owner", default=None,
                    help="GitHub 账号，默认取 gh 当前登录用户")
    ap.add_argument("--email", default="",
                    help="git 提交邮箱，默认 <owner>@users.noreply.github.com")
    ap.add_argument("--skills-root", default=str(Path.home() / ".workbuddy" / "skills"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    targets = list(a.dirs)
    if a.from_list:
        targets += [l.strip() for l in Path(a.from_list).read_text(encoding="utf-8").splitlines()
                    if l.strip() and not l.startswith("#")]
    if not targets:
        print("没给技能目录。传目录，或用 --from-list。")
        return 2

    owner = a.owner
    if a.stage in ("github", "all") and not owner:
        rc, out = run(["gh", "api", "user", "--jq", ".login"])
        if rc != 0 or not out:
            print("取不到 gh 登录用户，请显式传 --owner。")
            return 2
        owner = out.strip().splitlines()[-1].strip()
        print("GitHub 账号：%s" % owner)

    root = Path(a.skills_root)
    dirs = []
    for t in targets:
        p = Path(t)
        d = p if p.is_absolute() else root / t
        if not (d / "SKILL.md").exists():
            print("跳过（没有 SKILL.md）：%s" % d)
            continue
        dirs.append(d)
    if not dirs:
        print("没有可处理的技能。")
        return 2

    print("技能 %d 个，阶段=%s，发布间隔=%ds" % (len(dirs), a.stage, a.gap))
    if a.dry_run:
        for d in dirs:
            print("  - %s  changelog=%s" % (d.name, (a.changelog or read_summary(d))[:60]))
        print("--dry-run：未做任何写入。")
        return 0

    env = dict(os.environ)
    env["HOME"] = str(Path.home())
    env["USERPROFILE"] = str(Path.home())

    ok, fail = [], []
    for i, d in enumerate(dirs):
        print("=" * 50, flush=True)
        print(d.name, flush=True)
        good = True
        if a.stage in ("publish", "all"):
            good &= publish(d, a.changelog or read_summary(d) or "技能发布", env)
        if a.stage in ("github", "all"):
            good &= push_github(d, owner, a.branch, a.email)
        if a.stage in ("publish", "all"):
            verify_skillhub(d)  # 仅供参考，未过审不算失败
        (ok if good else fail).append(d.name)
        if a.stage in ("publish", "all") and i < len(dirs) - 1:
            time.sleep(a.gap)

    print("\n成功 %d / 失败 %d" % (len(ok), len(fail)))
    if fail:
        print("失败：", ", ".join(fail))
        print("提示：重跑失败的这几项即可（命令是幂等的；«已一致»代表无变化）。")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
