import os
import logging
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp

logger = logging.getLogger(__name__)

def get_transcript(video_id: str) -> str:
    """
    Attempts to fetch the transcript (subtitles) of a YouTube video.
    Returns the transcript as a string, or None if no subtitles are available.
    """
    try:
        # Try to get the transcript
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to find a manually created or auto-generated english/chinese transcript
        # Fallback to whatever is available
        try:
            transcript = transcript_list.find_transcript(['zh-CN', 'zh-TW', 'zh', 'en'])
        except Exception:
            # If preferred languages aren't found, pick the first available one
            transcript = transcript_list.find_generated_transcript(['en', 'zh', 'ja', 'ko']) or transcript_list.find_manually_created_transcript(['en', 'zh', 'ja', 'ko'])
            if not transcript:
                # Get anything
                transcript = list(transcript_list)[0]

        formatter = TextFormatter()
        text = formatter.format_transcript(transcript.fetch())
        return text

    except Exception as e:
        logger.warning(f"Could not get transcript for video {video_id}: {e}")
        return None

def download_audio(video_id: str, output_dir: str = "temp_audio") -> str:
    """
    Downloads the audio of a YouTube video using yt-dlp.
    Returns the path to the downloaded audio file, or None if failed.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    out_tmpl = os.path.join(output_dir, f"{video_id}.%(ext)s")
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': out_tmpl,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        logger.info(f"Downloading audio for {video_id} using yt-dlp...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                filename = filename.replace(".webm", ".m4a") # Just in case
            return filename
    except Exception as e:
        logger.error(f"Failed to download audio for {video_id}: {e}")
        return None

def extract_content(video_id: str) -> dict:
    """
    Main extraction function. Matches the dual nature of our bot.
    Returns:
    {
        'type': 'text' or 'audio',
        'data': str (text content or file path)
    }
    """
    # 1. Try checking for standard subtitles
    logger.info(f"[{video_id}] Attempting to fetch transcript...")
    transcript = get_transcript(video_id)
    if transcript:
        logger.info(f"[{video_id}] Transcript fetched successfully. Length: {len(transcript)} chars.")
        return {'type': 'text', 'data': transcript}

    # 2. Fallback to downloading audio
    logger.info(f"[{video_id}] Transcript failed. Falling back to audio download...")
    audio_path = download_audio(video_id)
    if audio_path:
        logger.info(f"[{video_id}] Audio downloaded successfully: {audio_path}")
        return {'type': 'audio', 'data': audio_path}

    logger.error(f"[{video_id}] Both transcript and audio download failed.")
    return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from pprint import pprint
    # Test text fallback
    # pprint(extract_content("dQw4w9WgXcQ")) 
