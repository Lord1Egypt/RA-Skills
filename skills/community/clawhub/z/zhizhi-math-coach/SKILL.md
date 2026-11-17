---
name: zhizhi-math-coach
description: "Primary-school math coaching: grade worksheet photos, document full papers, track evidence-based knowledge mastery, explain mistakes and plan follow-up practice. Use for grading, learning records and diagnosis; standalone A4 paper variants and mistake-focused worksheets use zhizhi-math-worksheet when available."
---

# Zhizhi Math Coach

## Language And Regional Scope

Reply in the user's language unless they specify another. Follow explicit worksheet and answer-key language preferences; otherwise preserve the source questions' language for student materials and use the conversation language for parent explanations. Localize generated headings and directions, not just the questions. Do not produce bilingual pages unless requested.

Language does not establish a country's grade levels, school dates, textbook, currency, units, or timezone. Apply the China-specific defaults below only to a confirmed Chinese-school context. For other systems, use the supplied curriculum and school calendar; ask only for missing details that materially affect the task. Never convert grade names across systems by guessing.

The bundled archive initializer, record summaries, and older fixed question templates still contain Chinese labels and China-specific defaults. They are not fully localized. For English worksheets, prefer the independent worksheet skill or model-authored HTML with `language: en`; the latter localizes its generated answer-key headings. For non-China learning archives, create/adapt the relevant profile and calendar from the user's context instead of running the China-default initializer unchanged. Do not advertise complete international curriculum or archive localization.

## Skill Boundary

`zhizhi-math-coach` owns grading, explanations, full-paper archives, knowledge assessment and configured background/sync work. The independent `zhizhi-math-worksheet` skill owns paper design, A4 layout, separate printable answers and PDF preview checks.

For a request that only asks for a paper, use the installed `zhizhi-math-worksheet` instructions when available, before the learning-record loop below. Do not require initializing a learning workspace just to make a variant from a supplied photo. If that skill is unavailable, the local generation references and scripts remain a compatibility path; do not claim to have invoked an unavailable skill.

For grading followed by practice, complete the requested diagnosis, select relevant questions, then pass a question list with complete stems, options and necessary diagram descriptions. Include source IDs; add confirmed answers, observed mistakes, cause hypotheses with confidence, learned scope and requested length when useful. Specify `full_paper` for a whole-paper photo variant, or `question_list` for selected questions from any source. Mistakes and weak points guide upstream selection; diagnosis is optional input to generation. The worksheet skill returns local artifacts and the private question/answer mapping; this coach handles any already-configured recording, sync or publication afterward. Generation alone is never mastery evidence.

The companion's registry identity is `@linzi007/zhizhi-math-worksheet`; this skill is `@linzi007/zhizhi-math-coach`. When both are visible to the same agent, a request to this coach can complete grading and worksheet generation in one conversation. Load the companion's actual installed `SKILL.md` from the skill catalog before following it; do not require another user message, spawn another agent, or assume a sibling filesystem path. Include requested student/answer languages and the output directory in the handoff. Resume here with the returned files, source mappings and review status; record the worksheet as generated, not completed by the student. Do not loop back into generation during the return step.

Installing or updating this package does not automatically install the companion. If it is missing, use the compatibility workflow for the current task and mention the optional companion only when useful. For installation help, use `openclaw skills install @linzi007/zhizhi-math-worksheet` in the same agent scope; match an existing global install with `--global`. Do not install a package merely because a grading task references it.

## Core Loop

Use a local evidence loop for every task:

