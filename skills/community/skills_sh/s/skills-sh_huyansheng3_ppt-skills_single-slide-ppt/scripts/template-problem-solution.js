const pptxgen = require('pptxgenjs');

/**
 * Example: Problem → Solution Comparison Slide
 * 
 * This template demonstrates the most common single-slide pattern:
 * - Left side: Problem/limitation cards
 * - Middle: Arrow connector
 * - Right side: Solution/capability features
 * - Bottom: Core value proposition
 */

async function createProblemSolutionSlide() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Your Name';
  pptx.title = 'Problem to Solution';
  
  const slide = pptx.addSlide();
  
  // Background - Dark theme
  slide.background = { color: '1a1a2e' };
  
  // Header with gradient effect (use solid color as PptxGenJS doesn't support gradients)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: '4a00e0' }
  });
  
  // Main title
  slide.addText('Problem → Solution Framework', {
    x: 0.5, y: 0.18, w: 9, h: 0.5,
    fontSize: 26, bold: true, color: 'ffffff',
    fontFace: 'Arial'
  });
  
  // LEFT SECTION - Problems
  slide.addText('🚫 Current Limitations', {
    x: 0.4, y: 1.0, w: 4, h: 0.4,
    fontSize: 14, bold: true, color: 'ff6b6b',
    fontFace: 'Arial'
  });
  
  // Problem Card 1
  addProblemCard(slide, pptx, {
    x: 0.4, y: 1.5,
    title: 'Issue #1',
    description: 'Description of the first limitation or problem'
  });
  
  // Problem Card 2
  addProblemCard(slide, pptx, {
    x: 0.4, y: 2.5,
    title: 'Issue #2',
    description: 'Description of the second limitation or problem'
  });
  
  // Comparison boxes at bottom
  addComparisonBox(slide, pptx, {
    x: 0.5, y: 3.6,
    label: 'Old Way',
    icon: '🧩',
    description: 'Limited approach',
    type: 'problem'
  });
  
  // MIDDLE SECTION - Arrow
  slide.addText('➔', {
    x: 4.6, y: 2.5, w: 0.6, h: 0.6,
    fontSize: 36, color: '8e2de2',
    align: 'center', valign: 'middle'
  });
  
  // RIGHT SECTION - Solutions
  slide.addText('✅ New Capabilities', {
    x: 5.3, y: 1.0, w: 4, h: 0.4,
    fontSize: 14, bold: true, color: '51cf66',
    fontFace: 'Arial'
  });
  
  // Feature Grid (2x3)
  const features = [
    { icon: '🔧', text: 'Feature 1' },
    { icon: '⚡', text: 'Feature 2' },
    { icon: '💻', text: 'Feature 3' },
    { icon: '📝', text: 'Feature 4' },
    { icon: '👻', text: 'Feature 5' },
    { icon: '🎨', text: 'Feature 6' }
  ];
  
  addFeatureGrid(slide, pptx, features, {
    startX: 5.3,
    startY: 1.45,
    columns: 2
  });
  
  // Solution comparison box
  addComparisonBox(slide, pptx, {
    x: 7.5, y: 3.6,
    label: 'New Way',
    icon: '👑',
    description: 'Full control',
    type: 'solution'
  });
  
  // Core Value Card
  addValueCard(slide, pptx, {
    x: 5.3, y: 3.6, w: 2.0,
    title: '🎯 Core Value',
    description: 'Clear statement of the transformation achieved'
  });
  
  // Save
  const outputPath = './problem-solution-slide.pptx';
  await pptx.writeFile({ fileName: outputPath });
  console.log('Slide created:', outputPath);
}

// Helper Functions

function addProblemCard(slide, pptx, options) {
  const { x, y, title, description } = options;
  const w = 4.2, h = 0.95;
  
  // Card background
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: '2d1f1f' }
  });
  
  // Left accent border
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w: 0.08, h,
    fill: { color: 'ff6b6b' }
  });
  
  // Title
  slide.addText(title, {
    x: x + 0.2, y: y + 0.05, w: w - 0.3, h: 0.3,
    fontSize: 12, bold: true, color: 'ff6b6b',
    fontFace: 'Arial'
  });
  
  // Description
  slide.addText(description, {
    x: x + 0.2, y: y + 0.37, w: w - 0.3, h: 0.55,
    fontSize: 9, color: 'a0a0a0',
    fontFace: 'Arial', wrap: true
  });
}

function addComparisonBox(slide, pptx, options) {
  const { x, y, label, icon, description, type } = options;
  const w = 2.0, h = 1.35;
  const color = type === 'problem' ? 'ff6b6b' : '51cf66';
  const bgColor = type === 'problem' ? '2a1a1a' : '1a2a1a';
  const lineStyle = type === 'problem' ? { dashType: 'dash', width: 1 } : { width: 2 };
  
  // Box
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: bgColor },
    line: { color, ...lineStyle }
  });
  
  // Label
  slide.addText(label, {
    x, y: y + 0.08, w, h: 0.3,
    fontSize: 11, bold: true, color,
    fontFace: 'Arial', align: 'center'
  });
  
  // Icon
  slide.addText(icon, {
    x, y: y + 0.35, w, h: 0.5,
    fontSize: 30, align: 'center'
  });
  
  // Description
  slide.addText(description, {
    x, y: y + 0.85, w, h: 0.3,
    fontSize: 9, color: '888888',
    fontFace: 'Arial', align: 'center'
  });
}

function addFeatureGrid(slide, pptx, features, options) {
  const { startX, startY, columns = 2 } = options;
  const itemW = 2.2, itemH = 0.6;
  const gapX = 0.1, gapY = 0.08;
  
  features.forEach((feat, idx) => {
    const col = idx % columns;
    const row = Math.floor(idx / columns);
    const x = startX + col * (itemW + gapX);
    const y = startY + row * (itemH + gapY);
    
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: itemW, h: itemH,
      fill: { color: '1a2a1a' },
      line: { color: '51cf66', width: 0.5 },
      rectRadius: 0.08
    });
    
    slide.addText(feat.icon + ' ' + feat.text, {
      x: x + 0.1, y: y + 0.12, w: itemW - 0.2, h: itemH - 0.24,
      fontSize: 10, color: 'e0e0e0',
      fontFace: 'Arial', valign: 'middle'
    });
  });
}

function addValueCard(slide, pptx, options) {
  const { x, y, w, title, description } = options;
  const h = 1.35;
  
  // Card background
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: '1a2d1a' }
  });
  
  // Left accent border
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w: 0.08, h,
    fill: { color: '51cf66' }
  });
  
  // Title
  slide.addText(title, {
    x: x + 0.15, y: y + 0.1, w: w - 0.2, h: 0.35,
    fontSize: 13, bold: true, color: '51cf66',
    fontFace: 'Arial'
  });
  
  // Description
  slide.addText(description, {
    x: x + 0.15, y: y + 0.45, w: w - 0.2, h: 0.85,
    fontSize: 9, color: 'a0a0a0',
    fontFace: 'Arial', wrap: true
  });
}

// Run
createProblemSolutionSlide().catch(console.error);
