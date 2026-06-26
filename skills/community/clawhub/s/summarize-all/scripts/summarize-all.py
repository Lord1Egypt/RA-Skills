#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              ✨ Summarize All Pro ✨                       ║
║         Advanced AI Smart Summarizer v2.5                  ║
╚══════════════════════════════════════════════════════════════╝

Features: Streaming | Markdown | Search | Batch | Notifications
         Compare | Keywords | Tags | PDF Merge | Academic Mode
"""
import sys
import os
import json
import pathlib
import re
import urllib.request
import subprocess
import base64
import hashlib
import threading
import http.server
import socketserver
import time
import textwrap
import signal
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import defaultdict

# ═══════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════
CONFIG_DIR = pathlib.Path.home() / ".config" / "summarize-all"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
CACHE_FILE = CONFIG_DIR / "cache.json"
TAGS_FILE = CONFIG_DIR / "tags.json"
KEYWORDS_FILE = CONFIG_DIR / "keywords.json"

# ═══════════════════════════════════════════════════════════
# Colors & Streaming
# ═══════════════════════════════════════════════════════════
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

class Streamer:
    """Streaming text output with typewriter effect"""
    def __init__(self, delay=0.01):
        self.delay = delay
    
    def print(self, text, end='\n', flush=False):
        """Stream text character by character"""
        for char in text:
            print(char, end='', flush=True)
            if char not in ' \n' and random.random() < 0.05:
                time.sleep(self.delay)
        print(end, flush=flush)
    
    def stream(self, text):
        """Stream full text"""
        print(text, flush=True)

import random

def print_banner():
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║{Colors.BLUE}              ✨ Summarize All Pro ✨                     {Colors.CYAN}║
║{Colors.DIM}         Advanced AI Smart Summarizer v2.5              {Colors.CYAN}║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}""")

def print_step(step, msg, color=Colors.BLUE):
    symbols = {
        "fetch": "📥", "analyze": "🧠", "score": "📊", "improve": "🔄",
        "done": "✅", "error": "❌", "cache": "📦", "think": "💭",
        "translate": "🌐", "compare": "⚖️", "graph": "🔗", "report": "📋",
        "stream": "📝", "search": "🔍", "batch": "📚", "notify": "🔔",
        "tag": "🏷️", "merge": "📑", "academic": "🎓", "keyword": "🔎"
    }
    sym = symbols.get(step, "•")
    print(f"  {color}{sym} {msg}{Colors.RESET}")

def print_markdown(text):
    """Pretty print markdown with basic formatting"""
    lines = text.split('\n')
    in_code = False
    
    for line in lines:
        # Headers
        if line.startswith('# '):
            print(f"{Colors.BOLD}{Colors.CYAN}{line}{Colors.RESET}")
        elif line.startswith('## '):
            print(f"{Colors.BOLD}{Colors.BLUE}{line}{Colors.RESET}")
        elif line.startswith('### '):
            print(f"{Colors.BOLD}{line}{Colors.RESET}")
        # Code blocks
        elif line.strip().startswith('```'):
            in_code = not in_code
            print(f"{Colors.DIM}{'─' * 50}{Colors.RESET}" if in_code else "")
        # Bold
        elif in_code:
            print(f"{Colors.YELLOW}{line}{Colors.RESET}")
        # Lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            print(f"  {Colors.GREEN}•{Colors.RESET} {line[2:]}")
        # Tables (simple)
        elif '|' in line and not line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            print('  '.join(parts))
        # Empty line
        elif line.strip() == '':
            print()
        # Normal text
        else:
            # Format bold parts
            line = re.sub(r'\*\*([^*]+)\*\*', f'{Colors.BOLD}\\1{Colors.RESET}', line)
            print(line)

# ═══════════════════════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════════════════════
def load_json(path):
    return json.load(open(path)) if path.exists() else {}

def save_json(path, data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(path, 'w'), indent=2)

def load_config():
    return load_json(CONFIG_FILE)

def save_config(cfg):
    save_json(CONFIG_FILE, cfg)

