#!/usr/bin/env python3
"""
PubMed 文献综述 Handler
用法: python3 scripts/run_pubmed_review.py <task_id>
"""
import sys
import os
import json
import time
import subprocess
import urllib.request
import urllib.parse
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # scripts/ 的父目录即项目根目录
TASKS_FILE = os.path.join(BASE_DIR, 'tasks', 'ablesci_tasks.json')
RESULTS_DIR = os.path.join(BASE_DIR, 'results', 'pubmed')
os.makedirs(RESULTS_DIR, exist_ok=True)

NOTIFY_SCRIPT = os.environ.get('NOTIFY_PATH', '/usr/local/bin/notify' if os.path.exists('/usr/local/bin/notify') else 'notify')
ESearch_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
EFetch_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'


def log(msg):
    print(f'[run_pubmed_review] {msg}')


def load_tasks():
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def get_task(tasks, task_id):
    for t in tasks:
        if t['id'] == task_id:
            return t
    return None


def update_task_status(task_id, status, fetched_count=None, error=None, enabled=None):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['status'] = status
            if fetched_count is not None:
                t['fetched_count'] = fetched_count
            if error is not None:
                t['error'] = error
            if enabled is not None:
                t['enabled'] = enabled
            break
    save_tasks(tasks)


def fetch_json(url, params):
    """带重试的 HTTP GET"""
    query = urllib.parse.urlencode(params)
    full_url = f'{url}?{query}'
    for attempt in range(3):
        try:
            req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode('utf-8')
        except Exception as e:
            log(f'请求失败 (尝试 {attempt+1}/3): {e}')
            if attempt < 2:
                time.sleep(3)
    return None


def search_pubmed(topic, max_articles=20):
    """esearch: 获取 article IDs"""
    params = {
        'db': 'pubmed',
        'term': topic,
        'retmax': max_articles,
        'retmode': 'json',
        'usehistory': 'n',
        'sort': 'relevance'
    }
    log(f'检索主题: {topic}')
    response = fetch_json(ESearch_URL, params)
    if not response:
        return None
    try:
        import json as json_mod
        data = json_mod.loads(response)
        ids = data.get('esearchresult', {}).get('idlist', [])
        log(f'找到 {len(ids)} 篇文献')
        return ids
    except Exception as e:
        log(f'解析检索结果失败: {e}')
        return None


def fetch_abstracts(pmids):
    """efetch: 批量获取摘要"""
    if not pmids:
        return []
    id_str = ','.join(pmids)
    params = {
        'db': 'pubmed',
        'id': id_str,
        'rettype': 'abstract',
        'retmode': 'xml'
    }
    log(f'获取 {len(pmids)} 篇摘要...')
    response = fetch_json(EFetch_URL, params)
    if not response:
        return []
    return parse_abstracts_xml(response)


def parse_abstracts_xml(xml_text):
    """解析 PubMed XML 摘要"""
    articles = []
    import re
    # 分割每篇文章
    article_blocks = re.split(r'<PubmedArticle>', xml_text)[1:]
    for block in article_blocks:
        pmid_match = re.search(r'<PMID[^>]*>(\d+)</PMID>', block)
        pmid = pmid_match.group(1) if pmid_match else ''
        title_match = re.search(r'<ArticleTitle>(.*?)</ArticleTitle>', block, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ''
        # 处理多个 AbstractText 节点
        abstract_parts = re.findall(r'<AbstractText[^>]*>(.*?)</AbstractText>', block, re.DOTALL)
        abstract = ' '.join(a.strip() for a in abstract_parts if a.strip())
        # 作者
        author_matches = re.findall(r'<Author[^>]*><LastName>([^<]+)</LastName>.*?<ForeName>([^<]+)</ForeName>', block)
        authors = [f'{last} {first}' for last, first in author_matches] if author_matches else []
        # 年份
        year_match = re.search(r'<PubDate>.*?<Year>(\d{4})</Year>', block)
        year = year_match.group(1) if year_match else ''
        # DOI
        doi_match = re.search(r'<ArticleId IdType="doi">([^<]+)</ArticleId>', block)
        doi = doi_match.group(1) if doi_match else ''
        if title or abstract:
            articles.append({
                'pmid': pmid,
                'title': title,
                'abstract': abstract,
                'authors': authors[:5],  # 只保留前5个作者
                'year': year,
                'doi': doi
            })
        time.sleep(0.4)  # NCBI 要求 ≤ 3 req/s
    return articles


def main():
    if len(sys.argv) < 2:
        print('用法: python3 scripts/run_pubmed_review.py <task_id>')
        sys.exit(1)

    task_id = sys.argv[1]
    tasks = load_tasks()
    task = get_task(tasks, task_id)

    if not task:
        log(f'任务未找到: {task_id}')
        sys.exit(1)

    topic = task['payload']['topic']
    max_articles = task['payload'].get('max_articles', 20)

    # 更新状态为 running
    update_task_status(task_id, 'running')
    log(f'开始处理任务: {task_id}')

    # 1. esearch
    pmids = search_pubmed(topic, max_articles)
    if pmids is None:
        log('esearch 失败')
        update_task_status(task_id, 'failed', error='esearch API 失败')
        sys.exit(1)

    if not pmids:
        log('未找到任何文献')
        update_task_status(task_id, 'failed', fetched_count=0, error='未找到相关文献')
        sys.exit(1)

    # 2. efetch
    articles = fetch_abstracts(pmids)
    if not articles:
        log('efetch 获取摘要失败')
        update_task_status(task_id, 'failed', fetched_count=0, error='efetch API 失败')
        sys.exit(1)

    # 3. 写入 articles.json
    articles_file = os.path.join(RESULTS_DIR, f'{task_id}_articles.json')
    with open(articles_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    log(f'已写入 {len(articles)} 篇摘要: {articles_file}')

    # 4. 更新 fetched_count
    update_task_status(task_id, 'running', fetched_count=len(articles))

    # 5. 同步调用 processor
    log('调用 pubmed_summary processor...')
    proc_result = subprocess.run(
        ['bash', f'{SCRIPT_DIR}/run_processor.sh', 'pubmed_summary', articles_file, task_id],
        check=False
    )
    proc_exit = proc_result.returncode

    # 6. 根据退出码写最终状态
    if proc_exit == 0:
        log(f'processor 成功，任务完成: {task_id}')
        update_task_status(task_id, 'completed', enabled=False)
    else:
        log(f'processor 失败，退出码: {proc_exit}')
        update_task_status(task_id, 'failed', error=f'processor 失败，退出码 {proc_exit}')

    sys.exit(0)


if __name__ == '__main__':
    main()
