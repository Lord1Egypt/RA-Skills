// Figma Plugin - UI Prototype Importer
// This plugin imports JSON-generated prototypes into Figma

figma.showUI(__html__, { width: 400, height: 500 });

// Handle messages from UI
figma.ui.onmessage = (msg) => {
  if (msg.type === 'import-json') {
    try {
      const data = JSON.parse(msg.jsonData);
      
      if (data.children || data.nodes) {
        importPrototype(data);
      } else {
        figma.notify('Invalid JSON format', { error: true });
      }
    } catch (error) {
      figma.notify('Error parsing JSON: ' + error.message, { error: true });
    }
  }
  
  if (msg.type === 'create-components') {
    createComponentLibrary();
  }
  
  if (msg.type === 'close') {
    figma.closePlugin();
  }
};

async function importPrototype(data) {
  const nodes = data.children || data.nodes || [];
  
  if (nodes.length === 0) {
    figma.notify('No nodes to import', { error: true });
    return;
  }
  
  figma.notify(`Importing ${nodes.length} nodes...`);
  
  const createdNodes = [];
  
  for (const nodeData of nodes) {
    const node = await createNode(nodeData);
    if (node) {
      figma.currentPage.appendChild(node);
      createdNodes.push(node);
    }
  }
  
  // Select created nodes
  figma.currentPage.selection = createdNodes;
  
  // Zoom to fit
  figma.viewport.scrollAndZoomIntoView(createdNodes);
  
  figma.notify(`✓ Imported ${createdNodes.length} nodes successfully!`);
}

async function createNode(data) {
  try {
    switch (data.type) {
      case 'FRAME':
        return createFrame(data);
      case 'RECTANGLE':
        return createRectangle(data);
      case 'TEXT':
        return await createText(data);
      case 'COMPONENT':
        return createComponent(data);
      case 'ELLIPSE':
        return createEllipse(data);
      case 'LINE':
        return createLine(data);
      default:
        console.log('Unknown node type:', data.type);
        return null;
    }
  } catch (error) {
    console.error('Error creating node:', error);
    return null;
  }
}

function createFrame(data) {
  const frame = figma.createFrame();
  
  frame.name = data.name || 'Frame';
  frame.x = data.x || 0;
  frame.y = data.y || 0;
  frame.resize(data.width || 100, data.height || 100);
  
  // Apply fills
  if (data.fills) {
    frame.fills = data.fills.map(fill => convertFill(fill));
  }
  
  // Apply strokes
  if (data.strokes) {
    frame.strokes = data.strokes.map(stroke => convertFill(stroke));
    frame.strokeWeight = data.strokeWeight || 1;
  }
  
  // Apply corner radius
  if (data.cornerRadius) {
    frame.topLeftRadius = data.cornerRadius;
    frame.topRightRadius = data.cornerRadius;
    frame.bottomLeftRadius = data.cornerRadius;
    frame.bottomRightRadius = data.cornerRadius;
  }
  
  // Apply effects (shadows)
  if (data.effects) {
    frame.effects = data.effects.map(effect => convertEffect(effect));
  }
  
  // Add children
  if (data.children) {
    for (const childData of data.children) {
      const child = createNode(childData);
      if (child) {
        frame.appendChild(child);
      }
    }
  }
  
  return frame;
}

function createRectangle(data) {
  const rect = figma.createRectangle();
  
  rect.name = data.name || 'Rectangle';
  rect.x = data.x || 0;
  rect.y = data.y || 0;
  rect.resize(data.width || 100, data.height || 100);
  
  if (data.fills) {
    rect.fills = data.fills.map(fill => convertFill(fill));
  }
  
  if (data.strokes) {
    rect.strokes = data.strokes.map(stroke => convertFill(stroke));
    rect.strokeWeight = data.strokeWeight || 1;
  }
  
  if (data.cornerRadius) {
    rect.topLeftRadius = data.cornerRadius;
    rect.topRightRadius = data.cornerRadius;
    rect.bottomLeftRadius = data.cornerRadius;
    rect.bottomRightRadius = data.cornerRadius;
  }
  
  return rect;
}

