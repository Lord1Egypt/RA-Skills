import { expect, test } from "@playwright/test";

test.describe("WCAG 4.1.2 dynamic state example", () => {
  test("exposes the toggle state and keeps it synchronized with the UI", async ({ page }) => {
    await page.goto(process.env.WCAG_TEST_URL ?? "http://127.0.0.1:8000/");
    const toggle = page.locator("#theme-toggle");

    await expect(toggle).toBeVisible();
    await expect(toggle).toHaveRole("button");
    await expect(toggle).toHaveAccessibleName("Dark theme");
    await expect(toggle).toHaveAttribute("aria-pressed", "false");
    await expect(page.locator("#theme-demo-correct")).not.toHaveClass(/is-dark/);

    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("#theme-demo-correct")).toHaveClass(/is-dark/);

    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-pressed", "false");
    await expect(page.locator("#theme-demo-correct")).not.toHaveClass(/is-dark/);
  });

  test("supports keyboard activation and exposes each resulting state", async ({ page }) => {
    await page.goto(process.env.WCAG_TEST_URL ?? "http://127.0.0.1:8000/");
    const toggle = page.locator("#theme-toggle");

    await toggle.focus();
    await expect(toggle).toBeFocused();
    await page.keyboard.press("Space");
    await expect(toggle).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("#theme-demo-correct")).toHaveClass(/is-dark/);

    await page.keyboard.press("Enter");
    await expect(toggle).toHaveAttribute("aria-pressed", "false");
    await expect(page.locator("#theme-demo-correct")).not.toHaveClass(/is-dark/);
  });

  test("shows why the button without exposed state is insufficient", async ({ page }) => {
    await page.goto(process.env.WCAG_TEST_URL ?? "http://127.0.0.1:8000/");
    const brokenToggle = page.locator("#theme-toggle-broken");

    await expect(brokenToggle).toHaveRole("button");
    await expect(brokenToggle).toHaveAccessibleName("Dark theme");
    expect(await brokenToggle.getAttribute("aria-pressed")).toBeNull();
    await brokenToggle.click();
    await expect(page.locator("#theme-demo-broken")).toHaveClass(/is-dark/);
    await expect(page.locator("#broken-theme-output")).toHaveText("dark");
    expect(await brokenToggle.getAttribute("aria-pressed")).toBeNull();
  });

  test("native checkbox and disclosure expose their changed states", async ({ page }) => {
    await page.goto(process.env.WCAG_TEST_URL ?? "http://127.0.0.1:8000/");
    const notifications = page.getByRole("checkbox", { name: "Notifications" });

    await expect(notifications).not.toBeChecked();
    await notifications.focus();
    await page.keyboard.press("Space");
    await expect(notifications).toBeChecked();

    const disclosure = page.locator("details");
    const summary = disclosure.locator("summary");
    await expect(disclosure).not.toHaveAttribute("open", "");
    await summary.focus();
    await page.keyboard.press("Enter");
    await expect(disclosure).toHaveAttribute("open", "");
  });

  test("custom switch exposes its state and updates the application", async ({ page }) => {
    await page.goto(process.env.WCAG_TEST_URL ?? "http://127.0.0.1:8000/");
    const compactToggle = page.getByRole("switch", { name: "Compact layout" });

    await expect(compactToggle).toHaveAttribute("aria-checked", "false");
    await compactToggle.focus();
    await page.keyboard.press("Space");
    await expect(compactToggle).toHaveAttribute("aria-checked", "true");
    await expect(page.locator("main")).toHaveClass(/compact/);
    await expect(page.locator("#compact-state")).toHaveText("Compact layout is on.");
  });
});
