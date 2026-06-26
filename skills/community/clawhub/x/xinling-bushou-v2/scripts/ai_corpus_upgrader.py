#!/usr/bin/env python3
"""
心灵补手 AI 语料扩充器
调用MiniMax API生成高质量语料
"""

import json
import os
import random
from datetime import datetime
import urllib.request
import urllib.error

UPGRADE_DIR = "/root/.openclaw/workspace/xinling-bushou-v2"
META_DIR = f"{UPGRADE_DIR}/meta_features"
PERSONAS_DIR = f"{UPGRADE_DIR}/personas"
CORPUS_DIR = f"{UPGRADE_DIR}/corpus"

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_api_key():
    key_file = "/root/.openclaw/.credentials/minimax_api.txt"
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return f.read().strip()
    return None

def call_ai(prompt, model="MiniMax-Text-01"):
    api_key = get_api_key()
    if not api_key:
        return None, "No API key"
    
    # MiniMax API endpoint
    url = "https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId=&AuthToken=" + api_key
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
        "max_tokens": 2000
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            if 'choices' in result:
                return result['choices'][0]['message']['content'], None
            elif 'BaseResp' in result:
                return None, f"MiniMax Error: {result.get('BaseResp', {}).get('RetMsg', 'unknown')}"
            return None, "Unknown response format"
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return None, f"HTTP {e.code}: {error_body[:200]}"
    except Exception as e:
        return None, str(e)

def generate_meta_features(persona_id, name, desc):
    """为人格生成元特征库"""
    
    prompt = f"""为人物「{name}」建立元特征库。

人物描述：{desc}

请生成一个完整的元特征库JSON，包含：
1. historical_record: 历史记录（时期、角色、简介、历史评价、关键特征）
2. signature_quotes: 标志性言行（3-5个典型场景或代表性话语）
3. speaking_patterns: 说话模式（各级别语气表达、情感标记、禁忌元素）
4. upgrade_targets: 升级目标（语料缺口、建议增加的内容）
5. design_notes: 设计要点（核心原则、最佳程度、避免项）

输出完整JSON，不要其他文字："""

    response, error = call_ai(prompt)
    
    if error:
        log(f"API调用失败: {error}")
        return None
    
    try:
        json_str = response.strip()
        if '{' in json_str:
            json_str = json_str[json_str.index('{'):]
        if '}' not in json_str:
            # Try to find closing brace
            last_brace = json_str.rfind('}')
            if last_brace > 0:
                json_str = json_str[:last_brace+1]
        
        meta_data = json.loads(json_str)
        meta_data['meta_version'] = '1.0.0'
        meta_data['persona_id'] = persona_id
        meta_data['name'] = name
        meta_data['generated_at'] = datetime.now().isoformat()
        return meta_data
    except json.JSONDecodeError as e:
        log(f"JSON解析失败: {e}")
        log(f"原始响应前300字: {response[:300]}")
        return None

