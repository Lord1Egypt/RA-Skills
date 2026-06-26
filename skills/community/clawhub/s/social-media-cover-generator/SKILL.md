---
name: social-media-cover-generator
description: Social media cover image generator. Generates HTML pages based on title content and automatically converts them to PNG images, suitable for creating cover images and graphics for platforms such as Xiaohongshu, WeChat Official Accounts, Weibo, Douyin, Bilibili, Zhihu, Twitter/X, Instagram, and LinkedIn.
---

# Social Media Cover Image Generator

Generate beautiful HTML pages based on title content and automatically convert them to PNG images.

## Use Cases

- User requests to generate social media covers, social media graphics, or article cover images
- User mentions keywords such as "cover image," "graphic," "social media image," or "self-media image"
- User needs to create images for specific platforms (Xiaohongshu, WeChat, Weibo, Douyin, Bilibili, Zhihu, Twitter, Instagram, LinkedIn)


## Workflow

### 1. Confirm Platform and Dimensions

Use the following preset dimensions (width×height, in pixels) based on the platform specified by the user:

| Platform | Dimensions | Purpose |
|----------|-----------|---------|
| Xiaohongshu | 1080×1440 (3:4) | Post cover |
| WeChat Official Account | 900×500 | Article cover (large) |
| WeChat Official Account (small) | 200×200 | Article cover (small) |
| Weibo | 1080×1260 | Long image / 9-grid |
| Douyin | 1080×1920 (9:16) | Video cover |
| Bilibili | 1920×1080 (16:9) | Video cover |
| Zhihu | 1120×630 | Article cover |
| Twitter/X | 1200×675 | Tweet image |
| Instagram | 1080×1080 (1:1) | Square post |
| Instagram Story | 1080×1920 (9:16) | Story |
| LinkedIn | 1200×627 | Post image |

If the user does not specify a platform, default to **Xiaohongshu 1080×1440**.

### 2. Design and Generate HTML Page

Design a visually appealing HTML page based on the title content, then call the conversion script to generate a PNG.

**Design Principles:**
- Strong visual impact with prominent titles
- Harmonious color schemes suitable for the target platform's style
- Appropriate whitespace to avoid clutter
- Support for Chinese fonts
- **Text content width occupies 80% of container width**: Control via font size (title font size = container width × 0.067 × 1.5 = container width × 0.1005; e.g., 1080px width corresponds to approximately 108px font size)

**Required Elements:**
- Title text (large, prominent)
- Background (gradient, solid color, or pattern)
- Decorative elements (optional: shapes, lines, icons)

**Font Recommendations:**
```css
font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
```

### 3. Automatically Generate PNG Image

Use the `scripts/html2png.js` script to automatically convert HTML to PNG:

```bash
node scripts/html2png.js <input.html> [output.png]
```

**Conversion Principle:**
1. Launch a headless browser using Puppeteer
2. Load the HTML file
3. Use snapdom to render the `#cover` element to canvas
4. Export as a PNG file

**Execution Command Example:**
```bash
node scripts/html2png.js cover.html cover.png
```

### 4. Return Results

Return the path of the generated PNG image to the user.

## HTML Template

The generated HTML file must contain the following structure:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Cover Image</title>
  <script src="https://unpkg.com/@zumer/snapdom/dist/snapdom.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: #f0f0f0;
    }
    
    /* Must have a container with id="cover" */
    .cover {
      width: {WIDTH}px;
      height: {HEIGHT}px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 40px;
    }
    
    .title {
      font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
      font-size: 108px;  /* Font size = container width × 0.1005 (approximately 80% width, 1.5x scaling) */
      font-weight: bold;
      color: #ffffff;
      text-align: center;
    }
  </style>
</head>
<body>
  <!-- Must have id="cover" -->
  <div class="cover" id="cover">
    <div class="title">{TITLE}</div>
  </div>
</body>
</html>
```

**Key Requirements:**
- Must include snapdom: `<script src="https://unpkg.com/@zumer/snapdom/dist/snapdom.js"></script>`
- Cover container must have `id="cover"`
- Styles must be inline in the HTML

## Complete Execution Flow

1. **Generate HTML**: Create an HTML file based on user requirements and save it to the working directory
2. **Convert to PNG**: Execute `node scripts/html2png.js <html-file> <png-file>`
3. **Return Results**: Inform the user of the PNG file path

## Usage Example

**User Input:**
> Help me generate a Xiaohongshu cover image with the title "5 Habits to Make You More Disciplined"

**Execution Flow:**
1. Confirm platform: Xiaohongshu → 1080×1440
2. Generate HTML: `cover_xiaohongshu_5habits.html`
3. Execute conversion: `node scripts/html2png.js cover_xiaohongshu_5habits.html cover_xiaohongshu_5habits.png`
4. Return: `cover_xiaohongshu_5habits.png`

## Color Scheme Suggestions

| Style | Gradient Colors |
|-------|-----------------|
| Motivational / Energetic | `#FF6B6B → #FFA500` |
| Knowledge / Education | `#4FACFE → #00F2FE` |
| Business / Professional | `#667EEA → #764BA2` |
| Lifestyle / Warm | `#FA8BFF → #2BD2FF` |
| Tech / Future | `#0F0C29 → #302B63 → #24243E` |
| Nature / Fresh | `#11998E → #38EF7D` |
| Elegant / Minimal | `#E0C3FC → #8EC5FC` |

## Notes

1. **Font Rendering**: Use system fonts for Chinese to ensure compatibility
2. **Image Dimensions**: Strictly follow platform requirements to avoid cropping
3. **Title Length**: Recommended to not exceed 20 characters; wrap to a new line if exceeded
4. **Contrast**: Ensure sufficient contrast between text and background for clear readability
5. **id="cover"**: The cover container must have this id; otherwise the conversion script will not work