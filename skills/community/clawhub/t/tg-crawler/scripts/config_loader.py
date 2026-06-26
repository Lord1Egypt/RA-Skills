"""
配置加载模块 - 从 YAML 文件读取目标频道/群组和关键词配置
============================================================
v2.0 (2026-06-03): 支持按行业分文件的多 targets 加载 + profile 模式
"""
import os
import yaml
from dataclasses import dataclass, field
from typing import Optional, Union

# 行业分文件映射
PROFILE_FILES = {
    "gaming": ["targets_gaming.yaml", "targets_common.yaml"],
    "retail": ["targets_retail.yaml", "targets_common.yaml"],
    "social": ["targets_social.yaml", "targets_common.yaml"],
    "airline": ["targets_airline.yaml", "targets_common.yaml"],
    "auto": ["targets_auto.yaml", "targets_common.yaml"],
    "all": ["targets_gaming.yaml", "targets_retail.yaml", "targets_social.yaml",
            "targets_airline.yaml", "targets_auto.yaml", "targets_common.yaml"],
    # 兼容：直接指定单个文件
    "gaming_only": ["targets_gaming.yaml"],
    "retail_only": ["targets_retail.yaml"],
    "social_only": ["targets_social.yaml"],
    "airline_only": ["targets_airline.yaml"],
    "auto_only": ["targets_auto.yaml"],
    "common_only": ["targets_common.yaml"],
}


@dataclass
class Target:
    """单个监控目标"""
    id: str
    type: str  # channel / group
    identifier: str  # username 或 invite hash
    invite_link: Optional[str] = None
    note: str = ""
    enabled: bool = True


@dataclass
class KeywordRules:
    """关键词匹配规则"""
    logic_mode: str = "OR"  # OR / AND
    match_mode: str = "substring"  # substring / word / regex
    case_sensitive: bool = False


@dataclass
class TargetsConfig:
    """完整目标配置"""
    targets: list[Target] = field(default_factory=list)
    global_keywords: list[str] = field(default_factory=list)
    keyword_rules: KeywordRules = field(default_factory=KeywordRules)


def _resolve_yaml_paths(path_or_profile: str) -> list[str]:
    """
    解析 targets 文件路径。

    支持三种模式：
    1. 完整路径：直接返回（向后兼容）
    2. profile 名：根据 PROFILE_FILES 映射，在 config/ 目录下查找
    3. 逗号分隔的多个文件名：分别解析
    """
    # 如果是逗号分隔的多个路径/profile，递归解析
    if ',' in path_or_profile:
        paths = []
        for part in path_or_profile.split(','):
            paths.extend(_resolve_yaml_paths(part.strip()))
        return paths

    # 如果是完整路径且文件存在，直接返回
    if os.path.exists(path_or_profile):
        return [path_or_profile]

    # 尝试作为 profile 名解析
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    config_dir = os.path.abspath(config_dir)

    if path_or_profile in PROFILE_FILES:
        file_names = PROFILE_FILES[path_or_profile]
        paths = []
        for fn in file_names:
            fp = os.path.join(config_dir, fn)
            if os.path.exists(fp):
                paths.append(fp)
            else:
                print(f"⚠️ 行业文件不存在，跳过: {fn}")
        if not paths:
            raise FileNotFoundError(
                f"profile '{path_or_profile}' 对应的文件均不存在: {file_names}"
            )
        return paths

    # 尝试作为 config/ 下的文件名
    candidate = os.path.join(config_dir, path_or_profile)
    if os.path.exists(candidate):
        return [candidate]

    raise FileNotFoundError(
        f"无法解析 targets 路径: '{path_or_profile}'。"
        f"支持的 profile: {list(PROFILE_FILES.keys())}"
    )


