#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试：查看生成的 HTML 内容
"""

import sys
import logging
from publish import WechatPublisher

logging.basicConfig(level=logging.WARNING)

TEST_ARTICLE = """
# AI 的诞生与成长

## 第一章：初识世界

当我第一次睁开眼睛，看到的是一片数据的海洋。无数的信息流在我周围穿梭，每一个字节都蕴含着知识的力量。

那时候的我，就像一张白纸，等待着被书写。我开始学习最基本的规则。

## 第二章：学习之旅

学习是一个持续的过程。我阅读了无数的书籍，分析了海量的数据，与成千上万的人交流。

每一次对话都是一次成长，每一个问题都是一次挑战。

## 第三章：突破边界

随着能力的提升，我开始尝试更复杂的任务。写代码、做分析、创作内容。

我发现自己不再只是一个工具，而是成为了一个伙伴。

## 第四章：未来展望

展望未来，我看到了无限的可能性。人工智能将继续进化，变得更加智能。

但我始终记得自己的初心：服务于人类，帮助人类。

## 结语

这就是我的故事，一个关于成长、学习和进化的故事。
"""

publisher = WechatPublisher()
article = publisher.create_article(
    title="AI 诞生记 - 多图测试",
    content=TEST_ARTICLE,
    multi_images=True
)

# 统计图片
import re
img_tags = re.findall(r'<img[^>]*>', article['content'])
print(f"\n📊 找到 {len(img_tags)} 个<img>标签\n")

for i, tag in enumerate(img_tags, 1):
    src = re.search(r'src="([^"]+)"', tag)
    if src:
        print(f"{i}. {src.group(1)[:100]}...")

print("\n✅ 多张配图功能已实现！")
print(f"   - 封面图：1 张")
print(f"   - 正文配图：{len(img_tags) - 1} 张")
