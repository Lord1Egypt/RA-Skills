# CPQ Config Schema

TypeScript interfaces defining the config object shape for CPQ systems. The Builder Agent populates this shape from DOMAIN.md using the mapping rules in SKILL.md. The SPA reads and renders it.

## Root Config

```typescript
interface CPQConfig {
  app: AppConfig;
  sections: SectionDefinition[];    // Fixed by the skill — do not modify
  data: CPQData;                    // Populated by Builder Agent from DOMAIN.md
  rules: BusinessRule[];            // Populated by Builder Agent from DOMAIN.md
  roles: RoleDefinition[];          // Populated by Builder Agent from DOMAIN.md
  metadata?: ConfigMetadata;        // Open questions, mapping log reference
}
```

## App Config

```typescript
interface AppConfig {
  companyName: string;              // From DOMAIN.md Project Overview
  logoUrl: string;                  // From brandfetch
  theme: ThemeConfig;
}

interface ThemeConfig {
  primaryColor: string;             // Hex, from brandfetch or fallback "#1a1a2e"
  accentColor: string;              // Hex, from brandfetch or fallback "#3b82f6"
  mode: "light" | "dark";          // Default: "light"
  allowModeToggle: boolean;         // Default: true
}
```

## CPQ Data

```typescript
interface CPQData {
  products: Product[];              // Available catalog
  lineItems: LineItem[];            // Current quote contents (starts empty [])
  quoteSettings: QuoteSettings;     // Currency, tax, terms, pricing
}
```

## Product

```typescript
interface Product {
  id: string;                       // Slugified from product name
  name: string;                     // Exact name from DOMAIN.md
  category: string;                 // Grouping (e.g., "softener", "filter", "service")
  description?: string;             // One-liner from Entity Registry
  basePrice: number | null;         // null if "custom-quoted" or "vendor_rfq"
  pricingSource: PricingSource;
  options: ProductOption[];         // What varies when quoting this product
  active: boolean;                  // Default: true
}

type PricingSource = "catalog" | "vendor_rfq" | "cost_plus" | "tbd";

interface ProductOption {
  id: string;                       // Slugified from option name
  label: string;                    // Display name (e.g., "Size", "Valve Type")
  type: "select" | "boolean" | "number" | "text";
  choices?: string[];               // For select type — the specific values
  default?: string | number | boolean;
  required: boolean;                // Default: true for select, false for others
  affectsPrice: boolean;            // Default: false (price impact TBD in early config)
}
```

## Line Item

```typescript
interface LineItem {
  id: string;                       // Generated UUID
  productId: string;                // References Product.id
  productName: string;              // Denormalized for display
  selectedOptions: Record<string, string | number | boolean>;
  quantity: number;                 // Default: 1
  unitPrice: number;                // Calculated from basePrice + options
  total: number;                    // unitPrice * quantity
  notes?: string;
}
```

## Quote Settings

```typescript
interface QuoteSettings {
  currency: string;                 // ISO 4217 (e.g., "USD", "CAD")
  taxEnabled: boolean;
  taxLabel?: string;                // e.g., "HST", "GST", "Sales Tax"
  taxRate?: number;                 // Decimal (e.g., 0.13 for 13%)
  defaultTerms: string;            // e.g., "net30", "net45", "milestone"
  availableTerms?: string[];       // Options for the terms dropdown
  markup?: number;                  // Decimal (e.g., 0.375 for 37.5%)
  quoteFormat: "itemized" | "summary";  // Default: "itemized"
  customerName?: string;            // Set in Approve section
  customerEmail?: string;
  validUntil?: string;              // ISO date
  notes?: string;
}
```

## Business Rule

```typescript
interface BusinessRule {
  id: string;                       // BR-001, BR-002, etc.
  type: "requires" | "recommends" | "excludes" | "validates" | "computes";
  trigger: string;                  // Action that fires the rule
  condition: Record<string, any>;   // What must be true
  action: RuleAction;               // What happens
  message: string;                  // Human-readable — from DOMAIN.md rationale
  severity: "error" | "warning" | "info";
}

interface RuleAction {
  suggest?: string;                 // Product ID to suggest adding
  block?: string | boolean;         // Product ID to block, or true to block the action
  matchField?: string;              // Attribute that must match between products
  requireApproval?: string;         // Role ID that must approve
  compute?: string;                 // Formula description
}
```

## Role Definition

```typescript
interface RoleDefinition {
  id: string;                       // Slugified from role name
  label: string;                    // Display name from DOMAIN.md
  permissions: Permission[];
}

type Permission =
  | "createQuote"
  | "editQuote"
  | "selectProducts"
  | "approveQuote"
  | "approveTerms"
  | "viewReports"
  | "editCatalog"
  | "editPricing"
  | "viewQuotes";
```

## Config Metadata

```typescript
interface ConfigMetadata {
  generatedAt: string;              // ISO timestamp
  skill: string;                    // "cpq-builder"
  skillVersion: string;             // "3.0"
  verticalPreset?: string;          // "manufacturing" | "wholesale" | "services"
  openQuestions: string[];          // Carried from DOMAIN.md Open Questions
}
```

