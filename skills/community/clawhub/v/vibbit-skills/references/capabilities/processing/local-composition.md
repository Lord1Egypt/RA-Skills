# Local media composition

Use an available FFmpeg installation for trimming, joining, resizing/padding, images, mixing, subtitles, and complete media assembly when no animation project is needed. Local work needs no Vibbit API key. If installation is declined, use an appropriate cloud route unless existing local tools are allowed.

Inspect executable versions, encoders/filters, and actual media streams, dimensions, sample aspect ratio, frame rate, duration, and audio. The render doctor does not have an FFmpeg engine mode or prove render success. Distinguish source intervals, target placement, and audio handling; generation minimum durations do not apply to ordinary cuts.

Use new output paths and track the actual process/logs. Stream-copy concatenation requires compatible streams. Reset timestamps for filter composition and explicitly select streams so desired audio is not dropped. Accurate cuts may require re-encoding. Handle audio tails, padding, constant frame rate, and mix duration deliberately; blindly using `-shortest` can truncate content.

Subtitle rendering needs appropriate filters such as libass, fonts, and real text/timing. It is not a Vibbit cloud template. Keep user text in separate files and use the appropriate filter/path escaping. Relax concat path restrictions only for trusted inputs.

Probe and review the exported file. A local process has no cloud task ID, and a successful export does not require a new project or library entry. Use cloud services only when needed by the task. See [local rendering](../../runtime/local-rendering.md).
