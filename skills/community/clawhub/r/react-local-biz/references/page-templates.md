# Page Templates Reference

Section-by-section structure for all 5 standard pages.

---

## Page 1: Home

### Sections (in order)

| # | Section | Background | Notes |
|---|---|---|---|
| 1 | **Hero** | Image + dark overlay | Full viewport, large H1, 2 CTAs, scroll indicator |
| 2 | **Stats Bar** | `bg-primary-800` | 4 numbers: projects, years, satisfaction %, awards |
| 3 | **Services Preview** | `bg-white` | 3 cards (subset of full services), "View All" CTA |
| 4 | **Why Choose Us** | `bg-neutral-50` | 2-col: image with floating badges + bullet list + CTAs |
| 5 | **Portfolio Preview** | `bg-white` | 6-image masonry grid, hover overlays |
| 6 | **Testimonials** | `bg-primary-900` | 3 cards, star ratings, customer name + location |
| 7 | **CTA Banner** | gradient primary-600→800 | 1-2 line headline + button |

### Hero Copy Formula
```
Badge: "[City]'s Premier [Business Type]"
H1:   "Transform Your [Thing] Into a [Desired Outcome]"
Sub:  "Professional [service] for residential & commercial [context]."
CTA1: "Get Free Quote" (btn-primary → /contact)
CTA2: "View Our Work" (btn-outline → /portfolio)
```

### Stats to Use (customize numbers)
- Projects Completed, Years Experience, Client Satisfaction %, Awards Won
- Icons: Trophy, Award, ThumbsUp, Star (from lucide-react)

---

## Page 2: Services

### Sections

| # | Section | Background |
|---|---|---|
| 1 | **Page Hero** | Image + overlay |
| 2 | **Services Grid** | `bg-neutral-50` |
| 3 | **How It Works** | `bg-white` |
| 4 | **CTA** | `bg-primary-800` |

### Services Grid Card Pattern (6 cards, 3-col)
Each card:
- Image (h-48) with icon overlay (absolute bottom-left)
- Title, description (3-4 sentences)
- 6 bullet features with Check icons
- "Get a Quote →" link

### Services List by Business Type
| Type | Services |
|---|---|
| Landscaping | Lawn Care, Garden Design, Trees/Shrubs, Irrigation, Hardscaping, Seasonal Cleanup |
| Restaurant | Dine-in, Takeout/Delivery, Catering, Private Events, Brunch, Seasonal Menu |
| Salon | Haircuts, Color, Highlights, Treatments, Blowouts, Nails, Waxing |
| Plumber | Emergency Repair, Drain Cleaning, Installation, Remodeling, Water Heater, Inspections |
| Gym | Personal Training, Group Classes, Nutrition, Online Coaching, Corporate, Kids |

### How It Works (4 Steps)
Number steps 01–04. Include:
- Step icon (lucide) in primary-600 square with number badge
- Step title (verb phrase)
- 1-2 sentence description
- Horizontal connecting line: `hidden lg:block absolute top-16 left-[12.5%] right-[12.5%] h-0.5 bg-gradient-to-r from-primary-200 via-primary-400 to-primary-200`

Common step patterns:
- Consultation → Design → Installation → Ongoing Care *(services)*
- Book → Arrive → Experience → Return *(salon/spa)*
- Call → Diagnose → Fix → Follow-Up *(home services)*

---

## Page 3: Portfolio / Gallery

### Sections

| # | Section | Background |
|---|---|---|
| 1 | **Page Hero** | Image + overlay |
| 2 | **Filter + Grid** | `bg-neutral-50` |
| 3 | **Featured Project** | `bg-white` |
| 4 | **CTA** | `bg-primary-800` |

### Filter Tabs
```jsx
const categories = ["All", "Residential", "Commercial", "Type A", "Type B"];
// Active: bg-primary-600 text-white shadow
// Inactive: bg-white text-neutral-600 border border-neutral-200
```

### Gallery Grid
- `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`
- Each card: `aspect-square overflow-hidden rounded-2xl`
- Hover: scale-110 image + opacity-0→100 dark overlay with title + location
- Badges: category (top-left), year (top-right)
- `AnimatePresence` + `motion.div layout` for filtered transitions

### Lightbox Pattern
```jsx
// State: lightbox = project.id | null
// On card click: setLightbox(project.id)
// Overlay: fixed inset-0 z-50 bg-black/95
// Include: X close button, prev/next chevrons, image + details panel
```

