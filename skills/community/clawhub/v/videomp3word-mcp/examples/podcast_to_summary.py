from sdk.python.videomp3word_client import Videomp3wordClient

client = Videomp3wordClient(base_url="http://localhost:3000", bearer_token="your-access-key")
result = client.video_to_knowledge(
    media_url="https://example.com/podcast.mp3",
    outputs=["summary", "topics", "qa"],
    mode="fast",
    export_formats=["json"],
)

print(result["summary"])
print(result["topics"])
