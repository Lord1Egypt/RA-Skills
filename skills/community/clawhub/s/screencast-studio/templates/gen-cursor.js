// Render a Windows-style arrow cursor as transparent PNG.
// Tip is at the top-left so overlay at (clickX, clickY) puts the tip on the click point.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 60, height: 60 },
    deviceScaleFactor: 2, // crisp arrow
  });
  const page = await context.newPage();

  // Tip at (1.5, 1.5) to leave room for stroke; classic Windows arrow proportions.
  // Arrow extends down-right from tip. White fill, black 1.5px outline.
  const html = `<!doctype html><html><head><style>
    html,body{margin:0;padding:0;background:transparent;}
    svg{display:block;}
  </style></head><body>
    <svg id="c" width="22" height="28" xmlns="http://www.w3.org/2000/svg">
      <polygon points="1.5,1.5 1.5,22 6.5,17.5 10,25.5 12.5,24.5 9,16.5 16.5,16.5"
               fill="white"
               stroke="black"
               stroke-width="1.6"
               stroke-linejoin="round"
               stroke-linecap="round" />
    </svg>
  </body></html>`;

  await page.setContent(html);
  const svg = page.locator('#c');
  await svg.screenshot({
    path: path.join(__dirname, 'cursor.png'),
    omitBackground: true,
  });

  await browser.close();
  console.log('Generated cursor.png (Windows arrow, 22x28 @2x)');
})();
