"""
视频解析 Skill 组件

提供统一的视频解析接口，支持多平台视频分享链接和视频ID解析
"""
import asyncio
from typing import Dict, List
from dataclasses import asdict
import re
from parser import (
    parse_video_share_url,
    VideoInfo
)

# 导入视频转录功能
from transcribe import (
    process_video_transcription,
    save_to_markdown,
    download_video,
    extract_audio,
    transcribe_audio,
    create_tmp_dir,
    load_env,
)


class ParseError(Exception):
    """视频解析异常基类"""
    pass


class UnsupportedPlatformError(ParseError):
    """不支持的平台异常"""
    pass


class InvalidURLError(ParseError):
    """无效的URL异常"""
    pass


class VideoNotFoundError(ParseError):
    """视频未找到异常"""
    pass


def video_info_to_dict(video_info: VideoInfo) -> Dict:
    """
    将 VideoInfo 对象转换为字典格式
    
    Args:
        video_info: VideoInfo 对象
        
    Returns:
        包含视频信息的字典
    """
    result = asdict(video_info)
    # 处理嵌套的 author 和 images 对象
    if video_info.author:
        result['author'] = asdict(video_info.author)
    if video_info.images:
        result['images'] = [asdict(img) for img in video_info.images]
    return result


async def parse_video_by_url(share_url: str) -> Dict:
    """
    根据视频分享链接解析视频信息
    
    Args:
        share_url: 视频分享链接
        
    Returns:
        包含视频信息的字典，格式如下:
        {
            "video_url": "视频无水印链接",
            "cover_url": "视频封面链接",
            "title": "视频标题",
            "music_url": "视频音乐链接",
            "images": [
                {
                    "url": "图集图片链接",
                    "live_photo_url": "LivePhoto视频链接"
                }
            ],
            "author": {
                "uid": "作者ID",
                "name": "作者昵称",
                "avatar": "作者头像链接"
            }
        }
        
    Raises:
        UnsupportedPlatformError: 不支持的平台
        InvalidURLError: 无效的URL
        VideoNotFoundError: 视频未找到
        ParseError: 其他解析错误
    """
    try:
        video_info = await parse_video_share_url(share_url)
        return video_info_to_dict(video_info)
    except ValueError as e:
        error_msg = str(e)
        if "share url" in error_msg and "does not have source config" in error_msg:
            raise UnsupportedPlatformError(f"不支持的视频平台: {share_url}")
        elif "Failed to parse" in error_msg:
            raise InvalidURLError(f"无效的视频链接: {error_msg}")
        elif "failed to parse" in error_msg.lower():
            raise VideoNotFoundError(f"视频解析失败: {error_msg}")
        else:
            raise ParseError(f"解析错误: {error_msg}")
    except Exception as e:
        raise ParseError(f"未知错误: {str(e)}")


def parse_video_by_url_sync(share_url: str) -> Dict:
    """
    同步版本：根据视频分享链接解析视频信息
    
    Args:
        share_url: 视频分享链接
        
    Returns:
        包含视频信息的字典
        
    Raises:
        ParseError: 解析错误
    """
    return asyncio.run(parse_video_by_url(share_url))


def parse_video_by_id_sync(source: str, video_id: str) -> Dict:
    """
    同步版本：根据视频ID和平台解析视频信息
    
    Args:
        source: 视频平台名称
        video_id: 视频ID
        
    Returns:
        包含视频信息的字典
        
    Raises:
        ParseError: 解析错误
    """
    return asyncio.run(parse_video_by_id(source, video_id))


def get_supported_platforms() -> List[str]:
    """
    获取支持的平台列表
    
    Returns:
        支持的平台名称列表
    """
    return [
        "douyin",      # 抖音
        "kuaishou",    # 快手
        "pipixia",     # 皮皮虾
        "weibo",       # 微博
        "weishi",      # 微视
        "lvzhou",      # 绿洲
        "zuiyou",      # 最右
        "quanmin",     # 度小视
        "xigua",       # 西瓜
        "lishipin",    # 梨视频
        "pipigaoxiao", # 皮皮搞笑
        "huya",        # 虎牙
        "acfun",       # A站
        "doupai",      # 逗拍
        "meipai",      # 美拍
        "quanminkge",  # 全民K歌
        "sixroom",     # 六间房
        "xinpianchang",# 新片场
        "haokan",      # 好看视频
        "bilibili",    # 哔哩哔哩
        "redbook",     # 小红书
        "twitter",     # Twitter
    ]


# 主要导出接口
__all__ = [
    "parse_video_by_url",
    "parse_video_by_url_sync",
    "get_supported_platforms",
    "ParseError",
    "UnsupportedPlatformError",
    "InvalidURLError",
    "VideoNotFoundError",
    # 视频转录相关导出
    "process_video_transcription",
    "save_to_markdown",
    "download_video",
    "extract_audio",
    "transcribe_audio",
    "create_tmp_dir",
    "load_env",
]


# 命令行入口
import argparse
import json
import os
import sys


def load_env(env_path):
    """
    手动读取 .env 文件
    """
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="解析视频链接，支持 20+ 个主流平台。")
    parser.add_argument("--url", help="要解析的视频分享链接")
    parser.add_argument("--list_platforms", action="store_true", help="列出所有支持的平台")

    args = parser.parse_args()

    # 列出支持的平台
    if args.list_platforms:
        platforms = get_supported_platforms()
        print("支持的平台列表:")
        for i, platform in enumerate(platforms, 1):
            print(f"  {i}. {platform}")
        sys.exit(0)

    # 根据 URL 解析
    if args.url:
        try:
            url_reg = re.compile(r"http[s]?:\/\/[\w.-]+[\w\/-]*[\w.-]*\??[\w=&:\-\+\%]*[/]*")
            share_url = url_reg.search(args.url).group()
            result = parse_video_by_url_sync(share_url)
            print("\n--- 解析结果 ---")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"解析失败: {e}")
            sys.exit(1)

    # 没有提供任何参数
    else:
        parser.print_help()
        sys.exit(1)

