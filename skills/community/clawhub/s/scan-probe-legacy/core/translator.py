# -*- coding: utf-8 -*-
"""F7: 基础汉化

自动提取模组的英语语言文件键值对，翻译为简体中文，
生成zh_cn.json汉化补丁，可调用F5重打包固化进JAR。

V1仅处理基础词条（方块/物品/道具名称），不涉及配置面板和深层代码文本汉化。

使用方式:
    from core.translator import run
    import argparse
    args = argparse.Namespace(jar_path="xxx.jar", target_lang="zh_cn", patch_only=False)
    result = run(args)
"""

import sys
import os
import json
import re
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.jar_utils import (
    extract_jar, create_temp_dir, cleanup_temp_dir,
    read_jar_file
)
from utils.report_gen import ReportGenerator

logger = get_logger("translator")

# V1.0.5: 离线翻译库
try:
    from data.translation_db import get_db as _get_translation_db
    _translation_db = _get_translation_db()
except ImportError:
    _translation_db = None
    logger.warning("离线翻译库未加载（data.translation_db 导入失败）")

# === MC基础词条分类正则 ===
CATEGORY_PATTERNS = {
    "block": re.compile(r"^(block|tile)\.", re.IGNORECASE),
    "item": re.compile(r"^(item|gun|ammo)\.", re.IGNORECASE),
    "tooltip": re.compile(r"\.tooltip\.|\.desc\.|\.info\.|\.text\.|tooltip|tooltip", re.IGNORECASE),
    "advancement": re.compile(r"^(advancement|achievement)\.", re.IGNORECASE),
    "entity": re.compile(r"^(entity|mob)\.", re.IGNORECASE),
    "sound": re.compile(r"^(sound|sounds|Music)\.", re.IGNORECASE),
    "creative": re.compile(r"^(itemGroup|creativeTab|tab)\.", re.IGNORECASE),
    "config": re.compile(r"^(config|gui|screen|button|option)\.", re.IGNORECASE),
}

# === MC常见术语翻译词典（英语 -> 目标语言） ===
# 主词典：英语 -> 简体中文（默认）
MC_TERMS_DICT = {
    # 通用词汇
    "item": "物品",
    "block": "方块",
    "tile": "方块",
    "entity": "实体",
    "mob": "生物",
    "player": "玩家",
    "damage": "伤害",
    "health": "生命",
    "speed": "速度",
    "duration": "持续时间",
    "infinite": "无限",
    "normal": "普通",
    "small": "小型",
    "large": "大型",
    # 矿物
    "coal": "煤炭",
    "iron": "铁",
    "gold": "金",
    "diamond": "钻石",
    "emerald": "绿宝石",
    "redstone": "红石",
    "lapis": "青金石",
    "obsidian": "黑曜石",
    # 工具
    "pickaxe": "镐",
    "sword": "剑",
    "axe": "斧",
    "shovel": "铲",
    "hoe": "锄",
    "hammer": "锤",
    "bow": "弓",
    "arrow": "箭",
    "shield": "盾牌",
    # 食物
    "apple": "苹果",
    "bread": "面包",
    "cooked": "熟",
    "raw": "生",
    # 颜色
    "white": "白色",
    "red": "红色",
    "green": "绿色",
    "blue": "蓝色",
    "black": "黑色",
    "yellow": "黄色",
    "gray": "灰色",
    "grey": "灰色",
    "silver": "银色",
    # 功能
    "toggle": "切换",
    "enabled": "启用",
    "disabled": "禁用",
    "allow": "允许",
    "deny": "拒绝",
    "open": "打开",
    "close": "关闭",
    "on": "开",
    "off": "关",
    "yes": "是",
    "no": "否",
    # 模组通用
    "create": "机械动力",
    "steam": "蒸汽",
    "rails": "铁轨",
    "engine": "引擎",
    "belt": "传送带",
    "gear": "齿轮",
    "shaft": "轴",
    "pulley": "滑轮",
    "chain": "链条",
    "windmill": "风车",
    "water": "水",
    "fire": "火",
    "air": "空气",
    "earth": "泥土",
    "stone": "石头",
    "wood": "木头",
    "plank": "木板",
    "log": "原木",
    "leaves": "树叶",
    # 附魔
    "enchanted": "附魔的",
    "enchantment": "附魔",
    "fortune": "时运",
    "silk": "精准采集",
    "unbreaking": "耐久",
    "efficiency": "效率",
    # 游戏机制
    "survival": "生存",
    "creative": "创造",
    "adventure": "冒险",
    "spectator": "旁观",
    "peaceful": "和平",
    "easy": "简单",
    "hard": "困难",
}

