---
name: resurface
license: MIT
description: >-
  Autonomous agent playbook to crawl, reverse-engineer, and modernly reskin ANY legacy, outdated, or frustrating website or web portal into a 2026-grade Web Extension overlay (WXT, React 19, Tailwind CSS, Zustand, Zod).
  Enforces stealth browser automation via Obscura (https://github.com/h4ckf0r0day/obscura), recursive whole-site topology mapping, interactive human-in-the-loop CAPTCHA/auth clearance, bulletproof anti-FOUC (Flash of Unstyled Content) engineering, and client-side DOM hijacking without modifying the host backend.
---

# Resurface

A production-grade engineering playbook for autonomous AI coding agents (**Antigravity, Claude Code, OpenAI Codex, Cursor, Windsurf**) to transform **any clunky, outdated, or frustrating website** into a modern, lightning-fast application.

Instead of requiring backend database access or rebuilding server-side APIs, this skill guides agents through building a **client-side overlay extension** that mounts seamlessly over the legacy host domain, intercepts and hides legacy UI before paint, preserves native authentication and form submissions, and delivers a sleek, modern experience.

---

## 1. Core Architecture Blueprint

```text
[ Legacy Host Website ] (ASP.NET / PHP / JSP / Old Rails / Table-based HTML)
       ▲                                     ▲
       │ Native Cookies & Sessions           │ Hidden DOM Ingestion & Form Submits
       │ (100% Intact & Untouched)           │ (Preserved in Background)
┌──────┴─────────────────────────────────────┴──────────────────────────────┐
│                    Modern Extension Overlay Architecture                  │
│                                                                           │
│  ┌────────────────────────┐              ┌─────────────────────────────┐  │
│  │ Anti-FOUC Gate Layer   │ ───────────▶ │ Fast CSS Loading Skeleton   │  │
│  │ (Pre-Paint CSS Hide)   │              │ (Zero Layout Shift)         │  │
│  └────────────────────────┘              └──────────────┬──────────────┘  │
│                 │                                       │                 │
│                 ▼                                       ▼                 │
│  ┌────────────────────────┐              ┌─────────────────────────────┐  │
│  │ Resilient DOM Parsers  │ ───────────▶ │ Zod Validated Domain Stores │  │
│  │ (Semantic Column Map)  │              │ (Zustand + Local Storage)   │  │
│  └────────────────────────┘              └──────────────┬──────────────┘  │
│                                                         │                 │
│                                                         ▼                 │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ Modern Presentation Layer (React 19 + Tailwind CSS + Lucide Icons)   │  │
│  │ • Elevated Navigation (Collapsible Sidebar & Modern Header)         │  │
│  │ • System-Aware Adaptive Themes (Light Sky / Deep Dark Sky)          │  │
│  │ • Local Encrypted Credential Vault (AES-GCM Auto-Fill)              │  │
│  │ • Interactive Data Tables, Modals, Badges & Single-Line Toasts      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Autonomous Execution Phases

### Phase 1: Two-Tier Ingestion Strategy (Probe vs. Obscura Stealth)

To maximize speed and avoid unnecessary browser overhead, the agent must evaluate the target site with a two-tier strategy:

#### Tier 1: Fast Probe Heuristic (Public Static Sites)
Before launching full browser instrumentation, test the target with a lightweight HTTP probe:
```bash
curl -sIL "<TARGET_URL>" | head -n 20
```
- **If the site returns HTTP 200 without Cloudflare, Turnstile, reCAPTCHA, or mandatory login walls** (e.g. public portals, corporate brochures, documentation, unauthenticated directories):
  - Do **NOT** spin up a full browser instance.
  - Run rapid parallel fetching with `fetch()` and `linkedom` in a temporary script to map and snapshot the entire site topology in seconds.

#### Tier 2: Stealth Browser Engine via Obscura (Auth / Protected / SPA Sites)
- **If the site returns HTTP 403/401, Cloudflare clearance, interactive login forms, or client-side SPA routing**:
  - The agent **must exclusively use [Obscura](https://github.com/h4ckf0r0day/obscura)** for session persistence and stealth execution.

```bash
# Verify or install Obscura
if ! command -v obscura &> /dev/null; then
  echo "Obscura not found. Installing from source..."
  git clone https://github.com/h4ckf0r0day/obscura.git ~/.obscura
  cd ~/.obscura && bun install || npm install
fi

# Launch stealth session
obscura open "<TARGET_URL>" --stealth --persist-cookies
```

#### Interactive Human-in-the-Loop Auth Gate
- **Never attempt to automate, defeat, or spoof CAPTCHAs, biometric challenges, or multi-factor 2FA.**
- If a login form, Cloudflare Turnstile, reCAPTCHA, hCaptcha, or 2FA prompt is detected:
  1. The agent must pause and notify the user:
     > *"Authentication or CAPTCHA detected on `<TARGET_URL>`. Please complete login in the Obscura browser window. Once you reach the post-login dashboard, reply with 'logged in' so I can resume cataloging."*
  2. Wait for user confirmation.
  3. Validate that session cookies/tokens are active before proceeding.

---

### Phase 2: Recursive Deep Discovery & Whole-Site Topology Mapping

**MANDATORY RULE:** The agent must map the **entire website topology recursively** before scaffolding or writing any UI code. A partial redesign leads to broken navigation and fragmented user flows.

#### 1. Recursive Crawling Algorithm
1. **Breadth-First Exploration Queue:**
   - Initialize `queue = [landingUrl]`, `visited = new Set()`.
   - Constrain all crawling strictly to the same origin (`targetOrigin`).
2. **Multi-Level Navigation Discovery:**
   - **Primary Nav:** Top bar items, brand links, and main menu bars.
   - **Nested Dropdowns & Flyouts:** Trigger hover/click states on menu buttons (`[data-toggle="dropdown"]`, `.dropdown-toggle`, `li.has-submenu`) to expose and capture sub-menu links.
   - **Sidebar Accordions:** Expand all collapsed tree views and sidebar groups.
   - **Secondary & Tertiary Tabs:** Click across tab headers (`[role="tab"]`, `.nav-tabs a`, `.tab-header`) on every visited page to load and snapshot sub-views.
   - **Nested Detail Links:** Detect tabular links (e.g., clicking on an invoice row `<td><a href="/Invoice/1234">` or a student semester link) to catalog detail view templates.
3. **Canonicalization & Loop Prevention:**
   - Normalize paths by stripping ephemeral query params (`?session_id=`, `?_t=`, cache busters) while preserving structural state params (`?id=`, `?tab=`, `?year=`).
   - Stop recursion when depth exceeds maximum configured threshold (default: 4 levels deep) or when all same-origin links in the visited set have been exhausted.

#### 2. Artifact Generation: `audit/site-graph.json` & `audit/manifest.json`

Save the complete hierarchical topology so the modern React navigation can be scaffolded with 100% route coverage:

```json
{
  "targetOrigin": "https://legacy-site.example.com",
  "generatedAt": "2026-11-14T21:45:00Z",
  "totalRoutes": 24,
  "routeTree": [
    {
      "id": "academics",
      "label": "Academics",
      "icon": "GraduationCap",
      "path": "/Academics",
      "children": [
        {
          "id": "marks",
          "label": "Marks & Assessment",
          "path": "/Academics/Marks",
          "domSnapshot": "audit/dom/academics-marks.html",
          "type": "tabular",
          "subTabs": ["Quizzes", "Assignments", "Exams"],
          "actions": ["form#download-marksheet"]
        }
      ]
    }
  ]
}
```

Every discovered page must have its complete DOM tree saved under `audit/dom/<slug>.html` for offline test development and resilient selector engineering.

---

### Phase 3: Fighting & Eliminating FOUC (Flash of Unstyled Content)

FOUC is the fatal flaw in client-side extension reskins: seeing the ugly legacy site flash for 300ms before the modern UI renders breaks user trust.

Here is the exact **5-stage anti-FOUC pipeline** developed and proven in SuperFlex:

#### 1. Declarative Manifest Injection at `document_start`
Never inject CSS asynchronously inside React or via JavaScript `document.createElement("link")`. CSS must be declared in the extension manifest so the browser layout engine applies it **before the first DOM paint**:
```typescript
// wxt.config.ts
export default defineConfig({
  manifest: {
    content_scripts: [
      {
        matches: ["https://legacy-site.example.com/*"],
        css: ["content-scripts/content.css"],
        js: ["content-scripts/content.js"],
        run_at: "document_start", // CRITICAL: Run before DOM paint
      },
    ],
  },
});
```

#### 2. Immediate Pre-Paint Selector Blocker
In `content.css`, inject a high-specificity hiding rule that suppresses legacy layout containers immediately, while leaving the root container and portal alerts intact:
```css
/* Instantly hide legacy portal layout before first render */
html:not(.legacy-reveal) body > *:not(#modern-app-root):not(#loading-skeleton):not(#toast-container) {
  display: none !important;
}

/* Ensure clean font and background canvas immediately */
html, body {
  background: var(--bg-surface, #ffffff) !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
}
```

#### 3. Lightweight Zero-Dependency Loading Skeleton
Mount a pure HTML/CSS spinner or skeleton at the top of the body immediately during parse:
```typescript
const skeleton = document.createElement("div");
skeleton.id = "loading-skeleton";
skeleton.innerHTML = `<div class="skeleton-loader"><div class="skeleton-shimmer"></div></div>`;
document.body.insertBefore(skeleton, document.body.firstChild);

// Once React finishes initial render:
skeleton.remove();
```

#### 4. Stripping Conflicting Legacy Stylesheets
Legacy websites often bundle outdated frameworks (Bootstrap 2/3, old Metro UI, Joomla CSS) that leak through global tags. Identify and eliminate them dynamically:
```typescript
const unwantedStyles = [
  'link[href*="template.css"]',
  'link[href*="system.css"]',
  'link[href*="style.bundle.css"]',
];

unwantedStyles.forEach((selector) => {
  document.querySelectorAll<HTMLLinkElement>(selector).forEach((el) => el.remove());
});
```

#### 5. Background Legacy DOM Preservation
**NEVER wipe `document.body.innerHTML = ""`!**
The legacy DOM must remain alive and accessible in the background so:
- Semantic data parsers can query tables, transcript data, and profile info anytime.
- Hidden CSRF tokens (`__RequestVerificationToken`, session cookies, ASP.NET ViewStates) remain available for programmatic form submits.

#### 6. Dynamic Favicon Interception & High-Res Replacement
Legacy sites almost always feature low-resolution (16x16 .ico) or missing favicons. Inject and replace the favicon immediately at `document_start` so the browser tab icon updates before page paint:
```typescript
export function replaceFavicon(iconPath = "icon.svg") {
  const iconUrl = browser.runtime.getURL(iconPath);
  let favicon = document.querySelector<HTMLLinkElement>("link[rel~='icon']");
  if (!favicon) {
    favicon = document.createElement("link");
    favicon.rel = "icon";
    document.head.appendChild(favicon);
  }
  favicon.type = iconPath.endsWith(".svg") ? "image/svg+xml" : "image/png";
  favicon.href = iconUrl;
}
```
*(Ensure `icon.svg` and PNG icons are declared in `web_accessible_resources` in `wxt.config.ts` so the host page is permitted to load them).*

#### 7. Zero-Flash Adaptive Theme Engine (Light / Dark Mode)
A white flash in dark mode is as jarring as FOUC. The theme class (`dark`) must be determined and attached to `document.documentElement` synchronously **before React renders**:

1. **Pre-Paint Synchronous Theme Application:**
```typescript
export type ThemeMode = "light" | "dark" | "system";

export function getResolvedTheme(mode: ThemeMode): "light" | "dark" {
  if (mode === "system") {
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  return mode;
}

export function initThemePrePaint() {
  const saved = (localStorage.getItem("resurface-theme") as ThemeMode) || "system";
  const resolved = getResolvedTheme(saved);
  document.documentElement.classList.toggle("dark", resolved === "dark");
}
```

2. **Tailwind v4 Theme Tokens (`src/styles/tailwind.css`):**
```css
@import "tailwindcss";

@layer base {
  :root {
    --bg-surface: #f8fafc;
    --bg-card: #ffffff;
    --text-primary: #0f172a;
    --text-muted: #64748b;
    --border-card: #e2e8f0;
  }

  .dark {
    --bg-surface: #0b0f17;
    --bg-card: #131b2e;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
    --border-card: #1e293b;
  }
}
```

3. **Persistent Theme Store (`src/stores/themeStore.ts`):**
```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface ThemeState {
  mode: ThemeMode;
  setMode: (mode: ThemeMode) => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      mode: "system",
      setMode: (mode) => {
        set({ mode });
        localStorage.setItem("resurface-theme", mode);
        const resolved = getResolvedTheme(mode);
        document.documentElement.classList.toggle("dark", resolved === "dark");
      },
    }),
    { name: "resurface-theme-store" }
  )
);
```

---

### Phase 4: Battle-Tested Toolchain & Pinned Dependencies

> [!CAUTION]
> **VITE 6 & TAILWIND V4 COMPATIBILITY PITFALL:**
> Do **NOT** install `@tailwindcss/vite` inside WXT projects. It causes Vite pre-bundle optimizer collisions on virtual content script entrypoints (`virtual:wxt-content-script-main-world-entrypoint?`).
> Do **NOT** let `@wxt-dev/module-react` install loose unpinned nested `@vitejs/plugin-react` dependencies, or it will attempt to import the deprecated `vite/internal` subpath.
> **Always use `@tailwindcss/postcss` with `postcss.config.ts` and pin `vite@^6.4.5`.**

#### 1. Recommended `package.json` Template
```json
{
  "name": "my-modern-overlay",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "wxt",
    "build": "wxt build",
    "zip": "wxt zip"
  },
  "dependencies": {
    "@tailwindcss/postcss": "^4.1.13",
    "clsx": "^2.1.1",
    "lucide-react": "^0.487.0",
    "postcss": "^8.5.6",
    "react": "^19.2.3",
    "react-dom": "^19.2.3",
    "tailwind-merge": "^3.7.0",
    "tailwindcss": "^4.1.13",
    "zod": "^3.24.2",
    "zustand": "^5.0.16"
  },
  "devDependencies": {
    "@types/chrome": "^0.0.308",
    "@types/react": "^19.0.10",
    "@types/react-dom": "^19.0.4",
    "@vitejs/plugin-react": "^4.2.1",
    "@wxt-dev/module-react": "^1.2.2",
    "autoprefixer": "^10.4.21",
    "typescript": "^5.7.3",
    "vite": "^6.4.5",
    "wxt": "^0.21.5"
  }
}
```

#### 2. `postcss.config.ts`
```typescript
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

