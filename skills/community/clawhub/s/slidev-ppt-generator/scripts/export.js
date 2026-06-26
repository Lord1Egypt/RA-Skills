#!/usr/bin/env node

/**
 * Slidev Export Wrapper
 * Simplifies PDF/PPTX/HTML export workflow
 *
 * Usage:
 * node export.js --format pdf --output presentation.pdf
 * node export.js --format pptx --output presentation.pptx
 * node export.js --format html --output dist/
 */

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function parseArgs(args) {
  const options = {
    format: 'pdf',
    output: null,
    withClicks: false,
    range: null
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--format':
      case '-f':
        options.format = args[++i];
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--with-clicks':
        options.withClicks = true;
        break;
      case '--range':
        options.range = args[++i];
        break;
    }
  }

  return options;
}

function resolveSlidevCommand() {
  const localBin = path.join(process.cwd(), 'node_modules', '.bin', 'slidev');
  return fs.existsSync(localBin) ? [localBin] : null;
}

function ensureProjectDep(name) {
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  const installed = {
    ...(pkg.dependencies || {}),
    ...(pkg.devDependencies || {}),
  };

  if (installed[name]) {
    return;
  }

  console.log(`Missing dependency ${name}, installing into project...`);
  execFileSync('npm', ['i', '-D', name], { stdio: 'inherit' });
}

function checkPlaywright() {
  try {
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf-8'));
    return pkg.devDependencies && pkg.devDependencies['playwright-chromium'];
  } catch (e) {
    return false;
  }
}

function exportSlides(slidevCmd, format, output, options) {
  const cmd = [...slidevCmd, 'export'];

  cmd.push(`--format`, format);

  if (output) {
    cmd.push(`--output`, output);
  }

  if (options.withClicks) {
    cmd.push('--with-clicks');
  }

  if (options.range) {
    cmd.push(`--range`, options.range);
  }

  console.log(`Running: ${cmd.join(' ')}`);

  try {
    execFileSync(cmd[0], cmd.slice(1), { stdio: 'inherit' });
    return true;
  } catch (e) {
    console.error('Export failed');
    return false;
  }
}

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Slidev Export Tool

Usage:
  node export.js [options]

Options:
  -f, --format <format>   Export format: pdf|pptx|png|md (default: pdf)
  -o, --output <file>     Output file path
  --with-clicks           Include animation steps
  --range <range>         Export specific pages (e.g. 1-5,8,10-12)
  -h, --help              Show help

Examples:
  node export.js -f pdf -o presentation.pdf
  node export.js -f pptx -o presentation.pptx
  node export.js -f png --with-clicks
  node export.js -f pdf --range 1-5,8,10
`);
    process.exit(0);
  }

  const options = parseArgs(args);

  console.log('Slidev Export Tool');
  console.log('==================');
  console.log('');

  const slidevCmd = resolveSlidevCommand();
  if (!slidevCmd) {
    console.log('Local Slidev not found, initializing project...');
    execFileSync('node', [
      path.join(__dirname, 'init-project.js'),
      '--dir',
      process.cwd(),
      ...( ['pdf', 'pptx', 'png'].includes(options.format) ? ['--with-export-deps'] : [] ),
    ], { stdio: 'inherit' });
  }
  const resolvedSlidevCmd = resolveSlidevCommand();
  if (!resolvedSlidevCmd) {
    console.error('Slidev project initialization failed');
    process.exit(1);
  }

  if (['pdf', 'pptx', 'png'].includes(options.format)) {
    if (!checkPlaywright()) {
      ensureProjectDep('playwright-chromium');
    }
  }

  let outputFile = options.output;
  if (!outputFile) {
    const ext = {
      pdf: 'pdf',
      pptx: 'pptx',
      png: 'png',
      md: 'md',
      html: 'html'
    }[options.format] || options.format;

    outputFile = `slides-export.${ext}`;
  }

  console.log(`Format: ${options.format}`);
  console.log(`Output: ${outputFile}`);
  console.log('');

  const success = exportSlides(resolvedSlidevCmd, options.format, outputFile, options);

  if (success) {
    console.log('');
    console.log(`Export complete: ${outputFile}`);
    console.log('');

    try {
      const stats = fs.statSync(outputFile);
      const size = (stats.size / 1024 / 1024).toFixed(2);
      console.log(`File size: ${size} MB`);
    } catch (e) {
      // ignore
    }
  } else {
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
