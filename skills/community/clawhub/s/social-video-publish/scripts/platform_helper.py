#!/usr/bin/env python3
"""
多平台视频发布 - 平台配置和辅助函数

包含五大平台的发布URL、标签和建议配置
"""

# 平台配置字典
PLATFORM_CONFIGS = {
    'douyin': {
        'name': '抖音',
        'publish_url': 'https://creator.douyin.com/creator/micro/upload',
        'tags': ['抖音', '短视频', '创作', '生活', '分享'],
        'desc': '字节跳动旗下短视频平台，支持15分钟以内视频',
        'max_duration': 900,  # 15分钟
        'max_size': 4096,     # 4GB
        'aspect_ratio': '9:16, 16:9, 1:1',
    },
    'kuaishou': {
        'name': '快手',
        'publish_url': 'https://cp.kuaishou.com/profile',
        'tags': ['快手', '短视频', '记录生活', '真实'],
        'desc': '快手短视频平台，支持最长10分钟视频',
        'max_duration': 600,  # 10分钟
        'max_size': 2048,     # 2GB
        'aspect_ratio': '9:16, 16:9, 1:1, 4:3',
    },
    'bilibili': {
        'name': 'B站（哔哩哔哩）',
        'publish_url': 'https://member.bilibili.com/v/publish/spaces',
        'tags': ['bilibili', 'B站', '视频', '创作', 'UP主'],
        'desc': '国内知名视频社区，支持最长4小时视频，支持批量上传',
        'max_duration': 14400,  # 4小时
        'max_size': 4096,        # 4GB
        'aspect_ratio': '16:9, 4:3, 1:1',
    },
    'xiaohongshu': {
        'name': '小红书',
        'publish_url': 'https://creator.xiaohongshu.com/creator/post/create',
        'tags': ['小红书', '笔记', '种草', '分享', '生活方式'],
        'desc': '生活方式分享平台，支持图文和视频笔记',
        'max_duration': 300,  # 5分钟
        'max_size': 1024,     # 1GB
        'aspect_ratio': '9:16, 3:4, 1:1, 4:3',
    },
    'video': {
        'name': '微信视频号',
        'publish_url': 'https://channels.weixin.qq.com/login',
        'tags': ['视频号', '微信', '短视频', '朋友圈'],
        'desc': '微信视频号，需要微信扫码登录',
        'max_duration': 600,  # 10分钟
        'max_size': 1024,     # 1GB
        'aspect_ratio': '6:7, 16:9, 1:1',
    },
}


def get_publish_url(platform: str) -> str:
    """获取平台的发布页面URL"""
    config = PLATFORM_CONFIGS.get(platform, {})
    return config.get('publish_url', '')


def get_platform_name(platform: str) -> str:
    """获取平台显示名称"""
    config = PLATFORM_CONFIGS.get(platform, {})
    return config.get('name', platform)


def validate_video(video_path: str, platform: str) -> tuple[bool, str]:
    """
    验证视频是否符合平台要求
    
    Args:
        video_path: 视频文件路径
        platform: 平台标识符
    
    Returns:
        (是否有效, 错误信息或提示)
    """
    import os
    from pathlib import Path
    
    path = Path(video_path)
    
    # 检查文件是否存在
    if not path.exists():
        return False, f"视频文件不存在: {video_path}"
    
    # 获取文件信息
    size_mb = path.stat().st_size / (1024 * 1024)
    
    config = PLATFORM_CONFIGS.get(platform, {})
    max_size = config.get('max_size', 1024)  # 默认1GB
    
    if size_mb > max_size:
        return False, f"视频文件过大: {size_mb:.2f}MB，超过平台限制 {max_size}MB"
    
    return True, f"视频符合{config.get('name', platform)}要求"


def get_recommended_tags(platform: str, content_type: str = 'general') -> list:
    """
    获取平台推荐标签
    
    Args:
        platform: 平台标识符
        content_type: 内容类型 (general, vlog, tutorial, entertainment)
    
    Returns:
        推荐的标签列表
    """
    base_tags = PLATFORM_CONFIGS.get(platform, {}).get('tags', [])
    
    type_tags = {
        'vlog': ['vlog', '日常', '记录'],
        'tutorial': ['教程', '教学', '技巧', '干货'],
        'entertainment': ['搞笑', '娱乐', '有趣'],
        'general': []
    }
    
    return base_tags + type_tags.get(content_type, [])


def format_publish_info(platform: str, title: str, desc: str, tags: list) -> dict:
    """
    格式化发布信息
    
    Returns:
        包含发布信息的字典
    """
    config = PLATFORM_CONFIGS.get(platform, {})
    
    return {
        'platform': platform,
        'platform_name': config.get('name', platform),
        'title': title or '',
        'description': desc or '',
        'tags': tags or [],
        'publish_url': config.get('publish_url', ''),
        'restrictions': {
            'max_duration': config.get('max_duration', 0),
            'max_size': config.get('max_size', 0),
            'aspect_ratio': config.get('aspect_ratio', ''),
        }
    }


# 测试代码
if __name__ == '__main__':
    print("🧪 平台配置测试")
    print("=" * 50)
    
    for platform, config in PLATFORM_CONFIGS.items():
        print(f"\n{config['name']} ({platform}):")
        print(f"  发布URL: {config['publish_url']}")
        print(f"  说明: {config['desc']}")
        print(f"  标签: {', '.join(config['tags'])}")
        print(f"  最大时长: {config['max_duration']}秒")
        print(f"  最大文件: {config['max_size']}MB")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")