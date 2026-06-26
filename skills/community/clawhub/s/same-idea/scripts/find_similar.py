#!/usr/bin/env python3
"""
Find similar ideas and quotes from user's knowledge base.
Searches Logseq and Obsidian vaults for resonating concepts.

Features:
- Smart keyword extraction using jieba (with fallback to n-gram)
- Semantic similarity matching
- Source extraction (book names, authors)
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple
import subprocess
import unicodedata

# Try to import jieba
try:
    import jieba
    jieba.initialize()
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("Warning: jieba not installed, using fallback segmentation", file=sys.stderr)

# Knowledge base paths
LOGSEQ_VAULT = Path.home() / "Library/Mobile Documents/iCloud~com~logseq~logseq/Documents"
OBSIDIAN_VAULT = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents"

# Chinese stop words (common function words)
CN_STOP_WORDS = {
    '可以', '需要', '通过', '进行', '使用', '方法', '方式', '结果', '过程', '部分',
    '方面', '情况', '问题', '东西', '时候', '地方', '人们', '所有', '有些', '很多',
    '非常', '比较', '相对', '关于', '根据', '按照', '由于', '因此', '所以', '但是',
    '然而', '不过', '只是', '还是', '或者', '以及', '还有', '另外', '此外', '而且',
    '并且', '不但', '不仅', '除非', '除了', '除去', '有关', '相关', '涉及', '包括',
    '包含', '含有', '具有', '拥有', '具备', '存在', '发生', '出现', '产生', '形成',
    '成为', '变成', '变为', '转为', '化为', '作为', '当作', '看做', '视为', '认为',
    '觉得', '感到', '感觉', '可能', '也许', '大概', '大约', '差不多', '几乎', '简直',
    '根本', '完全', '绝对', '肯定', '一定', '必须', '务必', '确定', '决定', '决心',
    '打算', '计划', '准备', '安排', '组织', '开展', '实施', '执行', '实行', '实现',
    '完成', '达到', '达成', '获得', '取得', '得到', '收到', '受到', '接受', '接收',
    '采纳', '采用', '采取', '运用', '应用', '利用', '开始', '启动', '发动', '发起',
    '动员', '调动', '调整', '调节', '调控', '管理', '治理', '处理', '处置', '办理',
    '解决', '解答', '解释', '说明', '阐明', '阐述', '论述', '讨论', '探讨', '研究',
    '钻研', '探索', '探求', '寻求', '寻找', '找出', '觉察', '意识', '认知', '明了',
    '懂得', '了解', '理解', '清楚', '清晰', '明确', '明显', '显著', '突出', '以为',
    '感受', '体会', '体验', '经历', '经验', '教训', '启示', '启发', '启迪', '提示',
    '提醒', '暗示', '表明', '显示', '展示', '展现', '呈现', '涌现', '浮现', '显露',
    '暴露', '揭露', '揭示', '揭开', '打开', '开启', '开放', '不是', '这些', '那些',
    '这个', '那个', '一种', '一些', '一点', '一旦', '一般', '一样', '一直', '一边',
    '一旦', '一方面', '另一方面', '其他', '其余', '其它', '每', '各', '某', '本',
    '此', '其', '之', '的', '了', '在', '是', '有', '和', '与', '或', '但', '而',
    '则', '就', '于', '从', '到', '把', '被', '让', '给', '向', '对', '为', '以',
    '及', '等', '如', '若', '因', '而', '则', '且', '并', '这', '那', '哪', '谁',
    '怎样', '如何', '多少', '什么', '几', '之', '所', '者', '被', '乎', '于'
}

# Semantic synonyms groups (concept -> related concepts)
SYNONYMS = {
    '复利': ['复利', '利滚利', '指数', '指数增长', '指数级', '增长', '积累'],
    '金钱': ['金钱', '钱', '财富', '资金', '资本', '资产', '货币', '财务', '经济'],
    '知识': ['知识', '智慧', '认知', '信息', '学问', '学识', '认知', '思维', '思想'],
    '关系': ['关系', '人脉', '人际', '社交', '连接', '联系', '网络'],
    '时间': ['时间', '时光', '光阴', '岁月', '时候', '时机', '期限'],
    '学习': ['学习', '读书', '阅读', '教育', '培训', '进修', '成长'],
    '习惯': ['习惯', '行为', '做法', '方式', '习性', '惯例'],
    '思维': ['思维', '思考', '想法', '观念', '理念', '认知', '心智'],
    '行动': ['行动', '实践', '执行', '做事', '行为', '作为'],
    '成功': ['成功', '成就', '胜利', '达成', '实现', '目标', '结果'],
    '失败': ['失败', '挫折', '错误', '失误', '教训'],
    '投资': ['投资', '投入', '花费', '支出', '成本'],
    '风险': ['风险', '危险', '不确定性', '波动', '概率'],
    '健康': ['健康', '身体', '体质', '健身', '运动', '养生'],
    '幸福': ['幸福', '快乐', '满足', '愉悦', '快乐', '美好'],
    '创造': ['创造', '创新', '发明', '设计', '构建'],
    '领导': ['领导', '管理', '带领', '指引', '影响'],
    '沟通': ['沟通', '交流', '对话', '谈话', '表达'],
    '决策': ['决策', '选择', '决定', '判断', '抉择'],
    '耐心': ['耐心', '坚持', '持续', '长期', '持久'],
    '专注': ['专注', '集中', '专注', '专心', '聚焦'],
    '效率': ['效率', '效能', '速度', '快速', '高效'],
    '目标': ['目标', '目的', '方向', '志向', '愿景'],
    '计划': ['计划', '规划', '安排', '方案', '策略'],
    '团队': ['团队', '团队', '群体', '组织', '集体'],
    '产品': ['产品', '商品', '作品', '成果', '产出'],
    '用户': ['用户', '客户', '消费者', '顾客', '使用者'],
    '价值': ['价值', '意义', '重要性', '意义', '用处'],
    '品牌': ['品牌', '声誉', '形象', '口碑', '信誉'],
    '市场': ['市场', '行业', '领域', '圈子', '界'],
    '销售': ['销售', '卖出', '营销', '推广', '推广'],
    '收入': ['收入', '收益', '盈利', '利润', '营收'],
    '成本': ['成本', '花费', '支出', '代价', '费用'],
}


def simple_chinese_segment(text: str) -> List[str]:
    """Fallback Chinese segmentation using n-gram and statistical approach."""
    if not text:
        return []
    
    # Remove punctuation - keep it simple
    text = re.sub(r'[,。!?;:\'"，。、；：""''（）【】《》—…·.]', ' ', text)
    
    # Common characters that shouldn't form words by themselves
    common_chars = set('的一是了不在有和人这那都着也就要会可被给向对为以及其于的')
    
    # Words that look like sentence fragments (incomplete phrases)
    fragment_patterns = ['不仅', '而且', '但是', '因此', '所以', '对于', '关于', '通过', '进行', 
                        '可以', '需要', '应该', '能够', '适用于', '不适用', '不仅适', '应不仅',
                        '于金', '于银', '于钱']
    
    # Extract Chinese words (2-4 chars) that are meaningful
    words = []
    for length in [4, 3, 2]:  # Try longer words first
        pattern = re.compile(rf'[\u4e00-\u9fff]{{{length}}}')
        found = pattern.findall(text)
        for word in found:
            # Skip if all chars are common
            if all(c in common_chars for c in word):
                continue
            # Skip if it's a stop word
            if word in CN_STOP_WORDS:
                continue
            # Skip fragments and partial matches
            if word in fragment_patterns:
                continue
            # Skip if too many common chars (>40%)
            common_count = sum(1 for c in word if c in common_chars)
            if common_count > len(word) * 0.4:
                continue
            # Skip if starts/ends with common char and is short
            if len(word) <= 2 and (word[0] in common_chars or word[-1] in common_chars):
                continue
            words.append(word)
    
    # Also extract English words
    english = re.findall(r'[a-zA-Z]{3,}', text.lower())
    words.extend(english)
    
    return words


def extract_keywords(text: str) -> List[str]:
    """Extract key concepts from input text using jieba or fallback."""
    # Clean text
    text = re.sub(r'[,。!?;:\'"，。、；：""''（）【】《》—…·.]', ' ', text)
    
    keywords = []
    
    if JIEBA_AVAILABLE:
        # Use jieba for precise segmentation
        words = jieba.cut(text)
        for word in words:
            word = word.strip()
            # Filter: 2+ chars for Chinese, 3+ for English, not stop word
            if (len(word) >= 2 and '\u4e00' <= word[0] <= '\u9fff' and word not in CN_STOP_WORDS) or \
               (word.isalpha() and len(word) >= 3):
                keywords.append(word)
    else:
        # Use fallback segmentation
        keywords = simple_chinese_segment(text)
    
    # Additional filtering: remove patterns that look like sentence fragments
    # Common fragments to avoid (appear in middle of phrases)
    fragments_to_remove = {'不仅', '而且', '但是', '因此', '所以', '对于', '关于', '通过', '进行', '可以', '需要', '应该', '能够'}
    
    # Deduplicate and filter
    seen = set()
    unique_keywords = []
    for kw in keywords:
        # Skip stop words and fragments
        if kw in CN_STOP_WORDS or kw in fragments_to_remove:
            continue
        if kw not in seen:
            seen.add(kw)
            # Additional check: skip if it's a substring of a longer keyword we already have
            is_substring = any(kw in longer and kw != longer for longer in unique_keywords)
            if not is_substring or len(kw) >= 3:
                unique_keywords.append(kw)
    
    # Return top 10 most relevant keywords (prefer longer, more specific keywords)
    unique_keywords.sort(key=len, reverse=True)
    return unique_keywords[:10]


def expand_keywords(keywords: List[str]) -> List[str]:
    """Expand keywords with semantic synonyms."""
    expanded = set(keywords)
    
    for kw in keywords:
        # Check if keyword belongs to any synonym group
        for group_name, group_words in SYNONYMS.items():
            if kw in group_words:
                expanded.update(group_words)
                break
        
        # Also add partial matches
        for group_name, group_words in SYNONYMS.items():
            if any(kw in w or w in kw for w in group_words if len(kw) > 1):
                expanded.update(group_words)
    
    return list(expanded)


def extract_source(text: str, filepath: str = "") -> Dict[str, str]:
    """Extract book name and author from text and filepath."""
    result = {'book': None, 'author': None}
    
    # Pattern for Chinese book names 《》
    book_pattern = re.compile(r'《([^》]+)》')
    book_match = book_pattern.search(text)
    if book_match:
        result['book'] = book_match.group(1).strip()
    
    # Pattern for English book titles ""
    eng_book_pattern = re.compile(r'"([^"]+)"')
    eng_book_match = eng_book_pattern.search(text)
    if eng_book_match and not result['book']:
        result['book'] = eng_book_match.group(1).strip()
    
    # Extract from filepath if in 书评/书 folder
    if not result['book'] and filepath:
        # Pattern: .../书评/书名.md or .../books/书名.md
        match = re.search(r'[/(](?:书评|books|book)[/\\]([^/\\.]+?)(?:\.md|$)', filepath, re.IGNORECASE)
        if match:
            result['book'] = match.group(1).strip()
    
    # Pattern for author - various formats
    author_patterns = [
        re.compile(r'作者[：:]\s*([^\s，。,]{2,10})'),
        re.compile(r'——\s*([^\s，。,]{2,10})'),
        re.compile(r'出自[^\w]+([^\s，。,]{2,10})'),
        re.compile(r'by\s+([A-Za-z\s]+)'),
    ]
    
    for pattern in author_patterns:
        match = pattern.search(text)
        if match:
            result['author'] = match.group(1).strip()
            break
    
    return result


def is_quote(text: str) -> bool:
    """Check if text is a quote."""
    quote_markers = ['"', '"', '「', '『', '"', '"', '>', '「', '『']
    return any(m in text for m in quote_markers)


def search_vault(vault_path: Path, keywords: List[str]) -> List[Dict]:
    """Search vault for files containing keywords."""
    results = []
    
    if not vault_path.exists():
        return results
    
    # Build search terms (combine original + expanded keywords)
    all_keywords = expand_keywords(keywords)
    
    for keyword in all_keywords[:8]:  # Limit to top 8 keywords
        cmd = ['rg', '-i', '-n', '--type', 'md', '-C', '2', '-w', keyword, str(vault_path)]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, timeout=15)
            lines = output.strip().split('\n')[:15]
            
            for line in lines:
                if ':' not in line or line.startswith('--'):
                    continue
                
                # Find first colon that's after a digit (line number)
                # Pattern: filepath:line:content
                match = re.match(r'^(.+?):(\d+):(.*)$', line)
                if match:
                    filepath, lineno, content = match.groups()
                    content = content.strip()
                else:
                    continue
                
                # Skip metadata lines and noise
                if any(marker in content for marker in ['tags::', 'category::', 'alias::']):
                    continue
                # Skip block IDs and URLs
                if re.match(r'^\d+\s+\^[a-zA-Z0-9-]+', content):
                    continue
                if 'http://' in content or 'https://' in content:
                    continue
                
                # Extract source info
                source = extract_source(content, filepath)
                
                results.append({
                    'file': filepath,
                    'line': int(lineno),
                    'content': content,
                    'vault': vault_path.name,
                    'matched_keyword': keyword,
                    'is_quote': is_quote(content),
                    'source_book': source.get('book'),
                    'source_author': source.get('author')
                })
        except subprocess.TimeoutExpired:
            continue
        except subprocess.CalledProcessError:
            continue
        except FileNotFoundError:
            # Fallback to grep
            break
    
    return results


def calculate_similarity(content: str, keywords: List[str]) -> float:
    """Calculate semantic similarity score."""
    score = 0.0
    content_lower = content.lower()
    
    for kw in keywords:
        kw_lower = kw.lower()
        
        # Exact match (highest weight)
        if kw_lower in content_lower:
            score += 1.0
        
        # Partial match
        elif any(kw_lower in word or word in kw_lower for word in content_lower.split()):
            score += 0.5
    
    # Bonus for quotes
    if is_quote(content):
        score += 0.5
    
    # Bonus for explicit sources
    if any(marker in content for marker in ['《', '作者', '来源', '出自', '——', '"']):
        score += 0.3
    
    return score


def rank_results(results: List[Dict], keywords: List[str]) -> List[Dict]:
    """Rank results by relevance using semantic similarity."""
    scored = []
    
    all_keywords = expand_keywords(keywords)
    
    for result in results:
        content = result.get('content', '')
        score = calculate_similarity(content, all_keywords)
        
        # Bonus for matching original keywords (not just synonyms)
        for kw in keywords:
            if kw.lower() in content.lower():
                score += 0.5
                break
        
        result['score'] = round(score, 2)
        scored.append(result)
    
    # Sort by score descending
    scored.sort(key=lambda x: x['score'], reverse=True)
    
    # Remove near-duplicates based on content similarity
    unique_results = []
    seen_content = set()
    
    for r in scored:
        # Create a simple fingerprint
        fingerprint = r['content'][:30].lower().strip()
        if fingerprint not in seen_content:
            seen_content.add(fingerprint)
            unique_results.append(r)
    
    return unique_results[:10]


def format_output(results: List[Dict], keywords: List[str]) -> str:
    """Format results for human-readable output."""
    if not results:
        return "没有找到相似的想法 💭"
    
    output_lines = []
    output_lines.append(f"🔍 关键词: {', '.join(keywords[:5])}")
    output_lines.append("")
    output_lines.append("💡 相似想法:")
    output_lines.append("")
    
    for i, r in enumerate(results, 1):
        content = r['content']
        if len(content) > 80:
            content = content[:80] + "..."
        
        # Add source info
        source_parts = []
        if r.get('source_book'):
            source_parts.append(f"《{r['source_book']}》")
        if r.get('source_author'):
            source_parts.append(r['source_author'])
        
        source_str = f" — {', '.join(source_parts)}" if source_parts else ""
        
        # Add quote marker
        if r.get('is_quote'):
            content = f"「{content}」"
        
        output_lines.append(f"{i}. {content}{source_str}")
        
        # Show matched keyword
        output_lines.append(f"   🔑 匹配词: {r.get('matched_keyword', 'N/A')} | 得分: {r.get('score', 0)}")
        output_lines.append("")
    
    return "\n".join(output_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: find_similar.py <idea_text>", file=sys.stderr)
        sys.exit(1)
    
    idea_text = sys.argv[1]
    
    # Extract keywords
    keywords = extract_keywords(idea_text)
    
    # Search both vaults
    all_results = []
    
    if LOGSEQ_VAULT.exists():
        results = search_vault(LOGSEQ_VAULT, keywords)
        all_results.extend(results)
        print(f"Logseq: found {len(results)} results", file=sys.stderr)
    
    if OBSIDIAN_VAULT.exists():
        results = search_vault(OBSIDIAN_VAULT, keywords)
        all_results.extend(results)
        print(f"Obsidian: found {len(results)} results", file=sys.stderr)
    
    # Rank results
    ranked = rank_results(all_results, keywords)
    
    # Output as JSON for programmatic use
    output = {
        'input': idea_text,
        'keywords': keywords,
        'expanded_keywords': expand_keywords(keywords),
        'results': ranked,
        'total_found': len(all_results)
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()