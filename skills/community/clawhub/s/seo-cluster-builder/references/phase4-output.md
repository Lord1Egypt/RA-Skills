# Phase 4 — Output Generation

Run after all article content and schema have been written and validated.

---

## Step 4.1 — HTML File Structure

The output is a single HTML file. Structure:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cluster: [Topic] – [N] Bài Viết | [domain]</title>
  <style>
    /* Paste contents of cluster-style.css here */
  </style>
</head>
<body>
<div class="page">

  <!-- 1. PAGE HEADER (.pg-hd) -->
  <!-- 2. AUDIT BOX (.audit) — pre-existing issues found in research -->
  <!-- 3. TABLE OF CONTENTS (.toc) — links to each article section -->
  <!-- 4. ARTICLE BLOCKS (.art) × N — one per article -->
  <!-- 5. SUMMARY BOX (.summary-box) — publish order + post-publish steps -->

</div>
<script>/* copy button JS */</script>
</body>
</html>
```

---

## Step 4.2 — Component Templates

### Page Header
```html
<div class="pg-hd">
  <h1>📝 Cluster: [Topic Name]</h1>
  <p>[N] bài viết đầy đủ — sẵn sàng copy vào WordPress · [domain]</p>
  <div class="stat-row">
    <div class="stat"><strong>[N]</strong>Bài viết</div>
    <div class="stat"><strong>1 Pillar</strong>+ [N-1] Cluster</div>
    <div class="stat"><strong>[N]</strong>Schema blocks</div>
    <div class="stat"><strong>[intent type]</strong>Mixed intent</div>
  </div>
</div>
```

### Audit Box (fill from Phase 1 research)
```html
<div class="audit">
  <h3>⚠️ Việc cần làm TRƯỚC khi đăng bài mới</h3>
  <ul>
    <li><strong>[Action]:</strong> [Description with specific URLs]</li>
    <!-- One item per pre-existing issue found in research -->
  </ul>
</div>
```

### Table of Contents
```html
<div class="toc">
  <h3>Danh sách [N] bài viết</h3>
  <ol>
    <li><a href="#bai1">PILLAR — [Title]</a> · <code>/[slug]/</code></li>
    <li><a href="#bai2">[Title]</a> · <code>/[slug]/</code></li>
    <!-- ... -->
  </ol>
</div>
```

### Article Block
```html
<div class="art" id="bai[N]">

  <!-- Article header -->
  <div class="art-hd">
    <div class="art-num">[N]</div>
    <div class="art-meta">
      <h2>[PILLAR / Article title]</h2>
      <div class="url-tag">[domain]/[slug]/</div>
      <div class="kw-tag">Từ khóa chính: [primary kw] | Phụ: [secondary kws]</div>
      <span class="priority p1">Ưu tiên 1</span>
      <!-- Add .merge badge if merging from existing articles -->
    </div>
  </div>

  <!-- SEO Meta Tags (copyable) -->
  <div class="meta-box">
    <div class="meta-box-hd">SEO Meta Tags <button class="copy-btn" onclick="copyEl(this)">Copy</button></div>
    <pre>Title tag (≤60 ký tự):
[title tag]

Meta description (150–160 ký tự):
[meta description]

URL slug: [slug]
Category: [category]
Tags: [tag1], [tag2], [tag3]
Featured image alt: [alt text]</pre>
  </div>

  <!-- Schema Markup (copyable) -->
  <div class="meta-box">
    <div class="meta-box-hd">Schema Markup — dán vào &lt;head&gt; <button class="copy-btn" onclick="copyEl(this)">Copy</button></div>
    <pre>[all schema blocks wrapped in &lt;script type="application/ld+json"&gt; tags]</pre>
  </div>

  <!-- Article Content (copyable) -->
  <div class="content-box">
    <div class="content-box-hd">Nội dung bài viết — copy vào WordPress <button class="copy-btn" onclick="copyEl(this)">Copy</button></div>
    <div class="content-area">
      [article HTML content]
    </div>
  </div>

  <!-- Internal Link Map (reference only — not copyable) -->
  <div class="il-map">
    <strong>🔗 Internal Link Map — Bài [N] cần link đến:</strong><br>
    → <code>/[target-slug]/</code> (anchor: "[anchor text]")<br>
    → <code>/[target-slug-2]/</code> (anchor: "[anchor text 2]")
  </div>

