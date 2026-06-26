import json
import os
from .client import build_client
from .config import load_config, Config


def _cache_file(cfg: Config) -> str:
    """Store cache under userdata to avoid accidental repo-root commits."""
    return os.path.join(cfg.project_root, "userdata", "my_telegram_groups.json")

def get_all_joined_groups(refresh: bool = False) -> list:
    """
    获取当前登录用户所有已加入的群和频道
    :param refresh: 是否强制刷新缓存，默认False优先读本地缓存
    """
    cfg = load_config()
    cache_file = _cache_file(cfg)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    # 优先读缓存
    if not refresh and os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    client = build_client(cfg)
    
    groups = []
    # 自动处理连接和登录
    with client:
        for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                groups.append({
                    "id": dialog.id,
                    "name": dialog.name,
                    "type": "超级群/频道" if dialog.is_channel else "普通群",
                    "username": dialog.entity.username if hasattr(dialog.entity, "username") else None,
                    "is_public": hasattr(dialog.entity, "username") and dialog.entity.username is not None
                })
    
    # 保存到缓存
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)
    
    return groups

def print_group_list(groups: list = None):
    """格式化输出群列表"""
    if groups is None:
        groups = get_all_joined_groups()
    
    print(f"✅ 您共加入了 {len(groups)} 个群/频道：")
    print("-" * 80)
    for idx, group in enumerate(groups, 1):
        username = f"(@{group['username']})" if group['username'] else "(私有群)"
        print(f"{idx:3d}. {group['name']:<40} {username:<20} ID: {group['id']} | 类型: {group['type']}")
    print("-" * 80)
    cfg = load_config()
    cache_file = _cache_file(cfg)
    print(f"💾 群列表已缓存到 {os.path.abspath(cache_file)}")
