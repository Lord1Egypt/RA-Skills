# Storyline Render Template

Produce all three outputs unless the user asks for less:

- markdown
- html
- json

## Output separation

Use this discipline:

- JSON: machine-readable structure
- Markdown: portable reading version
- HTML: polished visual version

Do not let HTML or Markdown inherit raw working-note language from your internal drafting steps.

## Trunk card

Each trunk card should contain:

- trunk title
- why this trunk matters
- core storyline paragraph

Voice:

- match the trunk domain
- macro trunks can be analytical
- hobby trunks should sound like they belong to that subculture, not like policy briefs

## Title rule

The trunk title is the name of the line, not the explanation of the line.
Prefer compact noun phrases.
Do not use self-talk, rhetorical flourishes, or overlong commentary as the title.

Good:

- `EVA 30 周年商品与内容热度延续`
- `FGO 新章预热与 Fate 周边节奏`
- `初夏温泉旅宿上新`

Bad:

- `EVA 30 周年这一波还在接力，不是零散周边，是整套热度延长线`
- `T1. ACG 与二创生态：授权、AI 生成、同人流通同时加速`
- `T3-B2 路 PLAVE：虚拟偶像从演唱会走向影院纪录片`

Those are too process-heavy, too thesis-like, or too self-explanatory for a stable tree label.
The title should name the line, not narrate your workflow.

## Branch block

For each branch:

- branch title
- branch type
- short rationale for why it hangs under this trunk
- merged timeline

Branch title rule:

- keep it shorter and more label-like than the rationale
- the rationale does the explaining
- do not include route markers, search markers, or notebook-style prefixes

Branch types may include:

- structural_driver
- market_validation
- policy_signal
- military_signal
- fandom_release_cadence
- merch_collab_line
- creator_or_event_line
- product_line_evolution
- destination_experience_line

## Timeline item format

- `YYYY-MM-DD | 事件标题`
- one short body line
- `source: known_pool` or `source: topic_top` or `source: syft_search_primary` or `source: syft_search_secondary`

The source label belongs in a small chip or a muted footer.
It does not belong inside the sentence itself.

## Language rule

The event title and body should read as natural Chinese.
Avoid note-fragment style.
Avoid translationese.
Avoid model self-talk.

Weak:

- `《序》CGI 制作秘话再被翻出来讲`

Better:

- `《序》的CG制作内幕再度成为周年讨论焦点`
- `《序》幕后制作往事又被周年节目重新带热`

Bad:

- `thin：本轮没有形成强证据`
- `topic top 路`
- `targeted search 路`
- `该条说明了……`
- `这条补上的是……`

The final render is not a lab notebook.
It should read like an edited reader-facing artifact.

## Tree quality rule

The tree should make relationships clearer than the flat briefing.
If a trunk or branch does not improve clarity, remove or merge it.
If a hobby item is clearly relevant but too thin for a branch, keep it visible in a small appendix instead of deleting it.

## HTML note

If you render HTML:

- use one timeline column per branch
- distinguish source types by color or chip label
- keep chronological order visually obvious
- add a compact appendix for `interest_watch` or `orphan_interest_highlights`
- use one coherent warm editorial style, not a bare utility dashboard
- avoid tiny default cards, harsh blue enterprise styling, or debug-table aesthetics

Canonical page feel:

- soft warm background
- rounded cards
- restrained shadows
- readable spacing
- strong hierarchy between hero / trunk / branch / appendix

The HTML should feel like a polished reading product, not a developer dump.
Save the final HTML as UTF-8 and do a quick visible-text sanity check before delivering.

## JSON note

Use a simple shape like:

```json
{
  "date": "2026-05-15",
  "trunks": [
    {
      "id": "T1",
      "title": "string",
      "why_it_matters": "string",
      "summary": "string",
      "branches": [
        {
          "id": "T1-B1",
          "title": "string",
          "branch_type": "market_validation",
          "rationale": "string",
          "timeline": [
            {
              "date": "2026-05-14",
              "title": "string",
              "body": "string",
              "source": "known_pool"
            }
          ]
        }
      ]
    }
  ],
  "orphan_interest_highlights": [
    {
      "interest_axis": "Fate",
      "title": "string",
      "why_it_still_matters": "string"
    }
  ]
}
```

## Final render discipline

The final visible outputs must not expose:

- query wording
- retrieval route names
- thin / discard note labels
- debug counters inside prose
- internal triage jargon

All of that belongs in working notes only.