def load_history():
    data = load_json(HISTORY_FILE)
    return data if isinstance(data, list) else []

def save_history(hist):
    save_json(HISTORY_FILE, hist[-100:])

def load_cache():
    return load_json(CACHE_FILE)

def save_cache(cache):
    now = datetime.now()
    cleaned = {k: v for k, v in cache.items() 
               if datetime.fromisoformat(v['time']) > now - timedelta(hours=24)}
    save_json(CACHE_FILE, cleaned)

def load_tags():
    return load_json(TAGS_FILE)

def save_tags(tags):
    save_json(TAGS_FILE, tags)

def load_keywords():
    return load_json(KEYWORDS_FILE)

def save_keywords(kw):
    save_json(KEYWORDS_FILE, kw)

def get_cache_key(url, length):
    return hashlib.md5(f"{url}:{length}".encode()).hexdigest()

# ═══════════════════════════════════════════════════════════
# Notifications
# ═══════════════════════════════════════════════════════════
def send_notification(title, message):
    """Send desktop notification"""
    try:
        subprocess.Popen(['notify-send', title, message])
    except:
        pass

# ═══════════════════════════════════════════════════════════
# Content Detection
# ═══════════════════════════════════════════════════════════
def detect_content_type(content, url):
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'video', "🎬 Video"
    if any(ext in url.lower() for ext in ['.pdf']):
        return 'document', "📄 Document"
    if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
        return 'image', "🖼️ Image"
    if any(ext in url.lower() for ext in ['.mp3', '.wav', '.mp4', '.m4a', '.ogg']):
        return 'audio', "🎵 Audio"
    
    cl = content.lower()
    indicators = [
        (['abstract', 'methodology', 'references', 'doi:', 'arxiv', 'paper', 'journal'], 'academic', "🎓 Academic"),
        (['product', 'price', 'buy', 'cart', 'specifications'], 'ecommerce', "🛒 Product"),
        (['news', 'breaking', 'report', 'says', 'according to'], 'news', "📰 News"),
        (['github', 'repository', 'commit', 'pull request'], 'code', "💻 Code"),
        (['recipe', 'ingredients', 'instructions', 'cook', 'servings'], 'recipe', "🍳 Recipe"),
        (['tutorial', 'step', 'guide', 'how to'], 'tutorial', "📖 Tutorial"),
        (['review', 'rating', 'pros', 'cons', 'verdict'], 'review', "⭐ Review"),
    ]
    
    for keywords, type_id, label in indicators:
        if sum(1 for kw in keywords if kw in cl) >= 2:
            return type_id, label
    
    return 'article', "📝 Article"

def auto_length(content):
    l = len(content)
    if l < 500: return 'short', "Brief"
    elif l < 2000: return 'medium', "Standard"
    elif l < 5000: return 'long', "Detailed"
    elif l < 10000: return 'xl', "Comprehensive"
    return 'xxl', "Complete"

def detect_language(content):
    if re.search(r'[\u4e00-\u9fff]', content): return 'zh'
    if re.search(r'[\u3040-\u30ff]', content): return 'ja'
    if re.search(r'[\uac00-\ud7af]', content): return 'ko'
    return 'en'

