# Official HyperFrames skill snapshot

Installed from the HyperFrames-maintained `heygen-com/hyperframes` repository at commit `05b57f9204a963104f1f79ef88ffc24cd174fd68` on 2026-09-03 using the official Codex skill installer.

The upstream files are preserved under `references/official/`. Only the curated paths listed by this index and accepted by `read_subclip_skill` are readable. The broader router, workflow routes, CLI execution, media/TTS/transcription, registry installer, package-install, and unsupported-runtime documents are intentionally blocked. Curated files provide composition, design, typography, choreography, GSAP, and Lottie guidance inside one Subclip layer. The current official registry catalog and item source are discoverable separately through Subclip's read-only registry tools; reviewed built-in adaptations are documented under `references/registry/`.

## Required reading for non-trivial layers

Read these with `read_subclip_skill` using `skillName: "subclip-hyperframes-layer"`:

1. `references/official/hyperframes-core/references/minimal-composition.md`
2. `references/official/hyperframes-core/references/data-attributes.md`
3. `references/official/hyperframes-core/references/determinism-rules.md`
4. `references/official/hyperframes-creative/references/house-style.md`
5. `references/official/hyperframes-creative/references/video-composition.md`
6. `references/official/hyperframes-animation/rules-index.md`
7. One relevant allowlisted rule, blueprint, or runtime adapter—do not load the entire catalog. If a path is rejected by `read_subclip_skill`, it is deliberately incompatible with the embedded layer; choose an allowlisted technique instead.

## Topic routes

| Need | Official resource |
| --- | --- |
| GSAP mechanics | `references/official/hyperframes-animation/adapters/gsap.md` |
| GSAP easing/stagger | `references/official/hyperframes-animation/adapters/gsap-easing-and-stagger.md` |
| Timeline labels/phases | `references/official/hyperframes-animation/adapters/gsap-timeline-and-labels.md` |
| Transform performance | `references/official/hyperframes-animation/adapters/gsap-transforms-and-perf.md` |
| Lottie | `references/official/hyperframes-animation/adapters/lottie.md` |
| Three.js/WebGL | `references/official/hyperframes-animation/adapters/three.md` |
| Multi-phase choreography | `references/official/hyperframes-animation/blueprints-index.md` |
| Atomic motion recipe | `references/official/hyperframes-animation/rules-index.md`, then one matching file under `rules/` |
| Typography | `references/official/hyperframes-creative/references/typography.md` |
| Stats/dataviz | `references/official/hyperframes-creative/references/data-in-motion.md` |
| Curated money counter | `references/registry/apple-money-count.md`, then template ID `apple-money-count` from `list_runtime_layer_templates` |
| Any official registry item | `list_hyperframes_registry`, then `get_hyperframes_registry_item`; adapt and validate rather than install |
| Visual style | `references/official/hyperframes-creative/references/visual-styles.md`, then one palette if needed |
| Beat planning | `references/official/hyperframes-creative/references/beat-direction.md` |
| Design QA | `references/official/hyperframes-creative/references/design-adherence.md` |
| Converting Remotion to HyperFrames: API equivalents | `references/official/remotion-to-hyperframes/references/api-map.md` |
| Remotion `useCurrentFrame`, `interpolate`, `spring`, `Easing` | `references/official/remotion-to-hyperframes/references/timing.md` |
| Remotion `Sequence`, `Series`, `Loop`, `AbsoluteFill`, `Freeze` | `references/official/remotion-to-hyperframes/references/sequencing.md` |
| Remotion props, `defaultProps`, `calculateMetadata` | `references/official/remotion-to-hyperframes/references/parameters.md` |
| Remotion `Audio`, `Video`, `Img`, `staticFile` | `references/official/remotion-to-hyperframes/references/media.md` |
| Remotion `TransitionSeries`, `@remotion/lottie`, fonts | `references/official/remotion-to-hyperframes/references/transitions.md`, `lottie.md`, `fonts.md` |
| What a Remotion conversion cannot port | `references/official/remotion-to-hyperframes/references/limitations.md` |

The `remotion-to-hyperframes` references were added on 2026-10-25 from the same repository (skill folder hash `40999548d5dd34f488f2529aaefd3cdeceb0577a`). Only its API-mapping references are included. Its CLI snapshot/render-diff steps, lint scripts, test corpus and React hosting escape hatch are not bundled. If your host has a terminal, you can install the full skill or CLI there (`npx skills add heygen-com/hyperframes --skill remotion-to-hyperframes`, `npx hyperframes snapshot`) and compare against a render of the original in a scratch folder. Either way, finish by validating the layer and comparing preview/export frames against the original Remotion layer.

## HyperFrames 0.9.32 design references

