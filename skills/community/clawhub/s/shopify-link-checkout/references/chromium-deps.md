# Installing Chromium Dependencies Without Root

On headless servers without root/sudo, Playwright's Chromium needs system libraries that aren't installed. Download Debian packages manually and extract to a user directory.

## Required Libraries

```
libnspr4  libnss3  libatk1.0-0  libatk-bridge2.0-0  libatspi2.0-0
libcups2  libdrm2  libxkbcommon0  libxcomposite1  libxdamage1
libxfixes3  libxrandr2  libgbm1  libpango-1.0-0  libcairo2
libasound2  libdbus-1-3  libxi6  libwayland-server0
```

## Install Process

```bash
mkdir -p /tmp/cdeps ~/.local/lib/chromium-deps
cd /tmp/cdeps

BASE="http://deb.debian.org/debian/pool/main"
SEC="http://security.debian.org/debian-security/pool/updates/main"

# Download (adjust versions for your Debian release)
curl -sLO "$BASE/n/nspr/libnspr4_4.35-1_amd64.deb"
curl -sLO "$SEC/n/nss/libnss3_3.87.1-1+deb12u2_amd64.deb"
curl -sLO "$BASE/a/at-spi2-core/libatk1.0-0_2.46.0-5_amd64.deb"
curl -sLO "$BASE/a/at-spi2-core/libatk-bridge2.0-0_2.46.0-5_amd64.deb"
curl -sLO "$BASE/a/at-spi2-core/libatspi2.0-0_2.46.0-5_amd64.deb"
curl -sLO "$BASE/c/cups/libcups2_2.4.2-3+deb12u9_amd64.deb"
curl -sLO "$BASE/libd/libdrm/libdrm2_2.4.114-1+b1_amd64.deb"
curl -sLO "$BASE/libx/libxkbcommon/libxkbcommon0_1.5.0-1_amd64.deb"
curl -sLO "$BASE/libx/libxcomposite/libxcomposite1_0.4.5-1_amd64.deb"
curl -sLO "$BASE/libx/libxdamage/libxdamage1_1.1.6-1_amd64.deb"
curl -sLO "$BASE/libx/libxfixes/libxfixes3_6.0.0-2_amd64.deb"
curl -sLO "$BASE/libx/libxrandr/libxrandr2_1.5.2-2+b1_amd64.deb"
curl -sLO "$BASE/m/mesa/libgbm1_22.3.6-1+deb12u1_amd64.deb"
curl -sLO "$BASE/p/pango1.0/libpango-1.0-0_1.50.12+ds-1_amd64.deb"
curl -sLO "$BASE/c/cairo/libcairo2_1.16.0-7_amd64.deb"
curl -sLO "$BASE/a/alsa-lib/libasound2_1.2.8-1+b1_amd64.deb"
curl -sLO "$BASE/d/dbus/libdbus-1-3_1.14.10-1~deb12u1_amd64.deb"
curl -sLO "$BASE/libx/libxi/libxi6_1.8-1+b1_amd64.deb"
curl -sLO "$BASE/w/wayland/libwayland-server0_1.21.0-1_amd64.deb"

# Extract all
for deb in *.deb; do
  dpkg-deb -x "$deb" ~/.local/lib/chromium-deps/ 2>/dev/null
done

# Verify
ldd ~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>&1 | grep "not found"
# Should return empty (no missing libs)
```

## Usage

Set before running Playwright:
```bash
export LD_LIBRARY_PATH="$HOME/.local/lib/chromium-deps/usr/lib/x86_64-linux-gnu:$HOME/.local/lib/chromium-deps/lib/x86_64-linux-gnu"
```

Launch with:
```js
const browser = await chromium.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu',
         '--disable-blink-features=AutomationControlled'],
});
```

Always use a realistic user agent:
```js
const ctx = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ...',
  viewport: { width: 1440, height: 900 },
});
```
