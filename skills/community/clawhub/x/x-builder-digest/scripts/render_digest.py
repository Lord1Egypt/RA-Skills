#!/usr/bin/env python3
import json
import html
import sys
from pathlib import Path

PEOPLE = {
    'Swyx': {'en': 'AI engineering writer and Latent Space co-host', 'zh': 'AI 工程作者，Latent Space 联合主持人'},
    'Kevin Weil': {'en': 'OpenAI VP of Science, focused on AI products and research tooling', 'zh': 'OpenAI 科学副总裁，偏 AI 产品和科研工具'},
    'Peter Yang': {'en': 'Product leader and AI educator known for practical tutorials', 'zh': '产品负责人，擅长输出实操型 AI 教程'},
}

ZH_OVERRIDES = {
    'Swyx': ['他在转发讨论时强调了 AI 安全术语命名和问题定义的重要差异。'],
    'Kevin Weil': ['他强调基于 AI 编码能力快速做出新功能，体现了 AI-native 产品的迭代速度。'],
    'Peter Yang': ['他在关注模型发布之外，更在追问这些能力是否真正进入了团队内部生产流程。'],
}

def clean(s):
    s = html.unescape((s or '').replace('\n', ' ').strip())
    return ' '.join(s.split())

def short(s, n=160):
    s = clean(s)
    return s if len(s) <= n else s[:n-3] + '...'

def person_blurb(name, lang):
    return PEOPLE.get(name, {}).get(lang, '')

def build_en(data):
    stats = data.get('stats', {})
    xs = data.get('x', [])
    podcasts = data.get('podcasts', [])
    blogs = data.get('blogs', [])
    lines = ['# Builder Digest (English)', '', '## Top takeaways']
    if xs:
        lines.append('- Focus names today: ' + ', '.join(clean(a.get('name') or a.get('handle') or 'unknown') for a in xs[:5]))
    lines.append(f"- Coverage: X builders {stats.get('xBuilders',0)}, tweets {stats.get('totalTweets',0)}, podcasts {stats.get('podcastEpisodes',0)}, blogs {stats.get('blogPosts',0)}")
    lines.append('')
    lines.append('## X / Builders')
    for author in xs[:8]:
        name = clean(author.get('name') or author.get('handle') or 'unknown')
        tweets = author.get('tweets', [])[:2]
        if not tweets:
            continue
        blurb = person_blurb(name, 'en')
        lines.append(f"- **{name}**{f' ({blurb})' if blurb else ''}")
        for t in tweets:
            text = short(t.get('text') or '')
            url = t.get('url') or ''
            lines.append(f'  - {text}')
            if url:
                lines.append(f'    - {url}')
    if podcasts:
        lines.extend(['', '## Podcasts'])
        for ep in podcasts[:3]:
            lines.append(f"- **{clean(ep.get('creator') or ep.get('podcast') or 'Podcast')}**: {clean(ep.get('title') or '')}")
            if ep.get('url'):
                lines.append(f"  - {ep.get('url')}")
    if blogs:
        lines.extend(['', '## Blogs'])
        for b in blogs[:3]:
            lines.append(f"- **{clean(b.get('source') or b.get('name') or 'Blog')}**: {clean(b.get('title') or '')}")
            if b.get('url'):
                lines.append(f"  - {b.get('url')}")
    return '\n'.join(lines) + '\n'

def build_zh(data):
    stats = data.get('stats', {})
    xs = data.get('x', [])
    podcasts = data.get('podcasts', [])
    blogs = data.get('blogs', [])
    lines = ['# Builder Digest（中文版）', '', '## 核心结论']
    if xs:
        lines.append('- 今日重点人物：' + '、'.join(clean(a.get('name') or a.get('handle') or 'unknown') for a in xs[:5]) + '。')
    lines.append(f"- 覆盖范围：{stats.get('xBuilders',0)} 个 X builders，{stats.get('totalTweets',0)} 条 tweets，{stats.get('podcastEpisodes',0)} 条 podcast，{stats.get('blogPosts',0)} 条 blog。")
    lines.append('')
    lines.append('## X / Builders')
    for author in xs[:8]:
        name = clean(author.get('name') or author.get('handle') or 'unknown')
        tweets = author.get('tweets', [])[:2]
        if not tweets:
            continue
        blurb = person_blurb(name, 'zh')
        lines.append(f"- **{name}**{f'（{blurb}）' if blurb else ''}")
        overrides = ZH_OVERRIDES.get(name, [])
        for idx, t in enumerate(tweets):
            summary = overrides[idx] if idx < len(overrides) else '这条内容值得进一步查看原文。'
            lines.append(f'  - {summary}')
            if t.get('url'):
                lines.append(f"    - 原文：{t.get('url')}")
    if podcasts:
        lines.extend(['', '## 播客'])
        for ep in podcasts[:3]:
            lines.append(f"- **{clean(ep.get('creator') or ep.get('podcast') or '播客')}**：{clean(ep.get('title') or '')}")
            if ep.get('url'):
                lines.append(f"  - 链接：{ep.get('url')}")
    if blogs:
        lines.extend(['', '## 博客'])
        for b in blogs[:3]:
            lines.append(f"- **{clean(b.get('source') or b.get('name') or '博客')}**：{clean(b.get('title') or '')}")
            if b.get('url'):
                lines.append(f"  - 链接：{b.get('url')}")
    return '\n'.join(lines) + '\n'

def main():
    if len(sys.argv) != 3:
        print('Usage: python3 scripts/render_digest.py input.json output_dir')
        sys.exit(1)
    input_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(input_path.read_text())
    (output_dir / 'digest-en.md').write_text(build_en(data))
    (output_dir / 'digest-zh.md').write_text(build_zh(data))
    print(output_dir / 'digest-en.md')
    print(output_dir / 'digest-zh.md')

if __name__ == '__main__':
    main()
