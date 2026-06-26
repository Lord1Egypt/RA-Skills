/**
 * playwright-config-example.ts — Production Playwright configuration.
 *
 * Place at: e2e/playwright.config.ts (or project root playwright.config.ts)
 *
 * This config provides:
 *   - Auth state reuse via a setup project
 *   - Multi-browser testing (Chromium, Firefox, WebKit)
 *   - CI-aware settings (retries, workers, traces)
 *   - Automatic dev server startup
 *   - Sensible timeouts and viewport defaults
 */

import { defineConfig, devices } from "@playwright/test";

/**
 * Read environment variables.
 * See https://playwright.dev/docs/test-configuration
 */
const BASE_URL = process.env.BASE_URL ?? "http://localhost:3000";
const CI = !!process.env.CI;

export default defineConfig({
  // ─── Test Discovery ───────────────────────────────────
  testDir: "./tests",
  testMatch: "**/*.spec.ts",

  // ─── Execution ────────────────────────────────────────
  fullyParallel: true,
  forbidOnly: CI, // Fail in CI if test.only is left in code
  retries: CI ? 2 : 0, // Retry failed tests in CI only
  workers: CI ? 2 : undefined, // Limit workers in CI for stability

  // ─── Timeouts ─────────────────────────────────────────
  timeout: 30_000, // Per-test timeout (30 seconds)
  expect: {
    timeout: 10_000, // Per-assertion timeout (10 seconds)
  },

  // ─── Reporting ────────────────────────────────────────
  reporter: [
    ["list"], // Console output during runs
    ["html", { open: CI ? "never" : "on-failure" }], // HTML report
    ...(CI ? [["junit", { outputFile: "test-results/junit.xml" }] as const] : []),
  ],

  // ─── Shared Settings ─────────────────────────────────
  use: {
    baseURL: BASE_URL,

    // Traces: capture on first retry for debugging flaky tests
    trace: "on-first-retry",

    // Screenshots: capture on failure only
    screenshot: "only-on-failure",

    // Video: capture on first retry
    video: "on-first-retry",

    // Viewport
    viewport: { width: 1280, height: 720 },

    // Disable animations for faster, more reliable tests
    // (CSS animations and transitions are skipped)
    // Note: Uncomment the line below to disable animations
    // actionTimeout: 10_000,

    // Ignore HTTPS errors in dev/staging
    ignoreHTTPSErrors: !CI,

    // Locale and timezone (consistent across environments)
    locale: "en-US",
    timezoneId: "America/New_York",
  },

  // ─── Projects ─────────────────────────────────────────
  projects: [
    // --- Setup: authenticate once, save state --------
    {
      name: "setup",
      testDir: "./fixtures",
      testMatch: "auth.fixture.ts",
    },

    // --- Chromium (primary) --------------------------
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        storageState: ".auth/user.json",
      },
      dependencies: ["setup"],
    },

    // --- Firefox -------------------------------------
    {
      name: "firefox",
      use: {
        ...devices["Desktop Firefox"],
        storageState: ".auth/user.json",
      },
      dependencies: ["setup"],
    },

    // --- WebKit (Safari) -----------------------------
    {
      name: "webkit",
      use: {
        ...devices["Desktop Safari"],
        storageState: ".auth/user.json",
      },
      dependencies: ["setup"],
    },

    // --- Mobile Chrome -------------------------------
    {
      name: "mobile-chrome",
      use: {
        ...devices["Pixel 7"],
        storageState: ".auth/user.json",
      },
      dependencies: ["setup"],
    },

    // --- Mobile Safari -------------------------------
    {
      name: "mobile-safari",
      use: {
        ...devices["iPhone 14"],
        storageState: ".auth/user.json",
      },
      dependencies: ["setup"],
    },
  ],

  // ─── Dev Server ───────────────────────────────────────
  // Automatically start the app before running tests (local dev only).
  // In CI, the app should already be running (via docker compose or a prior step).
  webServer: CI
    ? undefined
    : {
        command: "npm run dev",
        url: BASE_URL,
        reuseExistingServer: true,
        timeout: 120_000, // 2 minutes to start
        stdout: "pipe",
        stderr: "pipe",
      },
});
