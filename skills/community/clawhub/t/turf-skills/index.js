#!/usr/bin/env node
'use strict';

const { readInput, parseNumber, parseJSON, writeOutput } = require('./lib/parser');
const measurement = require('./lib/measurement');
const query = require('./lib/query');
const transformation = require('./lib/transformation');
const helpers = require('./lib/helpers');
const interpolation = require('./lib/interpolation');
const clustering = require('./lib/clustering');

const registry = {};

function register(mod, category) {
  for (const [name, handler] of Object.entries(mod)) {
    registry[name] = { handler, category };
  }
}

register(measurement, 'measurement');
register(query, 'query');
register(transformation, 'transformation');
register(helpers, 'helpers');
register(interpolation, 'interpolation');
register(clustering, 'clustering');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (key.startsWith('--')) {
      const name = key.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        args[name] = true;
      } else {
        args[name] = next;
        i++;
      }
    }
  }
  return args;
}

function main() {
  const raw = parseArgs(process.argv);

  if (raw.help || raw.h) {
    printHelp();
    return;
  }

  if (raw.list) {
    console.log(JSON.stringify(Object.keys(registry), null, 2));
    return;
  }

  const action = raw.action;
  if (!action) {
    console.error('Error: --action is required. Use --list to see available actions.');
    process.exit(1);
  }

  const entry = registry[action];
  if (!entry) {
    console.error(`Error: Unknown action "${action}". Use --list to see available actions.`);
    process.exit(1);
  }

  try {
    const { input, input2 } = readInput(raw);

    const args = {
      input,
      input2,
      units: raw.units,
      radius: parseNumber(raw.radius),
      bbox: parseJSON(raw.bbox),
      cellSide: parseNumber(raw.cellSide),
      coordinates: parseJSON(raw.coordinates),
      properties: parseJSON(raw.properties),
      numberOfClusters: parseNumber(raw.numberOfClusters),
      maxDistance: parseNumber(raw.maxDistance),
      minPoints: parseNumber(raw.minPoints),
      count: parseNumber(raw.count),
      tolerance: parseNumber(raw.tolerance),
      angle: parseNumber(raw.angle),
      factor: parseNumber(raw.factor),
      distance: parseNumber(raw.distance),
      direction: parseNumber(raw.direction),
      bearing_val: parseNumber(raw.bearing),
      breaks: parseJSON(raw.breaks),
      propertyName: raw.propertyName,
      gridType: raw.gridType,
      maxEdge: parseNumber(raw.maxEdge),
      resolution: parseNumber(raw.resolution),
      sharpness: parseNumber(raw.sharpness),
    };

    const result = entry.handler(args);
    writeOutput(result, raw.output);
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

function printHelp() {
  console.log(`turf-skills - Claude Code skill for Turf.js spatial analysis

Usage:
  turf-skills --action <name> [options]

Options:
  --action <name>       Turf function to execute (required)
  --input <geojson>     First GeoJSON input (string)
  --input2 <geojson>    Second GeoJSON input
  --file <path>         Read first input from file
  --file2 <path>        Read second input from file
  --output <path>       Write result to file (default: stdout)
  --units <km|mi|m>     Distance units
  --radius <n>          Buffer radius
  --bbox <json>         Bounding box [minX,minY,maxX,maxY]
  --cellSide <n>        Grid cell size
  --coordinates <json>  Coordinates array
  --properties <json>   Properties object
  --numberOfClusters <n> K-means cluster count
  --maxDistance <n>      DBSCAN max distance
  --count <n>           Random feature count
  --tolerance <n>       Simplify tolerance
  --angle <n>           Rotation angle
  --factor <n>          Scale factor
  --distance <n>        Translate/destination distance
  --direction <n>       Translate direction (degrees)
  --list                List all available actions
  --help                Show this help message
`);
}

main();
