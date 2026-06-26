#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自媒体文案生成器 - 核心生成引擎

支持平台：小红书、抖音、公众号、知乎
"""

import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Platform(Enum):
    """支持的平台"""
    XIAOHONGSHU = "xiaohongshu"  # 小红书
    DOUYIN = "douyin"  # 抖音
    WECHAT = "wechat"  # 公众号
    ZHIHU = "zhihu"  # 知乎


@dataclass
class GenerateRequest:
    """生成请求"""
    topic: str  # 主题
    platform: Platform  # 平台
    tone: str = "自然"  # 语气：自然/专业/幽默/温暖
    length: str = "medium"  # 长度：short/medium/long
    keywords: Optional[List[str]] = None  # 关键词
    target_audience: Optional[str] = None  # 目标受众


@dataclass
class GenerateResult:
    """生成结果"""
    title: str  # 标题
    content: str  # 正文
    tags: List[str]  # 标签
    platform: Platform  # 平台
    word_count: int  # 字数


# ============= 平台 Prompt 模板 =============

PLATFORM_TEMPLATES = {
    Platform.XIAOHONGSHU: {
        "system": """你是一名小红书爆款文案专家。

## 小红书文案特点
1. **标题吸引眼球** - 用 emoji、数字、疑问句
2. **正文口语化** - 像姐妹聊天，多用"我""你"
3. **情绪价值** - 共鸣、种草、避坑
4. **排版清晰** - 多分段，用 emoji 分隔
5. **标签精准** - 5-10 个相关标签

## 格式要求
- 标题：20 字以内，含 1-2 个 emoji
- 正文：300-800 字，分 3-5 段
- 每段开头用 emoji
- 结尾引导互动（点赞/收藏/评论）
- 标签：#标签 1 #标签 2 ...

## 禁用
- 硬广语气
- 过度夸张
- 长段落""",

        "user": """请为以下主题创作小红书文案：

**主题**: {topic}
**语气**: {tone}
**长度**: {length}
**关键词**: {keywords}
**目标受众**: {target_audience}

直接输出文案，不要解释。"""
    },

    Platform.DOUYIN: {
        "system": """你是一名抖音短视频脚本专家。

## 抖音文案特点
1. **前 3 秒抓人** - 开头必须有钩子
2. **节奏快** - 短句，信息密度高
3. **引导互动** - 点赞/评论/转发
4. **BGM 感** - 文字有节奏感
5. **话题性** - 容易引发讨论

## 格式要求
- 标题：15 字以内，悬念/疑问
- 正文：100-300 字（口播稿）
- 分镜提示（可选）
- 结尾引导关注

## 禁用
- 长句
- 复杂逻辑
- 说教语气""",

        "user": """请为以下主题创作抖音文案：

**主题**: {topic}
**语气**: {tone}
**关键词**: {keywords}

直接输出文案，不要解释。"""
    },

    Platform.WECHAT: {
        "system": """你是一名公众号爆款文章作者。

## 公众号文案特点
1. **标题党但不过分** - 吸引点击但不欺骗
2. **深度内容** - 有信息量、有观点
3. **结构清晰** - 小标题、分点论述
4. **金句频出** - 便于转发引用
5. **价值输出** - 读者有收获

## 格式要求
- 标题：20-30 字，可副标题
- 正文：800-2000 字
- 3-5 个小标题
- 开头引入 + 结尾升华
- 可加粗重点句

## 禁用
- 过于口语化
- 无实质内容
- 过度营销""",

        "user": """请为以下主题创作公众号文章：

**主题**: {topic}
**语气**: {tone}
**长度**: {length}
**关键词**: {keywords}
**目标受众**: {target_audience}

直接输出文章，不要解释。"""
    },

    Platform.ZHIHU: {
        "system": """你是一名知乎高赞回答作者。

## 知乎文案特点
1. **专业但不枯燥** - 有干货也有可读性
2. **逻辑清晰** - 论证严密，有依据
3. **个人经验** - 结合亲身经历
4. **数据支撑** - 有数据/案例
5. **结尾总结** - 便于读者记住

## 格式要求
- 标题：问题式或直接点题
- 正文：500-1500 字
- 可用列表、引用
- 开头亮观点
- 结尾可引导关注

## 禁用
- 无依据的断言
- 过度情绪化
- 纯营销内容""",

        "user": """请为以下主题创作知乎回答：

**主题**: {topic}
**语气**: {tone}
**关键词**: {keywords}
**目标受众**: {target_audience}

