import pool from '../browser.js';

/**
 * Vision primitive. Takes a screenshot and extracts accessibility/structural
 * information from a page for external visual reasoning.
 *
 * @param {import('playwright').Page|string} pageOrUrl - Playwright page instance or URL string
 * @param {string} [question] - Optional context about what to look for (for future AI integration)
 * @returns {object} { screenshot, description, url, elements, title }
 */
export async function see(pageOrUrl, question) {
  let page;
  let ownPage = false;

  if (typeof pageOrUrl === 'string') {
    // URL string — open a new page
    const domain = pool.getDomain(pageOrUrl);
    page = await pool.getPage(domain);
    ownPage = true;

    try {
      await page.goto(pageOrUrl, { waitUntil: 'networkidle', timeout: 30000 });
    } catch (e) {
      // Still try to capture what loaded
      console.log(`[see] Navigation warning: ${e.message}`);
    }
  } else {
    page = pageOrUrl;
  }

  try {
    const url = page.url();
    const title = await page.title().catch(() => '');

    // 1. Take screenshot
    const screenshotPath = await pool.screenshot(page, sanitize(url));

    // 2. Get accessibility tree (text representation of the page)
    const accessibilityTree = await getAccessibilitySnapshot(page);

    // 3. Extract interactive elements
    const elements = await extractInteractiveElements(page);

    // 4. Get visible text content
    const visibleText = await page.innerText('body').catch(() => '');
    const textPreview = visibleText.trim().substring(0, 2000);

    const result = {
      screenshot: screenshotPath,
      url,
      title,
      question: question || null,
      description: accessibilityTree,
      elements,
      textPreview,
    };

    console.log(`[see] Captured: ${url}`);
    console.log(`[see]   Screenshot: ${screenshotPath}`);
    console.log(`[see]   Elements: ${elements.length} interactive`);
    console.log(`[see]   Text: ${textPreview.length} chars`);

    return result;
  } finally {
    if (ownPage) {
      await page.close();
    }
  }
}

/**
 * Get the accessibility tree as a text description.
 * Falls back to a simulated tree if Playwright's accessibility API isn't available.
 */
async function getAccessibilitySnapshot(page) {
  try {
    const snapshot = await page.accessibility.snapshot();
    if (snapshot) {
      return formatAccessibilityNode(snapshot, 0);
    }
  } catch {
    // Accessibility API may not be available in all configs
  }

  // Fallback: build a structural description from the DOM
  return await page.evaluate(() => {
    const lines = [];

    function walk(el, depth = 0) {
      if (!el || depth > 6) return;

      const tag = el.tagName?.toLowerCase();
      if (!tag) return;

      // Skip invisible elements
      const style = window.getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden') return;

      // Skip non-content tags
      if (['script', 'style', 'noscript', 'svg', 'path'].includes(tag)) return;

      const indent = '  '.repeat(depth);
      const role = el.getAttribute('role') || '';
      const ariaLabel = el.getAttribute('aria-label') || '';
      const text = el.childNodes.length === 1 && el.childNodes[0].nodeType === 3
        ? el.childNodes[0].textContent?.trim().substring(0, 80) : '';

      let desc = `${indent}${tag}`;
      if (role) desc += `[role=${role}]`;
      if (ariaLabel) desc += `[aria-label="${ariaLabel}"]`;
      if (el.id) desc += `#${el.id}`;
      if (tag === 'a' && el.href) desc += ` → ${el.href}`;
      if (tag === 'img' && el.alt) desc += ` alt="${el.alt}"`;
      if (tag === 'input') desc += ` type=${el.type || 'text'} name=${el.name || '?'}`;
      if (tag === 'button') desc += ` "${el.textContent?.trim().substring(0, 40)}"`;
      if (text) desc += ` "${text}"`;

      // Only log meaningful elements
      if (['h1','h2','h3','h4','h5','h6','p','a','button','input','select','textarea',
           'img','form','nav','main','header','footer','section','article','table',
           'li','label','dialog'].includes(tag) || role || ariaLabel) {
        lines.push(desc);
      }

      for (const child of el.children) {
        walk(child, depth + 1);
      }
    }

    walk(document.body);
    return lines.join('\n');
  });
}

/**
 * Format a Playwright accessibility snapshot node into readable text.
 */
function formatAccessibilityNode(node, depth) {
  if (!node) return '';

  const indent = '  '.repeat(depth);
  let line = `${indent}${node.role || 'unknown'}`;

  if (node.name) line += ` "${node.name}"`;
  if (node.value) line += ` value="${node.value}"`;
  if (node.checked !== undefined) line += ` checked=${node.checked}`;
  if (node.pressed !== undefined) line += ` pressed=${node.pressed}`;
  if (node.level !== undefined) line += ` level=${node.level}`;

  const lines = [line];

  if (node.children) {
    for (const child of node.children) {
      lines.push(formatAccessibilityNode(child, depth + 1));
    }
  }

  return lines.join('\n');
}

/**
 * Extract all interactive elements from the page with their positions and labels.
 */
async function extractInteractiveElements(page) {
  return await page.evaluate(() => {
    const elements = [];
    const selectors = 'a, button, input, select, textarea, [role="button"], [role="link"], [role="tab"], [onclick]';

    for (const el of document.querySelectorAll(selectors)) {
      const rect = el.getBoundingClientRect();

      // Skip invisible or off-screen elements
      if (rect.width === 0 || rect.height === 0) continue;
      if (rect.bottom < 0 || rect.top > window.innerHeight) continue;

      const style = window.getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') continue;

      const tag = el.tagName.toLowerCase();
      const type = el.getAttribute('type') || '';
      const text = (el.textContent || '').trim().substring(0, 60);
      const ariaLabel = el.getAttribute('aria-label') || '';
      const placeholder = el.getAttribute('placeholder') || '';
      const href = el.getAttribute('href') || '';
      const name = el.getAttribute('name') || '';

      elements.push({
        tag,
        type,
        text: text || ariaLabel || placeholder || name || '(unlabeled)',
        href: tag === 'a' ? href : undefined,
        name: name || undefined,
        position: {
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
        },
      });
    }

    return elements;
  });
}

/**
 * Sanitize a URL for use as a filename.
 */
function sanitize(url) {
  try {
    return new URL(url).hostname.replace(/[^a-zA-Z0-9.-]/g, '_');
  } catch {
    return url.replace(/[^a-zA-Z0-9.-]/g, '_').substring(0, 50);
  }
}
