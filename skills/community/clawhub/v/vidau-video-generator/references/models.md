# Vidau Model List and Selection

Common model IDs supported by Vidau Open API and suggested use cases for choosing `--model` when creating tasks.

## Model IDs and description

| model ID | Description | Use case |
|----------|-------------|----------|
| `veo@3:normal` | Veo 3 | General video generation, brand and ads |
| `veo@3.1:normal` | Veo 3.1 quality | Multi-image reference, first/last frame control, brand consistency |
| `veo@3.1:fast` | Veo 3.1 fast | Speed-first |
| `sora@2:normal` | Sora 2 | Strong physics and lighting, cinematic |
| `sora@2:pro` | Sora 2 Pro | High-end creative, short-film grade |
| `seedance@1:pro` | Seedance Pro | Multi-shot narrative, artistic style |
| `seedance@1:pro_fast` | Seedance Pro Fast | Speed-first Seedance |
| `wan@2.5:preview` | Wan 2.5 | Chinese semantics, lip-sync and detail, short-form |
| `vidu@q2:turbo` | Vidu Q2 Turbo | Emotion and performance, story-driven |
| `vidu@q2:pro` | Vidu Q2 Pro | Higher-quality emotion and performance |

## Selection tips

- **Brand / e‑commerce**: Prefer `veo@3.1:normal` (first/last frame and multi-image reference).
- **Cinematic / creative shorts**: `sora@2:normal` or `sora@2:pro`.
- **Artistic style / music video**: `seedance@1:pro`.
- **Short-form / digital human (Chinese)**: `wan@2.5:preview`.
- **Story / emotion**: `vidu@q2:pro` or `vidu@q2:turbo`.

Full details: [Vidau Model Overview](https://doc.superaiglobal.com/en/overview/models.md).
