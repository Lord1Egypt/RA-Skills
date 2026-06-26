#!/usr/bin/env bash
# browser-setup: 验证浏览器环境
# 打开百度首页，截图并返回路径
set -e

WORKSPACE="${1:-.}"
SCREENSHOT_PATH="${2:-/tmp/browser-setup-verify.png}"
MODE="${3:-headless}"  # headless | headed

echo "=== 浏览器验证 ==="
echo "模式: $MODE"
echo ""

# 如果是 headed 模式，先启动 Xvfb（仅 Linux）
if [[ "$MODE" == "headed" ]] && [[ "$(uname -s)" == "Linux" ]]; then
  if ! pgrep -x Xvfb > /dev/null; then
    echo "启动 Xvfb 虚拟显示器..."
    Xvfb :99 -screen 0 1280x900x24 -ac &
    sleep 1
    export DISPLAY=:99
    echo "✅ Xvfb 已启动 (DISPLAY=:99)"
  else
    export DISPLAY=:99
    echo "✅ Xvfb 已在运行 (DISPLAY=:99)"
  fi
fi

cd "$WORKSPACE"

# 运行验证脚本
HEADED_ARG="true"
[[ "$MODE" == "headless" ]] && HEADED_ARG="false"

node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({
    headless: $HEADED_ARG,
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 900 });

  console.log('正在打开百度...');
  await page.goto('https://www.baidu.com', {
    waitUntil: 'networkidle',
    timeout: 30000
  });

  const title = await page.title();
  console.log('页面标题: ' + title);

  // 获取热搜第一
  const hotWord = await page.evaluate(() => {
    const el = document.querySelector('#hotsearch-content-wrapper li a span.title-content-title');
    return el ? el.textContent.trim() : null;
  });
  if (hotWord) {
    console.log('热搜第一: ' + hotWord);
  }

  await page.screenshot({ path: '$SCREENSHOT_PATH', fullPage: false });
  console.log('截图保存: $SCREENSHOT_PATH');

  await browser.close();
  console.log('');
  console.log('✅ 浏览器验证通过');
})().catch(e => {
  console.error('❌ 验证失败:', e.message);
  process.exit(1);
});
" 2>&1

echo ""
echo "截图路径: $SCREENSHOT_PATH"
