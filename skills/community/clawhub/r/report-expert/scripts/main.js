/* ============================================
   传霜 · 交互系统 v6
   ============================================ */

(function() {
  'use strict';

  /* --- Scroll Reveal --- */
  function initScrollReveal() {
    var els = document.querySelectorAll('[data-reveal]');
    if (!els.length) return;
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var delay = entry.target.getAttribute('data-reveal-delay') || 0;
          setTimeout(function() { entry.target.classList.add('revealed'); }, parseInt(delay));
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -20px 0px' });
    els.forEach(function(el) { observer.observe(el); });
  }

  /* --- Fixed Left TOC --- */
  function initTOC() {
    var sidebar = document.querySelector('.toc-sidebar');
    var toggle = document.querySelector('.toc-toggle');
    var closeBtn = document.querySelector('.toc-sidebar__close');
    if (!sidebar || !toggle) return;

    var isOpen = window.innerWidth >= 1024;

    function applyState() {
      if (isOpen) {
        sidebar.classList.add('toc-sidebar--open');
        toggle.classList.add('toc-toggle--hidden');
        document.body.classList.add('toc-open');
      } else {
        sidebar.classList.remove('toc-sidebar--open');
        toggle.classList.remove('toc-toggle--hidden');
        document.body.classList.remove('toc-open');
      }
    }

    toggle.addEventListener('click', function() {
      isOpen = true;
      applyState();
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        isOpen = false;
        applyState();
      });
    }

    // Generate TOC from headings
    var content = document.querySelector('.page-body');
    if (!content) return;
    // Auto-assign IDs to headings that lack them
    content.querySelectorAll('h2, h3').forEach(function(h, i) {
      if (!h.id) {
        var base = h.textContent.trim().replace(/[^\w\u4e00-\u9fff]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').toLowerCase();
        h.id = base || ('heading-' + i);
      }
    });
    var headings = content.querySelectorAll('h2[id], h3[id]');
    if (!headings.length) { sidebar.style.display = 'none'; toggle.style.display = 'none'; return; }

    var list = sidebar.querySelector('.toc-list');
    if (!list) return;
    list.innerHTML = '';

    headings.forEach(function(h) {
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.className = 'toc-list__item toc-list__item--' + h.tagName.toLowerCase();
      a.addEventListener('click', function(e) {
        e.preventDefault();
        var target = document.getElementById(h.id);
        if (target) {
          var offset = 90;
          var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
          window.scrollTo({ top: top, behavior: 'smooth' });
        }
      });
      list.appendChild(a);
    });

    // Active tracking
    var sections = [];
    headings.forEach(function(h) { sections.push({ id: h.id, el: h, top: 0 }); });

    function updateActive() {
      var scrollY = window.pageYOffset;
      var current = '';
      sections.forEach(function(s) {
        s.top = s.el.getBoundingClientRect().top + window.pageYOffset - 120;
        if (scrollY >= s.top) current = s.id;
      });
      var items = list.querySelectorAll('.toc-list__item');
      items.forEach(function(item) {
        item.classList.toggle('toc-list__item--active', item.getAttribute('href') === '#' + current);
      });
    }

    var ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) { requestAnimationFrame(function() { updateActive(); ticking = false; }); ticking = true; }
    });
    updateActive();
    applyState();
  }

  /* --- Scroll Progress --- */
  function initScrollProgress() {
    var bar = document.querySelector('.scroll-progress');
    if (!bar) return;
    window.addEventListener('scroll', function() {
      var scrollTop = window.pageYOffset;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%';
    });
  }

  /* --- Back to Top --- */
  function initBackToTop() {
    var btn = document.querySelector('.back-to-top');
    if (!btn) return;
    window.addEventListener('scroll', function() {
      btn.classList.toggle('back-to-top--visible', window.pageYOffset > 400);
    });
    btn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* --- Chart Zoom / Lightbox --- */
  function initChartZoom() {
    // Auto-inject zoom buttons into chart-boxes that lack one
    document.querySelectorAll('.chart-box:not(:has(.chart-box__zoom-btn))').forEach(function(box) {
      var btn = document.createElement('button');
      btn.className = 'chart-box__zoom-btn';
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>';
      btn.title = '放大查看';
      btn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:10;opacity:0.7;cursor:pointer;background:#f1f5f9;border:1px solid #e2e8f0;border-radius:6px;padding:6px;';
      box.style.position = 'relative';
      box.appendChild(btn);
    });

    // Also inject zoom buttons for ECharts divs
    document.querySelectorAll('div[id$="Chart"], .echart, [id*="chart"]').forEach(function(el) {
      if (el.closest('.chart-box') || el.querySelector('.chart-box__zoom-btn')) return;
      var btn = document.createElement('button');
      btn.className = 'chart-box__zoom-btn';
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>';
      btn.title = '放大查看';
      btn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:10;opacity:0.7;cursor:pointer;background:#f1f5f9;border:1px solid #e2e8f0;border-radius:6px;padding:6px;';
      el.style.position = 'relative';
      el.appendChild(btn);
    });

    // Inject zoom buttons for mermaid diagrams
    document.querySelectorAll('.mermaid, pre.mermaid').forEach(function(el) {
      if (el.closest('.chart-box') || el.querySelector('.chart-box__zoom-btn')) return;
      var wrapper = document.createElement('div');
      wrapper.className = 'mermaid-zoom-wrap';
      wrapper.style.cssText = 'position:relative;display:block;width:100%;';
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);
      var btn = document.createElement('button');
      btn.className = 'chart-box__zoom-btn';
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>';
      btn.title = '放大查看';
      btn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:10;opacity:0.7;cursor:pointer;background:#f1f5f9;border:1px solid #e2e8f0;border-radius:6px;padding:6px;';
      wrapper.appendChild(btn);
    });

    document.addEventListener('click', function(e) {
      var btn = e.target.closest('.chart-box__zoom-btn, .chart-zoom-wrap__btn');
      if (!btn) return;
      var box = btn.closest('.chart-box, .chart-zoom-wrap, .mermaid-zoom-wrap, div[id$="Chart"], .echart, [id*="chart"]');
      if (!box) return;
      e.preventDefault(); e.stopPropagation();
      var overlay = document.createElement('div');
      overlay.className = 'chart-zoom-overlay';
      overlay.style.cssText = 'position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.75);display:flex;align-items:center;justify-content:center;cursor:zoom-out;padding:32px;box-sizing:border-box;animation:fadeIn .2s ease;';
      var style = document.createElement('style');
      style.textContent = '@keyframes fadeIn{from{opacity:0}to{opacity:1}}';
      overlay.appendChild(style);
      // For ECharts: create fresh instance with original option
      if (typeof echarts !== 'undefined') {
        var origInstance = echarts.getInstanceByDom(box);
        if (origInstance) {
          var opt = origInstance.getOption();
          var container = document.createElement('div');
          container.style.cssText = 'max-width:95vw;max-height:90vh;width:90vw;height:70vh;background:#fff;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,0.4);box-sizing:border-box;';
          var chartDiv = document.createElement('div');
          chartDiv.style.cssText = 'width:100%;height:100%;box-sizing:border-box;';
          container.appendChild(chartDiv);
          overlay.appendChild(container);
          document.body.appendChild(overlay);
          setTimeout(function(){
            var newInst = echarts.init(chartDiv);
            newInst.setOption(opt);
            var closeFn = function() { newInst.dispose(); overlay.remove(); };
            overlay.addEventListener('click', function(ev) { if (ev.target === overlay) closeFn(); });
            document.addEventListener('keydown', function handler(ev) { if (ev.key === 'Escape') { closeFn(); document.removeEventListener('keydown', handler); } });
          }, 100);
          return;
        }
      }
      var clone = box.cloneNode(true);
      clone.style.cssText = 'max-width:95vw;max-height:90vh;width:90vw;overflow:auto;background:#fff;border-radius:12px;padding:24px;box-shadow:0 20px 60px rgba(0,0,0,0.4);';
      overlay.appendChild(clone);
      overlay.addEventListener('click', function(ev) { if (ev.target === overlay) overlay.remove(); });
      document.addEventListener('keydown', function handler(ev) { if (ev.key === 'Escape') { overlay.remove(); document.removeEventListener('keydown', handler); } });
      document.body.appendChild(overlay);
    });
  }

  /* --- ECharts Auto-Init --- */
  var _echartInstances = [];
  function initECharts() {
    if (typeof echarts === 'undefined') return;
    var els = document.querySelectorAll('.chart-box__canvas[data-option]');
    if (!els.length) return;
    els.forEach(function(el) {
      if (echarts.getInstanceByDom(el)) return;
      var optStr = el.getAttribute('data-option');
      if (!optStr) return;
      try {
        var opt = JSON.parse(optStr);
        var chart = echarts.init(el);
        chart.setOption(opt);
        _echartInstances.push(chart);
        window.addEventListener('resize', function() { chart.resize(); });
      } catch(e) {
        console.warn('ECharts auto-init error for', el.id, e);
      }
    });
    scheduleResize();
  }

  /* Resize all charts with retry — handles hidden iframe / layout settling */
  function scheduleResize() {
    function doResize() {
      _echartInstances.forEach(function(c) { try { c.resize(); } catch(e){} });
    }
    // Multiple delayed retries to catch different timing scenarios
    setTimeout(doResize, 50);
    setTimeout(doResize, 200);
    setTimeout(doResize, 600);
    setTimeout(doResize, 1500);
    // Also on window load (catches iframe src changes)
    window.addEventListener('load', doResize);
    // Also when becoming visible (e.g. iframe unhidden)
    if (document.hidden) {
      document.addEventListener('visibilitychange', function handler() {
        if (!document.hidden) { doResize(); document.removeEventListener('visibilitychange', handler); }
      });
    }
  }

  /* --- Init --- */
  document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initTOC();
    initScrollProgress();
    initBackToTop();
    initECharts();
    initChartZoom();
  });
})();

// ── Chart.js 自动初始化 ──
document.addEventListener('DOMContentLoaded', function() {
  if (typeof Chart === 'undefined') return;
  document.querySelectorAll('.chart-container[data-chart]').forEach(function(el) {
    var canvas = el.querySelector('canvas');
    if (!canvas) return;
    try {
      var config = {
        type: el.dataset.chart,
        data: {
          labels: JSON.parse(el.dataset.labels || '[]'),
          datasets: JSON.parse(el.dataset.datasets || '[]')
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
      };
      var h = el.dataset.height || '300px';
      canvas.style.height = h;
      canvas.parentElement.style.height = h;
      new Chart(canvas, config);
    } catch(e) { console.warn('Chart.js init error:', e); }
  });
});
