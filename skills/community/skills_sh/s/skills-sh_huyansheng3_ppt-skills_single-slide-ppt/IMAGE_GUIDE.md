# Image Enhancement Guide for Single-Slide PPT

This guide explains how to enhance your single-slide PowerPoint presentations with relevant images downloaded from the web.

## When to Use Images

Add images to strengthen your message when creating slides about:

- **Technical architectures** - Official documentation diagrams
- **Product comparisons** - Before/after screenshots
- **UI/UX concepts** - Interface mockups or wireframes
- **API limitations** - Architecture diagrams showing constraints
- **Feature showcases** - Product screenshots or demos

## Image Discovery Workflow

### Step 1: Search for Relevant Content

Use `search_web` to find official documentation or resources:

```javascript
// Example search queries:
- "VSCode extension API architecture official documentation"
- "[Product Name] architecture diagram official docs"
- "[Technology] system architecture GitHub"
```

### Step 2: Fetch and Extract Image URLs

Use `fetch_web` to get the documentation page content:

```javascript
// Look for image URLs in the content:
- <img src="/assets/...">
- ![diagram](https://...)
- background-image: url(...)
```

### Step 3: Download Images

Use `curl` or `execSync` to download images:

```javascript
const { execSync } = require('child_process');

function downloadImage(url, outputPath) {
  try {
    execSync(`curl -o ${outputPath} "${url}"`, { stdio: 'inherit' });
    console.log(`✓ Downloaded: ${outputPath}`);
    return true;
  } catch (error) {
    console.error(`✗ Failed to download: ${error.message}`);
    return false;
  }
}

// Example:
downloadImage(
  'https://code.visualstudio.com/assets/api/ux-guidelines/examples/architecture-containers.png',
  'workspace/vscode-architecture.png'
);
```

## Complete Example: Technical Architecture Slide

```javascript
const pptxgen = require('pptxgenjs');
const { execSync } = require('child_process');
const path = require('path');

async function createArchitectureSlide() {
  const workDir = path.join(__dirname);
  
  // Step 1: Download relevant images
  console.log('Downloading architecture diagrams...');
  
  const images = [
    {
      url: 'https://code.visualstudio.com/assets/api/ux-guidelines/examples/architecture-containers.png',
      path: path.join(workDir, 'vscode-containers.png')
    },
    {
      url: 'https://code.visualstudio.com/assets/api/ux-guidelines/examples/architecture-sections.png',
      path: path.join(workDir, 'vscode-sections.png')
    }
  ];
  
  for (const img of images) {
    try {
      execSync(`curl -o "${img.path}" "${img.url}"`, { stdio: 'inherit' });
      console.log(`✓ Downloaded: ${path.basename(img.path)}`);
    } catch (error) {
      console.error(`✗ Failed: ${path.basename(img.path)}`);
    }
  }
  
  // Step 2: Create presentation
  console.log('Creating presentation...');
  
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Your Team';
  pptx.title = 'VSCode Extension Architecture';
  
  const slide = pptx.addSlide();
  
  // Background
  slide.background = { color: 'FFFFFF' };
  
  // Header bar
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: 'fc5a1f' }
  });
  
  slide.addText('VSCode 扩展架构限制', {
    x: 0.5, y: 0.18, w: 9, h: 0.45,
    fontSize: 26, bold: true, color: 'ffffff',
    fontFace: 'Arial'
  });
  
  // Left: Architecture diagram
  slide.addImage({
    path: images[0].path,
    x: 0.5,
    y: 1.2,
    w: 4.8,
    h: 2.7
  });
  
  // Image caption
  slide.addText('VSCode 只对插件开放固定的"插槽"（Containers）', {
    x: 0.5, y: 4.0, w: 4.8, h: 0.3,
    fontSize: 10, color: '707070', italic: true,
    fontFace: 'Arial', align: 'center'
  });
  
  // Right: Key limitations
  slide.addText('架构限制', {
    x: 5.5, y: 1.2, w: 4.2, h: 0.4,
    fontSize: 20, bold: true, color: 'fc5a1f',
    fontFace: 'Arial'
  });
  
  // Limitation cards
  const limitations = [
    { title: 'API 受限', desc: '只能访问预定义的扩展点' },
    { title: 'UI 受限', desc: '无法自由定制核心界面' },
    { title: '性能受限', desc: '运行在独立的 Extension Host 进程' }
  ];
  
  limitations.forEach((item, idx) => {
    const y = 1.7 + idx * 1.0;
    
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 5.5, y: y, w: 4.2, h: 0.85,
      fill: { color: 'f8f8f8' },
      rectRadius: 0.1
    });
    
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 5.5, y: y, w: 0.06, h: 0.85,
      fill: { color: 'fc5a1f' }
    });
    
    slide.addText(item.title, {
      x: 5.7, y: y + 0.15, w: 3.9, h: 0.3,
      fontSize: 14, bold: true, color: '434343',
      fontFace: 'Arial'
    });
    
    slide.addText(item.desc, {
      x: 5.7, y: y + 0.45, w: 3.9, h: 0.3,
      fontSize: 11, color: '707070',
      fontFace: 'Arial'
    });
  });
  
  // Save
  const outputPath = path.join(workDir, 'architecture-slide.pptx');
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ Presentation saved: ${outputPath}`);
}

