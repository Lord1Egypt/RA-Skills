#!/usr/bin/env python3
"""Semantic metadata and matching for sticker-manager."""
import json
import os
import sys
from typing import Dict, List, Optional, Tuple

from common import get_target_dir, SUPPORTED_EXTS, t, get_lang, build_vision_plan_json, build_vision_plan, get_vision_models

TARGET_DIR = get_target_dir()
TAGS_FILE = os.path.join(TARGET_DIR, '.tags.json')

# Additional messages for new commands
MESSAGES_SEMANTIC: Dict[str, Dict[str, str]] = {
    "auto_tag_title": {"zh": "🏷️ 自动标签生成:", "en": "🏷️ Auto-tagging:"},
    "auto_tag_item": {"zh": "  分析: {name}", "en": "  Analyzing: {name}"},
    "auto_tag_vision": {"zh": "  需要视觉分析: {path}", "en": "  Vision analysis needed: {path}"},
    "auto_tag_saved": {"zh": "  ✓ 已保存标签: {name}", "en": "  ✓ Tags saved: {name}"},
    "auto_tag_no_files": {"zh": "未找到图片文件", "en": "No image files found"},
    "auto_tag_done": {"zh": "\n✅ 完成: {count} 个文件已处理", "en": "\n✅ Done: {count} files processed"},
    "context_rec_title": {"zh": "🎯 上下文推荐分析:", "en": "🎯 Context-aware recommendation:"},
    "context_rec_history": {"zh": "  对话历史 ({count} 条):", "en": "  Chat history ({count} messages):"},
    "context_rec_analysis": {"zh": "  分析: {analysis}", "en": "  Analysis: {analysis}"},
    "context_rec_top": {"zh": "  Top {n} 推荐:", "en": "  Top {n} recommendations:"},
    "context_rec_item": {"zh": "    {rank}. {name} (匹配度: {score})", "en": "    {rank}. {name} (score: {score})"},
    "context_rec_reason": {"zh": "       理由: {reason}", "en": "       Reason: {reason}"},
    "context_rec_no_history": {"zh": "未提供对话历史", "en": "No chat history provided"},
    "usage_semantic_extended": {
        "zh": "用法:\n  {cmd} tag <name> <emotions> <scenes> <keywords> [description]\n  {cmd} suggest <context> [--strategy auto|model|rules]\n  {cmd} prepare-model <context>\n  {cmd} vision-plan <image_path> [context]\n  {cmd} list\n  {cmd} auto-tag <path> [--apply]\n  {cmd} auto-tag-dir <directory> [--apply]\n  {cmd} context-recommend <history_file|json> [--top 3]",
        "en": "Usage:\n  {cmd} tag <name> <emotions> <scenes> <keywords> [description]\n  {cmd} suggest <context> [--strategy auto|model|rules]\n  {cmd} prepare-model <context>\n  {cmd} vision-plan <image_path> [context]\n  {cmd} list\n  {cmd} auto-tag <path> [--apply]\n  {cmd} auto-tag-dir <directory> [--apply]\n  {cmd} context-recommend <history_file|json> [--top 3]"
    },
}


def t_semantic(key: str, lang: str, **kwargs) -> str:
    entry = MESSAGES_SEMANTIC.get(key, {})
    template = entry.get(lang) or entry.get('en') or key
    return template.format(**kwargs)


def load_tags() -> Dict:
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_tags(tags: Dict):
    os.makedirs(TARGET_DIR, exist_ok=True)
    with open(TAGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)


def resolve_sticker_name(sticker_name: str) -> str:
    ext = os.path.splitext(sticker_name)[1].lower()
    if ext in SUPPORTED_EXTS:
        return sticker_name
    for candidate_ext in SUPPORTED_EXTS:
        candidate = sticker_name + candidate_ext
        if os.path.exists(os.path.join(TARGET_DIR, candidate)):
            return candidate
    return sticker_name + '.jpg'


def add_tags(sticker_name: str, emotions: List[str], scenes: List[str], keywords: List[str], description: str = ''):
    tags = load_tags()
    sticker_name = resolve_sticker_name(sticker_name)
    tags[sticker_name] = {
        'emotions': emotions,
        'scenes': scenes,
        'keywords': keywords,
        'description': description.strip(),
    }
    save_tags(tags)
    return True


