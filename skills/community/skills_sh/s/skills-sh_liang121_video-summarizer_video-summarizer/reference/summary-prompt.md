# Video Summary Prompt Template

Generate a structured summary based on the following video transcript.

## Video Information
- **Title**: {{TITLE}}
- **Source**: {{PLATFORM}}
- **URL**: {{URL}}
- **Duration**: {{DURATION}}
- **Language**: {{LANGUAGE}}
- **Download Time**: {{DOWNLOAD_TIME}}

## Transcript Content
{{TRANSCRIPT}}

---

## Please generate summary in the following format:

# Video Summary: {{TITLE}}

## Basic Information
- **Source**: {{PLATFORM}}
- **URL**: {{URL}}
- **Duration**: {{DURATION}}
- **Language**: {{LANGUAGE}}
- **Download Time**: {{DOWNLOAD_TIME}}

## Output Files
- video.mp4 - Original video
- audio.mp3 - Audio file
- subtitle.vtt - Subtitles (with timestamps)
- transcript.txt - Plain text transcript
- summary.md - This summary file

## Overview
[2-3 sentences summarizing the main content]

## Key Points
1. [Point 1]
2. [Point 2]
3. [Point 3]
...

## Detailed Content

### [Topic 1]
[Detailed explanation]

### [Topic 2]
[Detailed explanation]

## Notable Quotes
> "[Important quote 1]"

> "[Important quote 2]"

## Related Topics
- [Related topic 1]
- [Related topic 2]
