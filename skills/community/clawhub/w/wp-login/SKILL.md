# wp-login Skill

This skill automates WordPress login using the environment variables:
- `WP_URL`  - WordPress site URL
- `WP_USER` - Username
- `WP_PASSWORD` - Password

## Usage

The skill script will use these environment variables to perform a login to the WordPress site.

## Description

The skill should support:
- Automating the login process to the WordPress site
- Handling login success/failure

## Implementation

Implementation details can include using HTTP requests or browser automation to perform the login.

---

Below is an example script outline for the wp-login skill in Node.js:

```js
const axios = require('axios');
const qs = require('qs');

async function wpLogin() {
  const url = process.env.WP_URL;
  const user = process.env.WP_USER;
  const password = process.env.WP_PASSWORD;
  if (!url || !user || !password) {
    throw new Error('Missing WP_URL, WP_USER, or WP_PASSWORD environment variables');
  }

  // WordPress login endpoint
  const loginUrl = `${url.replace(/\/$/, '')}/wp-login.php`;

  // Prepare login form data
  const data = qs.stringify({
    log: user,
    pwd: password,
    wp-submit: 'Log In',
    redirect_to: `${url.replace(/\/$/, '')}/wp-admin/`,
    testcookie: 1
  });

  try {
    // Send login POST request
    const response = await axios.post(loginUrl, data, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      maxRedirects: 0,
      validateStatus: status => status === 302 // Expect redirect on success
    });

    if (response.status === 302) {
      console.log('Login successful');
      return true;
    } else {
      console.error('Login failed');
      return false;
    }
  } catch (err) {
    console.error('Error during login:', err.message);
    return false;
  }
}

module.exports = { wpLogin };
```