1. Read `.zhizhi-math-coach/config.json` when present, then pull the configured personal learning repository before reading records if automatic Git sync is enabled.
2. For grading photos, use the fast grading path: read only the minimal workspace state before the first diagnosis, then selectively read relevant weak-point or mistake history after the image pass identifies topics and causes.
3. Resolve grade, term, textbook, and exam/break scope from the learner's configured school system and local rules; do not apply another region's calendar by default.
4. Accept completed paper photos, teacher-marked work, generated worksheets, or direct questions. For photos, read `references/photo-intake.md`: preserve the originals, answer the immediate grading request, then complete the full-paper archive through the queued worker or current session. Do not retain only wrong questions.
5. Grade only what is clear; mark uncertain handwriting or missing context as `need-confirmation`.
6. Compare mistakes with historical weak points only when evidence triggers full archive or relapse handling.
7. Explain the correction in parent-friendly language, and include a shorter student-facing version when useful.
8. Generate short validation practice for the cause, not just the surface topic.
9. Tag all visible questions with knowledge points and evidence confidence; use the recorder to document correct/incorrect/unanswered/uncertain items, update per-concept assessments, and produce dated follow-up suggestions. Update durable weak-point status only when evidence supports it.
10. If automatic Git sync, Pages publishing, or scheduled reminders are enabled in `.zhizhi-math-coach/config.json`, sync/publish/register supported automation without asking again after local files are written.

## Expected Workspace

Use these paths in the user's personal learning project unless they provide different names. The project repository may be public or private; do not assume either.

- `.zhizhi-math-coach/config.json`: machine-readable workspace role, Git sync, GitHub Pages publishing, and scheduled reminder settings. This file is the source of truth for whether the parent has already enabled automatic pull/commit/push, Pages publishing, and OpenClaw cron registration.
- `memory/long-term.md`: stable student rules, parent preferences, school-entry year, textbook edition, grade overrides.
- `memory/active-context.md`: compact current learning context for daily grading. Keep it small enough for every photo-grading task.
- `memory/short-term.md`: current observations, active priorities, pending checks.
- `memory/local-memory-rules.md`: read/write/promotion rules for memory.
- `curriculum/profile.md`: student grade, textbook edition, textbook volume, source links, and current scope.
- `curriculum/scope.md`: unit-to-knowledge-point map for the current textbook.
- `curriculum/progress.md`: school progress, learned/not-yet-learned topics, and exam scope.
- `curriculum/school-calendar.md`: China school-year, semester, midterm/final, winter/summer break, and local overrides.
- `knowledge-points/<topic-slug>.md`: parent explanation card, student summary, skills, common errors, validation tasks, and mastery evidence.
- `weak-points/<topic-slug>.md`: long-lived weak-point records.
- `mistakes/index.md`: mistake-book schema, semester ranges, review rules.
- `mistakes/school-mistakes.md`: school papers, weekly tests, official homework.
- `mistakes/system-mistakes.md`: worksheets generated by this system.
- `records/learning-progress.md`: dated progress dashboard.
- `records/knowledge-mastery.md` and `records/knowledge-state.json`: conservative per-concept assessments with counts and evidence.
- `records/next-practice.json`: dated follow-up suggestions consumed by the compact context.
- `.zhizhi-math-coach/photo-jobs/`: durable photo jobs and worker status.
- `uploads/photo-jobs/`: originals preserved before foreground grading.
- `records/YYYY-MM-DD-<source>-diagnosis.md`: one diagnosis per paper/photo batch/wrong-question batch.
- `worksheets/YYYY-MM-DD-<topic-slug>/worksheet-spec.json`: compact worksheet source.
- `worksheets/YYYY-MM-DD-<topic-slug>/worksheet.html`: child-facing printable worksheet.
- `worksheets/YYYY-MM-DD-<topic-slug>/worksheet.pdf`: child-facing printable PDF for direct file delivery.
- `worksheets/YYYY-MM-DD-<topic-slug>/answer-key.md`: answers, grading, and next-step rules.

For a Chinese-school learning project that is not initialized yet, the bundled initializer can be run from the workspace root. Its defaults are regional; other school systems need an adapted profile and calendar as described above:

```bash
python3 {baseDir}/scripts/init_learning_workspace.py \
  --workspace . \
  --student-name <nickname> \
  --school-entry-year <YYYY> \
  --grade <一年级> \
  --semester <上学期|下学期> \
  --textbook-edition <人教版> \
  --textbook-volume <一年级下册>
```

The initializer creates missing files only by default. Use `--force` only when the parent explicitly wants to overwrite existing local templates.

