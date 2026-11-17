#!/usr/bin/env node
/**
 * check-diagram.mjs — zero-runtime-dependency post-render checker
 *
 * Usage:
 *   node scripts/check-diagram.mjs <path-to-diagram.html>
 *
 * Exit codes:
 *   0  all checks passed
 *   1  one or more checks failed (errors printed to stdout)
 *
 * Strategy (per R2 guidance):
 *   - Use the embedded IR JSON (#diagram-ir) as the authoritative geometry
 *     source when available (JSON.parse — no DOM parser needed).
 *   - Use data-node-id / data-edge-id attributes to cross-check SVG elements
 *     against the IR registry.
 *   - Validate IR regions (bounds inside viewBox, contains reference known
 *     nodes), remind revise-mode artifacts to carry edit_scope, and check
 *     optional edge labelAnchor geometry against node boxes.
 *   - Marker-reference integrity and placeholder detection use targeted regex
 *     on the raw HTML string — safe because the patterns are template-scoped.
 *   - No external npm packages. Requires Node 18+.
 */

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
const [, , inputPath] = process.argv;
if (!inputPath) {
  console.error('Usage: node scripts/check-diagram.mjs <path-to-diagram.html>');
  process.exit(1);
}

let html;
try {
  html = readFileSync(resolve(inputPath), 'utf8');
} catch (err) {
  console.error(`Cannot read input file: ${inputPath} (${err.code || err.message})`);
  console.error('Usage: node scripts/check-diagram.mjs <path-to-diagram.html>');
  process.exit(1);
}
const errors = [];
const warnings = [];