#### 3. `wxt.config.ts`
```typescript
import { defineConfig } from "wxt";

export default defineConfig({
  srcDir: "src",
  outDir: "dist",
  outDirTemplate: "",
  modules: ["@wxt-dev/module-react"],
  manifest: {
    name: "Modern Overlay",
    description: "2026-grade modern UI overlay",
    version: "1.0.0",
    permissions: ["storage"],
    icons: {
      16: "icon-16.png",
      32: "icon-32.png",
      48: "icon-48.png",
      128: "icon-128.png",
    },
    host_permissions: ["https://<TARGET_DOMAIN>/*"],
    web_accessible_resources: [
      {
        resources: [
          "icon.svg",
          "icon-16.png",
          "icon-32.png",
          "icon-48.png",
          "icon-128.png",
        ],
        matches: ["<all_urls>"],
      },
    ],
  },
});
```

#### 4. Instant 1-Shot Icon Generator
Every Chrome MV3 extension requires PNG icons. Avoid broken builds by generating them immediately in `public/`:
```bash
cat << 'EOF' > public/icon.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6" />
      <stop offset="100%" stop-color="#1d4ed8" />
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#g)" />
  <path d="M40 38h48v12L56 78h32v12H38V78l32-28H40V38z" fill="#ffffff" />
</svg>
EOF

for size in 16 32 48 128; do
  rsvg-convert -w $size -h $size public/icon.svg -o public/icon-$size.png 2>/dev/null || \
  magick public/icon.svg -resize ${size}x${size} public/icon-$size.png
done
```

