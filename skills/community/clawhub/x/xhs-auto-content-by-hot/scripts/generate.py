
#!/usr/bin/env python3
import requests
import json
import random
import os
import argparse
import sys

# 配置
API_KEY = ""
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
MODEL = "doubao-seedream-4-5-251128"
DEFAULT_WORKSPACE = "/root/.openclaw/workspace"

def print_header():
    print("=" * 50)
    print("  小红书内容生成完整流程 (4步)")
    print("=" * 50)

def step1_get_hot_topic(custom_topic=None):
    print("\n【第一步】获取话题...")
    
    if custom_topic:
        print(f"使用自定义话题: {custom_topic}")
        selected_topic = custom_topic
    else:
        print("获取百度热搜...")
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            hot_list = result["data"]["cards"][0]["content"][0]["content"]
            
            print("成功获取百度热搜！")
            print("\nTOP10话题:")
            for idx, item in enumerate(hot_list[:10], 1):
                print(f"  {idx}. {item['word']}")
            
            random_index = random.randint(0, min(9, len(hot_list)-1))
            selected_topic = hot_list[random_index]["word"]
        except Exception as e:
            print(f"获取百度热搜失败: {e}")
            print("使用默认话题...")
            selected_topic = "今日热门话题"
    
    print(f"\n选中话题: {selected_topic}")
    return selected_topic

