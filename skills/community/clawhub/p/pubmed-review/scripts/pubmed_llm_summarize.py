#!/usr/bin/env python3
"""
PubMed 文献综述生成器
用法: python3 scripts/pubmed_llm_summarize.py <articles_json> <output_md>
"""
import sys
import os
import json
import time

# LLM 配置
LLM_API_URL = os.environ.get('MINIMAX_API_URL', '')
LLM_API_KEY = os.environ.get('MINIMAX_API_KEY', '')
LLM_MODEL = os.environ.get('MINIMAX_MODEL', 'MiniMax-M2.7-highspeed')

MAX_ABSTRACT_LEN = 800  # 每篇摘要最多截取字符数


def build_prompt(articles, topic):
    """构建 LLM prompt"""
    article_blocks = []
    for i, art in enumerate(articles, 1):
        title = art.get('title', '') or ''
        abstract = art.get('abstract', '') or ''
        authors = art.get('authors', [])
        year = art.get('year', '')
        doi = art.get('doi', '')
        pmid = art.get('pmid', '')

        if len(abstract) > MAX_ABSTRACT_LEN:
            abstract = abstract[:MAX_ABSTRACT_LEN] + '...'

        author_str = ', '.join(authors[:3])
        if len(authors) > 3:
            author_str += ' et al.'

        ref = f"[{i}]"
        if pmid:
            ref += f" PMID:{pmid}"
        if doi:
            ref += f" DOI:{doi}"
        if year:
            ref += f" ({year})"

        article_blocks.append(f"### {ref} {title}\n**Authors:** {author_str}\n**Abstract:** {abstract}")

    articles_text = '\n\n'.join(article_blocks)

    prompt = f"""你是医学文献综述专家。请根据以下 PubMed 文献，撰写关于「{topic}」的结构化综述。

请严格按以下JSON格式输出，不要输出任何其他内容：
{{
  "brief": "精简摘要，使用要点列表，控制总长在200字以内，格式：
  · 核心结论（1句，不超过30字）
  · 主要机制（2-3个要点，每个不超过20字）
  · 临床提示（1句，不超过30字）",
  "full": "完整综述，Markdown格式，包含：\n## 一、研究背景\n## 二、作用机制\n## 三、临床应用\n## 四、疗效与安全性\n## 五、争议与不足\n## 六、未来研究方向\n## 七、参考文献（Title/Authors/Year/DOI）"
}}

文献列表：
{articles_text}

请开始撰写："""
    return prompt


def call_llm(prompt):
    """调用 LLM API 生成综述"""
    if not LLM_API_KEY:
        return generate_fallback_summary(prompt)

    try:
        import urllib.request
        import urllib.parse

        payload = {
            'model': LLM_MODEL,
            'messages': [
                {'role': 'system', 'content': '你是一位专业的医学文献综述专家，擅长归纳和总结医学研究文献。'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 2048,
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

        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            msg = result['choices'][0]['message']
            content = msg.get('content', '') or msg.get('reasoning_content', '')
            if not content:
                print(f'[pubmed_llm] ERROR: LLM 返回内容为空，finish_reason={result["choices"][0].get("finish_reason")}', file=sys.stderr)
                return None
            # 尝试解析 JSON
            try:
                return json.loads(content.strip())
            except json.JSONDecodeError:
                # 可能content中含真实换行符（而非\n转义），先替换为\n再解析
                try:
                    normalized = content.replace('\n', '\\n').replace('\r', '\\r')
                    return json.loads(normalized.strip())
                except Exception:
                    pass
                # fallback：提取 {..} JSON块并同样规范化
                import re
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    try:
                        block = match.group().replace('\n', '\\n').replace('\r', '\\r')
                        return json.loads(block.strip())
                    except:
                        pass
                return {'brief': content[:300], 'full': content}
    except Exception as e:
        print(f'[pubmed_llm] LLM API 调用失败: {e}', file=sys.stderr)
        return None


def generate_fallback_summary(prompt):
    """无 API key 时的降级：输出结构化摘要（不做 LLM 生成）"""
    print('[pubmed_llm] WARNING: 未配置 LLM API_KEY，使用降级模式', file=sys.stderr)
    return """[降级模式] 未配置 LLM API，无法生成 AI 综述。

请设置环境变量:
  export MINIMAX_API_URL="https://api.minimax.chat/v1/text/chatcompletion_v2"
  export MINIMAX_API_KEY="your_api_key"
  export MINIMAX_MODEL="MiniMax-M2.7-highspeed"

articles.json 中已包含所有摘要数据，可手动导入 Zotero 或其他工具进行综述。
"""


def main():
    if len(sys.argv) < 3:
        print('用法: python3 scripts/pubmed_llm_summarize.py <articles_json> <output_md>')
        sys.exit(1)

    articles_json = sys.argv[1]
    output_md = sys.argv[2]

    if not os.path.exists(articles_json):
        print(f'[pubmed_llm] ERROR: articles.json 不存在: {articles_json}', file=sys.stderr)
        sys.exit(1)

    # 读取文献
    with open(articles_json, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    if not articles:
        print('[pubmed_llm] ERROR: articles.json 为空', file=sys.stderr)
        sys.exit(1)

    # 从文件名提取 topic（格式: {task_id}_articles.json）
    task_id = os.path.basename(articles_json).replace('_articles.json', '')
    topic = task_id  # 降级用

    # 尝试从 tasks 文件读取 topic
    try:
        tasks_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tasks', 'ablesci_tasks.json')
        with open(tasks_file, 'r') as f:
            for t in json.load(f):
                if t.get('id') == task_id:
                    topic = t.get('payload', {}).get('topic', topic)
                    break
    except:
        pass

    print(f'[pubmed_llm] 生成综述: topic={topic}, articles={len(articles)}')

    # 构建 prompt
    prompt = build_prompt(articles, topic)

    # 调用 LLM
    result = call_llm(prompt)

    os.makedirs(os.path.dirname(output_md), exist_ok=True)

    if isinstance(result, dict) and 'full' in result:
        # 写入完整综述到文件
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(f'# 文献综述：{topic}\n\n')
            f.write(f'> 基于 {len(articles)} 篇 PubMed 文献自动生成\n\n')
            # result['full'] 可能是含真实换行的 Python str，直接写入
            f.write(result['full'])
        brief = result.get('brief', '')
        # brief 中可能含字面 \\n（两个字符），替换为真实换行
        brief = brief.replace('\\n', '\n')
        print(f'[pubmed_llm] 已写入完整综述: {output_md}')
        # stdout 输出 brief，供 shell 脚本捕获用于飞书通知
        print(brief)
    else:
        # 降级或旧格式
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(f'# 文献综述：{topic}\n\n')
            f.write(f'> 基于 {len(articles)} 篇 PubMed 文献自动生成\n\n')
            if result:
                f.write(str(result))
            else:
                f.write('\n'.join(f"- {a.get('title','')[:80]}" for a in articles[:10]))
        print(f'[pubmed_llm] 已写入（降级模式）: {output_md}')

    sys.exit(0)


if __name__ == '__main__':
    main()
