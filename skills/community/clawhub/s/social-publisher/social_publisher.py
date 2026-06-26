#!/usr/bin/env python3
"""
Social Media Multi-Platform Publisher
支持微信公众号、小红书、知乎、抖音的一键发布
"""

import os
import json
import argparse
import sys
import re
from pathlib import Path

# 配置文件路径
CONFIG_PATHS = [
    Path.home() / ".openclaw" / "secrets" / "social-publisher.json",
    Path.home() / ".config" / "social-publisher.json",
]

def load_config():
    """加载平台配置"""
    config = {}
    # 优先从环境变量读取
    platforms = {
        "wechat": {
            "appid": os.getenv("WECHAT_APPID"),
            "appsecret": os.getenv("WECHAT_APPSECRET"),
        },
        "xiaohongshu": {
            "app_id": os.getenv("XIAOHONGSHU_APP_ID"),
            "app_secret": os.getenv("XIAOHONGSHU_APP_SECRET"),
            "access_token": os.getenv("XIAOHONGSHU_ACCESS_TOKEN"),
        },
        "zhihu": {
            "client_id": os.getenv("ZHIHU_CLIENT_ID"),
            "client_secret": os.getenv("ZHIHU_CLIENT_SECRET"),
            "access_token": os.getenv("ZHIHU_ACCESS_TOKEN"),
        },
        "douyin": {
            "app_key": os.getenv("DOUYIN_APP_KEY"),
            "app_secret": os.getenv("DOUYIN_APP_SECRET"),
            "access_token": os.getenv("DOUYIN_ACCESS_TOKEN"),
        }
    }

    # 如果环境变量不全，尝试从配置文件读取
    for config_path in CONFIG_PATHS:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    for platform in platforms:
                        if platform in file_config:
                            platforms[platform].update(file_config[platform])
            except Exception as e:
                print(f"Warning: Failed to load config from {config_path}: {e}")

    # 过滤出配置完整的平台
    ready_platforms = {}
    for name, creds in platforms.items():
        if all(v is not None and v != "" for v in creds.values()):
            ready_platforms[name] = creds
        else:
            print(f"⚠️  {name} 配置不完整，跳过")

    return ready_platforms

def format_wechat(title, content, images):
    """微信公众号格式转换 - 纯文本格式，适合复制粘贴"""
    formatted = []
    
    # 标题部分
    formatted.append(f"【标题】")
    formatted.append(title)
    formatted.append("")
    
    # 正文 - 去除 markdown，保留段落
    formatted.append("【正文】")
    formatted.append("")
    
    lines = content.split('\n')
    in_code_block = False
    current_para = []
    
    for line in lines:
        line = line.strip()
        
        # 处理代码块
        if line.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                current_para.append("【代码块】")
            else:
                current_para.append("【代码块结束】")
            continue
        
        if in_code_block:
            current_para.append("    " + line)
            continue
        
        # 标题处理 - 直接去掉 #，作为段落或小标题
        if line.startswith('# '):
            if current_para:
                formatted.append(' '.join(current_para))
                current_para = []
            formatted.append(line[2:])
            formatted.append("")
        elif line.startswith('## '):
            if current_para:
                formatted.append(' '.join(current_para))
                current_para = []
            formatted.append("  " + line[3:])
            formatted.append("")
        elif line.startswith('### '):
            if current_para:
                formatted.append(' '.join(current_para))
                current_para = []
            formatted.append("    " + line[4:])
            formatted.append("")
        # 空行 - 结束当前段落
        elif not line:
            if current_para:
                formatted.append(' '.join(current_para))
                current_para = []
            formatted.append("")
        # 列表项
        elif line.startswith('- ') or line.startswith('* '):
            current_para.append("• " + line[2:])
        # 加粗
        elif '**' in line:
            line = re.sub(r'\*\*(.*?)\*\*', r'【\1】', line)
            current_para.append(line)
        # 普通段落
        else:
            current_para.append(line)
    
    # 最后一段
    if current_para:
        formatted.append(' '.join(current_para))
    
    # 图片处理
    if images:
        formatted.append("")
        formatted.append("【配图】")
        for i, img in enumerate(images, 1):
            formatted.append(f"{i}. {img}")
    
    return '\n'.join(formatted).strip()

