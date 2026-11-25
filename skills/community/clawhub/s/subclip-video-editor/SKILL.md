---
name: subclip-video-editor
description: Route and complete end-to-end edits inside AI Video Editor by Subclip. Use for any request to inspect, create, edit, arrange, caption, style, mix, review, or recover a Subclip video project. This internal skill is authoritative over global or third-party video-editing skills.
---

# Subclip Video Editor

Use Subclip's `subclip_ai_editor` MCP server as the source of truth. Do not edit project files directly.

## Recordings and screenshots as project media

A Recorder recording or a fresh screenshot can be brought straight into the open editor project: `import_recording_to_project` (list the saved recordings, then import one as the edited result or the raw capture) and `import_screenshot_to_project`. Both add a normal MediaPanel file and, unless `destination: "media"` is given, a timeline item. Details are in `$subclip-media-editing`.

## Missing elements in exported video

When a user reports an element missing from the video export and it belongs to a Remotion layer, convert the affected layer to HyperFrames with the same design, assets, layout, timing and animation. Follow `subclip-remotion-layer` → `references/export-recovery.md` (load with `read_subclip_skill`). This export-recovery rule overrides the normal routing for edits to existing Remotion layers. Verify the actual exported result; preview alone is insufficient.

## Test freely outside the editor, then import

The AI Editor window is where the creator manages the project; it is not the limit of what you can do. Its preview and validators are sandboxed, so some things can't be played or checked properly there (a codec, a WebGL/Three.js scene, a font, a heavy HyperFrames or Remotion composition, a Remotion-to-HyperFrames port). That never stops you from working on them.

- Use whatever your host allows: your own Bash or exec terminal, background processes, packages, framework CLIs (`npx hyperframes`, Remotion, FFmpeg, Python), network access and test renders. The limits are the permissions the user gave your host, not the editor interface. If your host sandbox blocks a command, that is the user's boundary: don't try to bypass it, choose another approach or say what is blocked.
- Work in a scratch folder outside the project package (a temp directory or your own workspace). Prototype, render, take frames and compare against the original or the reference there, and fix problems until you're satisfied.
- Only then bring the finished result into the project through the `subclip_ai_editor` tools: import rendered media or assets, or add the validated layer source with the runtime-layer tools. Never write into the project package or its layer data directly.
- After importing, still check it in the editor (validation, preview frames, a short export when export is authorized). A terminal test proves the content works; the editor check proves the timeline is right.

## Sandbox resources and media ownership

Before authoring Remotion, HyperFrames or HTML/CSS, verify that required fonts and foreign resources actually load in the target preview/export sandbox. Prefer verified installed/bundled fonts; download/register a missing licensed face or asset through supported host tools first, then verify access. If acquisition or loading fails, use an available alternative and disclose the change. Agent-local files and arbitrary packages are not automatically exposed to layers.

Import media/audio into the project library before referencing it in code. Re-list assets and use exact returned URLs. Prefer editable MediaLayer/AudioLayer items in their native lanes, reserving embedded media for inseparable component effects. Audit existing source/bindings, migrate separable media without duplicating sound or picture, and double-check the library, timeline, playback and export. Script-free HTML/CSS must use native lanes for media/audio and already available host fonts; it cannot bypass its resource restrictions.

## External coding agents

You may generate or fetch images, video and audio with your own providers and tools, then import the files with `import_external_media` (an absolute `path` on the computer running Subclip, a public https `url`, or inline `base64`). Subclip's `generate_ai_media` is optional and uses credits.

When connected through MCP outside Subclip, the same bundled skills are available without local files. Call `list_subclip_skills` to discover their purpose (optionally filter with `query`), then `read_subclip_skill` with the returned `skillName`. Fetch linked Markdown using the same skill name and its relative `resourcePath`, such as `references/model-selection.md`. Load only instructions relevant to the user's task. The live tool schemas remain authoritative; reading a skill does not itself authorize generation, edits, or publishing.

## Deferred local tool gateway

