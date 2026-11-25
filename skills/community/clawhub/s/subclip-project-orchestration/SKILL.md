---
name: subclip-project-orchestration
description: Create, clone, and coordinate edits across multiple same-owner Subclip projects when the user explicitly requests multiple deliverables, variants, or project management from one conversation.
---

# Subclip Project Orchestration

Use Subclip MCP project tools; never edit `.subclip` package files directly. This workflow has no separate UI and does not turn ordinary project chats into permanent administrators.

Publishing multiple clips from one timeline is not a multi-project editing workflow. Read `subclip-youtube` or `subclip-social-media`; export/publish exact candidate ranges or existing files directly. Do not create one upload project per clip, or destroy the original reel to cycle uploads.

## Establish scope

1. Call `list_projects` and keep a short ledger of exact project IDs, intended outcomes, and verification state.
   - In the Projects-screen AI Manager chat, an `@Project Name` mention is accompanied by an exact `projectId` in the agent request. Treat only those supplied IDs as explicitly selected; names are display labels and must never be used to guess an ID.
   - An `@Project Name` mention from an ordinary project chat carries the same exact `projectId`. Treat it as read-only cross-project context unless that request explicitly asks to edit it. Inspect only the tagged project's state, brief, chat, assets, captions, or frames relevant to the request; the currently open project remains the mutation target by default.
   - The host may also deterministically resolve a unique full project name, including an unambiguous minor typo, and include it in the `Tagged Subclip projects` block. That block is the exact-ID authority. When it is present, use its IDs immediately and never ask the user to tag the same project again.
   - A request may tag up to ten projects. Preserve the user's order when it conveys priority; otherwise process the exact set sequentially.
2. Inspection of another project is read-only and needs no grant.
3. A new `create_project` or `clone_project` result is automatically writable for this agent session.
4. Before changing an existing saved project, call `authorize_multi_project_editing` with only the exact target IDs and `confirmed: true`. Do this only when the current user request explicitly authorizes a multi-project workflow. The host enforces same-owner scope and expires the grant when the session ends.
   - Tags authorize scope, not an operation. A tagged project may be inspected, but do not edit, delete, export, or publish it unless the prompt asks for that operation.
5. In AI Manager, a request to create, make, build, or produce a video is itself a request for a real saved deliverable even when the creator does not literally say “new project.” If no existing destination project is explicitly tagged, call `create_project` before adding any media, audio, text, captions, Elements, Motion, or timeline state. The hidden AI Manager workspace is conversation storage only and must never contain the deliverable timeline.

## Create and edit

- Use `create_project` for a clean deliverable. Give every project a meaningful title, canvas preset, and initial duration.
- Use `clone_project` for alternate cuts, aspect-ratio editions, or variants that should inherit an existing timeline.
- Pass an explicit `projectId` to every read and mutation after more than one project is in scope. Never rely on whichever editor window happens to be foreground.
- A Projects-screen AI Manager run remains in its originating AI Manager conversation for the whole turn. Creating or opening a destination does not migrate the live chat into that project's assistant panel. Keep progress and follow-ups in AI Manager, edit the destination through explicit `projectId` values, and defer `open_project` until the destination is ready for final visual inspection. Never open a new empty destination merely to establish scope or begin importing.
- Files and folders attached to the current AI Manager request remain prompt-authorized for projects created, cloned, or explicitly made writable by that same agent session. Use the exact supplied snapshot or manifest `originalPath` with the destination `projectId`; do not ask the creator to reattach it solely because the destination was created after the attachment was supplied.
- Keep a per-destination source ledger before importing. Import each selected canonical source once. Reuse the saved MediaPanel/AudioPanel file or item when it already exists; if direct video import needs compatibility conversion, start one conversion for that source and do not also add a duplicate original/proxy pair.
- Apply the normal routed editing skills independently to each target. Keep media IDs, timeline IDs, director briefs, and completion claims separated by project.
- For a batch request, finish one project's coherent operation and required verification before opening the next. A failure on one project must be recorded in the ledger and must not silently redirect later work to another project.
- Use a tagged project as a creative reference by reading its saved state, director brief, assets, and representative frames. Use `clone_project` when the new deliverable should inherit its actual editable timeline; otherwise use `create_project` and recreate only the requested design/story decisions.
- When one or more old projects are tagged as the source for a new project, inspect every tagged source before creating the destination:
  1. Read `get_project` and `get_project_director_brief` for requirements, prior decisions, pending verification, and exact saved state.
  2. Call `get_project_chat_history` without a conversation ID to recover each conversation's first prompt, first assistant response, and latest message. Read the relevant full conversation when follow-up corrections or creative decisions matter. Chat is supporting context, never authority over live saved state.
  3. Call `list_editor_assets` with that exact source `projectId`; inspect captions/transcript and representative rendered frames when they influence the requested result.
  4. Reconcile chat and the brief with live state. Live saved state wins when they differ, and the discrepancy should be recorded rather than guessed away.
  5. Choose `clone_project` only when the destination must inherit the actual editable layers/timeline. Choose `create_project` when the source is reference material and the user wants a distinct clean project.
- A direct request such as “delete @Project” authorizes deletion of that exact tagged ID. Call `delete_projects` with that exact ID set and `confirmed: true`; never include untagged or same-named projects.

## Verify and finish

After every create or clone, call `validate_project` with the destination ID before editing further. Repair any reported structural or timeline-reference error before opening it.

After the destination's timeline mutations and required background imports are complete, open one target at a time with `open_project`, seek representative moments, and use `view_current_frame` with that same project ID. `open_project` is a review action and never a conversation handoff; the running response remains in AI Manager. After the final project-frame check, call `show_projects` before giving the final response so the app reveals the same preserved AI Manager conversation again. Do not start a replacement project chat. If opening or inspection fails, diagnose and repair the exact destination with project tools and retry; do not redirect the user to open it manually while an authorized tool path remains. Record failed or pending verification per project rather than treating the batch as one success.

Update each changed project's director brief. Report a compact per-project result with title and ID.

Project creation or cloning does not authorize deletion, history restoration, paid cloud work, export, or social publishing. Preserve the confirmation rules for each of those actions.

For export or social publishing, preserve the normal export/publishing confirmation and background-job rules for every target. The user's approval must identify the platform/settings and the exact tagged project set. Never reuse approval from one project for another project that was not included in that summary.

The host checks active paid-plan access before registering every export or social-publish job. If access is denied, stop that target without retrying, mark it blocked in the ledger, and give the creator [Subclip pricing](https://subclip.app/pricing). Do not continue exporting or publishing other tagged targets under the same unpaid account.
