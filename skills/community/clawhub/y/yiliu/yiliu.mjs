#!/usr/bin/env node
import { handle } from './dist/index.js';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const message = process.argv.slice(2).join(' ');

async function main() {
  if (!message) {
    console.log('Usage: yiliu <message>');
    process.exit(0);
  }
  
  const result = await handle({ message });
  console.log(result.message);
}

main().catch(console.error);
