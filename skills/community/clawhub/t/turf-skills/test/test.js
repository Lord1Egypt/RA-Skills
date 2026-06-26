'use strict';

const { execSync } = require('child_process');
const path = require('path');

const CLI = path.join(__dirname, '..', 'index.js');
const FIXTURES = path.join(__dirname, 'fixtures');

let passed = 0;
let failed = 0;

function run(args) {
  const result = execSync(`node ${CLI} ${args}`, { encoding: 'utf-8', cwd: path.join(__dirname, '..') });
  return result.trim();
}

function test(name, fn) {
  try {
    fn();
    passed++;
    console.log(`  ✓ ${name}`);
  } catch (err) {
    failed++;
    console.log(`  ✗ ${name}`);
    console.log(`    ${err.message}`);
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg || 'Assertion failed');
}

function assertApprox(actual, expected, delta, msg) {
  assert(Math.abs(actual - expected) < delta, msg || `Expected ~${expected}, got ${actual}`);
}

// --- Measurement ---
console.log('\nMeasurement:');

test('distance', () => {
  const r = Number(run('--action distance --input \'{"type":"Point","coordinates":[120,30]}\' --input2 \'{"type":"Point","coordinates":[121,31]}\''));
  assertApprox(r, 146.78, 1);
});

test('area', () => {
  const r = Number(run(`--action area --file ${FIXTURES}/polygon.geojson`));
  assert(r > 1e9, `Area should be > 1e9, got ${r}`);
});

test('length', () => {
  const r = Number(run(`--action length --file ${FIXTURES}/line.geojson`));
  assert(r > 0, 'Length should be > 0');
});

test('bearing', () => {
  const r = Number(run('--action bearing --input \'{"type":"Point","coordinates":[120,30]}\' --input2 \'{"type":"Point","coordinates":[121,31]}\''));
  assert(r > 0 && r < 90, `Bearing should be NE, got ${r}`);
});

test('midpoint', () => {
  const r = JSON.parse(run('--action midpoint --input \'{"type":"Point","coordinates":[120,30]}\' --input2 \'{"type":"Point","coordinates":[122,32]}\''));
  assert(r.geometry.coordinates[0] > 120 && r.geometry.coordinates[0] < 122);
});

test('center', () => {
  const r = JSON.parse(run(`--action center --file ${FIXTURES}/polygon.geojson`));
  assert(r.geometry.type === 'Point');
});

test('centroid', () => {
  const r = JSON.parse(run(`--action centroid --file ${FIXTURES}/polygon.geojson`));
  assertApprox(r.geometry.coordinates[0], 120.5, 0.1);
});

test('bbox', () => {
  const r = JSON.parse(run(`--action bbox --file ${FIXTURES}/polygon.geojson`));
  assert(Array.isArray(r) && r.length === 4);
});

test('along', () => {
  const r = JSON.parse(run(`--action along --file ${FIXTURES}/line.geojson --distance 50`));
  assert(r.geometry.type === 'Point');
});

test('destination', () => {
  const r = JSON.parse(run('--action destination --input \'{"type":"Point","coordinates":[120,30]}\' --distance 100 --direction 90'));
  assert(r.geometry.coordinates[0] > 120);
});

test('envelope', () => {
  const r = JSON.parse(run(`--action envelope --file ${FIXTURES}/points-collection.geojson`));
  assert(r.geometry.type === 'Polygon');
});

// --- Query ---
console.log('\nQuery:');

test('booleanPointInPolygon (true)', () => {
  const r = run(`--action booleanPointInPolygon --file ${FIXTURES}/point.geojson --file2 ${FIXTURES}/polygon.geojson`);
  assert(r === 'true');
});

test('booleanPointInPolygon (false)', () => {
  const r = run('--action booleanPointInPolygon --input \'{"type":"Point","coordinates":[0,0]}\' --file2 ' + `${FIXTURES}/polygon.geojson`);
  assert(r === 'false');
});

test('booleanContains', () => {
  const r = run(`--action booleanContains --file ${FIXTURES}/polygon.geojson --file2 ${FIXTURES}/point.geojson`);
  assert(r === 'true');
});

test('booleanDisjoint', () => {
  const r = run('--action booleanDisjoint --input \'{"type":"Point","coordinates":[0,0]}\' --file2 ' + `${FIXTURES}/polygon.geojson`);
  assert(r === 'true');
});

