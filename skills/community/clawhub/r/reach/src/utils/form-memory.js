import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FORMS_DIR = path.join(__dirname, '..', '..', 'data', 'forms');

fs.mkdirSync(FORMS_DIR, { recursive: true });

/**
 * Form Memory — remembers form fields and values for auto-fill.
 *
 * When Reach fills a form, the fields and values are saved keyed by domain+path.
 * On next visit, known fields are pre-filled automatically.
 *
 * Storage: data/forms/{domain}_{path}.json
 */

/**
 * Save form data for a URL.
 *
 * @param {string} url - Page URL where the form was found
 * @param {Array<{ selector, name, value, type }>} fields - Form fields and their values
 * @returns {object} { saved, url, fieldCount }
 */
export function saveForm(url, fields) {
  if (!fields || fields.length === 0) return { saved: false, reason: 'no fields' };

  const key = urlToKey(url);
  const filepath = path.join(FORMS_DIR, `${key}.json`);

  // Load existing form memory for this page
  let existing = {};
  if (fs.existsSync(filepath)) {
    try {
      existing = JSON.parse(fs.readFileSync(filepath, 'utf-8'));
    } catch {}
  }

  // Merge new fields into existing
  const formData = {
    url,
    lastUpdated: new Date().toISOString(),
    fields: { ...existing.fields },
  };

  for (const field of fields) {
    const fieldKey = field.name || field.selector || field.label;
    if (!fieldKey || !field.value) continue;

    // Don't save passwords or sensitive fields in plain text
    if (isSensitiveField(field)) {
      formData.fields[fieldKey] = {
        selector: field.selector,
        name: field.name,
        type: field.type,
        label: field.label,
        sensitive: true,
        // Don't store the value
      };
    } else {
      formData.fields[fieldKey] = {
        selector: field.selector,
        name: field.name,
        value: field.value,
        type: field.type,
        label: field.label,
        lastUsed: new Date().toISOString(),
      };
    }
  }

  fs.writeFileSync(filepath, JSON.stringify(formData, null, 2));
  console.log(`[form-memory] Saved ${fields.length} fields for ${url}`);

  return {
    saved: true,
    url,
    fieldCount: Object.keys(formData.fields).length,
    file: filepath,
  };
}

/**
 * Recall form data for a URL.
 *
 * @param {string} url - Page URL to recall form data for
 * @returns {object|null} Saved form data or null if not found
 */
export function recallForm(url) {
  const key = urlToKey(url);
  const filepath = path.join(FORMS_DIR, `${key}.json`);

  if (!fs.existsSync(filepath)) return null;

  try {
    const data = JSON.parse(fs.readFileSync(filepath, 'utf-8'));
    return data;
  } catch {
    return null;
  }
}

/**
 * Get auto-fill suggestions for a page's form fields.
 *
 * @param {string} url - Current page URL
 * @param {Array<{ selector, name, type }>} currentFields - Current form fields on the page
 * @returns {Array<{ selector, name, value }>} Fields with values to auto-fill
 */
export function getAutoFillData(url, currentFields = []) {
  const formData = recallForm(url);
  if (!formData || !formData.fields) return [];

  const suggestions = [];

  for (const field of currentFields) {
    const fieldKey = field.name || field.selector || field.label;
    if (!fieldKey) continue;

    // Try exact match by name
    const saved = formData.fields[fieldKey] ||
                  formData.fields[field.name] ||
                  formData.fields[field.selector];

    if (saved && saved.value && !saved.sensitive) {
      suggestions.push({
        selector: field.selector || saved.selector,
        name: field.name || saved.name,
        value: saved.value,
        type: field.type || saved.type,
      });
    }
  }

  return suggestions;
}

/**
 * Auto-fill a Playwright page with remembered form data.
 *
 * @param {import('playwright').Page} page - Playwright page
 * @param {string} url - Page URL
 * @returns {object} { filled, fieldCount }
 */
