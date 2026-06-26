#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自媒体文案生成器 - 主入口

用法:
    python generate.py "主题" -p [平台] -t [语气] -l [长度]
"""

import sys
import argparse
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from generator import CopywriterGenerator, GenerateRequest, Platform
from tag_recommender import TagRecommender


def main():
    parser = argparse.ArgumentParser(
        description="自媒体文案生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate.py "AI 写作技巧" -p xiaohongshu
  python generate.py "职场沟通" -p wechat -l long
  python generate.py "美妆教程" -p douyin -t 幽默
        """
    )
    
    parser.add_argument("topic", help="文案主题")
    parser.add_argument("-p", "--platform",
                       choices=["xiaohongshu", "douyin", "wechat", "zhihu"],
                       default="xiaohongshu",
                       help="目标平台 (默认：xiaohongshu)")
    parser.add_argument("-t", "--tone",
                       default="自然",
                       help="语气：自然/专业/幽默/温暖 (默认：自然)")
    parser.add_argument("-l", "--length",
                       choices=["short", "medium", "long"],
                       default="medium",
                       help="长度 (默认：medium)")
    parser.add_argument("-k", "--keywords",
                       nargs="+",
                       help="关键词")
    parser.add_argument("-a", "--audience",
                       help="目标受众")
    parser.add_argument("-o", "--output",
                       help="输出文件路径")
    parser.add_argument("--no-tags",
                       action="store_true",
                       help="不生成标签")
    parser.add_argument("--titles-only",
                       action="store_true",
                       help="只生成标题选项")
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = CopywriterGenerator()
    tag_recommender = TagRecommender()
    
    # 构建请求
    request = GenerateRequest(
        topic=args.topic,
        platform=Platform(args.platform),
        tone=args.tone,
        length=args.length,
        keywords=args.keywords,
        target_audience=args.audience
    )
    
    # 只生成标题
    if args.titles_only:
        from generator import generate_titles
        titles = generate_titles(args.topic, count=10)
        print("📝 标题选项：\n")
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")
        return
    
    # 生成文案
    print(f"📝 正在生成{args.platform}文案...\n")
    print("=" * 60)
    
    result = generator.generate(request)
    
    # 输出结果
    print(f"# {result.title}\n")
    print(result.content)
    
    # 生成标签
    if not args.no_tags:
        print("\n" + "=" * 60)
        print("🏷️  推荐标签：\n")
        
        recs = tag_recommender.recommend(
            args.topic,
            args.platform,
            count=10
        )
        
        formatted_tags = tag_recommender.format_tags(recs, args.platform)
        print(formatted_tags)
        
        print(f"\n💡 共{len(recs)}个标签")
        print(f"   - 热门：{sum(1 for r in recs if r.category == 'hot')}")
        print(f"   - 精准：{sum(1 for r in recs if r.category == 'precise')}")
        print(f"   - 长尾：{sum(1 for r in recs if r.category == 'longtail')}")
    
    # 统计信息
    print("\n" + "=" * 60)
    print(f"📊 统计信息:")
    print(f"   字数：{result.word_count}")
    print(f"   平台：{result.platform.value}")
    
    # 保存到文件
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        output_content = f"""# {result.title}

{result.content}

---
**平台**: {result.platform.value}
**字数**: {result.word_count}
**生成时间**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 标签
{tag_recommender.format_tags(recs, args.platform) if not args.no_tags else '无'}
"""
        
        output_path.write_text(output_content, encoding='utf-8')
        print(f"\n✅ 已保存到：{args.output}")


if __name__ == "__main__":
    main()