# 阿拉伯语术语词典（英语 -> 通用阿拉伯语）
MC_TERMS_DICT_AR_SA = {
    # General terms
    "item": "عنصر",
    "block": "كتلة",
    "tile": "كتلة",
    "entity": "كيان",
    "mob": "كائن",
    "player": "لاعب",
    "damage": "ضرر",
    "health": "صحة",
    "speed": "سرعة",
    "duration": "مدة",
    "infinite": "غير محدود",
    "normal": "عادي",
    "small": "صغير",
    "large": "كبير",
    # Minerals
    "coal": "فحم",
    "iron": "حديد",
    "gold": "ذهب",
    "diamond": "ماس",
    "emerald": "زمرد",
    "redstone": "ريدستون",
    "lapis": "لازورد",
    "obsidian": "أوبسيديان",
    # Tools
    "pickaxe": "معول",
    "sword": "سيف",
    "axe": "فأس",
    "shovel": "مجرفة",
    "hoe": "مذرع",
    "hammer": "مطرقة",
    "bow": "قوس",
    "arrow": "سهم",
    "shield": "درع",
    # Food
    "apple": "تفاحة",
    "bread": "خبز",
    "cooked": "مطبوخ",
    "raw": "نيء",
    # Colors
    "white": "أبيض",
    "red": "أحمر",
    "green": "أخضر",
    "blue": "أزرق",
    "black": "أسود",
    "yellow": "أصفر",
    "gray": "رمادي",
    "grey": "رمادي",
    "silver": "فضي",
    # Functions
    "toggle": "تبديل",
    "enabled": "مفعل",
    "disabled": "معطل",
    "allow": "سماح",
    "deny": "رفض",
    "open": "فتح",
    "close": "إغلاق",
    "on": "تشغيل",
    "off": "إيقاف",
    "yes": "نعم",
    "no": "لا",
    # Mods common
    "create": "كرييت",
    "steam": "بخار",
    "rails": "قضبان",
    "engine": "محرك",
    "belt": "حزام ناقل",
    "gear": "ترس",
    "shaft": "عمود",
    "pulley": "بكرة",
    "chain": "سلسلة",
    "windmill": "طاحونة هوائية",
    "water": "ماء",
    "fire": "نار",
    "air": "هواء",
    "earth": "تراب",
    "stone": "حجر",
    "wood": "خشب",
    "plank": "لوح خشبي",
    "log": "جذع شجرة",
    "leaves": "أوراق",
    # Enchantments
    "enchanted": "مشحون",
    "enchantment": "سحر",
    "fortune": "الحظ",
    "silk": "اللمس الحريري",
    "unbreaking": "عدم الكسر",
    "efficiency": "كفاءة",
    # Game mechanics
    "survival": "بقاء",
    "creative": "إبداع",
    "adventure": "مغامرة",
    "spectator": "متفرج",
    "peaceful": "هادئ",
    "easy": "سهل",
    "hard": "صعب",
}

# 语言 -> 术语词典映射表
LANG_TERMS_DICT = {
    "zh_cn": MC_TERMS_DICT,
    "zh_tw": MC_TERMS_DICT,  # 繁体暂用简体词典（后续可单独维护）
    "ar_sa": MC_TERMS_DICT_AR_SA,
}


def _categorize_key(key: str) -> str:
    """根据key判断词条分类"""
    for category, pattern in CATEGORY_PATTERNS.items():
        if pattern.search(key):
            return category
    return "other"


