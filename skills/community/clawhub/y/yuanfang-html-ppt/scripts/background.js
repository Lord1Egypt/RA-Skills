'use strict';

function applyBackground(slide, slideSpec) {
  const bg = slideSpec.background;
  if (!bg) return false;
  if (typeof bg === 'string' && bg.startsWith('#')) {
    slide.background = { color: bg };
  } else if (typeof bg === 'string') {
    slide.background = { path: bg };
  } else if (typeof bg === 'object') {
    slide.background = bg;
  }
  return true;
}

module.exports = { applyBackground };
