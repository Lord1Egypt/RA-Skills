# Vibbit cloud editing and local production choices

Default ordinary editing, material mixcuts, and caption/packaging assembly to Vibbit cloud `MEDIA_PRODUCTION`, without requiring customer-side FFmpeg or a locally rendered body. Respect an explicit local choice or an existing local project. Remotion/Hyperframes can prepare necessary programmatic animation; cloud composition does not run these engines. [Agent semantic mixcut](semantic-mixcut.md) supplies reference templates, selection, and audio/picture planning.

| Goal | Route |
| --- | --- |
| Existing media; simple cuts, joining, overlays, mixing, ordinary captions | Vibbit cloud by default; existing FFmpeg for an explicit local choice |
| Installation declined | Direct Vibbit cloud composition using existing media |
| Programmatic full video with ordinary music/captions | Complete local project and export |
| Specifically requested Vibbit subtitle/packaging style | Available body/clips plus the required cloud step |
| Explicit cloud editing of existing video | Direct cloud media; prepare only genuinely missing assets |
| B-roll/overlay only | Deliver that asset; assemble a full video only if requested |

“Add captions” does not inherently mean Vibbit cloud captions. Respect explicit local/cloud choices. Explain a real conflict between local-only delivery and a specific cloud-only style.

An installation refusal applies throughout the task: do not substitute temporary downloads or repeatedly propose another installer. Use installed tools only within the user's permission. Lack of installation alone is not a refusal.

For library media, use [material reuse](../resources/materials.md) to obtain current original/clip URLs and map them to the chosen local or cloud tracks. Trim verified source intervals only when clip files are unavailable. Refresh expired signatures and reuse local copies/probes, without reuploading, reimporting or regenerating usable media.

## A. Complete locally

Use this for an explicit local choice or an existing local project. Installed tools alone do not override the cloud default.

Use [FFmpeg](../capabilities/processing/local-composition.md) for simple composition or [programmatic rendering](../capabilities/generation/programmatic-video.md) for an animation project. Arrange real video, audio, graphics, and captions on one timeline. Retrieve cloud assets locally only when needed.

Verify the exported media and deliver it. Preserve the animation project or FFmpeg inputs/parameters. Upload only if requested or required downstream. Uploading an MP4 does not create editable React/HTML layers in Vibbit.

Captions do not always require ASR: reuse applicable SRT/VTT or verified recognition; a script without timing needs evidence for adopted audio. Export sentence captions with [transcript tools](../runtime/transcript-tools.md), then use actual post-production tools. File export is not completed composition and does not establish arbitrary cloud subtitle-file support. Caption/packaging edits with unchanged speech reuse recognition.

## B. Local body, cloud subtitles or packaging

Before making paid intermediates, verify [compose](../capabilities/processing/media-composition.md), required subtitle/template configuration, upload, and account access.

Export a completed body when only packaging remains; separate clips are necessary only if cloud assembly needs them. Keep wanted in-picture text and data labels, while avoiding duplicate postproduction layers.

Upload actual files and verify readable URLs. Library registration is separate and unnecessary for composition that accepts URLs directly. Use real subtitle text/timing; distinguish recognition time, source-clip time, and final placement.

Submit actual media URLs, intervals, audio choices, and supported template/track configuration. Engine names, local paths, and React/HTML project parameters are not cloud media inputs. Resume the returned task ID and report completion only when the actual final media is ready.

## C. Direct cloud composition

This is the default for ordinary editing and semantic mixcuts, including when local installation is declined.

Reuse accessible URLs, or use the supported [upload path](../runtime/media-inputs.md) for local files. Do not require local transcoding first when installation was declined. Use an available client or host API tool.

Cloud selection does not itself solve missing authentication, upload access, or nested track contracts. The CLI checks only part of the payload. Upload credentials alone are not a completed transfer; `upload_info --file` transfers bytes but does not register a library object. A template list provides candidates, not guaranteed application configuration.

Cloud composition cannot substitute for missing complex animation without an appropriate capability. Identify the exact gap and retain existing work. Do not silently replace a requested effect with generative video or a local imitation of a specific Vibbit style.

## Jianying draft delivery

For requested drafts, first check [desktop export eligibility](jianying-draft.md). Current OpenAPI cannot supply the required Job ID. Without a separate valid ID, retain outputs/recovery records and report draft export unavailable; client installation does not fix the ID gap. Proactively guide official installation when absent. Only a real ID enables task-prefilled launch and a user save. Disclose limitations before paid production when only a draft is wanted; an additional draft blocker does not prevent delivery of the completed video. Cloud editing remains the default.

## Revisions

Review the actual final export, including cloud-packaged media, through [video review](../capabilities/analysis/video-review.md). Change data/text/animation in the source project; change cloud intervals/order/packaging through supported composition fields. Retain unaffected sound, clips, and existing tasks. A cloud packaging failure does not require remaking a completed local body.
