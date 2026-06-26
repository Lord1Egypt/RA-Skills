# Saju Interpreter Rules

This file captures the default rule set for rule-based 사주 해석. It is not meant to settle every school dispute. Its job is to keep outputs consistent, evidence-first, and non-gimmicky.

## 1. Input model

Assume already-derived pillars.

```json
{
  "pillars": {
    "year": {"stem": "庚", "branch": "午"},
    "month": {"stem": "己", "branch": "卯"},
    "day": {"stem": "辛", "branch": "未"},
    "hour": {"stem": "己", "branch": "亥"}
  }
}
```

Interpretation works on the given pillars. Calendar derivation is out of scope unless separately implemented.

## 2. Core model

Treat each branch as having three layers:

1. surface element / polarity
2. hidden stems list
3. seasonal force, especially for the month branch

Default hidden-stem ordering: **본기 > 중기 > 여기**.
If weights are needed, use a conservative default like `1.0 / 0.5 / 0.25`.

### Hidden stems default table

Use this pragmatic default table unless the user explicitly asks for another school.

| Branch | 여기 | 중기 | 본기 |
| --- | --- | --- | --- |
| 子 | 壬 | - | 癸 |
| 丑 | 癸 | 辛 | 己 |
| 寅 | 戊 | 丙 | 甲 |
| 卯 | 甲 | - | 乙 |
| 辰 | 乙 | 癸 | 戊 |
| 巳 | 戊 | 庚 | 丙 |
| 午 | 丙 | 己 | 丁 |
| 未 | 丁 | 乙 | 己 |
| 申 | 戊 | 壬 | 庚 |
| 酉 | 庚 | - | 辛 |
| 戌 | 辛 | 丁 | 戊 |
| 亥 | 戊 | 甲 | 壬 |

This table matches the common Korean/Chinese practical ordering found in summary references for 지장간. Keep the order stable; let the numeric weighting remain configurable.

## 3. Ten Gods decision rule

Given:
- `E_dm`: day master element
- `Y_dm`: day master polarity
- `E_x`: target element
- `Y_x`: target polarity

First classify the elemental relation:
1. `E_x == E_dm`
2. `E_dm -> E_x` (day master produces target)
3. `E_dm controls E_x`
4. `E_x controls E_dm`
5. `E_x -> E_dm` (target produces day master)

Then resolve same/other polarity:

| Relation from DM perspective | same polarity | different polarity |
| --- | --- | --- |
| same element | 비견 | 겁재 |
| DM produces target | 식신 | 상관 |
| DM controls target | 정재 | 편재 |
| target controls DM | 정관 | 편관(칠살) |
| target produces DM | 정인 | 편인 |

Use 십성 structurally first. Add personality language only after the structure is stable.

## 4. Priority order

Default order:

1. **월령 / 계절성**
2. **일간 / 일지 축**
3. **강한 삼합/방합 + 월지 왕지 조건**
4. **천간합/육합의 합화 성립 여부**
5. **충(沖)**
6. **형·해·파**
7. **신살**

Do not let a lower-priority layer overturn a higher-priority layer without explaining why.

## 5. Relation handling

Track these separately:
- relation detected
- relation strength
- transformation candidate
- transformation success/failure
- blockers or weakening factors

This matters most for 합.

### Minimum supported relations

- 천간합: 甲己, 乙庚, 丙辛, 丁壬, 戊癸
- 육합: 子丑, 寅亥, 卯戌, 辰酉, 巳申, 午未
- 삼합: 申子辰(水), 寅午戌(火), 巳酉丑(金), 亥卯未(木)
- 충: 子午, 丑未, 寅申, 卯酉, 辰戌, 巳亥
- 형/해/파: treat as friction/disruption layers unless the user requests a stricter school

### Practical default tables for 형·해·파

Use these as interoperable defaults. If the user requests a specific school, override explicitly instead of silently mixing systems.

#### 형(刑)

| Type | Members |
| --- | --- |
| 삼형 | 寅巳申 / 丑戌未 |
| 자형 | 子子, 卯卯, 辰辰, 午午, 酉酉, 亥亥 |
| optional strict handling | treat school-specific subcases as options, not defaults |

#### 해(害)

| Pair |
| --- |
| 子未 |
| 丑午 |
| 寅巳 |
| 卯辰 |
| 申亥 |
| 酉戌 |

#### 파(破)

| Pair |
| --- |
| 子酉 |
| 丑辰 |
| 寅亥 |
| 卯午 |
| 申巳 |
| 未戌 |

