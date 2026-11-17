#!/usr/bin/env node
"use strict";
/**
 * Guards templates/canvas-comments.html — the reference page for commenting on a
 * canvas, where nothing has a DOM element of its own.
 *
 * These assert the parts that are a contract with ShareOne rather than taste. A
 * page author copying this file will change the nodes and the drawing; if they
 * also drop one of these, comments break in ways that look like ShareOne's fault:
 * anchors that never resolve, marks drifting away from their nodes, or readers
 * told that content was deleted when a view merely hid it.
 */
const fs = require("fs");
const path = require("path");

const FILE = path.join(__dirname, "..", "templates", "canvas-comments.html");
const html = fs.readFileSync(FILE, "utf8");

let failed = 0;
function check(name, ok, detail) {
  if (ok) {
    console.log(`  ok   ${name}`);
  } else {
    failed += 1;
    console.log(`  FAIL ${name}${detail ? " — " + detail : ""}`);
  }
}

console.log("canvas-comments.html");

// --- the SDK is optional, always ------------------------------------------------
// The page must work opened directly and with comments off, so every use goes
// through one guarded accessor rather than touching window.__SHAREONE__ inline.
const accessor = html.match(/function anchors\(\) \{[\s\S]*?\n  \}/);
check("has a single guarded accessor for the SDK", Boolean(accessor));
const outside = accessor ? html.replace(accessor[0], "") : html;
check("touches window.__SHAREONE__ only inside that accessor",
  !/window\.__SHAREONE__/.test(outside),
  "every other use must go through it, or the page breaks when opened directly");
check("the accessor is guarded",
  Boolean(accessor) && /window\.__SHAREONE__ && window\.__SHAREONE__\.anchors/.test(accessor[0]));
check("never assigns window.__SHAREONE__", !/window\.__SHAREONE__\s*=/.test(html),
  "several injected scripts attach namespaces to it; assigning deletes the rest");

// --- the three anchor states ---------------------------------------------------
check('reports "visible" with a rect', /state:\s*"visible"[\s\S]{0,80}rect/.test(html));
check('reports "hidden" for a view that does not draw it', /state:\s*"hidden"/.test(html));
check('does NOT report "missing" for something merely not drawn',
  !/state:\s*"missing"/.test(html),
  "missing means the content is gone; using it for a hidden node tells readers it was deleted");

// --- answering ShareOne --------------------------------------------------------
for (const ev of ["resync", "reveal", "hittest"]) {
  check(`handles "${ev}"`, new RegExp(`on\\(\\s*"${ev}"`).test(html));
}
check("hittest answers with labels, not bare ids",
  /on\(\s*"hittest"[\s\S]{0,700}label:\s*n\.label/.test(html),
  'a region named "3 items" tells a reader nothing about what was commented on');

// --- positions -----------------------------------------------------------------
check("reports positions on every redraw", /function draw\(\)[\s\S]{0,1400}report\(\)/.test(html));
check("re-reports when the canvas moves on screen",
  /addEventListener\("resize",\s*draw\)/.test(html) &&
  /addEventListener\("scroll",\s*report/.test(html),
  "positions are viewport-space, so scroll and resize change them");
check("positions are viewport-space (built from getBoundingClientRect)",
  /function rectOf[\s\S]{0,300}getBoundingClientRect\(\)/.test(html));

// --- the gesture ---------------------------------------------------------------
check("a press under a threshold is a click, not a drag", /DRAG_SLOP/.test(html));
check("does not capture the pointer on pointerdown",
  !/pointerdown[\s\S]{0,400}setPointerCapture/.test(html),
  "capturing on press makes every node in the page unclickable");
check("captures only after the threshold, inside try/catch",
  /drag\.moved = true[\s\S]{0,400}try\s*\{[\s\S]{0,120}setPointerCapture/.test(html),
  "a bare call can throw and abandon the very gesture it was protecting");
check("a pan does not become a selection", /if \(wasDrag\) return;/.test(html));

// --- ids -----------------------------------------------------------------------
const ids = [...html.matchAll(/id:\s*"((?:cap|type|row):[^"]+)"/g)].map((m) => m[1]);
check("declares ids for its nodes", ids.length >= 5, `found ${ids.length}`);
check("ids are unique within the page", new Set(ids).size === ids.length);
check("ids name the thing, not the render order",
  ids.every((id) => !/^\d+$|node-?\d+$/i.test(id)),
  "an index changes when the layout does, which is what an anchor must survive");

// --- self-contained ------------------------------------------------------------
check("no external script or style", !/<(script|link)[^>]+(src|href)=["']https?:/i.test(html));

console.log(failed === 0 ? "\nall checks passed" : `\n${failed} check(s) failed`);
process.exit(failed === 0 ? 0 : 1);
