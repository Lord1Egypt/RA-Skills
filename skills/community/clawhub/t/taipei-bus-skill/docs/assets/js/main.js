/**
 * main.js — Taipei Bus Skill Documentation
 * Language switching, theme toggle, navigation, code copy
 */

(function () {
  'use strict';

  // ─── Language ─────────────────────────────────────────────────
  const LANGS = { 'zh-TW': 'index.html', 'zh-CN': 'index.zh-CN.html', en: 'index.en.html' };
  const STORAGE_KEY_LANG = 'taipei-bus-docs-lang';
  const STORAGE_KEY_THEME = 'taipei-bus-docs-theme';

  function getLang() {
    return localStorage.getItem(STORAGE_KEY_LANG) || 'zh-TW';
  }

  function switchLang(lang) {
    localStorage.setItem(STORAGE_KEY_LANG, lang);
    const target = LANGS[lang];
    if (target) {
      window.location.href = target;
    }
  }

  function initLangSwitcher() {
    const btns = document.querySelectorAll('.lang-btn');
    const current = getLang();
    btns.forEach(btn => {
      if (btn.dataset.lang === current) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
      btn.addEventListener('click', () => switchLang(btn.dataset.lang));
    });
  }

  // ─── Theme ────────────────────────────────────────────────────
  function getTheme() {
    const stored = localStorage.getItem(STORAGE_KEY_THEME);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY_THEME, theme);
    const btn = document.getElementById('themeToggle');
    if (btn) {
      btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      btn.setAttribute('aria-label', theme === 'dark' ? '切換到淺色主題' : '切換到深色主題');
    }
  }

  function toggleTheme() {
    const next = getTheme() === 'dark' ? 'light' : 'dark';
    setTheme(next);
  }

  function initTheme() {
    setTheme(getTheme());
    const btn = document.getElementById('themeToggle');
    if (btn) {
      btn.addEventListener('click', toggleTheme);
    }
  }

  // ─── Mobile Menu ─────────────────────────────────────────────
  function initMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const btn = document.getElementById('mobileMenuBtn');
    const closeBtn = document.getElementById('closeSidebarBtn');

    function openMenu() {
      sidebar.classList.add('open');
      overlay.classList.add('visible');
      document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
      sidebar.classList.remove('open');
      overlay.classList.remove('visible');
      document.body.style.overflow = '';
    }

    if (btn) btn.addEventListener('click', openMenu);
    if (closeBtn) closeBtn.addEventListener('click', closeMenu);
    if (overlay) overlay.addEventListener('click', closeMenu);

    // Close on nav link click
    sidebar.querySelectorAll('.sidebar-link').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth < 768) closeMenu();
      });
    });
  }

  // ─── Active Nav on Scroll ─────────────────────────────────────
  function initActiveNav() {
    const sections = document.querySelectorAll('.section[id]');
    const navLinks = document.querySelectorAll('.sidebar-link[href^="#"]');

    if (!sections.length || !navLinks.length) return;

    let ticking = false;

    function updateActive() {
      const scrollY = window.scrollY + 100;

      let current = '';
      sections.forEach(section => {
        if (scrollY >= section.offsetTop) {
          current = section.getAttribute('id');
        }
      });

      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
          link.classList.add('active');
        }
      });

      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateActive);
        ticking = true;
      }
    }, { passive: true });

    updateActive();
  }

  // ─── Smooth Scroll for Anchor Links ───────────────────────────
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', e => {
        const targetId = anchor.getAttribute('href').slice(1);
        if (!targetId) return;
        const target = document.getElementById(targetId);
        if (!target) return;

        e.preventDefault();
        const offset = parseInt(anchor.dataset.offset || 0);
        const top = target.getBoundingClientRect().top + window.scrollY - 80 + offset;
        window.scrollTo({ top, behavior: 'smooth' });

        // Update URL without jump
        history.pushState(null, '', '#' + targetId);
      });
    });
  }

  // ─── Code Copy Buttons ───────────────────────────────────────
  function initCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        const wrapper = btn.closest('.code-wrapper');
        if (!wrapper) return;

        const code = wrapper.querySelector('code');
        if (!code) return;

        const text = code.textContent || '';
        try {
          await navigator.clipboard.writeText(text);
          btn.textContent = '✓ 已複製';
          btn.classList.add('copied');
          setTimeout(() => {
            btn.innerHTML = '📋 複製';
            btn.classList.remove('copied');
          }, 2000);
        } catch (err) {
          // Fallback for older browsers
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none;';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.textContent = '✓ 已複製';
          btn.classList.add('copied');
          setTimeout(() => {
            btn.innerHTML = '📋 複製';
            btn.classList.remove('copied');
          }, 2000);
        }
      });
    });
  }

  // ─── Function Card Toggles ───────────────────────────────────
  function initFunctionCards() {
    document.querySelectorAll('.function-card-header').forEach(header => {
      header.addEventListener('click', () => {
        const card = header.closest('.function-card');
        if (card) {
          card.classList.toggle('open');
        }
      });

      // Keyboard accessible
      header.setAttribute('tabindex', '0');
      header.setAttribute('role', 'button');
      header.setAttribute('aria-expanded', 'false');
      header.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          header.click();
        }
      });
    });

    // Update aria-expanded
    document.querySelectorAll('.function-card-header').forEach(header => {
      const observer = new MutationObserver(() => {
        const card = header.closest('.function-card');
        header.setAttribute('aria-expanded', card && card.classList.contains('open') ? 'true' : 'false');
      });
      const card = header.closest('.function-card');
      if (card) observer.observe(card, { attributes: true, attributeFilter: ['class'] });
    });
  }

  // ─── Mobile: close sidebar when clicking a link ──────────────
  function initMobileNavClose() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;

    sidebar.querySelectorAll('.sidebar-link').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth < 768) {
          sidebar.classList.remove('open');
          document.querySelector('.sidebar-overlay')?.classList.remove('visible');
          document.body.style.overflow = '';
        }
      });
    });
  }

  // ─── Search shortcut (Cmd/Ctrl + K) ─────────────────────────
  function initSearch() {
    document.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      }
    });
  }

  // ─── ETA Tier visualizer ─────────────────────────────────────
  function initEtaTiers() {
    const tierEls = document.querySelectorAll('[data-tier]');
    if (!tierEls.length) return;

    tierEls.forEach(el => {
      const tier = parseInt(el.dataset.tier || '0');
      const stars = '★'.repeat(tier) + '☆'.repeat(5 - tier);
      el.textContent = stars;
    });
  }

  // ─── Init all ─────────────────────────────────────────────────
  function init() {
    initTheme();
    initLangSwitcher();
    initMobileMenu();
    initActiveNav();
    initSmoothScroll();
    initCopyButtons();
    initFunctionCards();
    initMobileNavClose();
    initEtaTiers();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
