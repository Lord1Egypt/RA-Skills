#!/usr/bin/env python3
"""
SQL 拆分工具 - 版本与授权管理
一套代码，功能开关控制。License决定可用功能范围。

版本等级:
  community  — 免费社区版（20对象 + 1MB文件限制）
  pro        — 专业版（无限对象 + 批量处理 + 报告 + GUI）
  enterprise — 企业版（全部 + 自定义规则 + API不限 + Docker私有部署）

License Key格式: XXXX-XXXX-XXXX-XXXX（16位，4段）
绑定方式: 机器指纹 (CPU型号+MAC地址 SHA256前16位)
"""

import os
import sys
import json
import hashlib
import platform
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass


# === 版本等级 ===
TIER_COMMUNITY = 'community'
TIER_PRO = 'pro'
TIER_ENTERPRISE = 'enterprise'

# === 硬编码限制 ===
LIMITS = {
    TIER_COMMUNITY: {
        'max_objects': 20,          # 最多20个SQL对象
        'max_file_size_mb': 1,     # 单文件最大1MB
        'batch': False,            # 不支持批量
        'checkpoint': False,       # 不支持断点续传
        'preview': False,          # 不支持结果预览
        'config': False,           # 不支持配置管理
        'report': False,           # 不支持质量报告
        'gui': False,              # 不支持GUI
        'custom_rules': False,     # 不支持自定义规则
        'api_monthly': 0,          # 无API额度
        'docker': False,           # 不支持私有部署
    },
    TIER_PRO: {
        'max_objects': -1,         # 无限
        'max_file_size_mb': -1,    # 无限
        'batch': True,
        'checkpoint': True,
        'preview': True,
        'config': True,
        'report': True,
        'gui': True,
        'custom_rules': False,     # 预设规则
        'api_monthly': 1000,
        'docker': False,
    },
    TIER_ENTERPRISE: {
        'max_objects': -1,
        'max_file_size_mb': -1,
        'batch': True,
        'checkpoint': True,
        'preview': True,
        'config': True,
        'report': True,
        'gui': True,
        'custom_rules': True,      # 自定义DSL
        'api_monthly': -1,         # 无限
        'docker': True,
    },
}

# License文件默认路径
LICENSE_DIR = Path.home() / '.sql-splitter'
LICENSE_FILE = LICENSE_DIR / 'license.json'

# 升级提示
UPGRADE_MESSAGE = """
╔══════════════════════════════════════════════╗
║  🔒 此功能需要专业版或企业版授权            ║
║                                              ║
║  社区版限制: {limit}                          ║
║  当前已使用: {used}                           ║
║                                              ║
║  升级专业版: ¥299/月 (无限对象+批量+报告)   ║
║  升级企业版: ¥2999/月起 (私有部署+定制规则)  ║
║                                              ║
║  访问 https://sqlsplitter.com 了解详情       ║
║  或运行: sql-splitter license activate <KEY> ║
╚══════════════════════════════════════════════╝
"""


@dataclass
class LicenseInfo:
    """License信息"""
    key: str
    tier: str               # community / pro / enterprise
    machine_id: str         # 绑定的机器指纹
    holder: str             # 持有人
    expires: str            # 到期日 (YYYY-MM-DD), 'never'为永不过期
    activated_at: str       # 激活时间

    def is_expired(self) -> bool:
        if self.expires == 'never':
            return False
        from datetime import datetime
        try:
            return datetime.now().strftime('%Y-%m-%d') > self.expires
        except:
            return True

    def is_valid_for_machine(self, machine_id: str) -> bool:
        return self.machine_id == machine_id