# ═══════════════════════════════════════════════════════════
# API Call
# ═══════════════════════════════════════════════════════════
def call_api(prompt, model=None, temperature=0.7, timeout=90, stream=False):
    cfg = load_config()
    if not cfg.get('endpoint') or not cfg.get('key'):
        return None, "API not configured"
    
    endpoint = cfg['endpoint']
    api_key = cfg['key']
    model = model or cfg.get('model', 'gpt-4o-mini')
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    
    req = urllib.request.Request(
        endpoint.rstrip('/') + "/chat/completions",
        data=json.dumps(data).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
        method='POST'
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        result = json.loads(resp.read())
        if 'choices' in result:
            return result['choices'][0]['message']['content'], None
        return None, str(result)
    except Exception as e:
        return None, str(e)

# ═══════════════════════════════════════════════════════════
# Auto Tagging
# ═══════════════════════════════════════════════════════════
def extract_tags(content, summary):
    """Extract tags from content and summary"""
    prompt = f"""Extract 5-8 relevant tags for this content. Return ONLY a JSON array of tags (e.g., ["tag1", "tag2"]).

Content preview: {content[:500]}

Summary: {summary[:300]}"""
    
    result, error = call_api(prompt, temperature=0.3)
    if error:
        return []
    
    try:
        # Extract JSON array from response
        match = re.search(r'\[.*\]', result, re.DOTALL)
        if match:
            tags = json.loads(match.group())
            # Save to tags file
            tags_data = load_tags()
            for tag in tags:
                if tag not in tags_data:
                    tags_data[tag] = 0
                tags_data[tag] += 1
            save_tags(tags_data)
            return tags
    except:
        pass
    
    return []

def search_by_tag(tag):
    """Search history by tag"""
    history = load_history()
    results = []
    for item in history:
        if tag.lower() in [t.lower() for t in item.get('tags', [])]:
            results.append(item)
    return results

# ═══════════════════════════════════════════════════════════
# Keyword Tracking
# ═══════════════════════════════════════════════════════════
def add_keyword(keyword, alert):
    """Add keyword to track"""
    kw_data = load_keywords()
    kw_data[keyword] = {"alert": alert, "added": datetime.now().isoformat()}
    save_keywords(kw_data)
    print_step("keyword", f"Tracking: '{keyword}' → {alert}")

def remove_keyword(keyword):
    kw_data = load_keywords()
    if keyword in kw_data:
        del kw_data[keyword]
        save_keywords(kw_data)
        print_step("done", f"Removed: '{keyword}'")

def check_keywords(content, url):
    """Check if content contains tracked keywords"""
    kw_data = load_keywords()
    found = []
    for keyword, info in kw_data.items():
        if keyword.lower() in content.lower():
            found.append((keyword, info['alert']))
            send_notification(f"🔎 Keyword Alert: {keyword}", f"{url}\n{info['alert']}")
    return found

def list_keywords():
    kw_data = load_keywords()
    if not kw_data:
        print(f"{Colors.DIM}No keywords tracked{Colors.RESET}")
        return
    print(f"{Colors.CYAN}🔎 Tracked Keywords:{Colors.RESET}")
    for kw, info in kw_data.items():
        print(f"  • {kw} → {info['alert']}")

# ═══════════════════════════════════════════════════════════
# History Search
# ═══════════════════════════════════════════════════════════
def search_history(query):
    """Search history by query"""
    history = load_history()
    results = []
    query_lower = query.lower()
    
    for item in history:
        if (query_lower in item.get('source', '').lower() or
            query_lower in item.get('summary', '').lower() or
            query_lower in ' '.join(item.get('tags', [])).lower() or
            query_lower in item.get('type', '').lower()):
            results.append(item)
    
    return results

# ═══════════════════════════════════════════════════════════
# PDF Merge & Summarize
# ═══════════════════════════════════════════════════════════
def merge_pdfs(pdf_paths, output_path):
    """Merge multiple PDFs into one"""
    try:
        result = subprocess.run(
            ['pdftk'] + pdf_paths + ['cat', 'output', output_path],
            capture_output=True, timeout=60
        )
        if result.returncode == 0:
            return output_path
    except:
        pass
    
    # Alternative: use Python library
    try:
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        for pdf in pdf_paths:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        return output_path
    except:
        return None

def summarize_pdfs(pdf_paths, length='auto'):
    """Summarize multiple PDFs together"""
    print_step("merge", f"Merging {len(pdf_paths)} PDFs...")
    merged_path = f"/tmp/merged_{int(time.time())}.pdf"
    
    # Extract text from all PDFs
    all_content = []
    for pdf in pdf_paths:
        content = get_content(pdf)
        if len(content) > 20:
            all_content.append(f"--- Document: {pdf} ---\n{content[:3000]}")
    
    combined = "\n\n".join(all_content)
    
    if len(combined) < 50:
        print_step("error", "Could not extract text from PDFs")
        return None, None, 0
    
    # Detect type and summarize
    ctype, type_label = detect_content_type(combined, "merged://")
    if length == 'auto':
        length, _ = auto_length(combined)
    
    print_step("done", f"Combined: {len(combined)} chars from {len(pdf_paths)} files")
    
    # Build prompt
    prompt = build_prompt(combined, length, ctype, detect_language(combined))
    summary, error = call_api(prompt)
    
    if error:
        return None, ctype, 0
    
    # Extract tags
    tags = extract_tags(combined, summary)
    
    # Check keywords
    found_kw = check_keywords(combined, f"merged://{len(pdf_paths)}_files")
    
    # Clean up
    try:
        os.remove(merged_path)
    except:
        pass
    
    return summary, ctype, tags, found_kw

# ═══════════════════════════════════════════════════════════
# Academic Paper Mode
# ═══════════════════════════════════════════════════════════
def academic_summary(content):
    """Specialized academic paper summarization"""
    prompt = f"""## Task: Academic Paper Analysis

Analyze this academic paper and provide:

1. **Research Question** - What problem does this paper address?

2. **Methodology** - What methods were used?

3. **Key Findings** - What are the main results?

4. **Limitations** - What are the weaknesses?

5. **Significance** - Why does this matter?

6. **Related Work** - How does it compare to similar research?

7. **Future Directions** - What questions remain?

Format with clear headers. Be precise and academic.

Content ({len(content)} chars):
{content[:12000]}"""
    
    return call_api(prompt, temperature=0.5)

# ═══════════════════════════════════════════════════════════
# Article Comparison
# ═══════════════════════════════════════════════════════════
def compare_articles(urls):
    """Compare multiple articles on similar topics"""
    contents = []
    for url in urls:
        c = get_content(url)
        if len(c) > 50:
            ct, _ = detect_content_type(c, url)
            contents.append({"url": url, "content": c[:5000], "type": ct})
    
    if len(contents) < 2:
        print_step("error", "Need at least 2 valid articles")
        return
    
    prompt = f"""## Task: Multi-Article Comparison

Compare these {len(contents)} articles. Identify:
1. Common themes/topic
2. Different perspectives/angles
3. Contradictions (if any)
4. Complementary information
5. Which is most credible/reliable

Format:
## Overview
[1-2 sentences on the overall topic]

## Common Ground
• [Point 1]
• [Point 2]

## Key Differences
| Aspect | Article | Analysis |
|--------|---------|----------|
| ... | ... | ... |

## Credibility Ranking
1. [Best sourced]
2. [Second]
...

Articles:
{chr(10).join([f'--- {c["url"]} ---\n{c["content"][:2000]}' for c in contents])}"""
    
    result, error = call_api(prompt)
    if error:
        print_step("error", error)
        return
    
    print()
    print_markdown(result)

# ═══════════════════════════════════════════════════════════
# Prompts
# ═══════════════════════════════════════════════════════════
LANG_MAP = {"zh": "Chinese", "en": "English", "ja": "Japanese", 
            "ko": "Korean", "fr": "French", "de": "German", "es": "Spanish", "auto": "Same as source"}

LENGTH_MAP = {
    "short": "2-3 sentences", "medium": "1-2 paragraphs",
    "long": "detailed with key points", "xl": "comprehensive", "xxl": "complete report"
}

TYPE_PROMPTS = {
    "academic": "🎓 ACADEMIC: Research question, methodology, findings, limitations, significance. Formal tone.",
    "news": "📰 NEWS: 5W1H, key quotes, impact, context.",
    "ecommerce": "🛒 PRODUCT: Features, specs, price, pros/cons, alternatives.",
    "code": "💻 CODE: Functionality, API, requirements, examples.",
    "recipe": "🍳 RECIPE: Ingredients, time, difficulty, steps, tips.",
    "tutorial": "📖 TUTORIAL: Prerequisites, steps, common mistakes, tips.",
    "review": "⭐ REVIEW: Verdict, pros/cons, comparison, rating.",
    "video": "🎬 VIDEO: Topics, insights, timestamps, conclusions.",
    "article": "📝 ARTICLE: Main argument, evidence, conclusions."
}

def build_prompt(content, length, ctype, lang):
    return f"""Summarize in {LANG_MAP.get(lang, 'English')}.
Length: {LENGTH_MAP.get(length, LENGTH_MAP['medium'])}
Type: {TYPE_PROMPTS.get(ctype, TYPE_PROMPTS['article'])}

Format:
## Summary
[Clear summary]

## Key Points
• [Bullet 1 - specific]
• [Bullet 2 - with examples]
• [Bullet 3]
• [Bullet 4]
• [Bullet 5]

## Tags
#[tag1] #[tag2] #[tag3]

Content ({len(content)} chars):
{content[:10000]}"""

# ═══════════════════════════════════════════════════════════
# Content Fetching
# ═══════════════════════════════════════════════════════════
def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml'
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 10]
        return '\n'.join(lines)[:15000]
    except Exception as e:
        return f"[Error: {e}]"

