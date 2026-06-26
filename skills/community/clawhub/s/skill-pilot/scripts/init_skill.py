#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化 SkillPilot 技能模板

Usage:
    python scripts/init_skill.py <skill-name> --path <output-directory>

Example:
    python scripts/init_skill.py my-skill --path ./skills
"""

import os
import argparse
from pathlib import Path


def create_skill_template(skill_name: str, output_path: str):
    """创建技能模板"""
    # 创建目录结构
    skill_dir = Path(output_path) / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)
    
    # 创建 SKILL.md 模板
    skill_md = f"""---
name: {skill_name}
description: [TODO: Add comprehensive description including what the skill does and when to use it]
---

# {skill_name.replace('-', ' ').title()}

[TODO: Write skill instructions]

## When to Use This Skill

[TODO: Move "when to use" information to description above, not here]

## Usage

```bash
# Example usage
[TODO: Add examples]
```

## References

- [TODO: Add reference files as needed]
"""
    
    (skill_dir / "SKILL.md").write_text(skill_md)
    
    # 创建示例脚本
    example_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script for {skill_name}

# When to include scripts:
# - Same code is being rewritten repeatedly
# - Deterministic reliability is needed
# - Token efficiency is important
"""

def main():
    pass

if __name__ == "__main__":
    main()
'''
    
    script_file = skill_dir / "scripts" / "example.py"
    script_file.write_text(example_script.format(skill_name=skill_name))
    script_file.chmod(0o755)
    
    # 创建示例参考文档
    example_ref = f"""# {skill_name.replace('-', ' ').title()} - Reference

[TODO: Add reference documentation]

## Overview

[TODO: Describe what this reference covers]

## Usage

Load this reference when:
- [TODO: Specify when to load]
"""
    
    ref_file = skill_dir / "references" / "example.md"
    ref_file.write_text(example_ref)
    
    # 创建 README
    readme = f"""# {skill_name.replace('-', ' ').title()}

## Setup

No setup required.

## Usage

[TODO: Add usage instructions]

## Development

Run tests and package the skill using the provided scripts.
"""
    
    (skill_dir / "README.md").write_text(readme)
    
    print(f"✓ Skill template created: {skill_dir}")
    print(f"  - SKILL.md (edit this)")
    print(f"  - scripts/example.py (customize or delete)")
    print(f"  - references/example.md (customize or delete)")
    print(f"  - README.md")
    print(f"\nNext steps:")
    print(f"  1. Edit SKILL.md with your instructions")
    print(f"  2. Add scripts/references/assets as needed")
    print(f"  3. Run: python scripts/package_skill.py {skill_dir}")


def main():
    parser = argparse.ArgumentParser(description="Initialize SkillPilot skill template")
    parser.add_argument("skill_name", help="Skill name (e.g., my-skill)")
    parser.add_argument("--path", default="./skills", help="Output directory (default: ./skills)")
    
    args = parser.parse_args()
    create_skill_template(args.skill_name, args.path)


if __name__ == "__main__":
    main()
