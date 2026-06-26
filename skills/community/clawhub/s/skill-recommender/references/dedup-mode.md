# Dedup / Avoid-Rebuild Mode

Use this mode when the user is about to create a new skill and wants to know whether similar skills already exist.

## Goal

Prevent unnecessary duplicate skill development.

## Questions to answer

1. Is there already a direct-match skill?
2. Are there several overlapping skills that together already cover the request?
3. Is the new request only a small extension of an existing skill?
4. Should the user:
   - reuse an existing skill
   - extend an existing skill
   - merge several overlapping skills
   - create a new skill anyway

## Decision labels

- `reuse-existing`
- `extend-existing`
- `merge-overlap`
- `build-new`

## Strong duplicate signals

- same platform + same action pattern
- same user problem + only naming differs
- same inputs and outputs, minor workflow differences only
- one new request looks like a browser upgrade of an existing domain skill

## Response pattern

- 用户要做什么
- 已有最相近 skills
- 重叠点
- 缺口点
- 结论：复用 / 扩展 / 合并 / 新建