def fetch_pdf(path):
    try:
        result = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True, timeout=30)
        return result.stdout[:15000] if result.stdout else "[No text]"
    except:
        return "[pdftotext not found]"

def fetch_image(path):
    try:
        with open(path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        cfg = load_config()
        if not cfg.get('endpoint') or not cfg.get('key'):
            return "[API not configured]"
        data = {
            "model": cfg.get('model', 'gpt-4o-mini'),
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": "Describe this image thoroughly."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_data[:500000]}"}}
            ]}]
        }
        req = urllib.request.Request(
            cfg['endpoint'].rstrip('/') + "/chat/completions",
            data=json.dumps(data).encode(),
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {cfg["key"]}'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            if 'choices' in result:
                return result['choices'][0]['message']['content']
        return "[Vision error]"
    except Exception as e:
        return f"[Error: {e}]"

def fetch_youtube(url):
    try:
        result = subprocess.run(['summarize', url, '--extract-only'], capture_output=True, text=True, timeout=30)
        return result.stdout[:15000] if result.stdout else "[No transcript]"
    except:
        return "[summarize CLI not found]"

def fetch_audio(path):
    try:
        result = subprocess.run(['summarize', path, '--extract-only'], capture_output=True, text=True, timeout=60)
        return result.stdout[:15000] if result.stdout else "[Transcription failed]"
    except:
        return "[summarize CLI not found]"

def get_content(input_url):
    if 'youtube.com' in input_url or 'youtu.be' in input_url:
        return fetch_youtube(input_url)
    elif input_url.startswith(('http://', 'https://')):
        return fetch_url(input_url)
    elif os.path.isfile(input_url):
        ext = pathlib.Path(input_url).suffix.lower()
        fetchers = {'.pdf': fetch_pdf, '.jpg': fetch_image, '.jpeg': fetch_image, '.png': fetch_image,
                    '.gif': fetch_image, '.webp': fetch_image, '.mp3': fetch_audio, '.wav': fetch_audio,
                    '.mp4': fetch_audio, '.m4a': fetch_audio, '.ogg': fetch_audio}
        if ext in fetchers:
            return fetchers[ext](input_url)
        try:
            return open(input_url).read()[:15000]
        except:
            return "[Read error]"
    return input_url

# ═══════════════════════════════════════════════════════════
# Core Summarize
# ═══════════════════════════════════════════════════════════
def summarize(input_url, length='auto', lang='auto', use_cache=True, verbose=False, notify=False):
    cache_key = get_cache_key(input_url, length)
    cache = load_cache()
    
    if use_cache and cache_key in cache:
        cached = cache[cache_key]
        print_step("cache", f"Cached: {cached['time']}")
        return cached['summary'], cached.get('type', 'unknown'), cached.get('tags', [])
    
    print_step("fetch", f"Fetching: {input_url[:60]}...")
    content = get_content(input_url)
    if len(content) < 20:
        return content, "error", []
    
    ctype, type_label = detect_content_type(content, input_url)
    detected_lang = detect_language(content) if lang == 'auto' else lang
    summary_length, length_label = auto_length(content) if length == 'auto' else (length, length.title())
    
    if verbose:
        print_step("analyze", f"Type: {type_label} | Lang: {LANG_MAP.get(detected_lang)} | Length: {length_label}")
    
    prompt = build_prompt(content, summary_length, ctype, detected_lang)
    print_step("stream", "Generating summary...")
    
    summary, error = call_api(prompt)
    if error:
        return f"[Error: {error}]", ctype, []
    
    # Extract tags
    print_step("tag", "Extracting tags...")
    tags = extract_tags(content, summary)
    
    # Check keywords
    found_kw = check_keywords(content, input_url)
    if found_kw:
        print_step("keyword", f"Found: {', '.join([k for k, _ in found_kw])}")
    
    # Cache
    if use_cache:
        cache[cache_key] = {"time": datetime.now().isoformat(), "summary": summary, "type": ctype, "tags": tags}
        save_cache(cache)
    
    # History
    history = load_history()
    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": input_url[:100],
        "summary": summary[:200],
        "type": ctype,
        "tags": tags,
        "length": summary_length
    })
    save_history(history)
    
    # Notify
    if notify:
        send_notification("✨ Summary Complete", f"{input_url[:40]}...\nTap to view")
    
    return summary, ctype, tags