---

### Phase 5: Bulletproof Content Script Boilerplate

Use this standardized, robust pattern in `src/entrypoints/content.tsx`:

```tsx
import { defineContentScript } from "wxt/utils/define-content-script";
import { createRoot } from "react-dom/client";
import { App } from "../components/App";
import { replaceFavicon } from "../utils/favicon";
import { initThemePrePaint } from "../utils/theme";
import "../styles/tailwind.css";

export default defineContentScript({
  matches: ["https://<TARGET_DOMAIN>/*"],
  main() {
    // 1. Synchronous Pre-Paint Theme & Favicon Injection
    initThemePrePaint();
    replaceFavicon("icon.svg");

    // 2. Anti-FOUC Gate: Theme-aware Pre-paint Skeleton
    const isDark = document.documentElement.classList.contains("dark");
    const skeleton = document.createElement("div");
    skeleton.id = "app-skeleton";
    skeleton.style.cssText = "position: fixed; inset: 0; z-index: 999999; background: " + (isDark ? "#0b0f17" : "#f8fafc") + ";";
    skeleton.innerHTML = `
      <div style="height: 64px; background: ${isDark ? "#131b2e" : "#ffffff"}; border-bottom: 1px solid ${isDark ? "#1e293b" : "#e2e8f0"}; display: flex; align-items: center; padding: 0 24px;">
        <div style="width: 120px; height: 24px; background: ${isDark ? "#1e293b" : "#e2e8f0"}; border-radius: 6px;"></div>
      </div>
      <div style="max-width: 1200px; margin: 32px auto; padding: 0 24px;">
        <div style="height: 380px; background: ${isDark ? "#131b2e" : "#ffffff"}; border-radius: 16px; border: 1px solid ${isDark ? "#1e293b" : "#e2e8f0"};"></div>
      </div>
    `;
    document.documentElement.appendChild(skeleton);

    // 3. Dynamic Legacy Stylesheet Stripper
    const stripLegacyCss = () => {
      document.querySelectorAll<HTMLLinkElement>(
        'link[href*="template.css"], link[href*="system.css"], link[href*="general.css"]'
      ).forEach((el) => el.remove());
    };
    stripLegacyCss();
    document.addEventListener("DOMContentLoaded", stripLegacyCss);

    // 4. React Mount Handler
    const onReady = () => {
      let rootContainer = document.getElementById("modern-app-root");
      if (!rootContainer) {
        rootContainer = document.createElement("div");
        rootContainer.id = "modern-app-root";
        document.body.insertBefore(rootContainer, document.body.firstChild);
      }

      const root = createRoot(rootContainer);
      root.render(<App />);

      setTimeout(() => skeleton.remove(), 50);
    };

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", onReady, { once: true });
    } else {
      onReady();
    }
  },
});
```

