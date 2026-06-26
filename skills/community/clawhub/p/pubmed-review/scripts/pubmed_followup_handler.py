#!/usr/bin/env python3
"""
PubMed 综述追问处理器
用法: python3 scripts/pubmed_followup_handler.py "<用户追问>"
"""
import sys
import os
import json
import re
import subprocess
import urllib.request

# 路径配置（去硬编码）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
TASKS_DIR = os.path.join(BASE_DIR, 'tasks')
TASKS_FILE = os.path.join(TASKS_DIR, 'ablesci_tasks.json')
RESULTS_DIR = os.path.join(BASE_DIR, 'results', 'pubmed')
FOLLOWUP_STATE_FILE = os.path.join(BASE_DIR, '.pubmed_last_followed.json')
NOTIFY_SCRIPT = os.environ.get('NOTIFY_PATH', '/usr/local/bin/notify' if os.path.exists('/usr/local/bin/notify') else 'notify')

# MiniMax LLM 配置
def load_llm_env():
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

# 追问关键词
FOLLOWUP_KEYWORDS = [
    '展开', '详细说', '具体是', '解释一下',
    '哪些文献', '哪篇', '对应哪些',
    '机制是什么', '为什么', '如何实现',
    '有哪些证据', '支持这个结论',
    '展开讲', '详细讲', '具体机制',
]


def is_followup(text):
    """纯规则判断是否追问"""
    for kw in FOLLOWUP_KEYWORDS:
        if kw in text:
            return True
    return False


def extract_task_id(text):
    """从消息中提取显式 task_id（第一优先）"""
    import re
    # 匹配 task_id 格式：pubmed_数字_随机4位
    match = re.search(r'pubmed_\d+_\w{4}', text)
    if match:
        return match.group()
    return None


def find_active_followed_task():
    """找最近一次通过飞书通知返回给用户的任务（第二优先）"""
    if not os.path.exists(FOLLOWUP_STATE_FILE):
        return None
    try:
        with open(FOLLOWUP_STATE_FILE, 'r') as f:
            state = json.load(f)
        task_id = state.get('last_followed_task_id')
        if not task_id:
            return None
        # 验证该任务仍然存在且为 completed
        if not os.path.exists(TASKS_FILE):
            return None
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            for t in json.load(f):
                if t.get('id') == task_id and t.get('status') == 'completed':
                    return t
        return None
    except:
        return None


def match_task_by_keywords(question, tasks_list):
    """用户问题关键词 vs 各 task topic 匹配（第三优先）"""
    import re
    q_words = set(re.findall(r'\w+', question.lower()))
    scored = []
    for t in tasks_list:
        if t.get('status') != 'completed' or t.get('type') != 'pubmed_review':
            continue
        topic_words = set(re.findall(r'\w+', t.get('payload', {}).get('topic', '').lower()))
        score = len(q_words & topic_words)
        if score > 0:
            scored.append((score, t))
    if not scored:
        return None
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def find_latest_completed_task():
    """找最近一次 completed 的 pubmed_review 任务（第四优先）"""
    if not os.path.exists(TASKS_FILE):
        return None
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    completed = [
        t for t in tasks
        if t.get('type') == 'pubmed_review'
        and t.get('status') == 'completed'
    ]
    if not completed:
        return None
    # 按 created_at 降序
    completed.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return completed[0]


def get_articles_file(task_id):
    """获取 articles.json 路径"""
    path = os.path.join(RESULTS_DIR, f'{task_id}_articles.json')
    return path if os.path.exists(path) else None


def score_articles(articles, query):
    """关键词重叠评分：标题命中×3，摘要命中×1"""
    query_words = re.findall(r'\w+', query.lower())
    scored = []
    for art in articles:
        score = 0
        title_words = set(re.findall(r'\w+', art.get('title', '').lower()))
        abstract_words = set(re.findall(r'\w+', art.get('abstract', '').lower()))
        for w in query_words:
            if len(w) < 2:
                continue
            if w in title_words:
                score += 3
            if w in abstract_words:
                score += 1
        scored.append((score, art))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def build_reference_list(articles):
    """构建参考文献列表（含PMID）"""
    lines = []
    for i, art in enumerate(articles, 1):
        title = art.get('title', '未知')[:80]
        year = art.get('year', 'n.d.')
        pmid = art.get('pmid', '')
        authors = art.get('authors', [])
        author_str = ', '.join(authors[:3]) + (' et al.' if len(authors) > 3 else '')
        pmid_display = pmid if pmid else "未提供"
        lines.append(f"{i}. {title} ({year}) PMID:{pmid_display} — {author_str}")
    return '\n'.join(lines)


