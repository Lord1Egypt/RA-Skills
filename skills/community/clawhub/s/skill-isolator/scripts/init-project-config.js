#!/usr/bin/env node

/**
 * Initialize Project Skills Configuration
 * 
 * Creates a .openclaw-skills.json template in the current directory.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG_FILE = '.openclaw-skills.json';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question, defaultValue) {
  return new Promise((resolve) => {
    const prompt = defaultValue !== undefined
      ? `${question} [${defaultValue}]: `
      : `${question}: `;
    
    rl.question(prompt, (answer) => {
      resolve(answer || defaultValue);
    });
  });
}

function askYesNo(question, defaultYes = true) {
  return new Promise((resolve) => {
    const defaultValue = defaultYes ? 'Y' : 'N';
    rl.question(`${question} [${defaultValue}]: `, (answer) => {
      const normalized = (answer || defaultValue).toLowerCase();
      resolve(normalized === 'y' || normalized === 'yes' || (defaultYes && !answer));
    });
  });
}

async function main() {
  console.log('🚀 Project Skills Configuration Wizard\n');
  console.log('This will create a .openclaw-skills.json file in the current directory.\n');
  
  // Check if config already exists
  const configPath = path.join(process.cwd(), CONFIG_FILE);
  if (fs.existsSync(configPath)) {
    console.log('⚠️  Configuration file already exists!');
    const overwrite = await askYesNo('Overwrite?', false);
    if (!overwrite) {
      console.log('👋 Cancelled.');
      rl.close();
      return;
    }
  }
  
  // Project name
  const projectName = await ask(
    'Project name',
    path.basename(process.cwd())
  );
  
  // Skills
  console.log('\n📦 Enter skills to enable (comma-separated):');
  console.log('   Examples: feishu-doc, weather, stock-analyzer');
  const skillsInput = await ask('Skills', 'feishu-doc');
  const skills = skillsInput.split(',').map(s => s.trim()).filter(s => s);
  
  // Exclude global
  const excludeGlobal = await askYesNo('Exclude global skills?', true);
  
  // Sources
  console.log('\n🌐 Skill Sources:');
  const useClawhub = await askYesNo('  - Enable clawhub (registry)?', true);
  const useLocal = await askYesNo('  - Enable local filesystem?', true);
  const useGithub = await askYesNo('  - Enable GitHub (git)?', false);
  
  const sources = [];
  let priority = 1;
  
  if (useClawhub) {
    sources.push({
      name: 'clawhub',
      type: 'registry',
      priority: priority++,
      enabled: true
    });
  }
  
  if (useLocal) {
    sources.push({
      name: 'local',
      type: 'filesystem',
      priority: priority++,
      paths: ['~/.openclaw/skills']
    });
  }
  
  if (useGithub) {
    const repo = await ask('  GitHub repo (user/repo)', '');
    if (repo) {
      sources.push({
        name: 'github',
        type: 'git',
        priority: priority++,
        repos: [repo],
        branch: 'main'
      });
    }
  }
  
  // Cache
  const enableCache = await askYesNo('\n💾 Enable caching?', true);
  const ttlHours = enableCache
    ? parseInt(await ask('  Cache TTL (hours)', '24'), 10)
    : undefined;
  
  // Auto-sync
  const autoSync = await askYesNo('\n🔄 Enable auto-sync on project enter?', true);
  
  // Build config
  const config = {
    name: projectName,
    skills: skills,
    excludeGlobal: excludeGlobal,
    sources: sources.length > 0 ? sources : undefined,
    cache: enableCache ? {
      enabled: true,
      ttlHours: ttlHours
    } : undefined,
    autoSync: autoSync ? {
      onProjectEnter: true,
      onSkillMissing: true
    } : undefined
  };
  
  // Remove undefined fields
  Object.keys(config).forEach(key => {
    if (config[key] === undefined) delete config[key];
  });
  
  // Write config
  const content = JSON.stringify(config, null, 2);
  fs.writeFileSync(configPath, content);
  
  console.log('\n✅ Configuration created!');
  console.log(`   ${configPath}\n`);
  console.log('📄 Content:');
  console.log(content);
  console.log('\n💡 Next steps:');
  console.log('   1. Run "node scripts/sync-project-skills.js" to install skills');
  console.log('   2. Or use "/skills sync" in your chat session\n');
  
  rl.close();
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  rl.close();
  process.exit(1);
});
