#!/usr/bin/env python3
"""
wardrobe.py - 个人衣橱助手核心逻辑
输入：衣服照片/描述 → 存储
      场景需求（今天穿什么/旅行带什么）→ 推荐搭配
"""
import sys
import os
import json
import shutil
import hashlib
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import (
    init_db, save_clothing, get_all_clothing,
    get_clothing_by_category, search_clothing,
    save_outfit, get_recent_outfits, get_clothing, update_outfit_feedback
)

# ============ 图片存储 ============

_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data', 'images'
)


def store_image(src_path: str, item_name: str = '') -> str:
    """复制图片到本地衣橱目录，返回新路径"""
    if not src_path or not os.path.exists(src_path):
        return ''

    # 安全检查：确保是文件而不是目录
    if not os.path.isfile(src_path):
        return ''

    # 安全检查：限制文件大小（最大 10MB）
    if os.path.getsize(src_path) > 10 * 1024 * 1024:
        return ''

    # 安全检查：限制文件扩展名
    ext = os.path.splitext(src_path)[-1].lower()
    allowed_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if ext not in allowed_exts:
        ext = '.jpg'

    os.makedirs(_IMAGES_DIR, exist_ok=True)

    if item_name:
        safe_name = hashlib.md5(item_name.encode()).hexdigest()[:8]
    else:
        safe_name = hashlib.md5(str(os.path.getsize(src_path)).encode()).hexdigest()[:8]

    new_name = f"{safe_name}{ext}"
    new_path = os.path.join(_IMAGES_DIR, new_name)

    try:
        shutil.copy2(src_path, new_path)
        return new_path
    except Exception:
        return ''


# ============ 搭配推荐引擎 ============

def infer_clothing_attributes(image_path: str = '', user_description: str = '') -> dict:
    """
    根据图片路径或用户描述推断衣服属性。
    实际由调用方（AI对话）补充完整，此处仅提供结构。
    """
    return {
        'category': '',
        'color': '',
        'season': '',
        'style': '',
        'occasion': ''
    }


def build_outfit(items: list, scene: str = '', days: int = 1,
                 weather: str = '') -> str:
    """
    根据已有衣服生成搭配方案
    items: [{name, category, color, season, style, occasion, image_path}, ...]
    scene: 'today' / 'date' / 'work' / 'travel' / etc.
    days: 出行天数（travel时用）
    weather: 天气描述
    """
    scene = _normalize_scene(scene)
    if not items:
        return "❌ 衣橱里没有衣服，请先添加几件衣服再让我推荐搭配～"

    # 按品类分组，再按天气+季节字段在每个品类内排序（避免大热天仍取秋冬款）
    by_category = {}
    for item in items:
        cat = item.get('category', '其他')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)
    by_category = _sort_category_buckets_for_weather(by_category, items, weather)

    lines = []
    scene_label = _scene_label(scene, days, weather)

    lines.append(f"👔 搭配方案")
    lines.append(f"━━━━━━━━━━━━━━")
    lines.append(f"📍 场景：{scene_label}")
    lines.append(f"👕 衣橱共 {len(items)} 件衣服，覆盖 {len(by_category)} 个品类")
    lines.append(f"━━━━━━━━━━━━━━")

    if scene in ('travel', 'trip'):
        # 出行场景：按天数生成每天搭配 + 打包清单
        result = _build_travel_outfit(items, by_category, days, weather)
    elif scene == 'today':
        result = _build_daily_outfit(items, by_category, weather)
    else:
        result = _build_generic_outfit(items, by_category, weather)

    lines.append(result)

    return '\n'.join(lines)


def _scene_label(scene, days, weather):
    labels = {
        'today': '今日穿搭',
        'date': '约会穿搭',
        'work': '上班通勤',
        'casual': '休闲出行',
        'travel': '出行打包',
        'sport': '运动健身',
    }
    base = labels.get(scene, scene or '日常穿搭')
    if days > 1:
        base += f' · {days}天行程'
    if weather:
        base += f' · {weather}'
    return base


