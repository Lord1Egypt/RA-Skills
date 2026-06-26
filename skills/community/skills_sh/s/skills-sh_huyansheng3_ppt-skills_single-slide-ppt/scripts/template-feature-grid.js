const pptxgen = require('pptxgenjs');

/**
 * Example: Feature Grid Showcase
 * 
 * Ideal for displaying multiple features, capabilities, or options
 * in a clean, organized grid layout.
 */

async function createFeatureGridSlide() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Your Name';
  pptx.title = 'Feature Showcase';
  
  const slide = pptx.addSlide();
  
  // Light background theme
  slide.background = { color: 'f5f5f5' };
  
  // Header
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.9,
    fill: { color: '2C3E50' }
  });
  
  slide.addText('Product Features', {
    x: 0.5, y: 0.2, w: 9, h: 0.5,
    fontSize: 28, bold: true, color: 'ffffff',
    fontFace: 'Arial'
  });
  
  // Subtitle
  slide.addText('Everything you need in one platform', {
    x: 0.5, y: 1.1, w: 9, h: 0.3,
    fontSize: 14, color: '666666',
    fontFace: 'Arial', align: 'center'
  });
  
  // Features in 3x3 grid
  const features = [
    { icon: '🚀', title: 'Fast Performance', desc: 'Lightning-fast load times' },
    { icon: '🔒', title: 'Secure', desc: 'Enterprise-grade security' },
    { icon: '📊', title: 'Analytics', desc: 'Real-time insights' },
    { icon: '🌐', title: 'Global CDN', desc: 'Worldwide availability' },
    { icon: '🔧', title: 'Customizable', desc: 'Flexible configuration' },
    { icon: '📱', title: 'Mobile Ready', desc: 'Responsive design' },
    { icon: '🤝', title: 'Integrations', desc: '100+ integrations' },
    { icon: '💬', title: 'Support', desc: '24/7 customer care' },
    { icon: '📈', title: 'Scalable', desc: 'Grows with you' }
  ];
  
  const startX = 0.8;
  const startY = 1.6;
  const itemW = 2.8;
  const itemH = 1.2;
  const gapX = 0.2;
  const gapY = 0.2;
  const columns = 3;
  
  features.forEach((feat, idx) => {
    const col = idx % columns;
    const row = Math.floor(idx / columns);
    const x = startX + col * (itemW + gapX);
    const y = startY + row * (itemH + gapY);
    
    // Feature card with shadow effect (simulate with darker border)
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: itemW, h: itemH,
      fill: { color: 'ffffff' },
      line: { color: 'dddddd', width: 1 },
      rectRadius: 0.15
    });
    
    // Icon
    slide.addText(feat.icon, {
      x, y: y + 0.15, w: itemW, h: 0.4,
      fontSize: 32, align: 'center'
    });
    
    // Title
    slide.addText(feat.title, {
      x: x + 0.2, y: y + 0.55, w: itemW - 0.4, h: 0.3,
      fontSize: 13, bold: true, color: '2C3E50',
      fontFace: 'Arial', align: 'center'
    });
    
    // Description
    slide.addText(feat.desc, {
      x: x + 0.2, y: y + 0.85, w: itemW - 0.4, h: 0.25,
      fontSize: 10, color: '666666',
      fontFace: 'Arial', align: 'center'
    });
  });
  
  const outputPath = './feature-grid-slide.pptx';
  await pptx.writeFile({ fileName: outputPath });
  console.log('Slide created:', outputPath);
}

createFeatureGridSlide().catch(console.error);
