# Menu & navigation design spec

How to structure navigation in an ant-design-vue dashboard. Covers the global pattern choice, information architecture, the `a-menu` build, breadcrumbs, in-page nav, responsive behavior, and labeling.

## 1. Pick the global pattern

| Pattern | Layout | Use when | Components |
|---|---|---|---|
| **Side menu** (default for admin) | dark `a-layout-sider` with inline `a-menu`; header for context/account | 5–30 destinations, 1–2 levels deep, deep app | `a-layout-sider` + `a-menu mode="inline"` |
| **Top menu** | horizontal `a-menu` in `a-layout-header`, content centered | Few (≤7) top-level sections, marketing-ish, shallow | `a-menu mode="horizontal"` |
| **Top + side (hybrid)** | top bar picks a *product/module*; sider shows that module's pages | Large suite with several modules (e.g. Billing / CRM / Analytics) | horizontal top `a-menu` + inline sider `a-menu` |

**Default to the side menu** for dashboards. Reach for hybrid only when one sider can't hold the IA without exceeding 2 levels.

```
Side menu (default)          Top menu                 Hybrid
┌────┬──────────┐           ┌──────────────┐         ┌──────────────┐
│menu│  header  │           │ logo  nav  ⛃ │         │logo  modules ⛃│
│    ├──────────┤           ├──────────────┤         ├────┬─────────┤
│ ▤  │          │           │              │         │side│         │
│ ▤  │  content │           │   content    │         │menu│ content │
│ ▤  │          │           │              │         │    │         │
└────┴──────────┘           └──────────────┘         └────┴─────────┘
```

## 2. Information architecture

- **Max depth 2** in a sider (top item → one level of children). Three levels = redesign or use in-page Tabs for the third level.
- **7±2 top-level groups.** More than ~9 collapsed groups → reconsider grouping.
- **Order by frequency, then logically:** Overview/Dashboard first; Settings/Admin last; destructive/rare items at the bottom.
- **Group with `a-menu-item-group` or `a-sub-menu`:** use a *group* (non-collapsing header) for labels like "MANAGE", a *sub-menu* (collapsing) when children are many or situational.
- Separate clusters with `a-menu-divider`.
- One item is **selected** at a time (`selectedKeys` has one key). Parents auto-open via `openKeys`.

## 3. Build the sider menu

Slot form (readable in slides). Icons on **top-level items only** — child items align without icons.

```html
<a-layout-sider v-model:collapsed="collapsed" collapsible :width="220" theme="dark">
  <div class="logo">▦ Acme</div>
  <a-menu v-model:selectedKeys="selected" v-model:openKeys="open" mode="inline" theme="dark">
    <a-menu-item key="overview"><dashboard-outlined /> Overview</a-menu-item>

    <a-menu-item-group key="g-sell" title="SELL">
      <a-sub-menu key="orders">
        <template #title><shopping-outlined /> Orders</template>
        <a-menu-item key="orders-all">All orders</a-menu-item>
        <a-menu-item key="orders-refunds">Refunds</a-menu-item>
      </a-sub-menu>
      <a-menu-item key="customers"><team-outlined /> Customers</a-menu-item>
      <a-menu-item key="products"><appstore-outlined /> Products</a-menu-item>
    </a-menu-item-group>

    <a-menu-divider />
    <a-menu-item key="settings"><setting-outlined /> Settings</a-menu-item>
  </a-menu>
</a-layout-sider>
```

```html
<script setup>
import { ref } from 'vue'
const collapsed = ref(false)
const selected = ref(['overview'])   // current page — set per slide to show context
const open = ref(['orders'])         // expanded sub-menu
</script>
```

Rules:
- **`selectedKeys` reflects the current page** — on each slide, set it to the item the slide is "about" so the highlight is correct.
- **`theme="dark"`** sider + `theme="dark"` menu is the canonical Ant admin look; light sider for a softer product.
- **Collapsible:** `collapsible` + `v-model:collapsed`. Collapsed sider shows icons only — which is why top-level items need icons (children get Tooltips automatically when collapsed).
- **Keep keys stable & meaningful** (`orders-refunds`, not `2-1`) so it's self-documenting.
- **Do not bind `@click`/`selectedKeys` to Slidev's router.** Slidev owns slide navigation; the menu is a mock driven by local `ref`.

## 4. Header & breadcrumb

- **Breadcrumb** (`a-breadcrumb`) sits left in the header (or just under it), echoing the menu path: `Home / Orders / Refunds`. Show it for any page ≥2 levels deep; omit on top-level Overview.
- Right side of header, in an `a-space`: global `a-input-search`, a `a-badge` notification bell (`<bell-outlined/>`), and the user `a-dropdown` (avatar + name → menu with Profile / Settings / Logout).
- The breadcrumb's last segment = current page (not a link); earlier segments are links.

```html
<a-breadcrumb>
  <a-breadcrumb-item><home-outlined /></a-breadcrumb-item>
  <a-breadcrumb-item>Orders</a-breadcrumb-item>
  <a-breadcrumb-item>Refunds</a-breadcrumb-item>
</a-breadcrumb>
```

## 5. In-page (secondary) navigation

Once on a page, navigate *within* it without touching the global menu:

- **`a-tabs`** — switch between facets of the same entity (Overview / Activity / Settings on a detail page), or list views (All / Active / Archived). This is the "third level" the sider shouldn't carry.
- **`a-segmented`** — compact toggles inside a card (time range Day/Week/Month, chart type).
- **`a-steps`** — linear multi-stage flows (create wizard, KYC, checkout) where order matters and progress is shown.
- **`a-anchor`** — jump links on long single-page forms/settings ("Profile / Security / Billing / Notifications").
- **`a-radio-group button-style="solid"`** — small mutually-exclusive view switch when Tabs are too heavy.

Decision: changing the *page* → menu/breadcrumb; changing a *view of the same page* → Tabs/Segmented; a *sequential task* → Steps; jumping *within one long page* → Anchor.

## 6. Responsive / collapsed behavior

- Sider `breakpoint="lg"` + `collapsedWidth="0"` to auto-hide on narrow widths; pair with a `<menu-outlined/>` button in the header that toggles a `a-drawer` containing the menu (off-canvas nav).
- Collapsed icon rail (`collapsedWidth="64"`) keeps icons; antd shows item labels as Tooltips/flyouts on hover.
- On slides this matters less (fixed canvas), but show the collapsed state if the talk is about responsive design.

## 7. Labeling

- **Nouns for destinations** (Orders, Customers, Reports), **verbs for actions** (Create, Export) — actions are buttons, not menu items.
- Title Case or sentence case — be consistent across the whole menu.
- Short: 1–2 words per item. Put detail in sub-items, not long labels.
- Match the breadcrumb segment, page `<h2>` title, and menu label — same words for the same place.

## Do / Don't

**Do**
- One global pattern (default: side menu); be consistent across every slide.
- Keep IA ≤2 levels in the sider; push the 3rd level into Tabs.
- Icons on top-level items; stable, meaningful keys.
- Set `selectedKeys` to the current slide's page; keep breadcrumb in sync.
- Use Tabs/Segmented/Steps/Anchor for in-page navigation.

**Don't**
- Mix side and top primary menus arbitrarily (hybrid is a deliberate 2-tier pattern, not randomness).
- Nest 3+ menu levels or exceed ~9 collapsed groups.
- Put actions (Create/Delete/Export) in the nav menu.
- Bind the menu to Slidev's router, or let `selectedKeys` go empty/wrong on a slide.
- Use icons on child items (breaks alignment) or invent a different icon set than `@ant-design/icons-vue`.