def list_entries() -> List[Dict]:
    tags = load_tags()
    entries = []
    for sticker_name, tag_data in tags.items():
        sticker_path = os.path.join(TARGET_DIR, sticker_name)
        if os.path.exists(sticker_path):
            entries.append({
                'name': sticker_name,
                'path': sticker_path,
                'emotions': tag_data.get('emotions', []),
                'scenes': tag_data.get('scenes', []),
                'keywords': tag_data.get('keywords', []),
                'description': tag_data.get('description', ''),
            })
    return entries


def build_model_payload(context: str) -> Dict:
    return {
        'task': 'Choose the most suitable sticker for the user context based on semantic meaning, not string overlap.',
        'context': context,
        'instructions': [
            'Read the context and candidate descriptions.',
            'Pick the best candidate semantically.',
            'Prefer emotional and situational fit over keyword overlap.',
            'Return top candidates and explain the choice briefly.',
        ],
        'candidates': list_entries(),
    }


def find_by_rules(context: str) -> List[tuple]:
    tags = load_tags()
    if not tags:
        return []

    context_lower = context.lower()
    matches = []
    for sticker_name, tag_data in tags.items():
        score = 0
        matched_reasons = []
        for emotion in tag_data.get('emotions', []):
            if emotion.lower() in context_lower:
                score += 3
                matched_reasons.append(f'emotion:{emotion}')
        for scene in tag_data.get('scenes', []):
            if scene.lower() in context_lower:
                score += 3
                matched_reasons.append(f'scene:{scene}')
        for keyword in tag_data.get('keywords', []):
            if keyword.lower() in context_lower:
                score += 2
                matched_reasons.append(f'keyword:{keyword}')
        description = tag_data.get('description', '').lower()
        if description and any(token in description for token in context_lower.split() if len(token) > 1):
            score += 1
            matched_reasons.append('description-overlap')
        if score > 0:
            sticker_path = os.path.join(TARGET_DIR, sticker_name)
            if os.path.exists(sticker_path):
                matches.append((sticker_name, score, matched_reasons, sticker_path))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def suggest_for_context(context: str, strategy: str = 'auto', lang: Optional[str] = None) -> Optional[str]:
    payload = build_model_payload(context)
    if strategy in ('auto', 'model'):
        print('__MODEL_MATCH__:' + json.dumps(payload, ensure_ascii=False))
        if strategy == 'model':
            return None
    matches = find_by_rules(context)
    if matches:
        best_match = matches[0]
        print(t('recommendation', lang, name=best_match[0], score=best_match[1], reasons=', '.join(best_match[2])))
        return best_match[3]
    # If we have candidates and model strategy was used, still return success
    # The outer agent will process __MODEL_MATCH__ output
    if strategy == 'auto' and payload['candidates']:
        return None  # Model match was output, return None but not error
    return None


def auto_tag_sticker(sticker_name: str, description: str):
    return '__NEED_AUTO_TAG__'


# ============== NEW FUNCTIONS ==============

def build_auto_tag_plan(image_path: str, lang: str = 'en') -> Dict:
    """Build a vision plan for auto-tagging a single image."""
    return build_vision_plan(
        image_path,
        'Analyze this sticker image and extract: 1) emotions (list of emotional expressions), 2) scenes (list of contexts where this would fit), 3) keywords (list of descriptive keywords), 4) a brief description of what the image shows. Return as JSON.',
        lang
    )


def auto_tag_file(image_path: str, apply_tags: bool = False, lang: str = 'en') -> Dict:
    """
    Generate auto-tag plan for a single image file.
    Returns a plan that needs to be executed by a vision-capable model.
    """
    path = os.path.expanduser(image_path)
    if not os.path.exists(path):
        return {'error': f'File not found: {path}', 'status': 'error'}
    
    name = os.path.basename(path)
    plan = build_auto_tag_plan(path, lang)
    
    result = {
        'name': name,
        'path': path,
        'status': 'pending',
        'vision_plan': plan,
    }
    
    # Output the plan for the caller to execute
    print(json.dumps(result, ensure_ascii=False))
    print(f'__AUTO_TAG__:{json.dumps(result, ensure_ascii=False)}')
    
    return result


