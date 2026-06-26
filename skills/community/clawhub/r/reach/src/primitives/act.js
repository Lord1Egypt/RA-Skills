import pool from '../browser.js';
import { saveForm, recallForm, autoFillPage, extractFormFields } from '../utils/form-memory.js';

/**
 * Web interaction primitive. Performs actions on web pages.
 * Includes error recovery — each action tries multiple strategies before giving up.
 *
 * @param {string} url - URL to act on
 * @param {string} action - 'click' | 'type' | 'submit' | 'select' | 'scroll'
 * @param {object} params - Action parameters
 * @param {string} params.selector - CSS selector
 * @param {string} params.text - Text to match (for click) or type (for type)
 * @param {object} params.data - Form data (for submit)
 * @param {string} params.value - Value to select (for select)
 * @param {string} params.direction - 'up' | 'down' (for scroll)
 * @param {string} params.session - Session/cookie domain to use
 * @returns {object} { success, action, result, url }
 */
export async function act(url, action, params = {}) {
  const domain = pool.getDomain(url);
  const page = await pool.getPage(params.session || domain);

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    let result;

    switch (action) {
      case 'click':
        result = await doClick(page, params);
        break;
      case 'type':
        result = await doType(page, params);
        break;
      case 'submit':
        result = await doSubmit(page, params, url);
        break;
      case 'select':
        result = await doSelect(page, params);
        break;
      case 'scroll':
        result = await doScroll(page, params);
        break;
      default:
        throw new Error(`Unknown action: ${action}`);
    }

    // Save cookies after interaction
    await pool.saveCookies(domain);

    return { success: true, action, result, url };
  } catch (e) {
    return { success: false, action, error: e.message, url };
  } finally {
    await page.close();
  }
}

// --- Click with error recovery ---

async function doClick(page, params) {
  const { selector, text } = params;
  const errors = [];

  // Strategy 1: Click by CSS selector
  if (selector) {
    try {
      await page.click(selector, { timeout: 5000 });
      return { clicked: selector, strategy: 'selector' };
    } catch (e) {
      errors.push(`selector "${selector}": ${e.message}`);
    }
  }

  // Strategy 2: Click by text content
  if (text) {
    try {
      await page.locator(`text=${text}`).filter({ visible: true }).first().click({ timeout: 5000 });
      return { clicked: `text="${text}"`, strategy: 'text' };
    } catch (e) {
      errors.push(`text "${text}": ${e.message}`);
    }
  }

  // Strategy 3: Click by role (button, link)
  const target = text || selector;
  if (target) {
    for (const role of ['button', 'link', 'menuitem', 'tab', 'option']) {
      try {
        await page.getByRole(role, { name: target }).first().click({ timeout: 3000 });
        return { clicked: `role=${role} name="${target}"`, strategy: 'role' };
      } catch {
        // Continue to next role
      }
    }
    errors.push(`role-based: no matching role for "${target}"`);
  }

  // Strategy 4: Click by aria-label
  if (target) {
    try {
      await page.locator(`[aria-label="${target}"], [aria-label*="${target}" i]`).first().click({ timeout: 3000 });
      return { clicked: `aria-label="${target}"`, strategy: 'aria-label' };
    } catch (e) {
      errors.push(`aria-label "${target}": ${e.message}`);
    }
  }

  // Strategy 5: Click by coordinates (find element position via DOM)
  if (target) {
    try {
      const coords = await findElementCoordinates(page, target);
      if (coords) {
        await page.mouse.click(coords.x, coords.y);
        return { clicked: `coordinates (${coords.x}, ${coords.y})`, strategy: 'coordinates', target };
      }
    } catch (e) {
      errors.push(`coordinates: ${e.message}`);
    }
  }

  if (!selector && !text) {
    throw new Error('click requires selector or text');
  }

  throw new Error(`Click failed after all strategies. Errors: ${errors.join('; ')}`);
}

// --- Type with error recovery ---

