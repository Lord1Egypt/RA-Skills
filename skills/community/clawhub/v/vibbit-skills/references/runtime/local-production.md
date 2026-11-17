# Local production planning and reuse

`scripts/production.js` uses Node 18 and standard libraries to validate a [production plan](../contracts/production-plan.md), track selected artifacts, bind measured words to frames, and explain reuse. It does not call an API, install tools, transcribe, generate media, or render video.

Examples: [project](../../examples/production-project.json) and [run](../../examples/production-run.json). Their claims and timings are fictional examples, not user product facts. Produce the speaker first, then the final video.

## Paths and immutable receipts

Project inputs resolve from the project file's directory. The run's project, receipts, and timing paths resolve from the run directory. Receipt media paths resolve from the receipt directory. CLI paths resolve from the current working directory; use absolute paths when ambiguity matters. Outputs are not overwritten.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/production.js" plan --run /absolute/project/production-run.json
node "$VIBBIT_SKILL_DIR/scripts/production.js" record --run /absolute/project/production-run.json --output-id speaker --file /absolute/project/assets/speaker.mp4 --out /absolute/project/speaker-v1.receipt.json
~~~

`plan` returns reuse/execute decisions. It is read-only and does not verify account access, credits, or creative quality. Prepare missing inputs or select an intermediate target.

`record` hashes real local bytes. Optional task/result IDs must be real; recording does not query them. A remote preview is not a pinned local artifact. Select the receipt in the run, for example `"speaker": "speaker-v1.receipt.json"`, and plan again. Explicit clips must be actual files, not renamed whole videos.

Keep unaffected selected receipts. Changed bytes, incompatible declared dependencies, and mismatched inputs invalidate reuse. The tool does not clear selections or generate replacements. Downstream work requires the selected upstream artifacts.

## Measured speech timing

Accurate word binding requires actual word-level transcription/alignment. The public breakdown API returns segments, not word alignment. Do not evenly divide a segment or invent word times.

Audio ASR can be normalized from milliseconds and exported to valid word input using [transcript tools](transcript-tools.md). Missing or zero-duration words block word export while valid sentence SRT/VTT remains usable. Verify source, adopted media, and edit relationships before import. Audio and avatar video have different hashes; never replace a hash to bypass identity checks.

A timing import uses `version: 1`, `time_unit: "seconds"`, and `words: [{text, start, end}]`. An optional `media_sha256` ties the claim to media bytes; it does not prove how the transcription was obtained.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/production.js" import-timing --file /absolute/project/assets/speaker.mp4 --transcript /absolute/project/asr-words.json --language en --out /absolute/project/timing-v1.json
node "$VIBBIT_SKILL_DIR/scripts/production.js" bind --run /absolute/project/production-run.json --out /absolute/project/events-v1.json
~~~

Import uses ffprobe to check the real audio stream, duration, word ranges, and hash. Binding rounds ranges outward to frames and moments to the nearest frame. Repeated phrases require an explicit occurrence; edges use measured word boundaries. The complete speech word order must match the measured transcript.

The host adapts bound events to the chosen renderer; engines do not share a universal event format. Declare the event file and relevant project files as dependencies. After selecting the speaker, set the final target, execute the real renderer, review the export, and record it.

Changing speech media requires a new selection, timing, and events. Style-only changes can reuse valid timing. Use new paths for revisions.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/production.js" explain --run /absolute/project/run-v2.json --out /absolute/project/diagnosis-v2.json
~~~

`explain` returns `read_only_diagnosis` with reuse/execute/blocked decisions and relevant fields, files, and dependencies. Older receipts without input summaries cannot support detailed change explanations. `ready_for_host_review` is false when blocked. Diagnosis does not mutate the run. For an authorized caption revision, a new run can drop the obsolete final selection while preserving costly unaffected performance media and the previous run.
