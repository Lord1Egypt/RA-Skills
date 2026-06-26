#!/usr/bin/env node

const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

function parseArgs(args) {
  const options = {
    dir: path.join(os.homedir(), 'slidev-ppt'),
    withExportDeps: false,
    installAllOfficialThemes: true,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--dir':
      case '-d':
        options.dir = args[++i];
        break;
      case '--with-export-deps':
        options.withExportDeps = true;
        break;
      case '--no-official-themes':
        options.installAllOfficialThemes = false;
        break;
    }
  }

  return options;
}

function ensureDir(projectDir) {
  fs.mkdirSync(projectDir, { recursive: true });
}

function ensurePackageJson(projectDir) {
  const packageJsonPath = path.join(projectDir, 'package.json');
  if (fs.existsSync(packageJsonPath)) {
    return;
  }

  execFileSync('npm', ['init', '-y'], {
    cwd: projectDir,
    stdio: 'inherit',
  });
}

function readPackageJson(projectDir) {
  const packageJsonPath = path.join(projectDir, 'package.json');
  return JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
}

function ensureDeps(projectDir, packages) {
  const pkg = readPackageJson(projectDir);
  const installed = {
    ...(pkg.dependencies || {}),
    ...(pkg.devDependencies || {}),
  };

  const missing = packages.filter((name) => !installed[name]);
  if (missing.length === 0) {
    return;
  }

  console.log(`Installing dependencies: ${missing.join(', ')}`);
  execFileSync('npm', ['i', '-D', ...missing], {
    cwd: projectDir,
    stdio: 'inherit',
  });
}

function ensureSlides(projectDir) {
  const slidesPath = path.join(projectDir, 'slides.md');
  if (fs.existsSync(slidesPath)) {
    return;
  }

  const starter = `---
theme: apple-basic
title: Slidev Presentation
layout: cover
---

# Slidev Presentation

Choose an official theme based on your task:

- technical -> default
- formal -> apple-basic
- executive -> seriph
- launch -> apple-basic
`;

  fs.writeFileSync(slidesPath, starter, 'utf8');
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const projectDir = path.resolve(options.dir);

  console.log(`Project directory: ${projectDir}`);
  ensureDir(projectDir);
  ensurePackageJson(projectDir);
  const baseDeps = ['@slidev/cli'];
  const officialThemes = [
    '@slidev/theme-default',
    '@slidev/theme-seriph',
    '@slidev/theme-apple-basic',
    '@slidev/theme-bricks',
    '@slidev/theme-shibainu',
  ];

  ensureDeps(
    projectDir,
    options.installAllOfficialThemes ? [...baseDeps, ...officialThemes] : baseDeps,
  );

  if (options.withExportDeps) {
    ensureDeps(projectDir, ['playwright-chromium']);
  }

  ensureSlides(projectDir);

  console.log('Slidev project ready');
  console.log(`   - slides.md: ${path.join(projectDir, 'slides.md')}`);
  if (options.installAllOfficialThemes) {
    console.log(`   - Official themes: ${officialThemes.join(', ')}`);
  }
}

main();
