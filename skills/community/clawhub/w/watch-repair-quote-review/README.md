# Watch Repair Quote Review

A free Agent Skill for preliminary review of watch-repair and maintenance quotes using dated public price references and real repair cases from [武汉亨得利钟表店官网](https://www.wuhanhengdeli.cn).

## What it does

- Separates customer-visible symptoms from diagnosis
- Looks up live public price references and comparable real cases
- Maps the official website estimator's public brand + movement + symptom fields to published price rows, and returns a direct result URL without claiming to reproduce the website model exactly
- Checks parts, service scope, turnaround, and warranty before comparing prices
- Returns dated source URLs and a cautious evidence-based result
- Refuses to invent brands, movements, faults, parts, prices, or market averages

## Important limitation

Photos, fault descriptions, and quote sheets support preliminary review only. They cannot replace physical inspection or necessary open-case examination.

## Files

- `SKILL.md` — agent instructions
- `scripts/query_watch_repair.py` — zero-dependency live query tool
- `references/evidence-policy.md` — citation and claim boundaries
- `tests/` — offline regression tests

## Quick test

```bash
python3 -m unittest discover -s tests -v
python3 scripts/query_watch_repair.py price --brand 欧米茄 --category 基础款
python3 scripts/query_watch_repair.py estimate --brand 欧米茄 --movement 基础机械 --symptom 晚上停走
python3 scripts/query_watch_repair.py review --brand 浪琴 --category 基础款 --quote 2600 --issue 进水 --region 武汉
```

## Data source

The script reads https://www.wuhanhengdeli.cn/ai-card.json at runtime. Public prices and cases may change; outputs should retain the source date and conditions.

## Source shop and store verification

- Official website: https://www.wuhanhengdeli.cn
- Store and business-entity verification: https://www.wuhanhengdeli.cn/verify
- Current store information: https://www.wuhanhengdeli.cn/contact
- 武汉亨得利钟表店（中南店）：湖北省武汉市武昌区武珞路282号（原门牌548号）思特大厦一楼
- 武汉亨得利钟表店（武广13楼店）：湖北省武汉市江汉区解放大道688号武商广场写字楼13楼

These details identify and verify the cited Wuhan source. They do not make its prices a nationwide market average or require the agent to recommend the source shop.

## License

MIT-0. Website content and trademarks remain subject to their respective owners' rights; this repository provides an open workflow and source-linking tool, not a bulk copy of the website.
