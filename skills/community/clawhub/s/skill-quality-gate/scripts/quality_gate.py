# -*- coding: utf-8 -*-
"""技能质量门禁：9 维校验一个技能目录，逐维 pass/fail。零依赖。"""
import argparse, pathlib, py_compile, re

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    base = pathlib.Path(a.dir)
    skill = base / "SKILL.md"
    results = []
    def check(name, ok, fix=""):
        results.append((name, ok, fix))

    # 1 frontmatter 八字段
    txt = skill.read_text(encoding="utf-8-sig") if skill.exists() else ""
    fields = ["name:", "display_name:", "display_name_en:", "description:", "slug:",
              "version:", "author:", "category:"]
    miss = [f for f in fields if f not in txt]
    check("frontmatter八字段", not miss, f"缺: {miss}" if miss else "")

    # 2 脚本可编译
    ok_script = True; bad = []
    for p in (base / "scripts").glob("*.py") if (base / "scripts").exists() else []:
        try:
            py_compile.compile(str(p), doraise=True)
        except Exception as e:
            ok_script = False; bad.append(f"{p.name}: {e}")
    check("脚本可编译", ok_script, "; ".join(bad))

    # 3 图标
    icon = base / "icon.png"
    check("图标icon.png", icon.exists())

    # 4 README 双语
    rd = (base / "README.md").read_text(encoding="utf-8-sig", errors="ignore") if (base / "README.md").exists() else ""
    en_words = re.findall(r"[A-Za-z]{4,}", rd)
    has_en = len(en_words) >= 8
    has_zh = len(re.findall(r"[一-鿿]", rd)) >= 20
    check("README双语", has_en and has_zh, "需中英简介")

    # 5 无密钥
    secret = re.compile(r"(ghp_[A-Za-z0-9]{8,}|sk-[A-Za-z0-9]{8,}|password\s*=\s*\S+)", re.I)
    has_secret = any(secret.search(f.read_text(encoding="utf-8-sig", errors="ignore"))
                     for f in base.rglob("*") if f.is_file() and f.suffix in (".md", ".py", ".json", ".txt", ".yml", ".yaml"))
    check("无密钥明文", not has_secret)

    # 6 description 双语
    dm = re.search(r"description:\s*\"?([^\"\n]+)", txt)
    d = dm.group(1) if dm else ""
    en_words = re.findall(r"[A-Za-z]{3,}", d)
    has_en = len(en_words) >= 2
    has_zh = len(re.findall(r"[一-鿿]", d)) >= 5
    check("description双语", has_en and has_zh)

    # 7 触发词/read_when
    check("触发词/场景", ("read_when" in txt) or ("触发词" in txt))

    # 8 门禁/铁律节
    check("门禁/铁律节", ("铁律" in txt) or ("门禁" in txt))

    # 9 去敏
    leak = re.compile("(" + "C:" + "\\\\" + "[Uu]sers|/home/[\\w.-]+|" + "内部" + "代号|" + "雇" + "主)", re.I)
    has_leak = any(leak.search(f.read_text(encoding="utf-8-sig", errors="ignore"))
                   for f in base.rglob("*.md"))
    check("去敏无泄漏", not has_leak)

    print(f"质量门禁：{base}\n" + "=" * 40)
    passed = 0
    for name, ok, fix in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  → {fix}" if fix and not ok else ""))
        passed += ok
    print("=" * 40)
    print(f"结果：{passed}/{len(results)}  → {'✅ 放行' if passed == len(results) else '🔒 拦截发布'}")

if __name__ == "__main__":
    main()