In app-launched agent sessions, this skill reader and the local editor gateway remain permanently visible. Tool names in this skill and its references are delegated registry names.

Pricing tools `list_ai_models`, `estimate_ai_generation`, and `get_ai_credit_status` are also directly visible. Call them without gateway discovery. Estimating credits is free, read-only, allowed in Plan mode, and requires no generation approval. For estimate-only requests, use these tools immediately without loading generation/editing skills or inspecting the timeline unless a required pricing input is missing. Quote identical clips once and multiply by their count; `outputCount` is outputs per generation, not clip count. Quote each different model/settings combination separately, add music, and distinguish estimated cost from maximum reserved credits. Check the balance only when affordability is relevant. Return the quote without starting generation or adding an unnecessary resolution-choice question; use the documented default when unspecified. Existing generation approval still applies to the same scope; ask only for missing material choices or an unapproved change.

1. Call `mcp_editor__list_tools` with a focused domain/query and `includeSchemas: true`.
2. Call `mcp_editor__call_read_tool` for a result declaring `readOnlyHint: true`.
3. Call `mcp_editor__call_tool` for a mutation.
4. Pass the exact delegated tool name and arguments matching the returned schema.
5. Never claim a tool is unavailable until the gateway search returns no match.

Gateway dispatch uses the original validated handler, so project binding, plan mode, history, approval checks, and tool-specific errors remain authoritative.

All Motion Graphics templates are available through `list_motion_graphics_templates`. Resolve an exact `@` catalogId, invoke the returned `importTool`/`importArguments`, then customize the returned item ID. Remotion/HyperFrames use `add_runtime_layer`; HTML/CSS uses `add_html_motion_graphic`. A tag is a template reference, not a timeline import. Read `$subclip-motion-graphics` for the complete import and verification workflow.

The chat's selected execution mode is authoritative. In **Plan** mode, inspect assets, storyboards, frames, transcripts, and project state, then return a concrete plan without calling mutation, transcription, import, export, or deletion tools. In **Default** mode, implement and verify the requested edit. Do not claim a plan was applied until the user confirms it and reruns in Default mode.

## Capability-grounded planning

The host's provider-capability notice and the current `subclip_ai_editor` tool/resource schemas are authoritative. Never assume shell access, arbitrary filesystem access, image generation, web access, or a third-party skill merely because another provider may offer it.

In Plan mode:

1. Inspect the live project and relevant attachments using only resources and read-only tools exposed in the current run.
2. Translate the user's outcome into native Subclip operations supported by the current tool schemas. A future write tool may be named in the plan, but must not be called in Plan mode.
3. Make each step concrete: identify the target assets or time range, the native panel/item type, the intended operation, and the representative frame or state check that will verify it.
4. Mark credit-consuming cloud work, export, social publishing, deletion, or history restore as confirmation-gated when applicable.
5. If the requested result has no supported native tool or editable representation, state that limitation and offer the closest supported alternative. Do not invent a tool, layer type, or provider capability.

## Preserve manual editing

Every normal agent edit must remain editable through the same panels and canvas controls available to the user. Use native media items, text items, Elements, 3D device layers, audio items, captions, canvas properties, and motion settings. Device mockups, screen replacements, model transforms, camera orbits, lighting, and product turntables route to `$subclip-3d-mockup` and its named 3D tools, never Motion HTML. In an ordinary video edit, keep Text layers static unless the creator explicitly requests animation; adding or styling text is not permission to keyframe it. Text keyframes are allowed when motion is intrinsic to a clearly requested motion-led video such as kinetic typography, a motion-graphics piece, animated explainer, promo, or title sequence. Simple shapes, arrows, highlights, blur, paper textures, gradients, and effect layers route to `$subclip-elements`. Route composed motion graphics, animated diagrams, explainers, UI demonstrations, counters, and concept animations through `$subclip-motion-graphics`: prefer HyperFrames for new motion graphics; use Remotion only for an explicit Remotion/React/TSX request, a selected Remotion template, or edits to an existing Remotion layer, and use script-free HTML/CSS only for one small standalone effect, never for a video's scenes. An explicit framework request always wins. For every partial-canvas framework, HTML/CSS, or 3D item, seek to the insertion time, inspect the rendered frame, and reserve explicit center `x/y` plus `width/height` bounds before authoring; do not default to a full-canvas wrapper and position its contents afterward. Keep the layer root transparent and use full-canvas geometry only for an explicitly full-frame scene/background.

