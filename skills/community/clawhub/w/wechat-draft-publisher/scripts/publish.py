#!/usr/bin/env python3
"""
微信公众号一键写作发布 - 主流程脚本

用法：
    python3 publish.py \
        --article /tmp/article.md \
        --cover-prompt "A futuristic tech banner" \
        --author "作者名"
"""

import argparse
import json
import os
import sys
import tempfile

# 脚本所在目录 和 skill 根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

sys.path.insert(0, SCRIPT_DIR)

from wechat_api import WeChatAPI
from image_api import AIImageGenerator
from formatter import (
    markdown_to_wechat_html,
    extract_title,
    extract_digest,
    extract_image_prompts,
)

# 默认封面图路径
DEFAULT_COVER = os.path.join(SKILL_DIR, "assets", "default_cover.jpg")


def log(msg: str):
    """带前缀的日志输出"""
    print(f"[发布助手] {msg}")


def load_config() -> dict:
    """加载配置：优先读 config.json，不存在的字段回退到环境变量"""
    config = {}
    config_path = os.path.join(SKILL_DIR, "config.json")

    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        log(f"已加载配置文件: {config_path}")
    else:
        log("未找到 config.json，将使用环境变量")

    wechat = config.get("wechat", {})
    image = config.get("image_api", {})

    return {
        "wechat_appid": wechat.get("appid", "") or os.environ.get("WECHAT_APPID", ""),
        "wechat_appsecret": wechat.get("appsecret", "") or os.environ.get("WECHAT_APPSECRET", ""),
        "image_api_key": image.get("api_key", "") or os.environ.get("IMAGE_API_KEY", ""),
        "image_api_base_url": image.get("api_base_url", "") or os.environ.get("IMAGE_API_BASE_URL", ""),
        "image_model": image.get("model", "") or os.environ.get("IMAGE_MODEL", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="微信公众号一键写作发布")
    parser.add_argument(
        "--article", required=True, help="Markdown 文章文件路径"
    )
    parser.add_argument(
        "--cover-prompt", default="", help="封面图生成提示词（英文）"
    )
    parser.add_argument("--author", default="", help="文章作者")
    parser.add_argument(
        "--cover-image",
        default="",
        help="本地封面图片路径（不使用 AI 生成时提供）",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="跳过图片生成（仅发布文字）",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="创建草稿后立即提交发布（默认仅保存到草稿箱）",
    )
    args = parser.parse_args()

    # ---- 0. 加载配置 ----
    cfg = load_config()

    # ---- 1. 读取文章 ----
    log("读取文章内容...")
    with open(args.article, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    title = extract_title(markdown_text)
    digest = extract_digest(markdown_text)
    image_prompts = extract_image_prompts(markdown_text)

    log(f"标题: {title}")
    log(f"摘要: {digest}")
    log(f"发现 {len(image_prompts)} 个配图位置")

    # ---- 2. 生成图片 ----
    image_urls = {}  # index -> wechat_url
    cover_path = None
    tmp_dir = tempfile.mkdtemp(prefix="wechat_pub_")
    local_images = {}

    if not args.no_images:
        if not cfg["image_api_key"] or not cfg["image_api_base_url"]:
            log("未配置 image_api 的 api_key 或 api_base_url，自动切换为纯文字模式")
            args.no_images = True
        else:
            try:
                img_gen = AIImageGenerator(
                    api_key=cfg["image_api_key"],
                    api_base_url=cfg["image_api_base_url"],
                    model=cfg["image_model"] or "",
                )

                # 生成配图
                for i, prompt in enumerate(image_prompts):
                    log(f"生成配图 {i+1}/{len(image_prompts)}: {prompt[:50]}...")
                    try:
                        path = img_gen.generate_article_image(prompt, tmp_dir, i)
                        local_images[i] = path
                        log(f"  配图 {i+1} 已生成: {path}")
                    except Exception as e:
                        log(f"  配图 {i+1} 生成失败，跳过: {e}")

                # 生成封面
                cover_prompt = args.cover_prompt
                if not cover_prompt:
                    cover_prompt = f"Professional banner illustration about: {title}"
                log(f"生成封面: {cover_prompt[:50]}...")
                try:
                    cover_path = img_gen.generate_cover_image(cover_prompt, tmp_dir)
                    log(f"封面已生成: {cover_path}")
                except Exception as e:
                    log(f"封面生成失败: {e}")
                    cover_path = None

            except ValueError as e:
                log(f"图片生成服务不可用: {e}")
                log("将跳过配图，仅发布文字版本")
                local_images = {}
            except Exception as e:
                log(f"图片生成出错: {e}")
                local_images = {}

    if args.no_images:
        log("已跳过 AI 图片生成")
        local_images = {}
        # 按优先级查找封面：命令行参数 > 默认封面图
        if args.cover_image and os.path.isfile(args.cover_image):
            cover_path = args.cover_image
            log(f"使用本地封面图: {cover_path}")
        elif os.path.isfile(DEFAULT_COVER):
            cover_path = DEFAULT_COVER
            log(f"使用默认封面图: {cover_path}")
        else:
            log("警告: 未找到封面图。请放一张图到 assets/default_cover.jpg")

    # ---- 3. 上传图片到微信并格式化 ----
    try:
        wechat = WeChatAPI(appid=cfg["wechat_appid"], appsecret=cfg["wechat_appsecret"])
        log("微信 API 连接成功")

        # 上传配图
        for i, path in local_images.items():
            log(f"上传配图 {i+1} 到微信...")
            try:
                url = wechat.upload_article_image(path)
                image_urls[i] = url
                log(f"  配图 {i+1} 上传成功")
            except Exception as e:
                log(f"  配图 {i+1} 上传失败: {e}")

        # 上传封面
        thumb_media_id = ""
        if cover_path:
            log("上传封面到微信...")
            try:
                thumb_media_id = wechat.upload_thumb_image(cover_path)
                log(f"封面上传成功: media_id={thumb_media_id}")
            except Exception as e:
                log(f"封面上传失败: {e}")

        if not thumb_media_id:
            if local_images:
                first_img = list(local_images.values())[0]
                log("使用第一张配图作为封面...")
                try:
                    thumb_media_id = wechat.upload_thumb_image(first_img)
                except Exception as e:
                    log(f"备用封面上传失败: {e}")

        if not thumb_media_id:
            log("错误: 未能上传任何封面图片。微信草稿需要封面图。")
            if args.no_images:
                log("提示: 纯文字模式下请通过 --cover-image 提供一张本地封面图。")
            else:
                log("请检查图片生成 API 配置。")
            sys.exit(1)

        # ---- 4. 生成 HTML ----
        log("生成微信公众号 HTML...")
        html_content = markdown_to_wechat_html(
            markdown_text, image_urls, title, digest
        )
        log(f"HTML 生成完成，长度: {len(html_content)} 字符")

        # ---- 5. 创建草稿 ----
        log("创建微信公众号草稿...")
        media_id = wechat.add_draft(
            title=title,
            content=html_content,
            thumb_media_id=thumb_media_id,
            author=args.author,
            digest=digest,
        )
        log(f"草稿创建成功！media_id={media_id}")

        # ---- 6. 可选：提交发布 ----
        if args.publish:
            log("提交发布任务...")
            publish_id = wechat.submit_publish(media_id)
            log(f"发布任务已提交！publish_id={publish_id}")
            log("注意：发布需要平台审核，请在公众号后台查看发布状态。")

    except ValueError as e:
        log(f"微信 API 配置错误: {e}")
        sys.exit(1)
    except Exception as e:
        log(f"微信 API 错误: {e}")
        sys.exit(1)

    # ---- 7. 输出结果摘要 ----
    log("=" * 50)
    log("发布结果摘要")
    log("=" * 50)

    result_summary = {
        "title": title,
        "digest": digest,
        "wechat_draft_media_id": media_id,
        "images_generated": len(image_urls),
        "cover_generated": cover_path is not None,
    }

    log(f"标题: {title}")
    log(f"草稿 media_id: {media_id}")
    log(f"配图数量: {len(image_urls)}/{len(image_prompts)}")
    log(f"封面: {'已生成' if cover_path else '未生成'}")
    log("请前往微信公众号后台查看草稿箱，预览并正式发布。")

    print(f"\n__RESULT_JSON__:{json.dumps(result_summary, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
