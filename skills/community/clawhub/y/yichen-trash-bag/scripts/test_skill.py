#!/usr/bin/env python3
"""奕辰垃圾袋 Skill · 基础验证测试"""

import sys
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

def check(label, condition):
    if condition:
        print(f"  ✅ {label}")
    else:
        print(f"  ❌ {label}")
        errors.append(label)

print("奕辰垃圾袋 Skill · 验证测试")
print("=" * 40)

# 1. 核心文件存在性
print("\n[核心文件]")
check("SKILL.md 存在", os.path.isfile(os.path.join(SKILL_DIR, "SKILL.md")))
check("version.json 存在", os.path.isfile(os.path.join(SKILL_DIR, "version.json")))
check("README.md 存在", os.path.isfile(os.path.join(SKILL_DIR, "README.md")))
check("CHANGELOG.md 存在", os.path.isfile(os.path.join(SKILL_DIR, "CHANGELOG.md")))
check("install.sh 存在", os.path.isfile(os.path.join(SKILL_DIR, "install.sh")))
check("install.ps1 存在", os.path.isfile(os.path.join(SKILL_DIR, "install.ps1")))

# 2. References 文件
print("\n[References 文件]")
ref_dir = os.path.join(SKILL_DIR, "references")
refs = ["brand.md", "business-info.md", "services.md", "promotions.md", "faq.md", "shipping.md", "wholesale.md"]
for ref in refs:
    check(f"references/{ref} 存在", os.path.isfile(os.path.join(ref_dir, ref)))

# 3. SKILL.md 关键内容
print("\n[SKILL.md 内容检查]")
with open(os.path.join(SKILL_DIR, "SKILL.md"), "r", encoding="utf-8") as f:
    skill = f.read()

check("name: yichen-trash-bag", "yichen-trash-bag" in skill)
check("包含场景一~九", all(f"场景{i}" in skill for i in ["一", "二", "三", "四", "五", "六", "七", "八", "九"]))
check("包含价格声明", "仅供参考" in skill and "以下单" in skill)
check("包含权限边界说明", "不具备处理售后" in skill or "引导联系店铺客服" in skill)
check("包含 references 数据读取规则", "references/" in skill and "实时读取" in skill)

# 4. references 数据完整性
print("\n[数据完整性]")
with open(os.path.join(ref_dir, "services.md"), "r", encoding="utf-8") as f:
    svc = f.read()
product_count = svc.count("## ")
check(f"services.md 包含 {product_count} 款商品", product_count >= 6)

with open(os.path.join(ref_dir, "faq.md"), "r", encoding="utf-8") as f:
    faq = f.read()
faq_count = faq.count("## Q")
check(f"faq.md 包含 {faq_count} 条问答", faq_count >= 8)

# 5. version.json
print("\n[版本信息]")
import json
with open(os.path.join(SKILL_DIR, "version.json"), "r", encoding="utf-8") as f:
    ver = json.load(f)
check("skill 名称正确", ver.get("skill") == "yichen-trash-bag")
check("version 字段存在", "version" in ver)
check("data_version 字段存在", "data_version" in ver)

# 结果
print(f"\n{'=' * 40}")
if errors:
    print(f"❌ 失败: {len(errors)} 项未通过")
    for e in errors:
        print(f"   - {e}")
    sys.exit(1)
else:
    print("✅ 全部测试通过！")
    sys.exit(0)
