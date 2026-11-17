---
name: youtube-audience-research
description: Turn YouTube comment downloads into structured audience research questions, summaries, and follow-up analyses.
---

# YouTube audience research

Use the YouTube Comments Downloader MCP tools as the data collection step for audience research.

## Workflow

1. Ask for a YouTube URL and the intended research question.
2. Use `download_youtube_comments` with the narrowest matching `contentType`.
3. Use `get_youtube_download` until the download is finished or has an error.
4. Use `get_youtube_download_file` to return the file URL in the format the user requested.
5. When the video's content matters too, use `get_youtube_transcript` to read what was said.
6. Keep collection facts separate from interpretation. State when a conclusion is based on a sample or a download limit.

## Useful research prompts

- What recurring needs, objections, and questions appear in the comments?
- Which themes are positive, negative, or unresolved?
- What audience segments are implied by the language and use cases?
- Which comments should inform the next video, product, or support article?

Do not claim that the MCP server searches comments. Search is not a v1 tool. Every download uses credits from the user's YCD account.