def _normalize_scene(scene: str) -> str:
    s = (scene or '').strip().lower()
    mapping = {
        'today': 'today',
        'daily': 'today',
        'date': 'date',
        'dating': 'date',
        'work': 'work',
        'office': 'work',
        'commute': 'work',
        'casual': 'casual',
        'travel': 'travel',
        'trip': 'travel',
        'sport': 'sport',
        'gym': 'sport',
    }
    return mapping.get(s, s or 'today')


def _weather_tag(weather: str) -> str:
    w = (weather or '').lower()
    if any(k in w for k in ['冷', '寒', '低温', 'winter', '下雪', '冰冻']):
        return 'cold'
    # 热带/海岛/暴晒等未写「热」字也应判为高温场景
    if any(
        k in w
        for k in [
            '热', '暑', '高温', '酷暑', '暴晒', 'summer', '热带', '海南', '三亚',
            '海岛', '沙滩', '盛夏',
        ]
    ):
        return 'hot'
    return 'mild'


def _season_hot_score(season: str) -> float:
    """炎热天气下：season 字段适配度，越高越优先。无字段时略低于中性。"""
    s = (season or '').strip()
    if not s:
        return 45.0
    if '四季' in s or '通' in s or '全年' in s:
        return 100.0
    if all(x in s for x in ('春', '夏', '秋', '冬')):
        return 100.0
    if s == '夏' or ('夏' in s and '冬' not in s):
        return 100.0
    if '冬' in s and '夏' not in s:
        return 8.0
    if '秋冬' in s:
        return 12.0
    if '春秋' in s:
        return 28.0
    if s in ('春', '秋'):
        return 42.0
    return 48.0


def _season_cold_score(season: str) -> float:
    """寒冷天气下：season 适配度。"""
    s = (season or '').strip()
    if not s:
        return 45.0
    if '四季' in s or '通' in s or '全年' in s:
        return 95.0
    if '冬' in s or '秋冬' in s:
        return 100.0
    if '夏' in s and '冬' not in s:
        return 15.0
    if '春秋' in s:
        return 55.0
    return 50.0


def _season_weather_score(season: str, weather_tag: str) -> float:
    """当前天气下该衣物的季节适配分；温和天气不区分，仅靠偏好顺序。"""
    if weather_tag == 'mild':
        return 50.0
    if weather_tag == 'hot':
        return _season_hot_score(season)
    if weather_tag == 'cold':
        return _season_cold_score(season)
    return 50.0


def _sort_category_buckets_for_weather(
    by_category: Dict[str, List[dict]],
    ordered_items: List[dict],
    weather: str,
) -> Dict[str, List[dict]]:
    """按天气季节适配优先、再按偏好顺序，对每个品类内排序。"""
    tag = _weather_tag(weather)
    rank_index = {item['id']: i for i, item in enumerate(ordered_items)}

    def sort_key(it: dict):
        sid = it.get('id', '')
        return (
            -_season_weather_score(it.get('season'), tag),
            rank_index.get(sid, 9999),
        )

    out: Dict[str, List[dict]] = {}
    for cat, bucket in by_category.items():
        bucket = list(bucket)
        bucket.sort(key=sort_key)
        out[cat] = bucket
    return out


def _missing_category_hint(by_category: Dict[str, List[dict]]) -> str:
    required = ['上衣', '下装', '鞋子']
    missing = [cat for cat in required if not by_category.get(cat)]
    if not missing:
        return ''
    return f"⚠️ 当前衣橱缺少关键品类：{', '.join(missing)}，推荐结果将自动降级。"


def _missing_required_categories(items: List[dict]) -> List[str]:
    required = ['上衣', '下装', '鞋子']
    present = {i.get('category', '') for i in items}
    return [cat for cat in required if cat not in present]


def _build_preference_profile(limit: int = 100) -> Dict[str, Dict[str, float]]:
    profile: Dict[str, Dict[str, float]] = {
        'item': {},
        'color': {},
        'style': {},
        'category': {},
    }
    feedback_rows = get_recent_outfits(limit)
    weight_map = {'like': 1.0, 'dislike': -1.0, 'neutral': 0.0}
    cache: Dict[str, dict] = {}

    def bump(bucket: str, key: str, w: float):
        if not key:
            return
        profile[bucket][key] = profile[bucket].get(key, 0.0) + w

    for rec in feedback_rows:
        w = weight_map.get((rec.get('feedback') or '').strip().lower(), 0.0)
        if w == 0:
            continue
        for item_id in rec.get('items', []):
            bump('item', item_id, w)
            if item_id not in cache:
                cache[item_id] = get_clothing(item_id) or {}
            item = cache[item_id]
            bump('color', item.get('color', ''), w)
            bump('style', item.get('style', ''), w)
            bump('category', item.get('category', ''), w)

    return profile


