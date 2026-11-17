/** 站斧 Playwright 强制有界面模式（禁止无头）。 */

const HEADLESS_ENV_KEYS = [
  "PLAYWRIGHT_HEADLESS",
  "HEADLESS",
  "PW_HEADLESS",
  "CHROME_HEADLESS",
];

export function ensureHeadedMode() {
  for (const key of HEADLESS_ENV_KEYS) {
    process.env[key] = "0";
  }
}

export function headedLaunchOptions() {
  ensureHeadedMode();
  return { headless: false };
}

export function assertNotHeadlessLaunch(headless) {
  if (headless) {
    throw new Error("站斧自动化禁止使用无头模式（headless=True）");
  }
}
