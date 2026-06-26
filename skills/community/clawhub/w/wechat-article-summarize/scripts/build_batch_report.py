#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
from datetime import datetime

def safe_name(name:str)->str:
    return re.sub(r'[\\/:*?"<>|]+','-',name).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs', nargs='+', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--include-images', default='true')
    ap.add_argument('--report-label', default='微信文章日报')
    ap.add_argument('--combined-summary', required=True)
    args=ap.parse_args()
    include_images=args.include_images.lower()=='true'
    articles=[]
    for d in args.inputs:
        p=Path(d)
        result=json.loads((p/'result.json').read_text())
        body=(p/'body-fixed.txt').read_text(encoding='utf-8', errors='replace') if (p/'body-fixed.txt').exists() else ''
        summary=json.loads((p/'summary.json').read_text()).get('summary','').strip() if (p/'summary.json').exists() else ''
        articles.append((result,body,summary))
    combined=json.loads(Path(args.combined_summary).read_text()).get('summary','').strip()
    first_date=(articles[0][0].get('meta',{}).get('publish_time_iso') or datetime.utcnow().isoformat()).replace('-','')[:8]
    parts=[f'# {first_date} {args.report_label}（{len(articles)}篇）','',f'- 汇总日期：{first_date}',f'- 文章数量：{len(articles)}',f'- 汇总说明：{args.report_label}','', '---','', '## 今日总览','', combined,'', '---','', '# 单篇整理','']
    total_images=0
    for i,(result,body,summary) in enumerate(articles,1):
        meta=result.get('meta',{})
        parts += [f'## {i}. {meta.get("title") or "微信文章"}','',f'- 原文链接：{result.get("url")}',f'- 发布时间：{meta.get("publish_time_iso") or meta.get("publish_time") or ""}']
        if include_images:
            parts.append(f'- 图片数量：{len(meta.get("images",[]))}')
            total_images += len(meta.get('images',[]))
        parts += ['', '### 单篇摘要','', summary,'', '### 思维导图','', f'- {meta.get("title") or "微信文章"}', '  - 核心观点', '    - 基于单篇摘要展开', '', '---','']
    if include_images:
        parts += ['# 图片提取概览','', f'- 合计图片数：{total_images}','']
    out_dir=Path(args.output_dir).expanduser(); out_dir.mkdir(parents=True, exist_ok=True)
    out=out_dir / f'{first_date}-{len(articles)}篇-{safe_name(args.report_label)}.md'
    out.write_text('\n'.join(parts), encoding='utf-8')
    print(out)

if __name__=='__main__':
    main()
