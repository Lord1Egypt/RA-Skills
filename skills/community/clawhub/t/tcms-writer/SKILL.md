---
slug: tcms-writer
displayName: Tcms Writer
name: tcms-writer
version: "1.3.3"
not_for:
  - Social posts, short content, or channel adaptation (use an adaptation skill)
  - Neutral third-party industry research (use a deep-dive pipeline skill)
  - Publishing or distributing the draft (stops at first draft + review package)
  - Writing without a content brief or source knowledge base
description: |
  For tech-product marketing teams — turns a product knowledge base into brand-side long-form drafts (blogs, case studies, product write-ups), not third-party analysis.
  Produces only 1500-3000 word long-form drafts from a content brief; does not handle social posts, short content, or channel adaptation.
  Not for neutral industry research — use industry-deep-dive-pipeline for that.
description_zh: "技术产品营销写作器：面向技术产品营销团队，将产品知识库转化为品牌侧长文草稿（博客、案例、产品稿），仅产 1500-3000 字长文，不做社媒短文或渠道适配。"

read_when:
  - 写文章
  - 写稿
  - 写初稿
  - 起草
  - 技术博客
  - 品牌技术稿
  - 案例文章
  - 客户案例
  - 产品解读
  - 产品稿
  - 新闻稿
  - content brief
  - draft
  - 按brief写
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - web_fetch
  - search_content
  - search_file
  - list_dir
metadata:
  openclaw:
    tags:
      - content-marketing
      - tech-product
      - writing
      - copywriting
      - b2b
      - brand-marketing
      - tech-blog
      - long-form
disable: false
---

# Content Writer

Produces high-quality long-form first drafts from a product knowledge base, brand guidelines, and a content brief.

## Operating mode: prompt chaining

Executes in fixed steps; each step has clear inputs and outputs.

---

## Step 1: Confirm the topic [deterministic]

Read the topic information provided by the user and confirm the following elements:

| Element | Must be clear | If missing |
|---------|---------------|------------|
| Article type | tech blog / customer case / product update | ask the user |
| Target product | specific product name | ask the user |
| Target reader | architect / CTO / engineer / analyst | default "technical decision-maker" |
| Core message | the key value point to convey | extract from knowledge base |
| Source material | knowledge base / internal material / published article | default knowledge base |
| Confidentiality | whether internal cases need redaction | default full redaction |

If the user provides a brief file path, read the brief directly.

---

## Step 2: Read source material [deterministic]

**Read only files related to the target product; do not load unrelated product information:**

1. **Product knowledge base** → search the target product's section (don't read in full; use `search_content` to locate)
2. **Brand guidelines** → `references/brand-rules.md` (read every time)
3. **Article templates** → read the template matching the article type:
   - tech blog: `references/templates/tech-blog.md`
   - customer case: `references/templates/case-study.md`
   - product update: `references/templates/product-update.md`
4. **Supplementary material** (as needed): internal docs or published articles specified in the brief

> The paths above must be configured per the actual project directory.

---

## Step 3: Writing [LLM]

### Writing rules

**Product names:**
- First mention uses the official full name (see the product-name mapping table in `brand-rules.md`)
- Subsequent mentions may use the short name

**Brand presence:**
- Title includes the brand name or the specific product's official name
- Introduce the brand or specific product within the first two paragraphs
- Fixed brand format at the end

**Data citations:**
- All data must come from the knowledge base or published articles; never fabricate
- Record the source when citing (used to build the citation table in Step 5)

**Customer information:**
- Customer cases from internal sources are **redacted by default**
- Redaction format: "a {industry} {company-scale} company"
- Never show the customer's company name, internal staff names, or project code names
- Use the real customer name only when the user has explicitly confirmed authorization

**Competitor handling:**
- Never name any competitor directly
- Use substitute phrasing such as "a peer platform"

**Product-capability source verification:**
- Cite only capabilities that exist in the knowledge base
- If unsure whether something is publicly released, mark it "needs confirmation" in the pre-review checklist