async function doType(page, params) {
  const { selector, text, label } = params;
  const errors = [];

  if (!text) throw new Error('type requires text');

  // Strategy 1: Fill by CSS selector
  if (selector) {
    try {
      await page.fill(selector, text, { timeout: 5000 });
      return { typed: text, into: selector, strategy: 'selector' };
    } catch (e) {
      errors.push(`selector "${selector}": ${e.message}`);
    }
  }

  // Strategy 2: Fill by label text
  if (label || selector) {
    const labelText = label || selector;
    try {
      await page.getByLabel(labelText).first().fill(text, { timeout: 3000 });
      return { typed: text, into: `label="${labelText}"`, strategy: 'label' };
    } catch (e) {
      errors.push(`label "${labelText}": ${e.message}`);
    }
  }

  // Strategy 3: Fill by placeholder
  if (label || selector) {
    const placeholderText = label || selector;
    try {
      await page.getByPlaceholder(placeholderText).first().fill(text, { timeout: 3000 });
      return { typed: text, into: `placeholder="${placeholderText}"`, strategy: 'placeholder' };
    } catch (e) {
      errors.push(`placeholder "${placeholderText}": ${e.message}`);
    }
  }

  // Strategy 4: Try common input selectors
  const commonSelectors = [
    'input:focus',
    'input[type="text"]',
    'input[type="search"]',
    'textarea',
    'input:not([type="hidden"]):not([type="submit"])',
  ];

  for (const sel of commonSelectors) {
    try {
      const el = await page.$(sel);
      if (el) {
        await el.fill(text, { timeout: 3000 });
        return { typed: text, into: sel, strategy: 'common-selector' };
      }
    } catch {
      // Continue
    }
  }
  errors.push('common selectors: no matching input found');

  // Strategy 5: Type with keyboard events (last resort)
  try {
    // Focus the first visible input and type
    await page.evaluate(() => {
      const inputs = document.querySelectorAll('input:not([type="hidden"]):not([type="submit"]), textarea');
      for (const input of inputs) {
        const style = window.getComputedStyle(input);
        if (style.display !== 'none' && style.visibility !== 'hidden') {
          input.focus();
          return true;
        }
      }
      return false;
    });
    await page.keyboard.type(text, { delay: 50 });
    return { typed: text, into: 'keyboard-focus', strategy: 'keyboard' };
  } catch (e) {
    errors.push(`keyboard: ${e.message}`);
  }

  throw new Error(`Type failed after all strategies. Errors: ${errors.join('; ')}`);
}

// --- Submit with form memory ---

async function doSubmit(page, params, url) {
  const { data, selector } = params;

  // Check form memory for auto-fill data
  if (url) {
    try {
      const autoFillResult = await autoFillPage(page, url);
      if (autoFillResult.filled) {
        console.log(`[act] Auto-filled ${autoFillResult.fieldCount} fields from memory`);
      }
    } catch {
      // Form memory auto-fill is best-effort
    }
  }

  if (data && typeof data === 'object') {
    // Fill form fields by name or label
    for (const [key, value] of Object.entries(data)) {
      const errors = [];

      // Try by name attribute
      try {
        const byName = await page.$(`[name="${key}"]`);
        if (byName) {
          const tagName = await byName.evaluate(el => el.tagName.toLowerCase());
          if (tagName === 'select') {
            await byName.selectOption(value);
          } else {
            await byName.fill(String(value));
          }
          continue;
        }
      } catch (e) {
        errors.push(`name: ${e.message}`);
      }

      // Try by label
      try {
        await page.getByLabel(key).first().fill(String(value), { timeout: 3000 });
        continue;
      } catch (e) {
        errors.push(`label: ${e.message}`);
      }

      // Try by placeholder
      try {
        await page.getByPlaceholder(key).first().fill(String(value), { timeout: 3000 });
        continue;
      } catch (e) {
        errors.push(`placeholder: ${e.message}`);
      }

      // Try adjacent label selector (original approach)
      try {
        const byLabel = await page.$(`label:has-text("${key}") + input, label:has-text("${key}") + select, label:has-text("${key}") + textarea`);
        if (byLabel) {
          await byLabel.fill(String(value));
          continue;
        }
      } catch {}

      console.log(`[act] Could not find field for: ${key} (tried: ${errors.join(', ')})`);
    }
  }

  // Click submit button with error recovery
  const submitSelectors = [
    selector,
    'button[type="submit"]',
    'input[type="submit"]',
    'button:has-text("Submit")',
    'button:has-text("Send")',
    'button:has-text("Save")',
    'button:has-text("Continue")',
    'button:has-text("Next")',
  ].filter(Boolean);

  let submitted = false;
  for (const sel of submitSelectors) {
    try {
      await page.locator(sel).filter({ visible: true }).first().click({ timeout: 3000 });
      submitted = true;
      break;
    } catch {
      // Continue to next selector
    }
  }

  if (!submitted) {
    // Last resort: press Enter
    await page.keyboard.press('Enter');
  }

  // Wait for navigation or response
  await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});

  // Save form data to memory
  if (url && data) {
    try {
      const fields = Object.entries(data).map(([key, value]) => ({
        name: key,
        value: String(value),
        selector: `[name="${key}"]`,
      }));
      saveForm(url, fields);
    } catch {
      // Best-effort
    }
  }

  const pageText = await page.innerText('body').catch(() => '');
  return { submitted: true, pagePreview: pageText.slice(0, 500) };
}

