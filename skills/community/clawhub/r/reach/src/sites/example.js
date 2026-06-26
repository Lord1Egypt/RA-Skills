/**
 * Example Site Skill Template
 * 
 * Copy this file and customize it for any website you need Reach to interact with.
 * Site skills teach Reach how to navigate specific platforms.
 * 
 * Usage:
 *   import { login, search } from './sites/my-site.js';
 *   await login(reach);
 *   const results = await search(reach, 'query');
 */

export const name = 'example';
export const domain = 'example.com';

/**
 * Login to the site
 */
export async function login(reach, credentials = {}) {
  const { email, password } = credentials;
  
  // Step 1: Navigate to login page
  await reach.authenticate(domain, 'login', {
    url: `https://${domain}/login`,
    email,
    password,
  });
}

/**
 * Search for something on the site
 */
export async function search(reach, query) {
  const content = await reach.fetch(`https://${domain}/search?q=${encodeURIComponent(query)}`, {
    format: 'markdown',
    javascript: true,
  });
  return content;
}

/**
 * Submit a form
 */
export async function submitForm(reach, url, fields) {
  await reach.act(url, 'submit', { fields });
}

/**
 * Read a specific page
 */
export async function readPage(reach, path) {
  return await reach.fetch(`https://${domain}${path}`, { format: 'markdown' });
}
