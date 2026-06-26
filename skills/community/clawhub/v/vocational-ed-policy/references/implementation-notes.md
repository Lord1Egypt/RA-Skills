# Web Scraping Implementation Notes | 网页抓取实现笔记

## Core Implementation | 核心实现

### Technology Stack | 技术栈

**Python**:
- `requests` - HTTP library for fetching web pages
- `beautifulsoup4` - HTML parsing library
- `lxml` - Faster HTML parser (optional but recommended)

**Installation**:
```bash
pip install requests beautifulsoup4 lxml
```

---

## Scrape Website Method | 网站抓取方法

### Method Signature
```python
def scrape_website(self, site_name: str, site_config: Dict) -> int:
```

### Implementation Flow | 实现流程

1. **Setup Headers** | 设置请求头
   ```python
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
   }
   ```

2. **URL Priority** | URL 优先级
   - Try `vocational_url` first
   - Fallback to `policy_url`
   - This ensures vocational-specific content is prioritized

3. **Page Fetching** | 页面获取
   ```python
   response = requests.get(url, headers=headers, timeout=10)
   response.encoding = response.apparent_encoding
   soup = BeautifulSoup(response.text, 'html.parser')
   ```

4. **Link Extraction** | 链接提取
   ```python
   links = soup.find_all('a', href=True)
   ```

5. **Filtering Logic** | 过滤逻辑

   **Skip conditions** | 跳过条件:
   - Empty titles or < 5 characters
   - `javascript:` links and anchors
   - Navigation links ending with '司', '委员会', '办公室'
   - ICP/license info containing 'ICP' or '网安备'
   
   ```python
   if not title or len(title) < 5:
       continue
   
   href = link.get('href', '')
   if not href or href.startswith('javascript:') or href.startswith('#'):
       continue
   
   if re.search(r'司$|委员会$|办公室$', title):
       continue
   
   if 'ICP' in title or '网安备' in title:
       continue
   ```

6. **Date Extraction** | 日期提取

   **Supported formats** | 支持格式:
   - `YYYY-MM-DD` (2026-06-01)
   - `YYYY年MM月DD日` (2026年6月1日)
   - `YYYY/MM/DD` (2026/06/01)
   - `YYYY.MM.DD` (2026.06.01)
   
   ```python
   date_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', link_text)
   if date_match:
       date_str = date_match.group(0)
   else:
       date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', link_text)
       if date_match:
           year, month, day = date_match.groups()
           date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
   ```

7. **Duplicate Prevention** | 去重处理
   ```python
   if not any(r['title'] == title and r['url'] == full_url for r in self.results):
       self.results.append(result)
   ```

---

## Date Parsing | 日期解析

### Patterns Used | 使用的模式

```python
patterns = [
    r'(\d{4})-(\d{1,2})-(\d{1,2})',      # 2026-06-01
    r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 2026年6月1日
    r'(\d{4})/(\d{1,2})/(\d{1,2})',      # 2026/06/01
    r'(\d{4})\.(\d{1,2})\.(\d{1,2})'      # 2026.06.01
]
```

### Date Range Check | 日期范围检查

```python
def is_within_date_range(self, date: datetime) -> bool:
    cutoff_date = datetime.now() - timedelta(days=self.days)
    return date >= cutoff_date
```

---

## Filtering Mechanisms | 过滤机制

### Keyword Filtering | 关键词过滤

```python
def filter_by_keywords(self, title: str) -> bool:
    if not self.keywords:
        return True
    
    title_lower = title.lower()
    for keyword in self.keywords:
        if keyword.lower() in title_lower:
            return True
    return False
```

### Category Determination | 类别确定

```python
def determine_category(self, title: str) -> Optional[str]:
    if not self.category:
        for cat, cat_keywords in CATEGORIES.items():
            for kw in cat_keywords:
                if kw in title:
                    return cat
    return self.category
```

**Categories**:
- `policy`: 政策文件 (Policy Documents)
- `project`: 课题申报 (Project Applications)
- `achievement`: 教学成果奖 (Teaching Achievement Awards)
- `integration`: 产教融合 (Industry-Education Integration)
- `certificate`: 1+X证书 (1+X Certificates)
- `double_high`: 双高计划 (Double High Plan)

---

## Error Handling | 错误处理

### ImportError Handling
```python
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    error_msg = "缺少依赖库: requests 或 beautifulsoup4。请安装: pip install requests beautifulsoup4"
    self.errors.append(error_msg)
    print(f"❌ {error_msg}")
    return 0
```

### Request Error Handling
```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    # ... process response
except Exception as e:
    error_msg = f"{url}: {str(e)}"
    self.errors.append(error_msg)
    print(f"⚠️ 错误: {str(e)[:100]}")
    continue
```

---

## Performance Considerations | 性能考虑

### Current Implementation | 当前实现
- Sequential website scraping
- 1-second delay between requests
- Timeout: 10 seconds per request

### Future Optimizations | 未来优化
1. **Async/await** with `aiohttp`
2. **Concurrent processing** with `ThreadPoolExecutor`
3. **Response caching** to avoid duplicate requests
4. **Rate limiting** to be respectful to servers

---

## Testing Notes | 测试笔记

### Test Results | 测试结果

**Test Case 1**: Scrape without keywords
```bash
python scrape_voc_ed_policy.py --days 7
```
**Result**: 51 files found (includes navigation links)

**Test Case 2**: Scrape with keywords
```bash
python scrape_voc_ed_policy.py --keywords "职业教育" --days 7
```
**Result**: 7 files found (filtered by keywords)

**Test Case 3**: Scrape Ministry of Education
```bash
python scrape_voc_ed_policy.py --keywords "双高计划" --days 30
```
**Result**: Successfully extracts policy documents with relevant keywords

---

## Known Limitations | 已知限制

1. **HTML Structure Variations**: Different government websites use different HTML structures
2. **Anti-Scraping Mechanisms**: Some websites may block automated requests
3. **Date Format Variations**: Not all date formats are supported
4. **JavaScript-Rendered Content**: Does not capture dynamic content loaded via JavaScript

---

## WSL Publishing Workflow | WSL 发布工作流

When publishing to ClawHub from WSL:

```bash
# 1. Copy skill to Windows Desktop
cp -r ~/.hermes/skills/your-skill /mnt/c/Users/lenovo/Desktop/

# 2. Publish using PowerShell
powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version 1.0.0"

# 3. Verify publication
powershell.exe -Command "clawhub inspect your-slug"

# 4. Clean up
rm -rf /mnt/c/Users/lenovo/Desktop/your-skill
```

**Important**: WSL cannot execute Windows binaries directly (powershell.exe, cmd.exe). Use subprocess with PowerShell commands.

---

## ClawHub Specific Notes | ClawHub 特定说明

### Slug Format Restrictions
- Only lowercase letters, digits, and single hyphens
- Must start and end with a letter or digit
- NO Chinese characters
- NO consecutive hyphens

### Display Name Behavior
ClawHub auto-generates English display names from slug. The `displayName` field in SKILL.md does NOT affect the displayed name in skill listings.

**Workaround**: Use full Chinese description in the `description` field for clarity.

### Publishing Updates
To update an existing skill:
1. Use the SAME slug
2. Increment version number
3. Publish with `--version` parameter

```bash
clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version 1.1.0
```

To rename a skill:
```bash
clawhub skill rename old-slug new-slug --yes
```