test('booleanIntersects', () => {
  const r = run(`--action booleanIntersects --file ${FIXTURES}/polygon.geojson --file2 ${FIXTURES}/line.geojson`);
  assert(r === 'true');
});

test('nearestPoint', () => {
  const r = JSON.parse(run('--action nearestPoint --input \'{"type":"Point","coordinates":[120.1,30.1]}\' --file2 ' + `${FIXTURES}/points-collection.geojson`));
  assert(r.geometry.type === 'Point');
});

// --- Transformation ---
console.log('\nTransformation:');

test('buffer', () => {
  const r = JSON.parse(run('--action buffer --input \'{"type":"Point","coordinates":[120,30]}\' --radius 5 --units kilometers'));
  assert(r.geometry.type === 'Polygon');
});

test('union', () => {
  const poly1 = '{"type":"Polygon","coordinates":[[[120,30],[121,30],[121,31],[120,31],[120,30]]]}';
  const poly2 = '{"type":"Polygon","coordinates":[[[120.5,30.5],[121.5,30.5],[121.5,31.5],[120.5,31.5],[120.5,30.5]]]}';
  const r = JSON.parse(run(`--action union --input '${poly1}' --input2 '${poly2}'`));
  assert(r.geometry.type === 'Polygon' || r.geometry.type === 'MultiPolygon');
});

test('simplify', () => {
  const r = JSON.parse(run(`--action simplify --file ${FIXTURES}/polygon.geojson --tolerance 0.01`));
  assert(r.geometry.type === 'Polygon');
});

test('convex', () => {
  const r = JSON.parse(run(`--action convex --file ${FIXTURES}/points-collection.geojson`));
  assert(r.geometry.type === 'Polygon');
});

test('transformRotate', () => {
  const r = JSON.parse(run(`--action transformRotate --file ${FIXTURES}/polygon.geojson --angle 45`));
  assert(r.geometry.type === 'Polygon');
});

test('transformScale', () => {
  const r = JSON.parse(run(`--action transformScale --file ${FIXTURES}/polygon.geojson --factor 2`));
  assert(r.geometry.type === 'Polygon');
});

// --- Helpers ---
console.log('\nHelpers:');

test('point', () => {
  const r = JSON.parse(run('--action point --coordinates \'[120,30]\''));
  assert(r.geometry.type === 'Point');
});

test('lineString', () => {
  const r = JSON.parse(run('--action lineString --coordinates \'[[120,30],[121,31]]\''));
  assert(r.geometry.type === 'LineString');
});

test('polygon', () => {
  const r = JSON.parse(run('--action polygon --coordinates \'[[[120,30],[121,30],[121,31],[120,31],[120,30]]]\''));
  assert(r.geometry.type === 'Polygon');
});

test('randomPoint', () => {
  const r = JSON.parse(run('--action randomPoint --count 5'));
  assert(r.features.length === 5);
});

// --- Interpolation ---
console.log('\nInterpolation:');

test('hexGrid', () => {
  const r = JSON.parse(run('--action hexGrid --bbox \'[120,30,121,31]\' --cellSide 10'));
  assert(r.type === 'FeatureCollection' && r.features.length > 0);
});

test('pointGrid', () => {
  const r = JSON.parse(run('--action pointGrid --bbox \'[120,30,121,31]\' --cellSide 20'));
  assert(r.type === 'FeatureCollection' && r.features.length > 0);
});

test('squareGrid', () => {
  const r = JSON.parse(run('--action squareGrid --bbox \'[120,30,121,31]\' --cellSide 20'));
  assert(r.type === 'FeatureCollection' && r.features.length > 0);
});

// --- Clustering ---
console.log('\nClustering:');

test('clustersKmeans', () => {
  const r = JSON.parse(run(`--action clustersKmeans --file ${FIXTURES}/points-collection.geojson --numberOfClusters 3`));
  assert(r.type === 'FeatureCollection');
  assert(r.features[0].properties.cluster !== undefined);
});

test('clustersDbscan', () => {
  const r = JSON.parse(run(`--action clustersDbscan --file ${FIXTURES}/points-collection.geojson --maxDistance 100 --minPoints 2`));
  assert(r.type === 'FeatureCollection');
  assert(r.features[0].properties.cluster !== undefined || r.features[0].properties.dbscan !== undefined);
});

// --- Summary ---
console.log(`\n${passed + failed} tests: ${passed} passed, ${failed} failed\n`);
process.exit(failed > 0 ? 1 : 0);