Operational rule:
- 충 = strongest direct change/conflict layer
- 형 = pressure, entanglement, repetition, internal friction
- 해 = obstruction, discomfort, hidden interference
- 파 = splitting, cracking, partial breakdown of an existing pattern

Do not let 형·해·파 overturn month-branch season logic by themselves.

### 합 vs 합화

Never collapse these into one step.

- `합 detected`: a relationship exists
- `합화 succeeded`: transformation conditions are strong enough
- `합화 failed`: keep the relation but do not rewrite the element map

If there is 쟁합, 요합, 중첩, or interference from stronger seasonal or clash structure, mark that explicitly.

### Default 합화 decision rule

Use a **strict default** rather than a generous one.

#### Step 1: detect the base pair

- 甲己 → 土 candidate
- 乙庚 → 金 candidate
- 丙辛 → 水 candidate
- 丁壬 → 木 candidate
- 戊癸 → 火 candidate

#### Step 2: require all of the following before marking `transformed`

1. the pair is actually present and not merely implied
2. the surrounding chart supports the target element
3. the month branch / season does not strongly oppose the target element
4. there is no stronger clash, contention, or blocking pattern breaking the pair
5. if multiple schools disagree, keep `combined-but-not-transformed` as the safer default

#### Step 3: downgrade when one of these appears

- 쟁합: one stem is pulled by multiple partners
- 요합: relation exists but lacks stable support
- month-branch season clearly favors another dominant flow
- nearby controlling or breaking structure interrupts the pair

Practical implementation rule:
- default to `not_transformed` unless the chart gives a clear reason to promote it
- explain *why* it was promoted or blocked
- do not rewrite the whole chart around 합화 without an explicit note

## 6. Johuu / climate layer

Judge 조후 in two steps.

### Step A: seasonal climate profile from month branch

- 寅卯辰: spring, tends toward rising moisture / growth
- 巳午未: summer, tends toward warmth / heat
- 申酉戌: autumn, tends toward dryness
- 亥子丑: winter, tends toward cold

### Step B: correcting resources in the full chart

Ask:
- If cold, where is warmth/fire support?
- If hot, where is cooling/water support?
- If dry, where is moisture/water support?
- If damp, where is drying/fire-earth support?

Use 조후 as a major interpretive layer, but do not force it to erase all other structure.

## 7. Strength / balance

When discussing 신강/신약:
- start from month branch and seasonal support
- then check visible stems/branches
- then hidden stems
- then relation adjustments

Do not reduce the whole reading to a single strength label if the chart has mixed signals.

## 8. Shinsal policy

Default: optional, low weight.

Use 신살 only when:
- the user asks for it, or
- it adds a small explanatory tag after structural reading

Do not let 신살 become the main explanation.
Do not use it for fear-based or deterministic claims.

## 9. Suggested output schema

```json
{
  "core": {
    "day_master": "辛",
    "month_branch": "卯",
    "season_profile": "spring-moist",
    "five_elements": {},
    "yin_yang_balance": {}
  },
  "relations": {
    "combinations": [],
    "clashes": [],
    "frictions": []
  },
  "ten_gods": {},
  "johuu": {
    "profile": "cool-damp",
    "needs": [],
    "notes": "season-first"
  },
  "shinsal": [],
  "reading": {
    "strengths": "",
    "risks": "",
    "work_style": "",
    "relationships": "",
    "practical": ""
  },
  "uncertainty": []
}
```

## 10. Pseudocode

```text
interpret_saju(pillars, options):
  validate pillars
  annotate stems/branches
  attach hidden stems if enabled
  judge month-branch season
  score elements and yin/yang
  compute ten gods from day master
  detect relations
  evaluate relation strength with month-branch weighting
  mark combination vs transformation
  judge day-master strength conservatively
  judge johuu
  optionally compute low-weight shinsal
  generate evidence-first reading
```

## 11. Source notes for defaults

These defaults were tightened using publicly accessible reference material and common practical tables, especially for:
- 지장간 ordering and common weight hierarchies
- 십간/십이지 base mappings
- practical 형·해·파 pair tables used in Korean saju summaries
- conservative handling of 천간합 vs 합화

Use them as stable engineering defaults, not as claims of one universally final school.

## 12. Tone rules

- Prefer conditional language.
- Mention school-dependent ambiguity when relevant.
- Avoid deterministic fate language.
- Treat this as structural interpretation, not prophecy.