createArchitectureSlide().catch(console.error);
```

## Best Practices

### Image Sources Priority

1. **Official documentation** (highest trust)
   - Product official website
   - GitHub official repository
   - API documentation pages

2. **Technical blogs** (medium trust)
   - Engineering team blogs
   - Technical conference presentations
   - Well-known tech publications

3. **Community resources** (verify quality)
   - Stack Overflow diagrams
   - Medium articles
   - Developer tutorials

### Image Quality Checklist

- ✅ High resolution (at least 1000px width)
- ✅ Clear and readable text in diagrams
- ✅ Relevant to the content
- ✅ From authoritative sources
- ✅ Appropriate licensing/attribution

### Layout Tips with Images

**Left-Right Layout:**
```
┌────────────────────────────────┐
│  Image/Diagram  │  Text Cards  │
│  (explains      │  (highlights │
│   concept)      │   points)    │
└────────────────────────────────┘
```

**Top-Bottom Layout:**
```
┌────────────────────────────────┐
│     Image/Diagram (full width) │
├────────────────────────────────┤
│  Key Points Cards (below)      │
└────────────────────────────────┘
```

**Comparison Layout:**
```
┌────────────────────────────────┐
│  Before Image  │  After Image  │
├────────────────┼───────────────┤
│  Before Text   │  After Text   │
└────────────────────────────────┘
```

## Common Image Sources by Topic

### VSCode / IDE
- https://code.visualstudio.com/api/ux-guidelines/overview
- https://code.visualstudio.com/assets/api/...

### React / Frontend
- https://react.dev/learn
- https://reactjs.org/docs/...

### System Architecture
- GitHub repository docs/ folders
- Architecture Decision Records (ADRs)
- System design documentation

### API Documentation
- Swagger/OpenAPI spec visualizations
- Postman collections
- API reference pages

## Error Handling

Always include fallback logic when downloading images:

```javascript
async function downloadImageSafely(url, outputPath) {
  try {
    execSync(`curl -o "${outputPath}" "${url}"`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    console.warn(`⚠️  Image download failed: ${url}`);
    console.warn('Continuing without image...');
    return false;
  }
}

// Usage in slide creation
const imageDownloaded = await downloadImageSafely(imageUrl, imagePath);

if (imageDownloaded) {
  slide.addImage({ path: imagePath, x: 0.5, y: 1.2, w: 4.8, h: 2.7 });
} else {
  // Fallback: use text or emoji instead
  slide.addText('📊', {
    x: 2.0, y: 2.0, w: 2.0, h: 1.5,
    fontSize: 80, align: 'center'
  });
}
```

## Attribution

When using images from external sources, always add attribution:

```javascript
slide.addText('Source: VSCode Official Documentation', {
  x: 0.5, y: 5.2, w: 9, h: 0.2,
  fontSize: 8, color: '999999', italic: true,
  fontFace: 'Arial', align: 'right'
});
```

## Summary

The image enhancement workflow:

1. 🔍 **Search** for relevant official documentation
2. 🌐 **Fetch** the page content to find image URLs
3. ⬇️  **Download** images using curl
4. 🖼️  **Add** images to slide with proper layout
5. 📝 **Caption** images with source attribution
6. ✅ **Validate** final slide quality

This approach creates more authoritative, professional, and visually engaging presentations.
