---
name: china-3c-marketing-copilot
description: AI-powered marketing copilot for China's 3C consumer electronics market (mobile, laptops, earphones, wearables, smart home)
triggers:
  - "help me write a creative campaign for a new phone launch in China"
  - "analyze competitor risks for our earphone product"
  - "create a marketing strategy for smart home devices"
  - "evaluate risks for our laptop launch campaign"
  - "compare competitive landscape for wearables in China market"
  - "generate creative ideas for 3C product promotion"
  - "assess market positioning for consumer electronics"
  - "analyze KOL ecosystem for tech product launch"
---

# China 3C Marketing Copilot Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

An AI-powered knowledge base and copilot system for marketing consumer electronics (3C) in the Chinese market. Covers smartphones, laptops, earphones, wearables, and smart home devices with competitive analysis, creative campaign generation, risk assessment, and market insights.

## What This Project Does

China 3C Marketing Copilot is a structured knowledge base designed to be used as context for AI agents to:

- **Generate creative campaigns** grounded in real market data
- **Analyze competitive threats** using cross-referenced product evaluations
- **Assess marketing risks** including social media backlash scenarios
- **Provide category insights** from expert reviews (爱否科技, 笔吧评测室, etc.)
- **Simulate audience reactions** across 5 persona types
- **Break into new categories** using proven playbook strategies

The system enforces strict data discipline: no fabricated numbers, source attribution required, speculation must be labeled.

## Installation

Clone the repository:

```bash
git clone https://github.com/killsnake01/China-Marketing-Copilot-Skill.git
cd China-Marketing-Copilot-Skill
```

No additional dependencies required for basic usage. The knowledge base is pure Markdown.

For data preprocessing (optional):

```python
pip install pandas
python scripts/preprocess.py --input raw_data.csv --output knowledge-base/
```

## Project Structure

```
docs/
  templates/          # Output formats (creative, insights, risk)
  references/         # KOL database, platform rules, personas
  ecosystem/          # Industry terminology, memes to avoid
knowledge-base/
  mobile/            # Phone brand matrix, pricing tiers
  headphones/        # Earphone reviews, clip-on comparison
  laptops/           # Notebook selection guide (笔吧)
  wearables/         # Smartwatch/band market data
  smart-home/        # Robot vacuum reviews, case studies
scripts/
  preprocess.py      # Data cleaning utility
```

## Core Capabilities

### 1. Creative Campaign Generation

**Trigger phrases:**
- "帮我想几个创意" (give me some creative ideas)
- "写个传播方案" (write a campaign plan)
- "手机发布会创意" (phone launch event ideas)

**Output format:**
Uses `docs/templates/creative-output.md` template. Generates 3-5 ideas per request with:
- **Hook** (attention-grabbing headline)
- **Core Message** (data-driven value prop)
- **Execution** (platform-specific tactics)
- **Risk Flag** (potential backlash points)

**Example usage:**

```python
# In your AI agent prompt:
context = load_knowledge_base("knowledge-base/mobile/")
prompt = f"""
Using this data: {context}
Generate 3 creative campaign ideas for a mid-range phone (2000-3000 RMB)
with Snapdragon 8 Gen 3 chip, focusing on Xiaohongshu platform.
Follow creative-output.md template.
"""
```

**De-duplication:**
Check `docs/templates/used-ideas.md` before generation. Append new ideas to prevent repetition.

### 2. Competitive Analysis

