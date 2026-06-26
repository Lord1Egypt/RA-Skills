#!/usr/bin/env bun
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { execSync } from 'child_process';

const args = process.argv.slice(2);
const helpText = `
Slide Editor Injector

Usage:
  slide-editor <html-file> [options]

Options:
  --inline      Embed editor bundle directly in HTML (single file)
  --link        Reference external bundle file (creates separate .bundle.js)
  --remove      Remove editor from HTML
  --enable      Auto-enable editor (add ?edit=1 check)
  --open        Open in browser after injection (with ?edit=1)
  -o <file>     Output to different file

Examples:
  slide-editor presentation.html --inline --enable --open
  slide-editor presentation.html --link
  slide-editor presentation.html --remove
`;

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(helpText);
  process.exit(0);
}

const htmlFile = resolve(args[0]!);
const inline = args.includes('--inline');
const link = args.includes('--link');
const remove = args.includes('--remove');
const enable = args.includes('--enable');
const shouldOpen = args.includes('--open');
const outputIdx = args.indexOf('-o');
const outputFile = outputIdx > -1 ? resolve(args[outputIdx + 1]!) : htmlFile;

if (!existsSync(htmlFile)) {
  console.error(`Error: File not found: ${htmlFile}`);
  process.exit(1);
}

// Read HTML
let html = readFileSync(htmlFile, 'utf-8');

// Remove existing editor elements
const patterns = [
  /<!-- SLIDE_EDITOR_START -->[\s\S]*?<!-- SLIDE_EDITOR_END -->/g,
  /<script[^>]*src=["']editor\.bundle\.js["'][^>]*><\/script>/gi,
  /<script[^>]*>window\.__openclawEditor\.enable\(\);<\/script>/gi,
];

for (const pattern of patterns) {
  html = html.replace(pattern, '');
}

// If removing, write and exit
if (remove) {
  writeFileSync(outputFile, html);
  console.log(`✓ Editor removed from: ${outputFile}`);
  process.exit(0);
}

// Build the injection
let injection = '';

if (inline) {
  // Find the bundle
  const bundlePath = resolve(import.meta.dir, 'dist/editor.bundle.js');
  if (!existsSync(bundlePath)) {
    console.error('Error: Bundle not found. Run "bun run build" first.');
    process.exit(1);
  }
  const bundle = readFileSync(bundlePath, 'utf-8');

  injection = `
<!-- SLIDE_EDITOR_START -->
<script>
// SLIDE_EDITOR_BUNDLE
${bundle}
</script>
<!-- SLIDE_EDITOR_END -->
`;
} else if (link) {
  // Copy bundle to target directory
  const bundlePath = resolve(import.meta.dir, 'dist/editor.bundle.js');
  if (!existsSync(bundlePath)) {
    console.error('Error: Bundle not found. Run "bun run build" first.');
    process.exit(1);
  }
  const targetDir = dirname(outputFile);
  const targetBundlePath = resolve(targetDir, 'editor.bundle.js');
  const bundle = readFileSync(bundlePath, 'utf-8');
  writeFileSync(targetBundlePath, bundle);

  const bundleName = 'editor.bundle.js';
  injection = `
<!-- SLIDE_EDITOR_START -->
<script src="${bundleName}"></script>
<!-- SLIDE_EDITOR_END -->
`;
}

// Add auto-enable script if requested
// When --open is used, always enable immediately (file:// URLs don't support query params reliably)
if (enable) {
  if (shouldOpen) {
    // When opening directly, auto-enable without URL check
    injection += `
<script>
// Auto-enable editor (opened directly)
(function() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      window.__openclawEditor && window.__openclawEditor.enable();
    });
  } else {
    window.__openclawEditor && window.__openclawEditor.enable();
  }
})();
</script>
`;
  } else {
    // Normal enable with URL check
    injection += `
<script>
// Auto-enable editor when ?edit=1 is in URL
if (new URLSearchParams(location.search).get('edit') === '1') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      window.__openclawEditor && window.__openclawEditor.enable();
    });
  } else {
    window.__openclawEditor && window.__openclawEditor.enable();
  }
}
</script>
`;
  }
}

// Insert before </body> or </html>
const insertPoint = html.lastIndexOf('</body>');
if (insertPoint > -1) {
  html = html.slice(0, insertPoint) + injection + '\n' + html.slice(insertPoint);
} else {
  const htmlEnd = html.lastIndexOf('</html>');
  if (htmlEnd > -1) {
    html = html.slice(0, htmlEnd) + injection + '\n' + html.slice(htmlEnd);
  } else {
    // Just append at the end
    html += injection;
  }
}

// Write output
writeFileSync(outputFile, html);

console.log(`✓ Editor injected into: ${outputFile}`);
if (inline) {
  console.log('  Bundle: inline (embedded)');
} else if (link) {
  console.log('  Bundle: external link (editor.bundle.js)');
}
if (enable) {
  console.log('  Auto-enable: yes (?edit=1)');
}

// Open in browser if requested
if (shouldOpen) {
  const fileUrl = `file://${outputFile}?edit=1`;
  console.log(`\nOpening: ${fileUrl}`);

  try {
    // macOS
    execSync(`open "${fileUrl}"`, { stdio: 'ignore' });
  } catch {
    // Try xdg-open for Linux
    try {
      execSync(`xdg-open "${fileUrl}"`, { stdio: 'ignore' });
    } catch {
      // Try start for Windows
      try {
        execSync(`start "" "${fileUrl}"`, { stdio: 'ignore' });
      } catch {
        console.log(`Please open manually: ${fileUrl}`);
      }
    }
  }
}