def _simple_translate(text: str, target_lang: str = "zh_cn") -> str:
    """简易翻译（基于词典替换）

    V1.0.5 改进：支持多语言词典，按 target_lang 选择对应术语表
    离线模式下使用此函数；未匹配的词条原样返回
    """
    if not text or not isinstance(text, str):
        return text

    result = text

    # 按 target_lang 选择术语词典
    terms_dict = LANG_TERMS_DICT.get(target_lang, {})
    if not terms_dict:
        # 无对应词典，原样返回
        return result

    # 按长度降序排列，优先匹配长词
    sorted_terms = sorted(terms_dict.items(), key=lambda x: len(x[0]), reverse=True)

    for en, translated in sorted_terms:
        # 仅替换独立单词，不替换子串
        pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
        result = pattern.sub(translated, result)

    return result


def _find_language_files(jar_path: Path) -> List[Tuple[str, str]]:
    """在JAR中查找语言文件

    Returns:
        [(en_us_path, local_path), ...]
    """
    lang_files = []
    tmp_dir = create_temp_dir("lang_find")

    try:
        extract_jar(jar_path, tmp_dir)

        for root, dirs, files in os.walk(tmp_dir):
            for filename in files:
                if filename == "en_us.json":
                    local_path = str(Path(root) / filename)
                    # 计算JAR内相对路径（使用正斜杠）
                    rel_in_jar = Path(local_path).relative_to(tmp_dir).as_posix()
                    lang_files.append((rel_in_jar, local_path))
    except (zipfile.BadZipFile, Exception) as e:
        logger.warning(f"解压JAR失败 {jar_path.name}: {e}")
    finally:
        cleanup_temp_dir(tmp_dir)

    return lang_files


def _extract_lang_content(jar_path: Path, lang_path: str) -> Optional[Dict[str, Any]]:
    """从JAR中提取语言文件内容"""
    try:
        content = read_jar_file(jar_path, lang_path)
        if content:
            return json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError, KeyError) as e:
        logger.debug(f"读取语言文件失败: {lang_path}, 原因: {e}")
    return None


def _categorize_entries(lang_data: Dict[str, Any]) -> Dict[str, List[Tuple[str, str]]]:
    """按分类整理语言条目

    Returns:
        {category: [(key, value), ...]}
    """
    categorized = defaultdict(list)

    for key, value in lang_data.items():
        if not isinstance(value, str):
            continue
        category = _categorize_key(key)
        categorized[category].append((key, value))

    # 按分类排序
    for cat in categorized:
        categorized[cat].sort(key=lambda x: x[0])

    return dict(categorized)


def _emit_translation_prompt(
    mod_id: str,
    target_lang: str,
    pending_entries: List[Tuple[str, str]],
    jar_path: str,
    timestamp: str,
) -> str:
    """生成 AI Agent 翻译 prompt 文件

    当离线词典和翻译库都未命中时，生成 prompt 文件让宿主 AI Agent 翻译

    Returns:
        prompt 文件路径
    """
    output_dir = config.OUTPUT_DIR / "translation_prompts"
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = output_dir / f"translation_prompt_{timestamp}.md"

    # 语言名称映射
    lang_names = {
        "zh_cn": "简体中文", "zh_tw": "繁体中文", "ja_jp": "日本語",
        "ko_kr": "한국어", "ru_ru": "Русский", "es_es": "Español",
        "it_it": "Italiano", "el_gr": "Ελληνικά", "th_th": "ไทย",
        "hi_in": "हिन्दी", "ar_sa": "العربية",
    }
    lang_name = lang_names.get(target_lang, target_lang)

    # 构建待翻译条目表格
    entries_text = ""
    for i, (key, value) in enumerate(pending_entries, 1):
        entries_text += f"| {i} | `{key}` | `{value}` |\n"

    prompt_content = f"""# MC 模组翻译任务

## 任务说明
请将以下 Minecraft 模组的英语语言条目翻译为 **{lang_name}**（`{target_lang}`）。

## 模组信息
- 模组 ID: `{mod_id}`
- JAR 文件: `{jar_path}`

## 翻译规则
1. 保持 Minecraft 术语的准确性（如 "Block" → "方块"，"Item" → "物品"）
2. 保留格式化占位符（如 `%s`, `%d`, `%1$s` 等不动）
3. 保留颜色代码（如 `§a`, `§b` 等不动）
4. 翻译完成后，请将结果写入以下 JSON 文件：
   `output/translation_responses/translation_response_{timestamp}.json`

## 响应文件格式
```json
{{
  "mod_id": "{mod_id}",
  "target_lang": "{target_lang}",
  "translations": {{
    "<原文键名>": "<翻译结果>",
    ...
  }}
}}
```

## 待翻译条目（共 {len(pending_entries)} 条）

| # | 键名 | 英文原文 |
|---|------|----------|
{entries_text}

## 注意事项
- 请翻译 value 列的英文原文，不要修改 key
- 翻译结果写入 JSON 文件的 `translations` 字段
- 完成后运行: `python main.py --feature translator --mode apply-response --response-file output/translation_responses/translation_response_{timestamp}.json --jar-path {jar_path} --target-lang {target_lang}`
"""

    prompt_file.write_text(prompt_content, encoding="utf-8")
    logger.info(f"翻译 prompt 已生成: {prompt_file}")
    return str(prompt_file)


