#!/usr/bin/env node

/**
 * SVG Artist - Helper script for generating SVG images
 *
 * Usage:
 *   node generate_svg.js <description> <output.png>
 *   node generate_svg.js --template <template-name> <output.png>
 *
 * This script provides base templates. The LLM should write custom SVG
 * code directly for best results.
 */

const fs = require('fs');
const { execSync } = require('child_process');

const args = process.argv.slice(2);

// Parse arguments
let description = '';
let outputPath = '/tmp/svg_output.png';
let template = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--template' || args[i] === '-t') {
    template = args[++i];
  } else if (args[i] === '--output' || args[i] === '-o') {
    outputPath = args[++i];
  } else if (!args[i].startsWith('-')) {
    if (!description) {
      description = args[i];
    } else {
      outputPath = args[i];
    }
  }
}

// SVG Templates
const templates = {
  blank: (size = 400) => `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='white'/>
</svg>`,

  canvas: (size = 400, bg = '#87CEEB') => `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='${bg}'/>
  <!-- Add your shapes here -->
</svg>`,

  character: (size = 400) => `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='#E6F3FF'/>

  <!-- Body -->
  <ellipse cx='${size/2}' cy='${size*0.6}' rx='${size*0.25}' ry='${size*0.18}' fill='#D2691E' stroke='#8B4513' stroke-width='3'/>

  <!-- Head -->
  <ellipse cx='${size/2}' cy='${size*0.35}' rx='${size*0.18}' ry='${size*0.15}' fill='#D2691E' stroke='#8B4513' stroke-width='3'/>

  <!-- Eyes -->
  <ellipse cx='${size*0.42}' cy='${size*0.33}' rx='${size*0.04}' ry='${size*0.04}' fill='white' stroke='black' stroke-width='2'/>
  <ellipse cx='${size*0.58}' cy='${size*0.33}' rx='${size*0.04}' ry='${size*0.04}' fill='white' stroke='black' stroke-width='2'/>
  <ellipse cx='${size*0.43}' cy='${size*0.335}' rx='${size*0.02}' ry='${size*0.02}' fill='black'/>
  <ellipse cx='${size*0.59}' cy='${size*0.335}' rx='${size*0.02}' ry='${size*0.02}' fill='black'/>
  <ellipse cx='${size*0.435}' cy='${size*0.325}' rx='${size*0.008}' ry='${size*0.008}' fill='white'/>
  <ellipse cx='${size*0.595}' cy='${size*0.325}' rx='${size*0.008}' ry='${size*0.008}' fill='white'/>

  <!-- Nose -->
  <ellipse cx='${size/2}' cy='${size*0.4}' rx='${size*0.03}' ry='${size*0.02}' fill='black'/>

  <!-- Smile -->
  <path d='M ${size*0.45} ${size*0.42} A ${size*0.05} ${size*0.05} 0 0 0 ${size*0.55} ${size*0.42}' stroke='#8B4513' stroke-width='2' fill='none'/>

  <!-- Legs -->
  <ellipse cx='${size*0.35}' cy='${size*0.78}' rx='${size*0.05}' ry='${size*0.07}' fill='#D2691E' stroke='#8B4513' stroke-width='2'/>
  <ellipse cx='${size*0.65}' cy='${size*0.78}' rx='${size*0.05}' ry='${size*0.07}' fill='#D2691E' stroke='#8B4513' stroke-width='2'/>
</svg>`,

  icon: (size = 256) => `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='transparent'/>
  <!-- Icon content centered at ${size/2}, ${size/2} -->
  <circle cx='${size/2}' cy='${size/2}' r='${size*0.35}' fill='#4A90D9'/>
</svg>`,

  scene: (size = 400) => `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <!-- Sky -->
  <rect x='0' y='0' width='${size}' height='${size*0.6}' fill='#87CEEB'/>

  <!-- Sun -->
  <circle cx='${size*0.8}' cy='${size*0.15}' r='${size*0.08}' fill='#FFD700'/>

  <!-- Ground -->
  <rect x='0' y='${size*0.6}' width='${size}' height='${size*0.4}' fill='#90EE90'/>

  <!-- Add your scene elements here -->
</svg>`
};

// If template specified, use it
if (template && templates[template]) {
  const svg = templates[template](400);
  // Use outputPath from args if provided
  const finalOutput = args[args.length - 1].endsWith('.png') ? args[args.length - 1] : outputPath;
  saveAndConvert(svg, finalOutput);
  console.log(`Template '${template}' saved to ${finalOutput}`);
  process.exit(0);
}

// If no template, show available templates
if (!description || description === 'help') {
  console.log(`
SVG Artist - Helper Script

Usage:
  node generate_svg.js <description> <output.png>
  node generate_svg.js --template <name> <output.png>

Available Templates:
  blank     - Empty white canvas
  canvas    - Solid color background
  character - Basic character template
  icon      - Icon-sized square
  scene     - Outdoor scene with sky/ground

Note: For best results, have the LLM write custom SVG code directly.
This script just provides starting templates.

Example:
  node generate_svg.js --template character /tmp/char.png
`);
  process.exit(0);
}

// Save SVG and convert to PNG
function saveAndConvert(svg, output) {
  const svgPath = output.replace('.png', '.svg');
  fs.writeFileSync(svgPath, svg);

  try {
    execSync(`rsvg-convert "${svgPath}" -o "${output}"`, { stdio: 'pipe' });
  } catch (e) {
    try {
      execSync(`convert "${svgPath}" "${output}"`, { stdio: 'pipe' });
    } catch (e2) {
      console.error('Failed to convert SVG. Install rsvg-convert or ImageMagick.');
      console.error(`SVG saved at: ${svgPath}`);
      process.exit(1);
    }
  }
}

// Default output for description (LLM should generate the actual SVG)
console.log(`Description: ${description}`);
console.log(`Output: ${outputPath}`);
console.log(`\nNote: This script provides templates only.`);
console.log(`For custom images, have the LLM write SVG code directly.`);
