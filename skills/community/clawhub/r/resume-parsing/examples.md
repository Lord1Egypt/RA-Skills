# Mapping examples: extracted markdown → JSON Resume

Two worked examples showing the semantic step. Input is what `extract.py`
produces (`.extract.md` body + `.extract.json` contacts); output is `resume.json`.

## Example 1 — English resume

**`.extract.md`**
```markdown
# Zhang Wei

Senior Backend Engineer  zhangwei@example.com | +86 138-0000-0000 | github.com/zhangwei

## Experience

ByteDance  Senior Backend Engineer  2020-03 to 2024-06 - Reduced settlement latency from 800ms to 120ms

## Education

Shanghai Jiao Tong University  BSc Computer Science  2012-2016
```

**`.extract.json` contacts** → emails `[zhangwei@example.com]`, phones
`[+86 138-0000-0000]`, profiles `[{network:GitHub, url:https://github.com/zhangwei}]`.

**`resume.json`**
```json
{
  "basics": {
    "name": "Zhang Wei",
    "label": "Senior Backend Engineer",
    "email": "zhangwei@example.com",
    "phone": "+86 138-0000-0000",
    "url": "https://github.com/zhangwei",
    "profiles": [{ "network": "GitHub", "url": "https://github.com/zhangwei" }]
  },
  "work": [
    {
      "name": "ByteDance",
      "position": "Senior Backend Engineer",
      "startDate": "2020-03",
      "endDate": "2024-06",
      "highlights": ["Reduced settlement latency from 800ms to 120ms"]
    }
  ],
  "education": [
    {
      "institution": "Shanghai Jiao Tong University",
      "studyType": "BSc",
      "area": "Computer Science",
      "startDate": "2012",
      "endDate": "2016"
    }
  ],
  "meta": { "version": "v1.0.0" },
  "x_parse": { "source": "zhang_wei.pdf", "columns": 1, "confidence": "high" }
}
```

Note: `2012-2016` split into year-only `startDate`/`endDate`; the bullet became a
`highlights` entry; contacts came straight from the sidecar.

## Example 2 — 中文简历(含"至今")

**`.extract.md`**
```markdown
# 李娜

产品经理 | 女 / 1993.05 | lina@example.com | 139-1234-5678 | 上海
期望职位:高级产品经理 | 期望城市:上海/杭州

## 工作经历

美团  高级产品经理  2021年6月 - 至今
- 负责到店业务增长,GMV 同比提升 40%

## 教育背景

复旦大学  市场营销  硕士  2018.09 - 2021.06
```

**`resume.json`**
```json
{
  "basics": {
    "name": "李娜",
    "label": "产品经理",
    "email": "lina@example.com",
    "phone": "139-1234-5678",
    "location": { "city": "上海", "countryCode": "CN" }
  },
  "x_personal": { "birthDate": "1993-05", "gender": "女" },
  "x_objective": { "positions": ["高级产品经理"], "locations": ["上海", "杭州"] },
  "work": [
    {
      "name": "美团",
      "position": "高级产品经理",
      "startDate": "2021-06",
      "highlights": ["负责到店业务增长,GMV 同比提升 40%"]
    }
  ],
  "education": [
    {
      "institution": "复旦大学",
      "area": "市场营销",
      "studyType": "硕士",
      "startDate": "2018-09",
      "endDate": "2021-06"
    }
  ],
  "meta": { "version": "v1.0.0" },
  "x_parse": { "source": "李娜.pdf", "columns": 1, "confidence": "high" }
}
```

Note: "至今" → **no** `endDate` (current role); `2021年6月` → `2021-06`;
`2018.09` → `2018-09`; values stay in Chinese, keys stay English. Personal info
(`女 / 1993.05`) and job objective went to the fixed `x_personal` / `x_objective`
namespaces rather than being dropped or given ad-hoc keys.
