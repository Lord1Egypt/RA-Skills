#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/models-command.js';

const HELP = `List WeryAI image models and capabilities.

Usage:
  node {baseDir}/scripts/models-image.js
  node {baseDir}/scripts/models-image.js --mode text_to_image
  node {baseDir}/scripts/models-image.js --mode image_to_image

Options:
  --mode <mode>  Filter by text_to_image or image_to_image
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
