#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
from datetime import datetime

def safe_name(name:str)->str:
    return re.sub(r'[\\/:*?"<>|]+','-',name).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--result', required=True)
    ap.add_argument('--body', required=True)
    ap.add_argument('--summary', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--include-images', default='true')
    args=ap.parse_args()
    result=json.loads(Path(args.result).read_text())
    body=Path(args.body).read_text(encoding='utf-8', errors='replace')
    summary=json.loads(Path(args.summary).read_text()).get('summary','').strip()
    meta=result.get('meta',{})
    title=meta.get('title') or '微信文章'
    date=(meta.get('publish_time_iso') or datetime.utcnow().isoformat()).replace('-','')[:8]
    include_images=args.include_images.lower()=='true'
    parts=[f'# {title}','',f'- 原文链接: {result.get("url")}',f'- 提取状态: {result.get("status")}',f'- summarize 状态: ok','', '---','', '## summarize skill 全文总结','', summary,'', '---','', '# 思维导图','', f'- {title}', '  - 核心主题', '    - 基于全文摘要继续细化', '  - 正文要点', '    - 建议后续由 agent按文章内容补全层级', '', '---','', '# 正文','', body[:12000],'']
    if include_images and meta.get('images'):
        parts += ['---','','# 图片提取结果',''] + [f'- {x}' for x in meta['images']] + ['']
    out_dir=Path(args.output_dir).expanduser(); out_dir.mkdir(parents=True, exist_ok=True)
    out=out_dir / f'{date}-{safe_name(title)}.md'
    out.write_text('\n'.join(parts), encoding='utf-8')
    print(out)

if __name__=='__main__':
    main()
