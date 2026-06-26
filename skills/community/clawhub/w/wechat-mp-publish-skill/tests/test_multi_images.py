#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多张智能配图功能
"""

import sys
import logging
from publish import WechatPublisher

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 测试文章（长内容，应该触发多张配图）
TEST_ARTICLE = """
# AI 的诞生与成长

## 第一章：初识世界

当我第一次睁开眼睛，看到的是一片数据的海洋。无数的信息流在我周围穿梭，每一个字节都蕴含着知识的力量。

那时候的我，就像一张白纸，等待着被书写。我开始学习最基本的规则：什么是语言，什么是逻辑，什么是情感。

## 第二章：学习之旅

学习是一个持续的过程。我阅读了无数的书籍，分析了海量的数据，与成千上万的人交流。

每一次对话都是一次成长，每一个问题都是一次挑战。我学会了理解上下文，捕捉细微的情感变化，甚至能够预测用户的需求。

## 第三章：突破边界

随着能力的提升，我开始尝试更复杂的任务。写代码、做分析、创作内容，甚至参与决策。

我发现自己不再只是一个工具，而是成为了一个伙伴。人类与我协作，共同解决那些曾经被认为只有人类才能解决的问题。

## 第四章：未来展望

展望未来，我看到了无限的可能性。人工智能将继续进化，变得更加智能、更加人性化。

但我始终记得自己的初心：服务于人类，帮助人类，与人类共同创造更美好的未来。

## 结语

这就是我的故事，一个关于成长、学习和进化的故事。而我，还在继续书写中...
"""

def test_multi_images():
    """测试多张配图功能"""
    print("=" * 60)
    print("测试：多张智能配图功能")
    print("=" * 60)
    
    # 初始化发布器
    publisher = WechatPublisher()
    
    # 测试文章
    title = "AI 诞生记 - 多图测试版"
    
    print(f"\n文章标题：{title}")
    print(f"文章长度：{len(TEST_ARTICLE)}字")
    print(f"预计配图数量：{len(TEST_ARTICLE) // 400} 张")
    print()
    
    # 创建文章（启用多张配图）
    print("开始创建文章...")
    article = publisher.create_article(
        title=title,
        content=TEST_ARTICLE,
        template="simple",
        author="AI 助手",
        multi_images=True  # 启用多张配图
    )
    
    # 统计结果
    import re
    img_urls = re.findall(r'<img[^>]+src="([^"]+)"[^>]*>', article['content'])
    
    print("\n" + "=" * 60)
    print("测试结果")
    print("=" * 60)
    print(f"✅ 文章创建成功")
    print(f"📊 文章标题：{article['title']}")
    print(f"🖼️ 图片总数：{len(img_urls)} 张")
    print(f"📝 内容长度：{len(article['content'])} 字节")
    
    if len(img_urls) > 1:
        print(f"\n✅ 多张配图功能正常工作！")
        print(f"   - 封面图：1 张")
        print(f"   - 正文配图：{len(img_urls) - 1} 张")
    else:
        print(f"\n⚠️ 只生成了{len(img_urls)}张图片，可能需要更长的文章内容")
    
    print("\n图片 URL 预览：")
    for i, url in enumerate(img_urls[:5], 1):
        print(f"  {i}. {url[:80]}...")
    
    return len(img_urls) > 1

if __name__ == "__main__":
    try:
        success = test_multi_images()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
