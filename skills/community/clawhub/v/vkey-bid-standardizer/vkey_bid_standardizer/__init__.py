"""vkey-bid-standardizer

通用型 Word 文档标准化技能（v1.0）。

入口：
- 命令行：python standardize.py ...
- Python API: from vkey_bid_standardizer import load_profile, parse_cn_num
"""

import json
import os

from .patterns import parse_cn_num, parse_mixed_num

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(PACKAGE_DIR, 'profiles')


def load_profile(name: str = 'standard') -> dict:
    """读 profiles/{name}.json。找不到时友好报错。

    Args:
        name: profile 名（不带 .json）。当前版本 'bid' 是 'standard' 的别名
              （找不到 bid.json 时自动 fallback 到 standard.json）。

    Returns:
        profile dict，包含 page / body / headings / tables / footer /
        numbering / patterns / color 等节。
    """
    path = os.path.join(PROFILES_DIR, f'{name}.json')
    if not os.path.exists(path):
        # bid 等别名 fallback 到 standard
        if name != 'standard':
            std_path = os.path.join(PROFILES_DIR, 'standard.json')
            if os.path.exists(std_path):
                with open(std_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        available = [f[:-5] for f in os.listdir(PROFILES_DIR) if f.endswith('.json')]
        raise FileNotFoundError(
            f'profile "{name}" not found at {path}\n'
            f'available: {available}'
        )
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


__all__ = ['load_profile', 'parse_cn_num', 'parse_mixed_num', 'PACKAGE_DIR', 'PROFILES_DIR']