def _apply_translation_response(
    response_path: str,
    jar_path: str,
    target_lang: str,
) -> Dict[str, Any]:
    """应用 AI Agent 的翻译响应

    读取响应 JSON，写入翻译库（学习机制），然后调用 F5 重打包进 JAR

    Returns:
        结果字典
    """
    response_file = Path(response_path)
    if not response_file.exists():
        return {"status": "error", "error": f"响应文件不存在: {response_path}"}

    try:
        data = json.loads(response_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"status": "error", "error": f"JSON 解析失败: {e}"}

    mod_id = data.get("mod_id", Path(jar_path).stem)
    translations = data.get("translations", {})

    if not translations:
        return {"status": "error", "error": "响应中无翻译条目"}

    # === 学习机制：写入翻译库 ===
    if _translation_db:
        _translation_db.store_batch(mod_id, target_lang, translations)
        logger.info(f"已学习 {len(translations)} 条翻译到离线库（mod={mod_id}, lang={target_lang}）")

    # === 调用 F5 重打包 ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    patch_resources_dir = config.PATCH_DIR / "resources"
    patch_resources_dir.mkdir(parents=True, exist_ok=True)

    # 从 JAR 推断语言文件路径
    jar_path_obj = Path(jar_path)
    lang_files = _find_language_files(jar_path_obj)
    if not lang_files:
        return {"status": "error", "error": "JAR 中未找到 en_us.json"}

    first_lang_path = lang_files[0][0]
    target_lang_jar_path = first_lang_path.replace("en_us.json", f"{target_lang}.json")

    # 保存翻译到补丁目录
    patch_save_path = patch_resources_dir / target_lang_jar_path
    patch_save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(patch_save_path, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    # 调用 F5
    try:
        from core.repacker import run as repacker_run
        repacker_args = type("Args", (), {
            "jar_path": str(jar_path_obj),
            "resources_dir": str(patch_resources_dir),
            "output": str(Path(config.DOWNLOADS_DIR) / f"{jar_path_obj.stem}_{target_lang}.jar"),
            "validate": True,
        })()
        repacker_result = repacker_run(repacker_args)
        if repacker_result.get("status") == "success":
            repacked_jar = repacker_result["output_files"].get("downloaded", "")
            logger.info(f"翻译 JAR 已生成: {repacked_jar}")
            return {
                "status": "success",
                "mod_id": mod_id,
                "target_lang": target_lang,
                "translated_count": len(translations),
                "learned_to_db": _translation_db is not None,
                "patch_path": str(patch_save_path),
                "repacked_jar": repacked_jar,
            }
        else:
            return {
                "status": "warning",
                "mod_id": mod_id,
                "translated_count": len(translations),
                "learned_to_db": _translation_db is not None,
                "patch_path": str(patch_save_path),
                "repack_error": repacker_result.get("errors"),
            }
    except Exception as e:
        return {
            "status": "warning",
            "mod_id": mod_id,
            "translated_count": len(translations),
            "learned_to_db": _translation_db is not None,
            "patch_path": str(patch_save_path),
            "repack_error": str(e),
        }


def _generate_zh_cn(
    lang_data: Dict[str, Any],
    categories: Dict[str, List[Tuple[str, str]]],
    target_lang: str,
    mod_id: str = "",
    mode: str = "hybrid",
    jar_path: str = "",
    timestamp: str = "",
) -> Tuple[Dict[str, str], Dict[str, List[str]], List[Tuple[str, str]], Optional[str]]:
    """生成翻译文件（V1.0.5 三模式：offline/online/hybrid）

    Args:
        mode: offline=仅词典+翻译库; online=仅AI Agent; hybrid=词典+翻译库优先，未命中发prompt

    Returns:
        (translated_data, quality_notes, pending_entries, prompt_path)
        - pending_entries: 未命中需 AI 翻译的条目
        - prompt_path: 生成的 prompt 文件路径（online/hybrid 模式且有待翻译条目时）
    """
    translated = {}
    quality_notes = []
    pending_entries = []  # 未命中，需 AI 翻译的条目
    prompt_path = None

    # 仅翻译基础词条（V1范围）
    v1_categories = {"block", "item", "tooltip", "advancement", "entity", "other"}

    # 查询翻译库已有条目
    db_entries = {}
    if _translation_db and mod_id:
        db_entries = _translation_db.lookup_batch(mod_id, target_lang)

    for category, entries in categories.items():
        if category not in v1_categories:
            continue

        for key, value in entries:
            # 1. 翻译库命中（最高优先级）
            if key in db_entries:
                translated[key] = db_entries[key]
                continue

            # 2. 词典翻译（offline 和 hybrid 模式）
            if mode in ("offline", "hybrid"):
                dict_translated = _simple_translate(value, target_lang)
                # 如果词典有翻译且翻译结果与原文不同，使用词典翻译
                if dict_translated != value:
                    translated[key] = dict_translated
                    continue

            # 3. 未命中 → 加入 pending（online 和 hybrid 模式）
            if mode in ("online", "hybrid"):
                pending_entries.append((key, value))
            else:
                # offline 模式：原样保留未命中的条目
                translated[key] = value

    # 生成 prompt 文件（有待翻译条目且非 offline 模式）
    if pending_entries and mode in ("online", "hybrid") and timestamp:
        prompt_path = _emit_translation_prompt(
            mod_id or "unknown",
            target_lang,
            pending_entries,
            jar_path,
            timestamp,
        )

    # 质量说明
    cat_counts = {k: len(v) for k, v in categories.items() if k in v1_categories}
    if cat_counts.get("tooltip", 0) > 50:
        quality_notes.append("建议人工校对：tooltip类词条可能含模组专有术语")
    if cat_counts.get("advancement", 0) > 0:
        quality_notes.append("建议人工校对：advancement类词条需结合游戏进度理解")
    if cat_counts.get("config", 0) > 0:
        quality_notes.append("配置面板文本未汉化（V2功能），如需请升级到V2")
    if pending_entries and mode in ("online", "hybrid"):
        quality_notes.append(f"有 {len(pending_entries)} 条待 AI Agent 翻译，prompt 文件已生成")
    if db_entries:
        quality_notes.append(f"翻译库命中 {len(db_entries)} 条历史翻译")

    return translated, quality_notes, pending_entries, prompt_path


def _generate_html_report(
    jar_path: str,
    target_lang: str,
    categories: Dict[str, List[Tuple[str, str]]],
    zh_cn: Dict[str, str],
    quality_notes: List[str],
    timestamp: str,
) -> str:
    """生成HTML翻译报告"""
    rg = ReportGenerator("基础汉化报告")

    # === 统计概览 ===
    total_entries = sum(len(v) for v in categories.values())
    translated_count = len(zh_cn)
    untranslated_count = total_entries - translated_count

    overview_html = f"""
    <div class='overview-grid'>
      <div class='overview-card'>
        <div class='oc-num'>{total_entries}</div>
        <div class='oc-label'>源词条总数</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{translated_count}</div>
        <div class='oc-label'>已翻译词条</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{untranslated_count}</div>
        <div class='oc-label'>未翻译词条</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{len(categories)}</div>
        <div class='oc-label'>涉及分类</div>
      </div>
    </div>
    """

    # === 分类统计 ===
    category_labels = {
        "block": "方块", "item": "物品", "tooltip": "提示文本",
        "advancement": "进度", "entity": "实体", "sound": "音效",
        "creative": "创造标签", "config": "配置", "other": "其他",
    }

    cat_rows = ""
    for cat, entries in sorted(categories.items(), key=lambda x: -len(x[1])):
        label = category_labels.get(cat, cat)
        v1_tag = " <span class='badge badge-accent'>V1</span>" if cat in {"block", "item", "tooltip", "advancement"} else ""
        cat_rows += f"""
        <tr>
          <td>{label}{v1_tag}</td>
          <td>{len(entries)}</td>
          <td>{'✅' if cat in {'block', 'item', 'tooltip', 'advancement', 'entity', 'other'} else '⏭️'}</td>
        </tr>
        """

    cat_html = f"""
    <div class='callout'>
      <div class='callout-title'>📊 分类统计</div>
      <table class='data-table'>
        <thead>
          <tr><th>分类</th><th>词条数</th><th>V1是否处理</th></tr>
        </thead>
        <tbody>
          {cat_rows}
        </tbody>
      </table>
    </div>
    """

    # === 翻译示例 ===
    sample_entries = list(zh_cn.items())[:20]
    if sample_entries:
        sample_rows = ""
        for key, zh_val in sample_entries:
            en_val = ""
            for cat, entries in categories.items():
                for k, v in entries:
                    if k == key:
                        en_val = v
                        break
                if en_val:
                    break
            sample_rows += f"""
            <tr>
              <td><code>{key}</code></td>
              <td>{en_val}</td>
              <td><strong>{zh_val}</strong></td>
            </tr>
            """
        sample_html = f"""
        <div class='callout'>
          <div class='callout-title'>📝 翻译示例（前20条）</div>
          <table class='data-table'>
            <thead>
              <tr><th>Key</th><th>原文</th><th>译文</th></tr>
            </thead>
            <tbody>
              {sample_rows}
            </tbody>
          </table>
        </div>
        """
    else:
        sample_html = """
        <div class='callout warning'>
          <div class='callout-title'>⚠️ 无翻译内容</div>
          <p>该模组的语言文件可能为空，或已包含中文翻译。</p>
        </div>
        """

    # === 质量说明 ===
    quality_html = ""
    if quality_notes:
        notes_html = "".join(f"<li>{n}</li>" for n in quality_notes)
        quality_html = f"""
        <div class='callout warning'>
          <div class='callout-title'>🔍 质量提示</div>
          <ul>{notes_html}</ul>
        </div>
        """

    # === 技术说明 ===
    tech_html = """
    <div class='callout'>
      <div class='callout-title'>技术说明</div>
      <p>V1基础汉化仅处理以下分类：方块名、物品名、实体名、基础提示文本、进度文本。</p>
      <p>不处理：配置面板GUI文本、光影配置文件、深层代码硬编码文本。这些属于V2深度精细化汉化。</p>
      <p>翻译方式：V1使用本地词典替换，准确率约60%-70%。V2将接入AI翻译API，准确率可达85%-90%。</p>
      <p>建议：使用前人工校对关键词条，特别是模组专有术语。</p>
    </div>
    """

    body_html = f"""
    <h2>翻译概览</h2>
    {overview_html}

    <h2>分类统计</h2>
    {cat_html}

    <h2>翻译示例</h2>
    {sample_html}

    <h2>质量提示</h2>
    {quality_html}

    <h2>技术说明</h2>
    {tech_html}
    """

    return rg.render_full_html("基础汉化报告", body_html, timestamp)


def run(args) -> Dict[str, Any]:
    """F7 基础汉化主入口（V1.0.5 三模式：offline/online/hybrid）

    Args:
        args: argparse.Namespace，需包含:
            - jar_path: JAR文件路径
            - target_lang: 目标语言，默认zh_cn
            - patch_only: 仅生成补丁不固化进JAR
            - mode: 翻译模式（offline/online/hybrid，默认hybrid）
            - response_file: apply-response 模式的响应文件路径
            - output: 输出目录(可选)

    Returns:
        统一返回结构字典
    """
    start_time = datetime.now()
    jar_path = getattr(args, "jar_path", None)
    target_lang = getattr(args, "target_lang", "zh_cn")
    patch_only = getattr(args, "patch_only", False)
    mode = getattr(args, "mode", "hybrid")
    response_file = getattr(args, "response_file", None)
    output_dir = getattr(args, "output", None) or str(config.OUTPUT_DIR / "reports")

    # === apply-response 模式：应用 AI Agent 翻译响应 ===
    if mode == "apply-response":
        if not response_file:
            return config.make_result(
                status="error",
                feature="F7",
                input_summary={"mode": "apply-response"},
                result={"error": "apply-response 模式需要 --response-file 参数"},
                errors=["必须指定 --response-file 参数"],
            )
        if not jar_path:
            return config.make_result(
                status="error",
                feature="F7",
                input_summary={"mode": "apply-response"},
                result={"error": "apply-response 模式需要 --jar-path 参数"},
                errors=["必须指定 --jar-path 参数"],
            )
        result = _apply_translation_response(response_file, jar_path, target_lang)
        return config.make_result(
            status=result.get("status", "success"),
            feature="F7",
            input_summary={"mode": "apply-response", "jar_path": jar_path, "response_file": response_file},
            result=result,
        )

    if not jar_path:
        return config.make_result(
            status="error",
            feature="F7",
            input_summary={"jar_path": None},
            result={"error": "缺少 --jar-path 参数"},
            errors=["必须指定JAR文件路径"],
        )

    jar_path_obj = Path(jar_path)
    if not jar_path_obj.exists():
        return config.make_result(
            status="error",
            feature="F7",
            input_summary={"jar_path": str(jar_path_obj)},
            result={"error": f"文件不存在: {jar_path}"},
            errors=[f"JAR文件不存在: {jar_path}"],
        )

    # 验证 mode 参数
    if mode not in ("offline", "online", "hybrid"):
        return config.make_result(
            status="error",
            feature="F7",
            input_summary={"mode": mode},
            result={"error": f"无效的翻译模式: {mode}"},
            errors=["--mode 必须是 offline/online/hybrid/apply-response"],
        )

    logger.info(f"开始翻译: {jar_path} (模式={mode}, 目标语言={target_lang})")

    # === 1. 查找语言文件 ===
    lang_files = _find_language_files(jar_path_obj)
    if not lang_files:
        return config.make_result(
            status="warning",
            feature="F7",
            input_summary={"jar_path": str(jar_path_obj)},
            result={"error": "未找到英语语言文件(en_us.json)"},
            warnings=["该模组可能没有en_us.json，或语言文件结构特殊"],
        )

    logger.info(f"找到 {len(lang_files)} 个语言文件")

    # === 2. 提取语言内容 ===
    all_lang_data = {}
    for lang_path, local_path in lang_files:
        lang_data = _extract_lang_content(jar_path_obj, lang_path)
        if lang_data:
            all_lang_data[lang_path] = lang_data

    if not all_lang_data:
        return config.make_result(
            status="warning",
            feature="F7",
            input_summary={"jar_path": str(jar_path_obj)},
            result={"error": "语言文件解析失败"},
            warnings=["所有en_us.json文件均无法解析"],
        )

    # === 3. 合并所有语言数据 ===
    merged_lang = {}
    for lang_data in all_lang_data.values():
        merged_lang.update(lang_data)

    # === 4. 分类整理 ===
    categories = _categorize_entries(merged_lang)

    # === 4.5 推断 mod_id（从 JAR 元数据） ===
    mod_id = jar_path_obj.stem
    try:
        from core.jar_parser import parse_mod_metadata, parse_jar_structure
        tmp_dir = create_temp_dir("meta_extract")
        extract_jar(jar_path_obj, tmp_dir)
        meta = parse_mod_metadata(jar_path_obj, tmp_dir)
        if meta.get("mod_id"):
            mod_id = meta["mod_id"]
        cleanup_temp_dir(tmp_dir)
    except Exception:
        pass  # 推断失败用文件名

    # === 5. 生成翻译 ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    translated, quality_notes, pending_entries, prompt_path = _generate_zh_cn(
        merged_lang, categories, target_lang,
        mod_id=mod_id, mode=mode, jar_path=str(jar_path_obj), timestamp=timestamp,
    )

    # === 6. 保存翻译文件 ===
    os.makedirs(output_dir, exist_ok=True)

    # 补丁资源目录
    patch_resources_dir = config.PATCH_DIR / "resources"
    os.makedirs(patch_resources_dir, exist_ok=True)

    # 从语言文件路径推断资源路径
    first_lang_path = lang_files[0][0]
    target_lang_jar_path = first_lang_path.replace("en_us.json", f"{target_lang}.json")

    # 保存到补丁目录
    patch_save_path = patch_resources_dir / target_lang_jar_path
    os.makedirs(patch_save_path.parent, exist_ok=True)

    with open(patch_save_path, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)

    logger.info(f"翻译补丁已生成: {patch_save_path}")

    # === 7. 生成报告 ===
    total_entries = sum(len(v) for v in categories.values())
    report_html = _generate_html_report(
        str(jar_path_obj), target_lang, categories, translated, quality_notes, timestamp
    )
    html_path = Path(output_dir) / f"translator_{timestamp}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    # JSON数据
    json_path = Path(output_dir) / f"translator_{timestamp}.json"
    json_data = {
        "jar_path": str(jar_path_obj),
        "mod_id": mod_id,
        "target_lang": target_lang,
        "mode": mode,
        "categories": {k: len(v) for k, v in categories.items()},
        "total_entries": total_entries,
        "translated_entries": len(translated),
        "pending_entries": len(pending_entries),
        "quality_notes": quality_notes,
        "patch_path": str(patch_save_path),
    }
    if prompt_path:
        json_data["prompt_path"] = prompt_path
        json_data["status_detail"] = "awaiting_agent" if pending_entries else "complete"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # === 8. 如需要，调用F5固化进JAR ===
    output_files = {
        "report": str(html_path),
        "data": str(json_path),
        "patch": str(patch_save_path),
    }
    if prompt_path:
        output_files["prompt"] = prompt_path

    # offline 模式或有翻译结果且无 pending 时才固化
    should_repack = not patch_only and (mode == "offline" or len(pending_entries) == 0)
    if should_repack:
        try:
            from core.repacker import run as repacker_run

            repacker_args = type("Args", (), {
                "jar_path": str(jar_path_obj),
                "resources_dir": str(patch_resources_dir),
                "output": str(Path(config.DOWNLOADS_DIR) / f"{jar_path_obj.stem}_{target_lang}.jar"),
                "validate": True,
            })()

            repacker_result = repacker_run(repacker_args)
            if repacker_result.get("status") == "success":
                output_files["repacked_jar"] = repacker_result["output_files"].get("downloaded", "")
                logger.info(f"翻译JAR已生成: {output_files.get('repacked_jar')}")
            else:
                logger.warning(f"F5固化失败: {repacker_result.get('errors')}")
        except Exception as e:
            logger.warning(f"调用F5失败: {e}")

    # 确定最终状态
    if pending_entries and mode in ("online", "hybrid"):
        final_status = "awaiting_agent"
        logger.info(f"翻译暂停：{len(pending_entries)} 条待 AI Agent 翻译，prompt: {prompt_path}")
    else:
        final_status = "success"

    logger.info(
        f"翻译完成: {len(translated)}条已翻译, "
        f"{len(pending_entries)}条待翻译, "
        f"{len(quality_notes)}条质量提示"
    )

    return config.make_result(
        status=final_status,
        feature="F7",
        input_summary={
            "jar_path": str(jar_path_obj),
            "mod_id": mod_id,
            "target_lang": target_lang,
            "mode": mode,
            "patch_only": patch_only,
        },
        result={
            "total_entries": total_entries,
            "translated_entries": len(translated),
            "pending_entries": len(pending_entries),
            "categories": {k: len(v) for k, v in categories.items()},
            "quality_notes": quality_notes,
            "prompt_path": prompt_path,
            "mode": mode,
        },
        warnings=quality_notes,
        output_files=output_files,
    )
