#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Word文档创建器 - 使用示例
演示如何调用工业级Word文档创建函数
"""

import sys
import os
import json

# 添加技能目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# 导入核心函数
from word_creator import create_robust_word_doc, WORD_STYLE_CONFIG

def example_1_basic_usage():
    """示例1：基础用法"""
    print("📋 示例1：基础用法")
    
    title = "华为未来二十年发展展望"
    
    content_paragraphs = [
        "中国作为世界第二大经济体，在全球经济格局中扮演着举足轻重的角色。",
        "从经济总量来看，中国GDP持续稳步增长，展现出强大的经济韧性。",
        "未来二十年，随着科技创新和产业升级，中国经济结构将进一步优化。",
        "绿色能源、人工智能、生物医药等领域将成为新的增长引擎。",
        "同时，中国将继续推动高水平对外开放，与世界各国共享发展机遇。"
    ]
    
    output_path = r"E:\Desktop\华为未来二十年.docx"
    
    # 调用函数
    success = create_robust_word_doc(
        title=title,
        content_paragraphs=content_paragraphs,
        output_path=output_path,
        verbose=True
    )
    
    if success:
        print("✅ 示例1执行成功！")
    else:
        print("❌ 示例1执行失败！")
    
    return success

def example_2_custom_config():
    """示例2：自定义样式配置"""
    print("\n📋 示例2：自定义样式配置")
    
    title = "中美关系分析报告"
    
    content_paragraphs = [
        "中美作为世界上最大的两个经济体，其关系对全球格局具有深远影响。",
        "经济上，两国贸易往来密切，相互依存度较高。",
        "科技领域，竞争与合作并存，尤其在人工智能、半导体等前沿技术领域。",
        "地缘政治方面，双方在亚太地区存在战略博弈。",
        "未来，中美关系需要在竞争中找到合作空间，共同应对全球性挑战。"
    ]
    
    output_path = r"E:\Desktop\中美关系分析.docx"
    
    # 自定义配置
    custom_config = {
        'title_font_size': 20,           # 更大标题
        'normal_font_size': 11,          # 稍小正文
        'font_family': '宋体',           # 使用宋体
        'line_spacing': 1.8,             # 更大行距
        'title_color': (0, 51, 102),     # 深蓝色标题
        'save_temp_blank': False,        # 不保存临时文件
    }
    
    # 调用函数
    success = create_robust_word_doc(
        title=title,
        content_paragraphs=content_paragraphs,
        output_path=output_path,
        config=custom_config,
        verbose=True
    )
    
    if success:
        print("✅ 示例2执行成功！")
    else:
        print("❌ 示例2执行失败！")
    
    return success

def example_3_command_line_usage():
    """示例3：命令行调用方式"""
    print("\n📋 示例3：命令行调用方式")
    
    # 准备参数
    title = "技术文档模板"
    
    content_list = [
        "第一章：项目概述",
        "第二章：技术架构",
        "第三章：实施计划",
        "第四章：风险评估",
        "第五章：总结与展望"
    ]
    
    # 转换为JSON字符串
    content_json = json.dumps(content_list, ensure_ascii=False)
    
    output_path = r"E:\Desktop\技术文档模板.docx"
    
    # 构建命令行
    cmd = f'python scripts/word_creator.py --title "{title}" --content \'{content_json}\' --output "{output_path}"'
    
    print(f"命令行调用示例：")
    print(f"  {cmd}")
    
    # 实际执行（注释掉，仅展示）
    # import subprocess
    # result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # print(result.stdout)
    # print(result.stderr)
    
    print("📝 注意：实际使用时请取消注释执行代码")
    
    return True

def example_4_advanced_features():
    """示例4：高级功能演示"""
    print("\n📋 示例4：高级功能演示")
    
    # 演示如何修改默认配置
    print("默认样式配置：")
    for key, value in WORD_STYLE_CONFIG.items():
        if not callable(value):
            print(f"  {key}: {value}")
    
    # 演示如何批量生成文档
    print("\n批量生成文档示例：")
    
    documents = [
        {
            "title": "第一季度报告",
            "content": ["销售数据", "市场分析", "下季度计划"],
            "output": r"E:\Desktop\Q1报告.docx"
        },
        {
            "title": "项目总结",
            "content": ["项目背景", "完成情况", "经验教训"],
            "output": r"E:\Desktop\项目总结.docx"
        }
    ]
    
    for doc_info in documents:
        print(f"\n生成文档: {doc_info['title']}")
        # 实际调用代码（注释掉）
        # success = create_robust_word_doc(
        #     title=doc_info['title'],
        #     content_paragraphs=doc_info['content'],
        #     output_path=doc_info['output'],
        #     verbose=False
        # )
    
    return True

def main():
    """主函数：运行所有示例"""
    print("=" * 60)
    print("Word文档创建器 - 使用示例演示")
    print("=" * 60)
    
    results = []
    
    # 运行示例1
    results.append(("示例1：基础用法", example_1_basic_usage()))
    
    # 运行示例2
    results.append(("示例2：自定义配置", example_2_custom_config()))
    
    # 运行示例3
    results.append(("示例3：命令行调用", example_3_command_line_usage()))
    
    # 运行示例4
    results.append(("示例4：高级功能", example_4_advanced_features()))
    
    # 打印总结
    print("\n" + "=" * 60)
    print("示例执行总结：")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{name}: {status}")
    
    print("\n📚 技能文件位置：")
    print(f"  SKILL.md: skills/word-document-creator/SKILL.md")
    print(f"  核心脚本: skills/word-document-creator/scripts/word_creator.py")
    print(f"  使用示例: skills/word-document-creator/examples/example_usage.py")
    
    print("\n🚀 现在您可以通过以下方式使用：")
    print("  1. 直接导入函数使用")
    print("  2. 命令行调用")
    print("  3. 作为OpenClaw技能调用")

if __name__ == "__main__":
    main()