#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/models-command.js';

const HELP = `List WeryAI video models and capabilities.

Usage:
  node scripts/models-video.js
  node scripts/models-video.js --mode text_to_video
  node scripts/models-video.js --mode image_to_video
  node scripts/models-video.js --mode multi_image_to_video

Options:
  --mode <mode>  Filter by a specific video mode
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
