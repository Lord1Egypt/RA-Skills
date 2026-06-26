#!/usr/bin/env python3
# 质量自检脚本
# 检查 SKILL.md 是否符合质量通过标准

import re
import sys
from pathlib import Path

def check_skill_quality(skill_md_path):
    """质量检查"""
    if not os.path.exists(skill_md_path):
        print(f"错误: {skill_md_path} 不存在")
        return False
    
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = []
    
    # 1. 心智模型数量 (3-7个)
    mental_models = re.findall(r'^### \d+\. [^\n]+mental model', content, re.M)
    if 3 <= len(mental_models) <= 7:
        checks.append(("心智模型数量", "PASS", f"{len(mental_models)}个"))
    else:
        checks.append(("心智模型数量", "FAIL", f"只有{len(mental_models)}个 (应为3-7)"))
    
    # 2. 每个模型都有局限性描述
    model_sections = re.split(r'^### \d+\.', content, flags=re.M)
    limitations_found = 0
    for section in model_sections[1:]:  # 跳过第一个
        if re.search(r'局限性|失效条件|不适用', section):
            limitations_found += 1
    
    if limitations_found == len(mental_models):
        checks.append(("模型局限性", "PASS", "所有模型都标注了局限"))
    else:
        checks.append(("模型局限性", "FAIL", f"只有{limitations_found}/{len(mental_models)}个模型有局限"))
    
    # 3. 表达DNA辨识度
    voice_markers = re.findall(r'表达DNA|句式偏好|词汇特征|幽默方式|节奏感', content)
    if len(voice_markers) >= 2:
        checks.append(("表达DNA", "PASS", f"包含{len(voice_markers)}个语音标记"))
    else:
        checks.append(("表达DNA", "FAIL", "表达DNA描述不充分"))
    
    # 4. 诚实边界
    if re.search(r'诚实边界|局限|不确定|无法预测|不能替代', content):
        checks.append(("诚实边界", "PASS", "包含诚实边界说明"))
    else:
        checks.append(("诚实边界", "FAIL", "缺少诚实边界"))
    
    # 5. 内在张力/矛盾
    if re.search(r'矛盾|张力|内在冲突|价值观冲突', content):
        checks.append(("内在张力", "PASS", "包含矛盾张力"))
    else:
        checks.append(("内在张力", "FAIL", "缺少内在张力"))
    
    # 6. 一手来源占比
    sources_section = re.search(r'调研来源.*$', content, re.S)
    if sources_section:
        sources_text = sources_section.group(0)
        first_hand = len(re.findall(r'一手|本人|原始|著作', sources_text))
        second_hand = len(re.findall(r'二手|转述|他人|采访', sources_text))
        if first_hand > second_hand:
            checks.append(("一手来源", "PASS", f"一手{first_hand} vs 二手{second_hand}"))
        else:
            checks.append(("一手来源", "FAIL", f"二手过多 ({first_hand} vs {second_hand})"))
    else:
        checks.append(("一手来源", "FAIL", "缺少调研来源列表"))
    
    # 输出检查结果
    print("\n" + "="*60)
    print("质量自检结果")
    print("="*60)
    passed = 0
    for name, status, detail in checks:
        status_str = "✅" if status == "PASS" else "❌"
        print(f"{status_str} {name:<20} {status:<6} {detail}")
        if status == "PASS":
            passed += 1
    
    print("="*60)
    print(f"通过项: {passed}/{len(checks)}")
    print("="*60 + "\n")
    
    return passed == len(checks)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        check_skill_quality("SKILL.md")
    else:
        check_skill_quality(sys.argv[1])
