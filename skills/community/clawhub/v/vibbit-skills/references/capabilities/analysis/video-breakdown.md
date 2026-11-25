# Video breakdown

Use [breakdown](../../api/breakdown.md) and select only the requested analyses: `asr`, `hot`, `transition`, and `bgm` in the required string array. Supported share URLs can be passed directly.

For a reference-based reusable mixcut template, follow [Agent semantic mixcut](../../workflows/semantic-mixcut.md): hot for content structure, transition for shots/cuts, and asr for speech/timing, requesting only missing analysis. Add bgm only when music is relevant. Retain successful subresults and failure state, resume the original job, and avoid resubmitting the whole set. The Agent derives editing/sound rules from actual media; API analysis is not automatically a complete editing template.

Inspect each child task's state and decode returned result data as needed. Separate observations from interpretation and retain real timestamps. Preserve successful partial results instead of rerunning all analyses.

The root `video_url` identifies source media. Item-level video URLs may be analysis segments. Neither is a newly generated final video. Use [reference analysis](../../creation/reference-analysis.md) for creative interpretation and [task lifecycle](../../runtime/task-lifecycle.md) for recovery.
