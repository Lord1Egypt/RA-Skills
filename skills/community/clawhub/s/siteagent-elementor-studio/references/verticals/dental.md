# Dental — studio build pack

**When to use:** a dentist, orthodontist, or family/cosmetic practice that wants new patients to book online.

## Voice & positioning
Calm, clinical, reassuring — the page should feel like a clean waiting room, not a sales floor. The visitor's job is simple: confirm this practice is trustworthy and nearby, then book. Keep sentences short and free of jargon; lead with comfort and credentials, not discounts. **Primary conversion: book an appointment** (header button + repeated CTAs). Phone number stays visible for the call-first crowd.

## Design system
- **Palette** (maps onto brand-kit tokens — `brand` / a darker shade / `accent` / `heading` / `text` / `muted`):
  - primary `#1F8FA6` · primary-dark `#14606F` · accent `#5FCFBF` · dark `#16323A` · body-text `#3D4A4F` · muted `#7C8A90`
  - Teal/aqua reads medical-clean without going cold; pair with generous white space.
- **Typography:** headings in a humanist sans (Poppins or Lexend, 600); body in Inter/Source Sans (400). Scale `h1 48 / h2 36 / h3 28 / body 16` per brand-kit.
- **Spacing/rhythm:** airy — section padding 96–120px, boxed container ~1200px. Rounded corners (8–12px) on cards and the booking button to feel approachable.

## Section flow (top → bottom)
1. **Hero** — outcome headline ("A healthier smile, gently done") + one-line subhead + **Book Appointment** CTA + a calm clinic/patient photo.
2. **Trust strip** — years in practice, patients seen, association logos/badges (no claims, just facts).
3. **Services** — cleanings, fillings, whitening, implants, ortho — card grid with plain-language descriptions.
4. **Meet the team** — dentist + hygienists with short, warm bios; faces build trust fastest.
5. **Insurance & financing** — plans accepted, payment-plan note; reduces the silent "can I afford this" objection.
6. **Patient reviews** — 3–4 real testimonials, first name + initial; star row optional.
7. **FAQ** — first visit, nervous patients, emergencies, hours.
8. **Contact / booking** — embedded form or booking widget, map, hours, phone + footer.

## Build notes
- Build sections from the matching recipes in `references/recipes.md` (Hero, Services grid, Testimonials, FAQ, Contact), all bound to the named tokens from `references/brand-kit.md` — set the 8 colors / 2 fonts once, reference by name.
- **Compliance gotcha:** avoid medical claims, cure language, and guarantees ("painless", "100% safe", "best dentist"). Use outcome-neutral phrasing. Don't show before/after results as promises. If the practice wants specific clinical claims, flag them as the client's responsibility to substantiate.
- Booking: prefer a real booking integration or Pro Form widget; if no scheduler is wired yet, place the form as a flagged visual-only placeholder and tell the user.