### Expression red lines (writing discipline for tech-product marketing copy; converged from multiple revision rounds and the three-piece governance line — must not be violated)

1. **No meta-language / self-reference.** Delete any sentence that steps outside the article to talk about its own structure — e.g. "this article…", "the press release makes it clear that…", "deserves its own section", "back to the overall narrative", "as mentioned in the published draft", "the next section will…". Transition with the content facts directly.
2. **No business-jargon four-character slogans.** Slogans like "多、快、好、省" (many/fast/good/cheap) must be rewritten in engineering dimensions: load coverage / execution efficiency / operations experience / resource efficiency.
3. **No absolutist phrasing.** Words like "naturally connected", "seamless", "inevitable", "certain", "zero" must be replaced with bounded qualifiers (e.g. "permissions and lineage inherit uniformly with the table object, reducing cross-engine re-authorization and fragmentation").
4. **Naming consistency (P0).** A product's external name must match the already-published authoritative materials of the same campaign (press release / official site / official account) verbatim; the tech blog must not add its own version number or suffix (e.g. if the external name is uniformly "X", the blog must not write "X 2.0"); naming within the same campaign must be byte-for-byte consistent.
5. **Faithful transcription vs quantified claims.** Infrastructure capabilities (e.g. a specific networking/storage technique) may be stated as-is if backed by an architecture diagram or published material; but quantified speedup multiples (e.g. "X accelerates N times") must not be written without an official figure — use qualitative phrasing instead.

### English AI-signature and author-authority gate [mandatory for English drafts]

This section is the TCMS application of the canonical rule source `tech-writing-pipeline/references/english-ai-writing-strategy.md`. Load that reference when it is available; do not create a separate word blacklist or detector-based score. This gate supplements, and does not replace, the product, brand, customer, competitor, naming, and knowledge-base rules above.

1. **Build the claim map before drafting.** For an English draft, record `Claim / Evidence / Counterargument / Boundary / What the reader should not infer` in English before writing the prose. The English version is a rewrite with an English-native argument order, not a sentence-by-sentence translation from Chinese.
2. **P0 hard stops.** Stop and return to the brief or source material when the draft contains fabricated evidence, numbers, quotes, relationships or attribution; a generic opening or conclusion carrying the main information; a claim supported only by positive adjectives; an attribution such as `studies show` or `experts believe` without a checkable source; a counterargument that is mentioned but not evaluated; or Chinese parallelism and media phrasing carried directly into the English draft.
3. **P1 review triggers.** Send the draft to human review when style vocabulary clusters in one paragraph, repeated `not just X but Y` or similar contrast templates appear, em dashes or identical triads become rhythmic scaffolding, or positive language grows without a matching object, source, measurement or condition. A single style word is not a failure.
4. **Human-authority pass.** For each major paragraph, identify the concrete object, event, number or observed behavior; the sentence the author is willing to stand behind; the strongest plausible objection; the response to that objection; and the condition that would narrow or falsify the claim.
5. **Channel-aware interpretation.** A LinkedIn object list, responsibility list, fact-bearing triad or structural motif is not an AI-signature finding by itself. Escalate only when channel structure combines with empty framing, source non-adjudication, missing author judgment or repeated rhetorical packaging. Detector scores are optional observations and never a publication PASS/FAIL gate.

### Article structure

Do not write: feature 1 → feature 2 → feature 3 (a product spec sheet).

Do write: **problem → why it's hard → solution (naturally introducing product capability) → effect → applicability judgment**.

Every article must leave the reader with a clear takeaway — a judgment they can make, or a method they can learn.

### Word count

Target 1500-3000 words. Compress if over 3500; supplement if under 1200.

---

## Step 4: Self-check [LLM]

