/**
 * SendPulse UI audit — renders a page in real Chrome, in both themes, and reports the mistakes
 * that are invisible in the source and obvious on screen.
 *
 *   npm i -D playwright && npx playwright install chrome     # once, in the app repo
 *   node verify.mjs http://localhost:5173                    # or a file:// URL
 *
 * Run it from the repo that installed playwright — this file resolves it from the working
 * directory, because it normally lives outside the repo it audits.
 *   node verify.mjs http://localhost:5173 --app-prefix app-  # your own classes, not flagged
 *
 * --app-prefix is repeatable and accepts a comma-separated list, because an existing app usually
 * has many prefixes rather than one. Never declare a prefix the bundle already owns (color-, gap-,
 * btn-, …): it hides real findings — `color-muted` is not a class, `color-muted-link` is.
 *
 * Exits non-zero when something is wrong, so it drops into a pre-commit hook or CI as-is.
 *
 * The first check is the one that matters most: every class in the DOM is looked up in
 * classes.txt, so an invented class — the usual reason a screen stops looking like SendPulse —
 * is caught mechanically instead of in review. It has to work off the shipped list: the CDN
 * sends `access-control-allow-origin: https://login.sendpulse.com`, so the page cannot read
 * the bundle's own cssRules to ask it directly.
 */
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
// First non-flag argument, so `--app-prefix app- <url>` works in either order.
const url = args.find((a, i) => !a.startsWith("--") && !/^--app-prefix$/.test(args[i - 1]));
// Repeatable, and each value may itself be a comma-separated list. Indexed by position rather
// than indexOf, so two identical flags don't both resolve to the first one's value.
const appPrefixes = args
  .flatMap((a, i) => {
    if (!a.startsWith("--app-prefix")) return [];
    const inline = a.startsWith("--app-prefix=") ? a.slice("--app-prefix=".length) : null;
    return (inline ?? args[i + 1] ?? "").split(",");
  })
  .map((p) => p.trim())
  .filter(Boolean);

if (!url) {
  console.error("usage: node verify.mjs <url> [--app-prefix app-]...   (repeatable, comma-separated)");
  process.exit(2);
}

const KNOWN = new Set(
  readFileSync(resolve(here, "classes.txt"), "utf8").split("\n").filter(Boolean),
);
// The classes bundle-fixes.css itself introduces, read from the file so the two never drift.
for (const m of readFileSync(resolve(here, "bundle-fixes.css"), "utf8").matchAll(/\.([a-zA-Z][\w-]*)/g))
  KNOWN.add(m[1]);
// The bundle defines .ma-dark but not its light counterpart; both are theme hooks, not styling.
KNOWN.add("ma-light");
const ICONS = new Set(
  readFileSync(resolve(here, "icons.txt"), "utf8").split("\n").filter(Boolean),
);
// The custom properties the bundle reads and never defines — tokens.css is what supplies them.
const TOKENS = readFileSync(resolve(here, "tokens.css"), "utf8")
  .split("\n")
  .map((l) => l.match(/^\s*(--[\w-]+)\s*:/)?.[1])
  .filter(Boolean);

