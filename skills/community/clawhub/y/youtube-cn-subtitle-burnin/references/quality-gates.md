# Quality Gates

Use this file before accepting a subtitle or video output. A failed gate blocks delivery unless the user explicitly accepts the limitation.

## Automatic Gates

- No subtitle time overlap.
- No empty subtitle text.
- No accidental duplicate active subtitles in ASS.
- No short flashes below the chosen threshold unless they are intentional one-word reactions.
- No screen ending with dangling connectors or incomplete predicates.
- No screen ending with punctuation that leaves the sentence visibly unfinished, such as `，`、`、`、`：`、`；`.
- No screen remains too long or visually dense after dangling-ending repair.
- No line break splitting product names, English phrases, code/commands, number-unit pairs, or common Chinese meaning chunks.
- No visible newline artifacts such as a stray `N` where an ASS line break should be.
- ASS subtitle style matches a fixed profile and includes the style version comment: `zh-only-default`, `zh-only-raised`, `bilingual-default`, or `bilingual-raised`.
- Raised subtitle profiles are used only when the default bottom placement would cover important source content, and the reason is recorded.
- Bilingual ASS has Chinese above English, Chinese at most two lines, English at most one line, and no missing English line for active Chinese cues.
- Bilingual output defaults to Chinese-primary / English-auxiliary layout: English must be visibly smaller and must not make the block feel crowded in preview frames.
- Bilingual alignment report exists and includes opening, midpoint, ending, and dense-speech samples for meaning and voice-timing review.
- MP4 has valid duration, video stream, audio stream, and expected resolution.
- ffmpeg subtitle burn support is checked before full burn; if native subtitle filters are unavailable, the reusable PIL fallback renderer is used and recorded.
- A subtitled preview clip exists before full burn.
- The preview clip contains at least one visible subtitle cue; if the selected one-minute range has no subtitles, the preview duration or window is adjusted.
- Source-video subtitle check frames exist before final layout selection.
- Design confirmation frames exist before full burn.
- Review screenshots can be extracted from the final MP4.
- Original YouTube description is extracted and retained.
- If the original description is not Chinese, a Chinese translated description is retained.
- Original video thumbnail is downloaded and retained.
- Cover edit preference is recorded before delivery.
- If cover editing/localization is requested, edited cover exists in `07-cover/` and the original thumbnail remains unchanged.
- Cover mode is recorded as `preserve-original-text`, `translate-original-text`, or `localized-rewrite` before editing starts.
- Edited cover preserves all original thumbnail text exactly as-is unless the recorded cover mode allows translation or localized rewriting.
- Edited cover includes `中文字幕` and YouTube author/source information with the fixed prominent-label/secondary-source treatment.
- Edited cover has a 320px preview and the preview is checked for readability.

## Visual Gates

- Subtitle must be readable on phone-sized playback, not just desktop.
- Text must be strong enough against bright and dark backgrounds.
- Font size, outline, vertical position, and line breaks must be approved from preview screenshots before full burn.
- Preview and design frames must be checked against the fixed style profile, not only against subjective readability.
- For bilingual output, design confirmation frames must show Chinese above English and the subtitle area must not exceed the three-line default unless a documented exception is accepted.
- For bilingual output, first-minute preview frames must be checked for stray `N`, cluttered English, and Chinese/English pacing mismatch.
- Full video generation must wait for user approval of the subtitled preview clip unless the user explicitly waives this step or asks the agent to handle the job end to end. In direct-completion mode, preview screenshots must be self-checked and recorded.
- Subtitle must not cover faces, code, chart labels, important product UI, or bottom controls.
- If the source video already has burned-in English subtitles, default to Chinese-only and avoid the original subtitle area unless the user explicitly requests bilingual output.
- If the video is a software tutorial, inspect bottom input boxes, status bars, and right-side presenter overlays.
- Edited cover text must be readable at thumbnail size and must not cover faces, important UI, product signals, or the original main title.

## Language Gates

- Meaning is faithful to the original.
- Chinese is natural and watchable.
- For bilingual output, sampled Chinese meaning, English reference, and spoken audio timing must correspond closely enough that the viewer does not feel the lines are from different moments.
- Technical terms and names are consistent.
- Description translation preserves proper nouns, product names, URLs, and chapter timestamps.
- Negation, numbers, time, conditions, and confidence level are preserved.
- Long English sentences are converted into readable Chinese semantic screens.
- Subtitle line breaks preserve readable Chinese and keep protected terms intact.

## Known Reusable Failures

