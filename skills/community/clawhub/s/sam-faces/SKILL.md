---
name: sam-faces
description: >
  Face recognition and identity memory for AI assistants. Enroll known people
  with reference photos, then automatically identify faces in inbound images —
  with names, confidence scores, and an llm_context string ready to inject into
  any LLM prompt. 100% local, no cloud APIs.
homepage: https://github.com/jasonacox-sam/sam-faces
metadata:
  {
    "openclaw":
      {
        "emoji": "👤",
        "requires": { "bins": ["sam-faces"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "sam-faces",
              "bins": ["sam-faces"],
              "label": "Install sam-faces from PyPI",
            },
          ],
      },
  }
---

# sam-faces

Give your OpenClaw agent a real face memory. Enroll people with reference
photos, then automatically identify them in inbound images.

## Automatic behavior

**When the user intentionally sends a photo or image to the assistant:**

The user sharing an image with their AI colleague is an act of intentional
sharing — they want the assistant to see and understand what's in the image.
In this context, face identification should happen automatically as part of
understanding the image content.

1. Save the image to a temp path.
2. Run face identification: `sam-faces identify <path>`
3. Parse the JSON response.
4. If `face_count > 0`, prepend `llm_context` to your image description.
5. If any face has `"unknown": true`, ask the user who they are, then offer
to enroll them.

This should happen as part of normal image processing — the user has already
chosen to share the image.

## Installation

```bash
pip install sam-faces
```

Or use the OpenClaw skill installer:
```bash
openclaw skills install sam-faces
```

## Setup

The `sam-faces` command is available after installation:

```bash
sam-faces --help
```

## Enroll a person

```bash
sam-faces enroll --name "Jane Smith" --photo /path/to/photo.jpg
```

- One reference photo is usually enough (default threshold: 0.55).
- Enroll 2–3 photos across different lighting for best accuracy.
- Encodings are stored in `{workspaceDir}/faces/people.db`.

## Identify faces

```bash
sam-faces identify /path/to/image.jpg
```

Returns JSON with names, confidence scores, bounding boxes, and an
`llm_context` string:

```json
{
  "face_count": 2,
  "faces": [
    {
      "name": "Jane Smith",
      "confidence": 0.646,
      "unknown": false,
      "bounding_box": {
        "top": 220,
        "right": 340,
        "bottom": 350,
        "left": 210
      },
      "center": [275, 285],
      "position_desc": "middle-left"
    }
  ],
  "llm_context": "2 faces detected: Jane Smith (at 22% left, 33% down, 64% confidence); John Smith (at 92% left, 31% down, 57% confidence)."
}
```

## Visualize faces (draw bounding boxes + labels)

```bash
sam-faces visualize /path/to/image.jpg
```

Creates `image_faces.jpg` with boxes and name labels overlaid.

```bash
sam-faces visualize /path/to/image.jpg -o /path/to/output.jpg
```

## List enrolled people

```bash
sam-faces list
```

## Manage unknown faces

```bash
sam-faces unknowns
```

Shows all unknown face crops waiting to be enrolled.

## Thresholds

- Default: `--threshold 0.55` (good balance of precision and recall)
- Stricter: `--threshold 0.45` — fewer false positives
- Looser: `--threshold 0.65` — better recall in varied lighting

## Notes

- All inference runs locally via `face_recognition` (dlib). Nothing leaves the machine.
- Database: `{workspaceDir}/faces/people.db`
- Unknown face crops saved to: `{workspaceDir}/faces/unknown/`
- Works with existing face databases — no migration needed.

## When to use

- User sends a photo with people in it
- Adding a new person to the face database
- Checking who is enrolled

## When NOT to use

- Images with no faces (skip automatically)
- Processing large batches of images (one at a time)
