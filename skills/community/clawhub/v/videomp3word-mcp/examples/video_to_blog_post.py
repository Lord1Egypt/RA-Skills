from sdk.python.videomp3word_client import Videomp3wordClient

client = Videomp3wordClient(base_url="http://localhost:3000", bearer_token="your-access-key")
result = client.video_to_knowledge(
    media_url="https://example.com/podcast-episode.mp4",
    outputs=["summary", "topics", "qa", "flashcards"],
    mode="high_accuracy",
    export_formats=["json", "markdown"],
)

print("Blog-ready summary:\n")
print(result["summary"])
print("\nMarkdown export:\n")
print(result["exports"]["markdown"])
