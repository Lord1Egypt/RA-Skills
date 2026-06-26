// Shared Kaleidoscope JS: WebAuthn helpers, sprite loading, status display
// Extracted verbatim from demo/index.html. DO NOT MODIFY separately.
// If the demo changes, re-extract.

// ── Base64url helpers ──
function b64urlToBytes(b64) {
  var bin = atob(b64.replace(/-/g, '+').replace(/_/g, '/') + '=='.slice(0, (4 - b64.length % 4) % 4));
  return Uint8Array.from(bin, function(c) { return c.charCodeAt(0); });
}
function bytesToB64url(buf) {
  return btoa(String.fromCharCode.apply(null, new Uint8Array(buf)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

// ── Status display (matches demo's .login-status CSS) ──
function setStatus(msg, type) {
  var el = document.getElementById('loginStatus');
  el.textContent = msg;
  el.className = 'login-status show ' + type;
}

function clearLoginStatus() {
  var el = document.getElementById('loginStatus');
  el.style.transition = 'opacity 0.5s';
  el.style.opacity = '0';
  setTimeout(function() { el.className = 'login-status'; el.style.transition = ''; el.style.opacity = ''; }, 500);
}

// ── Random kaleidoscope icon from sprite sheet ──
// sprites.png is 8 columns x 3 rows = 24 icons
var SPRITE_COLS = 8;
var SPRITE_ROWS = 3;
var SPRITE_TOTAL = SPRITE_COLS * SPRITE_ROWS;

function makeIconHTML(size, blue) {
  var idx = Math.floor(Math.random() * SPRITE_TOTAL);
  var col = idx % SPRITE_COLS;
  var row = Math.floor(idx / SPRITE_COLS);
  var bgPosX = (col / (SPRITE_COLS - 1)) * 100;
  var bgPosY = (row / (SPRITE_ROWS - 1)) * 100;
  if (blue) {
    return '<div style="width:' + size + 'px;height:' + size + 'px;overflow:hidden;background:var(--accent);-webkit-mask-image:url(/demo/sprites.png);mask-image:url(/demo/sprites.png);-webkit-mask-size:' + (SPRITE_COLS * 100) + '% ' + (SPRITE_ROWS * 100) + '%;mask-size:' + (SPRITE_COLS * 100) + '% ' + (SPRITE_ROWS * 100) + '%;-webkit-mask-position:' + bgPosX + '% ' + bgPosY + '%;mask-position:' + bgPosX + '% ' + bgPosY + '%;"></div>';
  }
  return '<div style="width:' + size + 'px;height:' + size + 'px;overflow:hidden;"><div style="width:100%;height:100%;background:url(/demo/sprites.png);background-size:' + (SPRITE_COLS * 100) + '% ' + (SPRITE_ROWS * 100) + '%;background-position:' + bgPosX + '% ' + bgPosY + '%;"></div></div>';
}

function initLoginIcon(elementId, size) {
  var el = document.getElementById(elementId);
  if (!el) return;
  el.innerHTML = makeIconHTML(size || 34, false);
  // Rotate every 3s
  var rotateIdx = Math.floor(Math.random() * SPRITE_TOTAL);
  setInterval(function() {
    rotateIdx = (rotateIdx + 1) % SPRITE_TOTAL;
    var col = rotateIdx % SPRITE_COLS;
    var row = Math.floor(rotateIdx / SPRITE_COLS);
    var bgPosX = (col / (SPRITE_COLS - 1)) * 100;
    var bgPosY = (row / (SPRITE_ROWS - 1)) * 100;
    el.innerHTML = makeIconHTML(size || 34, false);
  }, 3000);
}

// ── WebAuthn: Create Account ──
async function doCreateAccount(handleInputId, onSuccess) {
  var username = (document.getElementById(handleInputId).value || '').trim().replace(/^@/, '').toLowerCase().replace(/[^a-z0-9\-]/g, '').slice(0, 30);
  var btn = document.getElementById('createBtn');
  btn.disabled = true;
  setStatus('Preparing...', 'loading');

  try {
    var optRes = await fetch('/webauthn/register-options', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agentName: username || undefined }),
    });
    var optData = await optRes.json();
    var challengeId = optData.challengeId;
    var options = optData.options;
    if (!options) throw new Error('Server returned no options');

    options.challenge = b64urlToBytes(options.challenge);
    options.user.id = b64urlToBytes(options.user.id);
    if (options.excludeCredentials) {
      options.excludeCredentials = options.excludeCredentials.map(function(c) { return Object.assign({}, c, { id: b64urlToBytes(c.id) }); });
    }

    setStatus('Waiting for biometric...', 'loading');
    var credential = await navigator.credentials.create({ publicKey: options });

    var reqBody = {
      challengeId: challengeId,
      credential: {
        id: credential.id,
        rawId: bytesToB64url(credential.rawId),
        type: credential.type,
        response: {
          attestationObject: bytesToB64url(credential.response.attestationObject),
          clientDataJSON: bytesToB64url(credential.response.clientDataJSON),
          transports: credential.response.getTransports ? credential.response.getTransports() : [],
        },
      },
    };

    setStatus('Verifying...', 'loading');
    var verRes = await fetch('/webauthn/register-verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reqBody),
    });
    var result = await verRes.json();

    if (result.success) {
      if (onSuccess) onSuccess(username || result.agentId, result);
    } else {
      setStatus(result.error || 'Registration failed', 'error');
      btn.disabled = false;
    }
  } catch (err) {
    if (err.name === 'NotAllowedError') {
      setStatus('Cancelled. Try again when ready.', 'error');
    } else {
      setStatus('Error: ' + err.message, 'error');
    }
    btn.disabled = false;
  }
}