# ═══════════════════════════════════════════════════════════
# Commands
# ═══════════════════════════════════════════════════════════
def cmd_search(args):
    """Search history"""
    if not args:
        print(f"{Colors.YELLOW}Usage: summarize-all search <query>{Colors.RESET}")
        return
    
    query = ' '.join(args)
    print_step("search", f"Searching: '{query}'...")
    results = search_history(query)
    
    if not results:
        print(f"{Colors.DIM}No results found{Colors.RESET}")
        return
    
    print(f"{Colors.CYAN}Found {len(results)} results:{Colors.RESET}\n")
    for i, item in enumerate(results, 1):
        tags = ', '.join([f"#{t}" for t in item.get('tags', [])]) or ""
        print(f"{i}. [{item['time']}] {item.get('type', '?').upper()} {tags}")
        print(f"   {item['source'][:60]}...")
        print(f"   {item['summary'][:80]}...")
        print()

def cmd_batch(args):
    """Batch process URLs from file or list"""
    urls = []
    
    # From file
    if args and os.path.isfile(args[0]):
        with open(args[0]) as f:
            urls = [line.strip() for line in f if line.strip().startswith(('http', 'https'))]
    
    # From stdin
    elif not args or args[0] == '-':
        print_step("batch", "Reading URLs from stdin (Ctrl+D to finish)...")
        try:
            urls = [line.strip() for line in sys.stdin if line.strip().startswith(('http', 'https'))]
        except:
            pass
    
    # From arguments
    else:
        urls = [arg for arg in args if arg.startswith(('http', 'https'))]
    
    if not urls:
        print(f"{Colors.YELLOW}No URLs provided{Colors.RESET}")
        print("Usage: summarize-all batch <file.txt>")
        print("   or: cat urls.txt | summarize-all batch -")
        return
    
    print_step("batch", f"Processing {len(urls)} URLs...")
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n{Colors.CYAN}[{i}/{len(urls)}]{Colors.RESET} {url}")
        summary, ctype, tags = summarize(url, 'auto', 'auto', True, True)
        results.append({"url": url, "summary": summary, "type": ctype, "tags": tags})
        
        if len(results) >= 3:
            print_step("notify", f"Processed {i}/{len(urls)}")
    
    # Summary report
    print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Batch Summary: {len(results)}/{len(urls)} completed{Colors.RESET}")
    
    send_notification("✨ Batch Complete", f"Processed {len(results)} URLs")

