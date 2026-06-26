const stealthPlugin = require('puppeteer-extra-plugin-stealth');
const puppeteerExtra = require('puppeteer-extra');
puppeteerExtra.use(stealthPlugin());
const path = require('path');

async function logoutWordPress(page) {
  console.log('Attempting to find logout link...');
  const logoutLinkSelectors = ['#wp-admin-bar-logout a', '#wp-admin-bar-log-out a', '#wp-adminbar li#wp-admin-bar-logout a'];
  for (const selector of logoutLinkSelectors) {
    const logoutLink = await page.$(selector);
    if (logoutLink) {
      console.log('Clicking logout link:', selector);
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle0' }),
        logoutLink.click(),
      ]);
      console.log('Logged out successfully');
      return true;
    }
  }
  console.warn('Logout link not found');
  return false;
}

async function loginWordPress(originalPage, url, username, password) {
  console.log('Launching Puppeteer with persistent profile');

  const userDataDir = path.resolve('./puppeteer_user_data');

  const browser = await puppeteerExtra.launch({
    headless: true,
    userDataDir,
  });

  const page = await browser.newPage();

  console.log('Navigating to login page:', url);
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36');
  await page.setBypassCSP(true);
  await page.setViewport({ width: 1200, height: 800 });
  await page.goto(url, { waitUntil: 'networkidle0' });

  console.log('Attempting logout if already logged in');
  await logoutWordPress(page);

  for (let attempt = 0; attempt < 3; attempt++) {
    console.log(`Login attempt ${attempt + 1}`);

    try {
      await page.type('#user_login', username, { delay: 100 });
      await page.type('#user_pass', password, { delay: 100 });

      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle0' }),
        page.click('#wp-submit'),
      ]);

      const loginError = await page.$('.login .message, .login .error');
      if (loginError) {
        const errorMessage = await page.evaluate(el => el.textContent, loginError);
        console.error('Login error detected:', errorMessage.trim());
        await page.screenshot({ path: 'login-error.png' });
        console.log('Screenshot saved: login-error.png');
        return false;
      }

      const loggedIn = await page.$('#wp-admin-bar-my-account, #wpadminbar, #wpbody-content');
      if (loggedIn) {
        console.log('Login successful');
        return true;
      }

      console.log('Login elements not found on the page');
      await page.screenshot({ path: `login-failed-attempt-${attempt + 1}.png` });
      console.log(`Screenshot saved: login-failed-attempt-${attempt + 1}.png`);
    } catch (err) {
      console.error('Error during login attempt:', err);
      await page.screenshot({ path: `error-attempt-${attempt + 1}.png` });
      console.log(`Screenshot saved: error-attempt-${attempt + 1}.png`);
    }
  }

  console.error('All login attempts failed');
  await browser.close();
  return false;
}

module.exports = { loginWordPress };
