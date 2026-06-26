# Session lesson: pagination rule must be applied to live templates immediately

User correction:

```text
你只更新了规范, 没有处理模版!!!
```

Context:

- User first stated a new xz01 hard rule: all dual-end list pages with data volume greater than one page must paginate; PC uses numeric page links; mobile uses 上一页/下一页, matching `xz01_demo`.
- The initial response updated the xz01 skill/rules but did not inspect or repair the currently deployed templates.
- User corrected the workflow: because the rule described an active template defect, the task required template repair immediately, not only durable rule capture.

Durable workflow lesson:

1. When a user states a new xz01 rule and the wording identifies a current live/template defect, treat it as two linked tasks:
   - update the durable xz01 skill/spec; and
   - apply the rule to the affected deployed/candidate templates immediately.
2. Do not stop after skill/memory updates when the user’s correction implies the current template is wrong.
3. For this pagination case, the repair pattern was:
   - scan deployed theme list templates under `/www/wwwroot/www.900az.com/public/themes/default/{cms,mobile}/list_*.html`;
   - repair only theme templates, never backend/controllers/routes;
   - PC templates: keep `$page_code|raw` priority if present, but fallback must output numeric page links (`1..page_count`, current marker, page-1 URL as `$list_url`, later pages as `list_N.html`);
   - mobile templates: do not raw-output `$page_code`; render `上一页  第 X / Y 页  下一页`, with disabled states at boundaries;
   - clear `/www/wwwroot/www.900az.com/runtime/` after edits;
   - verify with `php -l`, static checks, and HTTP render probes.
4. Final reporting must explicitly say both what was updated in the skill and what was changed in templates.

Future trigger examples:

- “这是规范” + mentions a visible/current page defect.
- “所有双端/列表页/详情页/导航/搜索…” where deployed templates likely already violate it.
- User pushes back that only rules were updated.

Pitfall to avoid:

- Treating a hard rule as documentation-only when it is also a live-template acceptance requirement.
