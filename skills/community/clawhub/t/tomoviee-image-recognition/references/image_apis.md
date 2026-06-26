# Tomoviee Image Generation APIs

## Overview
Tomoviee provides three image generation APIs for reference-based generation, localized editing, and intelligent segmentation.

## API Endpoints

### 1. Image-to-Image (tm_reference_img2img)
**Generate new image based on reference image**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_reference_img2img`

**Parameters**:
- `prompt` (required): Text description (reference + preserve + modify/add)
- `image` (required): Reference image URL (JPG/JPEG/PNG/WEBP, <200M)
- `resolution`: Image resolution - `512*512` (default), `768*768`, `1024*1024`
- `aspect_ratio`: Image aspect ratio - `1:1` (default), `16:9`, `9:16`, `4:3`, `3:4`
- `image_num`: Number of images to generate - 1 to 4 (default: 1)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Reimagine existing images with modifications
- Generate variations while preserving style/composition
- Change specific elements (clothing, background, objects)
- Maintain overall structure while altering details

**Prompt Structure**:
```
[Reference description] + [Elements to preserve] + [Modifications/additions]
```

**Example**:
```python
task_id = client.image_to_image(
    prompt="A woman in business attire, preserve facial features and pose, change background to modern office with floor-to-ceiling windows",
    image="https://example.com/portrait.jpg",
    resolution="1024*1024",
    aspect_ratio="3:4",
    image_num=2  # Generate 2 variations
)
```

**Important Notes**:
- The reference image guides style, composition, and structure
- Prompt should explicitly state what to preserve vs. modify
- Higher resolution = better detail but slower generation
- Multiple images (image_num > 1) generate variations with same prompt

---

### 2. Image Redrawing (tm_redrawing)
**Redraw specific region of image using mask**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_redrawing`

**Parameters**:
- `prompt` (required): Description of what to redraw in masked area
- `image` (required): Original image URL (JPG/JPEG/PNG/WEBP, <200M)
- `mask` (required): Mask image URL (white = redraw area, black = preserve area)
- `resolution`: Image resolution - `512*512` (default), `768*768`, `1024*1024`
- `aspect_ratio`: Image aspect ratio - `1:1` (default), `16:9`, `9:16`, `4:3`, `3:4`
- `image_num`: Number of images to generate - 1 to 4 (default: 1)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Remove/replace objects or people
- Edit specific image regions
- Inpainting and outpainting
- Fix or enhance localized areas
- Change backgrounds while keeping foreground

**Mask Requirements**:
- Same dimensions as input image
- White pixels (255, 255, 255) = areas to redraw
- Black pixels (0, 0, 0) = areas to preserve unchanged
- Grayscale values = partial blending (use with caution)

**Example**:
```python
# Remove person from photo
task_id = client.image_redrawing(
    prompt="Empty beach sand with natural texture",
    image="https://example.com/beach-with-person.jpg",
    mask="https://example.com/person-mask.png",  # White where person is
    resolution="1024*1024",
    image_num=1
)

# Change background
task_id = client.image_redrawing(
    prompt="Sunset sky with orange and purple clouds",
    image="https://example.com/portrait.jpg",
    mask="https://example.com/background-mask.png",  # White = background area
    resolution="1024*1024"
)
```

**Creating Masks**:
You can create masks using:
- Image editing software (Photoshop, GIMP)
- Programmatic tools (OpenCV, PIL/Pillow)
- The Image Recognition API (see below) to auto-generate masks

---

### 3. Image Recognition (tm_reference_img2mask)
**Recognize and segment image regions based on prompt**

**Endpoint**: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_reference_img2mask`

**Parameters**:
- `prompt` (required): Description of objects/regions to recognize
- `image` (required): Image URL to analyze (JPG/JPEG/PNG/WEBP, <200M)
- `callback`: Optional callback URL for async notification
- `params`: Optional transparent parameters passed back in callback

**Use Cases**:
- Generate masks for the Redrawing API
- Automatically segment objects in images
- Identify and isolate specific regions
- Create selection masks without manual editing
- Batch processing of similar images

**Output**:
Returns mask images where recognized objects are white, background is black.
Can return multiple masks if multiple objects match the prompt.

**Example**:
```python
# Recognize all people in image
task_id = client.image_recognition(
    prompt="people",
    image="https://example.com/group-photo.jpg"
)

# Recognize specific objects
task_id = client.image_recognition(
    prompt="the red car in the foreground",
    image="https://example.com/street-scene.jpg"
)

# Recognize background
task_id = client.image_recognition(
    prompt="sky and clouds",
    image="https://example.com/landscape.jpg"
)
```

**Recognition + Redrawing Workflow**:
```python
# Step 1: Recognize object to create mask
recognition_task = client.image_recognition(
    prompt="person in center",
    image="https://example.com/photo.jpg"
)
recognition_result = client.poll_until_complete(recognition_task)
mask_url = json.loads(recognition_result['result'])['mask_path'][0]

