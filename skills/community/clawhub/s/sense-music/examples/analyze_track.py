"""ClawHub example — analyze an audio track."""
from sense_music import analyze

result = analyze("song.mp3", lyrics=False)
print(result.summary)
result.save("output/")
