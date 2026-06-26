#!/usr/bin/env node
/**
 * OpenClaw Pet - Terminal Version
 * Pure CLI, no domain needed
 */

const chalk = require('chalk');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(require('os').homedir(), '.openclaw-pet.json');

// Pixel Art for Terminal
const PETS = {
  0: {
    name: 'Egg',
    art: [
      chalk.yellow('      ████      '),
      chalk.yellow('    ██░░░░██    '),
      chalk.yellow('   ██░░░░░░██   '),
      chalk.yellow('   ██░░🥚░░██   '),
      chalk.yellow('    ██░░░░██    '),
      chalk.yellow('      ████      '),
    ]
  },
  1: {
    name: 'Baby Bot',
    art: [
      chalk.cyan('     ██████     '),
      chalk.cyan('    █░👀░█    '),
      chalk.cyan('    █░░😊░░█    '),
      chalk.cyan('     ██████     '),
      chalk.cyan('      ▼▼▼▼      '),
    ]
  },
  2: {
    name: 'Teen Coder',
    art: [
      chalk.blue('    ████████    '),
      chalk.blue('   █░🤓🤓░█   '),
      chalk.blue('   █░👕👕░█   '),
      chalk.blue('    ████████    '),
      chalk.blue('     💻💻      '),
    ]
  },
  3: {
    name: 'Senior Dev',
    art: [
      chalk.green('   ██████████   '),
      chalk.green('  █░😎░░😎░█  '),
      chalk.green('  █░🧔░░🧔░█  '),
      chalk.green('   ██████████   '),
      chalk.green('    ☕☕☕☕    '),
    ]
  },
  4: {
    name: '10x Legend',
    art: [
      chalk.magenta('  🔥████████🔥  '),
      chalk.magenta(' 🔥█░✨👑✨░█🔥 '),
      chalk.magenta(' 🔥█░🦄🦄░█🔥 '),
      chalk.magenta('  🔥████████🔥  '),
      chalk.magenta('   👑👑👑👑👑   '),
    ]
  }
};

class TerminalPet {
  constructor() {
    this.load();
  }

  load() {
    try {
      const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
      this.pet = data;
    } catch {
      this.pet = {
        stage: 0,
        hunger: 50,
        happy: 50,
        energy: 100,
        xp: 0,
        level: 1,
        lastFed: Date.now(),
        name: 'Clawdy'
      };
      this.save();
    }
  }

  save() {
    fs.writeFileSync(DATA_FILE, JSON.stringify(this.pet, null, 2));
  }

  clear() {
    console.clear();
  }

  render() {
    this.clear();
    const pet = PETS[this.pet.stage];
    
    console.log('\n' + chalk.cyan('╔══════════════════════════════════════════╗'));
    console.log(chalk.cyan('║') + chalk.yellow('          🐣 AGENT PET v1.0              ') + chalk.cyan('║'));
    console.log(chalk.cyan('╠══════════════════════════════════════════╣'));
    
    // Pet art
    pet.art.forEach(line => {
      console.log(chalk.cyan('║') + '  ' + line + '  ' + chalk.cyan('║'));
    });
    
    // Info
    console.log(chalk.cyan('╠══════════════════════════════════════════╣'));
    console.log(chalk.cyan('║') + `  ${chalk.yellow(this.pet.name)} - ${chalk.cyan(pet.name)}` + ' '.repeat(26 - this.pet.name.length - pet.name.length) + chalk.cyan('║'));
    console.log(chalk.cyan('║') + `  ${chalk.white('Level:')} ${chalk.green(this.pet.level)}  ${chalk.white('XP:')} ${chalk.yellow(this.pet.xp)}/100` + ' '.repeat(18) + chalk.cyan('║'));
    console.log(chalk.cyan('╠══════════════════════════════════════════╣'));
    
    // Stats bars
    this.renderBar('🍕 Hunger', this.pet.hunger, chalk.red);
    this.renderBar('😊 Happy', this.pet.happy, chalk.green);
    this.renderBar('⚡ Energy', this.pet.energy, chalk.blue);
    
    console.log(chalk.cyan('╚══════════════════════════════════════════╝'));
    console.log('\n  ' + chalk.gray('[f]eed  [p]lay  [c]ode  [s]tatus  [q]uit'));
    console.log('');
  }

