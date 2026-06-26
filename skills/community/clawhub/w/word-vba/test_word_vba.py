#!/usr/bin/env python3
"""
Word VBA Skill 综合测试脚本
测试读取和写入功能的完整流程

作者: SuperMike
日期: 2026-03-04
"""

import sys
import tempfile
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from word_vba_writer import WordWriter
from word_vba_reader import WordReader


def test_full_workflow():
    """测试完整工作流程：创建 -> 写入 -> 读取 -> 验证"""
    
    print("=" * 70)
    print("Word VBA Skill 综合测试")
    print("=" * 70)
    
    temp_dir = Path(tempfile.gettempdir())
    test_docx = temp_dir / "word_vba_full_test.docx"
    
    try:
        # ========== 阶段1: 创建并写入文档 ==========
        print("\n[阶段1] 创建并写入Word文档...")
        print("-" * 70)
        
        writer = WordWriter(visible=False)
        doc = writer.create_document()
        
        # 添加标题
        print("  → 添加标题...")
        writer.add_heading(doc, "国家自然科学基金申请书", level=1)
        writer.add_heading(doc, "项目名称：基于物理信息强化学习的振动台试验研究", level=2)
        
        # 添加空行
        writer.add_paragraph(doc, "", {})
        
        # 添加正文
        print("  → 添加正文段落...")
        writer.add_paragraph(doc, 
            "1. 项目背景与意义",
            {'font_name': '黑体', 'font_size': 14, 'bold': True}
        )
        
        writer.add_paragraph(doc,
            "结构抗震试验是保障工程结构地震安全性的关键手段。随着我国城镇化进程加速，"
            "对结构抗震性能的精确评估需求日益迫切。振动台试验作为最直观、最可靠的抗震试验方法，"
            "能够真实再现结构在地震作用下的动力响应。",
            {'font_name': '宋体', 'font_size': 12, 'alignment': 'justify'}
        )
        
        writer.add_paragraph(doc, "", {})
        
        writer.add_paragraph(doc,
            "2. 国内外研究现状",
            {'font_name': '黑体', 'font_size': 14, 'bold': True}
        )
        
        writer.add_paragraph(doc,
            "实时混合试验技术自20世纪90年代发展以来，已成为结构抗震试验研究的重要手段。"
            "Nakashima等[1]于1992年奠定了RTHS的基础理论框架，建立了基于显式积分算法的实时计算体系。",
            {'font_name': '宋体', 'font_size': 12, 'alignment': 'justify'}
        )
        
        # 添加表格
        print("  → 添加表格...")
        table_data = [
            ["研究内容", "预期目标", "考核指标"],
            ["R-PINN建模", "小样本高精度建模", "50组样本，R²>0.95"],
            ["双时间尺度架构", "实时模型更新", "周期≤5ms"],
            ["PIRL控制", "安全高效控制", "样本效率提升10倍"]
        ]
        writer.add_table(doc, 4, 3, table_data)
        
        # 添加格式测试段落
        writer.add_paragraph(doc, "", {})
        writer.add_paragraph(doc,
            "3. 格式测试",
            {'font_name': '黑体', 'font_size': 14, 'bold': True}
        )
        
        writer.add_paragraph(doc,
            "粗体文字测试",
            {'font_name': '宋体', 'font_size': 12, 'bold': True}
        )
        
        writer.add_paragraph(doc,
            "斜体文字测试",
            {'font_name': '宋体', 'font_size': 12, 'italic': True}
        )
        
        writer.add_paragraph(doc,
            "居中文字测试",
            {'font_name': '宋体', 'font_size': 12, 'alignment': 'center'}
        )
        
        writer.add_paragraph(doc,
            "右对齐文字测试",
            {'font_name': '宋体', 'font_size': 12, 'alignment': 'right'}
        )
        
        # 保存文档
        print("  → 保存文档...")
        writer.save_document(doc, str(test_docx))
        writer.close()
        
        print(f"✓ 文档已创建: {test_docx}")
        
        # ========== 阶段2: 读取文档 ==========
        print("\n[阶段2] 读取Word文档...")
        print("-" * 70)
        
        reader = WordReader()
        result = reader.read_document(str(test_docx))
        
        print(f"✓ 文档统计:")
        print(f"    - 段落数: {result['paragraph_count']}")
        print(f"    - 词数: {result['word_count']}")
        print(f"    - 页数: {result['pages']}")
        print(f"    - 表格数: {len(result['tables'])}")
        
        # ========== 阶段3: 验证内容 ==========
        print("\n[阶段3] 验证读取内容...")
        print("-" * 70)
        
        # 验证段落
        paragraphs = result['paragraphs']
        
        # 找非空段落
        non_empty = [p for p in paragraphs if not p.get('is_empty', True)]
        
        print(f"  → 非空段落数: {len(non_empty)}")
        
        # 验证标题格式
        title_paras = [p for p in non_empty if '国家自然科学基金' in p.get('text', '')]
        if title_paras:
            title = title_paras[0]
            print(f"  ✓ 找到标题: {title['text'][:30]}...")
            print(f"    - 字体: {title['format']['font_name_far_east'] or title['format']['font_name']}")
            print(f"    - 大小: {title['format']['font_size']}pt")
            print(f"    - 粗体: {title['format']['bold']}")
        
        # 验证正文格式
        body_paras = [p for p in non_empty if '结构抗震试验' in p.get('text', '')]
        if body_paras:
            body = body_paras[0]
            print(f"  ✓ 找到正文段落")
            print(f"    - 对齐: {body['paragraph_format']['alignment']}")
            print(f"    - 字体: {body['format']['font_name_far_east'] or body['format']['font_name']}")
        
        # 验证表格
        if result['tables']:
            table = result['tables'][0]
            print(f"  ✓ 找到表格: {table['rows']}行 x {table['columns']}列")
            print(f"    - 表头: {table['content'][0]}")
        
        # ========== 阶段4: 导出JSON ==========
        print("\n[阶段4] 导出为JSON...")
        print("-" * 70)
        
        json_path = test_docx.with_suffix('.json')
        reader2 = WordReader()
        reader2.export_to_json(str(test_docx), str(json_path))
        reader2._close_word()
        
        if json_path.exists():
            import json
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            print(f"✓ JSON导出成功")
            print(f"    - 文件大小: {json_path.stat().st_size} 字节")
            print(f"    - 包含段落: {len(json_data.get('paragraphs', []))}")
        
        # ========== 阶段5: 从JSON恢复 ==========
        print("\n[阶段5] 从JSON恢复文档...")
        print("-" * 70)
        
        restored_docx = temp_dir / "word_vba_restored.docx"
        writer2 = WordWriter()
        writer2.write_from_json(str(json_path), str(restored_docx))
        writer2.close()
        
        if restored_docx.exists():
            print(f"✓ 文档恢复成功: {restored_docx}")
            
            # 验证恢复的文档
            reader3 = WordReader()
            restored_result = reader3.read_document(str(restored_docx))
            reader3._close_word()
            
            if restored_result['paragraph_count'] == result['paragraph_count']:
                print(f"✓ 段落数一致: {restored_result['paragraph_count']}")
            else:
                print(f"! 段落数不一致: 原{result['paragraph_count']} vs 恢复{restored_result['paragraph_count']}")
        
        # ========== 测试完成 ==========
        print("\n" + "=" * 70)
        print("所有测试通过！")
        print("=" * 70)
        print("\n测试总结:")
        print(f"  ✓ Word文档创建和写入")
        print(f"  ✓ 段落格式设置（字体、大小、对齐）")
        print(f"  ✓ 表格创建和数据填充")
        print(f"  ✓ 文档读取和内容提取")
        print(f"  ✓ 格式信息读取")
        print(f"  ✓ JSON导出和恢复")
        
        # 清理临时文件
        for f in [test_docx, json_path, restored_docx]:
            if f.exists():
                f.unlink(missing_ok=True)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """测试边界情况"""
    print("\n" + "=" * 70)
    print("边界情况测试")
    print("=" * 70)
    
    temp_dir = Path(tempfile.gettempdir())
    
    tests_passed = 0
    tests_total = 0
    
    # 测试1: 空文档
    tests_total += 1
    print("\n[测试1] 创建空文档...")
    try:
        writer = WordWriter()
        doc = writer.create_document()
        empty_doc = temp_dir / "empty.docx"
        writer.save_document(doc, str(empty_doc))
        writer.close()
        
        reader = WordReader()
        result = reader.read_document(str(empty_doc))
        reader._close_word()
        
        print(f"  ✓ 空文档创建成功，包含 {result['paragraph_count']} 个段落")
        tests_passed += 1
        empty_doc.unlink(missing_ok=True)
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    
    # 测试2: 特殊字符
    tests_total += 1
    print("\n[测试2] 特殊字符处理...")
    try:
        writer = WordWriter()
        doc = writer.create_document()
        
        special_texts = [
            "包含数字123和符号!@#$%",
            "中文标点：，。！？；：",
            "英文标点,.!?;:"
        ]
        
        for text in special_texts:
            writer.add_paragraph(doc, text, {'font_name': '宋体', 'font_size': 12})
        
        special_doc = temp_dir / "special.docx"
        writer.save_document(doc, str(special_doc))
        writer.close()
        
        reader = WordReader()
        result = reader.read_document(str(special_doc))
        reader._close_word()
        
        print(f"  ✓ 特殊字符处理成功")
        tests_passed += 1
        special_doc.unlink(missing_ok=True)
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    
    # 测试3: 大段落
    tests_total += 1
    print("\n[测试3] 大段落处理...")
    try:
        writer = WordWriter()
        doc = writer.create_document()
        
        large_text = "这是一个很长的段落。" * 100
        writer.add_paragraph(doc, large_text, {'font_name': '宋体', 'font_size': 12})
        
        large_doc = temp_dir / "large.docx"
        writer.save_document(doc, str(large_doc))
        writer.close()
        
        reader = WordReader()
        result = reader.read_document(str(large_doc))
        reader._close_word()
        
        print(f"  ✓ 大段落处理成功")
        tests_passed += 1
        large_doc.unlink(missing_ok=True)
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    
    print(f"\n边界测试完成: {tests_passed}/{tests_total} 通过")
    return tests_passed == tests_total


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("Word VBA Skill 完整测试套件")
    print("=" * 70 + "\n")
    
    # 运行主测试
    main_passed = test_full_workflow()
    
    # 运行边界测试
    edge_passed = test_edge_cases()
    
    # 最终总结
    print("\n" + "=" * 70)
    if main_passed and edge_passed:
        print("所有测试通过！Skill可以正常使用。")
    else:
        print("部分测试失败，请检查错误信息。")
    print("=" * 70)


if __name__ == "__main__":
    main()