def auto_tag_directory(directory: str, apply_tags: bool = False, lang: str = 'en') -> List[Dict]:
    """
    Generate auto-tag plans for all images in a directory.
    """
    dir_path = os.path.expanduser(directory)
    if not os.path.isdir(dir_path):
        print(t_semantic('auto_tag_no_files', lang))
        return []
    
    print(t_semantic('auto_tag_title', lang))
    
    results = []
    for f in sorted(os.listdir(dir_path)):
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS:
            path = os.path.join(dir_path, f)
            print(t_semantic('auto_tag_item', lang, name=f))
            result = auto_tag_file(path, apply_tags=apply_tags, lang=lang)
            results.append(result)
    
    if results:
        print(t_semantic('auto_tag_done', lang, count=len(results)))
    
    return results


def analyze_chat_history(history: List[Dict], lang: str = 'en') -> Dict:
    """
    Analyze chat history for context-aware recommendation.
    Expects a list of message dicts with 'content' and optionally 'role', 'timestamp'.
    """
    if not history:
        return {'error': 'No history provided', 'emotions': [], 'topics': []}
    
    # Extract text content
    texts = []
    for msg in history:
        content = msg.get('content', '') or msg.get('text', '')
        if content:
            texts.append(content)
    
    # Combine recent messages for analysis
    combined = '\n'.join(texts[-10:])  # Last 10 messages
    
    # Build analysis plan for model
    analysis_plan = {
        'task': 'Analyze the chat history and extract context for sticker recommendation.',
        'language': lang,
        'history': texts[-10:],
        'extract': [
            'dominant_emotion: The main emotional tone of the conversation',
            'topics: Key topics being discussed',
            'sentiment: positive/negative/neutral',
            'urgency: How urgent the conversation feels',
            'formality: casual/formal tone',
        ],
        'output_format': {
            'emotions': ['list of detected emotions'],
            'topics': ['list of topics'],
            'sentiment': 'positive/negative/neutral',
            'context_summary': 'brief summary of conversation context',
        }
    }
    
    print('__ANALYZE_HISTORY__:' + json.dumps(analysis_plan, ensure_ascii=False))
    
    return analysis_plan


def context_recommend(history: List[Dict], top_n: int = 3, lang: str = 'en') -> List[Dict]:
    """
    Generate context-aware sticker recommendations based on chat history.
    """
    print(t_semantic('context_rec_title', lang))
    
    if not history:
        print(t_semantic('context_rec_no_history', lang))
        return []
    
    print(t_semantic('context_rec_history', lang, count=len(history)))
    for i, msg in enumerate(history[-5:], 1):
        content = msg.get('content', '') or msg.get('text', '')
        if content:
            preview = content[:50] + '...' if len(content) > 50 else content
            print(f'    {i}. {preview}')
    
    # Analyze history
    analysis = analyze_chat_history(history, lang)
    
    # Get all tagged stickers
    entries = list_entries()
    if not entries:
        return []
    
    # Combine all text for matching
    combined_text = ' '.join([
        msg.get('content', '') or msg.get('text', '')
        for msg in history
    ]).lower()
    
    # Score each sticker based on context
    scored = []
    for entry in entries:
        score = 0
        reasons = []
        
        # Match emotions from tags with history context
        for emotion in entry.get('emotions', []):
            if emotion.lower() in combined_text:
                score += 3
                reasons.append(f'emotion match: {emotion}')
        
        # Match scenes
        for scene in entry.get('scenes', []):
            if scene.lower() in combined_text:
                score += 2
                reasons.append(f'scene match: {scene}')
        
        # Match keywords
        for keyword in entry.get('keywords', []):
            if keyword.lower() in combined_text:
                score += 2
                reasons.append(f'keyword: {keyword}')
        
        # Description semantic match (needs model)
        if entry.get('description'):
            score += 1
            reasons.append('has description')
        
        if score > 0 or len(scored) < top_n:  # Include some even without matches
            scored.append({
                'name': entry['name'],
                'path': entry['path'],
                'score': score,
                'reasons': reasons,
                'tags': entry,
            })
    
    # Sort by score
    scored.sort(key=lambda x: x['score'], reverse=True)
    top_results = scored[:top_n]
    
    print(t_semantic('context_rec_top', lang, n=top_n))
    for i, result in enumerate(top_results, 1):
        print(t_semantic('context_rec_item', lang, rank=i, name=result['name'], score=result['score']))
        if result['reasons']:
            reasons_str = ', '.join(result['reasons'][:3])
            print(t_semantic('context_rec_reason', lang, reason=reasons_str))
    
    # Output for model processing
    recommendation_payload = {
        'task': 'Select the best stickers for the conversation context.',
        'language': lang,
        'history_summary': combined_text[:500],
        'top_candidates': top_results,
        'requested_top_n': top_n,
    }
    print('\n__CONTEXT_RECOMMEND__:' + json.dumps(recommendation_payload, ensure_ascii=False))
    
    return top_results


