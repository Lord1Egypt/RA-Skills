# Visual And Prototype Reference

Use this reference when the user asks for an HTML demo, page mockup, image/prototype brief, screenshot analysis, sketch analysis, competitor-page analysis, or visual-to-PRD breakdown.

## One-Sentence To HTML Demo

When the user asks for a demo page from a rough idea:

1. Identify the main scenario and target user.
2. Decide the minimum pages needed for requirement alignment.
3. Include representative states instead of only the happy path.
4. Add obvious placeholder data for unknown content.
5. Keep it low-fidelity unless the user explicitly asks for polished visual design.
6. Label assumptions in the response or in comments near the demo description.

Recommended HTML demo contents:

- Main user-facing page
- Optional admin/configuration page
- Primary CTA actions
- Status examples
- Empty/loading/error examples when relevant
- Mock data
- Notes for product, design, engineering, and QA

For a website reservation campaign, include:

- Campaign banner or title area
- Campaign time
- Reward card
- Reservation button
- Reward claim button
- Activity rules
- Status tabs or state switcher for not started, ongoing, reserved, claimed, and ended
- Admin fields for campaign time, reward name, inventory, rules, and publish status

## HTML Demo Output Rules

If file creation is available:

- Create a self-contained `.html` file.
- Use inline CSS and lightweight vanilla JavaScript.
- Avoid external network assets unless the user provides them.
- Use stable layout dimensions so text and buttons do not jump between states.
- Include state controls when useful for review.
- Do not claim the demo is final UI design.

If file creation is not available:

- Provide the page structure and a concise implementation-ready HTML outline.
- Include the component list and state matrix.

## Visual Requirement Analysis

When the user provides a screenshot, sketch, image, or design reference, use this output structure:

1. Visible facts
   - Text visible in the image
   - Page areas and modules
   - Buttons, forms, tabs, tables, cards, banners, and status labels
   - Visual hierarchy and apparent entry points
2. Inferred requirements
   - Likely user goals
   - Likely user actions
   - Likely state changes
   - Likely backend dependencies
3. Page/module breakdown
   - Page name
   - Module name
   - Purpose
   - Main data fields
   - User operations
4. Interaction rules
   - Button behavior
   - Form validation
   - Empty/loading/error states
   - Login or permission states
5. Admin configuration needs
   - Configurable fields
   - Validation rules
   - Effective rules
   - Permission and operation log needs
6. Data and analytics
   - Events
   - Trigger timing
   - Properties
   - Funnel or report purpose
7. Edge cases
   - Missing config
   - Invalid state
   - Duplicate action
   - Permission failure
   - Network/API failure
8. PRD-ready feature list
   - P0/P1/P2 priority suggestion
   - Acceptance criteria
9. To confirm
   - Business rules not visible in the image
   - Data source
   - Eligibility, reward, payment, security, compliance, or SDK constraints

## Image Or Prototype Brief

When the user asks for a picture, prototype image, wireframe, or visual brief:

- First clarify whether they need low-fidelity wireframe, polished marketing visual, admin UI mockup, or flow diagram.
- If tools can generate images, provide a clear generation brief.
- If tools cannot generate images, provide a detailed visual specification.

Recommended brief fields:

- Canvas size or target device
- Page type
- Audience
- Modules
- Content hierarchy
- Key states
- Visual tone
- Required text
- Elements to avoid
- Follow-up PRD questions

## Quality Guardrails

- Do not infer hidden rules as facts.
- Do not assume payment, reward inventory, personal data, or compliance rules without confirmation.
- Do not describe invisible image areas as if they are present.
- Keep screenshot analysis useful for PRD drafting, not just visual description.
- For competitor references, avoid copying brand assets, logos, or proprietary copy into final deliverables.
