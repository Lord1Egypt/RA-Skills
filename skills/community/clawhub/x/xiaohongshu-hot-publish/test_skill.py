#!/usr/bin/env python3
"""
测试小红书热点发布系统技能
验证所有功能正常工作

版本: 1.1.0
"""

import os
import sys
import tempfile
import json
import webbrowser
from create_hot_publish_page import XiaohongshuHotPublishGenerator

def print_test_header(test_name: str):
    """打印测试标题"""
    print(f"\n🧪 {test_name}")
    print("-" * 50)

def test_basic_functionality():
    """测试1：基本功能测试"""
    print_test_header("基本功能测试")
    
    # 创建生成器
    generator = XiaohongshuHotPublishGenerator(
        theme="Python编程测试",
        brand_name="测试品牌"
    )
    
    # 生成内容
    contents = generator.generate_contents(3)
    
    # 验证内容生成
    assert len(contents) == 3, f"预期生成3个内容，实际生成{len(contents)}个"
    print(f"✅ 成功生成{len(contents)}个内容")
    
    # 验证每个内容的结构
    required_fields = ['title', 'content', 'tags', 'time_suggestion', 'emoji', 'content_type', 'published', 'word_count']
    
    for i, content in enumerate(contents, 1):
        for field in required_fields:
            assert field in content, f"内容{i}缺少{field}字段"
        
        # 验证具体字段值
        assert content['title'], f"内容{i}的title不能为空"
        assert content['content'], f"内容{i}的content不能为空"
        assert len(content['tags']) >= 3, f"内容{i}的标签数量不足"
        assert content['word_count'] > 0, f"内容{i}的字数应该大于0"
        
        print(f"✅ 内容{i}结构完整: {content['title'][:30]}...")
    
    return generator

def test_html_generation():
    """测试2：HTML生成测试"""
    print_test_header("HTML生成测试")
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        # 生成HTML页面
        generator = XiaohongshuHotPublishGenerator(
            theme="AI学习测试",
            brand_name="AI学习社区"
        )
        
        generator.generate_contents(2)
        html_content = generator.generate_html_page(temp_file)
        
        # 验证HTML文件
        assert os.path.exists(temp_file), "HTML文件未生成"
        assert os.path.getsize(temp_file) > 0, "HTML文件为空"
        
        # 验证HTML内容
        with open(temp_file, 'r', encoding='utf-8') as f:
            html = f.read()
            assert '<!DOCTYPE html>' in html, "HTML缺少DOCTYPE声明"
            assert '<title>' in html, "HTML缺少title标签"
            assert '小红书热点一键发布' in html, "HTML缺少标题"
            assert 'AI学习测试' in html, "HTML缺少主题内容"
            assert '{{' not in html, "HTML中还有未替换的模板变量"
            
        print(f"✅ HTML文件生成成功: {temp_file}")
        print(f"✅ 文件大小: {os.path.getsize(temp_file):,} 字节")
        
        # 验证JSON文件
        json_file = temp_file.replace('.html', '.json')
        assert os.path.exists(json_file), "JSON文件未生成"
        assert os.path.getsize(json_file) > 0, "JSON文件为空"
        
        # 验证JSON结构
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert 'theme' in data, "JSON缺少theme字段"
            assert 'contents' in data, "JSON缺少contents字段"
            assert 'metadata' in data, "JSON缺少metadata字段"
            
        print(f"✅ JSON文件生成成功: {json_file}")
        print(f"✅ JSON结构验证通过")
        
        return temp_file
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        json_file = temp_file.replace('.html', '.json')
        if os.path.exists(json_file):
            os.unlink(json_file)

def test_content_types():
    """测试3：内容类型测试"""
    print_test_header("内容类型测试")
    
    test_themes = [
        ("Python编程", "技术类"),
        ("AI学习", "学习类"),
        ("工作效率", "效率类"),
        ("健身计划", "健康类"),
        ("旅行攻略", "生活类"),
        ("美食烹饪", "美食类")
    ]
    
    for theme, category in test_themes:
        generator = XiaohongshuHotPublishGenerator(theme=theme)
        contents = generator.generate_contents(2)
        
        # 验证内容类型多样性
        content_types = set([c['content_type'] for c in contents])
        assert len(content_types) >= 1, f"{category}主题应该生成至少1种内容类型"
        
        print(f"✅ {category}主题 '{theme}' 生成成功")
        print(f"   生成类型: {', '.join(content_types)}")
        print(f"   标签示例: {', '.join(contents[0]['tags'][:3])}")

def test_time_suggestions():
    """测试4：时间建议测试"""
    print_test_header("时间建议测试")
    
    generator = XiaohongshuHotPublishGenerator(theme="时间测试")
    contents = generator.generate_contents(5)
    
    print("时间建议分布:")
    for i, content in enumerate(contents, 1):
        time_suggestion = content['time_suggestion']
        print(f"  内容{i}: {time_suggestion['display']} (状态: {time_suggestion['status']})")
    
    # 验证第一个内容应该是"now"状态
    assert contents[0]['time_suggestion']['status'] == 'now', "第一个内容应该是立即发布状态"
    
    # 验证时间格式
    for content in contents:
        time_str = content['time_suggestion']['time']
        assert ':' in time_str, f"时间格式错误: {time_str}"
        hour, minute = time_str.split(':')
        assert 0 <= int(hour) <= 23, f"小时超出范围: {hour}"
        assert 0 <= int(minute) <= 59, f"分钟超出范围: {minute}"
    
    print("✅ 时间建议逻辑正确")
    print("✅ 时间格式验证通过")