// Runs in the page. Playwright passes one argument, so everything arrives in one object.
const audit = ({ known: knownList, icons: iconList, tokens, prefixes, theme }) => {
  const known = new Set(knownList);
  const icons = new Set(iconList);
  const out = [];
  const add = (check, detail) => out.push({ check, detail });
  const sel = (s) => [...document.querySelectorAll(s)];
  const label = (el) =>
    `<${el.tagName.toLowerCase()} class="${el.className}">`.slice(0, 120);

  // 1. classes the bundle does not define
  const unknown = new Map();
  for (const el of sel("*")) {
    for (const c of el.classList) {
      if (known.has(c)) continue;
      if (c.startsWith("icon-")) {
        if (!icons.has(c.slice(5))) unknown.set(c, "no such sp_icons glyph");
        continue;
      }
      if (prefixes.some((p) => c.startsWith(p))) continue;
      unknown.set(c, label(el));
    }
  }
  for (const [c, where] of unknown) add("class not in the bundle", `.${c} — ${where}`);

  // 2. a second icon font
  for (const el of sel('[class*="glyphicon"]'))
    add("Bootstrap glyphicon used", `${label(el)} — use sp-icon icon-*`);

  // 3. the page background the dark build's reset gets wrong. Two ways to fail it: an unpainted
  // body, and — the actual gap of non-negotiable #4 — a body left white in the dark build, which
  // the reset does on its own and which looks fine until someone opens dark.
  const bodyBg = getComputedStyle(document.body).backgroundColor;
  if (/rgba\(0, 0, 0, 0\)|transparent/.test(bodyBg)) {
    add("body has no background", "the dark build's reset ships #fff — paint body yourself");
  } else if (theme === "dark") {
    const rgb = (bodyBg.match(/\d+/g) || []).slice(0, 3).map(Number);
    if (rgb.length === 3 && rgb.every((c) => c > 240))
      add(
        "body is white in the dark build",
        `${bodyBg} — the reset ships #fff in both builds; paint it yourself (tokens.css + bundle-fixes.css)`,
      );
  }

  // 4. native widgets follow the theme
  const rootStyle = getComputedStyle(document.documentElement);
  if (!rootStyle.colorScheme || rootStyle.colorScheme === "normal")
    add("color-scheme not declared", "select popups, scrollbars and date pickers stay light");

  // 5. the properties the bundle reads and never defines
  const missing = tokens.filter((t) => !rootStyle.getPropertyValue(t).trim());
  if (missing.length)
    add("custom properties undefined", `${missing.length} missing: ${missing.slice(0, 6).join(" ")}${missing.length > 6 ? " …" : ""}`);

  // 6. a competing font
  const font = getComputedStyle(document.body).fontFamily;
  if (!/Onest/i.test(font)) add("body font is not Onest", font);

  // 7. .badge-status is a 10x10 dot, so text in it clips
  for (const el of sel(".badge-status"))
    if (el.textContent.trim()) add("text inside .badge-status", `${label(el)} — dot + sibling label`);

  // 8. .list-divided never resets list-style
  for (const el of sel(".list-divided"))
    if (!el.classList.contains("list-unstyled") && getComputedStyle(el).listStyleType !== "none")
      add(".list-divided shows bullets", `${label(el)} — add .list-unstyled`);

  // 9. the dropped .nav foundation
  for (const el of sel(".nav-tabs > li"))
    if (getComputedStyle(el).float === "none") {
      add(".nav foundation missing", "tabs are stacking vertically — copy bundle-fixes.css");
      break;
    }

  // 10. the .input-group whose controls stack instead of sitting side by side.
  // Test the symptom, not the mechanism: the group itself computes `table` even when broken
  // (Chrome refuses display:table-cell on <input>/<select>, and the bundle floats them at
  // width:100%), so the parent's display proves nothing.
  for (const el of sel(".input-group")) {
    const kids = [...el.children].filter(
      (k) => k.matches(".form-control, .input-group-addon, .input-group-btn"),
    );
    if (kids.length < 2) continue;
    const box = el.getBoundingClientRect();
    const stacked = kids.every((k) => {
      const b = k.getBoundingClientRect();
      return Math.abs(b.left - box.left) < 2 && b.width > box.width - 2;
    });
    if (stacked)
      add(
        ".input-group controls are stacked",
        `${label(el)} — each child claims the full width; see bundle-fixes.css (.input-group-fit)`,
      );
  }

  // 11. the paid alert's badge must be its own child and must render
  for (const el of sel(".has-paid-badge")) {
    const badge = el.querySelector(":scope > .badge-paid");
    if (!badge) add(".has-paid-badge without a .badge-paid child", label(el));
    else if (!badge.textContent.trim() && !badge.offsetWidth)
      add(".badge-paid collapsed", "an empty inline span has no box — ship &nbsp;");
  }

  // 12. an icon-only control with nothing to read out
  for (const el of sel("button, a, [role=button]")) {
    if (el.textContent.trim()) continue;
    if (!el.querySelector(".sp-icon, .social-icon, .caret, .avatar")) continue;
    if (el.getAttribute("aria-label") || el.getAttribute("title")) continue;
    add("icon-only control has no accessible name", label(el));
  }

  // 13. .sp-icon has no margin of its own outside .btn / .dropdown-menu
  for (const el of sel(".sp-icon")) {
    const next = el.nextSibling;
    if (!next || !next.textContent?.trim()) continue;
    if (el.closest(".btn, .dropdown-menu")) continue;
    if (parseFloat(getComputedStyle(el).marginRight) > 0) continue;
    add("icon touching its label", `${label(el)} — add .margin-right-5`);
  }

  // 14. the app must fill the host frame: no outer gutter, no width cap, no centring
  const COMPONENT = ".panel, .well, .alert, .list-group, .form-group, .table, .side-panel";
  const frame = [document.documentElement, document.body];
  let node = document.body;
  for (let depth = 0; depth < 3; depth++) {
    const kids = [...node.children].filter((el) => !/^(SCRIPT|STYLE|LINK)$/.test(el.tagName));
    if (kids.length !== 1 || kids[0].matches(COMPONENT)) break;
    node = kids[0];
    frame.push(node);
  }
  for (const el of frame) {
    const st = getComputedStyle(el);
    if (st.maxWidth !== "none")
      add("width cap on the app root", `${label(el)} — max-width ${st.maxWidth}; the host owns the frame`);
    // getComputedStyle resolves `margin: 0 auto` to equal pixel values, so centring and a plain
    // symmetric margin look identical here — and both are the same mistake.
    const ml = parseFloat(st.marginLeft);
    if (ml > 0 && ml === parseFloat(st.marginRight))
      add("outer margin on the app root", `${label(el)} — ${st.marginLeft} each side; the app fills its frame`);
    if (el !== document.documentElement && el !== document.body)
      for (const side of ["paddingLeft", "paddingRight", "paddingTop"])
        if (parseFloat(st[side]) > 0) {
          add("outer gutter on the app root", `${label(el)} — ${side} ${st[side]}; .panel-body already insets`);
          break;
        }
  }

  // 15. the status dot that `.list-group-item .badge` out-specifies (gaps.md). Test the colour the
  //      modifier is supposed to produce, not the muted grey it loses to: the grey differs between
  //      the two builds, the four dot colours do not.
  const DOT = {
    "badge-status-success": "rgb(0, 177, 117)",
    "badge-status-primary": "rgb(66, 139, 202)",
    "badge-status-warning": "rgb(255, 155, 70)",
    "badge-status-danger": "rgb(248, 104, 80)",
  };
  for (const el of sel(".list-group-item [class*='badge-status-']")) {
    const mod = [...el.classList].find((c) => DOT[c]);
    if (!mod) continue;
    const got = getComputedStyle(el).backgroundColor;
    if (got !== DOT[mod])
      add(
        "status dot is the wrong colour inside a .list-group-item",
        `${label(el)} — ${got}, expected ${DOT[mod]}; .list-group-item .badge out-specifies the modifier, so copy bundle-fixes.css`,
      );
  }

  // 16. .avatar is inline-block with no vertical-align, so beside a label it sits below the baseline.
  for (const el of sel(".dropdown-toggle > .avatar, .dropdown-menu .avatar")) {
    if (getComputedStyle(el).verticalAlign === "baseline")
      add(
        ".avatar hangs below the baseline",
        `${label(el)} — needs vertical-align:middle; copy bundle-fixes.css`,
      );
  }

  // 17. the bundle ships no modal JS and no backdrop element, so a shown .modal is the app's job:
  //     display + .in on the dialog, its own .modal-backdrop, and modal-open on <body>.
  for (const el of sel(".modal")) {
    if (getComputedStyle(el).display === "none") continue;
    // Same escape hatch as check 20: a reference page pins a dialog open to show it.
    if (el.closest("[data-sp-audit-ignore]")) continue;
    if (!document.querySelector(".modal-backdrop"))
      add("modal shown with no backdrop", `${label(el)} — render your own .modal-backdrop.fade.in`);
    if (!document.body.classList.contains("modal-open"))
      add("modal shown without modal-open on body", `${label(el)} — the page scrolls behind it`);
    if (!el.classList.contains("in"))
      add("modal shown without .in", `${label(el)} — only .in animates the dialog into place`);
  }

  // 18. Classes the bundle defines and does not implement (gaps.md). They pass the vocabulary
  //     check above and still do nothing, so they are worth naming — but the fix is your own CSS
  //     or different markup, not a different class name, which is why this is one grouped note.
  const INERT = {
    accordion: "only sets width — build it from .panel-group + .collapse/.in",
    "tab-content": "there is no generic .tab-content rule — style the panel yourself",
    "bootstrap-select": "the plugin's own CSS is a vendor file the bundle does not carry",
    "settings-toggle-btn-sm": "internally inconsistent in the bundle — use the default size",
  };
  const inert = Object.keys(INERT).filter((c) => document.querySelector("." + c));
  if (inert.length)
    add(
      "styled but inert",
      inert.map((c) => `.${c} (${INERT[c]})`).join("; ") + " — see gaps.md",
    );

  // 19. .settings-toggle-radius is positioned only by descendant selectors, so as a sibling of the
  //     label it lands on top of the text instead of beside it. Measured, not inferred.
  for (const el of sel(".settings-toggle-radius")) {
    const knob = el.getBoundingClientRect();
    if (!knob.width) continue;
    for (const sib of el.parentElement?.children ?? []) {
      if (sib === el || !sib.textContent.trim()) continue;
      const text = sib.getBoundingClientRect();
      const overlaps =
        knob.left < text.right - 2 && knob.right > text.left + 2 &&
        knob.top < text.bottom - 2 && knob.bottom > text.top + 2;
      if (overlaps) {
        add(
          ".settings-toggle-radius sits over its label",
          `${label(el)} — nest the knob inside the label span, not beside it`,
        );
        break;
      }
    }
  }

  // 20. the theme belongs to the host, so the app must not offer a control for it.
  //     data-sp-audit-ignore exists for reference pages like kitchen-sink.html, which are browsed
  //     rather than embedded; an integration has no legitimate use for it.
  const THEME_CONTROL = /(dark|light)\s*(theme|mode)|theme\s*(switch|toggle|selector)|(switch|toggle)\s*(the\s*)?theme/i;
  for (const el of sel("button, a, [role=button], label, select")) {
    if (el.closest("[data-sp-audit-ignore]")) continue;
    if (THEME_CONTROL.test(el.textContent || ""))
      add("theme switcher in the app", `${label(el)} — the host passes ?theme=; read it, don't offer it`);
  }

  return out;
};

