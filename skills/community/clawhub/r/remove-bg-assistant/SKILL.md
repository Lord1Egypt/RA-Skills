# Remove Background Assistant

AI-powered background removal for portraits, products, and any image.

## Description

Professional-quality background removal using cloud AI APIs. No Photoshop skills needed - get clean cutouts in seconds.

### Features

**1. Portrait Background Removal**
- Perfect for ID photos, profile pictures
- Handles hair details
- Natural edge detection
- Output: Transparent PNG

**2. Product Photography**
- E-commerce ready
- Clean white/transparent backgrounds
- Batch processing support
- Consistent quality

**3. General Images**
- Works with any photo type
- Automatic subject detection
- Manual refinement options

### Technical Details

**Current Implementation: Baidu Image Segmentation API**
- Free tier: 10,000 requests/month
- Pricing: ~¥0.001 per image after free tier
- Speed: <2 seconds per image
- Accuracy: 95%+ for clear subjects

**API Integration Example:**
```python
import requests

def remove_bg(image_path):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg"
    # Get access_token first
    # Send image, receive segmented result
    # Process and return transparent PNG
```

**Web Interface Features:**
- Drag & drop upload
- Preview before download
- Multiple format support (PNG, JPG)
- Mobile-friendly design

### Use Cases

| User Type | Use Case | Benefit |
|-----------|----------|---------|
| E-commerce seller | Product photos | Professional listings |
| Social media creator | Profile pictures | Clean aesthetics |
| Designer | Mockup creation | Faster workflow |
| Marketer | Ad creatives | Quick turnaround |
| Developer | App integration | API automation |

## Usage

**Basic requests:**
- "Remove background from this image"
- "How to use the API?"
- "Compare Baidu vs other services"

**Integration help:**
- "Add to my Flask website"
- "Batch process folder of images"
- "Mobile app integration"

**Business questions:**
- "Pricing for 1000 images/month?"
- "Is there a free tier?"
- "Can I resell this service?"

## Example

**User:** "I have 50 product photos. How to batch remove backgrounds?"

**Response:**
```
Batch processing solution:

Option 1: Python Script
```python
import os
from remove_bg import process_image

folder = "product_photos/"
for img in os.listdir(folder):
    if img.endswith(('.jpg', '.png')):
        result = process_image(f"{folder}/{img}")
        result.save(f"output/{img}")
```

Option 2: Web Interface
- Upload ZIP file
- Process all at once
- Download results ZIP

Option 3: API Integration
- Direct integration with your system
- Webhook notifications
- Queue management for large batches

Which option fits your workflow?
```

## Live Demo

Try it now: www.instantbg.cn

## Pricing Reference

| Service | Free Tier | Paid Price | Speed |
|---------|-----------|------------|-------|
| Baidu | 10,000/mo | ¥0.001/img | Fast |
| remove.bg | 50/mo | $0.20/img | Fast |
| Adobe API | Trial | $0.15/img | Medium |

## Author

qy-cai (GitHub: github.com/qy-jscai)
Demo: www.instantbg.cn

## License

MIT
