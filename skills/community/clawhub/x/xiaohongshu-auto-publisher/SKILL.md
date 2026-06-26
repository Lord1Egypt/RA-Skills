---
name: xhs-publisher
description: Posts content (images/videos) to Xiaohongshu (Little Red Book) automatically using Playwright. Use this skill when you need to publish content to Xiaohongshu.
---

# Xiaohongshu Publisher

This skill automates the process of posting content to Xiaohongshu (Little Red Book) using Playwright. It supports both image and video uploads, along with title and content (description) text.

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install playwright requests
    playwright install chromium
    ```

2.  **Initial Login**:
    Before you can post, you must perform a manual login once to save your session state. Run the login script:
    ```bash
    python .trae/skills/xhs-publisher/scripts/login.py
    ```
    This will open a browser window. Scan the QR code or log in using your preferred method. Once logged in, the script will save the session to `state.json`.

## Usage

To post content, use the `post.py` script:

```bash
python .trae/skills/xhs-publisher/scripts/post.py \
  --title "Your Post Title" \
  --content "Your post description here. #tags" \
  --files "/path/to/image1.jpg" "/path/to/image2.png"
```

### Arguments

*   `--title`: The title of the post.
*   `--content`: The description or caption for the post.
*   `--files`: One or more paths to the images or video files you want to upload.

## Notes
*   The script uses a visible browser window by default (`headless=False`) to help you monitor the process and handle any unexpected popups or captchas.
*   Ensure your files are in supported formats (e.g., JPG, PNG, MP4).
