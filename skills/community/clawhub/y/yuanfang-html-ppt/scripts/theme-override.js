'use strict';

function applyThemeOverride(theme, slideSpec) {
  const next = { ...theme };
  const override = slideSpec.themeOverride;
  if (!override || typeof override !== 'object') return next;
  for (const [key, value] of Object.entries(override)) {
    if (value !== undefined && value !== null) {
      next[key] = value;
    }
  }
  return next;
}

module.exports = { applyThemeOverride };
