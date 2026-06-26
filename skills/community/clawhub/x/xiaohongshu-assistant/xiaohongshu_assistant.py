#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📕 Xiaohongshu Assistant - 小红书助手（优化版）
功能：文案生成、标题优化、话题推荐
支持 6 种风格：casual | professional | story | 小红书 | 知乎 | 微博
"""

import json
import random
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent
POSTS_FILE = DATA_DIR / "posts.json"

# 导入模板库
from templates import (
    TITLE_TEMPLATES, OPENINGS, BODY_TEMPLATES,
    CALLS_TO_ACTION, EMOJIS, HASHTAGS, RATINGS
)


def load_posts():
    """加载笔记"""
    if POSTS_FILE.exists():
        with open(POSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posts": []}


def save_posts(data):
    """保存笔记"""
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_title(topic, style="小红书"):
    """生成标题"""
    templates = TITLE_TEMPLATES.get(style, TITLE_TEMPLATES["小红书"])
    template = random.choice(templates)
    
    # 添加 emoji（小红书风格专属）
    if style == "小红书":
        emoji = random.choice(["🔥", "✨", "💯", "🎯", "💰", "⚠️", "🛍️", "🌟", "💄", "🎁"])
        title = f"{emoji} {template.replace('XXX', topic)}"
    elif style == "微博":
        title = f"#{topic}# {random.choice(['真的绝了！', '太香了！', '必须冲！'])}"
    else:
        title = template.replace('XXX', topic)
    
    return title


def generate_hashtags(category, count=10, style="小红书"):
    """生成话题标签"""
    tags = HASHTAGS.get(category, HASHTAGS["生活"])
    
    # 微博风格加话题前缀
    if style == "微博":
        return " ".join([f"#{tag.strip('#')}" for tag in random.sample(tags, min(count, len(tags)))])
    
    return random.sample(tags, min(count, len(tags)))


def generate_content(topic, category="生活", style="小红书"):
    """生成文案"""
    
    # 获取对应风格的模板
    openings = OPENINGS.get(style, OPENINGS["小红书"])
    opening = random.choice(openings).replace("XXX", topic)
    
    # 根据不同风格生成不同内容
    if style == "professional":
        content = generate_professional_content(topic, category, opening)
    elif style == "story":
        content = generate_story_content(topic, category, opening)
    elif style == "知乎":
        content = generate_zhihu_content(topic, category, opening)
    elif style == "微博":
        content = generate_weibo_content(topic, category, opening)
    else:
        content = generate_casual_content(topic, category, opening, style)
    
    return content


def generate_casual_content(topic, category, opening, style):
    """生成休闲/小红书风格内容"""
    experiences = [
        f"用了一周，真的惊艳到我了！{topic}的效果真的很不错～",
        f"亲测有效！{topic}比我预期的还要好！",
        f"说实话，{topic}完全超出了我的期待！",
        f"{topic}用了一次就离不开了，真的香！",
    ]
    
    highlights = [
        "1. 颜值高，设计贴心\n2. 效果好，性价比高\n3. 使用方便，物流快",
        "1. 功能强大，材质好\n2. 服务棒，售后好\n3. 包装好，客服好",
        "1. 效果惊艳，价格实惠\n2. 设计人性化，操作简单\n3. 品质可靠，值得入手",
    ]
    
    tips = [
        "敏感肌先试用，理性消费哦～",
        "按需购买，货比三家更稳妥！",
        "建议先小样试用，适合再入手！",
        "大促时买更划算，平时可以观望～",
    ]
    
    ctas = CALLS_TO_ACTION.get(style, CALLS_TO_ACTION["小红书"])
    cta = random.choice(ctas)
    
    rating = random.choice(["⭐⭐⭐⭐⭐", "🌟🌟🌟🌟🌟", "9/10 推荐", "100 分！"])
    
    body = f"""{opening}

✨ 使用感受：
{random.choice(experiences)}

💡 亮点：
{random.choice(highlights)}

⚠️ 注意事项：
{random.choice(tips)}

{cta}