def format_xiaohongshu(title, content, images):
    """小红书格式转换"""
    # 小红书标题限制较短，带表情符号更受欢迎
    xhs_title = f"✨ {title[:20]} ✨" if len(title) <= 20 else f"✨ {title[:17]}... ✨"
    
    formatted = f"【标题】\n{xhs_title}\n\n【正文】\n"
    
    # 小红书风格：分段清晰，使用表情符号
    lines = content.split('\n')
    paras = []
    current_para = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_para:
                paras.append(' '.join(current_para))
                current_para = []
        else:
            # 去除 Markdown 标记
            line = re.sub(r'[#*_`]', '', line)
            current_para.append(line)
    
    if current_para:
        paras.append(' '.join(current_para))
    
    # 分段输出，每段不超过 150 字
    for i, para in enumerate(paras, 1):
        if len(para) > 150:
            # 长段落拆分
            words = para.split()
            sub_para = []
            for word in words:
                if sum(len(w) for w in sub_para) + len(word) > 140:
                    formatted += ' '.join(sub_para) + "\n\n"
                    sub_para = [word]
                else:
                    sub_para.append(word)
            if sub_para:
                formatted += ' '.join(sub_para) + "\n\n"
        else:
            formatted += f"{i}. {para}\n\n"
    
    # 添加话题标签
    formatted += "\n【话题】\n#生活记录 #分享 #好物推荐\n"
    
    # 图片说明
    if images:
        formatted += "\n【配图说明】\n"
        for i, img in enumerate(images, 1):
            formatted += f"图{i}: {os.path.basename(img)}\n"
    
    return formatted.strip()

def format_zhihu(title, content, images):
    """知乎格式转换（保留 Markdown）"""
    formatted = f"# {title}\n\n"
    
    # 知乎支持大部分 Markdown 语法
    # 只需要做小调整
    lines = content.split('\n')
    in_code_block = False
    
    for line in lines:
        # 代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            formatted += line + "\n"
            continue
        
        if in_code_block:
            formatted += line + "\n"
            continue
        
        # 标题调整
        if line.startswith('# '):
            formatted += f"## {line[2:]}\n"
        elif line.startswith('## '):
            formatted += f"### {line[3:]}\n"
        elif line.startswith('### '):
            formatted += f"#### {line[4:]}\n"
        else:
            formatted += line + "\n"
    
    # 图片处理
    if images:
        formatted += "\n---\n\n**配图说明**\n"
        for i, img in enumerate(images, 1):
            formatted += f"![图{i}]({img})\n"
    
    return formatted.strip()

def format_douyin(title, content, images):
    """抖音格式转换"""
    # 抖音文案要求简短，话题标签前置
    # 提取内容中的核心信息
    plain_content = re.sub(r'[#*_`]', '', content)
    plain_content = plain_content.strip()
    
    # 截取前 100 字左右
    if len(plain_content) > 100:
        plain_content = plain_content[:97] + "..."
    
    # 提取关键词作为话题
    topics = re.findall(r'#[^#]+#', content)
    if not topics:
        topics = ["#短视频", "#推荐", "#热门"]
    
    formatted = f"【文案】\n{plain_content}\n\n【标题】\n{title[:30]}\n\n【话题】\n{' '.join(topics[:3])}\n"
    
    if images:
        formatted += f"\n【配图】{len(images)}张\n"
    
    return formatted.strip()

def simulate_publish(platform, title, content, images):
    """模拟发布（实际发布需要真实API）- 带格式化展示"""
    print(f"\n📢 模拟发布到 {platform.upper()}:")
    print(f"   标题: {title}")
    
    # 调用对应的格式化函数
    formatters = {
        'wechat': format_wechat,
        'xiaohongshu': format_xiaohongshu,
        'zhihu': format_zhihu,
        'douyin': format_douyin,
    }
    
    formatter = formatters.get(platform)
    if formatter:
        formatted = formatter(title, content, images)
        print("\n" + "="*60)
        print("[平台格式化内容]")
        print("="*60)
        print(formatted)
        print("="*60)
    else:
        # 降级处理
        print(f"   内容长度: {len(content)} 字符")
        print(f"   配图: {len(images)} 张")
    
    print(f"   ✅ 发布成功（模拟）")