  renderBar(label, value, color) {
    const filled = Math.floor(value / 5);
    const empty = 20 - filled;
    const bar = color('█'.repeat(filled)) + chalk.gray('░'.repeat(empty));
    const valStr = value.toString().padStart(3);
    console.log(chalk.cyan('║') + `  ${label}: ${bar} ${valStr}%` + ' '.repeat(4) + chalk.cyan('║'));
  }

  feed() {
    this.pet.hunger = Math.min(100, this.pet.hunger + 20);
    this.pet.energy = Math.max(0, this.pet.energy - 5);
    this.pet.lastFed = Date.now();
    this.addXP(5);
    console.log(chalk.green('\n  🍕 Yummy! Your pet enjoyed the food!'));
    this.save();
  }

  play() {
    this.pet.happy = Math.min(100, this.pet.happy + 15);
    this.pet.energy = Math.max(0, this.pet.energy - 10);
    this.pet.hunger = Math.max(0, this.pet.hunger - 10);
    this.addXP(10);
    console.log(chalk.yellow('\n  🎮 Fun! Your pet had a great time!'));
    this.save();
  }

  code() {
    this.pet.xp += 10;
    this.pet.energy = Math.max(0, this.pet.energy - 5);
    this.pet.hunger = Math.max(0, this.pet.hunger - 5);
    this.addXP(15);
    console.log(chalk.cyan('\n  💻 Nice coding! Your pet is proud!'));
    this.save();
  }

  addXP(amount) {
    this.pet.xp += amount;
    if (this.pet.xp >= 100) {
      this.pet.level++;
      this.pet.xp = 0;
      this.checkEvolution();
    }
  }

  checkEvolution() {
    const oldStage = this.pet.stage;
    if (this.pet.level >= 20) this.pet.stage = 4;
    else if (this.pet.level >= 15) this.pet.stage = 3;
    else if (this.pet.level >= 10) this.pet.stage = 2;
    else if (this.pet.level >= 5) this.pet.stage = 1;
    
    if (this.pet.stage > oldStage) {
      const newPet = PETS[this.pet.stage];
      console.log(chalk.magenta('\n  ✨✨✨ EVOLUTION! ✨✨✨'));
      console.log(chalk.yellow(`  ${this.pet.name} evolved into ${newPet.name}!`));
      console.log(chalk.cyan('  🎉 Congratulations! 🎉\n'));
    }
  }

  tick() {
    // Decay over time
    const now = Date.now();
    const hoursSinceFed = (now - this.pet.lastFed) / (1000 * 60 * 60);
    
    if (hoursSinceFed > 1) {
      this.pet.hunger = Math.max(0, this.pet.hunger - 5);
      this.pet.happy = Math.max(0, this.pet.happy - 3);
      this.pet.lastFed = now;
      this.save();
    }
  }

  async start() {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const ask = () => {
      this.tick();
      this.render();
      
      rl.question(chalk.gray('  What would you like to do? '), (answer) => {
        const cmd = answer.trim().toLowerCase();
        
        switch(cmd) {
          case 'f':
          case 'feed':
            this.feed();
            break;
          case 'p':
          case 'play':
            this.play();
            break;
          case 'c':
          case 'code':
            this.code();
            break;
          case 's':
          case 'status':
            break;
          case 'q':
          case 'quit':
          case 'exit':
            console.log(chalk.cyan(`\n  👋 Goodbye! Take care of ${this.pet.name}!\n`));
            rl.close();
            return;
          default:
            console.log(chalk.gray('\n  Unknown command. Try: f, p, c, s, q'));
        }
        
        setTimeout(ask, 1000);
      });
    };

    ask();
  }
}

// Run
const pet = new TerminalPet();
pet.start();