推荐指数：{rating}
"""
    
    # 添加话题
    hashtags = generate_hashtags(category, style=style)
    if style == "微博":
        body += f"\n{hashtags}"
    else:
        body += "\n" + " ".join(hashtags)
    
    return body


def generate_professional_content(topic, category, opening):
    """生成专业风格内容"""
    specs = [
        "• 规格：标准版/Pro 版\n• 价格：¥299-¥599\n• 保修：1 年质保",
        "• 材质：优质材料\n• 工艺：精细做工\n• 认证：多项认证",
        "• 性能：行业领先\n• 能耗：低功耗\n• 寿命：3-5 年",
    ]
    
    pros = [
        "✓ 性价比高，同价位无敌\n✓ 功能全面，满足日常需求\n✓ 品控稳定，售后靠谱",
        "✓ 设计合理，使用便捷\n✓ 材料环保，安全放心\n✓ 口碑好，复购率高",
        "✓ 技术成熟，性能稳定\n✓ 兼容性强，适配性好\n✓ 更新及时，支持到位",
    ]
    
    cons = [
        "✗ 颜色选择少\n✗ 包装一般\n✗ 物流稍慢",
        "✗ 价格略高\n✗ 需要学习成本\n✗ 部分功能鸡肋",
        "✗ 重量偏重\n✗ 配件需另购\n✗ 教程不够详细",
    ]
    
    value = [
        "综合考虑，性价比 8/10，值得入手。",
        "同价位中表现优秀，推荐购买。",
        "适合追求品质的用户，预算充足可入。",
    ]
    
    rating = random.randint(7, 10)
    recommendations = [
        "推荐追求性价比的用户入手。",
        "建议等大促时购买，更划算。",
        "适合有明确需求的用户，小白慎入。",
    ]
    
    body = f"""{opening}

📊 核心参数：
{random.choice(specs)}

✅ 优点分析：
{random.choice(pros)}

❌ 缺点说明：
{random.choice(cons)}

📈 性价比评估：
{random.choice(value)}

综合评分：{rating}/10
购买建议：{random.choice(recommendations)}

{random.choice(CALLS_TO_ACTION["professional"])}

{" ".join(generate_hashtags(category, style="professional"))}
"""
    
    return body


def generate_story_content(topic, category, opening):
    """生成故事风格内容"""
    first_impressions = [
        f"第一次见到{topic}，我是拒绝的。总觉得这种产品都是智商税。",
        f"朋友推荐{topic}的时候，我内心是抗拒的。毕竟踩坑太多次了。",
        f"说实话，刚开始我对{topic}没抱太大希望。",
    ]
    
    turning_points = [
        f"直到有一天，我抱着试试看的心态用了{topic}，结果...真香了！",
        f"改变发生在一个普通的下午，我试用了{topic}，从此打开了新世界。",
        f"转机出现在我最低落的时候，{topic}的出现让我看到了希望。",
    ]
    
    current_states = [
        f"现在，{topic}已经成为我生活中不可或缺的一部分。",
        f"不知不觉中，{topic}已经陪我走过了 X 个月。",
        f"回头看，遇见{topic}真的是我做过最对的决定之一。",
    ]
    
    reflections = [
        "有时候，放下偏见才能发现真正的好东西。",
        "适合自己的，才是最好的。",
        "有些东西，只有试过才知道值不值得。",
        "投资自己，永远是最划算的买卖。",
    ]
    
    body = f"""{opening}

🕐 初识：
{random.choice(first_impressions)}

💫 转变：
{random.choice(turning_points)}

🌈 现在：
{random.choice(current_states)}

💭 感悟：
{random.choice(reflections)}

这就是我和{topic}的故事。

{random.choice(CALLS_TO_ACTION["story"])}