### Featured Project Block (2-col split)
```
Left: Large image (aspect-ratio natural, h-80 mobile)
Right: Dark bg (stone-900), category badge, title (display font), 
       description, 3 stats (timeline, investment, year), CTA button
```

---

## Page 4: About

### Sections

| # | Section | Background |
|---|---|---|
| 1 | **Page Hero** | Image + overlay |
| 2 | **Our Story** | `bg-white` |
| 3 | **Core Values** | `bg-neutral-50` |
| 4 | **Timeline / Milestones** | `bg-white` |
| 5 | **Team** | `bg-neutral-50` |
| 6 | **Awards & Certifications** | `bg-white` |
| 7 | **CTA** | `bg-primary-800` |

### Story Section (2-col)
- Left: section-label, H2, 2 paragraphs, 2×2 stat grid (bg-neutral-50 rounded cards)
- Right: tall image (aspect-[3/4]) + floating stat badge (bottom-left, primary-600)
- Founding year, mission, growth story

### Values Cards (3-col)
```
Sustainability/Quality/Customer First
Icon in colored bg (bg-primary-50, bg-accent-50, etc.)
Title + 2-sentence description
```

### Timeline
```jsx
// Vertical line: absolute left-8 md:left-1/2 w-0.5 bg-primary-100
// Items alternate left/right on desktop (i % 2 === 0)
// Each item: year (text-primary-600) + event text in bg-neutral-50 card
// Dot: absolute, bg-primary-600, border-4 border-white, z-10
```

### Team Cards (4-col grid)
- Initials avatar (colored bg-primary-700/bark/etc. rounded-2xl w-20 h-20)
- Name (display font), Role (text-primary-600), Bio (2-3 sentences)
- No real photos needed — initials always look clean

### Awards Grid (3-col)
```jsx
// Each: flex items-center gap-4 bg-neutral-50 rounded-2xl p-5 border
// Left: emoji icon (text-3xl)
// Right: award name (font-semibold) + org + year (text-xs text-neutral-500)
```

---

## Page 5: Contact

### Sections

| # | Section | Background |
|---|---|---|
| 1 | **Page Hero** | Image + overlay |
| 2 | **Form + Info** | `bg-neutral-50` |
| 3 | **Social Proof Strip** | `bg-white border-t` |

### Form Layout (lg:grid-cols-5)
```
Form panel (col-span-3): bg-white rounded-3xl shadow-xl p-8
  - Title: "Get a Free Quote"
  - Fields: Name*, Email*, Phone (optional), Service dropdown, Message*
  - Grid: Name + Email in 2-col; Phone + Service in 2-col
  - Security note: CheckCircle icon + "Your info is never shared"
  - Submit: btn-primary full-width

Info panel (col-span-2): stacked cards
  1. Contact details (MapPin, Phone, Mail with icons)
  2. Business hours (table)
  3. Map placeholder (bg gradient + MapPin icon + "Open in Google Maps" link)
```

### Form Validation Pattern
```jsx
const [form, setForm] = useState({ name:"", email:"", phone:"", service:"", message:"" });
const [errors, setErrors] = useState({});
const [submitted, setSubmitted] = useState(false);

// Success state: CheckCircle icon + "Message Sent!" + personalized thank you
// Error state: red border + ring-1 ring-red-400 on input + error text below
```

### Social Proof Strip (flex wrap justify-center)
Items to include (pick 3-4):
- Google Reviews (Star icons + "4.9/5.0" + "N+ Reviews")
- BBB Accredited (badge bg-blue-600 + "A+ Rating")
- Licensed & Insured (badge + state license number)
- Industry awards (Houzz, Angi, etc.)

---

## Common Copy Patterns

### Section Labels
```
"What We Do" / "Our Services" / "Complete Solutions"
"Our Work" / "Recent Projects" / "Portfolio"
"Why Choose Us" / "The Difference"
"What Our Clients Say" / "Testimonials"
"Meet Our Team" / "The People Behind the Magic"
"Get in Touch" / "Let's Talk [Business Type]"
```

### Hero Headlines (formula)
```
Verb + possessive + thing + into + desired outcome
"Transform Your Outdoor Space Into a Paradise"
"Turn Your Vision Into Your Dream Home"
"Elevate Your Dining Experience"
"Build the Body You've Always Wanted"
```

### CTA Headlines
```
"Ready to [Transform/Elevate/Start] Your [Thing]?"
"Love What You See?"
"Work With Our Team"
"[Verb] Your Free [Quote/Consultation/Assessment] Today"
```