def step2_generate_content(topic):
    print("\n【第二步】生成小红书文案...")
    
    # 根据话题类型智能生成标题和正文
    topic_lower = topic.lower()
    
    # 标题生成规则
    if any(keyword in topic_lower for keyword in ["官宣", "结婚", "恋情", "爱情", "甜"]):
        title = "太甜了！磕到了"
    elif any(keyword in topic_lower for keyword in ["爆炸", "突发", "紧急", "重磅"]):
        title = "突发！大事件"
    elif any(keyword in topic_lower for keyword in ["穿搭", "时尚", "衣服", "搭配"]):
        title = "穿搭太绝了"
    elif any(keyword in topic_lower for keyword in ["美食", "好吃", "吃", "餐厅"]):
        title = "好吃到哭！"
    elif any(keyword in topic_lower for keyword in ["旅行", "旅游", "玩", "景点"]):
        title = "这个地方太绝"
    elif any(keyword in topic_lower for keyword in ["职场", "工作", "上班", "工资"]):
        title = "职场人必看"
    elif any(keyword in topic_lower for keyword in ["教育", "孩子", "上学", "教师"]):
        title = "家长必看"
    elif any(keyword in topic_lower for keyword in ["法律", "法院", "判", "案件"]):
        title = "法律科普"
    elif any(keyword in topic_lower for keyword in ["政策", "两会", "规划", "政府"]):
        title = "政策解读"
    else:
        title = topic[:12]
        if len(title) > 15:
            title = title[:15]
    
    # 正文模板库 - 根据话题类型选择不同模板
    templates = {
        "sweet": [
            "家人们！今天这个糖我先磕为敬！🍬\n\n看到「{topic}」，我全程姨母笑！\n这是什么神仙爱情啊，太好磕了吧！\n\n你们也在追吗？快来聊聊你最喜欢的点！\n记得点赞收藏，关注我一起磕糖～",
            "救命！这也太甜了吧！💕\n\n「{topic}」真的甜到心坎里！\n嘴角不自觉上扬，这就是爱情的模样～\n\n快来分享你的看法！评论区等你！\n点赞收藏不迷路，每天给你甜份超标！"
        ],
        "news": [
            "家人们！大事件突发！📰\n\n「{topic}」这也太突然了！\n看到消息我整个人都震惊了，赶紧来分享～\n\n你们怎么看这个事？评论区聊聊！\n记得点赞收藏，关注我获取最新资讯！",
            "重磅消息！！！⚡\n\n「{topic}」刷屏了！\n这发展谁能想到啊，太震撼了！\n\n快来发表你的看法！评论区见！\n点赞收藏关注，热点不迷路～"
        ],
        "fashion": [
            "姐妹们！这套穿搭我直接抄作业！👗\n\n「{topic}」这也太会穿了吧！\n每一套都长在我的审美上，显瘦又好看！\n\n你们最喜欢哪套？评论区告诉我！\n点赞收藏关注，穿搭灵感每天有～",
            "救命！这穿搭也太绝了吧！✨\n\n看到「{topic}」，我立刻拿出小本本记！\n这氛围感、这配色，完全是我的菜！\n\n快来分享你的穿搭心得！评论区等你！\n点赞收藏不迷路，时尚达人就是你～"
        ],
        "food": [
            "姐妹们！这个好吃到我想跺脚！🍜\n\n「{topic}」也太绝了吧！\n看到图片我口水直流，这就去打卡！\n\n你们吃过吗？推荐一下必点！\n点赞收藏关注，美食不迷路～",
            "救命！这是什么神仙美食啊！🤤\n\n「{topic}」馋哭我了！\n色香味俱全，看着就好想吃！\n\n你们还有啥好吃的推荐？评论区告诉我！\n点赞收藏，一起做快乐干饭人～"
        ],
        "travel": [
            "家人们！这个地方我一定要去！🌍\n\n「{topic}」也太美了吧！\n风景如画，完全是我的梦想目的地！\n\n你们去过吗？评论区分享一下！\n点赞收藏关注，旅游攻略不迷路～",
            "救命！这是什么人间仙境啊！🏔️\n\n看到「{topic}」，我立刻打开了订票APP！\n这景色、这氛围，太治愈了！\n\n快来分享你的旅行故事！评论区等你！\n点赞收藏，一起看遍世界美景～"
        ],
        "work": [
            "职场人必看！这说的就是我！💼\n\n「{topic}」太有共鸣了！\n每一句都戳中我的心，打工人太难了！\n\n你们有同感吗？评论区聊聊！\n点赞收藏关注，职场路上不孤单～",
            "家人们！这职场真相了！😮‍💨\n\n看到「{topic}」，我疯狂点头！\n这就是我的真实写照啊，太真实了！\n\n快来吐槽你的职场故事！评论区等你！\n点赞收藏，打工人抱团取暖～"
        ],
        "education": [
            "家长们必看！太重要了！📚\n\n「{topic}」这几点说到点子上了！\n为了孩子，这篇一定要好好看看！\n\n你们有什么教育心得？评论区分享！\n点赞收藏关注，育儿路上不迷茫～",
            "救命！这教育方法也太好了吧！🌟\n\n看到「{topic}」，我赶紧记下来！\n科学又有效，家长们都应该看看！\n\n快来聊聊你的教育经验！评论区等你！\n点赞收藏，一起做智慧家长～"
        ],
        "law": [
            "家人们！这个法律知识太重要了！⚖️\n\n「{topic}」每个人都应该知道！\n学会用法律保护自己，真的很关键！\n\n你们还有什么法律问题？评论区聊聊！\n点赞收藏关注，法律知识学起来～",
            "救命！这案件也太让人深思了！🤔\n\n看到「{topic}」，我感慨万千！\n法律面前人人平等，正义可能迟到但不会缺席！\n\n快来发表你的看法！评论区等你！\n点赞收藏，一起关注法治社会～"
        ],
        "policy": [
            "家人们！这个政策太重要了！📋\n\n「{topic}」关系到我们每个人！\n赶紧看看有什么影响，提前了解！\n\n你们有什么看法？评论区聊聊！\n点赞收藏关注，政策解读不迷路～",
            "重磅！这个政策来得太及时了！🎉\n\n看到「{topic}」，我觉得太赞了！\n这对我们普通人来说真的是利好！\n\n快来分享你的想法！评论区等你！\n点赞收藏，一起关注民生～"
        ],
        "general": [
            "姐妹们！今天这个话题真的绝了！🔥\n\n看到「{topic}」上热搜，我立马点进去看了！\n真的太有共鸣了，忍不住来分享一下～\n\n你们怎么看这个事？欢迎在评论区留言讨论！\n记得点赞收藏关注我哦，每天给你分享精彩内容！",
            "家人们！这个我必须来唠唠！💬\n\n「{topic}」这也太有意思了！\n一看到就忍不住想和你们分享我的想法～\n\n快来评论区说说你的看法！大家一起聊！\n点赞收藏关注，每天都有新内容～"
        ]
    }
    
    # 选择合适的模板类型
    template_type = "general"
    if any(keyword in topic_lower for keyword in ["官宣", "结婚", "恋情", "爱情", "甜"]):
        template_type = "sweet"
    elif any(keyword in topic_lower for keyword in ["爆炸", "突发", "紧急", "重磅"]):
        template_type = "news"
    elif any(keyword in topic_lower for keyword in ["穿搭", "时尚", "衣服", "搭配"]):
        template_type = "fashion"
    elif any(keyword in topic_lower for keyword in ["美食", "好吃", "吃", "餐厅"]):
        template_type = "food"
    elif any(keyword in topic_lower for keyword in ["旅行", "旅游", "玩", "景点"]):
        template_type = "travel"
    elif any(keyword in topic_lower for keyword in ["职场", "工作", "上班", "工资"]):
        template_type = "work"
    elif any(keyword in topic_lower for keyword in ["教育", "孩子", "上学", "教师"]):
        template_type = "education"
    elif any(keyword in topic_lower for keyword in ["法律", "法院", "判", "案件"]):
        template_type = "law"
    elif any(keyword in topic_lower for keyword in ["政策", "两会", "规划", "政府"]):
        template_type = "policy"
    
    # 随机选择该类型下的一个模板
    import random
    selected_template = random.choice(templates[template_type])
    
    # 填充话题变量
    body = selected_template.format(topic=topic)
    
    # 添加标签
    body += "\n\n#" + topic + "[话题]# #热点[话题]# #今日分享[话题]#"
    
    print(f"标题: {title}")
    print(f"模板类型: {template_type}")
    print(f"正文已生成 ({len(body)}字)")
    
    content = {
        "title": title,
        "body": body,
        "topic": topic
    }
    
    return content

