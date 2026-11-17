# Creator-led and digital human talking-head videos

Start from the user's current topic, script, original audio, or existing performance, and deliver the requested script or video. Digital humans are one production option; preserve an existing human performance when only postproduction is needed.

## Enter from the available input

- Topic only: establish the message and voice, then check audio/avatar/final-assembly dependencies.
- Adopted script: preserve it and proceed to sound or existing audio.
- Audio plus valid avatar ID: use [digital human video](../capabilities/generation/digital-human-video.md) directly.
- Local audio: upload the actual file to a readable URL; accessible audio URL: reuse it directly.
- Submitted audio task: query it and use the real completed result instead of generating again.
- Existing talking-head video: preserve picture/voice and add only the requested B-roll, captions, or editing.
- Avatar tryout without a selection: query existing [digital humans](../resources/digital-humans.md), show all returned entries and available previews with recommendations marked, or choose within existing delegated permission. Bind the selected original record's name, ID, and cover. A tryout does not imply cloning.

Upload is a necessary step already implied by an instruction to use a local audio file to drive an avatar. Use the supported Vibbit transfer path; a local path cannot be `audio_url`. If upload fails, retain the original and selected avatar instead of generating substitute speech.

## Identity and expression

Reuse established creator identity, adopted scripts, and sample style. Distinguish stable identity from the current topic/emotion. Do not invent biography, experience, expertise, or endorsements. A fictional role remains fictional.

Make tone concrete through vocabulary, sentence length, pauses, and explanation depth. Do not turn every topic into sales copy, force a CTA/twist, or fill speech with verbal tics. B-roll should aid understanding and preserve important expressions/actions.

For new writing, use [creative direction](../creation/creative-direction.md) and one adopted script linked to voice, captions, and lip sync through [handoff](../contracts/creative-handoff.md). Existing audio needs no forced transcript, voice selection, cloning, denoising, or rewritten script.

## Generate and resume

Check downstream avatar and media requirements before paying for audio. For text-only digital human narration, use [audio generation](../capabilities/generation/audio-generation.md) to generate the exact selected speech, continuous background music, and restrained effects together by default. Existing audio and explicit speech-only or separate-track requests take precedence. Use real references only when needed; ordinary voice style needs no voice-list API.

Wait for actual completed audio and adopt it before avatar generation; resolve known audio defects before paying for dependent lip sync. Pass its existing URL directly with a real `digital_human_id` to [digital_human_video](../api/digital_human_video.md). Check that ID against the selected original record once, preserving it as a string. A valid ID or unique name match can proceed without repeated selection.

Save each actual task ID and query the original job after a timeout. Do not replace video generation with project initialization or a project-page URL. Browser operation is appropriate only when the user actually requests it. This workflow delivers video, not an automatically saved editable platform project.

Current avatar input is audio URL plus avatar ID; creative wardrobe, scene, camera, expression, and gesture directions are not exposed controls. [Role strategy](../platforms/meta/role-play.md) is optional for a new Meta creator concept, not a prerequisite for driving an existing avatar.

## Full video and focused changes

For B-roll, charts, editing, or templates, treat the completed performance as real input to [hybrid production](hybrid-video.md). Reuse audio and avatar output when only postproduction changes. Download remote media only when a local project needs it.

Ordinary captions use [correction and segmentation](../capabilities/processing/subtitle-addition.md) with real segment times. Segment-level B-roll can share that timeline. Only word-specific graphics/highlighting use [semantic timing](../creation/script-and-timing.md) and real word evidence; segment ASR cannot be evenly split into exact words. Repeated revisions may use [production planning](../contracts/production-plan.md).

## Avoid repeating work

- Once the script is adopted, audio generation can run alongside authorized image/video B-roll and chart-template preparation that does not depend on final timing. Set exact duration and placement after audio adoption. An avatar-only request needs no forced captions or B-roll.
- Submit the avatar after audio adoption. When speech needs checking, first [transcribe that audio](../capabilities/analysis/speech-transcription.md), save one record with [transcript tools](../runtime/transcript-tools.md), compare adopted speech, and listen to uncertainties; captions/B-roll share the result. If only caption timing is needed and audio checks have passed, transcription can run alongside avatar generation; reuse sentence/word timing after verifying soundtrack and edit relationships. Do not render audio known to need replacement; new audio needs new transcription.
- Reuse versioned checks through [shared review](../capabilities/analysis/video-review.md). Unchanged speech, avatar selection, and media metadata need not be rechecked by each subworkflow. Final composition still needs checks for newly introduced captions, visuals, and audio/video relationships.
- Download only when local assembly needs the media; reuse local copies and probe results. Caption, chart, and B-roll edits preserve narration and avatar footage.
- In existing task records, retain stage start/end times and generation counts, separating service waits, transfer, production, and checks. Parallel task durations do not add up to wall time. Continue unchanged jobs through [task waiting](../runtime/task-lifecycle.md), without rereading instructions, replanning, or authenticating at every poll.

Resume the selected script/audio, avatar, results, and unresolved issues. A next episode reuses stable identity but needs its own content. A changed line affects its sound, lip sync, captions, and duration; disclose when the available API requires regenerating a whole performance. A new avatar can reuse approved sound. A B-roll/caption/music revision affects its own postproduction layer. Diagnose “unnatural” as wording, voice, lip sync, or performance before changing anything.

Include actual speech, identity, key lines, lip sync, captions, and supporting visuals in the same [review](../capabilities/analysis/video-review.md), reusing applicable intermediate checks instead of starting another complete review. A static preview cannot establish synchronization. Script-only delivery needs script review; an unfinished video remains an active task.