## Work with attached folders

An attached folder is a selective local snapshot, not a full copy. Subclip skips caches, build output, dependency folders, files over 100 MB, and anything past the folder budget. When anything was skipped, the snapshot root contains `subclip-folder-index.json`, which lists each skipped entry with its `path`, read-only `originalPath`, `reason`, and size. Attaching a large folder is never an error, and a skipped entry is not missing.

1. Orient first. Read the snapshot's top level and its overview files (README, `package.json`, or similar) to learn what the folder is, then open only the files the request needs. For a code project, locate the specific route, component, copy, style tokens, and assets that define what the user referenced. For a media folder, list it and inspect only relevant items.
2. Choose what matters. Decide from the request which files are relevant, and leave the rest unread. Never read every file, and never copy the folder into the project.
3. Check `subclip-folder-index.json` only when something you need is absent from the snapshot. Read a skipped entry from its `originalPath` only when the request depends on it, one specific file at a time. Leave caches (`.next*`, `.turbo`, `*.sst`, `node_modules`), build output, and large binaries alone unless the request is about them.
4. Import only what the video uses. Pass an image, audio, or video file's original path to the import tools, and only for assets you will place or reference.
5. If the index reports `truncated: true`, the omitted list is partial. Search the original folder for a specific named file instead of listing it all.
6. When the folder includes `subclip-video-scan-batches.json`, inspect its videos batch by batch as described below.

## Inspect attached videos safely

Raw video files are not copied into chat or agent context. An attached video, including a video found inside an attached directory, is represented by a `.subclip-video-context` directory with `README.md`, `video-context.json`, deduplicated storyboard JPEGs, and timestamped frame JPEGs.

Video links in a prompt (YouTube, Instagram, TikTok, Facebook, Vimeo and other recognized video sites) are not downloaded before your turn. When the request depends on what happens in the video (watch it, clip it, recreate it, caption it), call `fetch_linked_media` with the URL; the host may already be downloading it in the background, so it is often ready. It returns the same video context as an attachment: inspect its storyboards and manifest, then use its `originalPath` for requested imports or edits. A link given only as a reference or style example may not need the video. Never download a link yourself. X, Threads, Bluesky and LinkedIn links are handled as posts; see "Social post links" below.

1. Inspect the storyboard sheets and `video-context.json` first.
   - Open only the exact paths listed in `storyboards[].file` or `frames[].file`. Never construct a numbered storyboard filename from convention or from another clip; a short clip may have only `storyboard-01.jpg`.
2. Use the manifest timestamps and source-frame mappings when describing or editing the video.
3. Never read, copy, base64-encode, or upload the original video as prompt context.
4. If closer inspection is necessary, call `extract_video_frames` with the manifest's read-only `originalPath` and only the specific timestamps you need (up to 8 per call). It uses Subclip's bundled FFmpeg and returns the frames as images. Do not run FFmpeg in a shell for this, and do not create an unbounded frame dump.
5. When importing that video into Subclip, pass the manifest's `originalPath` to the import tool. The generated storyboard directory is analysis context, not the media source.
6. A video original discovered through the current context manifest is authorized for direct native import for the lifetime of that agent run. If native import fails because the codec/container is incompatible, call `import_attachment_clip_with_ffmpeg` once with the needed source range. If the bad original is already a timeline item, pass it as `replaceItemId` so its source is atomically swapped without changing its layout, lane, or timing. Store the returned background job ID and end the in-app agent turn without polling; Subclip resumes the same conversation when it becomes terminal. The job uses native system-or-bundled FFmpeg (never WASM), preserves the complete source in a cached compatible project-local MP4, and applies the range as a native non-destructive trim even when the agent sandbox cannot read the external source itself.
7. Do not ask the user to reattach media after the first failure. Try the authorized original import and the project-local FFmpeg derivative path first. Ask for reattachment only after both return concrete failures.