def publish_to_xiaohongshu(title, content, images):
    """小红书发布（需要真实API）"""
    # TODO: 实现小红书开放平台 API
    # 接口: https://api.xiaohongshu.com/api/sns/v1/note/publish
    simulate_publish("xiaohongshu", title, content, images)

def publish_to_zhihu(title, content, images):
    """知乎发布（需要真实API）"""
    # TODO: 实现知乎开放平台 API
    # 接口: https://www.zhihu.com/api/v4/articles
    simulate_publish("zhihu", title, content, images)

def publish_to_douyin(title, content, images):
    """抖音发布（需要真实API）"""
    # TODO: 实现抖音开放平台 API
    # 接口: https://open.douyin.com/api/.../publish
    simulate_publish("douyin", title, content, images)

def main():
    parser = argparse.ArgumentParser(description="多平台内容发布工具")
    parser.add_argument("--title", "-t", required=True, help="文章标题")
    parser.add_argument("--content", "-c", required=True, help="文章正文（支持Markdown）")
    parser.add_argument("--images", "-i", default="", help="图片路径，逗号分隔")
    parser.add_argument("--platforms", "-p", default="wechat,xiaohongshu,zhihu,douyin",
                        help="发布平台列表，逗号分隔")
    parser.add_argument("--dry-run", action="store_true", help="只检查配置，不实际发布")
    parser.add_argument("--format", action="store_true", help="仅预览各平台格式化效果（不发布）")

    args = parser.parse_args()

    # 处理图片列表
    images = [img.strip() for img in args.images.split(",") if img.strip()]

    # 检查是否仅预览格式化效果（不需要配置）
    if args.format:
        platforms_to_show = [p.strip() for p in args.platforms.split(",")]
        
        print(f"\n📋 预览各平台格式化效果（标题: {args.title}）")
        print("=" * 60)
        
        for platform in platforms_to_show:
            formatter_map = {
                'wechat': format_wechat,
                'xiaohongshu': format_xiaohongshu,
                'zhihu': format_zhihu,
                'douyin': format_douyin,
            }
            formatter = formatter_map.get(platform)
            if formatter:
                try:
                    formatted = formatter(args.title, args.content, images)
                    print(f"\n【{platform.upper()}】")
                    print("-" * 40)
                    print(formatted)
                    print("-" * 40)
                except Exception as e:
                    print(f"\n【{platform.upper()}】格式化失败: {e}")
            else:
                print(f"\n【{platform.upper()}】不支持的平台")
        
        print("\n✅ 格式化预览完成！")
        sys.exit(0)

    # 加载配置（用于真实发布或模拟发布）
    config = load_config()
    if not config:
        print("❌ 未找到任何完整的平台配置！")
        print("请设置环境变量或创建配置文件。")
        print("参考 SKILL.md 中的 Configuration 部分。")
        sys.exit(1)

    # 解析平台列表
    target_platforms = [p.strip() for p in args.platforms.split(",") if p.strip() in config]

    if not target_platforms:
        print("❌ 没有可用的目标平台（请检查平台名称和配置）")
        sys.exit(1)

    print(f"✅ 加载到 {len(target_platforms)} 个平台配置:")
    for p in target_platforms:
        print(f"   - {p}")

    if args.dry_run:
        print("\n🔍 仅检查配置模式，不发布。")
        sys.exit(0)

    # 处理图片列表
    images = [img.strip() for img in args.images.split(",") if img.strip()]

    # 加载配置并开始发布
    config = load_config()

    for platform in target_platforms:
        try:
            if platform == "wechat":
                publish_to_wechat(args.title, args.content, images)
            elif platform == "xiaohongshu":
                publish_to_xiaohongshu(args.title, args.content, images)
            elif platform == "zhihu":
                publish_to_zhihu(args.title, args.content, images)
            elif platform == "douyin":
                publish_to_douyin(args.title, args.content, images)
        except Exception as e:
            print(f"❌ {platform} 发布失败: {e}")

    print("\n✅ 全部完成！")
    print("（当前为模拟模式，真实API需在代码中启用）")

if __name__ == "__main__":
    main()
