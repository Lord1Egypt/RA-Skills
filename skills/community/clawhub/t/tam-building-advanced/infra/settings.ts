// The ICP gates every company passes through, whatever source found it. The
// source filters decide what you buy; these decide what counts. They are read
// by the `status` and `exclusion_reason` columns of tam_accounts, so moving a
// threshold re-gates every company at the next sync with no other edit. A
// company that fails one is kept, flagged `out_of_scope` with the reason, so the
// report can say what each source returned that was not your market.

// PLACEHOLDER: the size band from `context/icp.md`, in employees on LinkedIn.
// Read from the company page, not from the size a source reported: the two
// disagree often enough to matter.
export const minEmployees = 51;
export const maxEmployees = 1000;

// PLACEHOLDER: headquarters countries, as the two-letter codes LinkedIn returns
// in `hq_country`.
export const countries = ["US", "CA", "GB", "IE", "FR", "DE", "NL", "ES"];

// PLACEHOLDER: your categories. Use the values of the industry field in your
// CRM, so the TAM, the CRM and the reports speak the same language. Every
// company is classified into one of these from its own description, never
// from a provider's industry label.
export const inScopeCategories = [
  "B2B SaaS",
  "AI software",
  "Developer tools",
  "Data infrastructure",
  "Cloud software",
  "Cybersecurity",
  "Fintech software",
];

// What a company can be instead. Keep "Not enough information": a thin page
// is a coverage gap, not a verdict, and it is flagged for review rather than
// thrown out.
export const outOfScopeCategories = [
  "IT services or consulting",
  "Agency",
  "Consumer product",
  "Financial institution",
  "Hardware or manufacturing",
  "Other business",
];
export const unknownCategory = "Not enough information";

// How sure the classifier must be that a page is a subsidiary, a regional or
// country page, or an acquired brand before it is flagged out of scope (0 to
// 1). Read the flagged rows of the pilot: raise it if independent companies
// are flagged, lower it if "Acme France" pages get through.
export const subsidiaryThreshold = 0.5;

// How many companies each Exa query asks for (1 to 100). Exa bills per search
// plus per result past the tenth, so the queries times this is the cap.
export const exaResultsPerQuery = 50;

// PLACEHOLDER: the Exa queries, one per category and country, written the way a
// buyer would describe the company, not the way a database files it. They live
// here so every rebuild runs the same queries and the diff shows what changed.
// Start with the categories you expect providers to file under the wrong
// industry. tam_source_exa runs each one once per sync, at most 50.
export const exaQueries = [
  "AI agent platform headquartered in France, 50 to 1,000 employees, selling to businesses",
  "Developer tools company headquartered in Germany, 50 to 1,000 employees, selling to software teams",
];
