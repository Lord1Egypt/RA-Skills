const fs = require('fs');

function parseGeoJSON(str) {
  if (!str) return null;
  try {
    return JSON.parse(str);
  } catch {
    throw new Error(`Invalid GeoJSON: ${str.slice(0, 100)}`);
  }
}

function readInput(args) {
  let input = null;
  let input2 = null;

  if (args.file) {
    input = JSON.parse(fs.readFileSync(args.file, 'utf-8'));
  } else if (args.input) {
    input = parseGeoJSON(args.input);
  }

  if (args.file2) {
    input2 = JSON.parse(fs.readFileSync(args.file2, 'utf-8'));
  } else if (args.input2) {
    input2 = parseGeoJSON(args.input2);
  }

  return { input, input2 };
}

function parseNumber(val) {
  if (val === undefined || val === null) return undefined;
  const n = Number(val);
  if (isNaN(n)) throw new Error(`Invalid number: ${val}`);
  return n;
}

function parseJSON(val) {
  if (val === undefined || val === null) return undefined;
  if (typeof val === 'object') return val;
  try {
    return JSON.parse(val);
  } catch {
    throw new Error(`Invalid JSON: ${val}`);
  }
}

function writeOutput(result, outputPath) {
  const str = typeof result === 'object' ? JSON.stringify(result, null, 2) : String(result);
  if (outputPath) {
    fs.writeFileSync(outputPath, str + '\n');
  } else {
    process.stdout.write(str + '\n');
  }
}

module.exports = { parseGeoJSON, readInput, parseNumber, parseJSON, writeOutput };