def _score_item(item: dict, profile: Dict[str, Dict[str, float]]) -> float:
    # 显式反馈优先：单品 > 颜色/风格/品类
    return (
        profile['item'].get(item.get('id', ''), 0.0) * 3.0
        + profile['color'].get(item.get('color', ''), 0.0) * 1.5
        + profile['style'].get(item.get('style', ''), 0.0) * 1.2
        + profile['category'].get(item.get('category', ''), 0.0) * 1.0
    )


def _rank_items_by_preference(items: List[dict], profile: Dict[str, Dict[str, float]]) -> List[dict]:
    decorated = []
    for idx, item in enumerate(items):
        score = _score_item(item, profile)
        decorated.append((score, -idx, item))
    decorated.sort(reverse=True)
    return [it for _, __, it in decorated]


def _select_items_for_scene(items: List[dict], scene: str, days: int, weather: str) -> List[dict]:
    by_category: Dict[str, List[dict]] = {}
    for item in items:
        by_category.setdefault(item.get('category', '其他'), []).append(item)
    by_category = _sort_category_buckets_for_weather(by_category, items, weather)

    selected: List[dict] = []
    seen_ids = set()

    def pick_first(cat: str):
        for it in by_category.get(cat, []):
            if it['id'] not in seen_ids:
                selected.append(it)
                seen_ids.add(it['id'])
                return

    if scene == 'travel':
        total_sets = max(1, days) + 1
        travel_cats = ['外套', '上衣', '下装', '鞋子', '配饰']
        if _weather_tag(weather) == 'hot':
            travel_cats = ['上衣', '下装', '鞋子', '配饰']
        for cat in travel_cats:
            bucket = by_category.get(cat, [])
            count = min(len(bucket), max(1, total_sets // 5 + 1))
            for it in bucket[:count]:
                if it['id'] not in seen_ids:
                    selected.append(it)
                    seen_ids.add(it['id'])
        return selected

    order = ['上衣', '外套', '下装', '鞋子', '配饰']
    if _weather_tag(weather) == 'hot':
        order = ['上衣', '下装', '鞋子', '配饰']
    for cat in order:
        pick_first(cat)
    return selected


def _build_daily_outfit(items, by_category, weather):
    """单日日常搭配"""
    lines = []
    selected = []

    hint = _missing_category_hint(by_category)
    if hint:
        lines.append(hint)

    weather_tag = _weather_tag(weather)
    cat_candidates = ['上衣', '外套', '下装', '鞋子', '配饰']
    if weather_tag == 'hot':
        cat_candidates = ['上衣', '下装', '鞋子', '配饰']

    # 优先选基础品类
    for cat in cat_candidates:
        if cat in by_category and by_category[cat]:
            item = by_category[cat][0]
            selected.append(item)
            lines.append(f"\n✅ {item['name']}（{item['category']}）")
            if item.get('image_path'):
                lines.append(f"   📷 {item['image_path']}")
            if weather and item.get('season'):
                lines.append(f"   💡 适合{item['season']}季")

    # 颜色协调说明
    colors = [i.get('color', '') for i in selected if i.get('color')]
    if len(colors) >= 2:
        lines.append(f"\n🎨 配色：{' + '.join(colors[:3])}，整体协调")

    return '\n'.join(lines)


def _build_travel_outfit(items, by_category, days, weather):
    """出行打包方案"""
    lines = []

    # 预算：每天至少1套 + 备用1套
    total_sets = days + 1
    packed = set()

    # 按品类选（炎热天气不优先塞厚重外套，与今日/通用一致）
    cat_priority = ['外套', '上衣', '下装', '鞋子', '配饰']
    if _weather_tag(weather) == 'hot':
        cat_priority = ['上衣', '下装', '鞋子', '配饰']
    for cat in cat_priority:
        if cat not in by_category:
            continue
        count = min(len(by_category[cat]), max(1, total_sets // len(cat_priority) + 1))
        for item in by_category[cat][:count]:
            if item['id'] not in packed:
                packed.add(item['id'])
                lines.append(f"🳻 {item['name']}（{cat}）")
                if item.get('color'):
                    lines.append(f"   颜色：{item['color']}")
                if item.get('season'):
                    lines.append(f"   季节：{item['season']}")
                if item.get('image_path'):
                    lines.append(f"   📷 {item['image_path']}")

    hint = _missing_category_hint(by_category)
    if hint:
        lines.insert(0, hint)

    lines.append(f"\n📋 打包总结：共 {len(packed)} 件，覆盖 {len(by_category)} 个品类，{days}天刚好够用")

    # 天气补充建议
    if weather:
        w = weather.lower()
        if '冷' in w or '寒' in w:
            lines.append(f"\n❄️ 天气偏冷，建议带：保暖内衣、围巾、手套")
        elif '热' in w or '暑' in w:
            lines.append(f"\n☀️ 天气炎热，建议带：防晒霜、帽子、墨镜")

    return '\n'.join(lines)


def _build_generic_outfit(items, by_category, weather: str = ''):
    """通用搭配（约会/通勤/休闲等）；炎热时跳过厚重外套，与今日逻辑一致。"""
    lines = []

    weather_tag = _weather_tag(weather)
    cat_priority = ['上衣', '下装', '外套', '鞋子', '配饰']
    if weather_tag == 'hot':
        cat_priority = ['上衣', '下装', '鞋子', '配饰']
    selected = []

    hint = _missing_category_hint(by_category)
    if hint:
        lines.append(hint)

    for cat in cat_priority:
        if cat in by_category:
            for item in by_category[cat]:
                if item['id'] not in [i['id'] for i in selected]:
                    selected.append(item)
                    lines.append(f"\n✅ {item['name']}（{item['category']}）")
                    if item.get('color'):
                        lines.append(f"   颜色：{item['color']}")
                    if item.get('style'):
                        lines.append(f"   风格：{item['style']}")
                    if item.get('image_path'):
                        lines.append(f"   📷 {item['image_path']}")
                    if weather and item.get('season'):
                        lines.append(f"   💡 适合{item['season']}季")
                    break

    colors = [i.get('color', '') for i in selected if i.get('color')]
    if len(colors) >= 2:
        lines.append(f"\n🎨 配色：{' + '.join(colors[:3])}")

    return '\n'.join(lines)


def _json_print(payload: Dict[str, Any]):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _preference_explanations(selected_items: List[dict], profile: Dict[str, Dict[str, float]]) -> List[dict]:
    explanations = []
    for item in selected_items:
        reasons = []
        item_score = profile['item'].get(item.get('id', ''), 0.0)
        color_score = profile['color'].get(item.get('color', ''), 0.0)
        style_score = profile['style'].get(item.get('style', ''), 0.0)
        category_score = profile['category'].get(item.get('category', ''), 0.0)
        if item_score != 0:
            reasons.append(f"单品反馈分={item_score:.1f}")
        if color_score != 0:
            reasons.append(f"颜色偏好分={color_score:.1f}")
        if style_score != 0:
            reasons.append(f"风格偏好分={style_score:.1f}")
        if category_score != 0:
            reasons.append(f"品类偏好分={category_score:.1f}")
        explanations.append({
            'item_id': item.get('id', ''),
            'name': item.get('name', ''),
            'score': _score_item(item, profile),
            'reasons': reasons or ['无历史反馈，按基础规则推荐'],
        })
    return explanations


# ============ CLI ============

def main():
    import argparse
    parser = argparse.ArgumentParser(description='个人衣橱助手')
    sub = parser.add_subparsers(dest='cmd')

    p = sub.add_parser('init')
    p.add_argument('--json', action='store_true')
    p = sub.add_parser('list')
    p.add_argument('--limit', type=int, default=50)
    p.add_argument('--json', action='store_true')

    p = sub.add_parser('add')
    p.add_argument('--name', required=True)
    p.add_argument('--category', default='')
    p.add_argument('--color', default='')
    p.add_argument('--season', default='')
    p.add_argument('--style', default='')
    p.add_argument('--occasion', default='')
    p.add_argument('--image', default='')
    p.add_argument('--json', action='store_true')

    p = sub.add_parser('outfit')
    p.add_argument('--scene', default='today')
    p.add_argument('--days', type=int, default=1)
    p.add_argument('--weather', default='')
    p.add_argument('--json', action='store_true')

    p = sub.add_parser('feedback')
    p.add_argument('--outfit-id', required=True)
    p.add_argument('--feedback', choices=['like', 'dislike', 'neutral'], required=True)
    p.add_argument('--note', default='')
    p.add_argument('--json', action='store_true')

    args = parser.parse_args()

    if args.cmd == 'init':
        init_db()
        if args.json:
            _json_print({'status': 'ok', 'message': '衣橱数据库初始化完成'})
        else:
            print('✅ 衣橱数据库初始化完成')

    elif args.cmd == 'list':
        init_db()
        items = get_all_clothing(args.limit)
        if args.json:
            _json_print({
                'status': 'ok',
                'count': len(items),
                'items': items,
            })
        else:
            print(f'👕 衣橱共有 {len(items)} 件衣服：\n')
            cats = {}
            for item in items:
                cat = item.get('category', '其他')
                cats.setdefault(cat, []).append(item['name'])
            for cat, names in cats.items():
                print(f'【{cat}】{", ".join(names)}')

    elif args.cmd == 'add':
        init_db()
        img_path = ''
        if args.image and os.path.exists(args.image):
            img_path = store_image(args.image, args.name)
        item_id = save_clothing(
            args.name, args.category, args.color,
            args.season, args.style, args.occasion, img_path
        )
        if args.json:
            _json_print({
                'status': 'ok',
                'item_id': item_id,
                'name': args.name,
                'image_path': img_path,
            })
        else:
            print(f'✅ 已存入衣橱（id={item_id}）{f"📷 {img_path}" if img_path else ""}')

    elif args.cmd == 'outfit':
        init_db()
        items = get_all_clothing()
        profile = _build_preference_profile()
        ranked_items = _rank_items_by_preference(items, profile)
        normalized_scene = _normalize_scene(args.scene)
        result = build_outfit(ranked_items, normalized_scene, args.days, args.weather)
        selected_items = _select_items_for_scene(ranked_items, normalized_scene, args.days, args.weather)
        selected_ids = [i['id'] for i in selected_items]
        selected_images = [i.get('image_path', '') for i in selected_items if i.get('image_path')]
        outfit_id = save_outfit(
            name=f'auto-{normalized_scene}',
            scene=normalized_scene,
            description=result,
            items=selected_ids,
            image_paths=selected_images,
        )
        missing_categories = _missing_required_categories(ranked_items)
        preference_applied = any(
            profile[bucket] for bucket in ['item', 'color', 'style', 'category']
        )
        preference_reasons = _preference_explanations(selected_items, profile)
        if args.json:
            _json_print({
                'status': 'ok',
                'outfit_id': outfit_id,
                'scene': normalized_scene,
                'days': args.days,
                'weather': args.weather,
                'wardrobe_count': len(items),
                'category_count': len({i.get("category", "") for i in items}),
                'missing_categories': missing_categories,
                'is_degraded': len(missing_categories) > 0,
                'preference_applied': preference_applied,
                'preference_reasons': preference_reasons,
                'selected_items': selected_items,
                'result': result,
            })
        else:
            print(result)
            print(f"\n🧾 本次搭配记录ID：{outfit_id}")
            if preference_applied:
                print("💬 已应用历史显式反馈（like/dislike）进行排序。")

    elif args.cmd == 'feedback':
        init_db()
        ok = update_outfit_feedback(args.outfit_id, args.feedback, args.note)
        if args.json:
            _json_print({
                'status': 'ok' if ok else 'error',
                'outfit_id': args.outfit_id,
                'feedback': args.feedback,
                'note': args.note,
                'updated': ok,
            })
        else:
            if ok:
                print(f"✅ 已记录反馈：{args.outfit_id} -> {args.feedback}")
            else:
                print(f"❌ 未找到搭配记录：{args.outfit_id}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
