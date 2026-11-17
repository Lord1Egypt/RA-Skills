# media-upload: Uploading is two steps, and the second is yours

## Priority: CRITICAL

## What goes wrong

`media_upload` looks like it uploads. It does not. The bytes never travel
through the API — they go straight to storage — so one tool call cannot do it.

Stopping after step one leaves nothing: the URL expires and no file exists.

## When the person has the file

They attached it in the chat, or it is on their phone or computer. Call
**`media_upload` with no arguments**, as an ordinary tool call — not from
code, and without trying to send the file yourself. Chat apps that show
widgets (Claude, ChatGPT) put an upload box under the call: tell the person to
use it. It takes one video or up to ten photos, and posts their media ids to
the chat, in picking order, when they are in. Where no box appears, give them
`upload_page` — any device, no sign-in, an hour.

## When you hold the file

A terminal agent or a server that can make HTTP requests:

1. **`media_upload`** — pass `kind` and the exact `mime_type` the PUT will send.
   Returns an `id`, a short-lived `url`, and `expires_in_seconds`.
2. **PUT the bytes to that `url`** yourself, with a `Content-Type` matching the
   `mime_type` you declared, and no other headers. A mismatch fails the upload.

Apps that show widgets never get `url` — the box is the way there.

Either way the file is recorded on its own once it arrives: pass the `id` to
`posts_save`, `media_save` or anything else that takes a media id. It shows in
`media_list` within a few minutes.

If a flow is interrupted after a successful PUT, use the id you already have —
do not start a new upload.

## What the client must be able to do

Read the file and make an HTTP PUT. If it cannot, say which step is unavailable
and use an already uploaded file, or ask the user to upload through ViewPrinter.

- **Do not pass the id anywhere until the PUT has succeeded.** A post naming a
  file that never arrived is refused as unknown media.
- **Never expose the signed upload URL** in a public post or a user-facing log.

## Context

- Size and type are read back from storage rather than trusted from what you
  claimed.
- If a post reports the media as unknown, the PUT did not land. Retry the PUT
  while the URL is still valid, or start a new upload once it has expired.
- Call `media_list` before uploading anything — it takes `search` and `kind` —
  so you do not re-upload a file the user already has.