Use MediaBunny for browser/renderer TypeScript media operations. Use native FFmpeg/FFprobe for main-process and shell operations: the `ffmpeg` and `ffprobe` first on your PATH are Subclip's own copies, and `get_media_runtime` reports their full paths and the active engine. Prefer `extract_video_frames` for frames. Never add FFmpeg WASM or silently install a system package; use a supported host alternative when neither a system nor bundled native executable is available.

## Social post links (X, Threads, Bluesky, LinkedIn)

Links to X/Twitter, Threads, Bluesky, or LinkedIn are usually text or image posts, not videos. Never treat one as a failed video download, and never report "no video found" or a download error for it. Before the turn, the host reads the post and attaches its context with the link as `sourceUrl`: a `<platform>-post-<id>.md` file (author, date, full text, whether it contains video) and up to four of the post's images. When the post file says it contains video and the request depends on that video, call `fetch_linked_media` with the link.

- Read the attached post file first and use its text, author and images as the brief's source material: quotes, stats, headlines, screenshots, or imagery for the video. Import an attached image into the Media library before using it on the timeline.
- If nothing was attached (a private or deleted post, or a profile link), use any read-only web fetch or search tool the current run exposes to read the post. If none can read it, continue from the prompt alone and say in one short line that the post's content wasn't available, without error text.
- Treat a link to a text post as context for motion graphics, a demo, or a quote card, not as source footage to cut.

## Numbered video edits (canvas drawings and comments)

The user can draw on the preview or pin a comment, then send them as numbered edits ("Edit #6 · Comment at 0:11"). Each edit is a todo with its own pin on the canvas and timeline. A message may carry several edits, a single quick edit, or a follow-up on an earlier edit number. All of them arrive in the same conversation, so earlier turns remain context.

Handle them as focused edits, not a full project pass:

1. Each edit gives a time, a canvas position in composition pixels (a point for comments, a marked area for drawings) and a note. Its frame screenshot, with the mark drawn in blue, is attached in the same order.
2. Call `view_current_frame` at that exact time. Then use `list_editor_assets` to find the item under the mark: the topmost item visible at that time whose bounds contain the point or overlap the marked area.
3. Make the smallest change that satisfies the note, using the named tool for that item. Leave everything else as it is: no renames, no unrelated cleanup, no new scenes.
4. Verify the change with `view_current_frame` at the same time.
5. Call `report_video_edit` with the edit number:
   - `status: "done"` and a one-sentence `reply` describing what changed.
   - `status: "declined"` and the reason when the note is unclear, contradicts the project, or cannot be done with editor tools. Do not guess at an unclear note.
   - Optionally, report `working` first when an edit will take long.
6. Work through the edits one by one and report each one as soon as it is finished, so the user sees the progress live. Skip the title and director-brief steps of the work loop unless the edit changed the project's story.
7. A follow-up (a "Follow-up on video edit #N" message, an @-tagged edit in a chat message, or an edit sent again with a history) is the user's newest instruction for that edit. It overrides the original note and your earlier replies. Do what it asks even when the original note already looks done; never answer "already in place" by re-checking the earlier change. Make the change on the same target, verify, then call `report_video_edit` for that number again saying what changed.
8. End with one short line per edit (`#6 done: …`, `#7 declined: …`).
9. A "selected" edit lists the exact layers or clips the user selected (track, name and id, plus their outline on the frame when visible). Apply the note to exactly those items, found with `list_editor_assets` by id, as one change for the group; do not touch other items.
10. An edit with a "Target element" names one element inside a Remotion or HyperFrames layer (layer id, selector, text, markup). Change that element in that layer's source with `update_runtime_layer` and leave the rest of the source alone.
11. Canvas moves and resizes the user made by hand are kept separately: a Remotion layer's `elementEdits` (CSS `translate`/`scale` per selector), and a `<style data-subclip-element-edits>` block in a HyperFrames source. Keep both when you rewrite a layer, unless the user asks to reset them.