def test_template_loading():
    """测试5：模板加载测试"""
    print_test_header("模板加载测试")
    
    # 测试模板文件存在
    template_path = os.path.join(os.path.dirname(__file__), 'template.html')
    assert os.path.exists(template_path), f"模板文件不存在: {template_path}"
    
    # 读取模板内容
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # 验证模板关键部分
    required_variables = ['{{BRAND_NAME}}', '{{CONTENT_SELECTOR}}', '{{CONTENT_SECTIONS}}', '{{JS_DATA}}']
    
    for var in required_variables:
        assert var in template_content, f"模板缺少变量: {var}"
    
    # 验证CSS样式存在
    assert '<style>' in template_content, "模板缺少style标签"
    assert '</style>' in template_content, "模板缺少style结束标签"
    
    # 验证JavaScript存在
    assert '<script>' in template_content, "模板缺少script标签"
    assert '</script>' in template_content, "模板缺少script结束标签"
    
    print(f"✅ 模板文件加载成功: {template_path}")
    print(f"✅ 模板大小: {len(template_content):,} 字符")
    print(f"✅ 所有模板变量存在")

def test_error_handling():
    """测试6：错误处理测试"""
    print_test_header("错误处理测试")
    
    # 测试空主题
    try:
        generator = XiaohongshuHotPublishGenerator(theme="", brand_name="测试")
        assert False, "空主题应该抛出异常"
    except ValueError as e:
        print(f"✅ 空主题验证通过: {e}")
    
    # 测试空品牌
    try:
        generator = XiaohongshuHotPublishGenerator(theme="测试", brand_name="")
        assert False, "空品牌应该抛出异常"
    except ValueError as e:
        print(f"✅ 空品牌验证通过: {e}")
    
    # 测试无效内容数量
    generator = XiaohongshuHotPublishGenerator(theme="测试", brand_name="测试")
    try:
        generator.generate_contents(0)
        assert False, "内容数量0应该抛出异常"
    except ValueError as e:
        print(f"✅ 内容数量0验证通过: {e}")
    
    try:
        generator.generate_contents(6)
        assert False, "内容数量6应该抛出异常"
    except ValueError as e:
        print(f"✅ 内容数量6验证通过: {e}")
    
    # 测试未生成内容时生成HTML
    generator = XiaohongshuHotPublishGenerator(theme="测试", brand_name="测试")
    try:
        generator.generate_html_page()
        assert False, "未生成内容时生成HTML应该抛出异常"
    except ValueError as e:
        print(f"✅ 未生成内容验证通过: {e}")

def test_performance():
    """测试7：性能测试"""
    print_test_header("性能测试")
    
    import time
    
    # 测试生成速度
    start_time = time.time()
    
    generator = XiaohongshuHotPublishGenerator(
        theme="性能测试主题",
        brand_name="性能测试品牌"
    )
    
    # 生成最大数量的内容
    contents = generator.generate_contents(5)
    
    # 生成HTML页面到临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        generator.generate_html_page(temp_file)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"✅ 生成5个内容 + HTML页面耗时: {elapsed_time:.2f}秒")
        print(f"✅ 平均每个内容: {(elapsed_time/5):.2f}秒")
        
        # 验证性能要求（应该在3秒内完成）
        assert elapsed_time < 3.0, f"生成时间过长: {elapsed_time:.2f}秒"
        
        # 验证文件大小合理
        file_size = os.path.getsize(temp_file)
        print(f"✅ HTML文件大小: {file_size:,} 字节")
        assert 10000 < file_size < 100000, f"文件大小异常: {file_size}字节"
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        json_file = temp_file.replace('.html', '.json')
        if os.path.exists(json_file):
            os.unlink(json_file)

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始测试小红书热点发布系统技能")
    print("=" * 60)
    
    test_results = []
    
    try:
        # 运行测试
        test_results.append(("基本功能", test_basic_functionality()))
        test_results.append(("HTML生成", test_html_generation()))
        test_results.append(("内容类型", test_content_types()))
        test_results.append(("时间建议", test_time_suggestions()))
        test_results.append(("模板加载", test_template_loading()))
        test_results.append(("错误处理", test_error_handling()))
        test_results.append(("性能测试", test_performance()))
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！")
        print("\n📊 测试结果汇总:")
        print("-" * 40)
        
        for test_name, _ in test_results:
            print(f"  ✅ {test_name}")
        
        print(f"\n✨ 总共通过 {len(test_results)} 项测试")
        print("🚀 技能功能正常，可以投入使用。")
        
        # 询问是否打开示例页面
        choice = input("\n是否生成示例页面查看效果？(y/n): ").strip().lower()
        if choice == 'y':
            # 生成示例页面
            generator = XiaohongshuHotPublishGenerator(
                theme="测试演示",
                brand_name="测试系统"
            )
            generator.generate_contents(3)
            
            demo_file = "test_demo_output.html"
            generator.generate_html_page(demo_file)
            
            print(f"✅ 示例页面已生成: {demo_file}")
            
            # 询问是否在浏览器中打开
            if input("是否在浏览器中打开？(y/n): ").strip().lower() == 'y':
                webbrowser.open(f'file://{os.path.abspath(demo_file)}')
                print("🌐 已在浏览器中打开页面")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)