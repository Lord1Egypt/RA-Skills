# Failure modes

Stop and do not import automatically when one or more of these is true:
- title cannot be reconstructed coherently
- ingredients are mostly missing
- steps are mostly missing
- page contains almost no recipe text
- the result would be more fiction than reconstruction

## Common weak cases
- TikTok description is only a caption with no recipe detail
- video is mostly visual and page metadata is sparse
- measurements are absent and even the core structure is unclear
- extracted text is noisy or malformed beyond recovery

## Preferred behavior on failure
- fail cleanly
- explain briefly
- do not create placeholder junk in Mealie
