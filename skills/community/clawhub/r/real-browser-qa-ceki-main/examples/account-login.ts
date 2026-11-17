import { Browser, HumanActionDeclined, HumanActionTimeout } from '@ceki/sdk';

const br = new Browser({ token: 'YOUR_TOKEN' });
await br.connect();

const s = await br.openSession({
  mode: 'persona',
  domainHints: ['app.example.com'],
});

await s.navigate('https://app.example.com/login');

await s.injectCredentials('secret-abc-123', {
  username_selector: '#email',
  password_selector: '#password',
  submit_selector: '#login-btn',
});

try {
  const result = await s.requestHumanAction(
    '2fa',
    'Please enter the 2FA code from your authenticator app',
    120,
  );
  console.log(`2FA completed: ${result.status}`);
} catch (e) {
  if (e instanceof HumanActionDeclined) {
    console.log('Provider declined the 2FA request');
  } else if (e instanceof HumanActionTimeout) {
    console.log('Provider did not respond in time');
  } else {
    throw e;
  }
}

const page = await s.query('h1');
console.log(`Logged in. Page title: ${page.elements[0]?.textContent}`);

await s.close();
await br.close();
