# Session note: packaging gate, runtime clearing, and list/detail rendering requirements

## Context

The user corrected a run-0002 packaging mistake: the template was packaged even though required xz01 checks were incomplete. Reported failures included missing jQuery in the header, column URLs without trailing slashes, wrong rendered `cms/page/index/id/*` links, self-created filler SVG images used as data pictures, homepage data not materially rendered, and missing software/game list/detail page rendering.

## Durable rules

1. After every development change that adds, modifies, or deletes code/templates/CSS/JS/assets, validation must first clear the ThinkPHP runtime cache by deleting all directories/items under `/www/wwwroot/www.900az.com/runtime/`.
2. No template may be packaged as verified until PC and mobile homepage, relevant software/game list pages, and detail pages render correctly using database routes that actually exist.
3. Header jQuery loading is a required xz01 check for PC and mobile.
4. Rendered column links such as `/zoszx/`, `/zoszx01/`, `/zoszx02/`, `/zoszx03/` must end with `/`.
5. Rendered pages must not contain erroneous links such as `/cms/page/index/id/*` or generated `cms/Page/index` / `mobile/Page/index` URLs for fake/unroutable pages.
6. Templates must not use project-created filler images such as `/themes/default/common_cms/*/assets/images/app-*.svg`, `banner-*.svg`, or `topic-*.svg` as if they were data images. Use render expressions such as `cmf_get_image_url($vo.more.thumbnail)` for real data images. If no data exists, use honest text/style fallback without fake data pictures.
7. Validation must fail if pages are mostly placeholder `暂无...数据` blocks or have zero real content/detail links when the database contains usable records.

## Practical validation gate

Before packaging, test must verify at minimum:

- PC and mobile homepage HTTP 200, no `系统发生错误`.
- PC and mobile software/game list pages render with real data.
- PC and mobile detail pages render with real data.
- jQuery present in rendered head/output where required.
- known column links have trailing slash.
- no wrong `cms/page/index/id` links.
- no prohibited filler SVG data images in rendered HTML.
- mobile rendered HTML has no `target="_blank"`.
- screenshots + AI visual review are done after runtime clearing.

Packaging before this gate passes is a workflow failure.