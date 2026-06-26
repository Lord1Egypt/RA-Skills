'use strict';

const BRAND_COLOR_FIELDS = [
  ['primary', 'accent'],
  ['colors.primary', 'accent'],
];

const BRAND_SECONDARY_FIELDS = [
  ['secondary', 'secondary'],
  ['colors.secondary', 'secondary'],
];

function getBrandField(spec, fields) {
  if (!spec) return undefined;
  for (const field of fields) {
    const pathStr = Array.isArray(field) ? field[0] : field;
    const parts = pathStr.split('.');
    let cur = spec;
    for (const p of parts) {
      if (cur && typeof cur === 'object' && p in cur) {
        cur = cur[p];
      } else {
        cur = undefined;
        break;
      }
    }
    if (cur) return cur;
  }
  return undefined;
}

function isHexColor(s) {
  if (typeof s !== 'string') return false;
  return /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/.test(s.trim());
}

function applyBrandOverride(theme, brandSpec) {
  if (!brandSpec || typeof brandSpec !== 'object') return theme;

  const next = { ...theme };

  const primary = getBrandField(brandSpec, BRAND_COLOR_FIELDS);
  if (isHexColor(primary)) {
    next.accent = primary.trim();
  }

  const secondary = getBrandField(brandSpec, BRAND_SECONDARY_FIELDS);
  if (isHexColor(secondary)) {
    next.secondary = secondary.trim();
  }

  return next;
}

module.exports = { applyBrandOverride, isHexColor, getBrandField };