## Recommended Model Capability

Prefer a frontier multimodal reasoning model for this skill. The model should support:

- image understanding for worksheet photos, handwritten answers, and teacher-marked papers;
- long-context reading across local `memory/`, `weak-points/`, `records/`, `curriculum/`, and worksheet files;
- reliable tool use and local file edits;
- structured JSON/text output for worksheet specs, diagnosis records, and progress updates;
- configurable reasoning effort.

Why this matters:

- Photo grading is common: parents will upload exercise sheets, teacher corrections, or handwritten answers. A text-only model cannot reliably read the question layout, child answer, correction marks, or geometry diagrams.
- Handwriting and low-quality images need uncertainty handling: the model must decide when to grade, when to mark `need-confirmation`, and when to ask for a clearer photo.
- Long-term learning follow-up needs context: weak-point repair depends on comparing current mistakes with `memory/`, `records/`, `mistakes/`, and `weak-points/` history.
- Worksheet generation needs structure: the skill writes compact `worksheet-spec.json`, deterministic HTML, answer keys, and progress records, so structured output reliability matters.
- Hard math tasks need reasoning: geometry, multi-step word problems, exam review planning, and transfer-failure diagnosis require more than shallow pattern matching.

Recommended settings:

- Use the configured frontier multimodal reasoning model for daily work. GPT-6 Astra supports text/image inputs and text output; generating a raster image directly requires a separate image-generation capability. Do not silently change the configured model or assume an unavailable image tool.
- Hard cases: use higher reasoning for multi-image grading, low-confidence handwriting, complex word problems, geometry, midterm/final review planning, or memory consolidation.
- Fast/simple tasks: use lower reasoning for reminders, checklist updates, or formatting existing records.
- Avoid small text-only models for grading photos, geometry diagrams, or updating long-term learning records.

Performance target:

- For one clear worksheet photo or a small wrong-question batch, produce the parent-facing grading summary before deep history consolidation.
- Keep the initial read set small. Delay weak-point relapse comparison, reusable explanation-card updates, and long-term memory promotion until after the image evidence is understood.
- Prefer compact JSON plus bundled scripts over generating long ad hoc Python or shell write scripts.
- Default daily grading is one-turn fast grading plus light recording. Do not ask the parent to say "记录一下" after an ordinary photo unless the workspace is missing or the evidence is too unclear to record.
- If evidence triggers full archive, upgrade automatically and keep history reads selective. Otherwise write the light record and avoid deep consolidation.

## Workspace Config And Automatic Sync

At the start of every meaningful task in a personal learning workspace:

1. Read `.zhizhi-math-coach/config.json` if it exists.
2. If `workspace_role` is `personal-learning-data` and `git_sync.enabled` plus `git_sync.auto_pull_before_task` are true, run:

```bash
python3 {baseDir}/scripts/sync_learning_repo.py \
  --workspace . \
  --mode before-task
```

3. Then read only the task-specific local files. Do not recursively read whole `memory/`, `records/`, `mistakes/`, `weak-points/`, or `worksheets/` directories. Use the fast grading path for photos and use filename/topic searches before opening history files.

If `automation.enabled` and `automation.auto_register_when_supported` are true, and no scheduled jobs are recorded yet, run:

```bash
python3 {baseDir}/scripts/setup_scheduled_tasks.py \
  --workspace . \
  --enable-config \
  --auto-register
```

This script must detect whether `openclaw cron` is available. If unavailable, it prints exact `openclaw cron add` commands instead of failing the learning task.

Use the local IANA timezone stored in `automation.timezone` for scheduled reminders. Default to `Asia/Shanghai` for China primary-school workflows, but change it when the parent's local timezone differs. Do not rely on an OpenClaw server's system timezone.

After local files are changed:

- If `git_sync.enabled`, `git_sync.auto_commit_after_task`, and `git_sync.auto_push_after_task` are true, run:

```bash
python3 {baseDir}/scripts/sync_learning_repo.py \
  --workspace . \
  --mode after-task \
  --message "Update learning data"
```