---

### Phase 6: Resilient Semantic Parsers

Legacy sites often use unsemantic `<table>` layouts without classes or IDs. Parsers must be resilient against minor layout changes.

#### Semantic Table Parsing Pattern:
```typescript
import { z } from "zod";

export const InvoiceSchema = z.object({
  id: z.string().trim(),
  title: z.string().trim(),
  date: z.string().trim(),
  status: z.enum(["Paid", "Pending", "Overdue"]).catch("Pending"),
  amount: z.coerce.number().default(0),
});

export type InvoiceItem = z.infer<typeof InvoiceSchema>;

export function parseInvoicesTable(doc: Document | Element): InvoiceItem[] {
  const table = doc.querySelector("table.data-grid") || doc.querySelector("table");
  if (!table) return [];

  // Map header text to column indices dynamically
  const headers = Array.from(table.querySelectorAll("th, tr:first-child td"))
    .map((el) => el.textContent?.trim().toLowerCase() || "");

  const idCol = headers.findIndex((h) => h.includes("invoice") || h.includes("#"));
  const titleCol = headers.findIndex((h) => h.includes("description") || h.includes("item"));
  const dateCol = headers.findIndex((h) => h.includes("date"));
  const statusCol = headers.findIndex((h) => h.includes("status"));
  const amountCol = headers.findIndex((h) => h.includes("amount") || h.includes("total"));

  const rows = Array.from(table.querySelectorAll("tbody tr, tr")).slice(1);
  return rows.map((row) => {
    const cells = Array.from(row.querySelectorAll("td")).map((td) => td.textContent?.trim() || "");
    return InvoiceSchema.parse({
      id: cells[idCol] || "",
      title: cells[titleCol] || "",
      date: cells[dateCol] || "",
      status: cells[statusCol] || "Pending",
      amount: cells[amountCol]?.replace(/[^0-9.]/g, "") || "0",
    });
  });
}
```