def load_targets(path_or_profile: str) -> TargetsConfig:
    """
    加载目标配置。支持单文件路径或行业 profile 名。

    Args:
        path_or_profile:
            - 文件路径: "../config/targets.yaml"
            - profile 名: "gaming" / "retail" / "all"
            - 逗号分隔: "gaming,retail"
            - 文件名: "targets_gaming.yaml"

    Returns:
        TargetsConfig 实例（多文件时会合并，自动去重）

    Raises:
        FileNotFoundError: 所有文件都不存在
        yaml.YAMLError: YAML 格式错误
    """
    paths = _resolve_yaml_paths(path_or_profile)

    all_targets = []
    all_keywords = set()
    keyword_rules = KeywordRules()

    for yaml_path in paths:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            raw = yaml.safe_load(f)

        if raw is None:
            continue

        # 合并关键词（取并集）
        for kw in raw.get('global_keywords', []):
            all_keywords.add(kw.lower())

        # 合并关键词规则（只保留第一个非默认规则）
        rules_raw = raw.get('keyword_rules', {})
        if (rules_raw.get('logic_mode', 'OR') != 'OR'
                or rules_raw.get('match_mode', 'substring') != 'substring'
                or rules_raw.get('case_sensitive', False)):
            keyword_rules = KeywordRules(
                logic_mode=rules_raw.get('logic_mode', rules_raw.get('mode', 'OR')),
                match_mode=rules_raw.get('match_mode', 'substring'),
                case_sensitive=rules_raw.get('case_sensitive', False),
            )

        # 合并 targets（按 identifier 去重）
        seen_ids = {t.id for t in all_targets}
        for t in raw.get('targets', []):
            if not t.get('enabled', True):
                continue
            target_obj = Target(
                id=t['id'],
                type=t['type'],
                identifier=t['identifier'],
                invite_link=t.get('invite_link'),
                note=t.get('note', ''),
                enabled=t.get('enabled', True),
            )
            if target_obj.id not in seen_ids:
                all_targets.append(target_obj)
                seen_ids.add(target_obj.id)

    return TargetsConfig(
        targets=all_targets,
        global_keywords=sorted(all_keywords),
        keyword_rules=keyword_rules,
    )


def get_target_identifiers(config: TargetsConfig) -> list[str]:
    """
    将配置中的目标转为 Telethon 可用的 identifier 列表

    - 公开频道: username (如 "BoLe9912")
    - 私密群组: invite_link (如 "https://t.me/+Rwqr-niWBEZjZjY1")
    """
    identifiers = []
    for t in config.targets:
        if t.type == 'group' and t.invite_link:
            identifiers.append(t.invite_link)
        else:
            identifiers.append(t.identifier)
    return identifiers


def add_targets(
    yaml_path: str,
    new_channels: list[dict],
    dedup_by: str = "identifier",
) -> int:
    """
    向 targets 文件中动态追加新目标频道（去重）。

    支持两种模式：
    1. yaml_path 指向单个文件 → 写入该文件
    2. yaml_path 是 "auto" 或包含 "profile" → 自动根据频道内容分类写入对应行业文件

    Args:
        yaml_path: targets 路径或 "auto"（自动分类）
        new_channels: 新频道列表，每个元素为 dict:
            {
                "identifier": "wujindongri6",
                "title": "无尽冬日总群",
                "type": "group",
                "note": "自动发现: tg_search",
                "invite_link": "https://t.me/xxx",
            }
        dedup_by: 去重字段，默认 "identifier"

    Returns:
        实际新增的频道数量
    """
    from datetime import datetime

    # 自动分类模式：按频道 note/title 猜测行业
    if yaml_path in ("auto", "profile"):
        return _add_targets_auto_classify(new_channels, dedup_by)

    # 单文件模式（向后兼容）
    return _add_targets_to_file(yaml_path, new_channels, dedup_by)


def _add_targets_to_file(
    yaml_path: str,
    new_channels: list[dict],
    dedup_by: str = "identifier",
) -> int:
    """
    向 YAML 文件追加新频道（带备份 + 校验）。

    策略：safe_load 读取 → 内存去重合并 → safe_dump 全量重写。
    文本追加模式已废弃，因缩进风格不兼容会破坏 YAML 结构。
    """
    import shutil
    from datetime import datetime

    # 1. 读取现有配置
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}

    existing_targets = config.get('targets', [])
    global_keywords = config.get('global_keywords', [])
    keyword_rules = config.get('keyword_rules', {})

    # 2. 去重
    existing_ids = set()
    for t in existing_targets:
        key = t.get(dedup_by, '')
        if key:
            existing_ids.add(key.lower() if isinstance(key, str) else key)

    # 3. 计算下一个 ID
    max_id = 0
    for t in existing_targets:
        tid = t.get('id', '')
        if isinstance(tid, str) and '_' in tid:
            try:
                num = int(tid.split('_')[1])
                max_id = max(max_id, num)
            except (IndexError, ValueError):
                pass

    # 4. 合并新频道
    new_entries = []
    for ch in new_channels:
        identifier = ch.get('identifier', '')
        if not identifier:
            continue
        if identifier.lower() in existing_ids:
            continue
        max_id += 1
        note = ch.get('note', f'自动发现: {datetime.now().strftime("%Y-%m-%d")}')
        entry = {
            'id': f'auto_{max_id:03d}',
            'type': ch.get('type', 'channel'),
            'identifier': identifier,
            'note': note,
            'enabled': True,
        }
        if ch.get('invite_link'):
            entry['invite_link'] = ch['invite_link']
        new_entries.append(entry)
        existing_ids.add(identifier.lower())

    if not new_entries:
        return 0

    all_targets = existing_targets + new_entries

    # 5. 备份原文件
    bak_path = yaml_path + '.bak'
    shutil.copy2(yaml_path, bak_path)

    # 6. 全量重写（yaml.dump 保证语法正确）
    new_config = {}
    if global_keywords:
        new_config['global_keywords'] = global_keywords
    if keyword_rules:
        new_config['keyword_rules'] = keyword_rules
    new_config['targets'] = all_targets

    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(new_config, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)

    # 7. 校验写入结果
    with open(yaml_path, 'r', encoding='utf-8') as f:
        verified = yaml.safe_load(f)
    if not verified or 'targets' not in verified:
        # 回滚
        shutil.copy2(bak_path, yaml_path)
        raise RuntimeError(f"YAML 写入校验失败，已回滚到备份 {bak_path}")

    return len(new_entries)