// This script normally lives outside the repo it audits (in the skill directory), and Node resolves
// bare imports from the *importing file's* tree — so a plain `import "playwright"` cannot see the
// `npm i -D playwright` in the app. Resolve it from the working directory instead.
let chromium;
try {
  // require, not import(): playwright is CJS, and its named exports are not statically
  // detectable, so `await import(...)` hands back a namespace with chromium undefined.
  const req = createRequire(join(process.cwd(), "package.json"));
  ({ chromium } = req("playwright"));
} catch {
  console.error("playwright not found from " + process.cwd());
  console.error("  npm i -D playwright && npx playwright install chrome");
  process.exit(2);
}

const browser = await chromium.launch({ channel: "chrome" });
let failed = 0;
try {
  const page = await browser.newPage({ viewport: { width: 1000, height: 800 } });
  for (const theme of ["light", "dark"]) {
    // Dark is requested exactly how the host requests it, so a run also proves the app reads the
    // param rather than exposing a toggle.
    const target = new URL(url);
    if (theme === "dark") target.searchParams.set("theme", "dark");
    await page.goto(target.href, { waitUntil: "networkidle" });

    const notes = [];
    if (theme === "dark") {
      const applied = await page.evaluate(() =>
        document.documentElement.classList.contains("ma-dark"),
      );
      if (!applied) {
        notes.push(
          "?theme=dark did not set .ma-dark — read the host's theme param (Step 5). " +
            "Expected if the app is deliberately single-theme; the dark audit below is forced.",
        );
        // Force it anyway, so the rest of the dark audit still runs.
        await page.evaluate(() => {
          document.documentElement.classList.add("ma-dark");
          document.documentElement.classList.remove("ma-light");
          const links = [...document.querySelectorAll('link[href*="sp-marketplace-app-ui"]')];
          if (links.some((l) => /force=dark/.test(l.href))) {
            // Both builds are linked: enable the dark one, park the light one.
            for (const l of links) l.media = /force=dark/.test(l.href) ? "all" : "not all";
          } else {
            // One stylesheet, no dark build linked. Point it AT the dark build — disabling it
            // would leave the page unstyled and report every remaining check as broken.
            for (const l of links) {
              const u = new URL(l.href, location.href);
              u.searchParams.set("force", "dark");
              l.href = u.href;
            }
          }
        });
        // the swapped stylesheet has to arrive before anything is measured
        await page.waitForLoadState("networkidle").catch(() => {});
      }
    }
    await page.waitForTimeout(500);

    const findings = await page.evaluate(audit, {
      known: [...KNOWN],
      icons: [...ICONS],
      tokens: TOKENS,
      prefixes: appPrefixes,
      theme,
    });
    const total = findings.length + notes.length;
    console.log(`\n${theme}: ${total ? `${total} finding(s)` : "clean"}`);
    for (const n of notes) console.log(`  • ${n}`);
    for (const f of findings) console.log(`  • ${f.check}: ${f.detail}`);
    failed += total;
  }
} catch (err) {
  console.error(`\ncould not audit ${url}: ${err.message}`);
  failed = 1;
} finally {
  await browser.close();
}
process.exit(failed ? 1 : 0);
