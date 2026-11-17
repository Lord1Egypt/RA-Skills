# Music recognition

Use [breakdown](../../api/breakdown.md) with `sub_tasks: ["bgm"]` when music identification is requested. Report only the name, artist, confidence, and links actually returned. A match is not proof of reuse rights.

Do not automatically download, purchase, or reuse identified music. If the user wants newly generated music with a similar mood, route to [audio generation](../generation/audio-generation.md) and clearly distinguish the new audio from the reference.
