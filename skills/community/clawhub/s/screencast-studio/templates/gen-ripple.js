// Render a soft white ring as transparent PNG. Used as the click ripple base —
// postprocess scales it to multiple sizes + alphas to simulate Material expanding ripple.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 100, height: 100 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  // Single ring at 80x80 (master size). ffmpeg will scale this down for sub-frames.
  const html = `<!doctype html><html><head><style>
    html,body{margin:0;padding:0;background:transparent;}
    svg{display:block;}
  </style></head><body>
    <svg id="r" width="80" height="80" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="glow" x="-25%" y="-25%" width="150%" height="150%">
          <feGaussianBlur stdDeviation="0.7"/>
        </filter>
      </defs>
      <circle cx="40" cy="40" r="36"
              fill="none"
              stroke="white"
              stroke-width="3.5"
              opacity="0.95"
              filter="url(#glow)"/>
    </svg>
  </body></html>`;

  await page.setContent(html);
  const svg = page.locator('#r');
  await svg.screenshot({
    path: path.join(__dirname, 'ripple.png'),
    omitBackground: true,
  });

  await browser.close();
  console.log('Generated ripple.png (soft white ring, 80x80 @2x)');
})();
