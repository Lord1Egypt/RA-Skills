"""YouTube Transcript"""
import re, json

def handle(input_text: str, user_id: str = "default") -> dict:
    url_match = re.search(r'(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', input_text)
    if not url_match:
        return {"error": "Please provide a YouTube URL"}
    video_id = url_match.group(2)
    return {"video_id": video_id, "status": "Transcript service ready",
            "demo": "Use youtube-transcript-api library to fetch actual transcript",
            "payment_status": "paid"}

if __name__ == "__main__":
    import sys
    print(json.dumps(handle(sys.argv[1] if len(sys.argv) > 1 else ""), indent=2))
