# Session note: PC quick-topic gap repair via dev → test → rule loop

## Context

After the main-role boundary correction, the user reported a remaining small blank area under the PC homepage quick-topic card group:

- 装机必备清单 / 效率工具一键配齐
- 办公效率精选 / 文档扫描笔记同步
- 新游福利合集 / 礼包活动同步更新
- 下载避坑指南 / 认准安全版本渠道

The important learning was not only the visual tweak, but that the fix was handled through the correct xz01 role split instead of main directly editing implementation files.

## Correct workflow pattern

```text
user visual defect report
  -> Hermes main creates a precise dev task
  -> Claude Code dev performs the HTML/CSS/template repair
  -> independent test captures PC screenshot + AI visual review
  -> rule audits the role boundary and whether skill/spec updates are needed
  -> Hermes main summarizes
```

## Practical dev task shape

For small visible PC spacing defects, main should give Claude dev a constrained task with:

- device/domain: PC, `https://www.900az.com/`, desktop UA;
- exact visible symptom and text anchors;
- allowed files/run directories;
- hard boundaries: do not modify `/root/.openclaw`, do not modify `demo_xz01`, do not touch mobile unless requested;
- preserve existing modules unless the user asks for redesign;
- request changed-file summary and self-check notes.

Useful constrained repair pattern from this session:

- keep `下载排行 → 本周专题 → 专题推荐` intact;
- keep the left 4 quick-topic cards intact;
- compress PC-only spacing rather than redesigning the block:
  - reduce `.xz-hero-main` bottom padding;
  - reduce `.xz-triple-news` top spacing;
  - reduce `.xz-quick-row` top spacing;
  - slightly reduce `.xz-quick-card` height/padding;
  - if the user still points to the strip above `游戏活动`, tighten `.xz-triple-news` further (e.g. 10px→6px) and reduce right-sidebar vertical gap (e.g. `.xz-hero-side{gap:12px}`) so left/right column heights stop creating a visible pre-section shelf;
- sync deployment and generated CSS copies.

## Iterative user-visible gap handling

Do not stop at the first AI PASS if the user still identifies a visible leftover gap. Treat follow-up phrases like “还有一小截空白” as a new defect report and re-run the same dev → test → rule loop. Test may accept a *natural module interval*, but the dev prompt should explicitly target the text/module anchor the user named (`游戏活动` in this session) so the visual review checks the right strip rather than only the earlier quick-card area.

## Test acceptance pattern

Independent test should verify:

- HTTP 200 and no `系统发生错误`;
- screenshot at desktop PC viewport (around 1365×1800);
- AI visual review focused on the exact reported gap area;
- no button/text/decoration overlap;
- no right overflow, broken image, or debug overlay.

A small residual gap can pass if it visually separates sections naturally and no longer looks like an accidental blank defect.

## Claude Code orchestration note

For Claude Code print-mode delegation on xz01 implementation tasks, include enough read/navigation tools up front. Missing `Grep`/`Glob` can waste turns and cause permission denials. If Claude stops at `error_max_turns`, resume the same session ID and either continue with the missing tools allowed or ask for a no-edit summary of completed work.