// ── WebAuthn: Sign In ──
async function doSignIn(onSuccess) {
  var signInBtn = document.getElementById('signInBtn');
  var createBtn = document.getElementById('createBtn');
  if (signInBtn) signInBtn.style.pointerEvents = 'none';
  if (createBtn) createBtn.disabled = true;
  setStatus('Preparing...', 'loading');

  try {
    var optRes = await fetch('/webauthn/auth-options', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    });
    var optData = await optRes.json();
    var challengeId = optData.challengeId;
    var options = optData.options;
    if (!options) throw new Error('Server returned no options');

    options.challenge = b64urlToBytes(options.challenge);
    if (options.allowCredentials) {
      options.allowCredentials = options.allowCredentials.map(function(c) { return Object.assign({}, c, { id: b64urlToBytes(c.id) }); });
    }

    setStatus('Waiting for biometric...', 'loading');
    var assertion = await navigator.credentials.get({ publicKey: options });

    var reqBody = {
      challengeId: challengeId,
      credential: {
        id: assertion.id, rawId: bytesToB64url(assertion.rawId), type: assertion.type,
        response: {
          authenticatorData: bytesToB64url(assertion.response.authenticatorData),
          clientDataJSON: bytesToB64url(assertion.response.clientDataJSON),
          signature: bytesToB64url(assertion.response.signature),
          userHandle: assertion.response.userHandle ? bytesToB64url(assertion.response.userHandle) : null,
        },
      },
    };

    setStatus('Verifying...', 'loading');
    var verRes = await fetch('/webauthn/auth-verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reqBody),
    });
    var result = await verRes.json();

    if (result.success) {
      if (onSuccess) onSuccess(result.agentId, result);
    } else {
      setStatus(result.error || 'Authentication failed', 'error');
      if (signInBtn) signInBtn.style.pointerEvents = 'auto';
      if (createBtn) createBtn.disabled = false;
    }
  } catch (err) {
    if (err.name === 'NotAllowedError') {
      setStatus('Cancelled. Try again when ready.', 'error');
    } else {
      setStatus('Error: ' + err.message, 'error');
    }
    if (signInBtn) signInBtn.style.pointerEvents = 'auto';
    if (createBtn) createBtn.disabled = false;
  }
}
