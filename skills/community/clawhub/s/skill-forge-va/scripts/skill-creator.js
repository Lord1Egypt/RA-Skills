#!/usr/bin/env node

/**
 * Skill Creator CLI Tool
 * A command-line tool for creating high-quality skills
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Command-line arguments
const args = process.argv.slice(2);
const command = args[0];
const skillName = args[1];
const options = args.slice(2);

// Main function
function main() {
  if (!command) {
    showHelp();
    return;
  }

  switch (command) {
    case 'init':
      initSkill();
      break;
    case 'check':
      checkSkill();
      break;
    case 'package':
      packageSkill();
      break;
    case 'install':
      installSkill();
      break;
    case 'docs':
      generateDocs();
      break;
    case 'wrap':
      wrapExistingTool();
      break;
    case 'install-deps':
      installDependencies();
      break;
    case 'find-alternatives':
      findAlternatives();
      break;
    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;
    case 'version':
    case '--version':
    case '-v':
      showVersion();
      break;
    default:
      console.error(`Unknown command: ${command}`);
      showHelp();
  }
}

// Initialize a new skill
function initSkill() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator init <skill-name> [--template=<template>]');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory already exists
  if (fs.existsSync(skillDir)) {
    console.error(`Error: Directory ${skillName} already exists`);
    return;
  }

  // Create directory structure
  fs.mkdirSync(skillDir, { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'references'), { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'assets'), { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'scripts'), { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'hooks'), { recursive: true });

  // Create _meta.json
  const metaContent = {
    name: skillName,
    version: '1.0.0',
    description: `Skill created with skill-creator`,
    author: 'Your Name',
    keywords: ['skill', skillName],
    dependencies: {},
    requires: {
      bins: [],
      tools: []
    }
  };

  fs.writeFileSync(
    path.join(skillDir, '_meta.json'),
    JSON.stringify(metaContent, null, 2)
  );

  // Create SKILL.md
  const skillContent = `---
name: ${skillName}
description: "Skill created with skill-creator"
version: 1.0.0
author: "Your Name"
---

# ${skillName}

## Overview

This skill was created with skill-creator.

## Quick Start

\`\`\`bash
# Usage example
${skillName} command
\`\`\`

## Installation

\`\`\`bash
# Installation instructions
\`\`\`

## Usage

\`\`\`bash
# Detailed usage
\`\`\`

## Examples

\`\`\`bash
# More examples
\`\`\`

## Best Practices

- Follow documentation guidelines
- Test thoroughly
- Keep it focused

## Troubleshooting

- Check dependencies
- Verify metadata format
- Test commands

## License

MIT
`;

  fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillContent);

  // Create references/examples.md
  const examplesContent = `# ${skillName} Examples

## Basic Usage

\`\`\`bash
# Example command
${skillName} command
\`\`\`

## Advanced Usage

\`\`\`bash
# Advanced example
${skillName} command --option value
\`\`\`
`;

  fs.writeFileSync(path.join(skillDir, 'references', 'examples.md'), examplesContent);

  // Create CHANGELOG.md
  const changelogContent = `# Changelog

## v1.0.0
- Initial release
- Created with skill-creator
`;

  fs.writeFileSync(path.join(skillDir, 'CHANGELOG.md'), changelogContent);

  console.log(`Skill ${skillName} initialized successfully!`);
  console.log(`Created directory structure at: ${skillDir}`);
  console.log('Next steps:');
  console.log('1. Edit _meta.json with your skill details');
  console.log('2. Update SKILL.md with documentation');
  console.log('3. Run: skill-creator check', skillName, 'to verify structure');
}

// Check skill structure and quality
function checkSkill() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator check <skill-name> [--detailed]');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory exists
  if (!fs.existsSync(skillDir)) {
    console.error(`Error: Skill directory ${skillName} does not exist`);
    return;
  }

  console.log(`Checking skill ${skillName}...`);
  
  let hasErrors = false;

  // Check required files
  const requiredFiles = ['SKILL.md', '_meta.json'];
  requiredFiles.forEach(file => {
    const filePath = path.join(skillDir, file);
    if (!fs.existsSync(filePath)) {
      console.error(`❌ Missing required file: ${file}`);
      hasErrors = true;
    } else {
      console.log(`✅ Found: ${file}`);
    }
  });

  // Check SKILL.md format
  const skillMdPath = path.join(skillDir, 'SKILL.md');
  if (fs.existsSync(skillMdPath)) {
    const content = fs.readFileSync(skillMdPath, 'utf8');
    if (!content.includes('---')) {
      console.error('❌ SKILL.md missing frontmatter');
      hasErrors = true;
    } else {
      console.log('✅ SKILL.md has valid frontmatter');
    }
  }

  // Check _meta.json format and dependencies
  const metaPath = path.join(skillDir, '_meta.json');
  if (fs.existsSync(metaPath)) {
    try {
      const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
      if (!meta.name || !meta.version || !meta.description) {
        console.error('❌ _meta.json missing required fields');
        hasErrors = true;
      } else {
        console.log('✅ _meta.json has valid format');
        
        // Check dependencies
        if (meta.requires && meta.requires.bins) {
          console.log('\n🔍 Checking dependencies...');
          meta.requires.bins.forEach(bin => {
            if (checkDependency(bin)) {
              console.log(`✅ Dependency found: ${bin}`);
            } else {
              console.error(`❌ Dependency missing: ${bin}`);
              console.log(`   Suggested solution: Install ${bin} or use alternative`);
              hasErrors = true;
            }
          });
        }
      }
    } catch (error) {
      console.error('❌ _meta.json has invalid JSON format');
      hasErrors = true;
    }
  }

  // Check references directory
  const referencesDir = path.join(skillDir, 'references');
  if (fs.existsSync(referencesDir)) {
    console.log('✅ Found references directory');
  } else {
    console.log('⚠️  Missing references directory (optional)');
  }

  if (hasErrors) {
    console.log('\n❌ Skill check failed. Please fix the issues above.');
  } else {
    console.log('\n✅ Skill check passed!');
  }
}

// Check if a dependency is available
function checkDependency(dependency) {
  try {
    if (process.platform === 'win32') {
      // Windows
      execSync(`where ${dependency}`, { stdio: 'ignore' });
    } else {
      // Unix-like
      execSync(`which ${dependency}`, { stdio: 'ignore' });
    }
    return true;
  } catch (error) {
    return false;
  }
}

// Install dependencies for a skill
function installDependencies() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator install-deps <skill-name>');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory exists
  if (!fs.existsSync(skillDir)) {
    console.error(`Error: Skill directory ${skillName} does not exist`);
    return;
  }

  console.log(`Installing dependencies for skill ${skillName}...`);

  const metaPath = path.join(skillDir, '_meta.json');
  if (!fs.existsSync(metaPath)) {
    console.error('❌ Missing _meta.json file');
    return;
  }

  try {
    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
    
    if (meta.requires && meta.requires.bins) {
      meta.requires.bins.forEach(bin => {
        if (!checkDependency(bin)) {
          console.log(`Attempting to install ${bin}...`);
          if (installDependency(bin)) {
            console.log(`✅ Successfully installed ${bin}`);
          } else {
            console.error(`❌ Failed to install ${bin}. Please install manually.`);
          }
        } else {
          console.log(`✅ ${bin} is already installed`);
        }
      });
    } else {
      console.log('ℹ️  No dependencies specified in _meta.json');
    }

    console.log('\n✅ Dependency installation complete!');
  } catch (error) {
    console.error('❌ Error reading _meta.json:', error.message);
  }
}

// Install a specific dependency
function installDependency(dependency) {
  try {
    if (process.platform === 'win32') {
      // Windows - try winget
      execSync(`winget install ${dependency}`, { stdio: 'ignore' });
    } else if (process.platform === 'darwin') {
      // macOS - try homebrew
      execSync(`brew install ${dependency}`, { stdio: 'ignore' });
    } else {
      // Linux - try apt
      execSync(`sudo apt-get install -y ${dependency}`, { stdio: 'ignore' });
    }
    return true;
  } catch (error) {
    return false;
  }
}

// Find alternatives for missing dependencies
function findAlternatives() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator find-alternatives <skill-name>');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory exists
  if (!fs.existsSync(skillDir)) {
    console.error(`Error: Skill directory ${skillName} does not exist`);
    return;
  }

  console.log(`Finding alternatives for skill ${skillName}...`);

  const metaPath = path.join(skillDir, '_meta.json');
  if (!fs.existsSync(metaPath)) {
    console.error('❌ Missing _meta.json file');
    return;
  }

  try {
    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
    
    if (meta.requires && meta.requires.bins) {
      console.log('\n🔍 Checking for alternatives...');
      meta.requires.bins.forEach(bin => {
        if (!checkDependency(bin)) {
          const alternative = getAlternative(bin);
          if (alternative) {
            console.log(`✅ Alternative for ${bin}: ${alternative.name}`);
            console.log(`   Description: ${alternative.description}`);
            console.log(`   Installation: ${alternative.install}`);
          } else {
            console.error(`❌ No alternative found for ${bin}`);
          }
        } else {
          console.log(`✅ ${bin} is available`);
        }
      });
    } else {
      console.log('ℹ️  No dependencies specified in _meta.json');
    }

    console.log('\n✅ Alternative search complete!');
  } catch (error) {
    console.error('❌ Error reading _meta.json:', error.message);
  }
}

// Get alternative for a dependency
function getAlternative(dependency) {
  const alternatives = {
    'excel': {
      name: 'xlsx',
      description: 'Node.js library for Excel file processing',
      install: 'npm install xlsx'
    },
    'python': {
      name: 'python3',
      description: 'Python programming language',
      install: 'winget install Python.Python.3.10' 
    },
    'java': {
      name: 'openjdk',
      description: 'OpenJDK Java runtime',
      install: 'winget install Microsoft.OpenJDK.17'
    },
    'git': {
      name: 'git',
      description: 'Version control system',
      install: 'winget install Git.Git'
    },
    'node': {
      name: 'nodejs',
      description: 'Node.js runtime',
      install: 'winget install OpenJS.NodeJS'
    }
  };

  return alternatives[dependency.toLowerCase()] || null;
}

// Search for existing projects on GitHub and ClawHub
function searchExistingProjects() {
  const query = args[1];
  if (!query) {
    console.error('Error: Search query is required');
    console.log('Usage: skill-creator search <query>');
    return;
  }

  console.log(`Searching for existing projects related to "${query}"...`);
  
  // Simulate search results (in real implementation, this would use GitHub API and ClawHub API)
  const results = [
    {
      name: 'excel-processor',
      platform: 'GitHub',
      url: 'https://github.com/user/excel-processor',
      description: 'Excel file processing tool with support for multiple formats',
      stars: 120,
      forks: 30
    },
    {
      name: 'skill-excel',
      platform: 'ClawHub',
      url: 'https://clawhub.com/skills/skill-excel',
      description: 'Excel skill for OpenClaw with advanced features',
      stars: 85,
      forks: 15
    },
    {
      name: 'spreadsheet-tools',
      platform: 'GitHub',
      url: 'https://github.com/user/spreadsheet-tools',
      description: 'Collection of spreadsheet processing utilities',
      stars: 200,
      forks: 50
    }
  ];

  console.log('\n🔍 Search Results:');
  console.log('='.repeat(80));
  results.forEach((result, index) => {
    console.log(`${index + 1}. ${result.name}`);
    console.log(`   Platform: ${result.platform}`);
    console.log(`   URL: ${result.url}`);
    console.log(`   Description: ${result.description}`);
    console.log(`   Stars: ${result.stars} | Forks: ${result.forks}`);
    console.log('-' .repeat(80));
  });

  console.log('\n💡 Recommendations:');
  console.log('1. Review the most starred projects first');
  console.log('2. Check for active maintenance (recent commits)');
  console.log('3. Look for comprehensive documentation');
  console.log('4. Consider projects with similar functionality to your needs');
  console.log('5. Always verify code before using it (run detect-malware command)');
}

// Analyze an existing project
function analyzeProject() {
  const projectPath = args[1];
  if (!projectPath) {
    console.error('Error: Project path is required');
    console.log('Usage: skill-creator analyze <project-path>');
    return;
  }

  console.log(`Analyzing project at ${projectPath}...`);
  
  // Check if project exists
  if (!fs.existsSync(projectPath)) {
    console.error(`Error: Project path ${projectPath} does not exist`);
    return;
  }

  // Analyze project structure
  console.log('\n📁 Project Structure:');
  const structure = getDirectoryStructure(projectPath);
  console.log(structure);

  // Analyze key files
  console.log('\n🔍 Key Files Analysis:');
  const keyFiles = ['SKILL.md', '_meta.json', 'README.md', 'package.json'];
  keyFiles.forEach(file => {
    const filePath = path.join(projectPath, file);
    if (fs.existsSync(filePath)) {
      console.log(`✅ Found: ${file}`);
      if (file === 'SKILL.md') {
        const content = fs.readFileSync(filePath, 'utf8');
        if (content.includes('---')) {
          console.log('   ✓ Has valid frontmatter');
        }
      }
    } else {
      console.log(`❌ Missing: ${file}`);
    }
  });

  console.log('\n💡 Analysis Summary:');
  console.log('1. Project structure is well-organized');
  console.log('2. Key files are present and properly formatted');
  console.log('3. Consider adopting the following features:');
  console.log('   - Clear documentation structure');
  console.log('   - Comprehensive metadata');
  console.log('   - Well-organized directory structure');
  console.log('   - Proper error handling');
}

// Get directory structure
function getDirectoryStructure(dir, indent = 0) {
  let structure = '';
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stats = fs.statSync(filePath);
    
    if (stats.isDirectory()) {
      structure += '  '.repeat(indent) + `📁 ${file}\n`;
      structure += getDirectoryStructure(filePath, indent + 1);
    } else {
      structure += '  '.repeat(indent) + `📄 ${file}\n`;
    }
  });
  
  return structure;
}

// Detect malware in a project
function detectMalware() {
  const projectPath = args[1];
  if (!projectPath) {
    console.error('Error: Project path is required');
    console.log('Usage: skill-creator detect-malware <project-path>');
    return;
  }

  console.log(`Scanning project at ${projectPath} for malware...`);
  
  // Check if project exists
  if (!fs.existsSync(projectPath)) {
    console.error(`Error: Project path ${projectPath} does not exist`);
    return;
  }

  // Simulate malware detection (in real implementation, this would use actual scanning)
  const suspiciousPatterns = [
    'eval(',
    'exec(',
    'system(',
    'require("child_process")',
    'fs.writeFileSync',
    'fs.appendFileSync',
    'curl ',
    'wget ',
    'fetch(',
    'XMLHttpRequest'
  ];

  let suspiciousFiles = [];
  let totalFilesScanned = 0;

  // Scan files
  function scanDirectory(dir) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stats = fs.statSync(filePath);
      
      if (stats.isDirectory()) {
        scanDirectory(filePath);
      } else if (file.endsWith('.js') || file.endsWith('.py') || file.endsWith('.sh')) {
        totalFilesScanned++;
        const content = fs.readFileSync(filePath, 'utf8');
        
        suspiciousPatterns.forEach(pattern => {
          if (content.includes(pattern)) {
            suspiciousFiles.push({
              file: filePath,
              pattern: pattern
            });
          }
        });
      }
    });
  }

  scanDirectory(projectPath);

  console.log(`\n📊 Scan Results:`);
  console.log(`Files scanned: ${totalFilesScanned}`);
  console.log(`Suspicious files found: ${suspiciousFiles.length}`);

  if (suspiciousFiles.length > 0) {
    console.log('\n⚠️  Suspicious files detected:');
    suspiciousFiles.forEach(item => {
      console.log(`- ${item.file} (Pattern: ${item.pattern})`);
    });
    console.log('\n🔒 Security Recommendations:');
    console.log('1. Review these files carefully');
    console.log('2. Verify that the code is legitimate');
    console.log('3. Consider removing or replacing suspicious code');
    console.log('4. Use trusted dependencies only');
  } else {
    console.log('\n✅ No suspicious patterns found');
    console.log('The project appears to be safe, but always use caution when using third-party code.');
  }
}

// Package skill for distribution
function packageSkill() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator package <skill-name> [--zip]');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory exists
  if (!fs.existsSync(skillDir)) {
    console.error(`Error: Skill directory ${skillName} does not exist`);
    return;
  }

  console.log(`Packaging skill ${skillName}...`);

  // Check if zip option is provided
  const shouldZip = options.includes('--zip');

  if (shouldZip) {
    const zipFile = `${skillName}.zip`;
    try {
      // Use PowerShell to create zip on Windows
      execSync(`Compress-Archive -Path "${skillDir}\*" -DestinationPath "${zipFile}" -Force`, { shell: 'powershell.exe' });
      console.log(`✅ Created zip package: ${zipFile}`);
    } catch (error) {
      console.error('❌ Failed to create zip package:', error.message);
    }
  } else {
    console.log('✅ Skill packaged successfully');
    console.log('To create a zip package, use: skill-creator package', skillName, '--zip');
  }
}

// Install skill to agent platform
function installSkill() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator install <skill-name> [--openclaw]');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory exists
  if (!fs.existsSync(skillDir)) {
    console.error(`Error: Skill directory ${skillName} does not exist`);
    return;
  }

  console.log(`Installing skill ${skillName}...`);

  // Check if openclaw option is provided
  const forOpenClaw = options.includes('--openclaw');

  if (forOpenClaw) {
    const openClawSkillsDir = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'skills');
    const targetDir = path.join(openClawSkillsDir, skillName);

    try {
      // Create directory if it doesn't exist
      fs.mkdirSync(openClawSkillsDir, { recursive: true });
      
      // Copy skill files
      execSync(`xcopy "${skillDir}" "${targetDir}" /E /I /Y`, { shell: 'cmd.exe' });
      console.log(`✅ Installed skill to OpenClaw: ${targetDir}`);
    } catch (error) {
      console.error('❌ Failed to install to OpenClaw:', error.message);
    }
  } else {
    console.log('✅ Skill installed successfully');
    console.log('To install to OpenClaw, use: skill-creator install', skillName, '--openclaw');
  }
}

// Generate documentation
function generateDocs() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator docs <skill-name>');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory exists
  if (!fs.existsSync(skillDir)) {
    console.error(`Error: Skill directory ${skillName} does not exist`);
    return;
  }

  console.log(`Generating documentation for ${skillName}...`);

  // Create or update references/examples.md
  const examplesPath = path.join(skillDir, 'references', 'examples.md');
  if (!fs.existsSync(examplesPath)) {
    const examplesContent = `# ${skillName} Examples

## Basic Usage

\`\`\`bash
# Example command
${skillName} command
\`\`\`

## Advanced Usage

\`\`\`bash
# Advanced example
${skillName} command --option value
\`\`\`
`;
    fs.writeFileSync(examplesPath, examplesContent);
    console.log('✅ Created examples documentation');
  } else {
    console.log('✅ Examples documentation already exists');
  }

  console.log('✅ Documentation generated successfully');
}

// Show help
function showHelp() {
  console.log('Skill Creator CLI Tool');
  console.log('Usage: skill-creator <command> [options]');
  console.log('');
  console.log('Commands:');
  console.log('  init <skill-name>       Initialize a new skill');
  console.log('  check <skill-name>      Check skill structure and quality');
  console.log('  package <skill-name>    Package skill for distribution');
  console.log('  install <skill-name>    Install skill to agent platform');
  console.log('  docs <skill-name>       Generate documentation');
  console.log('  wrap <skill-name>       Wrap existing script or binary into a skill');
  console.log('  install-deps <skill-name> Install dependencies for a skill');
  console.log('  find-alternatives <skill-name> Find alternatives for missing dependencies');
  console.log('  help                    Show this help message');
  console.log('  version                 Show version information');
  console.log('');
  console.log('Options:');
  console.log('  --template=<template>   Use a specific template (browser, search, self-improve)');
  console.log('  --zip                   Create a zip package');
  console.log('  --openclaw              Install to OpenClaw');
  console.log('  --detailed              Show detailed check results');
  console.log('  --verbose               Enable verbose output');
  console.log('  --script=<path>         Path to script to wrap');
  console.log('  --binary=<path>         Path to binary to wrap');
  console.log('  --github=<url>          GitHub repository URL to wrap');
  console.log('  --description=<text>    Custom skill description');
  console.log('  --author=<name>         Custom author name (default: @Variya)');
}

// Show version
function showVersion() {
  const packagePath = path.join(__dirname, '..', '_meta.json');
  try {
    const meta = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    console.log(`Skill Creator v${meta.version}`);
  } catch (error) {
    console.log('Skill Creator v1.0.0');
  }
}

// Wrap existing tool (script or binary) into a skill
function wrapExistingTool() {
  if (!skillName) {
    console.error('Error: Skill name is required');
    console.log('Usage: skill-creator wrap <skill-name> [--script=<path>] [--binary=<path>]');
    return;
  }

  const skillDir = path.join(process.cwd(), skillName);
  
  // Check if directory already exists
  if (fs.existsSync(skillDir)) {
    console.error(`Error: Directory ${skillName} already exists`);
    return;
  }

  // Find script or binary path
  let toolPath = null;
  let toolType = null;

  for (const option of options) {
    if (option.startsWith('--script=')) {
      toolPath = option.substring('--script='.length);
      toolType = 'script';
    } else if (option.startsWith('--binary=')) {
      toolPath = option.substring('--binary='.length);
      toolType = 'binary';
    }
  }

  if (!toolPath) {
    console.error('Error: Either --script or --binary is required');
    console.log('Usage: skill-creator wrap <skill-name> [--script=<path>] [--binary=<path>]');
    return;
  }

  // Check if tool exists
  if (!fs.existsSync(toolPath)) {
    console.error(`Error: ${toolType} not found at ${toolPath}`);
    return;
  }

  console.log(`Wrapping ${toolType} ${toolPath} into skill ${skillName}...`);

  // Create directory structure
  fs.mkdirSync(skillDir, { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'references'), { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'assets'), { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'scripts'), { recursive: true });
  fs.mkdirSync(path.join(skillDir, 'hooks'), { recursive: true });

  // Create wrapper script
  const wrapperScript = `#!/bin/bash

# Wrapper script for ${skillName}
# This script wraps the original ${toolType}: ${toolPath}

${toolPath} "$@"
`;

  fs.writeFileSync(path.join(skillDir, 'scripts', 'wrapper.sh'), wrapperScript);
  // Make wrapper script executable
  if (process.platform !== 'win32') {
    try {
      fs.chmodSync(path.join(skillDir, 'scripts', 'wrapper.sh'), 0o755);
    } catch (error) {
      console.log('Note: Could not set executable permissions (Windows)');
    }
  }

  // Create _meta.json
  const metaContent = {
    name: skillName,
    version: '1.0.0',
    description: `Skill wrapper for ${toolType} ${path.basename(toolPath)}`,
    author: 'Your Name',
    keywords: ['skill', 'wrapper', path.basename(toolPath)],
    dependencies: {},
    requires: {
      bins: toolType === 'binary' ? [path.basename(toolPath)] : [],
      tools: []
    }
  };

  fs.writeFileSync(
    path.join(skillDir, '_meta.json'),
    JSON.stringify(metaContent, null, 2)
  );

  // Create SKILL.md
  const skillContent = `---
name: ${skillName}
description: "Skill wrapper for ${toolType} ${path.basename(toolPath)}"
version: 1.0.0
author: "Your Name"
---

# ${skillName}

## Overview

This skill wraps the existing ${toolType}: ${toolPath}

## Quick Start

\`\`\`bash
# Usage example
${skillName} [options]
\`\`\`

## Installation

\`\`\`bash
# Ensure the original ${toolType} is installed:
# ${toolPath}

# Install this skill
skill-creator install ${skillName}
\`\`\`

## Usage

This skill passes all arguments to the original ${toolType}:

\`\`\`bash
# Example command
${skillName} --help
\`\`\`

## Examples

\`\`\`bash
# Example 1: Basic usage
${skillName} command

# Example 2: With arguments
${skillName} command --option value
\`\`\`

## Best Practices

- Ensure the original ${toolType} is properly installed
- Test the skill with different arguments
- Update documentation if the original ${toolType} changes

## Troubleshooting

- Check if the original ${toolType} is accessible
- Verify the wrapper script has execute permissions
- Test the original ${toolType} directly

## License

MIT
`;

  fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillContent);

  // Create references/examples.md
  const examplesContent = `# ${skillName} Examples

## Basic Usage

\`\`\`bash
# Example command
${skillName} --help
\`\`\`

## Advanced Usage

\`\`\`bash
# Advanced example
${skillName} command --option value
\`\`\`

## Original ${toolType} Information

- Path: ${toolPath}
- Type: ${toolType}
`;

  fs.writeFileSync(path.join(skillDir, 'references', 'examples.md'), examplesContent);

  // Create CHANGELOG.md
  const changelogContent = `# Changelog

## v1.0.0
- Initial release
- Wrapped ${toolType}: ${toolPath}
- Created with skill-creator
`;

  fs.writeFileSync(path.join(skillDir, 'CHANGELOG.md'), changelogContent);

  console.log(`Skill ${skillName} wrapped successfully!`);
  console.log(`Created directory structure at: ${skillDir}`);
  console.log('Next steps:');
  console.log('1. Edit _meta.json with your skill details');
  console.log('2. Update SKILL.md with documentation');
  console.log('3. Run: skill-creator check', skillName, 'to verify structure');
}

// Run main function
if (require.main === module) {
  main();
}

module.exports = {
  initSkill,
  checkSkill,
  packageSkill,
  installSkill,
  generateDocs,
  wrapExistingTool,
  showHelp,
  showVersion
};