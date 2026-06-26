#!/usr/bin/env python3
"""
build_kb_structure.py — 通用工具：批量建 ima KB 目录树

解决 bash 中文变量名在 set -euo pipefail 下被吞的问题（2026-06-04 踩坑）：
  - bash 变量名不能用中文（L1_每日快报=... 会报 command not found）
  - python 字典/字符串天然支持中文，无编码坑

用法：
  1) 编辑 STRUCTURE 字典定义目录树（支持任意嵌套深度）
  2) python3 build_kb_structure.py <kb_id> [kb_name_for_display]
  3) 真用前先注释掉最后的 build_kb(kb_id, STRUCTURE) 行做 dry-run

字段说明：
  - openapi/wiki/v1/create_folder 的父目录字段名是 folder_id
    （v8 探针验证过；不是 parent_folder_id / parent_id / dst_folder_id）
  - 错误码 51 表示 name 为空 / 字段缺失
  - 错误码 220030 表示权限不足（你不是 KB 创建者）
"""

import subprocess
import json
import sys


IMA_API_CJS = "/home/jerome/.hermes/skills/ima/ima_api.cjs"


def create_folder(kb_id, name, parent_id=None):
    """调 ima_api.cjs 建一个 folder
    return: (code, media_id, msg)
    """
    if parent_id:
        parent_clause = ", folder_id:'" + parent_id + "'"
    else:
        parent_clause = ""
    name_json = json.dumps(name, ensure_ascii=False)
    node_code = (
        "const {imaApi} = require('" + IMA_API_CJS + "');\n"
        "const opts={clientId:process.env.IMA_OPENAPI_CLIENTID, apiKey:process.env.IMA_OPENAPI_APIKEY};\n"
        "const body={knowledge_base_id:'" + kb_id + "', name:" + name_json + parent_clause + "};\n"
        "imaApi('openapi/wiki/v1/create_folder', body, opts).then(r=>{\n"
        "  const d=JSON.parse(r);\n"
        "  process.stdout.write(JSON.stringify({code:d.code, mid:d.data && d.data.media_id, msg:d.msg}));\n"
        "}).catch(e=>{console.error(e.message); process.exit(1);});\n"
    )
    r = subprocess.run(["node", "-e", node_code], capture_output=True, text=True)
    try:
        last = [l for l in r.stdout.strip().splitlines() if l.startswith("{")][-1]
        d = json.loads(last)
        return d.get("code", -1), d.get("mid"), d.get("msg", "")
    except Exception as e:
        return -1, None, "parse err: %s, stdout=%s" % (e, r.stdout[:200])


def build_kb(kb_id, structure, indent=0):
    """递归建目录树
    structure: dict, key=目录名, value=子目录 dict（None = 叶子）
    """
    ok = 0
    fail = 0
    for name, sub in structure.items():
        code, mid, msg = create_folder(kb_id, name)
        prefix = "  " * indent
        if code == 0 and mid:
            print("%s  ✓ %s  →  %s" % (prefix, name, mid))
            ok += 1
            if sub:
                sub_ok, sub_fail = build_kb(kb_id, sub, parent_id=mid, indent=indent + 1)
                ok += sub_ok
                fail += sub_fail
        else:
            print("%s  ✗ %s  code=%s  msg=%s" % (prefix, name, code, msg))
            fail += 1
    return ok, fail


# ─────────── 结构定义（按你需求改）───────────
# 用法：把下面 STRUCTURE 替换成你自己的目录树
STRUCTURE = {
    "📰 每日快报": {
        "信号速递": None,
        "深读推荐": None,
        "我的短评": None,
    },
    "🔎 信号收集": {
        "论文与开源": None,
        "大厂与资本": None,
        "政策与监管": None,
        "跨界信号": None,
    },
    "💡 商业解读": {
        "成本影响": None,
        "收入影响": None,
        "风险判断": None,
        "行动建议": None,
    },
    "🧪 验证记录": {
        "工具实测": None,
        "方案跑通": None,
        "成本实测": None,
        "资源名录": None,
    },
    "📋 长期跟踪": {
        "持续关注的主题": None,
        "旧判断回顾": None,
    },
}


def main():
    if len(sys.argv) < 2:
        print("用法: python3 build_kb_structure.py <kb_id> [kb_name_for_display]")
        print()
        print("  kb_id: 已经 create-kb 建好的知识库 ID")
        print()
        print("示例:")
        print("  python3 build_kb_structure.py YOUR_KB_ID 'OpenClaw·技术策展库'")
        print()
        print("注意: 编辑本文件末尾的 STRUCTURE 字典定义你要建的目录树")
        sys.exit(1)

    kb_id = sys.argv[1]
    kb_name = sys.argv[2] if len(sys.argv) > 2 else "<未命名 KB>"

    print("══════════════════════════════════════════════════════════════")
    print(" 重建目录树: %s" % kb_name)
    print(" KB: %s" % kb_id)
    print("══════════════════════════════════════════════════════════════")
    print()

    ok, fail = build_kb(kb_id, STRUCTURE)

    print()
    print("══════════════════════════════════════════════════════════════")
    print(" 完成: %d 成功 / %d 失败" % (ok, fail))
    print("══════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
