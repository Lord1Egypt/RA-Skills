/**
 * South Park Commons (SPC) application client.
 *
 * SPC uses Airtable Interface forms for applications.
 * Since these are fully client-rendered SPAs, we use Playwright
 * to navigate, fill, and submit the form programmatically.
 *
 * Field labels were extracted from the rendered form via Playwright
 * and confirmed with getByLabel() — each label uniquely identifies its input.
 *
 * Important Airtable quirks:
 * - Rich text fields use contenteditable="plaintext-only" divs
 * - Location is a combobox with a search popup
 * - "How did you hear" is a visible listbox with clickable options
 * - Filling the "Which idea" field triggers progressive reveal of sub-questions
 */

import { chromium, type Page } from "playwright";

// --- Constants ---

export const SPC_APP_ID = "appxDXHfPCZvb75qk";

export const SPC_FORMS = {
  founderFellowship: {
    pageId: "pagyqQLVvYMoPT9pg",
    url: "https://airtable.com/appxDXHfPCZvb75qk/pagyqQLVvYMoPT9pg/form",
    name: "Founder Fellowship",
    description: "For founders committed to starting a venture-scale company. $400K for 7% + $600K follow-on.",
  },
  memberResidency: {
    pageId: "pagKjgMU7TbgeAYVb",
    url: "https://airtable.com/appxDXHfPCZvb75qk/pagKjgMU7TbgeAYVb/form",
    name: "Community Membership",
    description: "For technologists in the -1 to 0 phase. Up to 6 months exploring ideas at SPC.",
  },
} as const;

export type SpcFormType = keyof typeof SPC_FORMS;

export const HOW_HEARD_OPTIONS = [
  "I am an SPC Member",
  "From an SPC Member",
  "From an SPC Team Member",
  "Internet Search",
  "LinkedIn",
  "X",
  "SPC Event",
  "Word of Mouth",
  "Other",
] as const;

// --- Types ---

export interface SpcFounder {
  fullName: string;
  email: string;
  linkedin: string;
  phone?: string;
}

export interface SpcApplication {
  // Founders (up to 4, at least 1 required)
  founders: SpcFounder[];

  // Team
  roles: string;
  location: string;

  // Discovery
  howHeard: string;
  howHeardElaborate?: string;

  // Background
  financingHistory?: string;
  accomplishments: string;
  riskiestDecision: string;
  threeRecruits: string;

  // Ideas
  ideasRanked: string;
  ideaDetail: string;
  whyExcited?: string;
  expertise?: string;
  progress?: string;
  demoLink?: string;
  secondIdea?: string;
  optionalChanges?: string;
  backupIdeas?: string;

  // Opt-in
  stayInTouch?: boolean;
}

// --- Error ---

export class SpcError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "SpcError";
  }
}

// --- Playwright form filler ---

export interface SpcFillOptions {
  formType?: SpcFormType;
  headed?: boolean;
  dryRun?: boolean;
  slowMo?: number;
  onStatus?: (msg: string) => void;
}

/**
 * Fill the SPC Airtable form using Playwright.
 *
 * The form is filled in stages because Airtable progressively reveals
 * new fields as earlier ones are completed. Each stage fills a group
 * of fields, then waits for the form to potentially update.
 */