export async function autoFillPage(page, url) {
  const formData = recallForm(url);
  if (!formData || !formData.fields) {
    return { filled: false, reason: 'no saved form data' };
  }

  let filledCount = 0;

  for (const [, field] of Object.entries(formData.fields)) {
    if (!field.value || field.sensitive) continue;

    const selector = field.selector || (field.name ? `[name="${field.name}"]` : null);
    if (!selector) continue;

    try {
      const el = await page.$(selector);
      if (el) {
        const visible = await el.isVisible().catch(() => false);
        if (visible) {
          const currentValue = await el.inputValue().catch(() => '');
          // Only fill if field is empty
          if (!currentValue) {
            await el.fill(field.value);
            filledCount++;
            console.log(`[form-memory] Auto-filled: ${field.name || selector} = ${field.value.substring(0, 20)}...`);
          }
        }
      }
    } catch {
      // Field not found or not fillable — skip
    }
  }

  return { filled: filledCount > 0, fieldCount: filledCount };
}

/**
 * Extract form fields from a Playwright page.
 *
 * @param {import('playwright').Page} page - Playwright page
 * @returns {Array<{ selector, name, value, type, label }>}
 */
export async function extractFormFields(page) {
  return await page.evaluate(() => {
    const fields = [];
    const inputs = document.querySelectorAll('input, select, textarea');

    for (const input of inputs) {
      const type = input.getAttribute('type') || input.tagName.toLowerCase();
      // Skip hidden, submit, button types
      if (['hidden', 'submit', 'button', 'reset', 'image'].includes(type)) continue;

      const style = window.getComputedStyle(input);
      if (style.display === 'none' || style.visibility === 'hidden') continue;

      const name = input.getAttribute('name') || '';
      const id = input.getAttribute('id') || '';
      const placeholder = input.getAttribute('placeholder') || '';

      // Find associated label
      let label = '';
      if (id) {
        const labelEl = document.querySelector(`label[for="${id}"]`);
        if (labelEl) label = labelEl.textContent.trim();
      }
      if (!label) {
        const parent = input.closest('label');
        if (parent) label = parent.textContent.trim().replace(input.value || '', '').trim();
      }

      let value = '';
      if (input.tagName.toLowerCase() === 'select') {
        value = input.options[input.selectedIndex]?.text || input.value;
      } else if (type === 'checkbox' || type === 'radio') {
        value = input.checked ? 'checked' : '';
      } else {
        value = input.value || '';
      }

      const selector = id ? `#${id}` : (name ? `[name="${name}"]` : null);

      fields.push({
        selector,
        name,
        value,
        type,
        label: label || placeholder || name || id,
      });
    }

    return fields;
  });
}

/**
 * Forget form data for a URL.
 */
export function forgetForm(url) {
  const key = urlToKey(url);
  const filepath = path.join(FORMS_DIR, `${key}.json`);
  if (fs.existsSync(filepath)) {
    fs.unlinkSync(filepath);
    return true;
  }
  return false;
}

/**
 * List all saved form memories.
 */
export function listForms() {
  if (!fs.existsSync(FORMS_DIR)) return [];

  return fs.readdirSync(FORMS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => {
      try {
        const data = JSON.parse(fs.readFileSync(path.join(FORMS_DIR, f), 'utf-8'));
        return {
          url: data.url,
          fieldCount: Object.keys(data.fields || {}).length,
          lastUpdated: data.lastUpdated,
        };
      } catch {
        return { file: f, error: 'parse error' };
      }
    });
}

// --- Helpers ---

function urlToKey(url) {
  try {
    const u = new URL(url);
    const domain = u.hostname.replace(/[^a-zA-Z0-9.-]/g, '_');
    const urlPath = u.pathname.replace(/[^a-zA-Z0-9_-]/g, '_').replace(/^_+|_+$/g, '') || 'index';
    return `${domain}_${urlPath}`;
  } catch {
    return url.replace(/[^a-zA-Z0-9_-]/g, '_').substring(0, 100);
  }
}

function isSensitiveField(field) {
  const name = (field.name || '').toLowerCase();
  const type = (field.type || '').toLowerCase();
  const label = (field.label || '').toLowerCase();

  if (type === 'password') return true;
  if (/password|passwd|secret|token|key|ssn|social.security/i.test(name)) return true;
  if (/password|secret|ssn/i.test(label)) return true;

  return false;
}

export default {
  saveForm,
  recallForm,
  getAutoFillData,
  autoFillPage,
  extractFormFields,
  forgetForm,
  listForms,
};