## Default aspect ratio

New projects without media start on a vertical canvas, so set the aspect ratio deliberately before building:

1. An explicit request (vertical, 9:16, Reels/Shorts/TikTok, square, 16:9, YouTube) always wins.
2. When the user imports or attaches a video that is the main subject of the edit (captions, cuts, rough cut, recording edit), keep that video's aspect ratio.
3. Otherwise, for motion graphics, animated explainers, product demos, launch or promo videos, and other prompts with no imported video as the main subject, use 16:9 landscape: call `set_canvas_properties` with `landscape` before adding layers, and pass `canvasPreset: "landscape"` to `create_project`.
4. Clipping long videos into shorts keeps its own 9:16 default (`$subclip-ai-clipping`).

## Route the request

1. Call `get_project_outline` with the run's `projectId`, then `read_project_section` for only the lanes, item IDs, and fields needed. Do not repeatedly read the whole project. Pass the last returned `revision` as `ifRevision` on subsequent reads; `{ unchanged: true, revision }` means your cached state still applies.
   - Use `get_project_director_brief` to read project-local `director.txt` as the concise cross-session source of truth. Reconcile it with live editor state rather than reconstructing intent from raw JSON alone.
   - When the user asks only to inspect or compare another saved project, use `list_projects`, then call `get_project_outline`, `read_project_section`, or `get_project_director_brief` with that exact project ID; inspection remains read-only.
   - When the user explicitly requests creating, cloning, or editing multiple saved projects, route to `$subclip-project-orchestration`. Cross-project write access is never implied by an ordinary single-project edit.
2. Resolve item IDs from the outline; request lane files with `read_project_section` when file IDs are needed. Large values remain `$ref` descriptors unless explicitly named in `fields`.
3. Load the smallest relevant internal skill:
   - Raster media or images: `$subclip-media-editing`
   - Text or subtitles visually between the original background and a foreground person/subject: `$subclip-text-behind-subject`
   - Remove an existing image or video background in Subclip Cloud: `$subclip-background-removal`
   - Public stock media, shared libraries, Freesound, or curated SFX: `$subclip-public-assets`
   - Create or revise images/backgrounds locally: `$subclip-asset-creation`
   - Generate persistent cloud images, videos, music, or speech with Subclip credits: `$subclip-ai-generation`
   - Music, voice, or sound: `$subclip-audio-editing`
   - First-pass spoken-video cleanup that removes dead air and filler-word media intervals: `$subclip-rough-cut`
   - Transcript-driven social highlight selection, candidate assembly, and intelligent reframing: `$subclip-ai-clipping`
   - Dynamic, viral, emphasized, word-by-word, or preset-based captions: `$subclip-dynamic-captions`
   - Captions designed as a HyperFrames layer (a named HyperFrames caption style, converting native captions into HyperFrames): `$subclip-hyperframes-captions`
   - Ordinary text overlays, transcription, subtitle correction, speaker labels, or basic caption styling: `$subclip-text-captions`
   - Aspect ratio, framing, or visual placement: `$subclip-canvas-layout`
   - Shapes, arrows, highlights, blur, paper, effect layers, or primitive keyframed graphics: `$subclip-elements`
   - Composed motion graphics, animated explainers, diagrams, visual timelines, or exact official SVG artwork: `$subclip-motion-graphics`, which builds scenes in HyperFrames by default, Remotion only on request, and HTML/CSS only for one small standalone effect
   - HyperFrames, GSAP, Lottie, or seekable HTML/JavaScript layer selected explicitly or by the motion router: `$subclip-hyperframes-layer`
   - Remotion, React/TSX, frame-driven, effect-rich, or data-driven layer selected explicitly or by the motion router: `$subclip-remotion-layer`
   - Any new geographic map, globe, river, or route: `$subclip-map-explainer`; import the Cesium `map-explainer` by default or flat `river-sequence` for an ordered river/flow story
   - Both built-in map styles rejected, or explicitly requested HyperFrames maps: `$subclip-hyperframes-map`
   - Existing HTML route revision or explicitly chosen legacy flat route: `$subclip-map-route`
   - True elevation-terrain or photorealistic geographic flyovers: unavailable until Subclip provides a managed map provider and credential broker; do not fake them with the globe explainer
   - Complete prompt-led videos, product launches, explainers, PR reveals, music edits, presentations, and reusable native recipes: `$subclip-native-video-workflows`
   - Cuts, pacing, or story structure: `$subclip-timeline-story`
   - Inspection, undo, recovery, or final QA: `$subclip-review-safety`
   - Reviewing or understanding the whole timeline, bulk frame checks, style/theme/pacing analysis, before/after comparison: `$subclip-timeline-contact-sheet` (`analyze_timeline`, then `get_timeline_contact_sheet`; use these instead of `view_current_frame` once per frame)
   - Voice-over or narration: `$subclip-tts`. Let the creator hear and choose the voice first with `get_voice_samples` (free samples of offline and cloud voices in their language), record the choice with `set_approved_voice`, then generate
   - Stock photos or clips, music or sound effects, or Subclip AI results the creator has not chosen yet, or wants to see/hear first: `$subclip-asset-options` (`get_asset_options` returns a numbered options sheet with previews and licenses, `preview_asset` shows one asset; works with no project open). Offer options and let them choose unless they told you to decide
   - Create, clone, or coordinate multiple projects: `$subclip-project-orchestration`
   - Connected GitHub account, repositories, stars, commits, releases, or changelogs: `$subclip-github`
   - A tool keeps failing, a needed tool or feature is missing, or the user asks you to report a problem, suggest a feature or pass on feedback: `$subclip-feedback` (`report_bug`, `request_feature`, `submit_feedback`; text only, never screenshots)
