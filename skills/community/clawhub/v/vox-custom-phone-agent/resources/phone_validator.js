'use strict';

function normalizePhone(input) {
  if (!input) return '';
  const value = String(input).trim();
  const hasLeadingPlus = value.startsWith('+');
  const digits = value.replace(/[^0-9]/g, '');
  if (hasLeadingPlus) return `+${digits}`;
  if (digits.startsWith('86') && digits.length === 13) return digits.slice(2);
  return digits;
}

function extractPhone(text) {
  if (!text) return '';
  const mobileMatch = String(text).match(/(?:\+?86[-\s]?)?1[3-9]\d[-\s]?\d{4}[-\s]?\d{4}/);
  if (mobileMatch) return normalizePhone(mobileMatch[0]);
  const intlMatch = String(text).match(/\+\d[\d\s-]{7,18}\d/);
  return intlMatch ? normalizePhone(intlMatch[0]) : '';
}

function isValidPhone(phone) {
  const normalized = normalizePhone(phone);
  if (/^1[3-9]\d{9}$/.test(normalized)) return true;
  if (/^\+[1-9]\d{7,18}$/.test(normalized)) return true;
  return false;
}

function maskPhone(phone) {
  const normalized = normalizePhone(phone);
  if (/^1[3-9]\d{9}$/.test(normalized)) {
    return `${normalized.slice(0, 3)}****${normalized.slice(-4)}`;
  }
  if (normalized.startsWith('+') && normalized.length > 8) {
    return `${normalized.slice(0, 4)}****${normalized.slice(-4)}`;
  }
  return normalized ? '****' : '';
}

module.exports = {
  extractPhone,
  isValidPhone,
  maskPhone,
  normalizePhone
};