| Issue | Failure signal | Preventive action |
|---|---|---|
| YouTube overlap | Multiple cues active at once; previous line remains onscreen | Run overlap check before ASS generation and repair to non-overlap timing |
| Too fragmented | Frequent one-second flashes; reading feels jumpy | Merge related cues into semantic screens |
| Half-sentence screens | Screen ends with connector or unfinished predicate | Rebuild screens around complete sentences or closed meaning blocks |
| Incomplete punctuation screens | Screen ends with `，`、`、`、`：`、`；` even though the thought continues | Merge with the following cue or split again at a complete semantic boundary |
| Long dense screens after repair | Dangling-ending repair passes, but a subtitle still holds too much text or stays too long | Split long repaired cues by Chinese semantic punctuation and re-check readability |
| Subtitle too small | Looks acceptable on desktop but tiring on phone-sized playback | Require preview screenshots and adjust size/outline before full burn |
| Style drift between videos | Font size, outline, or vertical position changes across jobs without a reason | Generate ASS with a fixed style profile and run `check_subtitle_style.py` |
| Preview without subtitles | One-minute preview shows no subtitle, so user cannot judge style | Extend duration or move preview to a subtitle-bearing window before asking for approval |
| Bottom UI occlusion | Subtitle covers input fields, controls, code, chart labels, or lower-third text | Move subtitle upward, reduce line count, or use a safer region for that segment |
| YouTube translated caption rate limit | Chinese timedtext download returns HTTP 429 or repeated subtitle download errors | Stop repeated retries, use English captions, translate with the current agent model, and record the source limitation |
| External translation detour | Workflow tries APIs/tools even though the current agent model can translate | Use the current agent model as the default translator; external APIs/tools are fallback only |
| Translation batch drift | Long video translation misses ids, reorders subtitles, or cannot resume after interruption | Use numbered JSON batches, verify all ids, and save cache after every batch |
| Unstable cue ids | Cleaned captions are resegmented, then translation cache is matched against position-only ids | Keep stable `id` values in cue JSON and use those ids for batching/cache application |
| Hard character wrapping | Line break cuts product names, English phrases, or Chinese meaning chunks | Generate ASS with semantic wrapping and check line breaks from preview frames |
| Visible newline marker | ASS line break escaping is damaged and viewers see a stray `N` in the subtitle text | Run subtitle quality checks for visible newline artifacts before preview and full burn |
| Bilingual clutter | English line is treated like a second main subtitle, making the result harder to read than Chinese-only | Use Chinese-primary / English-auxiliary layout, with smaller English and preview-frame checks |
| Bilingual pacing mismatch | Reviewed Chinese semantic screens are paired with fragmented rolling English, making the two lines feel unrelated | Keep Chinese semantic timing by default; compare a matched-boundary preview only if it does not fragment Chinese |
| Missing bilingual alignment review | Timing checks pass, but no one sampled whether Chinese, English, and speech line up | Run `check_bilingual_alignment.py` and review the generated samples before final burn |
| Bilingual subtitle block too tall | Chinese already takes three lines, then English is added below | Repair or split Chinese subtitles before generating bilingual ASS; default maximum is Chinese two lines plus English one line |
| Duplicate English subtitles | Source video already has burned-in English subtitles and bilingual mode adds another English line | Extract source subtitle check frames and default to Chinese-only when burned-in English is visible |
| Missing design approval | Full video is burned before the user sees representative subtitle design frames | Extract 3-5 design confirmation frames from the preview and get approval or self-check in direct-completion mode |
| Missing ffmpeg subtitle support | Full burn fails because ffmpeg lacks ass/subtitles filters | Run ffmpeg subtitle support check before preview/full burn and switch to a libass-capable build |
| One-off fallback renderer | Project contains a temporary burn-in script that is not reusable next time | Use `scripts/burn_subtitles_pil.py` for fallback hard subtitles and keep renderer changes in the skill |
| Missing thumbnail | Video is delivered without saving the YouTube cover | Download and retain the thumbnail during source acquisition |
| Missing description | Video is delivered without saving the YouTube description | Extract and retain the original description during source acquisition |
| Description translation loses names | Chinese description translates product names, URLs, or timestamps incorrectly | Preserve proper nouns, product names, URLs, and chapter timestamps while translating surrounding text |
| Unclear cover preference | User may expect a Chinese-subtitle cover but the workflow never asks | Ask whether the thumbnail/cover should be prepared during intake and record the answer |
| Unclear cover mode | Cover copy gets translated, preserved, or rewritten inconsistently across videos | Record `preserve-original-text`, `translate-original-text`, or `localized-rewrite` before editing starts |
| Original cover text changed | Existing thumbnail wording is translated, rewritten, erased, or replaced without explicit user request | Keep original cover text unchanged; add only `中文字幕` and author/source information |
| Missing cover author | Edited cover only adds `中文字幕` and omits the YouTube author/source | Add compact author/source text such as `作者：<channel>` or `<channel> · @handle` |
| Cover thumbnail unreadable | Full-size edited cover looks acceptable, but labels fail at YouTube thumbnail size | Generate and inspect a 320px preview before delivery |
| Cover text blocks key image | Added Chinese label or author text covers a face, product signal, or title | Place cover text in empty space, use compact YouTube-style labels, and visually inspect before delivery |
| Edited cover not retained | Cover was generated but not copied into the project outputs | Copy edited cover into `07-cover/` with a versioned filename and keep the generator original in place |
| Accidental overwrite | Re-running a script replaces a previous MP4/SRT/ASS output | Choose a new versioned filename; only use force overwrite for scratch tests |

## Adding New Gates

When user feedback is reusable across future videos, add a new row above with:

- issue name
- failure signal
- preventive action

Then add the corresponding workflow step to `workflow.md`.
