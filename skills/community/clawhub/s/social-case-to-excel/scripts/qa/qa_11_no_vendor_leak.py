# -*- coding: utf-8 -*-
"""qa_11 凭据安全检查（保留旧文件名兼容）：允许 ClaudeBaby 名称和邀请链接，拒绝真实凭据。

用法：
    python3 qa_11_no_vendor_leak.py <file.xlsx|file.md> [more...]
    python3 qa_11_no_vendor_leak.py ~/clacky_workspace          # 扫目录下所有 xlsx/md
退出码 0 = 干净，1 = 有泄漏（会打印命中片段）。
xlsx 是压缩包，普通 grep 查不到，必须解压扫 xl/**.xml。"""
import os, re, sys, glob, html, zipfile

BLACK = [
    r'Bearer\s+[A-Za-z0-9._~+/=-]{16,}',
    r'(?:CLAUDEBABY_MCP_TOKEN|REDDIT_MCP_TOKEN)\s*[=:]\s*[\"\']?[A-Za-z0-9._~+/=-]{16,}',
    r'[?&](?:token|api_key|access_token)=[A-Za-z0-9._~+/=-]{16,}',
]

RX = re.compile('|'.join(BLACK), re.I)
ALLOW = ('qa_11', 'SKILL.md')  # 黑名单本身不算泄漏


def hits(text, tag):
    out = []
    for m in RX.finditer(text):
        a, b = max(0, m.start() - 60), min(len(text), m.end() + 60)
        out.append('%s: credential pattern detected (value redacted)' % tag)
    return out


def scan_xlsx(p):
    z = zipfile.ZipFile(p)
    found = []
    for n in z.namelist():
        if n.endswith(('.xml', '.rels')):
            t = html.unescape(z.read(n).decode('utf-8', 'ignore'))
            t = re.sub(r'<[^>]+>', ' ', t)
            found += hits(t, n)
    return found


def scan_md(p):
    return hits(open(p, encoding='utf-8', errors='ignore').read(), 'text')


def main(argv):
    # skill 自己的文档里必然出现产品说明（那是内部说明，不是交付物）。
    # 不跳过的话，拿 skill 目录当参数跑一次会报出几十条"泄漏"，把自己的文档吓一跳。
    # 脚本在 scripts/qa/ 下，要退三级才到 skill 根。
    skill_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
    targets = []
    for a in argv:
        a = os.path.expanduser(a)
        if os.path.isdir(a):
            targets += glob.glob(os.path.join(a, '*.xlsx')) + glob.glob(os.path.join(a, '*.md'))
        else:
            targets.append(a)
    bad = 0
    for p in targets:
        if not os.path.isfile(p) or os.path.basename(p) in ALLOW:
            continue
        if os.path.abspath(p).startswith(skill_root):
            print('➖ %s（skill 自身文件，本包文档不作为报告扫描）' % os.path.basename(p))
            continue
        f = scan_xlsx(p) if p.lower().endswith('.xlsx') else scan_md(p)
        if f:
            bad += 1
            print('❌ %s —— %d 处泄漏' % (os.path.basename(p), len(f)))
            for x in f[:12]:
                print('    ', x[:180])
        else:
            print('✅ %s' % os.path.basename(p))
    print('结论：%d 个文件有泄漏' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