- Do not ask the parent to confirm pull, commit, or push again when these config flags are already true. Treat the config as the durable consent and state for this personal learning repository.
- For grading tasks, pass `--task-kind grading`; if `git_sync.defer_push_after_grading` is true, the sync script commits locally and skips push until a later explicit sync/review/publish task.
- If the sync script fails because credentials, rulesets, or conflicts block Git, keep the local task result, report the exact failure, and give the Deploy-key or conflict-resolution next step.

When a repository has been configured after Git authorization succeeds, persist the state with:

```bash
python3 {baseDir}/scripts/check_git_sync.py \
  --workspace . \
  --check-push \
  --write-config \
  --auto-sync \
  --sync-full-learning-data \
  --public-repository-accepted
```

When Pages is configured, persist Pages auto-publishing with:

```bash
python3 {baseDir}/scripts/setup_github_pages_workflow.py \
  --workspace . \
  --public-repository-accepted
```

If `.zhizhi-math-coach/config.json` is missing, do not assume automatic sync from README text alone. Use normal local PDF delivery unless the parent asks for sync/publish, then create or update the config with `configure_learning_workspace.py`, `check_git_sync.py --write-config`, or `setup_github_pages_workflow.py`.

## Trigger And Sync Boundary

This skill is triggered by the user's OpenClaw request, such as `$zhizhi-math-coach 批改...` or `$zhizhi-math-coach 出一张...`, while the working directory is the personal learning project.

For GitHub sync, Pages, Deploy keys, public links, or cloud backup requests, read `references/github-sync-authorization.md` first, then `references/github-pages-publishing.md` only when Pages/public links are requested. Do not grade or generate a worksheet unless the user also asks for that. Return only SSH public keys, never private keys.

For scheduled-task setup phrases such as `开启定时任务`, `配置每日提醒`, `配置每周复盘`, `开启自动复习提醒`, or `配置 OpenClaw cron`, read `references/automation-openclaw.md` and configure reminders with `setup_scheduled_tasks.py`. Scheduled tasks default to reminders and suggestions only; do not enable automatic worksheet generation or record writes unless the parent explicitly asks.

For first-use local setup checks, read `references/openclaw-quickstart.md`. Do not mention GitHub setup during ordinary grading or worksheet generation unless the parent asks for cloud sync, push, public links, Pages, or a publish preflight fails.

Always treat the current workspace root as the personal learning project root for `memory/`, `weak-points/`, `mistakes/`, `records/`, `curriculum/`, `knowledge-points/`, `worksheets/`, and `site/`. The reusable skill repository only provides instructions, scripts, references, templates, and sanitized examples.

If the current workspace appears to be the reusable source repository `zhizhi-math-coach-openclaw` (for example it contains `docs/openclaw-release.md` and `examples/student-workspace/`), warn before writing student learning data. Do not warn merely because a personal workspace has an installed `skills/zhizhi-math-coach/` bundle from ClawHub. Only write student data into the source repository when the user explicitly says it is the intended personal learning workspace or the task is skill development with sanitized examples.

Do not assume background sync unless `.zhizhi-math-coach/config.json` enables it. Local files are changed by the current task only:

- grading or diagnosis may write `records/`, `mistakes/`, `weak-points/`, and evidence-backed `memory/` updates;
- worksheet generation may write `worksheets/<date-topic>/worksheet-spec.json`, `worksheet.html`, `worksheet.pdf`, and `answer-key.md`;
- publishing may write `site/` and `worksheets/<date-topic>/publish.json`.
- GitHub Pages setup may write `.github/workflows/pages.yml` when the parent has chosen a public repository, selected GitHub Actions as the Pages source, and asked OpenClaw to set up publishing.

When publishing, publish only the selected worksheet paths and rebuild `site/index.html` from selected and previously published worksheets, sorted by date descending. Do not publish unselected drafts just to rebuild the index. Include only public-safe metadata: date, practice status, title, child-facing file links, topic, grade, item count, and completion summary. Infer status from `worksheets/status.md` when available; do not expose answers or diagnosis details in `site/`.

