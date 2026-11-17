#!/usr/bin/env python3
"""
发布质量门禁 - 四层敏感信息扫描脚本
用法:
  python check_release.py <目标目录或zip> [发布物名称]

四层检查:
  L1 公司敏感信息: 公司名/人名/证号/内部资料
  L2 本机信息:     本机路径/电脑用户名/安装路径
  L3 个人信息:     手机号/邮箱/身份证/微信/QQ/地址
  L4 机密信息:     API密钥/密码/平台账号/内部代号/外部IP

输出: 命中列表 + 误报判定建议，退出码 0=零真实命中 1=有疑似命中
"""

import re
import os
import sys
import zipfile

TEXT_EXTS = {'.md', '.py', '.json', '.txt', '.yml', '.yaml', '.html', '.csv', '.xml', '.ini', '.cfg', '.env'}
BIN_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.pdf', '.docx', '.xlsx', '.pptx', '.zip'}

# ============ 四层检查模式 ============

LAYERS = {
    "L1 公司敏感信息": {
        "公司名": r'(?i)([\u4e00-\u9fa5]{2,8}(?:医疗|科技|集团|药业|有限公司|股份有限公司))',
        "人名": r'(?i)([\u4e00-\u9fa5]{2,4}\s*(?:先生|女士|经理|总监|工程师))',
        "证号": r'(?i)(注册证号|备案号|营业执照号|统一社会信用代码|[A-Z]{2}[0-9]{6,})',
        "内部资料词": r'(?i)(内部体系文件|客户合同|未公开|机密文件|confidential)',
    },
    "L2 本机信息": {
        "本机路径": r'(?i)(C:[/\\\\]Users[/\\\\]\w+|D:[/\\\\]Workbuddy[/\\\\]\w+|[\/]c[\/]Users[\/]\w+|[\/]home[\/]\w+)',
        "电脑用户名": r'(?i)(desktop-[a-z0-9]+|pc-\w+)',
        "安装路径": r'(?i)(%LOCALAPPDATA%|%APPDATA%|C:[/\\\\]Program Files[/\\\\](?!Ollama))',
    },
    "L3 个人信息": {
        "手机号": r'(?<!\d)1[3-9]\d{9}(?!\d)',
        "邮箱": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}',
        "身份证": r'(?<!\d)\d{17}[\dXx](?!\d)',
        "QQ号": r'(?<!\d)[1-9]\d{5,11}(?!\d)',
        "地址": r'(?i)(天津市|北京市|上海市|广东省|深圳市|香港|澳门|滨海新区)[^\s]{0,30}(路|街|道|号|大厦|中心|广场)',
    },
    "L4 机密信息": {
        "API密钥": r'(?i)(sk-[a-zA-Z0-9]{16,}|api[_-]?key\s*[=:]\s*["\']\S{8,}["\']|access[_-]?token\s*[=:]\s*["\']\S{8,}["\']|secret[_-]?key\s*[=:]\s*["\']\S{8,}["\'])',
        "密码": r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']\S{4,}["\']',
        "平台账号": r'(?i)(ima[_-]?mcp|agent[_-]?mail|示例平台账号)',
        "内部代号": r'(?i)(项目代号|内部系统名|内部代号)',
        "外部IP": r'(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?![\d.])',
    },
}

# ============ 已知误报（技术参数，非敏感） ============
# 端口号、上下文窗口、MD5、回环地址、通用占位符等

KNOWN_FALSE_POSITIVES = [
    r'localhost:\d+',           # 本地服务端口
    r'127\.0\.0\.1(?::\d+)?',   # 回环地址（含不带端口）
    r'0\.0\.0\.0',              # 全零地址
    r'11434',                   # Ollama 默认端口
    r'\b(8192|16384|32768|65536)\b',  # 上下文窗口
    r'[a-f0-9]{32}',            # MD5
    r'[0-9]{4}-[0-9]{2}-[0-9]{2}',   # 日期
    r'qwen2\.5[:0-9a-z.]+',     # 模型名
    r'deepseek[-\w:.]*',        # 模型名
    r'\bGMP-\d{4}\b',           # 法规年份
    r'ISO\s?13485',             # 标准号
]

# ============ 品牌豁免（公开品牌，有意保留） ============
# 发布者公开的公司品牌/作者品牌，出现在发布物中是有意的品牌曝光，不算泄露。
# 命中这些词 → 列为"品牌确认"而非风险。
BRAND_NAMES = ["注册老炮"]

# ============ 作者署名豁免 ============
# 发布者有意保留的作者署名（建立实名可信度），不算泄露。
# 命中这些名字且出现在 author/作者/署名 上下文中 → 列为"署名确认"而非风险。
AUTHOR_NAMES = ["注册老炮"]


def is_author_credit(hit):
    """判断命中是否为作者署名或公开品牌（有意保留）"""
    # 公开品牌豁免（如作者品牌、公开署名，有意保留）
    matched_lower = hit['matched'].lower()
    if any(brand.lower() in matched_lower for brand in BRAND_NAMES):
        return True
    ctx = hit['snippet'].lower()
    if any(brand.lower() in ctx for brand in BRAND_NAMES):
        if any(kw in ctx for kw in ['注册老炮', '"name"', 'author', '作者', '署名', '版权', '©']):
            return True
    # 作者署名豁免
    if hit['type'] != '人名':
        return False
    # 命中值本身是作者名
    if any(name.lower() in matched_lower for name in AUTHOR_NAMES):
        return True
    # 上下文含署名语义
    if any(name.lower() in ctx for name in AUTHOR_NAMES):
        if any(kw in ctx for kw in ['"name"', 'author', '作者', '署名', '原创', '整理']):
            return True
    return False


