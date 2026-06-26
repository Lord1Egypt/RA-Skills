/**
 * e2e-test-template.ts — Annotated E2E test using Playwright.
 *
 * Place at: e2e/tests/users/create-user.spec.ts
 *
 * This template demonstrates:
 *   - Using page objects (tests never touch selectors directly)
 *   - API-based test data setup (fast) and cleanup (reliable)
 *   - Explicit waits (never hardcoded timeouts)
 *   - Testing success paths, error paths, and edge cases
 *   - Auth state reuse via storageState
 */

import { test, expect } from "@playwright/test";
import { UsersPage, CreateUserDialog } from "../pages/users.page";
import { TestDataAPI } from "../utils/api-helpers";

// ─── Test Suite: Create User ────────────────────────────────────────────────────

test.describe("Create User", () => {
  let usersPage: UsersPage;
  let api: TestDataAPI;

  test.beforeEach(async ({ page, request }) => {
    // Initialize page objects and API helpers
    usersPage = new UsersPage(page);
    api = new TestDataAPI(request);

    // Navigate to the users page (auth state is pre-loaded via storageState)
    await usersPage.goto();
  });

  // ─── Success Path ───────────────────────────────────
  test("creates a new user with valid data", async ({ page }) => {
    // Arrange: open the create dialog
    await usersPage.clickCreateUser();
    const dialog = new CreateUserDialog(page);

    // Act: fill and submit the form
    await dialog.fillForm({
      email: `e2e-create-${Date.now()}@example.com`,
      displayName: "E2E Test User",
      role: "member",
    });
    await dialog.submit();

    // Assert: success toast appears
    await expect(usersPage.toast).toContainText(/created successfully/i);

    // Assert: user appears in the list
    await expect(
      usersPage.getUserRow(`e2e-create-${Date.now()}@example.com`),
    ).toBeVisible();
  });

  // ─── Validation Error Path ──────────────────────────
  test("shows validation error for invalid email", async ({ page }) => {
    await usersPage.clickCreateUser();
    const dialog = new CreateUserDialog(page);

    // Act: submit with invalid email
    await dialog.fillForm({
      email: "not-an-email",
      displayName: "Invalid Email User",
    });
    await dialog.submitButton.click();

    // Assert: validation error appears (form is NOT submitted)
    const errorMessage = page.getByText(/invalid email/i);
    await expect(errorMessage).toBeVisible();
  });

  // ─── Duplicate Error Path ──────────────────────────
  test("shows error when creating user with duplicate email", async ({
    page,
    request,
  }) => {
    const duplicateEmail = `e2e-dup-${Date.now()}@example.com`;

    // Arrange: create a user via API first (fast setup)
    const existingUser = await api.createUser({
      email: duplicateEmail,
      displayName: "Existing User",
    });

    try {
      // Act: try to create another user with the same email via UI
      await usersPage.clickCreateUser();
      const dialog = new CreateUserDialog(page);
      await dialog.fillForm({
        email: duplicateEmail,
        displayName: "Duplicate User",
      });
      await dialog.submitButton.click();

      // Assert: error toast with conflict message
      await expect(usersPage.toast).toContainText(/already exists/i);
    } finally {
      // Cleanup: remove the test user
      await api.deleteUser(existingUser.id);
    }
  });

  // ─── Cancel Flow ────────────────────────────────────
  test("cancelling the dialog does not create a user", async ({ page }) => {
    const countBefore = await usersPage.getUserCount();

    // Act: open dialog, fill form, then cancel
    await usersPage.clickCreateUser();
    const dialog = new CreateUserDialog(page);
    await dialog.fillForm({
      email: "should-not-exist@example.com",
      displayName: "Cancelled User",
    });
    await dialog.cancel();

    // Assert: user count unchanged
    const countAfter = await usersPage.getUserCount();
    expect(countAfter).toBe(countBefore);
  });
});

// ─── Test Suite: User List ──────────────────────────────────────────────────────

test.describe("User List", () => {
  let usersPage: UsersPage;
  let api: TestDataAPI;
  const testUsers: Array<{ id: number }> = [];

  test.beforeAll(async ({ request }) => {
    // Create test data via API (runs once for the suite)
    api = new TestDataAPI(request);
    for (let i = 0; i < 3; i++) {
      const user = await api.createUser({
        email: `e2e-list-${i}-${Date.now()}@example.com`,
        displayName: `List User ${i}`,
      });
      testUsers.push(user);
    }
  });

  test.afterAll(async () => {
    // Cleanup all test users
    for (const user of testUsers) {
      await api.deleteUser(user.id);
    }
  });

  test.beforeEach(async ({ page, request }) => {
    usersPage = new UsersPage(page);
    api = new TestDataAPI(request);
    await usersPage.goto();
  });

  test("displays users in a table", async () => {
    const count = await usersPage.getUserCount();
    expect(count).toBeGreaterThanOrEqual(3);
  });

  test("filters users by search query", async () => {
    await usersPage.searchFor("List User 0");

    // Verify filtered results
    const count = await usersPage.getUserCount();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("shows empty state for no results", async () => {
    await usersPage.searchFor("nonexistent-user-xyz-999");

    await expect(usersPage.emptyState).toBeVisible();
  });
});

// ─── Test Suite: User Edit (example with navigation) ─────────────────────────

test.describe("Edit User", () => {
  let usersPage: UsersPage;
  let api: TestDataAPI;
  let testUser: { id: number; email: string };

  test.beforeEach(async ({ page, request }) => {
    api = new TestDataAPI(request);
    usersPage = new UsersPage(page);

    // Create a fresh user for each edit test
    testUser = await api.createUser({
      email: `e2e-edit-${Date.now()}@example.com`,
      displayName: "Before Edit",
    });

    await usersPage.goto();
  });

  test.afterEach(async () => {
    // Cleanup
    await api.deleteUser(testUser.id);
  });

  test("edits user display name", async ({ page }) => {
    // Act: click edit on the user row
    await usersPage.clickEditUser(testUser.email);

    // Wait for edit page/dialog to load
    await page.waitForURL(`**/users/${testUser.id}/edit`);

    // Fill in new name
    const nameInput = page.getByLabel("Display name");
    await nameInput.clear();
    await nameInput.fill("After Edit");

    // Submit
    await page.getByRole("button", { name: /save/i }).click();

    // Assert: redirect back to list with success message
    await page.waitForURL("**/users");
    await expect(page.getByRole("alert")).toContainText(/updated/i);
  });
});
