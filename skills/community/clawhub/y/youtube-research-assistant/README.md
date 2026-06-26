# YouTube Watcher Skill

A personal AI research assistant for YouTube videos that extracts transcripts and provides structured summaries, Q&A, deep dives, and actionable insights.

## Overview

This skill allows OpenClaw to fetch transcripts from YouTube videos and provide structured multilingual summaries, Q&A capabilities, deep dives into content, and actionable insights.

## Features

- **Transcript Extraction**: Fetches transcripts using yt-dlp and converts subtitles into clean transcripts
- **Structured Summaries**: Provides 5 key points, important timestamps, and core takeaways
- **Q&A Capability**: Answer specific questions from stored transcripts
- **Deep Dives**: Explore topics in detail using transcript content
- **Action Points**: Extract actionable insights from videos
- **Multilingual Support**: Detect user language and translate responses
- **Anti-Hallucination**: All responses must come from transcript content only

## Installation

This skill is designed to be used with OpenClaw. To install:

1. Ensure OpenClaw is installed and running
2. Place this skill folder in your OpenClaw skills directory
3. The skill will automatically be detected and available

## Requirements

- Python 3
- yt-dlp (for transcript extraction)
- OpenClaw (for integration)

## Usage

### Basic Commands

When a YouTube URL is provided:

```bash
python3 scripts/get_transcript.py fetch "YOUTUBE_URL"
```

This command:
- Fetches the transcript using yt-dlp
- Converts subtitles into a clean transcript
- Saves the transcript to `data/VIDEO_ID.txt`
- Automatically cleans transcripts older than 24 hours

### Ask Questions

```bash
python3 scripts/get_transcript.py ask VIDEO_ID "user question here"
```

This command:
- Loads the stored transcript
- Splits the transcript into chunks
- Retrieves relevant chunks using keyword search
- Returns transcript sections with timestamps

### List Stored Transcripts

```bash
python3 scripts/get_transcript.py list
```

Displays all stored videos.

### Manual Cleanup

```bash
python3 scripts/get_transcript.py cleanup
```

Deletes transcripts older than 24 hours.

## Output Formats

### Default Summary

```
🎬 Video Title
📌 5 Key Points
🕐 Important Timestamps
🧠 Core Takeaway
```

### Q&A Format

Returns transcript sections with timestamps that match the user's question.

## Anti-Hallucination Rules

- **STRICTLY FORBIDDEN**: Using YouTube metadata, video title, description, tags, or thumbnail
- **STRICTLY FORBIDDEN**: Using your own training data or prior knowledge about the video
- **STRICTLY FORBIDDEN**: External APIs, web search, or HTTP requests
- **STRICTLY FORBIDDEN**: Guessing or inferring content from the URL or video ID
- **STRICTLY FORBIDDEN**: Title-based summaries

If the transcript does not contain the answer, respond exactly:

"This topic is not covered in the video."

## Edge Cases

| Situation | Action |
|-----------|---------|
| Script timeout | Ask the user to retry |
| No subtitles | "This video has no captions available." |
| Invalid URL | "Invalid YouTube URL. Please check the link." |
| No stored transcript | Run fetch first |
| Very long transcript | Use ask command retrieval |

## Security & Privacy

- All transcript data is stored locally in the `data/` directory
- Transcripts older than 24 hours are automatically cleaned up
- No external API calls are made beyond the initial transcript fetch
- All responses must be traceable to transcript content

## Development

### File Structure

```
youtube-watcher/
├── scripts/
│   └── get_transcript.py    # Main script for transcript operations
├── data/                    # Stored transcripts (auto-created)
├── SKILL.md                # Skill definition and rules
└── README.md               # This file
```

### Testing

1. Test transcript fetching with a known YouTube URL
2. Verify Q&A functionality with stored transcripts
3. Test cleanup functionality
4. Verify multilingual support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This skill is designed for use with OpenClaw and follows OpenClaw's licensing terms.

## Support

For issues or questions:
- Check the OpenClaw documentation
- Review the skill logs for error messages
- Ensure all dependencies are installed
- Verify YouTube URL accessibility

---

**Note**: This skill is designed to be used with OpenClaw AI assistant. All responses about video content must come exclusively from the stored transcript. No exceptions.