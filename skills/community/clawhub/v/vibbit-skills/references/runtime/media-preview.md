# Image previews

Use before displaying avatar covers, generated images, or existing images. Converting the specified OSS origin is mandatory in WorkBuddy and other Agents, including chat images, galleries, and visual cards. Conversion is local and submits no generation task.

The client adds `artifacts[].preview_url` where possible. Avatar lists expose `previews[]` with resource_id, name when available, original url, and preview_url. These are presentation fields; preserve original results, IDs, and generation inputs.

- Always convert `https://willing-video-test.oss-cn-shanghai.aliyuncs.com/` to `https://media.vibbit.cn/`, preserving path, query, and fragment. Direct OSS URLs may force downloads and must not be used for image display.
- Match only that complete HTTPS origin. Other hosts, buckets, ports, or embedded credentials are unchanged.
- Preserve query parameters byte for byte, including image processing, signatures, and temporary credentials. Do not strip, decode, or rebuild them. Keep the original URL in the resource record.
- Reuse media.vibbit.cn URLs. Conversion does not prove availability or host preview support.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" preview_url --url 'https://willing-video-test.oss-cn-shanghai.aliyuncs.com/agentcy/cover/example.jpg'
~~~

The filename is a placeholder; use an actual returned URL. The command needs no key/network.

Use `result` for the complete avatar catalog and match `previews[].resource_id` to each actual ID. Card images must use `previews[].preview_url`; image artifacts use `artifacts[].preview_url`. If only a raw `cover` or image URL is available, run `preview_url --url` first. Do not embed it before conversion.

In a gallery or HTML card, the actual `<img src>`, CSS image URL, and preview link must use the converted address. Changing only the click-through link while leaving an OSS image `src` does not satisfy conversion. Other origins may remain unchanged when the converter returns them unchanged. Do not use the `avatar` field as a cover.

If inline display is unavailable, use a host-supported gallery or the converted preview link. Host support is not guaranteed. On failure, retain the name, ID, and original resource record, and show a cover-loading message with the converted preview link instead of an empty card. Never fall back to the direct OSS URL. A failed preview does not mean the avatar is absent and must not trigger regeneration. Display candidates before waiting when the user requests selection.
