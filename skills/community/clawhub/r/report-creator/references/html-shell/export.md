# Export Menu and Image Export

        /* Export */
        .export-btn { position: fixed; bottom: 16px; right: 16px; z-index: 10001; background: var(--primary); color: #fff; border: none; border-radius: 6px; padding: .45rem .9rem; font-size: .82rem; cursor: pointer; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,.2); font-family: var(--font-sans, system-ui); letter-spacing: .02em; }
        .export-menu { position: fixed; bottom: 52px; right: 16px; z-index: 10001; background: var(--surface, #fff); border: 1px solid var(--border, #e5e7eb); border-radius: 6px; overflow: hidden; display: none; box-shadow: 0 4px 16px rgba(0,0,0,.15); min-width: 148px; }
        .export-menu.open { display: block; }
        .export-item { display: block; width: 100%; padding: .55rem 1rem; font-size: .84rem; background: none; border: none; cursor: pointer; text-align: left; color: var(--text, #111); font-family: var(--font-sans, system-ui); white-space: nowrap; border-bottom: 1px solid var(--border, #e5e7eb); }
        .export-item:last-child { border-bottom: none; }
        .export-item:hover { background: var(--primary-light, #e3edff); }

      <!-- Export (always present) -->
      <!-- lang:en labels: "↓ Export" / "🖨 Print / PDF" / "🖥 Save PNG (Desktop)" / "📱 Save PNG (Mobile)" / "💬 IM Image" -->
      <!-- lang:zh labels: "↓ 导出"  / "🖨 打印 / PDF"  / "🖥 保存图片（桌面）"    / "📱 保存图片（手机）"  / "💬 IM 分享长图"   -->
      <div class="export-menu" id="export-menu">
        <button class="export-item" id="export-print">[🖨 Print / PDF|🖨 打印 / PDF]</button>
        <button class="export-item" id="export-png-desktop">[🖥 Save PNG (Desktop)|🖥 保存图片（桌面）]</button>
        <button class="export-item" id="export-png-mobile">[📱 Save PNG (Mobile)|📱 保存图片（手机）]</button>
        <button class="export-item" id="export-im-share">[💬 IM Image|💬 IM 长图]</button>
      </div>
      <button class="export-btn" id="export-btn" title="Export">[↓ Export|↓ 导出]</button>

      <script>
        // Export: Print/PDF via prepared print mode; images via html2canvas (preloaded on page open)
        // Desktop PNG : full-page, adaptive scale (2× short / 1.5× long pages), PNG
        // Mobile PNG  : .report-wrapper 750px wide (iPhone 2× Retina), JPEG 92%
        // IM Share    : .report-wrapper 800px wide (WeChat/Feishu/DingTalk), JPEG 92%
        (function() {
          const exportBtn  = document.getElementById('export-btn');
          const exportMenu = document.getElementById('export-menu');
          const printBtn   = document.getElementById('export-print');
          const pngDesktop = document.getElementById('export-png-desktop');
          const pngMobile  = document.getElementById('export-png-mobile');
          const pngIM      = document.getElementById('export-im-share');
          if (!exportBtn || !exportMenu) return;
          const LABEL = exportBtn.textContent;
          const PRINT_MODE_CLASS = 'print-exporting';

          exportBtn.addEventListener('click', e => { e.stopPropagation(); exportMenu.classList.toggle('open'); });
          document.addEventListener('click', e => {
            if (!exportBtn.contains(e.target) && !exportMenu.contains(e.target))
              exportMenu.classList.remove('open');
          });

          /* Preload html2canvas immediately — ready before first click */
          let libPromise = null;
          function loadLib() {
            if (libPromise) return libPromise;
            libPromise = new Promise(resolve => {
              if (window.html2canvas) { resolve(); return; }
              const s = document.createElement('script');
              s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1/dist/html2canvas.min.js';
              s.onload = resolve; document.head.appendChild(s);
            });
            return libPromise;
          }
          loadLib(); /* fire immediately */

          function restore() { exportBtn.style.visibility = ''; exportBtn.textContent = LABEL; }
          function preparePrintExport() {
            exportMenu.classList.remove('open');
            exportBtn.style.visibility = 'hidden';
            exportBtn.textContent = '…';
            document.documentElement.classList.add(PRINT_MODE_CLASS);
            document.documentElement.style.setProperty('--print-bg-color', exportBackgroundColor());
          }
          function cleanupPrintExport() {
            document.documentElement.classList.remove(PRINT_MODE_CLASS);
            document.documentElement.style.removeProperty('--print-bg-color');
            restore();
          }
          function filename(suffix, ext) {
            const d = new Date(), pad = n => String(n).padStart(2,'0');
            const date = `${d.getFullYear()}${pad(d.getMonth()+1)}${pad(d.getDate())}`;
            return (document.title||'report').replace(/[/\\:*?"<>|]/g,'_') + `_${date}${suffix}.${ext}`;
          }
          function exportBackgroundColor() {
            const rootStyles = getComputedStyle(document.documentElement);
            const cssVar = (rootStyles.getPropertyValue('--bg') || '').trim();
            if (cssVar) return cssVar;
            const bodyColor = getComputedStyle(document.body).backgroundColor;
            if (bodyColor && bodyColor !== 'rgba(0, 0, 0, 0)' && bodyColor !== 'rgba(0,0,0,0)' && bodyColor !== 'transparent') {
              return bodyColor;
            }
            return '#ffffff';
          }
          function saveBlob(canvas, fname, jpeg) {
            canvas.toBlob(blob => {
              const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: fname });
              a.click(); URL.revokeObjectURL(a.href); restore();
            }, jpeg ? 'image/jpeg' : 'image/png', jpeg ? 0.92 : 1);
          }
          function capture(el, cfg, fname, jpeg) {
            exportMenu.classList.remove('open');
            exportBtn.style.visibility = 'hidden';
            exportBtn.textContent = '…';
            const cardBtn = document.getElementById('card-mode-btn');
            if (cardBtn) cardBtn.style.visibility = 'hidden';
            // When summary card is open, capture .sc-card directly
            // (html2canvas cannot capture position:fixed overlays)
            if (document.body.classList.contains('card-mode')) {
              const card = document.getElementById('sc-card');
              const cardFname = filename('-摘要卡', jpeg ? 'jpg' : 'png');
              loadLib().then(() => html2canvas(card, { scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#ffffff' }).then(c => {
                if (cardBtn) cardBtn.style.visibility = '';
                restore();
                saveBlob(c, cardFname, jpeg);
              }));
              return;
            }
            const tocSidebar = document.getElementById('toc-sidebar');
            const tocToggle = document.getElementById('toc-toggle-btn');
            const tocIsOpen = tocSidebar && tocSidebar.classList.contains('open');
            if (tocToggle && !tocIsOpen) tocToggle.style.visibility = 'hidden';
            document.querySelectorAll('.fade-in-up').forEach(e => e.classList.add('visible'));
            loadLib().then(() => html2canvas(el, cfg).then(c => {
              if (tocToggle && !tocIsOpen) tocToggle.style.visibility = '';
              if (cardBtn) cardBtn.style.visibility = '';
              saveBlob(c, fname, jpeg);
            }));
          }
          window.addEventListener('afterprint', cleanupPrintExport);

          printBtn && printBtn.addEventListener('click', () => {
            preparePrintExport();
            requestAnimationFrame(() => {
              requestAnimationFrame(() => {
                window.print();
              });
            });
          });

          pngDesktop && pngDesktop.addEventListener('click', () => {
            const H = document.documentElement.scrollHeight;
            capture(document.documentElement, {
              scale: H > 4000 ? 2.5 : 3, useCORS: true, allowTaint: true,
              scrollX: 0, scrollY: 0,
              width: document.documentElement.scrollWidth, height: H,
              windowWidth: document.documentElement.scrollWidth, windowHeight: H
            }, filename('', 'png'), false);
          });

          pngMobile && pngMobile.addEventListener('click', () => {
            const el = document.querySelector('.report-wrapper') || document.documentElement;
            capture(el, {
              scale: (750 / el.offsetWidth) * 2, useCORS: true, allowTaint: true,
              backgroundColor: exportBackgroundColor(),
              scrollX: 0, scrollY: 0, width: el.scrollWidth, height: el.scrollHeight
            }, filename('-mobile', 'jpg'), true);
          });

          pngIM && pngIM.addEventListener('click', () => {
            const el = document.querySelector('.report-wrapper') || document.documentElement;
            capture(el, {
              scale: (800 / el.offsetWidth) * 2, useCORS: true, allowTaint: true,
              backgroundColor: exportBackgroundColor(),
              scrollX: 0, scrollY: 0, width: el.scrollWidth, height: el.scrollHeight
            }, filename('-im', 'jpg'), true);
          });
        })();
      </script>
