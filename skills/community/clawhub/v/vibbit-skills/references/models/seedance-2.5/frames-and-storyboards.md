# Frames and storyboards

Distinguish narrative reference images from actual first/last-frame inputs. A contact sheet can guide a sequence but does not guarantee that each cell becomes a specific shot.

For real start/end constraints, use the API's first/last-frame fields with adaptive aspect ratio. The last frame requires a first frame; do not mix these fields with other image/reference modes. Match framing and aspect ratio across the endpoints and explain continuity requirements.

For a storyboard reference, identify the ordered images and intended sequence. Do not claim exact shot timing from image order alone. Reuse suitable existing images; do not automatically regenerate them just to split a board.

When exact timing or transitions are required, compose actual clips locally or through media composition. See [API compatibility](../../api/seedance.md) and [storyboard production](../../workflows/storyboard-video.md).
