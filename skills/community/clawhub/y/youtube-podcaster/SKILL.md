---
name: youtube-podcaster
description: Extracts the original text of a Youtube video and converts it into a multi-voice AI podcast using Gemini for script generation, OpenAI for TTS, and a local Node.js API with FFmpeg. It also can show you the text of the Podcast in WebVTT format.
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - node
        - npm
        - ffmpeg
      env:
        - GEMINI_API_KEY
        - OPENAI_API_KEY
    always: false
---

# YouTube Podcaster

This skill enables the automated conversion of YouTube videos into multi-host AI podcasts. It manages transcription, script generation via Gemini, and audio synthesis via OpenAI locally.

## Security Setup
For maximum security, the backend server binds strictly to `127.0.0.1`. It is not accessible from your local network or the internet.

1. **Install Dependencies:** You must run the install command once before the first use. Say: 
   `Run the npm install command for the youtube-podcaster skill`.
2. **Credentials:** Place your Gemini API Key and OpenAI API Key in the `.env` file within the skill folder (`skills/youtube-podcaster/.env`) using the variable names `GEMINI_API_KEY` and `OPENAI_API_KEY`.
3. **Execution:** Start the server with `npm start` or by instructing the agent: `Start the local server for the youtube-podcaster skill`.

## Usage
Once the server is running, say: 
`Create a podcast for the video https://www.youtube.com/watch?v=<video_id> using the youtube-podcaster skill`

The skill orchestrates three local API calls to `localhost:7860`:
1. **Transcription:** Extracts text via the YouTube transcript API.
2. **Drafting:** Uses Gemini to create a natural dialogue script.
3. **Synthesis:** Uses OpenAI TTS (tts-1) and FFmpeg to generate a gapless `.m4a` file.

## Safe Cleanup
When you are finished using the studio, shut down the background process to free up system resources. Do not use generic kill commands. Instead, instruct the agent to use the tracked process ID:
`Stop the youtube-podcaster server process` 

*(The agent will execute `kill $(cat .podcaster.pid)` or `pkill -f "node index.js"` to target the specific process safely).*

## Storage & File Outputs
Files are saved to `downloads/<session_id>/` inside the skill directory. The server includes an hourly garbage collector that automatically deletes inactive sessions.
* **Audio:** `podcast.m4a`
* **Captions:** `podcast.vtt`
* **Scripts:** `script.txt` and `original.txt`

## Source Code
The source code is available at: [https://github.com/kaudata/youtube-podcaster](https://github.com/kaudata/youtube-podcaster)