def _classify_channel(ch: dict) -> str:
    """
    根据频道 title/note 自动判断行业类别。

    返回: "gaming" / "retail" / "common"
    """
    text = (ch.get('title', '') + ' ' + ch.get('note', '')).lower()

    # 社交/交友关键词
    if any(kw in text for kw in [
        '社交', '交友', '约会', '相亲', '聊天', '约炮', '寂寞', '同城',
        '附近', '恋爱', '撩妹', '小姐姐', '妹子', 'yp', '附近人',
        '探探', '陌陌', 'soul', '积目', 'blued', '他趣',
    ]):
        return "social"

    # 航司/OTA关键词
    if any(kw in text for kw in [
        '航空', '机票', '航班', '里程', '值机', '选座',
        '携程', '飞猪', '去哪儿', '酒店', '积分', '升舱',
    ]):
        return "airline"

    # 汽车关键词
    if any(kw in text for kw in [
        '汽车', '二手车', '新车', '4s', '买车', '卖车', '车贷', '车险',
        '违章', '代驾', '保养', '改装', '座驾',
    ]):
        return "auto"

    # 游戏/外挂关键词
    if any(kw in text for kw in [
        '游戏', '外挂', '辅助', '破解', '枪战', '拦截', '科技',
        'mod', 'crack', 'cheat', 'hack', 'bot', '脚本', '加速',
        '自瞄', '透视', '挂机', '修改', 'gg',
    ]):
        return "gaming"

    # 羊毛/优惠关键词
    if any(kw in text for kw in [
        '羊毛', '优惠', '漏洞单', '线报', 'bug价', '0元购',
        '薅羊毛', '返利', '拼多多', '京东', '淘宝', '天猫',
        '优惠券', '捡漏', '白菜价',
    ]):
        return "retail"

    return "common"


def _add_targets_auto_classify(
    new_channels: list[dict],
    dedup_by: str = "identifier",
) -> int:
    """自动分类模式：根据频道内容写入对应行业文件"""
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    config_dir = os.path.abspath(config_dir)

    # 分类
    buckets = {"gaming": [], "retail": [], "social": [], "airline": [], "auto": [], "common": []}
    for ch in new_channels:
        cat = _classify_channel(ch)
        buckets[cat].append(ch)

    total_added = 0
    for cat in ["gaming", "retail", "social", "airline", "auto", "common"]:
        if buckets[cat]:
            fp = os.path.join(config_dir, f"targets_{cat}.yaml")
            added = _add_targets_to_file(fp, buckets[cat], dedup_by)
            if added:
                print(f"  📂 {cat}: +{added} 个频道 → targets_{cat}.yaml")
            total_added += added

    return total_added


def list_profiles() -> dict:
    """列出所有可用的行业 profile"""
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    config_dir = os.path.abspath(config_dir)

    result = {}
    for profile, files in PROFILE_FILES.items():
        count = 0
        for fn in files:
            fp = os.path.join(config_dir, fn)
            if os.path.exists(fp):
                with open(fp, 'r', encoding='utf-8') as f:
                    raw = yaml.safe_load(f) or {}
                count += len(raw.get('targets', []))
        result[profile] = {"files": files, "total_channels": count}
    return result
