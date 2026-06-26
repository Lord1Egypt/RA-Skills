#!/usr/bin/env python3
"""
豆包视觉模型集成使用示例
演示如何在tianji-fengshui技能中使用豆包图片分析功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

def example_1_direct_api_call():
    """示例1: 直接调用豆包视觉分析器"""
    print("📋 示例1: 直接调用豆包视觉分析器")
    print("=" * 60)
    
    from doubao_vision_integration import DoubaoVisionAnalyzer
    
    # 初始化分析器
    analyzer = DoubaoVisionAnalyzer("config_enhanced.json")
    
    # 如果需要，可以动态设置API密钥
    # analyzer.set_api_key("从全局配置获取")
    
    # 测试图片路径（使用占位符）
    test_image = "/path/to/your/palm_image.jpg"
    
    if os.path.exists(test_image):
        print(f"📸 使用测试图片: {test_image}")
        
        # 方法A: 分析掌纹（详细）
        print("\n🖐️ 方法A: 详细掌纹分析")
        result = analyzer.analyze_palm(test_image, detailed=True)
        
        if result["success"]:
            print(f"✅ 分析成功！响应时间: {result.get('response_time', 0):.2f}秒")
            # [安全] 已移除API密钥打印.get('total_tokens', '未知')}")
            print("\n📋 分析结果摘要:")
            analysis = result["analysis"]
            lines = analysis.split('\n')
            for line in lines[:10]:  # 显示前10行
                if line.strip():
                    print(f"  {line}")
            if len(lines) > 10:
                print(f"  ... (共{len(lines)}行)")
        else:
            print(f"❌ 分析失败: {result.get('error', '未知错误')}")
        
        # 方法B: 简要掌纹分析
        print("\n🖐️ 方法B: 简要掌纹分析")
        result = analyzer.analyze_palm(test_image, detailed=False)
        
        if result["success"]:
            print(f"✅ 简要分析成功！")
            # [安全] 已移除API密钥打印.get('total_tokens', '未知')}")
        else:
            print(f"❌ 简要分析失败: {result.get('error', '未知错误')}")
            
    else:
        print(f"⚠️  测试图片不存在: {test_image}")
        print("💡 请准备测试图片到指定路径")

def example_2_enhanced_processor():
    """示例2: 使用增强版天机处理器"""
    print("\n\n📋 示例2: 使用增强版天机处理器")
    print("=" * 60)
    
    from tianji_core_enhanced import TianjiProcessor
    
    # 初始化处理器
    processor = TianjiProcessor("config_enhanced.json")
    
    # 测试不同的用户请求
    test_requests = [
        "豆包分析掌纹图片 /path/to/your/palm_image.jpg",
        "分析办公室风水 /path/to/your/office_image.jpg",
        "八字分析 1990年1月1日 子时 男",
        "你好，玄机子，你能做什么？",
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. 请求: {request[:50]}...")
        print("-" * 50)
        
        # 检测请求类型
        request_type, details = processor.detect_request_type(request)
        print(f"   检测类型: {request_type}")
        
        if "file_path" in details:
            print(f"   文件路径: {details['file_path']}")
        
        # 处理请求
        response = processor.process_request(request)
        
        # 显示响应摘要
        lines = response.split('\n')
        for line in lines[:5]:  # 显示前5行
            if line.strip():
                print(f"   响应: {line}")
        if len(lines) > 5:
            print(f"   ... (共{len(lines)}行)")

def example_3_command_line_usage():
    """示例3: 命令行使用方式"""
    print("\n\n📋 示例3: 命令行使用方式")
    print("=" * 60)
    
    print("方法1: 直接调用豆包视觉分析器")
    print("  python3 doubao_vision_integration.py \\")
    # [安全] 已移除API密钥打印
    print("    /path/to/image.jpg palm")
    print("")
    print("方法2: 使用增强版天机处理器")
    print("  python3 tianji_core_enhanced.py \\")
    print("    \"豆包分析掌纹图片 /path/to/palm.jpg\"")
    print("")
    print("方法3: 在OpenClaw中集成使用")
    print("  1. 将config_enhanced.json重命名为config.json")
    print("  2. 更新tianji_core.py以集成新功能")
    print("  3. 通过OpenClaw会话调用玄机子技能")

def example_4_integration_with_openclaw():
    """示例4: 与OpenClaw集成"""
    print("\n\n📋 示例4: 与OpenClaw集成建议")
    print("=" * 60)
    
    print("1. 更新现有配置:")
    print("  cp config_enhanced.json config.json")
    print("")
    print("2. 更新核心处理器（可选）:")
    print("  cp tianji_core_enhanced.py tianji_core.py")
    print("  或修改现有tianji_core.py集成豆包功能")
    print("")
    print("3. 测试集成功能:")
    print("  python3 tianji_core.py \\")
    print("    \"豆包分析掌纹图片 /tmp/test_images/example_image.jpg\"")
    print("")
    print("4. 在OpenClaw会话中使用:")
    print("  用户: 玄机子，帮我分析这张掌纹图片")
    print("  系统: 自动调用豆包视觉模型进行分析")
    print("  返回: 专业的掌纹分析报告")

def main():
    """主函数"""
    print("🧭 玄机子·豆包视觉模型集成使用示例")
    print("=" * 60)
    
    # 运行示例
    example_1_direct_api_call()
    example_2_enhanced_processor()
    example_3_command_line_usage()
    example_4_integration_with_openclaw()
    
    print("\n" + "=" * 60)
    print("🎯 集成完成！您现在可以:")
    print("1. 使用豆包视觉模型分析掌纹、风水等图片")
    print("2. 通过命令行或代码调用分析功能")
    print("3. 将功能集成到OpenClaw工作流中")
    print("4. 扩展支持更多图片分析场景")
    print("=" * 60)

if __name__ == "__main__":
    main()