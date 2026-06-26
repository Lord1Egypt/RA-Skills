---
name: saju-interpreter
description: Interpret East Asian Four Pillars / Saju charts from already-derived pillars (year, month, day, hour stems/branches). Use when the user asks for 사주, 사주팔자, 명리, 팔자, 십성, 조후, 합충형해파, 신강약, 일간, 용신 discussion, or wants a rule-based reading from known pillars such as 경오년 기묘월 신미일 기해시. Prefer this skill for interpretation, not calendar derivation; assume the four pillars are already given unless the user explicitly asks for calendar conversion.
---

# Saju Interpreter

Interpret 사주팔자를 **evidence-first**. Start from structure, then explain meaning. Do not jump straight to fortune-teller prose.

This skill is intentionally calm and non-gimmicky:
- prefer structure over theatrical fortune-teller language
- prefer conditional claims over deterministic prophecy
- prefer explanation over intimidation
- treat people as more complex than one neat label

## Quick workflow

1. Normalize the input into four pillars.
   - Year / Month / Day / Hour
   - Each pillar = stem + branch
2. Treat **pillar derivation** and **pillar interpretation** as separate tasks.
   - If the user already gives pillars, do not re-derive them.
   - If the user gives birth date/time, use `scripts/calculate-pillars.py` for a first-pass calculation.
   - Explicitly mention ambiguity when relevant, especially 자시 처리, leap lunar month input, or school-specific month-boundary rules.
3. Analyze in this order:
   - **월령 / 계절성**
   - **일간 / 일지 축**
   - **오행 분포 + 음양 밸런스**
   - **십성 분포**
   - **합·충·형·해·파 / 삼합·육합**
   - **조후(한난조습)**
   - **신살** only as optional low-weight tags
4. Separate:
   - relationship detected
   - relationship strength
   - transformation success/failure
5. Write the interpretation in layers:
   - structural findings
   - conditional meaning
   - practical reading
   - uncertainty / school-dependent branches

## Output style

Use calm, conditional language.

- Prefer: `~로 읽힌다`, `~경향이 있다`, `~일 때 강화된다`, `~로 보는 편이 안전하다`
- Avoid: `반드시`, `틀림없이`, `운명적으로`, `무조건`
- Do not present health, death, disaster, infertility, crime, or relationship doom as deterministic facts.
- Do not let 신살 overrule structure.

## Default interpretation policy

Use these defaults unless the user asks for a different school.

- **Priority 1:** 월령(월지)와 계절성
- **Priority 2:** 일간 기준 십성/신강약의 기본 축
- **Priority 3:** 강한 삼합/방합 구조와 월지 가중
- **Priority 4:** 합 발견 후 합화 성립 여부 별도 판정
- **Priority 5:** 충은 강한 변동 요인으로 반영
- **Priority 6:** 형·해·파는 보정층으로 반영
- **Priority 7:** 신살은 보조 태그만 허용

## Reading checklist

Before writing the final reading, verify:

- Did I identify the **day master** correctly?
- Did I anchor the reading in **month branch / season**?
- Did I distinguish **same-element support** from **actual usable balance**?
- Did I separate **합** from **합화**?
- Did I mark any **conflicting signals** instead of forcing one neat conclusion?
- Did I keep **신살** below structure?

## What to read when needed

Read `references/rules.md` when you need the detailed rule specification, including:
- 십성 decision rules
- 조후 defaults
- relation priority model
- interpretation pseudocode
- example output shape

## Response template

Use a compact structure like this unless the user asks for a freer reading:

```markdown
## 기본 구조
- 일간:
- 월령/계절:
- 눈에 띄는 오행:

## 관계와 포인트
- 합/충/형/해/파:
- 십성 분포 핵심:
- 조후 포인트:

## 해석
- 강점:
- 부담/리스크:
- 관계/일 방식:
- 실용 코멘트:

## 단서
- 학파나 가중치에 따라 달라질 수 있는 부분:
```

## Boundaries

- Do not pretend there is one universally correct school.
- Do not silently invent missing pillars.
- If a pillar or birth-time assumption is uncertain, say so explicitly.
- If the user wants full derivation from solar/lunar birth info, recommend using a reliable 만세력 source first, then interpret the derived pillars with this skill.
ith this skill.