def call_llm(question, all_titles, top_articles):
    """调用 LLM 回答追问"""
    articles_text = []
    for i, art in enumerate(top_articles, 1):
        pmid = art.get('pmid', '')
        pmid_display = pmid if pmid else "未提供"
        articles_text.append(
            f"【文献{i}】\n标题：{art.get('title','未知')}\n"
            f"PMID：{pmid}\n"
            f"摘要：{art.get('abstract','无')[:400]}\n"
        )

    prompt = f"""你是一个医学文献助手。用户正在追问一篇已生成的文献综述。

用户问题：{question}

以下是相关文献的标题（完整列表）：
{all_titles}

以下是得分最高的相关文献摘要：
{'\n'.join(articles_text)}

请基于以上内容回答用户追问。

要求：
1. 回答简洁，针对用户问题
2. 引用相关文献（用 [1]、[2] 等格式，标注PMID）
3. 如实说明，不要编造文献中没有的信息
4. 优先选3-5篇最相关的文献

回答格式：
回答：...

相关文献：
1. 文献标题（年份）PMID: xxxxxxxx
2. 文献标题（年份）PMID: xxxxxxxx
...
（没有PMID的不要写，不要编造）"""

    payload = {
        'model': LLM_MODEL,
        'messages': [
            {'role': 'system', 'content': '你是一个严谨的医学文献助手，基于提供的文献内容回答问题，如实引用，不编造。'},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 800,
        'temperature': 0.3
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

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        msg = result['choices'][0]['message']
        content = msg.get('content', '') or msg.get('reasoning_content', '')
        return content.strip() if content else None


def notify_user(message):
    """发送飞书消息"""
    subprocess.run(
        [NOTIFY_SCRIPT, '-t', '综述追问回复', '-m', message],
        shell=False
    )


def save_followed_task(task_id):
    """记录最近一次成功追问的任务，作为活跃上下文"""
    with open(FOLLOWUP_STATE_FILE, 'w') as f:
        json.dump({'last_followed_task_id': task_id}, f)


def resolve_task(question):
    """
    4层fallback解析任务上下文
    返回: (task, source) 或 (None, None)
    """
    # 第一优先：消息中显式 task_id
    explicit_id = extract_task_id(question)
    if explicit_id:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            for t in json.load(f):
                if t.get('id') == explicit_id and t.get('status') == 'completed':
                    return t, 'explicit'
        print(f'[followup] 显式task_id {explicit_id} 未找到或非completed，跳过')

    # 第二优先：最近一次活跃追踪的任务
    task = find_active_followed_task()
    if task:
        return task, 'active'

    # 第三优先：关键词匹配
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        all_tasks = json.load(f)
    task = match_task_by_keywords(question, all_tasks)
    if task:
        return task, 'keyword'

    # 第四优先：最近一次 completed
    task = find_latest_completed_task()
    if task:
        return task, 'latest'

    return None, None


def main():
    if len(sys.argv) < 2:
        print('用法: python3 scripts/pubmed_followup_handler.py "<用户追问>"')
        sys.exit(1)

    user_question = sys.argv[1]
    print(f'[followup] 收到追问: {user_question}')

    # 1. 检测追问意图
    if not is_followup(user_question):
        print('[followup] 非追问，跳过')
        sys.exit(0)

    # 2. 4层fallback解析任务
    task, source = resolve_task(user_question)
    if not task:
        msg = '暂无可追问的已完成综述，请先发起文献检索（例如：帮我查瘢痕相关文献）。'
        print(f'[followup] {msg}')
        notify_user(msg)
        sys.exit(0)

    task_id = task['id']
    topic = task.get('payload', {}).get('topic', task_id)
    print(f'[followup] 基于任务: {task_id} (topic={topic}) [来源:{source}]')

    # 3. 读取 articles.json
    articles_file = get_articles_file(task_id)
    if not articles_file:
        msg = f'未找到文献数据文件（任务 {task_id}），无法回答追问。'
        print(f'[followup] {msg}')
        notify_user(msg)
        sys.exit(1)

    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # 4. 构建参考文献列表（所有标题）
    ref_list = build_reference_list(articles[:20])

    # 5. 关键词评分选 top3
    scored = score_articles(articles, user_question)
    top3 = [a for _, a in scored[:3]]
    print(f'[followup] Top3: {[a.get("title","")[:40] for a in top3]}')

    # 6. 调用 LLM
    answer = call_llm(user_question, ref_list, top3)

    if not answer:
        msg = '追问回答生成失败，请稍后重试。'
        notify_user(msg)
        sys.exit(1)

    # 7. 记录为活跃追踪任务（下次追问优先使用）
    save_followed_task(task_id)

    # 8. 若非显式task_id，追加提示
    hint = f"\n\n💡 提示：如需精确追问某次综述，请在消息中附上 task_id: {task_id}"
    if source == 'explicit':
        hint = ''

    # 9. 飞书发送
    full_msg = f"📖 综述追问回复\n\n{answer}{hint}"
    notify_user(full_msg)
    print('[followup] 回复已发送')
    print(answer)


if __name__ == '__main__':
    main()