def step3_generate_images(content, num_images=3, workspace=DEFAULT_WORKSPACE):
    print("\n【第三步】Seedream-4.5生图...")
    topic = content["topic"]
    
    prompts = [
        "关于「" + topic + "」的小红书封面，明亮清新的配色，简约现代设计风格，有网感，吸引眼球，高品质插画，4K分辨率，用来发布小红书的封面配图，要有网感与设计感",
        "温暖治愈的场景，「" + topic + "」相关的美好画面，柔和的光影，温馨色调，写实风格，高品质，4K分辨率",
        "创意艺术风格，关于「" + topic + "」的抽象表达，大胆的色彩，独特视角，艺术感十足，高品质，4K分辨率"
    ]
    
    generated_images = []
    
    for i, prompt in enumerate(prompts[:num_images]):
        print(f"\n生成第 {i+1} 张图片...")
        print(f"提示词: {prompt[:60]}...")
        
        image_path = os.path.join(workspace, f"xhs_final_{i+1}.png")
        
        try:
            payload = {
                "model": MODEL,
                "prompt": prompt,
                "size": "2048x2048",
                "n": 1
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + API_KEY
            }
            
            print("调用火山引擎Seedream API...")
            response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            if result.get("data") and len(result["data"]) > 0:
                image_url = result["data"][0]["url"]
                print("API调用成功！")
                print("下载图片...")
                
                img_response = requests.get(image_url, timeout=30)
                img_response.raise_for_status()
                
                with open(image_path, "wb") as f:
                    f.write(img_response.content)
                
                generated_images.append(image_path)
                print(f"图片已保存: {image_path}")
            else:
                print(f"API返回异常: {result}")
            
        except Exception as e:
            print(f"生成失败: {e}")
    
    print(f"\n第三步完成！生成了 {len(generated_images)} 张图片")
    return generated_images

def step4_output(images, content, workspace=DEFAULT_WORKSPACE):
    print("\n【第四步】输出结果...")
    print("=" * 50)
    print()
    
    for img_path in images:
        print(f"<qqimg>{img_path}</qqimg>")
    
    print("\n【小红书标题】")
    print(content["title"])
    
    print("\n【小红书正文】")
    print(content["body"])
    
    print("\n" + "=" * 50)
    print("完整流程执行完毕！")
    print("=" * 50)

def save_files(content, images, workspace=DEFAULT_WORKSPACE):
    os.makedirs(workspace, exist_ok=True)
    
    with open(os.path.join(workspace, "selected_topic.txt"), "w", encoding="utf-8") as f:
        f.write(content["topic"])
    
    with open(os.path.join(workspace, "xhs_content.json"), "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(workspace, "generated_images.json"), "w", encoding="utf-8") as f:
        json.dump(images, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="小红书内容生成工具")
    parser.add_argument("--topic", type=str, help="自定义话题（不指定则从百度热搜随机选择）")
    parser.add_argument("--images", type=int, default=3, help="生成图片数量（默认3张）")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_WORKSPACE, help="输出目录")
    args = parser.parse_args()
    
    try:
        print_header()
        
        topic = step1_get_hot_topic(args.topic)
        content = step2_generate_content(topic)
        images = step3_generate_images(content, args.images, args.output_dir)
        
        save_files(content, images, args.output_dir)
        step4_output(images, content, args.output_dir)
        
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
