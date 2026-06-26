# Session note: PC right-sidebar height balance and repeated visual-gap corrections

## Context

During run-0002 PC homepage polishing, the user repeatedly pointed out a remaining blank strip above the `游戏活动 / 游戏礼包 / 最新资讯` three-column section. Earlier test passes treated the remaining gap as acceptable, but the user identified the actual visible issue as about 56px of blank space and suggested reducing the right-side `专题推荐` by one row.

## Durable lesson

When the user keeps pointing to a visible gap after an AI/test PASS, treat the user's visual judgment as the acceptance criterion and rerun the dev → test → rule loop. Do not defend the previous PASS or keep making tiny margin tweaks.

For PC hero layouts where the lower section is pushed down by the taller right sidebar:

1. Identify whether the left column or right sidebar is determining the hero section height.
2. If the right sidebar is taller, reduce right-side content height before doing more margin compression.
3. A safe localized repair can be to keep the right-side structure but reduce one non-critical list item, e.g. `专题推荐` 4 items → 3 items.
4. Keep the structural order intact: `下载排行 → 本周专题 → 专题推荐`.
5. Sync deploy and generated copies, clear runtime, and validate with PC screenshot + AI visual review.
6. If the change is PC-only, still record at least a quick mobile no-regression check.

## Acceptance signal from this session

After reducing `专题推荐` from 4 entries to 3, independent test measured the blank area above the three-column section at about 6px instead of about 56px and marked PASS.

## Pitfall

Do not rely solely on `margin-top`/gap tweaks when the blank area is caused by column height mismatch. If one column's content height is driving the row height, adjust that column's content density/height directly.