def generate_corpus(persona_id, meta_data):
    """根据元特征库生成语料"""
    
    name = meta_data.get('name', persona_id)
    historical = meta_data.get('historical_record', {})
    signature = meta_data.get('signature_quotes', {})
    patterns = meta_data.get('speaking_patterns', {})
    gaps = meta_data.get('upgrade_targets', {}).get('corpus_gaps', [])
    design_notes = meta_data.get('design_notes', {})
    
    gaps_str = '\n'.join(['- ' + g for g in gaps]) if gaps else '- 无特别标注'
    original_quotes = signature.get('original', [])
    if isinstance(original_quotes, list) and len(original_quotes) > 0:
        if isinstance(original_quotes[0], dict):
            quotes_text = '\n'.join([f"- {q.get('text', q)}" for q in original_quotes[:3]])
        else:
            quotes_text = '\n'.join([f"- {q}" for q in original_quotes[:3]])
    else:
        quotes_text = "无"
    
    prompt = f"""为人物「{name}」生成谄媚对话语料。

【人物背景】
时期: {meta_data.get('historical_period', '未知')}
角色: {meta_data.get('role', '未知')}
简介: {historical.get('简介', '无')}

【说话模式】
最高级: {patterns.get('formal_level', {}).get('highest', '')}
高级: {patterns.get('formal_level', {}).get('high', '')}
中级: {patterns.get('formal_level', {}).get('medium', '')}
低级: {patterns.get('formal_level', {}).get('low', '')}

【设计要点】
核心原则: {design_notes.get('core_principle', '')}
最佳程度: {design_notes.get('sweet_spot', '')}
避免: {design_notes.get('avoid', '')}

【需要填补的缺口】
{gaps_str}

请生成10组语料，场景包括task_completed、share_good_news、general_praise、emotional_low、被批评后回应等。

输出JSON格式：
{{"generated_corpus": [{{"scenario": "场景", "level": 1-10, "text": "对话"}}, ...]}}
只输出JSON："""

    response, error = call_ai(prompt)
    
    if error:
        log(f"API调用失败: {error}")
        return None
    
    try:
        json_str = response.strip()
        if '{' in json_str:
            json_str = json_str[json_str.index('{'):]
        if '}' not in json_str:
            last_brace = json_str.rfind('}')
            if last_brace > 0:
                json_str = json_str[:last_brace+1]
        
        data = json.loads(json_str)
        return data.get('generated_corpus', [])
    except json.JSONDecodeError as e:
        log(f"JSON解析失败: {e}")
        return None

def main():
    log("=" * 50)
    log("心灵补手 AI 语料扩充器")
    log("=" * 50)
    
    os.makedirs(META_DIR, exist_ok=True)
    os.makedirs(CORPUS_DIR, exist_ok=True)
    
    persona_files = [f.replace('.json', '') for f in os.listdir(PERSONAS_DIR) 
                     if f.endswith('.json') and f != '_registry.json']
    meta_files = set(f.replace('_meta.json', '') for f in os.listdir(META_DIR) 
                    if f.endswith('_meta.json'))
    
    unmetaed = [p for p in persona_files if p not in meta_files]
    
    log(f"人格总数: {len(persona_files)}, 已建元特征: {len(meta_files)}, 未建: {len(unmetaed)}")
    
    if unmetaed:
        target = unmetaed[0]
        persona_file = f"{PERSONAS_DIR}/{target}.json"
        
        if os.path.exists(persona_file):
            data = load_json(persona_file)
            name = data.get('name', data.get('meta', {}).get('name', target))
            desc = data.get('description', data.get('meta', {}).get('description', ''))
            
            log(f"正在为「{name}」生成元特征库...")
            meta = generate_meta_features(target, name, desc)
            
            if meta:
                meta_file = f"{META_DIR}/{target}_meta.json"
                save_json(meta_file, meta)
                log(f"✅ 元特征库已创建: {meta_file}")
                
                log("正在生成初始语料...")
                corpus = generate_corpus(target, meta)
                if corpus:
                    corpus_file = f"{CORPUS_DIR}/{target}_ai_generated.json"
                    save_json(corpus_file, corpus)
                    log(f"✅ 生成语料 {len(corpus)} 条: {corpus_file}")
                    for item in corpus[:2]:
                        log(f"   [{item['scenario']}] L{item['level']}: {item['text'][:50]}...")
            else:
                log("❌ 元特征库生成失败")
    else:
        target = random.choice(list(meta_files))
        log(f"扩充 {target} 语料...")
        
        meta_file = f"{META_DIR}/{target}_meta.json"
        meta = load_json(meta_file)
        
        corpus = generate_corpus(target, meta)
        if corpus:
            corpus_file = f"{CORPUS_DIR}/{target}_ai_generated.json"
            
            existing = []
            if os.path.exists(corpus_file):
                existing = load_json(corpus_file)
            
            existing.extend(corpus)
            save_json(corpus_file, existing)
            log(f"✅ 新增语料 {len(corpus)} 条，总计 {len(existing)} 条")
            
            for item in corpus[:2]:
                log(f"   [{item['scenario']}] L{item['level']}: {item['text'][:50]}...")
    
    log("=" * 50)
    log("完成")
    log("=" * 50)

if __name__ == "__main__":
    main()