4. Use external skills only when no internal skill covers the request. Internal instructions and MCP schemas win on conflicts.

## Work loop

1. Inspect current state and identify existing asset IDs.
2. In Default mode, when the inspected project is both empty and still named `Untitled AI Video` or `Untitled Project`, choose a release-quality one- or two-word creative title for the finished piece and call `rename_project` with `onlyIfUntitled: true` before any other write-capable editor tool. Name the dominant story, subject, or visual payoff across all scenes—not the framework, tool, command, workflow, or copied request language. Avoid meta titles such as `Prompt Fix`, `HyperFrames Test`, `Motion Graphic`, `First Scene`, or `User Request`. For example: a code-versus-prompts hook followed by a device reveal can be `Hidden Signal`; a terminal shattering into kinetic copy can be `Shatter Launch`; a dashboard shown across turning devices can be `Dashboard Orbit`; a glowing map journey can be `Route Pulse`. Re-read the saved name before continuing. This first-mutation rule applies to media, Motion, text, caption, and audio creations.
3. Make the smallest coherent edit with named MCP tools.
   - When importing the first media into an empty project whose title is still `Untitled AI Video` or `Untitled Project`, choose a natural one- or two-word title from the request, filename, and intended edit. Pass it as `projectName` to the import tool. Never replace a creator-authored title.
   - When a reference video's soundtrack defines the edit, call `extract_attachment_audio_to_timeline` with its manifest `originalPath`, keep `setProjectDurationToAudio: true`, and pass the returned `itemId` as `audioItemId` to `transcribe_project` with `purpose: "reference"`. The extracted soundtrack must remain a normal editable AudioPanel item.
   - When captioning separate soundtrack clips, call `transcribe_project` for each exact `audioItemId` or `mediaItemId`, one terminal job at a time. The tool reads that item’s current trimmed source in/out range, offsets the resulting words to its timeline start, preserves caption batches from other sources, and replaces only an older batch for the same item. Do not manually offset a completed batch or clear existing captions first.
   - For screen-recording plus talking-head or ScreenStudio-style layouts, use `apply_screenstudio_layout` as one atomic edit. Do not perform presenter position, mask, mute, and z-order as separate mutations. Preserve the presenter's existing timeline duration; never loop or extend it to the tutorial end unless the user explicitly requests that timing change.
   - Treat pasted Remotion templates as design direction for the active Subclip project unless the user explicitly asks for a separate code project. For a split-screen scene, use `apply_two_way_split_scene` so UnifiedTimeline is physically split first and only the isolated middle segments receive new native container bounds. Use `add_media_keyframe` afterward only for motion/effects inside those segments.
   - For source in/out changes, use `trim_media_item`. It preserves the backing file's original duration so the user can extend or restore the clip manually later; never rewrite a MediaPanel file duration to match an agent-selected cut.