def cmd_compare(args):
    """Compare multiple sources"""
    if len(args) < 2:
        print(f"{Colors.YELLOW}Usage: summarize-all compare <url1> <url2> [url3...]{Colors.RESET}")
        return
    
    urls = [arg for arg in args if arg.startswith(('http', 'https'))]
    if len(urls) < 2:
        print(f"{Colors.YELLOW}Need at least 2 URLs{Colors.RESET}")
        return
    
    if len(urls) <= 3:
        compare_articles(urls)
    else:
        # Multi-article comparison
        compare_articles(urls)

def cmd_academic(args):
    """Academic paper mode"""
    if not args:
        print(f"{Colors.YELLOW}Usage: summarize-all academic <pdf_or_url>{Colors.RESET}")
        return
    
    url = args[0]
    print_step("academic", f"Academic analysis: {url}")
    
    content = get_content(url)
    if len(content) < 100:
        print_step("error", "Could not extract content")
        return
    
    print_step("academic", "Analyzing paper structure...")
    result, error = academic_summary(content)
    
    if error:
        print_step("error", error)
        return
    
    print()
    print_markdown(result)

def cmd_server(args):
    """API server"""
    port = int(args[0]) if args and args[0].isdigit() else 8080
    
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass
        
        def do_POST(self):
            if self.path != '/summarize':
                self.send_error(404)
                return
            try:
                length = int(self.headers.get('Content-Length', 0))
                data = json.loads(self.rfile.read(length).decode())
                
                url = data.get('url', '')
                lang = data.get('lang', 'auto')
                
                summary, ctype, tags = summarize(url, 'auto', lang, True, True)
                
                result = {"summary": summary, "type": ctype, "tags": tags}
                
                # Webhook
                if data.get('webhook'):
                    try:
                        req = urllib.request.Request(
                            data['webhook'],
                            data=json.dumps(result).encode(),
                            headers={'Content-Type': 'application/json'},
                            method='POST'
                        )
                        urllib.request.urlopen(req, timeout=10)
                    except:
                        pass
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_error(500)
        
        def do_GET(self):
            if self.path == '/health':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            elif self.path == '/tags':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(load_tags()).encode())
            else:
                self.send_error(404)
    
    print_banner()
    print(f"\n{Colors.GREEN}🚀 API Server on port {port}{Colors.RESET}")
    print(f"{Colors.DIM}   POST /summarize {{url, lang, webhook}}{Colors.RESET}")
    print(f"{Colors.DIM}   GET  /health{Colors.RESET}")
    print(f"{Colors.DIM}   GET  /tags{Colors.RESET}\n")
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        httpd.serve_forever()

