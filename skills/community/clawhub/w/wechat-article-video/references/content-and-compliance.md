# Content And Compliance

## Contents

1. Article objective
2. Compression by mode
3. Compact-standard coverage
4. Evidence map
5. Medical and pharma rules
6. Voiceover style
7. Publish package

## Article Objective

Write one sentence before scripting:

```text
After watching, the intended viewer should ______.
```

Examples:

- 厂家完成免费入驻
- 行业用户进入小程序查看联系人
- 医学专业人士了解本期企业和重点品种

Keep no more than three supporting messages. Background that does not change the viewer's next action belongs in the article, not necessarily in the video.

## Compression By Mode

### Brief: 15-25 seconds

- one hook
- one or two benefits/facts
- one action

### Compact-standard: 30-40 seconds

- complete cover and one intended action
- company identity plus 1-2 strongest credibility facts
- material qualification/domain evidence
- every featured product, dosage form, and main indication/use
- differentiating specifications when material
- complete disclaimer
- normally 6-8 scenes, with 34-38 seconds preferred over unreadable compression

Treat this as a complete-information short version, not a brief teaser. Preserve key facts on screen even when only the core sentence is narrated.

### Standard: 40-75 seconds

- cover/hook
- company or event context
- two or three evidence/product beats
- platform action
- disclaimer when required

### Detail: 75-120 seconds

- clear chapter progression
- additional qualification, specification, or policy detail
- visual breathing beats between dense sections

Avoid reading dosage instructions, long specification lists, or every qualification unless the user explicitly wants a detailed professional explainer.

## Compact-Standard Coverage

Classify source claims as `critical`, `supporting`, or `article_only`. Add every critical claim ID to `critical_claim_ids` in `content-brief.json`. A compact-standard storyboard is invalid until every critical claim's source reference appears in at least one scene.

Do not reduce duration by dropping a featured product, removing its dosage form or main indication/use, omitting a material specification, deleting the CTA/disclaimer, shrinking text below readable sizes, or raising Edge TTS above `+20%`.

Reduce duration by shortening connective language, combining the platform CTA, and moving supporting facts from voiceover to the frame.

## Evidence Map

Use this shape for `content-brief.json`:

```json
{
  "title": "文章标题",
  "mode": "standard",
  "objective": "医学专业人士进入行业平台小程序查看联系人和更多信息",
  "audience": "医药行业及医学专业人士",
  "critical_claim_ids": ["c01"],
  "claims": [
    {
      "id": "c01",
      "text": "示例药企成立于2001年",
      "source_ref": "section-1-paragraph-1",
      "priority": "critical",
      "allowed_in_voiceover": true,
      "allowed_on_screen": true
    }
  ],
  "required_disclaimer": "仅供医学人士学习、交流使用，不具有任何商业用途",
  "cta": "点击行业平台小程序链接免费获取联系人及更多详细信息",
  "assets": [
    {
      "path": "source/images/company.jpg",
      "status": "ready",
      "subject": "企业厂区正门和办公生产建筑",
      "crop_safety": "safe",
      "risks": []
    }
  ],
  "production_status": "ready"
}
```

Every number, qualification, product name, indication, dosage, specification, exposure count, and platform promise needs a source reference. Image recognition may identify candidate text but is not a factual source.

Set `production_status` to `blocked` when any required supplied asset cannot be copied or visually inspected. A blocked content brief must not pass storyboard validation.

## Medical And Pharma Rules

- Preserve generic names, dosage forms, indications, specifications, and disclaimers exactly enough to remain faithful.
- Do not introduce words such as 治愈、根治、特效、最佳、绝对安全 unless the source explicitly and lawfully contains them.
- Do not convert professional indications into consumer treatment advice.
- Do not invent a hospital, formal notice, attachment, prescription requirement, or approval status.
- Keep the audience qualifier visible where the source limits use to medical professionals.
- When a product image is too small to read, do not infer packaging details from it.
- Separate platform CTA from product efficacy statements.

## Voiceover Style

- Use spoken Chinese, but keep facts conservative.
- Prefer short clauses and deliberate punctuation.
- Speak one information unit at a time.
- Read long numbers in a way that is easy to understand.
- Avoid exaggerated sales delivery for medical content.
- Keep one continuous Edge TTS render; do not synthesize each scene separately.
- For compact-standard, use `+12%` to `+20%`; prefer 35-38 seconds over faster speech.
- Let supporting facts remain visible without forcing them into narration.

## Publish Package

Create `publish-copy.md` containing:

- video title: usually 16-28 Chinese characters
- cover title: ideally no more than two lines and 18 Chinese characters
- 1-2 sentence post copy
- CTA
- required disclaimer
- relevant tags, kept restrained

The cover title is a click decision, not the full article title. It must identify the company/product or literal offer in the first viewport.