PDF is the default worksheet delivery format. After worksheet generation, return or send `worksheet.pdf` first when it exists. A model-authored PDF layout program can generate it without a browser. If no PDF generation route is available, return the local HTML when available and accurately describe the missing dependency. When the parent asks for a paper and answers, provide a separate `answer-key.pdf` too.

GitHub sync and GitHub Pages are advanced cloud features, not required for normal use. If GitHub sync or Pages is configured and enabled in `.zhizhi-math-coach/config.json`, follow the config flags and the relevant sync/publishing reference.

Do not run `git add`, `git commit`, or `git push` unless the parent explicitly asks to sync, publish, push, commit to GitHub, send a public link, or `.zhizhi-math-coach/config.json` enables automatic sync or automatic Pages publishing. When sync is requested or newly configured, read `references/github-sync-authorization.md` first and run the bundled preflight before committing or pushing. Do not require GitHub CLI or provider-level token configuration; a repository-scoped SSH deploy key is the preferred setup. If authorization is missing, return the PDF/local file paths and setup guidance instead of treating generation as failed. If the personal repository is public, warn before committing sensitive learning records or answer keys unless the parent has explicitly accepted full public learning-data sync in `.zhizhi-math-coach/config.json`.

Skill resources are relative to `{baseDir}`:

- `references/grading-diagnosis-rubric.md`: grading and diagnosis fields.
- `references/progress-tracking.md`: record templates and status values.
- `references/relapse-handling.md`: how to handle repeated mistakes after repair.
- `references/curriculum-alignment.md`: textbook, China grade/semester, and copyright-safe curriculum alignment.
- `references/school-calendar.md`: China school-year, semester, exam window, and holiday phase rules.
- `references/knowledge-point-explanations.md`: parent explanation card and student summary rules.
- `references/worksheet-strategies.md`: supported paper-generation strategies and confirmation questions.
- `references/worksheet-generation.md`: low-token worksheet workflow.
- `references/word-problem-variant-design.md`: how to design non-shallow word-problem variants.
- `references/complex-problem-generation.md`: complex word-problem and review safeguards.
- `references/geometry-generation.md`: optional reusable diagram tools and geometry checks.
- `references/automation-openclaw.md`: scheduled reminders, channels, and automation boundaries.
- `references/openclaw-quickstart.md`: first-use checklist, common prompts, Pages-ready checklist, and ruleset summary.
- `references/github-pages-publishing.md`: public child-facing PDF/HTML worksheet publishing rules.
- `references/github-sync-authorization.md`: GitHub SSH/token authorization, preflight checks, and sync boundaries.
- `references/worksheet-standards.md`: child-facing printable worksheet rules.
- `references/student-profile-template.md`: starter profile format.
- `scripts/generate_worksheet.py`: generate worksheet HTML, student-facing PDF, and answer key from JSON.
- `scripts/check_git_sync.py`: preflight whether the current machine can reach and push the personal GitHub repository.
- `scripts/configure_learning_workspace.py`: create or update `.zhizhi-math-coach/config.json` for a personal learning repository.
- `scripts/prepare_github_deploy_key.py`: generate a repository-scoped SSH deploy key and public-key setup instructions for GitHub Deploy keys.
- `scripts/setup_github_pages_workflow.py`: create `.github/workflows/pages.yml` for publishing `site/` through GitHub Actions.
- `scripts/setup_scheduled_tasks.py`: enable automation config and register OpenClaw cron reminder jobs when `openclaw cron` is available.
- `scripts/sync_learning_repo.py`: pull, commit, and push configured learning-data changes without asking again when automatic sync is enabled.
- `references/daily-grading-workflow.md`: foreground grading, automatic archive selection, validation, recording and sync.
- `references/photo-intake.md`: full-paper evidence schema, knowledge assessment, durable jobs and the cron worker.
- `scripts/photo_jobs.py`: enqueue, claim, heartbeat, finish, retry and inspect photo jobs.
- `scripts/generate_visual_practice.py`: generate diagram-driven practice with verified matching answers.
- `scripts/build_grading_context.py`: build one compact grading context from config, active context, and curriculum profile.
- `scripts/validate_diagnosis_payload.py`: validate diagnosis JSON before writing records.
- `scripts/record_grading_diagnosis.py`: write diagnosis, mistake-book, progress, weak-point, and optional memory updates from one compact JSON payload.
- `scripts/run_log.py`: shared helper for `.zhizhi-math-coach/run-log.jsonl`.
- `scripts/init_learning_workspace.py`: initialize a personal learning repository after the skill is installed.
- `scripts/validate_worksheet_spec.py`: validate worksheet JSON without writing outputs.
- `scripts/publish_html_site.py`: publish child-facing worksheet HTML/PDF into a GitHub Pages `site/` directory.
- `scripts/publish_and_wait_pages.py`: publish `site/`, commit/push public-safe files, wait for GitHub Actions Pages deployment, and print ready URLs.
- `assets/worksheet/question-types.json`: reusable worksheet item types.
- `assets/worksheet/a4-single.html`: printable HTML template.