def cmd_config(args):
    cfg = load_config()
    if not args:
        if cfg:
            print(f"{Colors.CYAN}⚙️  Config:{Colors.RESET}")
            for k, v in cfg.items():
                if k == 'key':
                    v = v[:8] + "..." + v[-4:] if len(v) > 12 else v
                print(f"  {k}: {v}")
        else:
            print(f"{Colors.DIM}Not configured{Colors.RESET}")
        return
    
    if args[0] == 'set' and len(args) >= 3:
        cfg[args[1]] = ' '.join(args[2:])
        save_config(cfg)
        print_step("done", f"Set {args[1]}")
    elif args[0] == 'reset':
        for f in [CONFIG_FILE, CACHE_FILE, HISTORY_FILE, TAGS_FILE, KEYWORDS_FILE]:
            if f.exists():
                f.unlink()
        print_step("done", "All data reset")

def cmd_history(args):
    limit = int(args[0]) if args and args[0].isdigit() else 10
    history = load_history()
    if not history:
        print(f"{Colors.DIM}No history{Colors.RESET}")
        return
    recent = history[-limit:]
    print(f"{Colors.CYAN}📜 History ({len(recent)}):{Colors.RESET}\n")
    for i, item in enumerate(reversed(recent), 1):
        tags = ', '.join([f"#{t}" for t in item.get('tags', [])]) or ""
        print(f"{i}. [{item['time']}] {item.get('type', '?').upper()} {tags}")
        print(f"   {item['source'][:60]}")
        print()

def cmd_keywords(args):
    if not args:
        list_keywords()
    elif args[0] == 'add' and len(args) >= 2:
        add_keyword(args[1], args[2] if len(args) > 2 else "Alert")
    elif args[0] == 'remove':
        for kw in args[1:]:
            remove_keyword(kw)
    elif args[0] == 'list':
        list_keywords()

