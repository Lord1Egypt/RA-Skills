/**
 * page-object-template.ts — Annotated page object class for Playwright E2E tests.
 *
 * Place at: e2e/pages/users.page.ts
 *
 * This template demonstrates:
 *   - Extending a base page object for shared behavior
 *   - Declaring locators as public readonly properties
 *   - Encapsulating user actions as async methods
 *   - Internal wait handling (page objects handle waits, tests handle assertions)
 *   - Composing page objects for forms and dialogs
 */

import { type Page, type Locator, expect } from "@playwright/test";

// ─── Base Page Object ───────────────────────────────────────────────────────────

/**
 * Abstract base class for all page objects.
 * Provides shared navigation and utility methods.
 */
export abstract class BasePage {
  constructor(protected readonly page: Page) {}

  /** Navigate to the page's URL. Subclasses must implement. */
  abstract goto(): Promise<void>;

  /** Wait for the page to be fully loaded (network idle). */
  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState("networkidle");
  }

  /** Get toast/notification messages (role="alert"). */
  get toast(): Locator {
    return this.page.getByRole("alert");
  }

  /** Get the primary page heading (h1). */
  get heading(): Locator {
    return this.page.getByRole("heading", { level: 1 });
  }

  /** Check if a loading spinner is visible. */
  async isLoading(): Promise<boolean> {
    return this.page.getByTestId("loading-spinner").isVisible();
  }
}

// ─── Users List Page ────────────────────────────────────────────────────────────

/**
 * Page object for the Users list page (/users).
 *
 * Usage in tests:
 *   const usersPage = new UsersPage(page);
 *   await usersPage.goto();
 *   await usersPage.searchFor("alice");
 *   const count = await usersPage.getUserCount();
 */
export class UsersPage extends BasePage {
  // ─── Locators (public, readonly) ──────────────────────
  // Use data-testid for interactive elements, role for semantic elements
  readonly createButton: Locator;
  readonly searchInput: Locator;
  readonly userTable: Locator;
  readonly emptyState: Locator;
  readonly paginationNext: Locator;
  readonly paginationPrev: Locator;

  constructor(page: Page) {
    super(page);
    this.createButton = page.getByTestId("create-user-btn");
    this.searchInput = page.getByRole("searchbox", { name: /search users/i });
    this.userTable = page.getByRole("table");
    this.emptyState = page.getByTestId("empty-state");
    this.paginationNext = page.getByRole("button", { name: /next/i });
    this.paginationPrev = page.getByRole("button", { name: /previous/i });
  }

  // ─── Navigation ──────────────────────────────────────
  async goto(): Promise<void> {
    await this.page.goto("/users");
    await this.waitForLoad();
  }

  // ─── Actions ─────────────────────────────────────────
  /** Type a search query and wait for the results API response. */
  async searchFor(query: string): Promise<void> {
    await this.searchInput.fill(query);
    // Wait for the debounced API call to complete
    await this.page.waitForResponse(
      (res) => res.url().includes("/api/v1/users") && res.status() === 200,
    );
  }

  /** Click the "Create User" button. */
  async clickCreateUser(): Promise<void> {
    await this.createButton.click();
  }

  /** Get a specific user's row by email. */
  getUserRow(email: string): Locator {
    return this.userTable.getByRole("row").filter({ hasText: email });
  }

  /** Click the edit button for a specific user row. */
  async clickEditUser(email: string): Promise<void> {
    const row = this.getUserRow(email);
    await row.getByRole("button", { name: /edit/i }).click();
  }

  /** Click the delete button for a specific user row. */
  async clickDeleteUser(email: string): Promise<void> {
    const row = this.getUserRow(email);
    await row.getByRole("button", { name: /delete/i }).click();
  }

  /** Get the total count of user rows (excluding header). */
  async getUserCount(): Promise<number> {
    const rows = this.userTable.getByRole("row");
    const count = await rows.count();
    return Math.max(0, count - 1); // Subtract header row
  }

  /** Navigate to the next page. */
  async goToNextPage(): Promise<void> {
    await this.paginationNext.click();
    await this.waitForLoad();
  }
}

// ─── Create User Dialog ─────────────────────────────────────────────────────────

/**
 * Page object for the Create User dialog/form.
 *
 * Usage in tests:
 *   const dialog = new CreateUserDialog(page);
 *   await dialog.fillForm({ email: "test@example.com", displayName: "Test" });
 *   await dialog.submit();
 */
export class CreateUserDialog {
  readonly dialog: Locator;
  readonly emailInput: Locator;
  readonly displayNameInput: Locator;
  readonly roleSelect: Locator;
  readonly submitButton: Locator;
  readonly cancelButton: Locator;

  constructor(private readonly page: Page) {
    this.dialog = page.getByRole("dialog", { name: /create user/i });
    this.emailInput = this.dialog.getByLabel("Email");
    this.displayNameInput = this.dialog.getByLabel("Display name");
    this.roleSelect = this.dialog.getByLabel("Role");
    this.submitButton = this.dialog.getByRole("button", { name: /create/i });
    this.cancelButton = this.dialog.getByRole("button", { name: /cancel/i });
  }

  /** Fill in the create user form. */
  async fillForm(data: {
    email: string;
    displayName: string;
    role?: string;
  }): Promise<void> {
    await this.emailInput.fill(data.email);
    await this.displayNameInput.fill(data.displayName);
    if (data.role) {
      await this.roleSelect.selectOption(data.role);
    }
  }

  /** Submit the form and wait for the API response. */
  async submit(): Promise<void> {
    await this.submitButton.click();
    await this.page.waitForResponse(
      (res) => res.url().includes("/api/v1/users") && res.status() === 201,
    );
  }

  /** Cancel and close the dialog. */
  async cancel(): Promise<void> {
    await this.cancelButton.click();
    await this.dialog.waitFor({ state: "hidden" });
  }
}
