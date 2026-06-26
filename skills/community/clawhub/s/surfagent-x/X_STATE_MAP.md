# X State Map

Practical state map for X account switching, community posting, and composer recovery.

## 1. Trust hierarchy

When signals conflict, trust this order:
1. visible sidebar account label
2. screenshot or visual snapshot of the active surface
3. visible route, modal state, and button state
4. targeted DOM extraction
5. wrapper success text

## 2. Bottom-left account switcher

Known landmarks:
- active account button in the left sidebar, usually `SideNav_AccountSwitcher_Button`
- menu rows that behave like full account cells, often `UserCell`
- menu items may include:
  - current account
  - alternate account(s)
  - Add an existing account
  - Manage accounts
  - Log out

Known trap:
- partial extraction can show only the current account and hide the alternate account row
- do not conclude an account is missing until the switcher is visibly inspected

Known-good switching flow:
1. read current sidebar account label
2. open switcher
3. inspect screenshot if the menu is ambiguous
4. click the full target account row
5. verify sidebar label changed
6. verify route settled on a normal X page

## 3. Community page landmarks

Known landmarks on a community page:
- community title near the top of the main column
- membership state, usually `Join` or `Joined`
- tabs like `Top`, `Latest`, `Media`, `About`
- community composer can expose an audience selector with the community name

Known-good community posting flow:
1. verify active account first
2. verify community name
3. join if required
4. confirm audience selector shows the intended community before typing
5. submit only after composer state is healthy
6. verify the new post appears in the community feed under the correct account

## 4. Composer trap: text visible, Post disabled

Real failure mode:
- text appears visually present
- Post button still disabled
- X has not accepted the content as real typed input

Common causes:
- DOM-only insertion
- unresolved composer state
- overflow or hidden validation issue

Known-good recovery:
1. inspect remaining character count
2. if not overflow, assume input registration failure
3. focus composer
4. select all
5. clear
6. type through the real keyboard/input path
7. verify Post becomes enabled
8. submit

## 5. Fast escalation rules

Escalate to screenshot or visual snapshot early when:
- account identity matters
- a modal or drawer is open
- the community composer is visible
- extraction and visible state disagree
- a button should be enabled but is not

If one screenshot can settle the state, take it. Do not burn minutes arguing with half-truth DOM output.