def cmd_tags(args):
    tags = load_tags()
    if not tags:
        print(f"{Colors.DIM}No tags yet{Colors.RESET}")
        return
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    print(f"{Colors.CYAN}🏷️  Tag Cloud:{Colors.RESET}\n")
    for tag, count in sorted_tags[:20]:
        print(f"  {tag}: {count}")

def interactive_mode():
    print_banner()
    print(f"""
{Colors.CYAN}Commands:{Colors.RESET}
  <url>              Summarize
  batch <file>      Batch process URLs
  compare <u1> <u2>  Compare articles
  academic <pdf/url> Academic paper mode
  search <query>     Search history
  tags               Show tag cloud
  keywords add <kw> [alert]  Track keyword
  keywords list      Show tracked keywords
  server [port]     API server
  config             Show config
  history [n]        Show history
  help               This help
  quit

{Colors.DIM}Examples:{Colors.RESET}
  > summarize-all https://news.com/article
  > batch urls.txt
  > compare a.com b.com c.com
  > academic paper.pdf
  > search "machine learning"
  > keywords add "AI" "New AI development"
""")
    while True:
        try:
            cmd = input(f"{Colors.GREEN}❯ {Colors.RESET}").strip()
            if not cmd:
                continue
            if cmd in ['quit', 'exit']:
                break
            
            parts = cmd.split()
            c = parts[0].lower()
            
            if c == 'batch':
                cmd_batch(parts[1:])
            elif c == 'compare':
                cmd_compare(parts[1:])
            elif c == 'academic':
                cmd_academic(parts[1:])
            elif c == 'search':
                cmd_search(parts[1:])
            elif c == 'tags':
                cmd_tags(parts[1:])
            elif c == 'keywords':
                cmd_keywords(parts[1:])
            elif c == 'server':
                cmd_server(parts[1:])
            elif c == 'config':
                cmd_config(parts[1:])
            elif c == 'history':
                cmd_history(parts[1:])
            elif c.startswith(('http://', 'https://')):
                summary, ctype, tags = summarize(c, 'auto', 'auto', True, True, True)
                print()
                print_markdown(f"## 📝 {ctype.upper()} Summary\n\n{summary}\n\n**Tags:** {', '.join(['#'+t for t in tags])}")
            elif os.path.isfile(c):
                summary, ctype, tags = summarize(c, 'auto', 'auto', True, True, True)
                print()
                print_markdown(f"## 📝 {ctype.upper()} Summary\n\n{summary}")
            else:
                # Plain text
                result, err = call_api(build_prompt(cmd, 'medium', 'article', 'auto'))
                if err:
                    print_step("error", err)
                else:
                    print_markdown(result)
        except (KeyboardInterrupt, EOFError):
            break
    print(f"{Colors.DIM}Goodbye!{Colors.RESET}")

def main():
    if len(sys.argv) < 2:
        interactive_mode()
        return
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ['--help', '-h']:
            print(__doc__)
            return
        elif arg == '--interactive' or arg == '-i':
            interactive_mode()
            return
        elif arg == 'batch':
            cmd_batch(args[i+1:])
            return
        elif arg == 'compare':
            cmd_compare(args[i+1:])
            return
        elif arg == 'academic':
            cmd_academic(args[i+1:])
            return
        elif arg == 'search':
            cmd_search(args[i+1:])
            return
        elif arg == 'tags':
            cmd_tags(args[i+1:])
            return
        elif arg == 'keywords':
            cmd_keywords(args[i+1:])
            return
        elif arg == 'server':
            cmd_server(args[i+1:])
            return
        elif arg == 'config':
            cmd_config(args[i+1:])
            return
        elif arg == 'history':
            cmd_history(args[i+1:])
            return
        elif arg.startswith('-'):
            i += 2 if i+1 < len(args) else 1
        else:
            # URL or file
            summary, ctype, tags = summarize(arg, 'auto', 'auto', True, True, True)
            print()
            print_markdown(f"## 📝 {ctype.upper()} Summary\n\n{summary}\n\n**Tags:** {', '.join(['#'+t for t in tags])}")
            i += 1

if __name__ == "__main__":
    main()