直接输出回答，不要解释。"""
    }
}


# ============= 标题优化器 =============

TITLE_TEMPLATES = [
    "{emoji} {num} 个{topic}技巧，第{num2}个绝了！",
    "后悔没早知道！{topic}的{num}个真相",
    "{topic}怎么做？看这篇就够了",
    "亲测有效！{topic}的{num}种方法",
    "别再{mistake}了！{topic}正确打开方式",
    "{topic}避坑指南｜{num}个血泪教训",
    "月薪{num}k 的{topic}秘籍",
    "{topic}小白必看｜从 0 到 1 全攻略",
    "为什么你的{topic}没效果？{num}个原因",
    "{topic}天花板！这个{method}太绝了",
]


def generate_titles(topic: str, count: int = 5) -> List[str]:
    """生成多个标题选项"""
    titles = []
    
    for i in range(count):
        template = random.choice(TITLE_TEMPLATES)
        title = template.format(
            emoji=random.choice(["🔥", "✨", "💡", "📝", "🎯", "💰", "⚡", "🌟"]),
            num=random.choice([3, 5, 7, 9, 10]),
            num2=random.randint(1, 5),
            topic=topic,
            mistake=random.choice(["盲目尝试", "走弯路", "花冤枉钱"]),
            method=random.choice(["思路", "技巧", "工具"])
        )
        titles.append(title)
    
    return titles


# ============= 核心生成器 =============

class CopywriterGenerator:
    """文案生成器"""
    
    def __init__(self, client=None):
        """
        初始化生成器
        
        Args:
            client: LLM 客户端（如 story-cog client）
        """
        self.client = client
        self.templates = PLATFORM_TEMPLATES
    
    def generate(self, request: GenerateRequest) -> GenerateResult:
        """
        生成文案
        
        Args:
            request: 生成请求
            
        Returns:
            生成结果
        """
        # 构建 prompt
        template = self.templates[request.platform]
        
        user_prompt = template["user"].format(
            topic=request.topic,
            tone=request.tone,
            length=request.length,
            keywords=", ".join(request.keywords) if request.keywords else "无",
            target_audience=request.target_audience or "通用"
        )
        
        # 调用 LLM 生成
        if self.client:
            # 实际调用 LLM
            response = self._call_llm(
                system=template["system"],
                user=user_prompt
            )
        else:
            # 无 client 时返回占位
            response = self._mock_generate(request)
        
        # 解析结果
        result = self._parse_response(response, request.platform)
        
        return result
    
    def _call_llm(self, system: str, user: str) -> str:
        """调用 LLM 生成文案（百炼 dashscope API）"""
        try:
            import urllib.request
            import json
            
            # 百炼 API 配置
            api_key = "sk-sp-1f1d92cdff7d4cbd8dcbe1cd08711606"
            url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
            
            # 构建请求
            data = {
                "model": "qwen3.5-plus",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            # 发送请求
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result['choices'][0]['message']['content']
                return content.strip()
                
        except Exception as e:
            # API 调用失败时返回 mock 内容
            print(f"⚠️  LLM API 调用失败：{e}，使用 mock 内容")
            return self._mock_generate_from_template(system, user)
    
    def _mock_generate_from_template(self, system: str, user: str) -> str:
        """从模板生成 mock 内容（备用方案）"""
        # 根据 platform 提取模板
        if "小红书" in system or "xiaohongshu" in system.lower():
            return self._mock_xiaohongshu(user)
        elif "抖音" in system or "douyin" in system.lower():
            return self._mock_douyin(user)
        elif "公众号" in system or "wechat" in system.lower():
            return self._mock_wechat(user)
        elif "知乎" in system or "zhihu" in system.lower():
            return self._mock_zhihu(user)
        else:
            return self._mock_generate(None)
    
    def _mock_xiaohongshu(self, user: str) -> str:
        """小红书 mock 模板"""
        return """🔥 亲测有效！这个技巧太绝了

姐妹们！

今天想和大家聊聊这个话题～

## 为什么重要
很多人都不知道，其实有个秘密...

## 具体做法
1. 第一步：先准备好工具
2. 第二步：按照步骤操作
3. 第三步：注意细节调整

## 我的体验
用了这个方法之后，效率真的提升太多了！
之前要花 3 小时，现在 30 分钟搞定～

## 注意事项
⚠️ 记得不要着急，慢慢来
⚠️ 第一次可能不熟练，多试几次

希望这篇笔记对你们有帮助！
觉得有用记得点赞收藏哦～💕

