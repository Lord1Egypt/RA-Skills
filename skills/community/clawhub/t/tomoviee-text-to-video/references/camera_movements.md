# Camera Movement Types Reference

Complete list of camera movement types for `camera_move_index` parameter.

## Movement Types (1-46)

| Index | Type | Description |
|-------|------|-------------|
| 1 | orbit | Camera circles around subject |
| 2 | spin | Rotating motion |
| 3 | pan left | Camera pans to the left |
| 4 | pan right | Camera pans to the right |
| 5 | tilt up | Camera tilts upward |
| 6 | tilt down | Camera tilts downward |
| 7 | push in | Camera moves closer to subject |
| 8 | pull out | Camera moves away from subject |
| 9 | static | No camera movement |
| 10 | tracking | Camera follows subject movement |
| 11 | others | Unspecified movement |
| 12 | object pov | Point of view from object perspective |
| 13 | super dolly in | Dramatic push into scene |
| 14 | super dolly out | Dramatic pull from scene |
| 15 | snorricam | Camera fixed to subject while rotating |
| 16 | head tracking | Follows head/face movement |
| 17 | car grip | Camera mounted on vehicle |
| 18 | screen transition | Transition effect movement |
| 19 | car chasing | Following vehicle action |
| 20 | fisheye | Wide-angle distortion effect |
| 21 | FPV drone | First-person drone perspective |
| 22 | crane over the head | Overhead crane shot |
| 23 | timelapse landscape | Time-lapse scenery |
| 24 | dolly in | Smooth push toward subject |
| 25 | dolly out | Smooth pull from subject |
| 26 | zoom in | Lens zooms closer |
| 27 | zoom out | Lens zooms further |
| 28 | full shot | Wide establishing shot |
| 29 | close-up shot | Tight framing on subject |
| 30 | extreme close-up | Very tight detail shot |
| 31 | Macro shot | Extreme close-up of small details |
| 32 | bird's-eye view | Overhead perspective |
| 33 | rule of thirds | Compositional guideline |
| 34 | symmetrical composition | Balanced framing |
| 35 | handheld | Shaky, documentary-style |
| 36 | FPV shot | First-person view |
| 37 | jib up | Crane moves upward |
| 38 | jib down | Crane moves downward |
| 39 | full shot | Complete subject in frame |
| 40 | Time lapse shot | Compressed time progression |
| 41 | aerial shot | High-altitude view |
| 42 | low angle shot | Camera positioned below subject |
| 43 | Eye-level shot | Camera at subject's eye level |
| 44 | diagonal composition | Angled framing |
| 45 | over shoulder shot | View from behind subject |
| 46 | crane down | Crane descends |

## Usage Example

```python
# Static shot with no camera movement
client.create_video(
    prompt="猫咪转头看向镜头",
    image="https://example.com/cat.jpg",
    camera_move_index=9  # static
)

# Dramatic push in shot
client.create_video(
    prompt="女孩突然转头,右手拿起无线耳机戴在耳朵上",
    image="https://example.com/girl.jpg",
    camera_move_index=13  # super dolly in
)
```