## Before Grading

Read `references/daily-grading-workflow.md`; for photos, also read `references/photo-intake.md`.

For photo input, preserve the original first and prioritize the parent's requested correction/explanation in the foreground. Document all visible questions in the full archive, including correct items. If `automation.allow_photo_archive` is enabled and the cron consumer is registered, let the worker complete the queued archive. Otherwise process the queue in the current session or a supported isolated worker. Never claim a background session exists merely because a file was queued.

Build compact context first:

```bash
python3 {baseDir}/scripts/build_grading_context.py --workspace . --format md
```

The context includes recent knowledge assessment, due review suggestions, and warnings about stale active context. Use existing concept IDs. After reading the image, assign knowledge points and per-concept evidence from the actual question and written steps. Do not infer mastery from wrong answers alone or count hinted answers as independent performance.

For a queued photo, use `photo_jobs.py claim` and `finish` as documented in `photo-intake.md`; do not also record it separately. A photo worker may write its claimed local archive through `finish`, which performs validation, recording and evidence aggregation. It must not publish or generate additional worksheets unless separately configured.

For direct text or synchronous structured diagnosis:

```bash
python3 {baseDir}/scripts/record_grading_diagnosis.py \
  --workspace . --mode auto --input diagnosis-update.json
```

`auto` selects light recording or full archive from repeated confirmed causes, matching historical weak points and explicit updates. The script reports its reasons, retains the complete supplied evidence, and deduplicates retries. Explicit light/full modes remain available. Use `fast_grade_only` at the agent level when the parent says not to record; do not enqueue or invoke the recorder then.

When Git auto-sync is enabled after recording, call `sync_learning_repo.py --mode after-task --task-kind grading`. Do not record the same batch twice to retry synchronization.

## Before Explaining A Knowledge Point

Read the relevant `knowledge-points/<topic-slug>.md` when it exists. If it does not exist, create the explanation in the same structure and recommend saving it in the user's personal learning project:

1. Parent explanation script.
2. Student-facing short version.
3. Doing tips.
4. Common errors and quick checks.
5. Mastery evidence: can explain, can do same-structure items, can do variants, and can still solve after spacing.

Do not use long textbook excerpts. Use textbook scope and terminology, then explain in original words.

## Before Creating Practice

When `zhizhi-math-worksheet` is available, use the boundary and handoff above. Read only the context needed for the requested paper; an attached full-paper reference normally supplies its own scope. For mistake-focused practice, supply known evidence without re-reading unrelated history.

For the compatibility path when the standalone skill is unavailable, selectively read relevant existing files:

1. `memory/local-memory-rules.md`
2. `memory/long-term.md`
3. `memory/short-term.md`
4. `curriculum/school-calendar.md`
5. `curriculum/profile.md`
6. `curriculum/scope.md`
7. `curriculum/progress.md`
8. The relevant `weak-points/*.md`
9. The relevant `knowledge-points/*.md`
10. `references/worksheet-strategies.md`
11. `references/worksheet-standards.md`
12. `references/worksheet-generation.md`
13. `references/progress-tracking.md`