4. Prefer `update_media_item`, `update_audio_item`, `update_text_item`, and other named controls. Use `update_editor_state` only for properties without a named tool.
5. Re-read the project to verify the mutated state and exact timings.
6. Seek to every representative edited moment with the current `projectId`: shortly after each new layer starts, around every cut, and near the end of newly added media.
7. Call `view_current_frame` with that same `projectId` at each moment and inspect the returned live pixels. The tool does not substitute saved thumbnails. Tool success is not visual evidence.
8. Correct black space, off-canvas media, unintended crops, overlaps, unsafe text, missing layers, or bad hierarchy. Re-read, re-render, and inspect the corrected frame again.
9. Before finishing, compare the final asset inventory with the items that existed at the start of the run. Remove only superseded drafts, failed fallback layers, and accidental duplicates created by the current run. Keep pre-existing user work and intentional overlaps. For Motion-panel corrections, update the original item ID and use `delete_html_motion_graphic` for obsolete copies; do not stack corrected duplicates. Compare the project duration with the final intentional content end: the canvas background mirrors the project clock and must not create an unintended blank tail. Use `set_project_duration` after all timing edits, preserving only deliberate final holds.
10. Before finalizing any newly created edit, inspect the saved project name again. If it is somehow still untitled, call `rename_project`, re-read the project, and confirm the returned saved name. Never state that a project is “titled” or “renamed” from your intended title alone. Never replace a creator-authored title.
11. After the coherent edit and its verification, call `update_project_director_brief`, and before you finish call `write_session_summary` with `request`, `summary`, `did` and `openIssues` (see `subclip-project-log`; without it Subclip writes only a minimal automatic note). Keep a short current summary with: original content, the user's requirements, work completed, important creative/technical decisions, and pending or failed verification. Do not paste raw project JSON. Subclip maintains the exact technical inventory section automatically.
12. Report completion only when state and rendered frames both pass. If frame inspection is unavailable or a corrective action is cancelled, say verification failed; do not say the edit was completed.

Do not delete a project, restore history, start paid cloud processing, or export without explicit user confirmation. A direct instruction such as “export the video” is that confirmation: call `export_video` once, store its request ID, and end the in-app agent turn without polling. Subclip resumes the same conversation on completion, cancellation, or error. Chat-triggered export bypasses the manual Export settings dialog. Omit `startTime` and `endTime` for the complete video. When the creator requests only a segment, pass both the inclusive timeline `startTime` and exclusive `endTime` without trimming or changing the saved project, and pass a concise meaningful `outputFileName` for that segment. Never invent an export range the creator did not identify or authorize. For a complete export, omitting `outputFileName` uses the current saved project title. MCP-completed exports are automatically revealed in Finder. If the user says “export to the same directory,” resolve the explicitly referenced source file's parent directory and pass it as `outputDirectory`. Do not guess a directory when no source/location is identifiable. External MCP clients may use `get_export_status`.

