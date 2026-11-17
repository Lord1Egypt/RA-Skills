#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skill-skeleton-generator — 一键生成四角度合规 AI 技能骨架（SKILL.md + AGENTS.md + 目录）。
理论根基：LGD 三律（有籍·有证·有门禁）。Usage:
  python skeleton.py --name my-skill --description "..." [--out dir]"""
import argparse, datetime, os, sys

TEMPLATE = '''---
name: {name}
description: "{desc}"
version: 0.1.0
license: MIT
category: {cat}
author: SynomosAI (LGD initiative)
platforms: [windows, macos, linux]
tags: [{tags}]
slug: {slug}
risk_tier: medium
---

# {display}

## 定位一句话 / One-liner
> {oneliner_en}
> {oneliner_zh}

## 功能 / Capabilities
- {cap1_en}
- {cap1_zh}
- {cap2_en}
- {cap2_zh}

## 用法 / Usage
```bash
{usage}
```

## 三律对齐 / LGD alignment
| 律 | 本技能如何满足 |
|---|---|
| 有籍 Registered | frontmatter 完整：name/description/license/version |
| 有证 Evidenced | 输出可复现，含验证段 |
| 有门禁 Gated | 最小权限、fail-closed、禁止危险操作 |

## License & attribution
© 2026 SynomosAI contributors. initiative. Code MIT; SKILL.md theory text All rights reserved.
'''

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--description", required=True)
    p.add_argument("--cat", default="AI工程")
    p.add_argument("--out", default=".")
    a = p.parse_args()
    slug = a.name.lower().replace(" ", "-")
    os.makedirs(a.out, exist_ok=True)
    md = TEMPLATE.format(
        name=a.name, desc=a.description, cat=a.cat, tags=a.name.lower().replace(" ", ","),
        slug=slug, display=a.name.replace("-", " ").title(),
        oneliner_en=a.description, oneliner_zh=a.description,
        cap1_en="Core capability placeholder — edit me", cap1_zh="核心能力占位 — 请编辑",
        cap2_en="Verification placeholder — edit me", cap2_zh="验证占位 — 请编辑",
        usage="python %s.py <args>" % slug,
    )
    with open(os.path.join(a.out, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(a.out, "AGENTS.md"), "w", encoding="utf-8") as f:
        f.write("# AGENTS.md\n\nMachine-readable entry for %s. See SKILL.md.\n" % a.name)
    print("generated:", os.path.join(a.out, "SKILL.md"), "and AGENTS.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
