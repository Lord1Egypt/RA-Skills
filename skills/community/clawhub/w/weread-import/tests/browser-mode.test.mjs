import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeCookieSource, isBrowserCookieMode, isManagedBrowserMode, isLiveBrowserMode } from '../src/browser-mode.mjs';

describe('normalizeCookieSource', () => {
  it('maps browser to browser-managed for backward compatibility', () => {
    assert.equal(normalizeCookieSource('browser'), 'browser-managed');
  });

  it('keeps explicit browser-live and browser-managed values', () => {
    assert.equal(normalizeCookieSource('browser-live'), 'browser-live');
    assert.equal(normalizeCookieSource('browser-managed'), 'browser-managed');
  });

  it('falls back to manual for unknown values', () => {
    assert.equal(normalizeCookieSource('manual'), 'manual');
    assert.equal(normalizeCookieSource('unknown'), 'manual');
  });
});

describe('browser mode predicates', () => {
  it('distinguishes browser and manual modes', () => {
    assert.equal(isBrowserCookieMode('manual'), false);
    assert.equal(isBrowserCookieMode('browser'), true);
    assert.equal(isBrowserCookieMode('browser-live'), true);
  });

  it('distinguishes managed and live browser modes', () => {
    assert.equal(isManagedBrowserMode('browser'), true);
    assert.equal(isManagedBrowserMode('browser-managed'), true);
    assert.equal(isManagedBrowserMode('browser-live'), false);
    assert.equal(isLiveBrowserMode('browser-live'), true);
    assert.equal(isLiveBrowserMode('browser-managed'), false);
  });
});
