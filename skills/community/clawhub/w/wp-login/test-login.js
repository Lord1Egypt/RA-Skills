require('dotenv').config({ path: '/Users/denis/.openclaw/openclaw.json' });
const { wpLogin } = require('./index');

(async () => {
  const success = await wpLogin();
  if (success) {
    console.log('Test login succeeded');
    process.exit(0);
  } else {
    console.error('Test login failed');
    process.exit(1);
  }
})();