def is_false_positive(hit_text):
    """判断命中是否为已知技术参数误报"""
    return any(re.search(pat, hit_text, re.IGNORECASE) for pat in KNOWN_FALSE_POSITIVES)


def scan_text(name, content):
    """扫描单文件文本内容，返回命中列表"""
    hits = []
    for layer, patterns in LAYERS.items():
        for pname, pat in patterns.items():
            for m in re.finditer(pat, content):
                start = max(0, m.start() - 25)
                end = min(len(content), m.end() + 25)
                snippet = content[start:end].replace('\n', ' ')
                line_no = content[:m.start()].count('\n') + 1
                hits.append({
                    'layer': layer,
                    'type': pname,
                    'file': name,
                    'line': line_no,
                    'snippet': snippet,
                    'matched': m.group(0)[:60],
                    'false_positive': is_false_positive(snippet),
                })
    return hits


def scan_path(path, label_prefix=""):
    """扫描文件或目录，返回命中列表"""
    hits = []
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lower()
        if ext in TEXT_EXTS:
            try:
                with open(path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                    content = f.read()
                hits += scan_text(label_prefix + os.path.basename(path), content)
            except Exception:
                pass
        return hits

    for root, dirs, files in os.walk(path):
        # 跳过隐藏目录和临时目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__')]
        for f in files:
            full = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in TEXT_EXTS:
                try:
                    with open(full, 'r', encoding='utf-8-sig', errors='ignore') as fh:
                        content = fh.read()
                    rel = os.path.relpath(full, path)
                    hits += scan_text(rel, content)
                except Exception:
                    pass
    return hits


def scan_zip(zip_path):
    """扫描 zip 内文本内容"""
    hits = []
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for name in zf.namelist():
                ext = os.path.splitext(name)[1].lower()
                if ext in TEXT_EXTS:
                    try:
                        content = zf.read(name).decode('utf-8', errors='ignore')
                        hits += scan_text(name, content)
                    except Exception:
                        pass
    except Exception as e:
        print(f"[!] 无法读取 zip: {e}")
    return hits


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    target = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(target)

    print(f"🔍 四层敏感信息扫描: {label}")
    print(f"   目标: {target}\n")

    all_hits = []
    if os.path.isdir(target):
        all_hits = scan_path(target)
    elif zipfile.is_zipfile(target):
        all_hits = scan_zip(target)
    else:
        all_hits = scan_path(target)

    # 汇总
    real_hits = [h for h in all_hits if not h['false_positive'] and not is_author_credit(h)]
    credit_hits = [h for h in all_hits if not h['false_positive'] and is_author_credit(h)]
    fp_hits = [h for h in all_hits if h['false_positive']]

    # 按层分组统计
    layer_stats = {}
    for h in real_hits:
        layer_stats.setdefault(h['layer'], []).append(h)

    print("=" * 60)
    print("扫描结果统计:")
    for layer in LAYERS:
        n = len(layer_stats.get(layer, []))
        status = "✅ 零命中" if n == 0 else f"⚠️ {n} 个疑似命中"
        print(f"  {layer}: {status}")
    print(f"  已知技术参数误报（自动排除）: {len(fp_hits)} 个")
    if credit_hits:
        print(f"  作者署名/公开品牌（有意保留，需确认）: {len(credit_hits)} 个")
    print("=" * 60)

    if not real_hits:
        print("\n✅ 四层检查通过（无真实敏感信息泄露）!")
        if credit_hits:
            print(f"\n📝 另发现 {len(credit_hits)} 处作者署名/公开品牌（如 注册老炮），请确认是有意保留的:")
            for h in credit_hits:
                print(f"  - {h['file']}:{h['line']}: {h['matched']}")
        sys.exit(0)

    # 打印疑似命中，供人工复核
    print(f"\n⚠️ 发现 {len(real_hits)} 个疑似敏感信息（需人工逐条复核）:\n")
    for i, h in enumerate(real_hits, 1):
        print(f"--- [{h['layer']} / {h['type']}] ---")
        print(f"  文件: {h['file']}:{h['line']}")
        print(f"  命中: {h['matched']}")
        print(f"  上下文: ...{h['snippet']}...")
        print()

    if credit_hits:
        print(f"📝 另发现 {len(credit_hits)} 处作者署名/公开品牌（有意保留，需确认）:\n")
        for h in credit_hits:
            print(f"  - [{h['layer']} / {h['type']}] {h['file']}:{h['line']}: {h['matched']}")
        print()

    print("=" * 60)
    print("复核建议:")
    print("  1. 逐条判断是真实敏感信息还是误报（已自动排除端口/MD5/回环等常见误报）")
    print("  2. 真实命中 → 脱敏修改 → 重新打包 → 重新扫描直到零命中")
    print("  3. 注意: 二进制图片(png等)的正则命中几乎都是误报，跳过即可")
    sys.exit(1)


if __name__ == "__main__":
    main()
