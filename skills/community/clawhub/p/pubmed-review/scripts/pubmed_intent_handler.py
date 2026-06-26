#!/usr/bin/env python3
"""
PubMed 文献检索意图识别处理器
用法: python3 scripts/pubmed_intent_handler.py "<用户消息>"
"""
import sys
import os
import json
import re
import subprocess
import urllib.request
import urllib.parse

# 路径配置（去硬编码，使用相对路径）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # scripts/ 的父目录即为项目根目录
PROMPT_FILE = os.path.join(SCRIPT_DIR, 'pubmed_intent_prompt.md')
DICT_FILE = os.path.join(SCRIPT_DIR, 'pubmed_medical_dict.json')
TASKS_DIR = os.path.join(BASE_DIR, 'tasks')
TASKS_FILE = os.path.join(TASKS_DIR, 'ablesci_tasks.json')
ADD_TASK_SCRIPT = os.path.join(SCRIPT_DIR, 'add_pubmed_task.py')
# notify 路径：优先环境变量，其次尝试 which 发现
NOTIFY_SCRIPT = os.environ.get('NOTIFY_PATH', '/usr/local/bin/notify' if os.path.exists('/usr/local/bin/notify') else 'notify')

# 加载医学词汇映射表
def load_medical_dict():
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

MEDICAL_DICT = load_medical_dict()

# MiniMax LLM 配置（从 env 文件加载）
def load_llm_env():
    # 优先从环境变量指定的文件加载，其次查找项目根目录的 .env.minimax
    env_file = os.environ.get('MINIMAX_ENV_FILE', os.path.join(BASE_DIR, '.env.minimax'))
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ[k] = v

load_llm_env()

LLM_API_URL = os.environ.get('MINIMAX_API_URL', 'https://api.minimax.chat/v1/text/chatcompletion_v2')
LLM_API_KEY = os.environ.get('MINIMAX_API_KEY', '')
LLM_MODEL = os.environ.get('MINIMAX_MODEL', 'MiniMax-M2.7-highspeed')


def read_prompt():
    with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def call_llm(user_message):
    """调用 MiniMax LLM 进行意图识别"""
    system_prompt = read_prompt()

    payload = {
        'model': LLM_MODEL,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ],
        'max_tokens': 256,
        'temperature': 0.1
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        LLM_API_URL,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LLM_API_KEY}'
        },
        method='POST'
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        msg = result['choices'][0]['message']
        content = msg.get('content', '') or msg.get('reasoning_content', '')
        return content.strip()


def parse_llm_response(text):
    """从 LLM 输出中提取 JSON（鲁棒版本）"""
    import re
    text = text.strip()
    # 策略1：提取 ```json ... ``` 代码块
    if '```' in text:
        for block in text.split('```'):
            block = block.strip()
            if block.startswith('json'):
                block = block[4:].strip()
            if block.startswith('{') and block.endswith('}'):
                return json.loads(block)
    # 策略2：从任意位置找第一个 { 到最后一个 } 的 JSON 对象
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    # 策略3：直接尝试解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    return None


def standardize_term(term):
    """
    医学词汇标准化纠偏（英文→英文）：
    - 短语优先匹配（按 key 长度降序）
    - 不破坏已有的标准英文专有多词短语
    """
    if not term or not MEDICAL_DICT:
        return term
    result = term
    # 按长度降序排列，确保短语优先匹配（如 pulsed dye laser 先于 laser）
    sorted_keys = sorted(MEDICAL_DICT.keys(), key=len, reverse=True)
    for en_word in sorted_keys:
        standard = MEDICAL_DICT[en_word]
        # 大小写敏感替换
        if en_word in result:
            result = result.replace(en_word, standard)
    return result


# OR扩展组：每个key扩展为OR连接的同义词组
OR_GROUP = {
    # scar泛指扩展到具体类型
    'scar': 'scar OR keloid OR hypertrophic scar',
    # keloid/ hypertrophic scar 不扩展（已是特指）
    'hypertrophic scar': 'hypertrophic scar',
    'keloid': 'keloid',
    # laser扩展组
    'fractional laser': 'laser OR fractional laser OR pulsed dye laser OR PDL OR CO2 laser',
    'pulsed dye laser': 'laser OR fractional laser OR pulsed dye laser OR PDL OR CO2 laser',
    'PDL': 'laser OR fractional laser OR pulsed dye laser OR PDL OR CO2 laser',
    'CO2 laser': 'laser OR fractional laser OR pulsed dye laser OR PDL OR CO2 laser',
    'laser': 'laser OR fractional laser OR pulsed dye laser OR PDL OR CO2 laser',
    # 血管瘤扩展组
    'infantile hemangioma': 'infantile hemangioma OR hemangioma',
    'hemangioma': 'infantile hemangioma OR hemangioma',
    # 药物（不扩展）
    'propranolol': 'propranolol',
    'cryotherapy': 'cryotherapy OR cryosurgery',
    'steroid': 'corticosteroid OR steroid injection OR triamcinolone',
}