{" ".join(generate_hashtags(category, style="story"))}
"""
    
    return body


def generate_zhihu_content(topic, category, opening):
    """生成知乎风格内容"""
    definitions = [
        f"简单来说，{topic}就是解决 XX 问题的工具/产品。",
        f"{topic}的本质是 XX，核心功能是 XX。",
        f"从技术角度，{topic}采用了 XX 方案，实现了 XX 效果。",
    ]
    
    pros_cons = [
        f"优点：{topic}在 XX 方面表现突出，特别是 XX 功能。\n缺点：价格偏高，学习曲线陡峭。",
        f"优点：性价比高，功能全面。\n缺点：细节有待优化，教程不够完善。",
        f"优点：技术成熟，生态完善。\n缺点：创新不足，同质化严重。",
    ]
    
    target_audiences = [
        f"{topic}适合：有 XX 需求的人、预算充足的人、追求效率的人。",
        f"推荐人群：XX 从业者、XX 爱好者、愿意尝试新事物的人。",
        f"不适合：预算有限、需求简单、不愿学习的人。",
    ]
    
    recommendations = [
        "建议先试用再决定，不要盲目跟风。",
        "大促时入手更划算，平时可以观望。",
        "明确自己的需求，按需购买。",
    ]
    
    body = f"""{opening}

一、{topic}是什么
{random.choice(definitions)}

二、{topic}的优缺点
{random.choice(pros_cons)}

三、{topic}适合什么人
{random.choice(target_audiences)}

四、购买建议
{random.choice(recommendations)}

以上。

{random.choice(CALLS_TO_ACTION["知乎"])}

{" ".join(generate_hashtags(category, style="知乎"))}
"""
    
    return body


def generate_weibo_content(topic, category, opening):
    """生成微博风格内容"""
    highlights = [
        f"🔥 {topic}真的绝了！用了一次就爱上！",
        f"💯 {topic}必须拥有姓名！谁用谁知道！",
        f"✨ {topic}太香了！强烈安利给你们！",
    ]
    
    ctas = [
        "转评赞走一波！👇",
        "评论区聊聊你的看法！💬",
        "关注我，不迷路！🔔",
        "转发给需要的人！📤",
    ]
    
    hashtags = generate_hashtags(category, count=5, style="微博")
    
    body = f"""{opening}

{random.choice(highlights)}

{random.choice(ctas)}

{hashtags}
"""
    
    return body


def create_post(title, content, category="生活", style="小红书"):
    """创建笔记"""
    data = load_posts()
    
    post = {
        "title": title,
        "content": content,
        "category": category,
        "style": style,
        "created": datetime.now().isoformat(),
        "likes": 0,
        "comments": 0,
        "status": "draft"
    }
    
    data["posts"].append(post)
    save_posts(data)
    
    return post


def format_post(post):
    """格式化笔记"""
    response = f"📕 **{post['title']}**\n\n"
    response += f"📂 分类：{post['category']}\n"
    response += f"🎨 风格：{post.get('style', '小红书')}\n"
    response += f"📅 创建：{post['created'][:10]}\n"
    response += f"❤️ 点赞：{post['likes']}\n"
    response += f"💬 评论：{post['comments']}\n"
    response += f"📊 状态：{post['status']}\n\n"
    response += "---\n\n"
    response += post['content'][:300] + "...\n"
    
    return response


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # 解析风格和主题
    styles = ["casual", "professional", "story", "小红书", "知乎", "微博"]
    detected_style = "小红书"  # 默认
    
    for style in styles:
        if style in query_lower:
            detected_style = style
            break
    
    # 提取主题（简单实现）
    topic = "好物"
    if "写" in query or "生成" in query:
        # 尝试提取引号内的内容作为主题
        if '"' in query:
            parts = query.split('"')
            if len(parts) > 1:
                topic = parts[1]
        elif "'" in query:
            parts = query.split("'")
            if len(parts) > 1:
                topic = parts[1]
    
    # ========== 安全提示：发布功能已禁用 ==========
    # 如果用户提到发布，给出安全提示
    if "发布" in query_lower or "上传" in query_lower:
        # 生成文案供用户手动复制
        title = generate_title(topic, style=detected_style)
        content = generate_content(topic, style=detected_style)
        
        return f"""📕 **文案已生成**（安全模式）

🎯 **标题**：
{title}