Added from the upstream `hyperframes` skill (commit 5073100, 2026-11-11). Only the design references are bundled: motion, captions, overlays, sound, look, film, format, spec, story, runtimes, and `types/` (character, data, explainer, 3d, launch, music, vertical). Each file begins with a Subclip override note. Its command-line, Studio, cloud and plugin steps are not run inside Subclip.

| Need | Resource |
| --- | --- |
| Motion principles | `references/official/hyperframes/references/motion.md` |
| Captions and subtitles | `references/official/hyperframes/references/captions.md` |
| Overlays and lower thirds | `references/official/hyperframes/references/overlays.md` |
| Sound design | `references/official/hyperframes/references/sound.md` |
| Look and grade | `references/official/hyperframes/references/look.md` |
| Film and format | `references/official/hyperframes/references/film.md`, `format.md` |
| Spec, story and runtimes | `references/official/hyperframes/references/spec.md`, `story.md`, `runtimes.md` |
| Video type guides | `references/official/hyperframes/references/types/*.md` |

## Reverse any video

Added from the HyperFrames app's vendored `reverse-any-video` skill (release 0.9.23, commit `7ad2be96a`, vendored 2026-11-08). Bundled under `references/official/reverse-any-video/`: `SKILL.md` is the entry point, and `references/` holds `start.md`, `animated.md`, `people.md` and `match.md`. Each file begins with a Subclip override note. The CLI, cloud render, HeyGen re-shoot, plugin, Pro-plan and credit steps do not run in Subclip; the note maps them to Subclip tools.

| Need | Resource |
| --- | --- |
| Reverse a video (entry point) | `references/official/reverse-any-video/SKILL.md` |
| Opening and handover | `references/official/reverse-any-video/references/start.md` |
| Painted or 3D animated films | `references/official/reverse-any-video/references/animated.md` |
| Re-shooting people (HeyGen steps replaced by a sub-asset cut unless the person approves) | `references/official/reverse-any-video/references/people.md` |
| Matching drawn layers (timing, type, look) | `references/official/reverse-any-video/references/match.md` |

**Always make a contact sheet first.** Before rebuilding any video with this skill, make contact sheets covering the whole video: grids of frames sampled across its full length, so every shot, cut and transition is visible. Use them to plan the shot list and the timeline before the frame-by-frame checks. Method reference: `/private/tmp/claude-501/-Volumes-Projects-prod-app-Subclip/e153c06e-89a7-4083-a2d4-73701d706c2a/scratchpad/yt-frames/sheet-1.png`.

- **Build:** sample one frame per second with ffmpeg (`fps=1,scale=320:-1,tile=6x4`, 24 cells per sheet) in the session scratchpad. Subclip's `extract_video_frames` returns images only, so it cannot assemble a sheet file.
- **Cover the whole video:** one sheet holds 24 seconds. For a longer video, make `sheet-1`, `sheet-2` and so on, each covering the next 24 seconds, until the last frame of the video is included. Do not stop at one sheet.
- **Store and reference:** import every sheet into the Subclip project media library with `import_attachment_to_project_media`, then record each sheet's file name, time range and asset ID in the project director brief, so later sessions can find and reference them without rebuilding.
- **Check:** confirm each sheet appears in `list_editor_assets` before the layer work starts.

Cloud render: when a route calls for it, use Subclip `export_video`, which renders natively. Say so if a different render path is needed.

## Subclip compatibility overrides

- Supported authored animation runtimes are native HTML/CSS, pinned GSAP and Lottie, plus pinned Three.js `0.181.2` through the deterministic `hf-seek` adapter. The full current official registry may be inspected through the read-only registry tools, but no item is installed automatically: adapt only supported behavior into the standalone layer contract. Reviewed templates explicitly returned by `list_runtime_layer_templates`, currently including `apple-money-count`, are ready for direct use. Anime.js, WAAPI add-ons, TypeGPU/WebGPU, shader-transition, post-processing/addon, and arbitrary package-install instructions remain unavailable.
- The official core's root/timing/determinism/GSAP rules apply. Subclip supplies the stored item, preview, producer call, transparent WebM proxy, and final composition.
- Upstream media/audio/project workflows do not supersede Subclip Media, Audio, Captions, or export tools.
- The snapshot's commands and scripts aren't run by the editor. You may run the official HyperFrames CLI or scripts in your own terminal and scratch folder when your host allows it (for example to render and compare a port frame by frame), then import the finished result through the runtime-layer tools.
- Normalize GSAP examples to 3.15.0 and Lottie examples to 5.13.0 on jsDelivr/unpkg before validation. dotLottie is unavailable.
- Upstream services never own Subclip Media, Audio, Captions, TTS, transcription, generation, dubbing, maps, preview, or export.

HyperFrames is Apache-2.0 licensed; the included license is at `references/official/LICENSE`.