async function createText(data) {
  const text = figma.createText();
  
  text.name = data.name || 'Text';
  text.x = data.x || 0;
  text.y = data.y || 0;
  
  // Load font
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });
  
  text.fontName = { family: "Inter", style: "Regular" };
  text.characters = data.characters || '';
  
  if (data.style) {
    if (data.style.fontSize) {
      text.fontSize = data.style.fontSize;
    }
    if (data.style.fontWeight) {
      // Map weight to style
      const weight = data.style.fontWeight;
      if (weight >= 700) {
        await figma.loadFontAsync({ family: "Inter", style: "Bold" });
        text.fontName = { family: "Inter", style: "Bold" };
      } else if (weight >= 500) {
        await figma.loadFontAsync({ family: "Inter", style: "Medium" });
        text.fontName = { family: "Inter", style: "Medium" };
      }
    }
  }
  
  if (data.style && data.style.fills) {
    text.fills = data.style.fills.map(fill => convertFill(fill));
  }
  
  return text;
}

function createComponent(data) {
  const component = figma.createComponent();
  
  component.name = data.name || 'Component';
  component.x = data.x || 0;
  component.y = data.y || 0;
  component.resize(data.width || 100, data.height || 100);
  
  if (data.fills) {
    component.fills = data.fills.map(fill => convertFill(fill));
  }
  
  if (data.strokes) {
    component.strokes = data.strokes.map(stroke => convertFill(stroke));
    component.strokeWeight = data.strokeWeight || 1;
  }
  
  if (data.cornerRadius) {
    component.topLeftRadius = data.cornerRadius;
    component.topRightRadius = data.cornerRadius;
    component.bottomLeftRadius = data.cornerRadius;
    component.bottomRightRadius = data.cornerRadius;
  }
  
  return component;
}

function createEllipse(data) {
  const ellipse = figma.createEllipse();
  
  ellipse.name = data.name || 'Ellipse';
  ellipse.x = data.x || 0;
  ellipse.y = data.y || 0;
  ellipse.resize(data.width || 100, data.height || 100);
  
  if (data.fills) {
    ellipse.fills = data.fills.map(fill => convertFill(fill));
  }
  
  return ellipse;
}

function createLine(data) {
  const line = figma.createLine();
  
  line.name = data.name || 'Line';
  line.x = data.x || 0;
  line.y = data.y || 0;
  
  // Set line points
  const width = data.width || 100;
  line.resize(width, 0);
  
  if (data.strokes) {
    line.strokes = data.strokes.map(stroke => convertFill(stroke));
    line.strokeWeight = data.strokeWeight || 1;
  }
  
  return line;
}

function convertFill(fill) {
  if (fill.type === 'SOLID') {
    const color = fill.color || { r: 0, g: 0, b: 0 };
    return {
      type: 'SOLID',
      color: {
        r: color.r || 0,
        g: color.g || 0,
        b: color.b || 0
      },
      opacity: color.a || 1
    };
  }
  
  // Default to solid black
  return { type: 'SOLID', color: { r: 0, g: 0, b: 0 } };
}

function convertEffect(effect) {
  if (effect.type === 'DROP_SHADOW') {
    return {
      type: 'DROP_SHADOW',
      color: {
        r: effect.color?.r || 0,
        g: effect.color?.g || 0,
        b: effect.color?.b || 0,
        a: effect.color?.a || 0.5
      },
      offset: {
        x: effect.offset?.x || 0,
        y: effect.offset?.y || 4
      },
      radius: effect.radius || 8,
      spread: effect.spread || 0,
      visible: true,
      blendMode: 'NORMAL'
    };
  }
  
  return effect;
}

async function createComponentLibrary() {
  figma.notify('Creating component library...');
  
  const components = [
    {
      name: 'Button/Primary',
      width: 120,
      height: 40,
      fills: [{ type: 'SOLID', color: { r: 0.094, g: 0.565, b: 1 } }],
      cornerRadius: 4
    },
    {
      name: 'Button/Default',
      width: 120,
      height: 40,
      fills: [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }],
      strokes: [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }],
      cornerRadius: 4
    },
    {
      name: 'Input/Text',
      width: 200,
      height: 35,
      fills: [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }],
      strokes: [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }],
      cornerRadius: 4
    }
  ];
  
  const created = [];
  let yOffset = 0;
  
  for (const compData of components) {
    compData.y = yOffset;
    const component = createComponent(compData);
    if (component) {
      figma.currentPage.appendChild(component);
      created.push(component);
      yOffset += compData.height + 20;
    }
  }
  
  figma.currentPage.selection = created;
  figma.viewport.scrollAndZoomIntoView(created);
  
  figma.notify(`✓ Created ${created.length} components!`);
}