// Stable error/warning codes — keep in sync with the "Error codes" table in README.md.
// Codes are matched on message content at fail()/warn() time; validation logic is unchanged.
const ERROR_CODE_TABLE = [
  [/^Usage:/, 'E001'],
  [/invalid JSON/, 'E002'],
  [/region/i, 'E003'],
  [/#diagram-ir must|missing a non-empty string id|Duplicate IR/, 'E004'],
  [/no bounds|invalid bounds|viewBox/, 'E005'],
  [/overlaps node/, 'E006'],
  [/missing a source node|missing a target node|references unknown/, 'E007'],
  [/data-node-id|data-edge-id/, 'E008'],
  [/marker/i, 'E009'],
  [/Placeholder text/, 'E010'],
  [/Notes rail/, 'E011'],
  [/self-contained/, 'E012'],
  [/labelAnchor/, 'E013'],
  [/starts away from|ends away from|passes through or hugs|runs along node/, 'E014'],
];
const WARN_CODE_TABLE = [
  [/legacy mode/, 'W001'],
  [/edit_scope is missing/, 'W002'],
  [/may be intentionally omitted|export buttons may not work/, 'W003'],
  [/unsupported SVG path syntax/, 'W004'],
];
function codeFor(msg, table, fallback) {
  for (const [re, code] of table) if (re.test(msg)) return code;
  return fallback;
}
function fail(msg) { errors.push(`[${codeFor(msg, ERROR_CODE_TABLE, 'E099')}] ${msg}`); }
function warn(msg) { warnings.push(`[${codeFor(msg, WARN_CODE_TABLE, 'W099')}] ${msg}`); }

// ---------------------------------------------------------------------------
// 1. Extract embedded IR JSON
// ---------------------------------------------------------------------------
let ir = null;
const irMatch = html.match(/<script[^>]+id="diagram-ir"[^>]*>([\s\S]*?)<\/script>/);
if (!irMatch) {
  warn('No #diagram-ir slot found — running in legacy mode. Geometry checks (node bounds, overlap, region containment, connector endpoints, connector routing, labelAnchor overlap) are SKIPPED. Only placeholder, marker, self-containment, and structural checks run. Re-emit the artifact with an embedded IR slot to enable full validation.');
} else {
  try {
    ir = JSON.parse(irMatch[1].trim());
  } catch (e) {
    fail(`#diagram-ir slot contains invalid JSON: ${e.message}`);
  }
}

// Normalized node list, safe to use anywhere below even when the IR is
// malformed (e.g. ir.nodes is missing or not an array). Section 3 below
// already fails the check when nodes/edges aren't proper arrays; this just
// prevents a TypeError from crashing the rest of the script afterward.
const irNodes = ir && Array.isArray(ir.nodes) ? ir.nodes : [];

function isFiniteNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function collectAttributeValues(attributeName) {
  const values = new Set();
  const pattern = new RegExp(`\\b${attributeName}\\s*=\\s*["']([^"']+)["']`, 'g');
  for (const match of html.matchAll(pattern)) values.add(match[1]);
  return values;
}

// ---------------------------------------------------------------------------
// 2. Parse viewBox from SVG
// ---------------------------------------------------------------------------
const viewBoxMatch = html.match(/\bviewBox\s*=\s*["']([^"']+)["']/);
let vbX = 0, vbY = 0, vbW = 1500, vbH = 900;
if (viewBoxMatch) {
  const parts = viewBoxMatch[1].trim().split(/[\s,]+/).map(Number);
  if (parts.length === 4 && parts.every(n => !Number.isNaN(n))) {
    [vbX, vbY, vbW, vbH] = parts;
  }
}

// ---------------------------------------------------------------------------
// 3. IR-based geometry checks
// ---------------------------------------------------------------------------
if (ir) {
  if (typeof ir !== 'object' || Array.isArray(ir)) {
    fail('#diagram-ir must contain a JSON object.');
  }

  // Validate top-level IR fields: mode and lens must use supported values so
  // downstream renderers and the revise workflow behave predictably.
  const VALID_MODES = ['create', 'revise'];
  // Accept both "data movement" (rules doc spelling) and "data-movement"
  // (fixture/IR convention) so the checker does not reject valid artifacts.
  const VALID_LENSES = ['system', 'implementation', 'infrastructure', 'trust', 'data movement', 'data-movement', 'deployment', 'process'];
  if (ir.mode !== undefined && !VALID_MODES.includes(ir.mode)) {
    fail(`IR mode "${ir.mode}" is not one of ${VALID_MODES.join(', ')}.`);
  }
  if (ir.lens !== undefined && !VALID_LENSES.includes(ir.lens)) {
    fail(`IR lens "${ir.lens}" is not one of ${VALID_LENSES.join(', ')}.`);
  }

  const nodes = irNodes;
  const edges = ir && Array.isArray(ir.edges) ? ir.edges : [];
  if (!Array.isArray(ir.nodes) || !Array.isArray(ir.edges)) {
    fail('#diagram-ir must define nodes and edges arrays.');
  }
  if (nodes.length === 0) {
    fail('#diagram-ir must contain at least one node; empty IR cannot validate the rendered SVG.');
  }
  const nodeMap = {};
  const nodeIds = new Set();
  const edgeIds = new Set();

  // 3a. Node bounds inside viewBox
  for (const node of nodes) {
    if (!node || typeof node !== 'object' || typeof node.id !== 'string' || node.id.trim() === '') {
      fail(`IR node is missing a non-empty string id: ${JSON.stringify(node)}`);
      continue;
    }
    if (nodeIds.has(node.id)) {
      fail(`Duplicate IR node id: "${node.id}".`);
      continue;
    }
    nodeIds.add(node.id);
    const b = node.bounds;
    if (!b || typeof b !== 'object') {
      fail(`IR node "${node.id}" has no bounds.`);
      continue;
    }
    if (![b.x, b.y, b.width, b.height].every(isFiniteNumber) || b.width <= 0 || b.height <= 0) {
      fail(`IR node "${node.id}" has invalid bounds: ${JSON.stringify(b)}.`);
      continue;
    }
    nodeMap[node.id] = b;

    if (b.x < vbX) fail(`Node "${node.id}" left edge (${b.x}) is outside viewBox left (${vbX}).`);
    if (b.y < vbY) fail(`Node "${node.id}" top edge (${b.y}) is outside viewBox top (${vbY}).`);
    if (b.x + b.width > vbX + vbW) fail(`Node "${node.id}" right edge (${b.x + b.width}) exceeds viewBox right (${vbX + vbW}).`);
    if (b.y + b.height > vbY + vbH) fail(`Node "${node.id}" bottom edge (${b.y + b.height}) exceeds viewBox bottom (${vbY + vbH}).`);
  }

  // 3b. Pairwise node overlap
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], bNode = nodes[j];
      const ab = a.bounds, bb = bNode.bounds;
      if (!ab || !bb) continue;
      const overlapX = ab.x < bb.x + bb.width && ab.x + ab.width > bb.x;
      const overlapY = ab.y < bb.y + bb.height && ab.y + ab.height > bb.y;
      if (overlapX && overlapY) {
        fail(`Node "${a.id}" overlaps node "${bNode.id}" (IR bounds intersection).`);
      }
    }
  }

  // 3b-2. Region integrity: bounds inside viewBox, contains reference known
  // nodes. Nested regions (a region inside another region's bounds) are a
  // legitimate pattern and are NOT flagged.
  const regions = Array.isArray(ir.regions) ? ir.regions : null;
  if (ir.regions !== undefined && regions === null) {
    fail('#diagram-ir regions must be an array when present.');
  }
  const regionIds = new Set();
  if (regions) {
    for (const region of regions) {
      if (!region || typeof region !== 'object' || typeof region.id !== 'string' || region.id.trim() === '') {
        fail(`IR region is missing a non-empty string id: ${JSON.stringify(region)}`);
        continue;
      }
      if (regionIds.has(region.id)) {
        fail(`Duplicate IR region id: "${region.id}".`);
        continue;
      }
      regionIds.add(region.id);
      const rb = region.bounds;
      if (!rb || typeof rb !== 'object') {
        fail(`IR region "${region.id}" has no bounds.`);
        continue;
      }
      if (![rb.x, rb.y, rb.width, rb.height].every(isFiniteNumber) || rb.width <= 0 || rb.height <= 0) {
        fail(`IR region "${region.id}" has invalid bounds: ${JSON.stringify(rb)}.`);
        continue;
      }
      if (rb.x < vbX || rb.y < vbY || rb.x + rb.width > vbX + vbW || rb.y + rb.height > vbY + vbH) {
        fail(`IR region "${region.id}" bounds exceed the viewBox.`);
      }
      if (region.contains !== undefined) {
        if (!Array.isArray(region.contains)) {
          fail(`IR region "${region.id}" contains must be an array when present.`);
        } else {
          for (const cid of region.contains) {
            if (typeof cid !== 'string' || !nodeIds.has(cid)) {
              fail(`IR region "${region.id}" contains unknown node id: ${JSON.stringify(cid)}.`);
            }
          }
        }
      }
    }
  }

  // 3b-3. Region containment and gutter: a node listed in region.contains must
  // sit fully inside the region with a visible gutter on every side. A node
  // flush with the region border (0px gutter) makes the two strokes paint on
  // top of each other and reads as a broken frame in the render — the most
  // common region defect that pure viewBox/bounds checks miss.
  const MIN_REGION_GUTTER = 10;
  if (regions) {
    for (const region of regions) {
      if (!region || typeof region !== 'object') continue;
      const rb = region.bounds;
      if (!rb || ![rb.x, rb.y, rb.width, rb.height].every(isFiniteNumber)) continue;
      if (!Array.isArray(region.contains)) continue;
      for (const cid of region.contains) {
        const nb = nodeMap[cid];
        if (!nb) continue; // unknown ids already failed in 3b
        const escapes = nb.x < rb.x || nb.y < rb.y ||
          nb.x + nb.width > rb.x + rb.width || nb.y + nb.height > rb.y + rb.height;
        if (escapes) {
          fail(`Node "${cid}" in region "${region.id}" escapes the region bounds.`);
          continue;
        }
        const gutters = {
          left: nb.x - rb.x,
          top: nb.y - rb.y,
          right: rb.x + rb.width - (nb.x + nb.width),
          bottom: rb.y + rb.height - (nb.y + nb.height),
        };
        const tight = Object.entries(gutters).filter(([, g]) => g < MIN_REGION_GUTTER);
        if (tight.length > 0) {
          const detail = tight.map(([side, g]) => `${side}: ${g}px`).join(', ');
          fail(`Node "${cid}" sits too close to region "${region.id}" border (${detail}; minimum ${MIN_REGION_GUTTER}px).`);
        }
      }
    }
  }

  // Revise artifacts should record their edit scope.
  if (ir.mode === 'revise') {
    const scopeValue = ir.edit_scope;
    if (scopeValue === undefined || scopeValue === null || String(scopeValue).trim() === '') {
      warn('IR mode is "revise" but edit_scope is missing — record the revision scope.');
    }
  }

  // 3c. Edge endpoint reachability
  for (const edge of edges) {
    if (!edge || typeof edge !== 'object' || typeof edge.id !== 'string' || edge.id.trim() === '') {
      fail(`IR edge is missing a non-empty string id: ${JSON.stringify(edge)}`);
      continue;
    }
    if (edgeIds.has(edge.id)) {
      fail(`Duplicate IR edge id: "${edge.id}".`);
      continue;
    }
    edgeIds.add(edge.id);
    if (typeof edge.from !== 'string' || edge.from.trim() === '') {
      fail(`Edge "${edge.id}" is missing a source node id.`);
    }
    if (typeof edge.to !== 'string' || edge.to.trim() === '') {
      fail(`Edge "${edge.id}" is missing a target node id.`);
    }
    const fromBounds = nodeMap[edge.from];
    const toBounds = nodeMap[edge.to];
    if (edge.from && !fromBounds) fail(`Edge "${edge.id}" references unknown source node "${edge.from}".`);
    if (edge.to && !toBounds) fail(`Edge "${edge.id}" references unknown target node "${edge.to}".`);

    // Optional label geometry: when a renderer records where a connector label
    // sits, verify it does not sit on top of any node box (the most common
    // visual defect). Absence of labelAnchor simply skips the check.
    if (edge.labelAnchor !== undefined && edge.labelAnchor !== null) {
      const la = edge.labelAnchor;
      if (typeof la !== 'object' || !isFiniteNumber(la.x) || !isFiniteNumber(la.y)) {
        fail(`Edge "${edge.id}" has invalid labelAnchor: ${JSON.stringify(la)}.`);
      } else {
        const halfW = isFiniteNumber(la.width) && la.width > 0 ? la.width / 2 : 0;
        // Approximate 10px label box around a baseline-anchored text point.
        const left = la.x - halfW, right = la.x + halfW;
        const top = la.y - 10, bottom = la.y + 2;
        for (const [nid, nb] of Object.entries(nodeMap)) {
          const overlapX = left < nb.x + nb.width && right > nb.x;
          const overlapY = top < nb.y + nb.height && bottom > nb.y;
          if (overlapX && overlapY) {
            fail(`Edge "${edge.id}" labelAnchor sits on node "${nid}".`);
            break;
          }
        }
      }
    }
  }

  // 3d/3e. Bidirectional data attribute cross-check
  const svgNodeIds = collectAttributeValues('data-node-id');
  const svgEdgeIds = collectAttributeValues('data-edge-id');
  for (const id of nodeIds) {
    if (!svgNodeIds.has(id)) fail(`IR node "${id}" has no matching data-node-id attribute in the SVG.`);
  }
  for (const id of edgeIds) {
    if (!svgEdgeIds.has(id)) fail(`IR edge "${id}" has no matching data-edge-id attribute in the SVG.`);
  }
  for (const id of svgNodeIds) {
    if (!nodeIds.has(id)) fail(`SVG data-node-id "${id}" is missing from the IR.`);
  }
  for (const id of svgEdgeIds) {
    if (!edgeIds.has(id)) fail(`SVG data-edge-id "${id}" is missing from the IR.`);
  }
}