export async function fillSpcForm(
  application: SpcApplication,
  options: SpcFillOptions = {},
): Promise<{ submitted: boolean; screenshotPath?: string }> {
  const {
    formType = "founderFellowship",
    headed = false,
    dryRun = false,
    slowMo = 50,
    onStatus = () => {},
  } = options;

  const form = SPC_FORMS[formType];
  const browser = await chromium.launch({ headless: !headed, slowMo });

  try {
    const page = await browser.newPage();
    onStatus(`Navigating to ${form.name} form...`);
    await page.goto(form.url, { waitUntil: "networkidle" });

    // Wait for the form to render (Airtable SPA)
    await page.waitForSelector("textarea, input", { timeout: 30000 });
    onStatus("Form loaded. Filling fields...");

    // === Stage 1: Contact & Team (textarea/input fields) ===

    for (let i = 0; i < application.founders.length && i < 4; i++) {
      const f = application.founders[i];
      const n = i + 1;
      await fillField(page, `Full Name (Founder #${n})`, f.fullName);
      await fillField(page, `Email (Founder #${n})`, f.email);
      await fillField(page, `LinkedIn (Founder #${n})`, f.linkedin);
      if (f.phone) {
        await fillField(page, `Phone number (Founder #${n})`, f.phone);
      }
    }

    await fillField(page, "What roles do you", application.roles);

    // Location combobox — special handling
    await fillCombobox(page, application.location);

    // How did you hear — visible listbox with clickable options
    await selectListboxOption(page, application.howHeard);

    if (application.howHeardElaborate) {
      await fillField(page, "briefly elaborate", application.howHeardElaborate);
    }
    if (application.financingHistory) {
      await fillField(page, "financing history", application.financingHistory);
    }

    onStatus("Stage 1 (contact & team) done.");
    await page.waitForTimeout(500);

    // === Stage 2: Background (contenteditable fields) ===
    // These are rich text fields. We click to focus, then type via keyboard.

    await fillRichText(page, "accomplishment", application.accomplishments);
    await fillRichText(page, "riskiest decision", application.riskiestDecision);
    await fillRichText(page, "three people you would recruit", application.threeRecruits);

    onStatus("Stage 2 (background) done.");
    await page.waitForTimeout(500);

    // === Stage 3: Ideas (contenteditable fields) ===

    await fillRichText(page, "List out the specific", application.ideasRanked);
    await fillRichText(page, "Which idea from the list", application.ideaDetail);

    // Wait for progressive reveal of idea sub-questions
    await page.waitForTimeout(1500);

    // Sub-questions that appear after filling "Which idea from the list"
    if (application.whyExcited) {
      await fillRichText(page, "Why are you excited", application.whyExcited);
    }
    if (application.expertise) {
      await fillRichText(page, "What expertise do you have", application.expertise);
    }
    if (application.progress) {
      await fillRichText(page, "What progress have you made", application.progress);
    }
    if (application.demoLink) {
      await fillRichText(page, "Link us to something", application.demoLink);
    }

    if (application.secondIdea) {
      await fillRichText(page, "another idea you have explored", application.secondIdea);
    }
    if (application.optionalChanges) {
      await fillRichText(page, "did anything change", application.optionalChanges);
    }
    if (application.backupIdeas) {
      await fillRichText(page, "none of your current ideas", application.backupIdeas);
    }

    onStatus("Stage 3 (ideas) done.");

    // === Stage 4: Opt-in ===

    if (application.stayInTouch) {
      const checkbox = page.getByRole("checkbox");
      if (await checkbox.count() > 0) {
        await checkbox.first().check();
      }
    }

    onStatus("All fields filled.");

    // Screenshot for review
    const screenshotPath = `/tmp/spc-form-${Date.now()}.png`;
    await page.screenshot({ path: screenshotPath, fullPage: true });
    onStatus(`Screenshot saved: ${screenshotPath}`);

    if (dryRun) {
      onStatus("Dry run — not submitting.");
      return { submitted: false, screenshotPath };
    }

    // Submit
    const submitBtn = page.getByRole("button", { name: /submit/i });
    if (await submitBtn.count() > 0) {
      await submitBtn.click();
      await page.waitForTimeout(3000);
      const afterScreenshot = `/tmp/spc-form-submitted-${Date.now()}.png`;
      await page.screenshot({ path: afterScreenshot, fullPage: true });
      onStatus("Form submitted!");
      return { submitted: true, screenshotPath: afterScreenshot };
    } else {
      throw new SpcError("Submit button not found");
    }
  } finally {
    await browser.close();
  }
}

// --- Field helpers ---

/**
 * Fill a standard text field (input or textarea) by partial label match.
 */
async function fillField(page: Page, labelSubstring: string, value: string): Promise<void> {
  const locator = page.getByLabel(labelSubstring, { exact: false }).first();
  if (await locator.count() === 0) return;
  await locator.fill(value);
}

/**
 * Fill a rich text field (contenteditable div) by clicking and typing.
 * Playwright's fill() works on contenteditable but can be unreliable
 * in Airtable's SPA — click + keyboard.type is more robust.
 */
async function fillRichText(page: Page, labelSubstring: string, value: string): Promise<void> {
  const locator = page.getByLabel(labelSubstring, { exact: false }).first();
  if (await locator.count() === 0) return;

  await locator.click();
  await page.waitForTimeout(100);
  await page.keyboard.type(value, { delay: 5 });
  // Click away to commit the value
  await page.locator("body").click({ position: { x: 10, y: 10 } });
  await page.waitForTimeout(100);
}

/**
 * Handle Airtable's location combobox.
 * Clicks the trigger, types in the search popup (input[type=search]),
 * then selects from the controlled listbox (via aria-controls).
 */
async function fillCombobox(page: Page, value: string): Promise<void> {
  const combobox = page.getByRole("combobox").first();
  if (await combobox.count() === 0) return;

  await combobox.click();
  await page.waitForTimeout(500);

  // The search input is type="search" with placeholder="Find an option"
  const searchInput = page.locator('input[type="search"]').first();
  if (await searchInput.count() === 0) return;

  // Search with city name only (strip state/country after comma)
  const searchTerm = value.split(",")[0].trim();
  await searchInput.fill(searchTerm);
  await page.waitForTimeout(800);

  // Select from the controlled listbox (not the "How did you hear" listbox)
  const listboxId = await searchInput.getAttribute("aria-controls");
  if (listboxId) {
    const option = page.locator(`[id="${listboxId}"] [role="option"]`).first();
    if (await option.count() > 0) {
      await option.click();
      return;
    }
  }

  // Fallback
  await page.keyboard.press("Enter");
}

/**
 * Select an option from Airtable's visible listbox.
 * The "How did you hear" field renders all options as clickable items.
 */
async function selectListboxOption(page: Page, value: string): Promise<void> {
  // The listbox options might conflict with combobox options, so scope to the listbox
  const listbox = page.getByRole("listbox").first();
  if (await listbox.count() === 0) return;

  const option = listbox.getByRole("option", { name: value, exact: true }).first();
  if (await option.count() > 0) {
    await option.click();
    return;
  }

  // Fallback: find by text
  const item = listbox.getByText(value, { exact: true }).first();
  if (await item.count() > 0) {
    await item.click();
  }
}