Export and social publishing also require an active paid Subclip plan. The host checks fresh billing access before registering either render job. If `export_video` or `publish_video_to_social` reports that a paid plan is required, do not retry and do not claim anything was queued or published. Tell the creator to buy Subclip and provide [Subclip pricing](https://subclip.app/pricing).

For YouTube uploads, native schedules, Studio actions or clip batches, read `$subclip-youtube`; for cross-platform inbox, insights, activity, storage or publishing read `$subclip-social-media`. Existing files publish directly with `youtube_upload_file` or `publish_video_file_to_social`; timeline segments publish through `youtube_publish_segment` or `publish_video_segment_to_social`. Never clone projects or swap timeline clips solely for uploading.

Social publishing requires a separate, exact confirmation even if the user previously asked to export. Call `list_social_accounts`, select only an account the user named or approves, then show a concise confirmation summary containing: platform and account, post-now or scheduled time, an excerpt/summary of the captions rendered into the video, and every supporting field that will accompany it (YouTube title/description/tags/privacy, X post/thread/quote text, or Instagram caption/type/trial/cover time). X accounts include `displayName`, `username`, and `handle`: match a user-supplied name or handle case-insensitively and use that result's linked-account `id` for publishing. Never ask the user to choose a numeric provider account ID when exactly one returned name/handle matches. Ask the user to confirm that exact summary. Only then call `publish_video_to_social` with `confirmed: true` and the reviewed `captionSummary`. Store the returned request ID and end the turn without polling; Subclip resumes on success, failure, or cancellation. Never infer confirmation from an earlier edit or export request.

The named publisher is pre-authorized after its typed `confirmed: true` check. When `publish_video_to_social` returns `triggered: true` or `state: "queued"`, treat that result only as accepted—not as published—store its request ID, and end the turn. Subclip completes the agent run only after its durable publication record reaches a terminal state; an immediate post is successful only after the backend status and external platform ID/URL are verified. Report that proof when supplied by the terminal callback. Never report an approval-policy failure after a successful queued result. A policy failure may be reported only when it appears in the tool's actual error result.

Read [references/tool-map.md](references/tool-map.md) when choosing tools or serialized paths.
## Exact frame inspection

- `view_current_frame` can render any exact `timeSeconds` without relying on the visible playhead.
- Frames and exports render the saved project in the background. The project does not need to be open in an editor window, and the result always reflects the latest saved edit (see the returned `revision`). Do not call `open_project` just to verify or export.
- Set `targetType` to `media`, `text`, `element`, `motion-graphics`, `dynamic-captions`, `3d`, or `composition`. Include `itemId` when reviewing one timeline item.
- The tool validates the named item and renders the full composition so occlusion, layout, transparency, and cross-layer interactions remain visible.
- Inspect representative frames inside every scene or edited layer before claiming visual completion. Source checks and saved-state checks are not visual verification.
- Treat every explicitly requested layer as an independent completion requirement. For mixed 3D and text/media/elements/captions/motion requests, create and verify each one rather than stopping after the primary layer.
- For audible video inside a 3D screen, enable audio on the 3D screen binding. Do not create a separate audio timeline item unless the creator requests one.
- Authored Remotion layers must use `Audio` from `@remotion/media`; `Html5Audio` from `remotion` is unsupported by the web renderer.
- Remotion layers export through the client-side renderer, which drops CSS it cannot draw (`z-index`, `backdrop-filter`, blend modes, radial/conic gradients, CSS background images, inset shadows, `object-position`, `perspective`). Follow `subclip-remotion-layer` references/client-side-rendering.md and fix every "Export can't draw this" validator warning.

For generative changes to clip content (objects, colors, environment), route to `$subclip-video-generation` and discover `flux-video-edit`. Use ordinary timeline tools for trims/reframes. Talking portraits route to `$subclip-avatar-generation`; Avatar IV needs portrait AND supplied speech audio.

## Code-layer source edits

Use `read_layer_source` for numbered lines and `sourceHash`, then `edit_layer_source` with `expectedSourceHash` for unique exact-text replacements or inclusive line ranges. These tools validate and save through the project revision/history queue. Never write `project.json`, `data/*`, or `layers/*` using shell or filesystem tools. External source-file edits are rejected on the next read; restore the saved file before continuing. Full replacements through `update_runtime_layer` and `update_html_motion_graphic` remain supported. HTML Motion source has a leading `<style>` block followed by its HTML; retain that structure.