def expand_search_term(term):
    """
    对 standardize_term 输出的检索词做OR扩展，生成专业化布尔检索式。
    策略：先在原句中把多词短语整体替换为临时占位符，处理完后再恢复并OR扩展。
    """
    if not term or not OR_GROUP:
        return term
    # 按长度降序排列，确保长词优先处理
    sorted_keys = sorted(OR_GROUP.keys(), key=len, reverse=True)
    # 第一步：用临时占位符保护已匹配的多词短语
    temp_map = {}
    temp_result = term
    for key in sorted_keys:
        # 检查key是否完整出现在当前剩余字符串中
        placeholder = f'__TEMP_{len(temp_map)}__'
        if key in temp_result:
            temp_result = temp_result.replace(key, placeholder)
            temp_map[placeholder] = key
    # 第二步：按空格分词，替换非占位符token
    tokens = temp_result.split()
    final_parts = []
    for token in tokens:
        if token in temp_map:
            # 恢复占位符对应的原始key
            original_key = temp_map[token]
            if original_key in OR_GROUP:
                final_parts.append(f'({OR_GROUP[original_key]})')
            else:
                final_parts.append(original_key)
        elif token in OR_GROUP:
            final_parts.append(f'({OR_GROUP[token]})')
        else:
            final_parts.append(token)
    return ' AND '.join(final_parts)


# 限定词映射表
TIME_FILTER = {
    '最近5年': 'last 5 years[dp]',
    '最近10年': 'last 10 years[dp]',
}
TYPE_FILTER = {
    '系统评价': 'systematic review',
    'meta分析': 'meta-analysis',
    '综述': 'review[pt]',
}
POPULATION_FILTER = {
    '儿童': '(child OR infant)',
    '成人': 'adult',
}
STUDY_FILTER = {
    '随机对照': 'randomized controlled trial',
    '临床研究': 'clinical study',
}


def apply_filters(user_text, expanded_term):
    """
    对检索词追加时间、文献类型、人群、研究类型限定词。
    执行顺序：
    1. 时间限定词（取最高优先级）
    2. 文献类型限定词（取最高优先级）
    3. 人群限定词（互斥时跳过）
    4. 仅在前3步均未添加时才加研究类型
    """
    if not user_text:
        return expanded_term

    filters = []

    # 1. 时间（取最高优先级：5年>10年）
    if '最近5年' in user_text:
        filters.append(TIME_FILTER['最近5年'])
    elif '最近10年' in user_text:
        filters.append(TIME_FILTER['最近10年'])

    # 2. 文献类型（取最高优先级：系统评价>meta分析>综述）
    for kw in ['系统评价', 'meta分析', '综述']:
        if kw in user_text:
            filters.append(TYPE_FILTER[kw])
            break

    # 3. 人群（互斥时跳过）
    has_child = '儿童' in user_text
    has_adult = '成人' in user_text
    if has_child and has_adult:
        pass  # 互斥，跳过
    elif has_child:
        filters.append(POPULATION_FILTER['儿童'])
    elif has_adult:
        filters.append(POPULATION_FILTER['成人'])

    # 4. 研究类型（仅当前3步均未添加时使用，随机对照>临床研究）
    if len(filters) == 0:
        for kw in ['随机对照', '临床研究']:
            if kw in user_text:
                filters.append(STUDY_FILTER[kw])
                break

    if not filters:
        return expanded_term

    return expanded_term + ''.join(f' AND {f}' for f in filters)


def run_add_task(search_term):
    """调用 add_pubmed_task.py 创建任务"""
    result = subprocess.run(
        [sys.executable, ADD_TASK_SCRIPT, search_term],
        capture_output=True,
        text=True,
        cwd=BASE_DIR
    )
    return result.returncode, result.stdout, result.stderr


def notify_user(message):
    """发送飞书通知（安全实现，无 shell=True）"""
    msg_file = '/tmp/pubmed_intent_notify.msg'
    with open(msg_file, 'w') as f:
        f.write(message)
    subprocess.run([NOTIFY_SCRIPT, '-t', '文献综述', '-m', message], shell=False)
    os.remove(msg_file)


def main():
    if len(sys.argv) < 2:
        print('用法: python3 scripts/pubmed_intent_handler.py "<用户消息>"')
        sys.exit(1)

    user_message = sys.argv[1]

    # 1. 调用 LLM
    raw_response = call_llm(user_message)

    # 2. 解析 JSON
    parsed = parse_llm_response(raw_response)
    if not parsed:
        print('[pubmed_intent] ERROR: 无法解析LLM输出')
        print(raw_response)
        sys.exit(1)

    intent = parsed.get('intent', 'other')
    search_term = parsed.get('pubmed_search_term', '')
    reply = parsed.get('reply', '')

    print(f'[pubmed_intent] intent={intent}, search_term={search_term}')
    print(f'[pubmed_intent] reply={reply}')

    # 4. 标准化纠偏
    if search_term:
        original_term = search_term
        search_term = standardize_term(search_term)
        if original_term != search_term:
            print(f'[pubmed_intent] 标准化纠偏: {original_term} → {search_term}')

    # 5. 检索词专业化扩展
    if search_term:
        expanded_term = expand_search_term(search_term)
        if expanded_term != search_term:
            print(f'[pubmed_intent] OR扩展: {search_term} → {expanded_term}')
            search_term = expanded_term

    # 6. 追加时间/类型/人群/研究类型限定词
    if search_term:
        filtered_term = apply_filters(user_message, search_term)
        if filtered_term != search_term:
            print(f'[pubmed_intent] 限定词追加: {search_term} → {filtered_term}')
            search_term = filtered_term

    # 7. 规则执行
    if intent == 'pubmed_review' and search_term:
        print(f'[pubmed_intent] 创建任务: {search_term}')
        exit_code, stdout, stderr = run_add_task(search_term)
        if exit_code == 0:
            notify_user(f'已收到您的文献检索请求，正在生成综述...\n\n检索式：{search_term}\n\n请稍候，飞书通知将推送结果。')
            print(f'[pubmed_intent] 任务创建成功')
        else:
            print(f'[pubmed_intent] 任务创建失败: {stderr}')
            notify_user(f'任务创建失败，请稍后重试。')
        print(reply)
    else:
        print(reply)


if __name__ == '__main__':
    main()
