(function() {
  function isLocalPasskeysOn() {
    return localStorage.getItem('localPasskeys') === 'on';
  }

  function updatePasskeysDot() {
    var button = document.querySelector('[data-passkeys]');
    var label = document.querySelector('[data-passkeys-label]');
    if (!button || !label) return;
    var on = isLocalPasskeysOn();
    button.classList.toggle('is-on', on);
    button.setAttribute('aria-pressed', on ? 'true' : 'false');
    button.setAttribute('aria-label', 'Local passkeys ' + (on ? 'on' : 'off'));
    label.textContent = 'Local passkeys ' + (on ? 'on' : 'off');
  }

  function initFooterPasskeys() {
    var button = document.querySelector('[data-passkeys]');
    if (!button) return;
    button.addEventListener('click', function() {
      var on = isLocalPasskeysOn();
      localStorage.setItem('localPasskeys', on ? 'off' : 'on');
      updatePasskeysDot();
    });
    updatePasskeysDot();
  }

  function initFooterPasskeysInfo() {
    var button = document.querySelector('[data-passkeys-info]');
    if (!button) return;
    var popover = document.getElementById(button.getAttribute('aria-describedby'));
    var startScrollY = 0;

    function positionPopover() {
      if (!popover || button.getAttribute('aria-expanded') !== 'true') return;
      popover.style.setProperty('--shift', '0px');
      var rect = popover.getBoundingClientRect();
      var padding = 16;
      var shift = 0;
      if (rect.left < padding) shift = padding - rect.left;
      if (rect.right > window.innerWidth - padding) shift = window.innerWidth - padding - rect.right;
      popover.style.setProperty('--shift', shift + 'px');
    }

    function setOpen(open) {
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        startScrollY = window.scrollY;
        positionPopover();
      }
    }

    button.addEventListener('click', function(event) {
      event.stopPropagation();
      setOpen(button.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('click', function(event) {
      if (!button.contains(event.target) && (!popover || !popover.contains(event.target))) {
        setOpen(false);
      }
    });
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape') setOpen(false);
    });
    window.addEventListener('scroll', function() {
      if (button.getAttribute('aria-expanded') === 'true' && Math.abs(window.scrollY - startScrollY) > 24) {
        setOpen(false);
      }
    }, { passive: true });
    window.addEventListener('resize', positionPopover);
  }

  initFooterPasskeys();
  initFooterPasskeysInfo();
})();
