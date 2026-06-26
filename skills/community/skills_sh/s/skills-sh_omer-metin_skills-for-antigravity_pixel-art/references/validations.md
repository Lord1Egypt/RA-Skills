# Pixel Art - Validations

## Anti-aliasing Disabled in Renderer

### **Id**
pixelart-no-antialiasing
### **Severity**
error
### **Type**
regex
### **Pattern**
  - antialias:\s*true
  - antiAlias:\s*true
  - anti-alias:\s*true
  - image-rendering:\s*auto
  - smoothing:\\s*true
  - imageSmoothingEnabled\\s*=\\s*true
### **Message**
Anti-aliasing must be disabled for pixel art. Use antialias: false and nearest-neighbor filtering.
### **Fix Action**
Set antialias: false, pixelArt: true, and image-rendering: pixelated
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx
  - *.css

## Non-Integer Scale Values

### **Id**
pixelart-integer-scaling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setScale\\s*\\(\\s*[0-9]*\\.[0-9]+[^,\\)]*\\)
  - scale\\s*[:=]\\s*[0-9]*\\.[0-9]+(?!\\s*[*/])
  - scale\\(\\s*[0-9]*\\.[1-9]
  - zoom:\\s*[0-9]*\\.[0-9]+
### **Message**
Pixel art should use integer scaling only (1, 2, 3...). Non-integer scaling causes uneven pixels.
### **Fix Action**
Use Math.floor() to ensure integer scale values: Math.floor(screenWidth / gameWidth)
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Rotation Applied to Pixel Art Sprites

### **Id**
pixelart-rotation-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.rotation\\s*=\\s*[^0]
  - \\.angle\\s*=\\s*(?!0|90|180|270|-90|-180|-270)
  - rotate\\(\\s*(?!0|90|180|270|Math\\.PI|Math\\.PI\\s*/\\s*2)
  - transform:\\s*rotate\\(\\s*(?!0deg|90deg|180deg|270deg)
### **Message**
Rotating pixel art by non-90-degree angles destroys pixel grid. Use pre-rendered rotation frames instead.
### **Fix Action**
Create separate sprite frames for each rotation angle, or limit to 90-degree increments
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx
  - *.css

## Phaser Pixel Art Configuration

### **Id**
pixelart-phaser-config
### **Severity**
error
### **Type**
regex
### **Pattern**
  - pixelArt:\\s*false
  - roundPixels:\\s*false
### **Message**
Phaser config must have pixelArt: true and roundPixels: true for pixel art games.
### **Fix Action**
Add to Phaser config: render: { pixelArt: true, roundPixels: true, antialias: false }
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Excessive Color Count

### **Id**
pixelart-color-count-warning
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - #[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}.{0,100}#[0-9a-fA-F]{6}
### **Message**
Detected many color values. Pixel art typically uses 8-32 colors. Consider using a defined palette constant.
### **Fix Action**
Define colors in a palette object and reference by name: palette.skinLight, palette.skinDark
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx
  - *.css

## JPEG Format for Pixel Art

### **Id**
pixelart-jpeg-export
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \.jpe?g["']\s*(?:as\s+)?(?:sprite|texture|tileset|atlas|sheet)
  - load\.image\([^)]+\.jpe?g
  - load\.spritesheet\([^)]+\.jpe?g
  - src=['"][^'"]+sprite[^'"]*\.jpe?g
### **Message**
JPEG causes compression artifacts in pixel art. Use PNG format instead.
### **Fix Action**
Export sprites as PNG (indexed color for best results) instead of JPEG
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx
  - *.html

## Animation Frame Duration Too Short

### **Id**
pixelart-animation-too-fast
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - duration:\\s*[1-4][0-9](?![0-9])
  - frameTime:\\s*[1-4][0-9](?![0-9])
  - frameRate:\\s*[3-9][0-9]
### **Message**
Frame duration under 50ms (or frameRate over 30) may be too fast for pixel art. Typical range: 80-200ms.
### **Fix Action**
For walk cycles: 100-150ms. For idle: 200-400ms. For attacks: 50-100ms (only impact frames).
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Canvas 2D Context Missing Pixel Art Settings

### **Id**
pixelart-canvas-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - getContext\\(["']2d["']\\)(?![\\s\\S]{0,100}imageSmoothingEnabled\\s*=\\s*false)
### **Message**
Canvas 2D context should have imageSmoothingEnabled = false for pixel art.
### **Fix Action**
After getContext('2d'), add: ctx.imageSmoothingEnabled = false
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Spritesheet Loaded Without Frame Dimensions

### **Id**
pixelart-missing-framesize
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - load\\.spritesheet\\([^)]+\\)(?![\\s\\S]{0,30}frameWidth)
  - load\\.atlas\\([^)]+\\)(?![\\s\\S]{0,30}\\.json)
### **Message**
Spritesheet loading should specify frame dimensions or use JSON atlas for consistent frame sizes.
### **Fix Action**
Specify frameWidth and frameHeight, or export with JSON metadata from Aseprite
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Sprite Position Not Rounded

### **Id**
pixelart-position-rounding
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.x\\s*\\+=\\s*[^;]+\\*\\s*delta
  - \\.y\\s*\\+=\\s*[^;]+\\*\\s*delta
  - position\\.x\\s*\\+=\\s*velocity
  - position\\.y\\s*\\+=\\s*velocity
### **Message**
Sprite positions should be rounded to integers for rendering to prevent subpixel jitter.
### **Fix Action**
Store subpixel position separately, render at Math.floor(position). Example: renderX = Math.floor(subPixelX)
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Missing Pixelated Image Rendering

### **Id**
pixelart-css-rendering
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - canvas\\s*\\{[^}]+\\}(?![^}]*image-rendering)
  - \\.game[^{]*\\{[^}]+\\}(?![^}]*image-rendering)
  - #game[^{]*\\{[^}]+\\}(?![^}]*image-rendering)
### **Message**
Canvas or game container should have image-rendering: pixelated for crisp pixel art scaling.
### **Fix Action**
Add CSS: canvas { image-rendering: pixelated; image-rendering: crisp-edges; }
### **Applies To**
  - *.css
  - *.scss
  - *.less

## WebGL Texture Using Linear Filtering

### **Id**
pixelart-webgl-filtering
### **Severity**
error
### **Type**
regex
### **Pattern**
  - texture\\.minFilter\\s*=\\s*THREE\\.LinearFilter
  - texture\\.magFilter\\s*=\\s*THREE\\.LinearFilter
  - gl\\.texParameteri[^;]+LINEAR
### **Message**
Pixel art textures must use NEAREST filtering, not LINEAR. Linear filtering blurs pixels.
### **Fix Action**
Use NearestFilter: texture.minFilter = THREE.NearestFilter; texture.magFilter = THREE.NearestFilter
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Unity Sprite Filter Mode

### **Id**
pixelart-unity-filtermode
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - FilterMode\\.Bilinear
  - FilterMode\\.Trilinear
### **Message**
Unity sprites for pixel art should use FilterMode.Point to prevent blurring.
### **Fix Action**
Set sprite FilterMode to Point in import settings or via script
### **Applies To**
  - *.cs

## Godot Texture Filter Setting

### **Id**
pixelart-godot-filter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - texture_filter\\s*=\\s*[12345]
  - filter\\s*=\\s*true
### **Message**
Godot pixel art should use TEXTURE_FILTER_NEAREST (0) or filter = false.
### **Fix Action**
Set texture_filter = TEXTURE_FILTER_NEAREST in CanvasItem or material
### **Applies To**
  - *.gd
  - *.gdshader
  - *.tres
  - *.tscn