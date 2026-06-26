#!/usr/bin/env node

// Extract exact YouTube watch links from the current page DOM.
// Intended for browser-console use or quick local adaptation.

const anchors = Array.from(document.querySelectorAll('a#video-title'));
const items = anchors
  .map((a) => ({
    title: (a.textContent || '').trim().replace(/\s+/g, ' '),
    url: a.href,
  }))
  .filter((x) => x.title && x.url)
  .filter((x, i, arr) => arr.findIndex((y) => y.url === x.url) === i);

console.log(JSON.stringify(items, null, 2));
