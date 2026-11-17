# Digital humans

Use [list_digital_humans](../api/list_digital_humans.md) to query accessible resources. Preserve actual IDs, names, avatar/voice fields, covers, and any status returned; do not invent missing properties or an independent voice ID from a voice label.

## Show the complete returned list

For browsing or selection, show all returned entries and the count, including entries without covers. Mark recommendations within the full list instead of reducing it to a few candidates. Use a gallery or complete pagination where the host supports it; if the message cannot fit everything, provide an accessible complete list and state the visible range. Filter only when requested, and do not describe recommendations as the complete catalog.

The public contract has no creation timestamp, sorting, or pagination parameters. Sort newest first only with a timestamp whose meaning the service confirms. Otherwise retain response order and explain that creation order is unavailable; do not infer it from IDs or reverse the array. A returned count does not prove account-wide completeness. If the response indicates pagination, continue only through a confirmed pagination contract.

Bind the selection directly to the original record's `id + name + cover`. Display numbers belong to that displayed list, never to the API; do not reuse number mappings after reordering. Before submission, check `digital_human_id` against the selected record once, using the exact string instead of manually reconstructing a mapping. A unique match or existing permission to choose needs no repeated confirmation.

Use `result` for the full catalog; `previews[]` includes only entries with usable covers. Before displaying covers, follow [image previews](../runtime/media-preview.md). Match each preview by `resource_id`; card image `src` must use its `preview_url`. If only raw records are available, convert each cover with `preview_url --url` first. Never embed or fall back to a direct URL from the specified OSS origin. Keep `result[].cover` as the source record. Do not download every cover just to list resources. The `avatar` field is not necessarily an image URL.

A valid complete ID supplied by the user can be used directly. A uniquely matched name can be selected; resolve duplicates when they affect the choice. Preserve 64-bit IDs as strings. Use real resource previews when available.

## Associated voice

Preserve the returned `voice` field, but audio generation has no `voice_id` input, so this field alone cannot select the avatar's voice for new speech. The documented listing has no voice-preview URL. Show a real preview when its meaning is established; otherwise state that it was not supplied. Use [voices](voices.md) to establish an actual reference rather than guessing a voice from a name or cover.

A failed lookup is not a reason to create a project or a new avatar. Explicit reusable-avatar creation follows [digital human creation](../capabilities/generation/digital-human-creation.md); ordinary generation follows [digital human video](../capabilities/generation/digital-human-video.md).
