# Nielsen's 10 Usability Heuristics — QA Checklist

Based on Jakob Nielsen's heuristics (Nielsen Norman Group, 1994).
Source: https://www.nngroup.com/articles/ten-usability-heuristics/

For each heuristic, check applicable items against the work just completed.
Mark issues with severity: 🔴 Blocker | 🟠 Major | 🟡 Minor | 🔵 Enhancement

---

## H1: Visibility of System Status

*Keep users informed about what is going on through appropriate feedback within
a reasonable amount of time. Predictable interactions create trust.*

- [ ] Loading states — spinner/skeleton while data fetches
- [ ] Progress feedback — multi-step flows show current step and total
- [ ] Action confirmation — success/failure feedback after form submit, save, delete
- [ ] Current location — active nav item, breadcrumbs, page title
- [ ] Data freshness — user knows if data is stale or updating
- [ ] Real-time validation — input errors shown as user types, not only on submit
- [ ] Disabled state clarity — disabled buttons explain why (tooltip or helper text)

## H2: Match Between System and the Real World

*Speak the user's language. Use familiar words, phrases, and concepts.
Follow real-world conventions and natural, logical ordering.*

- [ ] Plain language — no developer jargon, error codes, or internal IDs shown to user
- [ ] Intuitive icons — icons match common mental models (trash = delete, pencil = edit)
- [ ] Logical ordering — information appears in the order users expect
- [ ] Familiar patterns — interactions match what users know from similar products
- [ ] Locale-appropriate — dates, currency, units match target audience expectations

## H3: User Control and Freedom

*Provide clearly marked "emergency exits" so users can leave unwanted states
without extended processes. Fosters confidence and sense of control.*

- [ ] Undo available — destructive actions can be reversed or have confirmation
- [ ] Cancel/back — multi-step flows allow going back or canceling entirely
- [ ] Close/dismiss — modals, drawers, toasts can be dismissed easily
- [ ] No dead ends — every screen has a path forward or back
- [ ] Unsaved changes — warn before navigating away from dirty forms
- [ ] Bulk undo — if bulk actions exist, they can be reversed

## H4: Consistency and Standards

*Users should not wonder whether different words, situations, or actions mean the
same thing. Follow platform and industry conventions.*

- [ ] Internal consistency — same action looks/works the same across all pages
- [ ] External consistency — follows web platform conventions (link = underline/color, etc.)
- [ ] Terminology — same concept uses same word everywhere
- [ ] Visual consistency — button styles, spacing, typography uniform throughout
- [ ] Interaction consistency — similar features behave the same way

## H5: Error Prevention

*Prevent problems before they occur. Eliminate error-prone conditions or present
confirmation before committing. Address both slips and mistakes.*

- [ ] Input constraints — date pickers instead of free text, dropdowns where appropriate
- [ ] Smart defaults — forms pre-filled with sensible defaults where possible
- [ ] Destructive confirmation — delete/remove/cancel-order requires explicit confirmation
- [ ] Disabled invalid actions — buttons disabled when preconditions unmet
- [ ] Real-time validation — catch errors on input, not just on submit
- [ ] Autosave — long forms or editors save progress to prevent data loss

## H6: Recognition Rather Than Recall

*Minimize memory load. Make elements, actions, and options visible. Users should
not have to remember information between screens.*

- [ ] Visible options — key actions visible, not buried in menus
- [ ] Context preserved — navigating back restores previous state (filters, scroll position)
- [ ] Search/autocomplete — search has suggestions, recently used items surface
- [ ] Inline help — complex fields have helper text or tooltips
- [ ] Labels visible — form fields have persistent labels (not placeholder-only)
- [ ] Reference info — show relevant details in-context (e.g., order summary on checkout)

## H7: Flexibility and Efficiency of Use

*Cater to both novice and expert users. Shortcuts speed up expert interaction.
Allow users to tailor frequent actions.*

- [ ] Keyboard support — common actions reachable via keyboard
- [ ] Shortcuts — power users have faster paths (keyboard shortcuts, quick actions)
- [ ] Batch operations — lists support multi-select and bulk actions where appropriate
- [ ] Responsive input — search, filters, sort available for data-heavy views
- [ ] Progressive disclosure — advanced options hidden until needed

## H8: Aesthetic and Minimalist Design

*Only show information relevant to the task. Every extra element competes with
essential content and diminishes relative visibility.*

- [ ] Clear hierarchy — most important content is most prominent
- [ ] No clutter — no unnecessary decorative elements competing for attention
- [ ] Adequate whitespace — content has room to breathe
- [ ] Single focus — each page/modal has one clear primary action
- [ ] Content relevance — everything visible serves the user's current task

## H9: Help Users Recognize, Diagnose, and Recover from Errors

*Error messages in plain language. Precisely indicate the problem.
Constructively suggest a solution.*

- [ ] Human-readable errors — no raw error codes, stack traces, or "Something went wrong"
- [ ] Specific problem — message says what went wrong specifically
- [ ] Solution offered — message suggests what to do next (retry, correct input, contact support)
- [ ] Visual marking — error fields highlighted, message placed near the problem
- [ ] Input preserved — form data retained after error so user doesn't re-enter everything
- [ ] Recovery path — clear action to resolve (retry button, link to fix, back button)

## H10: Help and Documentation

*Best if the system needs no explanation. When help is needed, make it easy to
search, task-focused, concise, and actionable.*

- [ ] Onboarding — first-time users guided through key features if complex
- [ ] Contextual help — tooltips or info icons near complex fields
- [ ] Searchable help — if docs exist, they're searchable
- [ ] Task-oriented — help organized by what user wants to do, not by feature list
- [ ] Concise steps — help content gives clear, numbered steps
