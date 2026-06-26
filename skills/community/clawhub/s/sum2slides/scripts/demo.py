#!/usr/bin/env python3
"""
Sum2Slides 使用演示脚本
展示Sum2Slides的主要功能和输出效果
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

try:
    from sum2slides import Sum2Slides
    from sum2slides.utils import file
except ImportError:
    print("❌ 无法导入Sum2Slides，请先安装依赖")
    print("运行: pip install -e .")
    sys.exit(1)


def create_demo_outputs():
    """创建演示输出"""
    
    print("🎬 Sum2Slides v1.0.1 使用演示")
    print("=" * 50)
    
    # 创建输出目录
    output_dir = project_root / "demo_outputs"
    output_dir.mkdir(exist_ok=True)
    
    # 创建转换器实例
    converter = Sum2Slides()
    
    # 演示1：基本文本转换
    print("\n📝 演示1：基本文本转换")
    print("-" * 30)
    
    basic_text = """项目总结报告

项目名称：AI助手开发
项目周期：2026年1月-3月
项目状态：已完成

关键成果：
1. 完成核心架构设计
2. 实现基础功能模块
3. 通过测试验证
4. 用户反馈良好

技术亮点：
• 采用模块化设计
• 支持多平台运行
• 性能优化显著

下一步计划：
1. 功能扩展
2. 性能优化
3. 用户界面改进"""
    
    print("输入文本长度:", len(basic_text), "字符")
    
    try:
        presentation = converter.convert(basic_text)
        output_path = output_dir / "basic_demo.pptx"
        presentation.save(str(output_path))
        print(f"✅ 生成成功: {output_path}")
        print(f"   文件大小: {output_path.stat().st_size / 1024:.1f} KB")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
    
    # 演示2：使用商务模板
    print("\n💼 演示2：使用商务模板")
    print("-" * 30)
    
    business_text = """季度业务报告

Q1 2026 业绩总结
• 营收增长：+25%
• 客户增长：+15%
• 市场份额：提升3%

主要成就：
1. 新产品发布成功
2. 客户满意度提升
3. 团队效率提高

挑战与应对：
• 市场竞争加剧 → 差异化策略
• 成本压力增加 → 优化运营
• 人才需求增长 → 加强培训

Q2 目标：
1. 营收增长30%
2. 新客户获取20%
3. 产品创新加速"""
    
    business_converter = Sum2Slides(template="business", theme="light")
    try:
        presentation = business_converter.convert(business_text)
        output_path = output_dir / "business_demo.pptx"
        presentation.save(str(output_path))
        print(f"✅ 生成成功: {output_path}")
        print(f"   使用模板: business, 主题: light")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
    
    # 演示3：使用学术模板
    print("\n🎓 演示3：使用学术模板")
    print("-" * 30)
    
    academic_text = """研究论文：人工智能在教育中的应用

摘要
本研究探讨了AI技术在现代教育中的应用现状和发展趋势。

研究背景
1. 教育信息化快速发展
2. AI技术日益成熟
3. 个性化学习需求增长

研究方法
• 文献综述法
• 案例分析法
• 实证研究法

研究结果
1. AI提升教学效率30%
2. 学生满意度提高25%
3. 个性化学习效果显著

结论与建议
1. AI在教育中具有广阔应用前景
2. 需要加强教师培训
3. 关注数据隐私和安全"""
    
    academic_converter = Sum2Slides(template="academic", theme="light", max_slides=8)
    try:
        presentation = academic_converter.convert(academic_text)
        output_path = output_dir / "academic_demo.pptx"
        presentation.save(str(output_path))
        print(f"✅ 生成成功: {output_path}")
        print(f"   使用模板: academic, 最大幻灯片数: 8")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
    
    # 演示4：从文件转换
    print("\n📄 演示4：从文件转换")
    print("-" * 30)
    
    # 创建示例文件
    sample_file = output_dir / "sample_input.txt"
    sample_content = """会议纪要

会议主题：项目进度评审
会议时间：2026-03-29 14:00
参会人员：项目组全体成员

会议内容：
1. 项目整体进度：75%
2. 本周完成工作：
   • 完成用户界面优化
   • 修复已知bug
   • 更新项目文档
3. 下周计划：
   • 进行系统测试
   • 准备发布材料
   • 安排用户培训

决议事项：
1. 增加测试资源
2. 调整发布时间
3. 加强沟通协调"""
    
    file.write_file(str(sample_file), sample_content)
    
    try:
        # 读取文件内容
        content = file.read_file(str(sample_file))
        presentation = converter.convert(content)
        output_path = output_dir / "file_demo.pptx"
        presentation.save(str(output_path))
        print(f"✅ 生成成功: {output_path}")
        print(f"   输入文件: {sample_file}")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
    
    # 演示5：高级配置
    print("\n⚙️ 演示5：高级配置演示")
    print("-" * 30)
    
    advanced_converter = Sum2Slides(
        template="default",
        theme="dark",
        max_slides=6,
        font_size=16,
        title_size=32,
        bullet_style="circle"
    )
    
    advanced_text = """技术分享：Python最佳实践

内容概要：
1. 代码规范与风格
2. 性能优化技巧
3. 错误处理策略
4. 测试驱动开发

代码规范：
• 遵循PEP 8
• 使用类型提示
• 添加文档字符串
• 保持代码简洁

性能优化：
1. 使用适当的数据结构
2. 避免不必要的计算
3. 利用缓存机制
4. 并行处理优化

总结：
Python开发需要注重代码质量、性能和可维护性。"""
    
    try:
        presentation = advanced_converter.convert(advanced_text)
        output_path = output_dir / "advanced_demo.pptx"
        presentation.save(str(output_path))
        print(f"✅ 生成成功: {output_path}")
        print(f"   配置: theme=dark, font_size=16, bullet_style=circle")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
    
    # 总结
    print("\n" + "=" * 50)
    print("🎉 演示完成！")
    print(f"所有输出文件保存在: {output_dir}")
    print("\n📊 演示总结：")
    print("1. 基本文本转换 - 快速生成演示文稿")
    print("2. 商务模板 - 专业商务演示")
    print("3. 学术模板 - 学术研究展示")
    print("4. 文件转换 - 从文件自动生成")
    print("5. 高级配置 - 自定义样式和布局")
    print("\n🚀 下一步：")
    print("• 查看生成的PPTX文件")
    print("• 尝试修改输入文本")
    print("• 探索更多配置选项")
    print("• 阅读文档了解更多功能")


if __name__ == "__main__":
    create_demo_outputs()