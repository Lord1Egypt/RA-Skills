const { chromium } = require('playwright');

async function wpLogin() {
  const url = process.env.WP_URL;
  const user = process.env.WP_USER;
  const password = process.env.WP_PASSWORD;
  const loginUrl = url.replace(/\/$/, '') + '/wp-login.php';

  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  
  const context = await browser.newContext({
  userAgent: '...',
  viewport: { width: 1280, height: 800 },
  locale: 'fr-FR',
  timezoneId: 'Europe/Paris',
  permissions: ['geolocation'],
  reducedMotion: 'no-preference',
  javaScriptEnabled: true,
  bypassCSP: true,  // parfois utile
  ignoreHTTPSErrors: true,  // si certificat foireux
});
  const page = await context.newPage();

  try {
    // Pré-pose le test cookie (comme avant)
    await context.addCookies([{
      name: 'wordpress_test_cookie',
      value: 'WP Cookie check',
      url: new URL(loginUrl).origin,
      secure: loginUrl.startsWith('https'),
      sameSite: 'Lax'
    }]);

    await page.goto(loginUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('#user_login', { state: 'visible' });

    await page.screenshot({ path: 'playwright_initial.png' });

    await page.fill('#user_login', user);
    await page.fill('#user_pass', password);

    await Promise.all([
      page.click('#wp-submit'),
      page.waitForNavigation({ waitUntil: 'domcontentloaded' })
    ]);

    await page.screenshot({ path: 'playwright_after_submit.png' });

    if (page.url().includes('/wp-admin/')) {
      console.log('Login réussi avec Playwright !');
      // Sauvegarde storage state pour réutiliser
      await context.storageState({ path: 'wp-state.json' });
      return true;
    } else {
      console.error('Échec - URL actuelle:', page.url());
      return false;
    }
  } catch (err) {
    console.error('Erreur Playwright:', err);
    return false;
  } finally {
    await browser.close();
  }
}

module.exports = { wpLogin };
