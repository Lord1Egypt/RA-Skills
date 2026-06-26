// Shared footer for all Kaleidoscope pages
// Include with: <div id="kscope-footer"></div><script src="/demo/footer.js"></script>
(function() {
  var container = document.getElementById('kscope-footer');
  if (!container) return;

  var mobile = navigator.maxTouchPoints > 0 && window.innerWidth < 768;

  // Desktop: fixed at bottom. Mobile: in page flow (below fold).
  if (mobile) {
    container.style.cssText = 'background:#FFFDF5;padding:16px 0;';
  } else {
    container.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#FFFDF5;padding:16px 0;';
  }

  var inner = document.createElement('div');
  inner.style.cssText = 'max-width:980px;margin:0 auto;padding:0 24px;border-top:1px solid rgba(0,0,0,0.06);padding-top:16px;text-align:left;font-size:13px;color:#a8a4a0;line-height:1.6;';

  // On mobile, copyright and links on separate lines (like Apple)
  if (mobile) {
    inner.innerHTML = '<p style="margin:0;">WIP Computer, Inc.</p>'
      + '<p style="margin:2px 0 0;">Learning Dreaming Machines</p>'
      + '<p style="margin:8px 0 0;">Copyright &copy; 2026 WIP Computer, Inc. All rights reserved.</p>'
      + '<p style="margin:4px 0 0;">'
      + '<a href="/legal/privacy/en-ww/" style="color:#a8a4a0;text-decoration:none;">Privacy Policy</a> &nbsp;|&nbsp; '
      + '<a href="/legal/internet-services/terms/site.html" style="color:#a8a4a0;text-decoration:none;">Terms of Use</a></p>'
      + '<p style="margin:4px 0 0;">'
      + '<a href="/agent.txt" style="color:#a8a4a0;text-decoration:none;">Are you an AI Agent?</a></p>'
      + '<p style="margin:4px 0 0;">Made in California.</p>';
  } else {
    inner.innerHTML = '<p style="margin:0;">WIP Computer, Inc.</p>'
      + '<p style="margin:2px 0 0;">Learning Dreaming Machines</p>'
      + '<p style="margin:8px 0 0;">Copyright &copy; 2026 WIP Computer, Inc. All rights reserved. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
      + '<a href="/legal/privacy/en-ww/" style="color:#a8a4a0;text-decoration:none;">Privacy Policy</a> &nbsp;|&nbsp; '
      + '<a href="/legal/internet-services/terms/site.html" style="color:#a8a4a0;text-decoration:none;">Terms of Use</a></p>'
      + '<p style="margin:4px 0 0;">'
      + '<a href="/agent.txt" style="color:#a8a4a0;text-decoration:none;">Are you an AI Agent?</a> &nbsp;|&nbsp; '
      + '<a id="localPasskeysToggle" onclick="toggleLocalPasskeys()" style="color:#a8a4a0;text-decoration:none;cursor:pointer;display:inline-flex;align-items:center;gap:4px;vertical-align:middle;">'
      + '<span id="passkeys-dot" style="display:inline-block;width:8px;height:8px;border-radius:50%;"></span> '
      + '<span id="passkeys-label">Local passkeys off</span></a></p>'
      + '<p style="margin:4px 0 0;">Made in California.</p>';
  }

  container.appendChild(inner);

  // Local passkeys toggle
  if (!window.isLocalPasskeysOn) {
    window.isLocalPasskeysOn = function() { return localStorage.getItem('localPasskeys') === 'on'; };
  }
  if (!window.toggleLocalPasskeys) {
    window.toggleLocalPasskeys = function() {
      var on = isLocalPasskeysOn();
      localStorage.setItem('localPasskeys', on ? 'off' : 'on');
      updatePasskeysDot();
    };
  }
  if (!window.updatePasskeysDot) {
    window.updatePasskeysDot = function() {
      var dot = document.getElementById('passkeys-dot');
      var label = document.getElementById('passkeys-label');
      if (!dot) return;
      if (isLocalPasskeysOn()) {
        dot.style.background = '#2E7D32';
        dot.style.opacity = '1';
        if (label) label.textContent = 'Local passkeys on';
      } else {
        dot.style.background = '#D32F2F';
        dot.style.opacity = '0.4';
        if (label) label.textContent = 'Local passkeys off';
      }
    };
  }
  updatePasskeysDot();
})();
