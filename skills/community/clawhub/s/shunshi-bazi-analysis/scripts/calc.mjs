#!/usr/bin/env node
/**
 * Standalone Bazi chart calculator.
 * Usage: node calc.mjs <year> <month> <day> <hour> <minute> <gender> [city] [longitude] [latitude] [standardMeridian]
 *
 * Example:
 *   node calc.mjs 1993 8 18 14 30 1 广州
 *   node calc.mjs 1993 8 18 14 30 1 "" 113.26 23.13
 */

import { getBaziChart } from 'shunshi-bazi-core';

const args = process.argv.slice(2);
if (args.length < 6) {
  console.error('Usage: node calc.mjs <year> <month> <day> <hour> <minute> <gender> [city] [lon] [lat] [stdMeridian]');
  process.exit(1);
}

const input = {
  year: parseInt(args[0]),
  month: parseInt(args[1]),
  day: parseInt(args[2]),
  hour: parseInt(args[3]),
  minute: parseInt(args[4]) || 0,
  gender: parseInt(args[5]),
};

if (args[6] && args[6] !== '""' && args[6] !== "''") input.city = args[6];
if (args[7]) input.longitude = parseFloat(args[7]);
if (args[8]) input.latitude = parseFloat(args[8]);
if (args[9]) input.standardMeridian = parseFloat(args[9]);

const result = getBaziChart(input);
console.log(JSON.stringify(result, null, 2));
