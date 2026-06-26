# Channel flow: chat channels to a visual inspiration library

Design the skill as a channel-agnostic ingestion workflow with thin channel adapters.

## Goal

Allow the user to submit UI inspiration images from chat channels while reusing the same downstream analysis and storage flow.

## Canonical flow

1. Receive a user message with one or more images.
2. Detect the current channel.
3. Extract or download image attachments using the channel-specific path.
4. Normalize all local files into a single ingestion list.
5. Run image analysis on each image.
6. Convert the analysis into the library schema.
7. Create or update a library item and upload/store the image.
8. Reply in the same channel with a concise archive result.

## Adapter guidance

### Generic adapter rules
- Keep channel-specific file handling isolated.
- Normalize local files into the same internal ingestion format.
- Do not entangle classification logic with transport-specific code.

### UX rule
Return a concise result in the source channel:
- archived count,
- generated title,
- core tags,
- whether the image was successfully stored.

If part of the flow fails, separate the failure clearly:
- image received but analysis failed,
- analysis succeeded but library write failed,
- partial success for batch upload.
