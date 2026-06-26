'use strict';

const PT_TO_INCH = 1 / 72;

function ptInch(pt) {
  if (typeof pt !== 'number' || !isFinite(pt)) return 0;
  return Math.round(pt * PT_TO_INCH * 1000) / 1000;
}

function pxInch(px) {
  if (typeof px !== 'number' || !isFinite(px)) return 0;
  return Math.round(px * (1 / 96) * 1000) / 1000;
}

function usableWidth(dims, spacingPt) {
  return dims.w - ptInch(spacingPt) * 2;
}

function leftEdge(dims, spacingPt) {
  return ptInch(spacingPt);
}

module.exports = { ptInch, pxInch, usableWidth, leftEdge, PT_TO_INCH };