| Check | Pass criterion | If fail |
|-------|----------------|---------|
| Customer-name leak | no customer name in internally-sourced cases | immediately replace with redacted version |
| Competitor naming | no competitor company name | replace |
| Product-name规范 | first mention uses official full name | fix |
| Brand presence | present in title / opening / closing | supplement |
| Data has source | every number points to a knowledge-base entry | delete unsourced data |
| Title anchor | headline carries a concrete anchor (who/scenario/problem); no abstract or filename-style titles | rewrite title |
| Internal code name | no undisclosed product code name / feature name | delete |
| English claim map | English drafts include Claim / Evidence / Counterargument / Boundary / What the reader should not infer | stop and rebuild the map |
| English author authority | every major paragraph has a concrete object, owned judgment, objection, response and boundary | human review |
| English AI-signature combination | no P0; P1 combinations are reviewed in context, not by single-word blacklist | stop or revise |
| Word-count range | 1500-3000 words | adjust |

---

## Step 5: Output [deterministic]

Produce two files:

**File 1: article first draft**
Path: `content/drafts/YYYY-MM-{product}-{topic-short}.md`

**File 2: citation-traceability table + pre-review checklist**
Path: same directory, filename with `-review` suffix

```markdown
## Execution summary
- Source material read: [list actual files read]
- Template chosen: [article type]
- Article word count: [actual]
- Cited data points: [N] ( [M] public, [K] internal redacted)
- Self-check: 11 checks, [X] passed [Y] fixed

## Citation traceability

| Data point in text | Knowledge-base entry / source | Public status |
|--------------------|------------------------------|---------------|
| "xxx" | xxx entry / source article | ✅ public / 📋 internal (redacted) |

## Pre-review checklist

- [ ] Customer-name redaction check
- [ ] Product-capability public-status check
- [ ] Data points PM needs to confirm
```

---

## Hard rules

1. **Never fabricate data.** Don't write numbers without a source.
2. **Internal cases are redacted by default.** Unless the user has explicitly confirmed authorization.
3. **Never name competitors.**
4. **Product names follow the official site.**
5. **Don't cite product capabilities not in the knowledge base.** Mark uncertain ones "needs confirmation".
6. **Every article must attach a citation-traceability table.**
7. **Don't promote products whose external messaging is unconfirmed.**
8. **Expression red lines are non-negotiable** (see the "Expression red lines" subsection in Step 3): no meta-language/self-reference, no business-jargon four-character slogans, no absolutist phrasing, naming consistency (P0 — external name follows the same-campaign published materials, no version-number suffix), faithful transcription vs quantified claims. Must be followed while writing; issues of the same kind found in pre-publication audit count as a miss by this Skill.
9. **English drafts must pass the English AI-signature and author-authority gate**: claim map before drafting, P0 hard stops, contextual P1 review, concrete author judgment, counterargument handling and evidence boundaries. Do not replace this gate with a banned-word list or detector score.

---

## Failure handling

| Scenario | Handling |
|----------|----------|
| Target product not found in knowledge base | stop generation, report "no information on {product} in knowledge base" |
| Brief requests an article type with no template | use tech-blog template as default |
| Cited data marked "expired" | don't cite; flag in pre-review checklist |
| Customer authorization status unclear | default redaction |
| Article over 3500 words | give compression suggestions |
| Core message not derivable from knowledge base | stop and ask the user to supply the key value point; never invent one |

---

## ⚠️ Human-in-the-loop

After output, the article enters **human review**. This Skill does not auto-publish; every first draft must be confirmed by a human before entering `content-adapter` for channel adaptation.

---

## 中文摘要

Content Writer 是面向品牌营销的长文创作 Agent：基于产品知识库、品牌规范与选题 Brief，产出 1500–3000 字的技术博客、客户案例或产品解读初稿（不含社交帖与渠道适配）。写作严守五条表达红线（禁用元语言/自我指涉、禁用商务腔四字总结、禁止绝对化表述、P0 命名一致性、忠实转录 vs 量化断言）；内部客户案例默认脱敏、不点名竞品、所有数据须有出处并附引用追溯表。初稿完成后进入人工 review，不自动发布。