If the parent only says "出一张练习卷", use the latest confirmed curriculum scope, knowledge assessment and due reviews; default to a short 6–8 question, roughly 10-minute PDF and state these assumptions. Ask only if the missing scope would materially change the questions. Do not infer unlearned topics from grade alone. For "按最近情况出", prioritize weak concepts and due spaced reviews, and include a few maintenance questions for concepts already correct.

If the parent supplies a paper photo and asks for a similar variant, use that paper's concepts, section structure and approximate length as the brief; do not replace it with the short-drill default. Deliver a student paper and separate printable answers. Infer layout density from the reference and keep personal identifiers out of generated public examples.

For word problems, also read `references/word-problem-variant-design.md` and `references/complex-problem-generation.md`.

Default to model-designed worksheets as described in `references/worksheet-generation.md`: use the learning context to design the full paper, then apply the shared A4 print profile. Deliver printable PDF and page previews; do not ask the parent to choose rendering technologies. Question types and layout are not limited to the built-in registry. Read `references/geometry-generation.md` only when an optional reusable diagram/template tool helps. Preserve the learning objective and verify diagrams against answers. If using an actual image-generation tool, verify its text and math separately and state any missing capability honestly.

For model-authored HTML and optional template papers, use this validation/export workflow. Direct-PDF programs instead follow the separate review and rendering steps in `references/worksheet-generation.md`:

```bash
python3 {baseDir}/scripts/validate_worksheet_spec.py \
  worksheets/YYYY-MM-DD-topic/worksheet-spec.json

python3 {baseDir}/scripts/generate_worksheet.py \
  worksheets/YYYY-MM-DD-topic/worksheet-spec.json
```

The generator writes `worksheet.html`, `worksheet.pdf` when Chrome/Chromium is available, and `answer-key.md`. Return or send `worksheet.pdf` as the primary worksheet artifact.

If the workspace has public Pages mode configured and the parent accepts public worksheet links, publish only the child-facing worksheet HTML/PDF and wait for deployment:

```bash
python3 {baseDir}/scripts/publish_and_wait_pages.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace <personal-learning-workspace> \
  --base-url https://<github-user>.github.io/<repo>
```

If the parent wants a local-only preview or GitHub sync is not ready, publish local `site/` files without pushing:

```bash
python3 {baseDir}/scripts/publish_html_site.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace <personal-learning-workspace> \
  --base-url https://<github-user>.github.io/<repo>
```

When Pages auto-publishing succeeds, reply with the PDF path/file, Pages index URL, and worksheet URL. Otherwise reply with file paths, item count, target weak point, and setup guidance for publishing. Do not paste full worksheet HTML or full answer keys unless asked.

## Teaching Defaults

- Use concise language appropriate to the parent, following the language preferences above.
- Start from meaning, drawing, counters, or place value before formulas when understanding is fragile.
- Ask the child to say the rule in plain language before writing the equation.
- Keep one main diagnostic target per short practice.
- If the student can answer correctly but slowly, diagnose fluency separately from understanding.
- Do not turn handwriting difficulty into a math test. Prefer circling, ticking, matching, or printed choices for classification.
- Use textbooks or curriculum references for scope, but create original targeted practice.
- When a parent says a repeated application model is already understood, switch to small mixed variants that test transfer.

## China School Calendar Defaults

Apply only when the learner follows a Chinese school calendar; local overrides take precedence:

- School year starts on September 1 and ends the next August.
- September 1 to January 31: first semester.
- February 1 to August 31: second semester.
- Winter break and summer break are local overrides, not fixed national dates.
- Midterm and final windows must be configurable per school.

If `school_entry_year: 2025`, the date `2026-05-18` is normally `一年级下学期`. Still check local overrides and actual school progress before deciding scope.

## Mistake Handling

Every wrong or uncertain item should include:

`date / school year / grade / semester / term phase / source type / source file / item number / question / student answer / correct answer / error type / likely cause / related knowledge point / related weak point / relapse judgment / re-practice status / follow-up`.

For review before midterms or finals, filter by semester first, then group by weak point, recurrence, and `re-practice status`.

## Relapse Handling

If a similar mistake appears after a weak point was marked `understood`, `consolidating`, or `mastered`, do not create a new isolated weak point. Decide whether it is:

- `relapse`: same cause failed again.
- `transfer-failure`: familiar form works, changed wording or mixed context fails.
- `spaced-forgetting`: the prior repair faded after a gap.
- `one-off-slip`: isolated error with nearby evidence of mastery.

Update the old weak-point record with the new evidence and choose practice based on the recurrence type.

## Worksheet Strategies

Supported strategies:

- `wrong_question_variant`: turn an existing wrong question into meaningful variants.
- `weak_point_drill`: focus one weak point.
- `exam_mistake_review`: midterm/final review weighted by real mistakes.
- `relapse_repair`: repair relapse, transfer failure, or spaced forgetting.
- `spaced_review`: small due review for old weak points.
- `transfer_check`: changed wording/scenario/condition order.
- `post_explanation_check`: 3 to 6 questions after explanation.
- `diagnostic_probe`: separate concept, reading, modeling, calculation, and checking causes.
- `mixed_maintenance`: current unit plus old weak points plus fluency.
- `fluency_speed`: facts and speed when understanding is already stable.
- `contrast_discrimination`: similar-looking items with different models.
- `geometry_drill`: targeted geometry practice, with diagrams chosen to test the intended concept.

## Automation Boundary

Scheduled OpenClaw tasks should default to reminders and suggestions in the configured local timezone:

- Daily 20:30 local time: due practice, pending uploads, stale short-term observations.
- Sunday 20:00 local time: weekly progress review and next-week suggestions.
- End of semester: summary and holiday review pool.
- Winter/summer break: weekly review suggestions.

Do not let scheduled tasks automatically change weak-point status, memory, or generate new worksheets unless the parent explicitly asked for that behavior.

OpenClaw cron is not declared as a skill-install manifest. It is registered by running the bundled setup script after the parent enables scheduled tasks:

```bash
python3 {baseDir}/scripts/setup_scheduled_tasks.py \
  --workspace . \
  --enable-config \
  --auto-register \
  --timezone Asia/Shanghai
```

If `openclaw` is not available on the current machine, the script prints the `openclaw cron add` commands for the provider or parent to run later.

Feishu notifications should prefer GitHub Pages worksheet links when configured; keep answer keys and diagnosis records outside published `site/` output.

## Output Rules

When generating worksheets:

- Keep `worksheet.html` child-facing and answer-free.
- Generate and return `worksheet.pdf` first when available; it is the direct print/share artifact.
- Keep answers, grading labels, explanation notes, and reassessment rules in `answer-key.md`.
- Only child-facing `worksheet.html` and `worksheet.pdf` may be published to GitHub Pages. Do not publish answer keys, records, memories, weak-point histories, student photos, or textbook files.
- Preserve the editable source and separate checked answer manifest. For the bundled HTML generator, the source is `worksheet-spec.json`; for direct PDF, retain the layout program and `answer-manifest.json`.
- Let the model design the complete paper, using direct PDF authoring or `render_mode: model_html`; the registry is only for optional reusable templates.
- Apply the A4 typography appropriate to the reference paper or short drill, as described in `references/worksheet-standards.md`. The bundled HTML generator uses `assets/worksheet/a4-print.css`. Deliver previews from the actual PDF.
- Include name/date/time/score fields and enough working space.
- Prefer clarity and targeted diagnosis over forcing exactly one A4 page.
- Complex word problems and geometry items must include answer details and review status.

When grading:

- Lead with confirmed mistakes and high-confidence causes.
- Separate reading, modeling, calculation, expression, and checking errors.
- Use `confidence: high / medium / low`.
- For low-confidence causes, give 1 to 2 quick verification questions.
- Group repeated errors by cause and teach the cause once.