# Step 2: Use generated mask to redraw that region
redraw_task = client.image_redrawing(
    prompt="beautiful garden with flowers",
    image="https://example.com/photo.jpg",
    mask=mask_url  # Use auto-generated mask
)
redraw_result = client.poll_until_complete(redraw_task)
final_image = json.loads(redraw_result['result'])['image_path'][0]
```

---

## Common Parameters

### Resolution Options
- `512*512`: Fast generation, lower detail
- `768*768`: Balanced speed and quality
- `1024*1024`: Best quality, slower generation

### Aspect Ratio Options
- `1:1`: Square - Instagram, profile pictures
- `16:9`: Landscape - desktop wallpaper, presentations
- `9:16`: Portrait - mobile wallpaper, stories
- `4:3`: Traditional photo format
- `3:4`: Portrait photo format

### Image Number (image_num)
- `1`: Single image (fastest)
- `2-4`: Multiple variations (same prompt, different results)
- Useful for A/B testing or getting options to choose from

---

## Async Workflow

All image APIs are asynchronous:

1. **Create Task**: Call API endpoint → receive `task_id`
2. **Poll Status**: Call unified result endpoint with `task_id`
3. **Check Status**: 
   - `1` = Queued
   - `2` = Processing
   - `3` = Success (images ready)
   - `4` = Failed
   - `5` = Cancelled
   - `6` = Timeout
4. **Get Result**: When status=3, extract image URL(s) from result JSON

**Unified Result Endpoint**: `https://openapi.wondershare.cc/v1/open/pub/task`

**Example Workflow**:
```python
# Create task
task_id = client.image_to_image(prompt="...", image="...", image_num=2)

# Poll for completion
result = client.poll_until_complete(task_id, poll_interval=5, timeout=300)

# Extract image URLs
import json
result_data = json.loads(result['result'])
image_urls = result_data['image_path']  # List of URLs (length = image_num)
```

---

## Prompt Engineering Tips

### Image-to-Image Prompts
**Structure**: `[Reference] + [Preserve] + [Modify]`

**Good Examples**:
- "A modern kitchen with white cabinets, preserve layout and appliance positions, change color scheme to navy blue and gold accents"
- "Portrait of a woman, keep facial features and expression, change hairstyle to long wavy hair and add glasses"
- "Street scene with cars, maintain composition and perspective, change time to sunset with golden hour lighting"

**Avoid**:
- Vague prompts: "make it better"
- No preservation guidance: "different background" (what else to keep?)
- Conflicting instructions: "keep everything the same but completely different style"

### Redrawing Prompts
**Structure**: `[What to draw in masked area]`

**Good Examples**:
- "Clear blue sky with white fluffy clouds"
- "Modern glass windows with reflections"
- "Natural grass texture with small wildflowers"
- "Empty wooden table surface"

**Avoid**:
- Mentioning what to remove: "remove the person" (just describe what replaces it)
- Complex multi-object prompts in small masks
- Instructions about preserved areas (mask already defines this)

### Recognition Prompts
**Structure**: `[Objects/regions to identify]`

**Good Examples**:
- "person" / "all people"
- "the red car"
- "sky and clouds"
- "foreground objects"
- "background"
- "text and logos"

**Avoid**:
- Overly specific if object isn't clearly visible
- Multiple unrelated objects (split into separate calls)
- Negations ("not the person") - describe what you want, not what you don't

---

## Error Handling

**Common Errors**:
- `400`: Invalid parameters (check resolution format, aspect_ratio, image_num range)
- `401`: Authentication failed
- `413`: Image too large (must be <200M)
- `422`: Invalid image format or mask doesn't match image dimensions
- Task status `4`: Generation failed (check prompt clarity or image quality)

**Best Practices**:
- Validate image URLs are publicly accessible
- Ensure masks match image dimensions exactly
- Keep prompts clear and specific
- Use lower resolutions for testing, higher for final generation
- Implement retry logic with exponential backoff

---

## Quota and Limits

- File size: <200M per image
- Supported formats: JPG, JPEG, PNG, WEBP
- Image number range: 1-4 per request
- Generation time: Typically 30 seconds to 2 minutes
- Concurrent tasks: Check your plan limits

---

## Comparison

| Feature | Image-to-Image | Redrawing | Recognition |
|---------|----------------|-----------|-------------|
| Purpose | Reimagine entire image | Edit specific region | Generate masks |
| Inputs | Image + prompt | Image + mask + prompt | Image + prompt |
| Output | Modified image(s) | Image with region redrawn | Mask image(s) |
| Use Global/Local | Global transformation | Localized editing | N/A (tool for Redrawing) |
| Prompt Focus | Overall changes | What replaces masked area | What to segment |
| Typical Use | Style transfer, variations | Object removal, background change | Automation for Redrawing |

**When to use which**:
- **Image-to-Image**: Want to change overall style/theme while keeping structure
- **Redrawing**: Need precise control over specific regions (with manual or auto mask)
- **Recognition**: Automate mask creation for Redrawing workflow