def get_machine_id() -> str:
    """获取当前机器指纹 (CPU型号+MAC地址 SHA256前16位)"""
    parts = []
    
    # CPU信息
    try:
        parts.append(platform.processor())
    except:
        parts.append('unknown-cpu')
    
    # MAC地址
    try:
        mac = hex(hash(getattr(os, 'urandom', lambda x: b'')(-1)))[2:]
    except:
        mac = 'unknown-mac'
    
    # 用node作为更稳定的标识
    parts.append(str(os.stat(__file__).st_dev if hasattr(os, 'stat') else platform.node()))
    parts.append(platform.node())
    
    raw = '|'.join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def load_license() -> Optional[LicenseInfo]:
    """加载本地License文件"""
    if not LICENSE_FILE.exists():
        return None
    
    try:
        with open(LICENSE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 简单的完整性校验
        if 'key' not in data or 'tier' not in data:
            return None
        
        return LicenseInfo(
            key=data['key'],
            tier=data['tier'],
            machine_id=data.get('machine_id', ''),
            holder=data.get('holder', ''),
            expires=data.get('expires', 'never'),
            activated_at=data.get('activated_at', ''),
        )
    except (json.JSONDecodeError, KeyError):
        return None


def save_license(info: LicenseInfo):
    """保存License到本地文件"""
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        'key': info.key,
        'tier': info.tier,
        'machine_id': info.machine_id,
        'holder': info.holder,
        'expires': info.expires,
        'activated_at': info.activated_at,
    }
    with open(LICENSE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_current_tier() -> str:
    """获取当前版本等级"""
    info = load_license()
    if info is None:
        return TIER_COMMUNITY
    
    # 校验
    machine_id = get_machine_id()
    if not info.is_valid_for_machine(machine_id):
        return TIER_COMMUNITY
    
    if info.is_expired():
        return TIER_COMMUNITY
    
    return info.tier


def get_limits(tier: str = '') -> dict:
    """获取版本限制"""
    tier = tier or get_current_tier()
    return LIMITS.get(tier, LIMITS[TIER_COMMUNITY])


def check_feature(feature: str, tier: str = '') -> bool:
    """检查功能是否可用"""
    limits = get_limits(tier)
    return limits.get(feature, False)


def check_object_limit(object_count: int, tier: str = '') -> Tuple[bool, str]:
    """
    检查对象数量限制
    
    Returns:
        (allowed, message) — allowed=True允许继续，message为空或提示信息
    """
    limits = get_limits(tier)
    max_objects = limits.get('max_objects', 20)
    
    if max_objects == -1:  # 无限
        return True, ''
    
    if object_count > max_objects:
        msg = UPGRADE_MESSAGE.format(
            limit=f'≤{max_objects}个对象',
            used=f'{object_count}个对象',
        )
        return False, msg
    
    return True, ''


def check_file_size(file_size_bytes: int, tier: str = '') -> Tuple[bool, str]:
    """
    检查文件大小限制
    
    Returns:
        (allowed, message)
    """
    limits = get_limits(tier)
    max_mb = limits.get('max_file_size_mb', 1)
    
    if max_mb == -1:  # 无限
        return True, ''
    
    file_mb = file_size_bytes / (1024 * 1024)
    if file_mb > max_mb:
        msg = UPGRADE_MESSAGE.format(
            limit=f'≤{max_mb}MB文件',
            used=f'{file_mb:.1f}MB文件',
        )
        return False, msg
    
    return True, ''


def require_feature(feature: str, feature_name: str = ''):
    """
    功能守卫 — 对于付费功能，检查License后决定是否允许
    用法: 在函数入口或CLI分支处调用
    
    Args:
        feature: 功能键名 (batch/checkpoint/preview/config/report/gui/custom_rules/docker)
        feature_name: 用户友好的功能名称
    
    Returns:
        True if allowed, False if blocked (已打印提示)
    """
    if check_feature(feature):
        return True
    
    name = feature_name or feature
    print(f'⚠️ {name} 功能需要专业版或企业版授权')
    print(f'   社区版不含此功能。升级请访问 https://sqlsplitter.com')
    print(f'   或运行: sql-splitter license activate <KEY>')
    return False


def activate_license(key: str, holder: str = '') -> Tuple[bool, str]:
    """
    激活License Key
    
    Args:
        key: 16位License Key (XXXX-XXXX-XXXX-XXXX)
        holder: 持有人名称
    
    Returns:
        (success, message)
    """
    # 格式校验
    clean_key = key.strip().upper().replace('-', '')
    if len(clean_key) != 16 or not clean_key.isalnum():
        return False, 'License Key格式错误，应为 XXXX-XXXX-XXXX-XXXX'
    
    # TODO: 这里后续对接服务端RSA验签
    # 当前版本：本地根据Key前缀判断tier
    #  E开头 = Enterprise, P开头 = Pro, 其他 = Community
    tier = TIER_COMMUNITY
    if clean_key.startswith('E'):
        tier = TIER_ENTERPRISE
    elif clean_key.startswith('P'):
        tier = TIER_PRO
    else:
        return False, '无效的License Key（需以P或E开头）'
    
    # 保存
    from datetime import datetime
    info = LicenseInfo(
        key=key,
        tier=tier,
        machine_id=get_machine_id(),
        holder=holder or 'user',
        expires='never',  # TODO: 对接服务端后设置实际过期时间
        activated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )
    save_license(info)
    
    tier_names = {TIER_PRO: '专业版', TIER_ENTERPRISE: '企业版'}
    return True, f'✅ {tier_names.get(tier, tier)}已激活！机器指纹: {info.machine_id}'


def deactivate_license() -> str:
    """注销License"""
    if LICENSE_FILE.exists():
        LICENSE_FILE.unlink()
        return '✅ License已注销，已恢复为社区版'
    return '当前无License，已是社区版'


def show_status():
    """显示当前授权状态"""
    tier = get_current_tier()
    tier_names = {
        TIER_COMMUNITY: '社区版(免费)',
        TIER_PRO: '专业版',
        TIER_ENTERPRISE: '企业版',
    }
    limits = get_limits(tier)
    
    print(f'当前版本: {tier_names.get(tier, tier)}')
    print(f'机器指纹: {get_machine_id()}')
    
    if tier != TIER_COMMUNITY:
        info = load_license()
        if info:
            print(f'持有人: {info.holder}')
            print(f'到期日: {info.expires}')
    
    print()
    print('功能权限:')
    features = ['batch', 'checkpoint', 'preview', 'config', 'report', 'gui', 'custom_rules', 'docker']
    feature_names = {
        'batch': '批量处理',
        'checkpoint': '断点续传',
        'preview': '结果预览',
        'config': '配置管理',
        'report': '质量报告',
        'gui': 'GUI界面',
        'custom_rules': '自定义规则',
        'docker': '私有部署',
    }
    for feat in features:
        allowed = limits.get(feat, False)
        icon = '✅' if allowed else '❌'
        print(f'  {icon} {feature_names.get(feat, feat)}')
    
    if limits.get('max_objects', 0) > 0:
        print(f'  📊 对象数量上限: {limits["max_objects"]}')
    else:
        print(f'  📊 对象数量上限: 无限')
    
    if limits.get('max_file_size_mb', 0) > 0:
        print(f'  📁 文件大小上限: {limits["max_file_size_mb"]}MB')
    else:
        print(f'  📁 文件大小上限: 无限')
    
    if limits.get('api_monthly', 0) > 0:
        print(f'  🔌 API月额度: {limits["api_monthly"]}次')
    elif limits.get('api_monthly', 0) == -1:
        print(f'  🔌 API月额度: 无限')
    else:
        print(f'  🔌 API月额度: 无')


# === CLI ===

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='sql-splitter 授权管理')
    sub = parser.add_subparsers(dest='cmd')
    
    status_cmd = sub.add_parser('status', help='查看授权状态')
    
    act_cmd = sub.add_parser('activate', help='激活License')
    act_cmd.add_argument('key', help='License Key (XXXX-XXXX-XXXX-XXXX)')
    act_cmd.add_argument('--holder', default='', help='持有人名称')
    
    sub.add_parser('deactivate', help='注销License')
    sub.add_parser('machine-id', help='显示机器指纹')
    
    args = parser.parse_args()
    
    if args.cmd == 'status':
        show_status()
    elif args.cmd == 'activate':
        ok, msg = activate_license(args.key, args.holder)
        print(msg)
    elif args.cmd == 'deactivate':
        print(deactivate_license())
    elif args.cmd == 'machine-id':
        print(get_machine_id())
    else:
        parser.print_help()
