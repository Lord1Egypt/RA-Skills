from sdk.python.videomp3word_client import Videomp3wordClient

client = Videomp3wordClient(base_url="http://localhost:3000", bearer_token="your-access-key")
result = client.video_to_knowledge(
    media_url="https://example.com/meeting-recording.mp4",
    outputs=["summary", "tasks", "topics"],
    mode="balanced",
    export_formats=["json", "notion"],
)

for item in result["action_items"]:
    print(f"- {item['task']} | owner={item['owner']} | deadline={item['deadline']}")