**Trigger phrases:**
- "XX发布了,对我们有什么威胁" (XX launched, what's the threat)
- "分析竞品" (analyze competitors)
- "横评对比" (cross-evaluation comparison)

**Data sources in knowledge base:**
- `mobile/_index.md`: 16 phone brands, chipset camps, pricing tiers
- `laptops/_index.md`: 笔吧 2025 laptop guide, 8 price segments
- `headphones/_index.md`: 12 clip-on earphone comparison (爱否科技)

**Example code:**

```python
import os
import re

def load_category_data(category: str) -> dict:
    """Load brand matrix and evaluation data for a category."""
    base_path = f"knowledge-base/{category}/"
    index_file = os.path.join(base_path, "_index.md")
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract brand matrix table
    brands = re.findall(r'\| (.+?) \| (.+?) \| (.+?) \|', content)
    
    return {
        'category': category,
        'brands': brands,
        'raw_content': content
    }

# Usage
laptop_data = load_category_data('laptops')
# Feed to AI agent for competitive threat analysis
```

**Output format:**
Uses `docs/templates/insight-output.md` with required sections:
- **Market Position** (price tier, feature positioning)
- **Competitive Threats** (direct overlap products)
- **Differentiation Gaps** (where competitor is weak)
- **Data Sources** (must cite: KOL name + platform + date)

### 3. Risk Assessment

**Trigger phrases:**
- "会不会翻车" (will this backfire)
- "风险评估" (risk assessment)
- "有没有负面" (any negative risks)

**Template:**
`docs/templates/risk-assessment.md` includes:
- **Technical Risk** (spec exaggeration, measurement tricks)
- **Social Risk** (5 persona backlash simulation)
- **Platform Risk** (content guideline violations)
- **Historical Precedent** (similar campaigns that failed)

**Persona simulation:**
Load from `docs/references/comment-personas.md`:

```python
PERSONAS = {
    "参数党": "Spec sheet warriors - will fact-check every number",
    "解构找茬": "Deconstruction trolls - expose marketing tricks",
    "真实体验派": "Real user experience advocates - hate hype",
    "品牌信仰": "Brand loyalists - defend their tribe",
    "吃瓜群众": "Casual observers - amplify drama"
}

def simulate_comment_section(campaign_text: str, personas: dict) -> list:
    """Generate predicted negative comments from each persona."""
    comments = []
    for persona_type, description in personas.items():
        prompt = f"As a {persona_type} ({description}), critique: {campaign_text}"
        # Feed to AI agent
        comments.append(generate_critique(prompt))
    return comments
```

**Case study integration:**
Knowledge base includes real翻车案例 (backfire cases):
- `knowledge-base/laptops/_index.md`: Lenovo Y9000P thermal issues
- `knowledge-base/smart-home/`: Robot vacuum "deceptive cleaning" scandal

### 4. New Category Playbook

**Trigger phrases:**
- "怎么传播新品类" (how to promote new category)
- "市场教育成本高" (high market education cost)
- "新品类破局" (breakthrough strategy for new category)

**5 proven methods:**
Located in `docs/templates/new-category-playbook.md`

**Example - Method 1: 认知刷新法 (Perception Reset)**

```python
def generate_perception_reset_campaign(product_data: dict) -> dict:
    """
    Find human limit benchmark → Product breaks it → Visualize data
    
    Example: DJI ROMO cleaning 500㎡ villa in 2 hours
    (Human baseline: 4+ hours)
    """
    return {
        "human_baseline": "Find existing perception (e.g., 'villa cleaning takes half a day')",
        "product_performance": product_data['key_metric'],
        "visualization": "Side-by-side time-lapse video",
        "data_source": "Must cite: test environment + conditions"
    }

# Usage for smart home robot vacuum
romo_data = {
    'key_metric': '2小时清洁500㎡别墅 (2 hours for 500㎡ villa)',
    'comparison': '人工清洁需4小时+ (Manual: 4+ hours)'
}
campaign = generate_perception_reset_campaign(romo_data)
```

**Method 5: 专业信任纪录片法 (Professional Trust Documentary)**
- Recruit real professionals (not actors)
- 6-month field test period
- Minimalist documentary style (no hype language)
- Case study: DJI agriculture drones with actual farmers

### 5. Data Import & Preprocessing

**Trigger phrase:**
- "处理新数据" (process new data)
- "我导入了新文件" (I imported a new file)

**Preprocessing script:**

```python
# scripts/preprocess.py
import pandas as pd
import json
import sys

def clean_review_data(input_file: str, output_dir: str):
    """
    Clean and validate review data before adding to knowledge base.
    
    Validation rules:
    - Numbers must have units
    - Ratings must have scale (e.g., 5/5)
    - Price must include currency and date
    - Source must include: KOL name + platform + publish date
    """
    df = pd.read_csv(input_file)
    
    # Validation
    required_columns = ['product_name', 'metric', 'value', 'unit', 'source', 'date']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Check source format
    for idx, row in df.iterrows():
        source = row['source']
        if not ('|' in source and len(source.split('|')) >= 3):
            print(f"Warning: Invalid source format at row {idx}: {source}")
            print("Expected: KOL名|平台|日期 (e.g., 爱否科技|Bilibili|2025-03)")
    
    # Export to knowledge base
    category = df['category'].iloc[0]
    output_path = f"{output_dir}/{category}/_data.json"
    
    df.to_json(output_path, orient='records', force_ascii=False, indent=2)
    print(f"Processed {len(df)} records to {output_path}")

# Usage
if __name__ == "__main__":
    clean_review_data(sys.argv[1], sys.argv[2])
```

**Run preprocessing:**

```bash
python scripts/preprocess.py earphone_reviews.csv knowledge-base/
```

## Configuration

### User Profile (Optional)

Create `user-config.json` for personalized output:

```json
{
  "brand": "your_brand_name",
  "category": "mobile",
  "target_price_range": "2000-3000",
  "competitors": ["Redmi", "Realme", "iQOO"],
  "platforms": ["Xiaohongshu", "Douyin", "Bilibili"],
  "risk_tolerance": "conservative",
  "kol_preferences": ["爱否科技", "ZEALER"]
}
```

### Environment Variables

For API integrations (optional):

```bash
# .env file
XIAOHONGSHU_API_KEY=your_key_here
BILIBILI_API_KEY=your_key_here
MARKET_DATA_SOURCE=https://your-data-api.com
```

Load in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('XIAOHONGSHU_API_KEY')
```

## Real-World Workflow Example

### Complete campaign generation flow:

```python
import os
import json

# 1. Load knowledge base
def load_knowledge_base(category: str) -> str:
    path = f"knowledge-base/{category}/_index.md"
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 2. Load templates
def load_template(template_name: str) -> str:
    path = f"docs/templates/{template_name}.md"
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 3. Check used ideas for deduplication
def load_used_ideas() -> list:
    path = "docs/templates/used-ideas.md"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Extract hooks from markdown list
        import re
        hooks = re.findall(r'- \*\*(.+?)\*\*', content)
        return hooks

# 4. Generate campaign
def generate_campaign(product_spec: dict, platform: str):
    kb_data = load_knowledge_base(product_spec['category'])
    template = load_template('creative-output')
    used_hooks = load_used_ideas()
    
    prompt = f"""
    Knowledge Base:
    {kb_data}
    
    Template:
    {template}
    
    Already Used Hooks (avoid these):
    {used_hooks}
    
    Product Specs:
    {json.dumps(product_spec, ensure_ascii=False)}
    
    Target Platform: {platform}
    
    Generate 3 creative campaign ideas following the template.
    Ensure:
    1. Every number has a source citation
    2. No AI clichés (no "值得注意的是", "首先其次")
    3. Hooks are not in used_hooks list
    4. Include risk assessment for each idea
    """
    
    # Feed to your AI agent (Claude, GPT, etc.)
    return prompt

# 5. Usage
product = {
    'category': 'mobile',
    'name': 'SuperPhone X1',
    'chipset': 'Snapdragon 8 Gen 3',
    'price': 2499,
    'key_features': ['120Hz OLED', '5000mAh battery', '67W charging']
}

campaign_prompt = generate_campaign(product, 'Xiaohongshu')
# Send campaign_prompt to AI agent
```

### Risk assessment workflow:

```python
def assess_campaign_risk(campaign_text: str) -> dict:
    """
    Run multi-layer risk check on campaign content.
    """
    # Load personas
    personas_content = load_template('comment-personas')
    
    # Load historical failures
    kb_smart_home = load_knowledge_base('smart-home')
    failures = extract_case_studies(kb_smart_home)
    
    prompt = f"""
    Campaign Text:
    {campaign_text}
    
    Comment Personas (simulate negative reactions):
    {personas_content}
    
    Historical Failures (check for similar patterns):
    {failures}
    
    Assess risks in these dimensions:
    1. Technical credibility (can 参数党 debunk it?)
    2. Perception tricks (will 解构找茬 expose methods?)
    3. Platform compliance (content guidelines)
    4. Similar historical failures
    
    Output in risk-assessment.md template format.
    """
    
    return prompt

# Usage
risk_prompt = assess_campaign_risk(campaign_output)
```

## Common Patterns

### Pattern 1: Cross-Category Competitive Analysis

```python
def cross_category_comparison(product_a: dict, product_b: dict) -> str:
    """
    Compare products from different categories (e.g., phone vs tablet).
    Must ensure data sources are compatible.
    """
    kb_a = load_knowledge_base(product_a['category'])
    kb_b = load_knowledge_base(product_b['category'])
    
    # Verify data source compatibility
    source_a = extract_sources(kb_a, product_a['name'])
    source_b = extract_sources(kb_b, product_b['name'])
    
    if not sources_compatible(source_a, source_b):
        return "Error: Cannot compare - data sources not aligned (different test methodologies)"
    
    # Proceed with comparison...
```

### Pattern 2: KOL Ecosystem Integration

```python
def select_kols_for_category(category: str, budget: int) -> list:
    """
    Select KOLs based on category expertise and budget.
    """
    kol_db_path = "docs/ecosystem/kols.md"
    with open(kol_db_path, 'r', encoding='utf-8') as f:
        kol_data = f.read()
    
    # Extract KOLs for category
    import re
    kol_pattern = rf'\| (.+?) \| {category} \| (.+?) \| (.+?) \|'
    matches = re.findall(kol_pattern, kol_data)
    
    # matches = [(name, followers, estimated_cost), ...]
    affordable_kols = [k for k in matches if parse_cost(k[2]) <= budget]
    
    return affordable_kols
```

### Pattern 3: Meme/Jargon Validation

```python
def validate_campaign_language(text: str) -> list:
    """
    Check campaign text against industry meme database to avoid backfires.
    """
    meme_db = load_template('industry-memes')
    warnings = []
    
    # Load risky phrases
    risky_phrases = extract_risky_phrases(meme_db)
    
    for phrase in risky_phrases:
        if phrase in text:
            context = get_meme_context(meme_db, phrase)
            warnings.append({
                'phrase': phrase,
                'risk': context['risk_level'],
                'explanation': context['why_risky']
            })
    
    return warnings

# Usage
warnings = validate_campaign_language("我们的产品遥遥领先")
# Output: [{'phrase': '遥遥领先', 'risk': 'high', 'explanation': 'Huawei meme - used ironically'}]
```

## Troubleshooting

### Issue 1: "知识库暂无此数据" (No data in knowledge base)

**Cause:** Querying product/brand not in knowledge base

**Solution:**
```python
# Add data via preprocessing
python scripts/preprocess.py new_product_data.csv knowledge-base/

# Or manually create markdown file
# knowledge-base/mobile/new-brand.md
```

### Issue 2: Source Attribution Missing

**Cause:** Generated content lacks proper citations

**Fix:**
```python
# Add validation step
def validate_sources(content: str) -> bool:
    """Check if every claim has a source."""
    import re
    # Numbers without sources
    numbers = re.findall(r'\d+(?:\.\d+)?[%㎡mAh元]', content)
    sources = re.findall(r'\[来源:.+?\]', content)
    
    if len(numbers) > len(sources):
        raise ValueError(f"Found {len(numbers)} claims but only {len(sources)} sources")
    return True
```

### Issue 3: AI Clichés in Output

**Cause:** Template not enforcing de-AI rules

**Fix:**
```python
AI_CLICHES = [
    "值得注意的是", "首先其次最后", "我们可以发现",
    "不是A而是B", "在...背景下", "赋能", "生态"
]

def check_ai_language(text: str) -> list:
    """Detect AI clichés."""
    found = [phrase for phrase in AI_CLICHES if phrase in text]
    if found:
        print(f"Warning: AI clichés detected: {found}")
        print("Rewrite using colloquial language or data-driven statements")
    return found
```

### Issue 4: Data Source Conflicts

**Cause:** Mixing incompatible evaluation methodologies

**Example:**
```python
# Wrong: Comparing battery life from different test conditions
laptop_a_battery = "10 hours (PCMark 10 test)"
laptop_b_battery = "12 hours (video playback)"

# Fix: Flag as incomparable
def compare_metrics(metric_a: dict, metric_b: dict):
    if metric_a['test_method'] != metric_b['test_method']:
        return {
            'comparable': False,
            'reason': f"Different test methods: {metric_a['test_method']} vs {metric_b['test_method']}"
        }
```

### Issue 5: Missing Risk Flags

**Cause:** Campaign generated without persona simulation

**Fix:**
```python
def enforce_risk_check(campaign: str) -> str:
    """Mandatory risk assessment before finalizing campaign."""
    personas = load_template('comment-personas')
    
    if "[风险评估]" not in campaign:
        risk_section = generate_risk_assessment(campaign, personas)
        campaign += f"\n\n## 风险评估\n{risk_section}"
    
    return campaign
```

## Quality Checklist

Before finalizing any campaign output:

```python
QUALITY_CHECKS = {
    "数据纪律": [
        "✓ Every number has source citation",
        "✓ No fabricated statistics",
        "✓ Speculation labeled as [推测]",
        "✓ Competitive data from same source"
    ],
    "去AI化": [
        "✓ No '值得注意的是' phrases",
        "✓ No '首先其次最后' structures",
        "✓ No generic corporate jargon"
    ],
    "风险覆盖": [
        "✓ 5 personas simulated",
        "✓ Historical case studies checked",
        "✓ Platform compliance verified"
    ]
}

def run_quality_check(content: str) -> dict:
    """Run full quality validation."""
    results = {}
    for category, checks in QUALITY_CHECKS.items():
        results[category] = []
        for check in checks:
            # Implement validation logic for each check
            pass
    return results
```

## Advanced Usage

### Sub-Agent Integration

**DataProcessor Sub-Agent:**

```python
# Triggered by: "处理新数据"
def activate_data_processor(raw_data: str):
    """
    Sub-agent for data cleaning and validation.
    See: docs/references/subagent-dataprocessor.md
    """
    steps = [
        "1. 纠错 - Fix encoding, formatting",
        "2. 判断类型 - Classify data type (review/spec/comment)",
        "3. 清洗 - Remove ads, extract facts",
        "4. 提取 - Structured data extraction",
        "5. 更新索引 - Update knowledge base index"
    ]
    # Execute preprocessing pipeline
    return process_pipeline(raw_data, steps)
```

**FactChecker Sub-Agent:**

```python
# Triggered by: "帮我检查"
def activate_fact_checker(content: str):
    """
    Adversarial audit for generated content.
    See: docs/references/subagent-factchecker.md
    """
    checks = {
        "数据核验": verify_data_sources(content),
        "遗漏检测": check_missing_citations(content),
        "幻觉扫描": detect_fabrications(content),
        "逻辑一致性": validate_logic_chain(content)
    }
    return checks
```

## Knowledge Base Coverage

| Category | Completeness | Data Sources |
|----------|-------------|--------------|
| Mobile | ⭐⭐⭐ | 16 brands, chipset camps, price tiers |
| Earphones | ⭐⭐⭐ | 爱否科技 12-product clip-on review |
| Laptops | ⭐⭐⭐ | 笔吧 2025 guide, 8 price segments |
| Wearables | ⭐⭐⭐ | IDC 2025 market share, brand matrix |
| Smart Home | ⭐⭐⭐⭐ | 4 cross-referenced robot vacuum reviews, DJI ROMO case |

---

**License:** MIT  
**Repository:** https://github.com/killsnake01/China-Marketing-Copilot-Skill  
**Last Updated:** 2026-05-09
