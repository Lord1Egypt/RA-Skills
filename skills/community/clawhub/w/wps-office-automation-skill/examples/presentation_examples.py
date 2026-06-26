"""
使用示例：演示文稿处理
"""

import asyncio
import base64
from main import execute


async def example_generate_outline():
    """示例：生成PPT大纲"""
    params = {
        "action": "生成PPT大纲",
        "action_type": "generate_ppt_outline",
        "topic": "2026年度数字化转型战略规划",
        "slide_count": 12,
        "target_audience": "公司高层管理层",
        "key_points": [
            "数字化转型背景与必要性",
            "现状分析与痛点识别",
            "转型目标与战略路径",
            "关键项目与实施计划",
            "资源需求与预算规划",
            "风险评估与应对措施"
        ]
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"\n演示标题: {result['data']['title']}")
        print("\n幻灯片大纲:")
        for i, slide in enumerate(result['data']['slides'], 1):
            print(f"\n第{i}张: {slide['title']}")
            for point in slide['content']:
                print(f"  • {point}")


async def example_create_presentation():
    """示例：创建演示文稿"""
    outline = {
        "title": "产品发布会",
        "slides": [
            {
                "title": "产品发布会",
                "content": ["全新智能产品系列", "2026年3月"],
                "layout_type": "title"
            },
            {
                "title": "产品亮点",
                "content": [
                    "AI智能助手",
                    "超长续航",
                    "极致设计",
                    "无缝互联"
                ],
                "layout_type": "title_content"
            },
            {
                "title": "技术规格",
                "content": [
                    "处理器：最新AI芯片",
                    "内存：16GB",
                    "存储：512GB SSD",
                    "屏幕：15.6英寸4K"
                ],
                "layout_type": "title_content"
            },
            {
                "title": "价格与上市",
                "content": [
                    "基础版：¥5999",
                    "专业版：¥7999",
                    "旗舰版：¥9999",
                    "上市时间：2026年4月"
                ],
                "layout_type": "title_content"
            },
            {
                "title": "谢谢",
                "content": ["了解更多：www.example.com"],
                "layout_type": "title"
            }
        ]
    }
    
    params = {
        "action": "创建PPT",
        "action_type": "create_presentation",
        "outline": outline,
        "style": "business",
        "include_images": False
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        
        file_data = base64.b64decode(result["file_data"])
        with open("产品发布会.pptx", "wb") as f:
            f.write(file_data)
        print(f"✓ 文件已保存: {result['file_name']}")


async def example_create_tech_presentation():
    """示例：创建科技风格演示文稿"""
    outline = {
        "title": "技术架构演进",
        "slides": [
            {
                "title": "技术架构演进",
                "content": ["从单体到微服务", "2026技术规划"],
                "layout_type": "title"
            },
            {
                "title": "当前架构",
                "content": [
                    "单体应用",
                    "紧耦合",
                    "扩展困难",
                    "维护成本高"
                ],
                "layout_type": "title_content"
            },
            {
                "title": "目标架构",
                "content": [
                    "微服务架构",
                    "容器化部署",
                    "服务网格",
                    "云原生"
                ],
                "layout_type": "title_content"
            },
            {
                "title": "实施路线",
                "content": [
                    "Q1: 服务拆分",
                    "Q2: 容器化",
                    "Q3: 服务网格",
                    "Q4: 全面上云"
                ],
                "layout_type": "title_content"
            },
            {
                "title": "谢谢",
                "content": ["技术团队"],
                "layout_type": "title"
            }
        ]
    }
    
    params = {
        "action": "创建科技风格PPT",
        "action_type": "create_presentation",
        "outline": outline,
        "style": "tech"
    }
    
    result = await execute(params)
    
    if result["success"]:
        file_data = base64.b64decode(result["file_data"])
        with open("技术架构演进.pptx", "wb") as f:
            f.write(file_data)
        print(f"✓ 科技风格PPT创建成功")


async def main():
    """运行所有示例"""
    print("=" * 60)
    print("示例1: 生成PPT大纲")
    print("=" * 60)
    await example_generate_outline()
    
    print("\n" + "=" * 60)
    print("示例2: 创建商务演示文稿")
    print("=" * 60)
    await example_create_presentation()
    
    print("\n" + "=" * 60)
    print("示例3: 创建科技风格演示文稿")
    print("=" * 60)
    await example_create_tech_presentation()


if __name__ == "__main__":
    asyncio.run(main())