#干货 #技巧 #分享 #生活记录"""

    def _mock_douyin(self, user: str) -> str:
        """抖音 mock 模板"""
        return """（开头 3 秒钩子）
你知道吗？90% 的人都做错了！

（正文）
今天告诉你正确方法...

第一步...
第二步...
第三步...

（结尾引导）
学会了吗？评论区告诉我！
记得点赞关注哦～

#干货 #技巧"""

    def _mock_wechat(self, user: str) -> str:
        """公众号 mock 模板"""
        return """# 标题：深度解析这个话题

**文 | 作者**

## 引言

在这个快速发展的时代，这个话题越来越重要...

## 一、背景分析

首先，我们需要了解...

## 二、核心方法

### 1. 第一步
详细说明...

### 2. 第二步
具体操作...

### 3. 第三步
注意事项...

## 三、实践建议

基于以上分析，我建议...

## 结语

希望这篇文章能给你带来启发。

**欢迎转发分享，转载请注明出处。**"""

    def _mock_zhihu(self, user: str) -> str:
        """知乎 mock 模板"""
        return """这个问题我来回答。

先说结论：**这个话题确实值得深入探讨**。

## 背景

我在这个领域有 X 年经验，遇到过类似问题...

## 分析

从专业角度来看，主要有以下几点：

1. **第一点**：详细说明...
2. **第二点**：具体分析...
3. **第三点**：补充说明...

## 建议

基于我的经验，建议如下：

- 短期：先做...
- 中期：再做...
- 长期：最后...

## 总结

总的来说，这个话题需要...

**以上，希望能帮到你。**

如果觉得有用，欢迎点赞收藏～"""
    
    def _mock_generate(self, request: GenerateRequest) -> str:
        """模拟生成（用于测试）"""
        platform_names = {
            Platform.XIAOHONGSHU: "小红书",
            Platform.DOUYIN: "抖音",
            Platform.WECHAT: "公众号",
            Platform.ZHIHU: "知乎"
        }
        
        return f"""# {random.choice(["🔥", "✨", "💡"])} {request.topic}

{random.choice(["姐妹们", "朋友们", "大家好"])}！

今天想和大家聊聊{request.topic}这个话题～

## 为什么重要
{random.choice(["很多人都不知道", "其实有个秘密", "我发现了一个方法"])}...

## 具体做法
1. 第一步...
2. 第二步...
3. 第三步...

## 注意事项
⚠️ 记得{random.choice(["不要着急", "多尝试", "坚持一下"])}

希望这篇笔记对你们有帮助！
觉得有用记得点赞收藏哦～💕

#{" #".join([request.topic, "干货", "技巧", "分享"])}"""
    
    def _parse_response(self, response: str, platform: Platform) -> GenerateResult:
        """解析 LLM 响应"""
        # 简单解析，实际应该更复杂
        lines = response.strip().split("\n")
        title = lines[0].replace("#", "").strip() if lines else "未命名"
        content = "\n".join(lines[1:])
        
        # 提取标签
        tags = []
        for line in lines:
            if line.startswith("#"):
                tags.extend(line.split("#")[1:])
        
        return GenerateResult(
            title=title,
            content=content,
            tags=tags[:10],
            platform=platform,
            word_count=len(content)
        )


# ============= 命令行接口 =============

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="自媒体文案生成器")
    parser.add_argument("topic", help="文案主题")
    parser.add_argument("-p", "--platform", 
                       choices=["xiaohongshu", "douyin", "wechat", "zhihu"],
                       default="xiaohongshu",
                       help="目标平台")
    parser.add_argument("-t", "--tone", default="自然",
                       help="语气（自然/专业/幽默/温暖）")
    parser.add_argument("-l", "--length", default="medium",
                       choices=["short", "medium", "long"],
                       help="长度")
    parser.add_argument("-k", "--keywords", nargs="+",
                       help="关键词")
    parser.add_argument("-o", "--output", help="输出文件")
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = CopywriterGenerator()
    
    # 构建请求
    request = GenerateRequest(
        topic=args.topic,
        platform=Platform(args.platform),
        tone=args.tone,
        length=args.length,
        keywords=args.keywords
    )
    
    # 生成文案
    print(f"📝 正在生成{args.platform}文案...")
    result = generator.generate(request)
    
    # 输出结果
    output = f"""# {result.title}

{result.content}

---
**字数**: {result.word_count}
**平台**: {result.platform.value}
**标签**: {" ".join(result.tags)}
"""
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 已保存到 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