if __name__ == '__main__':
    lang = get_lang()
    raw_args = sys.argv[1:]
    args = []
    strategy = 'auto'
    apply_tags = False
    top_n = 3
    
    for arg in raw_args:
        if arg.startswith('--lang='):
            lang = get_lang(arg.split('=', 1)[1])
        elif arg.startswith('--strategy='):
            strategy = arg.split('=', 1)[1]
        elif arg == '--apply':
            apply_tags = True
        elif arg.startswith('--top='):
            top_n = int(arg.split('=', 1)[1])
        else:
            args.append(arg)

    if len(args) < 1:
        print(t_semantic('usage_semantic_extended', lang, cmd=sys.argv[0]))
        raise SystemExit(1)

    action = args[0]
    
    # Existing actions
    if action == 'tag' and len(args) >= 5:
        name = args[1]
        emotions = args[2].split(',') if args[2] else []
        scenes = args[3].split(',') if args[3] else []
        keywords = args[4].split(',') if args[4] else []
        description = args[5] if len(args) >= 6 else ''
        add_tags(name, emotions, scenes, keywords, description)
        description_line = t('description_line', lang, description=description) if description else ''
        print(t('tag_added', lang, name=name, emotions=emotions, scenes=scenes, keywords=keywords, description_line=description_line))
        raise SystemExit(0)

    if action == 'suggest' and len(args) >= 2:
        context = args[1]
        payload = build_model_payload(context)
        result = suggest_for_context(context, strategy=strategy, lang=lang)
        if result:
            print(result)
            raise SystemExit(0)
        if strategy == 'model':
            raise SystemExit(0)
        # For 'auto' strategy with candidates, return success even without rule match
        if strategy == 'auto' and payload['candidates']:
            raise SystemExit(0)
        print(t('no_match', lang))
        raise SystemExit(1)

    if action == 'prepare-model' and len(args) >= 2:
        context = args[1]
        print(json.dumps(build_model_payload(context), ensure_ascii=False, indent=2))
        raise SystemExit(0)

    if action == 'vision-plan' and len(args) >= 2:
        image_path = args[1]
        context = args[2] if len(args) >= 3 else ''
        print(build_vision_plan_json(image_path, context, lang))
        raise SystemExit(0)

    if action == 'list':
        tags = load_tags()
        if tags:
            print(t('tags_title', lang))
            for name, data in tags.items():
                emotions = ','.join(data.get('emotions', []))
                scenes = ','.join(data.get('scenes', []))
                desc = data.get('description', '')
                suffix = f' | [{desc}]' if desc else ''
                print(f'  {name}: [{emotions}] | [{scenes}]{suffix}')
        else:
            print(t('tags_empty', lang))
        raise SystemExit(0)

    # NEW ACTIONS
    if action == 'auto-tag' and len(args) >= 2:
        image_path = args[1]
        result = auto_tag_file(image_path, apply_tags=apply_tags, lang=lang)
        raise SystemExit(0 if result.get('status') != 'error' else 1)

    if action == 'auto-tag-dir' and len(args) >= 2:
        directory = args[1]
        results = auto_tag_directory(directory, apply_tags=apply_tags, lang=lang)
        raise SystemExit(0 if results else 1)

    if action == 'context-recommend' and len(args) >= 2:
        history_input = args[1]
        history = []
        
        # Try to load history from file or parse as JSON
        if os.path.exists(os.path.expanduser(history_input)):
            with open(os.path.expanduser(history_input), 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    history = json.loads(content)
                    if isinstance(history, str):
                        # Single text, wrap it
                        history = [{'content': history}]
                except json.JSONDecodeError:
                    # Treat each line as a message
                    history = [{'content': line.strip()} for line in content.splitlines() if line.strip()]
        else:
            # Try to parse as JSON string
            try:
                history = json.loads(history_input)
                if isinstance(history, str):
                    history = [{'content': history}]
            except json.JSONDecodeError:
                # Treat as single message
                history = [{'content': history_input}]
        
        results = context_recommend(history, top_n=top_n, lang=lang)
        raise SystemExit(0 if results else 1)

    print(t('unknown_action', lang))
    raise SystemExit(1)