📝 **正文**：
{content}

---

⚠️ **安全提示**：
为避免封号风险，请**手动复制**以上内容到小红书发布。

**发布步骤**：
1. 打开小红书创作者中心
2. 点击"发布笔记"
3. 复制上方标题和正文
4. 手动上传配图
5. 添加话题标签
6. 人工确认后发布

💡 **安全建议**：
- 每天最多发布 3 篇
- 发布间隔至少 2 小时
- 人工审核修改内容
- 使用真实图片
- 完善账号资料
"""
    
    # 生成标题
    if "标题" in query_lower or "起名" in query_lower:
        title = generate_title(topic, style=detected_style)
        return f"""📕 **标题建议**（{detected_style}风格）

{title}

💡 告诉我你的主题和想要的风格，我帮你生成更精准的标题！
支持风格：casual | professional | story | 小红书 | 知乎 | 微博"""
    
    # 生成文案
    if "文案" in query_lower or "写笔记" in query_lower or "生成" in query_lower:
        category = "生活"
        for cat in HASHTAGS.keys():
            if cat in query:
                category = cat
                break
        
        content = generate_content(topic, category=category, style=detected_style)
        return f"""📕 **文案生成**（{detected_style}风格）

{content}

💡 告诉我：
1. 你想写什么主题？
2. 想要什么风格？（casual/professional/story/小红书/知乎/微博）
3. 属于哪个分类？（美妆/美食/旅行/穿搭/学习/生活/购物/职场/科技/健身/宠物/家居/读书/电影/音乐）"""
    
    # 生成话题
    if "话题" in query_lower or "标签" in query_lower:
        category = "生活"
        for cat in HASHTAGS.keys():
            if cat in query:
                category = cat
                break
        
        tags = generate_hashtags(category, style=detected_style)
        response = f"🏷️ **话题推荐**（{category}分类）：\n\n"
        if detected_style == "微博":
            response += tags
        else:
            for tag in tags:
                response += f"{tag} "
        return response
    
    # 创建笔记
    if "创建" in query_lower or "保存" in query_lower:
        title = generate_title(topic, style=detected_style)
        content = generate_content(topic, style=detected_style)
        post = create_post(title, content, style=detected_style)
        return f"✅ 笔记已创建！\n\n{format_post(post)}"
    
    # 查看笔记列表
    if "笔记" in query_lower and "列表" in query_lower:
        data = load_posts()
        if not data["posts"]:
            return "📕 暂无笔记"
        
        response = "📕 **笔记列表**：\n\n"
        for p in data["posts"][-5:]:
            style_tag = f" [{p.get('style', '小红书')}]" if p.get('style') else ""
            response += f"📝 {p['title']}{style_tag} ({p['created'][:10]})\n"
        
        return response
    
    # 默认回复
    return """📕 小红书助手（优化版）

**功能**：
1. 标题生成 - "帮我想个标题"
2. 文案生成 - "写一篇好物分享"
3. 话题推荐 - "推荐话题标签"
4. 笔记管理 - "查看笔记列表"

**支持 6 种风格**：
- casual - 休闲随意，像朋友聊天
- professional - 理性分析，数据说话
- story - 情感共鸣，讲述经历
- 小红书 - 爆款公式，emoji 丰富
- 知乎 - 深度分析，专业解答
- 微博 - 短小精悍，话题性强

**使用示例**：
- "用小红书风格写一篇美妆文案"
- "用 professional 风格生成标题"
- "用 story 风格写一个学习分享"
- "用知乎风格推荐电影"
- "用微博风格发个穿搭"

告诉我你想写什么？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 测试各种风格
    print("=" * 60)
    print("📕 小红书助手 - 6 种风格测试")
    print("=" * 60)
    
    for style in ["casual", "professional", "story", "小红书", "知乎", "微博"]:
        print(f"\n{'='*20} {style} {'='*20}")
        title = generate_title("咖啡机", style=style)
        print(f"标题：{title}\n")
        content = generate_content("咖啡机", category="生活", style=style)
        print(content[:500] + "...")