</div>
```

### Summary Box (bottom of file)
```html
<div class="summary-box">
  <h3>✅ Tóm tắt cluster — Thứ tự đăng và việc cần làm</h3>
  <ol>
    <li><strong>Trước khi đăng:</strong> [Redirect/merge instructions]</li>
    <li><strong>Tuần 1:</strong> Bài [N] (Pillar) + Bài [N] ([type]) + ...</li>
    <li><strong>Tuần 2:</strong> Bài [N] ([type]) + ...</li>
    <li><strong>Sau khi đăng:</strong> Request indexing tất cả [N] URL trong Google Search Console</li>
    <li><strong>Update trang cũ:</strong> Thêm internal link từ [old article] → [new pillar]</li>
  </ol>
</div>
```

### Copy Button JavaScript
```html
<script>
function copyEl(btn) {
  const box = btn.closest('.meta-box, .content-box');
  const el = box.querySelector('pre, .content-area');
  const text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = '✓ Copied!';
    btn.classList.add('ok');
    setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('ok'); }, 2200);
  }).catch(() => {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    btn.textContent = '✓ Copied!';
    btn.classList.add('ok');
    setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('ok'); }, 2200);
  });
}
</script>
```

---

## Step 4.3 — Final Validation Script

Run this Python script after generating the HTML file:

```python
from bs4 import BeautifulSoup
import json, re, html as htmllib

content = open('cluster-[topic].html').read()
soup = BeautifulSoup(content, 'html.parser')

# Define article IDs and labels
articles = [('bai1','PILLAR'), ('bai2','Article 2'), ...]  # fill in

# Skip these hrefs when counting internal links
skip = {'chude', 'shop', 'zalo', 'tel:', 'cua-hang'}

errors = []
print("=== VALIDATION REPORT ===\n")

for art_id, label in articles:
    art = soup.find('div', {'id': art_id})
    ca = art.find('div', {'class': 'content-area'})

    # Check internal links in body
    internal = [
        a for a in ca.find_all('a', href=True)
        if '[domain]' in a['href']
        and not any(s in a['href'] for s in skip)
    ]
    if len(internal) < 3:
        errors.append(f"{label}: only {len(internal)} internal links (need ≥3)")
    print(f"  {'✅' if len(internal) >= 3 else '❌'} [{label}] — {len(internal)} internal links")

# Check schema validity
pre_blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL)
schema_ok = 0; schema_errors = []
for block in pre_blocks:
    decoded = htmllib.unescape(block)
    for s in re.findall(r'<script type=[^>]+>(.*?)</script>', decoded, re.DOTALL):
        try:
            json.loads(s.strip())
            schema_ok += 1
        except Exception as e:
            schema_errors.append(str(e))

print(f"\n  Schema: {schema_ok} valid, {len(schema_errors)} errors")
if schema_errors:
    for e in schema_errors: print(f"    ERROR: {e}")

print(f"\n  Total errors: {len(errors) + len(schema_errors)}")
if not errors and not schema_errors:
    print("  ✅ ALL CHECKS PASSED")
```

**Minimum passing criteria:**
- All articles: ≥3 internal links in body
- All schema JSON: valid (0 parse errors)
- Pillar: links to all cluster articles
- All articles: have Article + FAQPage + BreadcrumbList schema

---

## Step 4.4 — Output Checklist

```
☐ File named: cluster-[topic-slug].html
☐ CSS from cluster-style.css inlined in <style>
☐ Audit box filled with pre-existing issues from Phase 1
☐ Every article has: meta-box (SEO tags) + meta-box (schema) + content-box
☐ Every article has: il-map with full link targets
☐ Copy buttons work (test copyEl function)
☐ Summary box has publish order + post-publish steps
☐ Validation script run: 0 errors
☐ File presented to user via present_files tool
```

---

## Step 4.5 — Deliver to User

1. Run validation (Step 4.3)
2. Copy file to `/mnt/user-data/outputs/cluster-[topic-slug].html`
3. Call `present_files` with the file path
4. Report: "X bài viết · Y schema blocks valid · Z internal links verified"
5. Tell user the 3 most important actions to take before publishing (from audit box + summary box)
