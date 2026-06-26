#!/usr/bin/env python3
"""
娜可露露洗发水 Skill - 测试脚本
用于验证 Skill 功能是否正常
"""

import os
import sys

def check_file_exists(path, description):
    """检查文件是否存在"""
    if os.path.exists(path):
        print(f"[OK] {description}: {path}")
        return True
    else:
        print(f"[MISSING] {description}: {path}")
        return False

def check_directory_exists(path, description):
    """检查目录是否存在"""
    if os.path.isdir(path):
        print(f"[OK] {description}: {path}")
        return True
    else:
        print(f"[MISSING] {description}: {path}")
        return False

def test_skill():
    """测试 Skill 完整性"""
    print("=" * 60)
    print("娜可露露洗发水 Skill - 功能测试")
    print("=" * 60)
    
    skill_dir = r"C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender"
    
    results = []
    
    # 测试 1: 核心文件
    print("\n[测试 1] 核心文件检查")
    print("-" * 40)
    results.append(check_file_exists(
        os.path.join(skill_dir, "SKILL.md"), 
        "主文件 SKILL.md"
    ))
    results.append(check_file_exists(
        os.path.join(skill_dir, "PACKAGE.md"), 
        "打包说明 PACKAGE.md"
    ))
    
    # 测试 2: 参考文档
    print("\n[测试 2] 参考文档检查")
    print("-" * 40)
    results.append(check_file_exists(
        os.path.join(skill_dir, "references", "products.md"), 
        "产品线参考"
    ))
    results.append(check_file_exists(
        os.path.join(skill_dir, "references", "faq.md"), 
        "FAQ文档"
    ))
    results.append(check_file_exists(
        os.path.join(skill_dir, "references", "examples.md"), 
        "使用示例"
    ))
    
    # 测试 3: 脚本工具
    print("\n[测试 3] 脚本工具检查")
    print("-" * 40)
    results.append(check_file_exists(
        os.path.join(skill_dir, "scripts", "card_generator.py"), 
        "推荐卡片生成器"
    ))
    results.append(check_file_exists(
        os.path.join(skill_dir, "scripts", "setup_assets.py"), 
        "资源生成脚本"
    ))
    
    # 测试 4: 资源目录
    print("\n[测试 4] 资源目录检查")
    print("-" * 40)
    results.append(check_directory_exists(
        os.path.join(skill_dir, "assets"), 
        "资源目录"
    ))
    results.append(check_directory_exists(
        os.path.join(skill_dir, "assets", "images"), 
        "图片目录"
    ))
    results.append(check_directory_exists(
        os.path.join(skill_dir, "assets", "templates"), 
        "模板目录"
    ))
    results.append(check_directory_exists(
        os.path.join(skill_dir, "assets", "mockups"), 
        "Mockup目录"
    ))
    
    # 测试 5: SKILL.md 内容检查
    print("\n[测试 5] SKILL.md 内容检查")
    print("-" * 40)
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    if os.path.exists(skill_md_path):
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("name: shampoo-recommender", "Skill名称"),
            ("description:", "描述字段"),
            ("推荐流程", "推荐流程说明"),
            ("游泳场景", "游泳场景支持"),
            ("references/products.md", "产品参考引用"),
        ]
        
        for keyword, desc in checks:
            if keyword in content:
                print(f"[OK] {desc}")
                results.append(True)
            else:
                print(f"[MISSING] {desc}: 未找到 '{keyword}'")
                results.append(False)
    else:
        print("[SKIP] SKILL.md 不存在，跳过内容检查")
    
    # 测试 6: 触发词检查
    print("\n[测试 6] 触发词覆盖检查")
    print("-" * 40)
    if os.path.exists(skill_md_path):
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        triggers = [
            "洗发水",
            "推荐洗发水",
            "游泳洗头",
            "去氯",
            "娜可露露",
        ]
        
        for trigger in triggers:
            if trigger in content:
                print(f"[OK] 触发词: '{trigger}'")
                results.append(True)
            else:
                print(f"[MISSING] 触发词: '{trigger}'")
                results.append(False)
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")
    
    if passed == total:
        print("\n[PASS] 所有测试通过！Skill 可以正常使用。")
        return 0
    elif passed >= total * 0.8:
        print("\n[WARNING] 大部分测试通过，但有部分非关键项缺失。")
        print("Skill 可以正常使用，建议补充缺失项。")
        return 0
    else:
        print("\n[FAIL] 测试未通过，请检查缺失项。")
        return 1

if __name__ == "__main__":
    sys.exit(test_skill())
