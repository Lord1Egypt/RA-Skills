#!/usr/bin/env node
import { Command } from 'commander';
import { registerCompactCommands } from '../dist/cli/register.js';

const program = new Command();
program.name('openclaw-session-compact');

registerCompactCommands(program);
program.parse(process.argv);