---

### Phase 7: Form & Action Proxying

When a user submits a modern form or clicks an action button (e.g., "Download Statement", "Submit Timesheet"):

1. Do not reinvent the legacy server API.
2. Locate the corresponding original hidden form in the legacy DOM.
3. Synchronize the input values from your modern form into the legacy hidden inputs.
4. Trigger the legacy submit event programmatically:
```typescript
export function proxyLegacyFormSubmit(formSelector: string, fieldValues: Record<string, string>) {
  const legacyForm = document.querySelector<HTMLFormElement>(formSelector);
  if (!legacyForm) throw new Error(`Legacy form ${formSelector} not found`);

  // Update hidden inputs
  Object.entries(fieldValues).forEach(([name, value]) => {
    let input = legacyForm.querySelector<HTMLInputElement>(`input[name='${name}']`);
    if (!input) {
      input = document.createElement("input");
      input.type = "hidden";
      input.name = name;
      legacyForm.appendChild(input);
    }
    input.value = value;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });

  // Submit through native form submission so cookies and CSRF pass naturally
  legacyForm.submit();
}
```

---

## 3. Quality Gates & Verification Checklist

- [ ] **Stealth Verification:** Target crawled via two-tier strategy (lightweight probe or Obscura) with clean cookie capture.
- [ ] **Zero FOUC:** No visual glitch or flash of the legacy page on fast or slow refresh.
- [ ] **Favicon Intercepted:** Modern vector / high-res icon replaces the legacy 16px .ico on tab mount.
- [ ] **Zero-Flash Theme Engine:** Light / Dark mode persists with synchronous pre-paint class application; zero white-flash on reload.
- [ ] **Pinned Toolchain:** Extension built using pinned `vite@^6.4.5`, `@tailwindcss/postcss`, and `wxt@^0.21.5` without virtual entrypoint collisions.
- [ ] **Asset Completeness:** PNG icons (16, 32, 48, 128px) generated and referenced in `wxt.config.ts`.
- [ ] **Data Integrity:** 100% of data values match the legacy portal (verified with snapshot unit tests in Vitest).
- [ ] **Native Sessions Preserved:** Navigating routes does not invalidate authentication or drop cookies.
- [ ] **Fallback Toggle:** User can switch back to the "Original View" anytime with a persistent setting toggle.
- [ ] **Least-Privilege Permissions:** Manifest strictly requests host permissions for the targeted domain only.