// ---------------------------------------------------------------------------
// 4. Marker-reference integrity (regex-safe on template-scoped patterns)
// ---------------------------------------------------------------------------
// Collect all defined marker IDs
const definedMarkers = new Map();
for (const m of html.matchAll(/<marker\b[^>]+\bid\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/marker>/gi)) {
  const fill = m[2].match(/\bfill\s*=\s*["']([^"']+)["']/i)?.[1];
  definedMarkers.set(m[1], fill);
}

// Collect all used marker-end references
const usedMarkers = new Set();
for (const m of html.matchAll(/<[^>]+\bmarker-end\s*=\s*["']url\(#([^)]+)\)["'][^>]*>/gi)) {
  usedMarkers.add(m[1]);
  const stroke = m[0].match(/\bstroke\s*=\s*["']([^"']+)["']/i)?.[1];
  const markerFill = definedMarkers.get(m[1]);
  if (!definedMarkers.has(m[1])) {
    fail(`marker-end references "#${m[1]}" but no <marker id="${m[1]}"> is defined in <defs>.`);
  } else if (stroke && markerFill && stroke !== markerFill) {
    fail(`marker "#${m[1]}" fill (${markerFill}) does not match connector stroke (${stroke}).`);
  }
}

// ---------------------------------------------------------------------------
// 5. Placeholder text detection
// ---------------------------------------------------------------------------
const PLACEHOLDER_PATTERNS = [
  /System Map Title/,
  /One sentence that states the system boundary/,
  /Summarize the runtime boundary/,
  /Describe the primary request path/,
  /Describe identity, event, data-write/,
  /List scale, resilience/,
  /Record assumptions made because the source brief omitted/,
];

for (const pat of PLACEHOLDER_PATTERNS) {
  if (pat.test(html)) {
    fail(`Placeholder text still present: matches /${pat.source}/.`);
  }
}

// ---------------------------------------------------------------------------
// 6. Structural presence checks
// ---------------------------------------------------------------------------
if (!/<aside\b[^>]*class="[^"]*notes[^"]*"/.test(html)) {
  fail('Notes rail (<aside class="notes">) is missing.');
}
if (!/<nav\b[^>]*class="[^"]*toolbar[^"]*"/.test(html)) {
  warn('Export toolbar (<nav class="toolbar">) not found — may be intentionally omitted.');
}
if (!/<script\b[^>]+id="diagram-ir"/.test(html)) {
  // Already warned above; skip duplicate
}
if (!/<svg\b[^>]+id="system-map"/.test(html)) {
  warn('SVG element with id="system-map" not found — export buttons may not work.');
}

// No external asset references (enforces self-contained rule)
for (const m of html.matchAll(/(?:src|href)\s*=\s*["']([^"']+)["']/gi)) {
  const value = m[1].trim();
  if (/^(?:https?:)?\/\//i.test(value) || !/^(?:#|data:|about:|javascript:)/i.test(value)) {
    fail(`External or relative asset reference found: ${value} — artifact must be self-contained.`);
  }
}
const inlineCss = [...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map(match => match[1]).join('\n');
if (/(?:@import\s+|url\(\s*["']?)(?!(?:data:|#|about:|javascript:))/i.test(inlineCss)) {
  fail('External CSS asset reference found via @import or url() — artifact must be self-contained.');
}

// ---------------------------------------------------------------------------
// 7. Simple SVG connector endpoint checks
// ---------------------------------------------------------------------------
// Generated diagrams use simple absolute M/H/V paths. Keep this parser small
// and dependency-free; unsupported path syntax is surfaced as a warning for
// human review rather than guessed incorrectly.
function parseSimplePathEndpoints(d) {
  const tokens = d.match(/[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?/g) || [];
  let command = null;
  let current = { x: 0, y: 0 };
  let start = null;
  let index = 0;
  let end = null;
  while (index < tokens.length) {
    if (/^[a-zA-Z]$/.test(tokens[index])) command = tokens[index++];
    if (!command || !/^[MmHhVvLlZz]$/.test(command)) return null;
    if (command === 'Z' || command === 'z') {
      current = start || current;
      end = { ...current };
      command = null;
      continue;
    }
    const relative = command === command.toLowerCase();
    const upper = command.toUpperCase();
    if (upper === 'H') {
      if (index >= tokens.length || /^[a-zA-Z]$/.test(tokens[index])) return null;
      const x = Number(tokens[index++]);
      current = { x: relative ? current.x + x : x, y: current.y };
    } else if (upper === 'V') {
      if (index >= tokens.length || /^[a-zA-Z]$/.test(tokens[index])) return null;
      const y = Number(tokens[index++]);
      current = { x: current.x, y: relative ? current.y + y : y };
    } else {
      if (index + 1 >= tokens.length || /^[a-zA-Z]$/.test(tokens[index]) || /^[a-zA-Z]$/.test(tokens[index + 1])) return null;
      const x = Number(tokens[index++]);
      const y = Number(tokens[index++]);
      current = { x: relative ? current.x + x : x, y: relative ? current.y + y : y };
      if (!start) start = { ...current };
      if (upper === 'M') command = relative ? 'l' : 'L';
    }
    end = { ...current };
  }
  return start && end ? { start, end } : null;
}

function pointOnRectEdge(point, bounds, tolerance = 2) {
  const inX = point.x >= bounds.x - tolerance && point.x <= bounds.x + bounds.width + tolerance;
  const inY = point.y >= bounds.y - tolerance && point.y <= bounds.y + bounds.height + tolerance;
  const onVertical = (Math.abs(point.x - bounds.x) <= tolerance || Math.abs(point.x - (bounds.x + bounds.width)) <= tolerance) && inY;
  const onHorizontal = (Math.abs(point.y - bounds.y) <= tolerance || Math.abs(point.y - (bounds.y + bounds.height)) <= tolerance) && inX;
  return onVertical || onHorizontal;
}

// Parse a simple M/H/V/L/Z path into its constituent line segments. Returns
// null for unsupported path syntax (caller falls back to a warning). Each
// segment is { x1, y1, x2, y2 } in absolute coordinates.
function parsePathSegments(d) {
  const tokens = d.match(/[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?/g) || [];
  const segments = [];
  let command = null;
  let current = { x: 0, y: 0 };
  let subpathStart = null;
  let index = 0;
  while (index < tokens.length) {
    if (/^[a-zA-Z]$/.test(tokens[index])) command = tokens[index++];
    if (!command || !/^[MmHhVvLlZz]$/.test(command)) return null;
    if (command === 'Z' || command === 'z') {
      if (subpathStart) {
        segments.push({ x1: current.x, y1: current.y, x2: subpathStart.x, y2: subpathStart.y });
        current = { ...subpathStart };
      }
      command = null;
      continue;
    }
    const relative = command === command.toLowerCase();
    const upper = command.toUpperCase();
    let next;
    if (upper === 'H') {
      if (index >= tokens.length || /^[a-zA-Z]$/.test(tokens[index])) return null;
      const x = Number(tokens[index++]);
      next = { x: relative ? current.x + x : x, y: current.y };
    } else if (upper === 'V') {
      if (index >= tokens.length || /^[a-zA-Z]$/.test(tokens[index])) return null;
      const y = Number(tokens[index++]);
      next = { x: current.x, y: relative ? current.y + y : y };
    } else {
      if (index + 1 >= tokens.length || /^[a-zA-Z]$/.test(tokens[index]) || /^[a-zA-Z]$/.test(tokens[index + 1])) return null;
      const x = Number(tokens[index++]);
      const y = Number(tokens[index++]);
      next = { x: relative ? current.x + x : x, y: relative ? current.y + y : y };
    }
    if (upper !== 'M') {
      segments.push({ x1: current.x, y1: current.y, x2: next.x, y2: next.y });
    } else {
      subpathStart = { ...next };
    }
    current = next;
    if (upper === 'M') command = relative ? 'l' : 'L'; // implicit line-to after move
  }
  return segments;
}

// Return true when the segment (x1,y1)-(x2,y2) passes through the *strict
// interior* of the rectangle [rx, rx+rw] x [ry, ry+rh]. Endpoints and segments
// lying exactly on a rectangle edge do NOT count — only segments that cross the
// box. Uses the parametric t-interval of the open rectangle; an empty overlap
// means the segment does not penetrate the interior.
function segmentIntersectsRectInterior(x1, y1, x2, y2, rx, ry, rw, rh) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  let tMin = 0;
  let tMax = 1;
  if (dx > 0) {
    tMin = Math.max(tMin, (rx - x1) / dx);
    tMax = Math.min(tMax, (rx + rw - x1) / dx);
  } else if (dx < 0) {
    tMin = Math.max(tMin, (rx + rw - x1) / dx);
    tMax = Math.min(tMax, (rx - x1) / dx);
  } else if (!(x1 > rx && x1 < rx + rw)) {
    return false;
  }
  if (dy > 0) {
    tMin = Math.max(tMin, (ry - y1) / dy);
    tMax = Math.min(tMax, (ry + rh - y1) / dy);
  } else if (dy < 0) {
    tMin = Math.max(tMin, (ry + rh - y1) / dy);
    tMax = Math.min(tMax, (ry - y1) / dy);
  } else if (!(y1 > ry && y1 < ry + rh)) {
    return false;
  }
  return tMin < tMax;
}

// Minimum distance from a point to an axis-aligned rectangle. Returns 0 when
// the point is inside or on the rectangle border.
function pointRectDistance(px, py, rx, ry, rw, rh) {
  const dx = Math.max(rx - px, 0, px - (rx + rw));
  const dy = Math.max(ry - py, 0, py - (ry + rh));
  return Math.hypot(dx, dy);
}

// Minimum distance from an axis-aligned (horizontal/vertical) segment to a
// rectangle. Diagonal segments fall back to sampling endpoints + midpoint,
// which is conservative (may over-report closeness) — generated diagrams use
// only orthogonal connectors so this path is rarely hit.
function segmentRectMinDistance(seg, rect) {
  const { x1, y1, x2, y2 } = seg;
  const rx = rect.x, ry = rect.y, rw = rect.width, rh = rect.height;
  const rRight = rx + rw, rBottom = ry + rh;
  if (y1 === y2) {
    const cy = y1;
    const xL = Math.min(x1, x2), xR = Math.max(x1, x2);
    if (xR < rx) {
      return Math.hypot(rx - xR, Math.max(0, ry - cy, cy - rBottom));
    } else if (xL > rRight) {
      return Math.hypot(xL - rRight, Math.max(0, ry - cy, cy - rBottom));
    }
    return Math.max(0, ry - cy, cy - rBottom);
  } else if (x1 === x2) {
    const cx = x1;
    const yB = Math.min(y1, y2), yT = Math.max(y1, y2);
    if (yT < ry) {
      return Math.hypot(Math.max(0, rx - cx, cx - rRight), ry - yT);
    } else if (yB > rBottom) {
      return Math.hypot(Math.max(0, rx - cx, cx - rRight), yB - rBottom);
    }
    return Math.max(0, rx - cx, cx - rRight);
  }
  return Math.min(
    pointRectDistance(x1, y1, rx, ry, rw, rh),
    pointRectDistance(x2, y2, rx, ry, rw, rh),
    pointRectDistance((x1 + x2) / 2, (y1 + y2) / 2, rx, ry, rw, rh)
  );
}

// A connector segment that runs collinearly along a region's border for more
// than a short stub looks like a merged/double line. Perpendicular crossings of
// region borders are allowed; only long collinear overlaps are defects.
function segmentRunsAlongRegionBorder(seg, rect) {
  const { x1, y1, x2, y2 } = seg;
  const rx = rect.x, ry = rect.y, rRight = rx + rect.width, rBottom = ry + rect.height;
  const EDGE_TOL = 1.5;     // how close to the edge counts as "along"
  const MIN_OVERLAP = 12;   // minimum collinear overlap length to flag
  if (y1 === y2) {
    const cy = y1;
    if (Math.abs(cy - ry) > EDGE_TOL && Math.abs(cy - rBottom) > EDGE_TOL) return false;
    const xL = Math.min(x1, x2), xR = Math.max(x1, x2);
    const overlap = Math.max(0, Math.min(xR, rRight) - Math.max(xL, rx));
    return overlap > MIN_OVERLAP;
  } else if (x1 === x2) {
    const cx = x1;
    if (Math.abs(cx - rx) > EDGE_TOL && Math.abs(cx - rRight) > EDGE_TOL) return false;
    const yB = Math.min(y1, y2), yT = Math.max(y1, y2);
    const overlap = Math.max(0, Math.min(yT, rBottom) - Math.max(yB, ry));
    return overlap > MIN_OVERLAP;
  }
  return false;
}

// Connectors must keep clear of every node border (except their own source and
// target, which the endpoints legitimately touch). MIN_NODE_CLEARANCE is the
// required gap in pixels; anything closer reads as a merged or overlapping line.
const MIN_NODE_CLEARANCE = 3;

// A connector segment must not run collinearly along any node's edge (including
// its own source or target). The endpoint may touch the edge, but only when the
// segment is perpendicular to it. A segment that is collinear with an edge and
// shares any point with it (overlapping the edge, or touching it at a corner so
// it visually extends the border) merges with the node stroke and is rejected.
function segmentRunsAlongNodeEdge(seg, rect) {
  const { x1, y1, x2, y2 } = seg;
  const rx = rect.x, ry = rect.y, rRight = rx + rect.width, rBottom = ry + rect.height;
  const EDGE_TOL = 1.5;
  if (y1 === y2) {
    const cy = y1;
    if (Math.abs(cy - ry) > EDGE_TOL && Math.abs(cy - rBottom) > EDGE_TOL) return false;
    const xL = Math.min(x1, x2), xR = Math.max(x1, x2);
    // Flag if the segment's x-span intersects the edge's span (touch or overlap).
    return Math.min(xR, rRight) >= Math.max(xL, rx);
  } else if (x1 === x2) {
    const cx = x1;
    if (Math.abs(cx - rx) > EDGE_TOL && Math.abs(cx - rRight) > EDGE_TOL) return false;
    const yB = Math.min(y1, y2), yT = Math.max(y1, y2);
    return Math.min(yT, rBottom) >= Math.max(yB, ry);
  }
  return false;
}

const irEdges = ir && Array.isArray(ir.edges) ? new Map(ir.edges.filter(edge => edge?.id).map(edge => [edge.id, edge])) : new Map();
const nodeBoundsMap = new Map(irNodes.filter(n => n?.id && n.bounds).map(n => [n.id, n.bounds]));
const regionBoundsList = (Array.isArray(ir.regions) ? ir.regions : [])
  .filter(r => r && r.bounds)
  .map(r => ({ id: r.id, bounds: r.bounds }));

for (const match of html.matchAll(/<path\b[^>]*\bdata-edge-id\s*=\s*["']([^"']+)["'][^>]*\bd\s*=\s*["']([^"']+)["'][^>]*>/gi)) {
  const edgeId = match[1];
  const edge = irEdges.get(edgeId);
  if (!edge || !ir) continue;
  const endpoints = parseSimplePathEndpoints(match[2]);
  if (!endpoints) {
    warn(`Edge "${edgeId}" uses unsupported SVG path syntax; endpoint geometry was not checked.`);
    continue;
  }
  const from = irNodes.find(node => node?.id === edge.from)?.bounds;
  const to = irNodes.find(node => node?.id === edge.to)?.bounds;
  if (from && !pointOnRectEdge(endpoints.start, from)) fail(`Edge "${edgeId}" starts away from source node "${edge.from}".`);
  if (to && !pointOnRectEdge(endpoints.end, to)) fail(`Edge "${edgeId}" ends away from target node "${edge.to}".`);

  const segments = parsePathSegments(match[2]);
  if (!segments) continue;

  // 1. No connector segment may pass through or run along any node rectangle
  //    except the connector's own source and target nodes.
  for (const [nid, nb] of nodeBoundsMap) {
    if (nid === edge.from || nid === edge.to) continue;
    for (const seg of segments) {
      if (segmentRectMinDistance(seg, nb) < MIN_NODE_CLEARANCE) {
        fail(`Edge "${edgeId}" path passes through or hugs node "${nid}" (${segmentRectMinDistance(seg, nb).toFixed(1)}px clearance).`);
        break;
      }
    }
  }

  // 1b. A connector segment (including the terminal one that lands on the
  //     source/target) must not run collinearly along a node's edge. The
  //     endpoint may touch the edge at one point, but a segment that coincides
  //     with the edge for an extended stretch merges with the node border.
  for (const [nid, nb] of nodeBoundsMap) {
    for (const seg of segments) {
      if (segmentRunsAlongNodeEdge(seg, nb)) {
        fail(`Edge "${edgeId}" runs along node "${nid}" border (segment is collinear with and touches the edge).`);
        break;
      }
    }
  }

  // 2. No connector segment may run collinearly along a region border for more
  //    than a short stub. Perpendicular crossings of region borders are fine.
  for (const region of regionBoundsList) {
    for (const seg of segments) {
      if (segmentRunsAlongRegionBorder(seg, region.bounds)) {
        fail(`Edge "${edgeId}" runs along region "${region.id}" border.`);
        break;
      }
    }
  }
}

// ---------------------------------------------------------------------------
// 8. Report
// ---------------------------------------------------------------------------

let exitCode = 0;

if (warnings.length > 0) {
  console.log(`\nWarnings (${warnings.length}):`);
  for (const w of warnings) console.log(`  ⚠  ${w}`);
}

if (errors.length > 0) {
  console.log(`\nErrors (${errors.length}):`);
  for (const e of errors) console.log(`  ✗  ${e}`);
  console.log(`\ncheck-diagram: FAILED (${errors.length} error(s))`);
  exitCode = 1;
} else {
  console.log(`\ncheck-diagram: PASSED${warnings.length > 0 ? ` (${warnings.length} warning(s))` : ''}`);
}

process.exit(exitCode);
