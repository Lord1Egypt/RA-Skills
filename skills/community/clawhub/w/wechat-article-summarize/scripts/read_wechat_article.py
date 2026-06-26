#!/usr/bin/env python3
import argparse, datetime as dt, html, json, re, sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

UA=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
BLOCK_PATTERNS=[r"环境异常",r"异常访问",r"去验证",r"verifycode",r"操作频繁",r"访问过于频繁",r"请在微信客户端打开"]

def safe_slug(url:str)->str:
    tail=url.rstrip('/').split('/')[-1] or 'wechat_article'
    return (re.sub(r'[^a-zA-Z0-9._-]+','-',tail)[:80] or 'wechat_article')

def fetch(url:str, timeout:int=20):
    req=Request(url, headers={
        'User-Agent':UA,
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control':'no-cache',
        'Pragma':'no-cache',
    })
    with urlopen(req, timeout=timeout) as resp:
        charset=resp.headers.get_content_charset() or 'utf-8'
        return {'status_code':getattr(resp,'status',None),'final_url':resp.geturl(),'text':resp.read().decode(charset,errors='replace')}

def find_first(patterns, text):
    for p in patterns:
        m=re.search(p,text,flags=re.I|re.S)
        if m:
            return m.group(1).strip()
    return None

def detect_block(text:str):
    for p in BLOCK_PATTERNS:
        if re.search(p,text,flags=re.I):
            return p
    return None

def decode_js(s:str)->str:
    return html.unescape(s.encode('utf-8').decode('unicode_escape'))

def html_to_text(fragment:str)->str:
    s=fragment
    s=re.sub(r'<script.*?</script>','',s,flags=re.I|re.S)
    s=re.sub(r'<style.*?</style>','',s,flags=re.I|re.S)
    s=re.sub(r'<br\s*/?>','\n',s,flags=re.I)
    s=re.sub(r'</p\s*>','\n\n',s,flags=re.I)
    s=re.sub(r'</h[1-6]\s*>','\n\n',s,flags=re.I)
    s=re.sub(r'<[^>]+>','',s)
    s=html.unescape(s).replace('\xa0',' ')
    return re.sub(r'\n{3,}','\n\n',s).strip()

def extract_images(fragment:str):
    out=[]
    for m in re.finditer(r'<img[^>]+(?:data-src|src)="([^"]+)"[^>]*', fragment, re.I|re.S):
        u=html.unescape(m.group(1)).replace('&amp;','&')
        if u not in out:
            out.append(u)
    return out

def extract(html_text:str):
    title=find_first([r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']',r'<title>(.*?)</title>',r'var\s+msg_title\s*=\s*["\'](.*?)["\']\s*;',r'title:\s*JsDecode\(\'(.*?)\'\)'], html_text)
    author=find_first([r'var\s+nickname\s*=\s*["\'](.*?)["\']\s*;',r'var\s+user_name\s*=\s*["\'](.*?)["\']\s*;',r'nick_name:\s*JsDecode\(\'(.*?)\'\)'], html_text)
    publish_time=find_first([r'var\s+publish_time\s*=\s*["\']?(\d{10})["\']?\s*;',r'var\s+ct\s*=\s*["\']?(\d{10})["\']?\s*;',r'var\s+ct\s*=\s*"(\d{10})";'], html_text)
    digest=find_first([r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']',r'var\s+msg_desc\s*=\s*["\'](.*?)["\']\s*;',r'desc:\s*JsDecode\(\'(.*?)\'\)'], html_text)
    body_html=find_first([r'content_noencode:\s*JsDecode\(\'(.*?)\'\),', r'<div[^>]+id=["\']js_content["\'][^>]*>(.*?)</div>'], html_text)
    decoded=decode_js(body_html) if body_html else ''
    images=extract_images(decoded)
    body_text=html_to_text(decoded) if decoded else None
    out={
        'title': html.unescape(title) if title else None,
        'author': html.unescape(author) if author else None,
        'publish_time': publish_time,
        'digest': html.unescape(digest) if digest else None,
        'images': images,
        'body_text': body_text,
    }
    if publish_time and publish_time.isdigit():
        out['publish_time_iso']=dt.datetime.utcfromtimestamp(int(publish_time)).isoformat()+'Z'
    return out

def build_article_md(url, meta):
    parts=[f"# {meta.get('title') or 'WeChat Article'}",'',f"- Source URL: {url}"]
    if meta.get('author'): parts.append(f"- Author: {meta['author']}")
    if meta.get('publish_time_iso'): parts.append(f"- Publish time: {meta['publish_time_iso']}")
    if meta.get('images'): parts.append(f"- Images found: {len(meta['images'])}")
    parts.append('')
    if meta.get('digest'):
        parts += ['## Summary','',meta['digest'],'']
    if meta.get('images'):
        parts += ['## Images',''] + [f'- {x}' for x in meta['images']] + ['']
    if meta.get('body_text'):
        parts += ['## Body','',meta['body_text'],'']
    return '\n'.join(parts).strip()+'\n'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--out', default=None)
    args=ap.parse_args()
    url=args.url.strip()
    if 'mp.weixin.qq.com' not in url:
        print('URL must point to mp.weixin.qq.com', file=sys.stderr); return 2
    out_dir=Path(args.out or (Path.cwd()/f'wechat-output-{safe_slug(url)}'))
    out_dir.mkdir(parents=True, exist_ok=True)
    result={'url':url,'status':'blocked','reason':None,'direct':{},'meta':{},'files':{}}
    try:
        resp=fetch(url)
        html_text=resp['text']
        (out_dir/'raw.html').write_text(html_text, encoding='utf-8')
        result['direct']={'status_code':resp['status_code'],'final_url':resp['final_url']}
        result['files']['raw_html']=str(out_dir/'raw.html')
        meta=extract(html_text)
        result['meta']= {k:v for k,v in meta.items() if k!='body_text'}
        if meta.get('title') and (meta.get('body_text') or ''):
            result['status']='ok'; result['reason']='direct_fetch'
            (out_dir/'article.md').write_text(build_article_md(url, meta), encoding='utf-8')
            result['files']['article_md']=str(out_dir/'article.md')
        else:
            result['status']='blocked' if detect_block(html_text) else 'partial'
            result['reason']=detect_block(html_text) or 'direct_fetch_incomplete'
    except Exception as e:
        result['reason']='direct_fetch_error'; result['direct']['error']=str(e)
    (out_dir/'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    result['files']['result_json']=str(out_dir/'result.json')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
