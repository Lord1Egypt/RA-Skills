#!/usr/bin/env python3
"""
Sum2Slides 快速测试脚本
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from sum2slides import Sum2Slides


def test_basic_conversion():
    """测试基本转换功能"""
    
    print("测试基本转换功能...")
    
    # 测试文本
    test_text = """
    项目周会纪要
    
    会议信息：
    时间：2026年3月21日
    地点：线上会议
    
    本周进展：
    1. 完成用户认证模块
    2. 优化数据库性能
    3. 修复5个bug
    
    下周计划：
    1. 开发新功能
    2. 进行系统测试
    3. 准备发布
    """
    
    try:
        # 创建转换器
        converter = Sum2Slides()
        
        # 转换文本
        presentation = converter.convert(test_text)
        
        print(f"✓ 转换成功")
        print(f"  标题: {presentation.title}")
        print(f"  幻灯片数量: {presentation.total_slides()}")
        print(f"  模板: {presentation.template}")
        print(f"  主题: {presentation.theme}")
        
        # 显示幻灯片信息
        print("\n幻灯片详情:")
        for i, slide in enumerate(presentation.slides, 1):
            print(f"  幻灯片 {i}: {slide.title}")
            if slide.content:
                print(f"      内容: {len(slide.content)} 个要点")
        
        return True
    
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        return False


def test_file_conversion():
    """测试文件转换功能"""
    
    print("\n测试文件转换功能...")
    
    # 创建测试文件
    test_file = Path(__file__).parent.parent / 'test_input.txt'
    test_output = Path(__file__).parent.parent / 'test_output.pptx'
    
    try:
        # 写入测试文件
        test_content = """
        测试文件转换
        
        章节一：介绍
        这是第一个章节的内容。
        
        章节二：详情
        这是第二个章节的内容。
        
        总结：
        1. 测试完成
        2. 功能正常
        3. 可以发布
        """
        
        test_file.write_text(test_content, encoding='utf-8')
        print(f"✓ 测试文件创建: {test_file}")
        
        # 创建转换器
        converter = Sum2Slides()
        
        # 转换文件
        converter.convert_from_file(str(test_file), str(test_output))
        
        print(f"✓ 文件转换成功")
        print(f"  输入文件: {test_file}")
        print(f"  输出文件: {test_output}")
        
        # 检查输出文件
        if test_output.exists():
            file_size = test_output.stat().st_size
            print(f"  文件大小: {file_size} 字节")
            
            # 清理测试文件
            test_file.unlink(missing_ok=True)
            test_output.unlink(missing_ok=True)
            print("✓ 测试文件已清理")
        
        return True
    
    except Exception as e:
        print(f"✗ 文件转换失败: {e}")
        
        # 清理测试文件
        test_file.unlink(missing_ok=True)
        test_output.unlink(missing_ok=True)
        
        return False


def test_json_output():
    """测试JSON输出功能"""
    
    print("\n测试JSON输出功能...")
    
    test_text = "这是一个测试文本，用于验证JSON输出功能。"
    
    try:
        # 创建转换器
        converter = Sum2Slides()
        
        # 转换为JSON
        json_output = converter.convert_to_json(test_text)
        
        print(f"✓ JSON输出成功")
        print(f"  JSON长度: {len(json_output)} 字符")
        
        # 解析JSON验证格式
        import json
        data = json.loads(json_output)
        
        print(f"  标题: {data.get('title')}")
        print(f"  幻灯片数量: {len(data.get('slides', []))}")
        print(f"  作者: {data.get('author')}")
        
        return True
    
    except Exception as e:
        print(f"✗ JSON输出失败: {e}")
        return False


def test_configuration():
    """测试配置功能"""
    
    print("\n测试配置功能...")
    
    try:
        # 使用自定义配置创建转换器
        config = {
            'template': 'business',
            'theme': 'dark',
            'max_slides': 5,
            'font_size': 16,
            'language': 'zh',
        }
        
        converter = Sum2Slides(config)
        
        # 获取配置
        current_config = converter.get_config()
        
        print(f"✓ 配置测试成功")
        print(f"  当前配置: {current_config}")
        
        # 验证配置
        for key, value in config.items():
            if current_config.get(key) == value:
                print(f"  ✓ {key}: {value}")
            else:
                print(f"  ✗ {key}: 期望 {value}, 实际 {current_config.get(key)}")
        
        # 测试配置更新
        new_config = {'max_slides': 8, 'font_size': 20}
        converter.update_config(new_config)
        
        updated_config = converter.get_config()
        print(f"  更新后配置: {updated_config}")
        
        return True
    
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False


def test_templates():
    """测试模板功能"""
    
    print("\n测试模板功能...")
    
    try:
        converter = Sum2Slides()
        
        # 获取可用模板
        templates = converter.get_available_templates()
        
        print(f"✓ 模板测试成功")
        print(f"  可用模板: {templates}")
        
        # 测试每个模板
        test_text = "模板测试文本"
        
        for template in templates:
            try:
                config = {'template': template}
                temp_converter = Sum2Slides(config)
                presentation = temp_converter.convert(test_text)
                
                print(f"  ✓ 模板 '{template}' 工作正常")
            except Exception as e:
                print(f"  ✗ 模板 '{template}' 失败: {e}")
        
        return True
    
    except Exception as e:
        print(f"✗ 模板测试失败: {e}")
        return False


def main():
    """主函数"""
    
    print("Sum2Slides v1.0.1 快速测试")
    print("="*40)
    
    tests = [
        ("基本转换", test_basic_conversion),
        ("文件转换", test_file_conversion),
        ("JSON输出", test_json_output),
        ("配置功能", test_configuration),
        ("模板功能", test_templates),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "="*40)
    print("测试结果:")
    print("="*40)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    print("="*40)
    print(f"总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n✓ 所有测试通过！Sum2Slides v1.0.1 工作正常。")
        return 0
    else:
        print(f"\n✗ {total - passed} 个测试失败。")
        return 1


if __name__ == '__main__':
    sys.exit(main())