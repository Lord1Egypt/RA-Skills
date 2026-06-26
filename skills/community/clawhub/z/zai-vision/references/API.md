# Z.AI Vision API Reference

## Quick Start

### Installation

```bash
pip install zai-sdk
```

### API Key Setup

Set your Z.AI API key as an environment variable:

```bash
export ZAI_API_KEY='your-api-key-here'
```

## Image Analysis

### Basic Usage

```bash
python3 vision_analyze.py /path/to/image.jpg "What's in this image?"
```

### With Custom Parameters

```bash
python3 vision_analyze.py /path/to/image.png "Describe this UI design" \
  --model glm-4.6v \
  --max-tokens 2000 \
  --temperature 0.5
```

### JSON Output

```bash
python3 vision_analyze.py /path/to/image.jpg "Extract all text" --json
```

## Video Analysis

### Basic Usage

```bash
python3 video_analyze.py /path/to/video.mp4 "What happens in this video?"
```

### Important Notes

- **File Size Limit**: Videos up to 8MB recommended for best results
- **Supported Formats**: MP4, MOV, M4V
- **Processing**: Videos are analyzed frame-by-frame by the vision model
- **For Video Generation**: Use Z.AI's video generation API (cogvideox-3) instead

## Common Use Cases

### 1. UI Design Analysis

```bash
python3 vision_analyze.py ui-mockup.png "Analyze this UI design and suggest improvements"
```

### 2. OCR / Text Extraction

```bash
python3 vision_analyze.py screenshot.png "Extract all text from this image"
```

### 3. Error Diagnosis

```bash
python3 vision_analyze.py error-screenshot.jpg "What's wrong with this code? How do I fix it?"
```

### 4. Technical Diagram Understanding

```bash
python3 vision_analyze.py architecture.png "Explain this architecture diagram"
```

### 5. Data Visualization Analysis

```bash
python3 vision_analyze.py chart.png "What insights does this chart show?"
```

### 6. Video Scene Description

```bash
python3 video_analyze.py clip.mp4 "Describe what's happening in this video"
```

## Model Parameters

| Parameter | Default | Description |
|-----------|----------|-------------|
| `--model` | glm-4.6v | Vision model to use |
| `--max-tokens` | 2000 | Maximum response tokens |
| `--temperature` | 0.5 | Generation temperature (0-2) |
| `--json` | false | Output as JSON format |

## Error Handling

### Common Errors

**No API key:**
```
❌ ZAI_API_KEY environment variable not set
```
**Fix:** Set environment variable: `export ZAI_API_KEY='your-key'`

**Image not found:**
```
❌ Image file not found: /path/to/image.jpg
```
**Fix:** Verify the file path is correct

**SDK not installed:**
```
❌ zai-sdk not installed
```
**Fix:** Install with: `pip install zai-sdk`

**File too large:**
```
⚠️  Warning: Video is 12.50MB (exceeds 8MB recommended limit)
```
**Fix:** Compress the video or use a shorter clip

## Integration Examples

### Python API Direct Usage

```python
from zai import ZaiClient
import base64

# Initialize client
client = ZaiClient(api_key='your-api-key')

# Encode image
with open('image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Analyze
response = client.chat.completions.create(
    model='glm-4.6v',
    messages=[
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': "What's in this image?"},
                {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{image_data}'}},
            ],
        }
    ],
    temperature=0.5,
    max_tokens=2000
)

print(response.choices[0].message.content)
```

## Tips for Best Results

1. **Be specific with prompts**: Instead of "What's this?", use "Describe the UI elements in this screenshot"
2. **Use high-quality images**: Better resolution = better understanding
3. **Consider temperature**: Lower (0.2-0.5) for factual analysis, higher (0.7-1.0) for creative interpretations
4. **Batch processing**: For multiple images, use a script loop
5. **Handle errors gracefully**: Always check for API errors and handle appropriately

## Advanced: Using with Safe Scripts

When integrating with Clawdbot's safe-scripts skill:

```bash
clawd-run /root/clawd/zai-vision/scripts/vision_analyze.py image.png "Describe this"
```

This provides:
- Automatic syntax validation
- Backup creation before execution
- 60-second timeout protection
- Better error formatting