// --- Select with error recovery ---

async function doSelect(page, params) {
  const { selector, value, text } = params;
  const errors = [];

  // Strategy 1: Select by CSS selector + value
  if (selector && value) {
    try {
      await page.selectOption(selector, value, { timeout: 5000 });
      return { selected: value, from: selector, strategy: 'selector-value' };
    } catch (e) {
      errors.push(`selector+value: ${e.message}`);
    }
  }

  // Strategy 2: Select by CSS selector + label text
  if (selector && text) {
    try {
      await page.selectOption(selector, { label: text }, { timeout: 5000 });
      return { selected: text, from: selector, strategy: 'selector-label' };
    } catch (e) {
      errors.push(`selector+label: ${e.message}`);
    }
  }

  // Strategy 3: Click custom dropdown option by role
  if (text) {
    try {
      await page.getByRole('option', { name: text }).first().click({ timeout: 3000 });
      return { selected: text, strategy: 'role-option' };
    } catch (e) {
      errors.push(`role-option: ${e.message}`);
    }
  }

  // Strategy 4: Click listbox item
  if (text) {
    try {
      await page.locator(`[role="listbox"] >> text=${text}`).first().click({ timeout: 3000 });
      return { selected: text, strategy: 'listbox' };
    } catch (e) {
      errors.push(`listbox: ${e.message}`);
    }
  }

  if (!selector && !text && !value) {
    throw new Error('select requires selector+value or text');
  }

  throw new Error(`Select failed after all strategies. Errors: ${errors.join('; ')}`);
}

async function doScroll(page, params) {
  const { direction = 'down', amount = 500 } = params;
  const delta = direction === 'up' ? -amount : amount;
  await page.mouse.wheel(0, delta);
  await page.waitForTimeout(500);
  return { scrolled: direction, amount };
}

/**
 * Find element coordinates by searching visible text/attributes.
 * Used as last-resort click strategy.
 */
async function findElementCoordinates(page, target) {
  return await page.evaluate((searchText) => {
    const allElements = document.querySelectorAll('*');
    for (const el of allElements) {
      const text = el.textContent?.trim();
      const ariaLabel = el.getAttribute('aria-label');
      const title = el.getAttribute('title');

      if (
        (text && text === searchText) ||
        (ariaLabel && ariaLabel.includes(searchText)) ||
        (title && title.includes(searchText))
      ) {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          return {
            x: Math.round(rect.x + rect.width / 2),
            y: Math.round(rect.y + rect.height / 2),
          };
        }
      }
    }
    return null;
  }, target);
}
