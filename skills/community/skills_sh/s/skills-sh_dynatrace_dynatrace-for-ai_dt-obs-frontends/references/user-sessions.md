# User Sessions & Analytics

Track active user sessions, unique users, engagement patterns, and leverage custom properties for business insights.

## Contents

- [Schema Reference: `user.sessions`](#schema-reference-usersessions)
- [Core Session Metrics](#core-session-metrics)
- [Active User Session Monitoring](#active-user-session-monitoring)
- [Unique Active User Tracking](#unique-active-user-tracking)
- [Geographic User Distribution](#geographic-user-distribution)
- [Device Type Usage Patterns](#device-type-usage-patterns)
- [Browser Adoption Tracking](#browser-adoption-tracking)
- [Sessions with User Tags](#sessions-with-user-tags)
- [Sessions by Custom Property](#sessions-by-custom-property)
- [Session Duration Analysis](#session-duration-analysis)
- [Session Journey Overview](#session-journey-overview)
- [New vs Returning Users](#new-vs-returning-users)
- [User Interactions](#user-interactions)
- [Page & View Analysis](#page--view-analysis)

## Schema Reference: `user.sessions`

`user.sessions` contains session-level aggregates produced by the session aggregation service from `user.events`. **Field names differ from `user.events`** — sessions use underscores where events use dots.

**Session identity and context:**
- `dt.rum.session.id` — Session ID (NOT `dt.rum.session_id`)
- `dt.rum.instance.id` — Instance ID
- `frontend.name` — array of frontends involved in session
- `dt.rum.application.type` — `web` or `mobile`
- `dt.rum.user_type` — `real_user`, `synthetic`, or `robot`


**Session aggregates (underscore naming — NOT dot):**

| Field | Description | ⚠️ NOT this |
|-------|-------------|-------------|
| `navigation_count` | Number of navigations | ~~`navigation.count`~~ |
| `user_interaction_count` | Clicks, form submissions | ~~`user_interaction.count`~~ |
| `user_action_count` | User actions | ~~`user_action.count`~~ |
| `request_count` | XHR/fetch requests | ~~`request.count`~~ |
| `event_count` | Total events in session | ~~`event.count`~~ |
| `page_summary_count` | Page views (web) | ~~`page_summary.count`~~ |
| `view_summary_count` | Views (mobile/SPA) | ~~`view_summary.count`~~ |

**Error fields (dot naming — same as events):**
- `error.count`, `error.exception_count`, `error.http_4xx_count`, `error.http_5xx_count`
- `error.anr_count`, `error.csp_violation_count`, `error.has_crash`

**Session lifecycle:**
- `start_time`, `end_time`, `duration` (nanoseconds)
- `end_reason` — `timeout`, `synthetic_execution_finished`, etc.
- `characteristics.is_bounce` — Boolean bounce flag
- `characteristics.has_replay` — Session replay available

**User identity:**
- `dt.rum.user_tag` — User identifier (typically email, username or customerId), set via `dtrum.identifyUser()` API call in the instrumented frontend. **Not always populated** — only present when the frontend explicitly calls `identifyUser()`.
- When `dt.rum.user_tag` is empty, `dt.rum.instance.id` is often the only user differentiator. The value is a random ID assigned by the RUM agent on the client side, so it is not personally identifiable but can be used to distinguish unique users when `user_tag` is not set. On web this is based on a persistent cookie, so it can be deleted by the user.
- The user tag is a **session-level field** — query it from `user.sessions`, not `user.events` (where it may be empty even if the session has one).

**Client/device context:**
- `browser.name`, `browser.version`, `device.type`, `os.name`
- `geo.country.iso_code`, `client.ip`, `client.isp`

**Synthetic-only fields:**
- `dt.entity.synthetic_test`, `dt.entity.synthetic_location`, `dt.entity.synthetic_test_step`

**Time window behavior:**
- `fetch user.sessions, from: X, to: Y` only returns sessions that **started** in `[X, Y]` — NOT sessions that were merely active during that window.
- Sessions can last 8h+ (the aggregation service waits 30+ minutes of inactivity before closing a session).
- To find all sessions active during a time window, extend the lookback by at least 8 hours: e.g., to cover events from the last 24h, query `fetch user.sessions, from: now() - 32h`.
- This matters for correlation queries (e.g., matching `user.events` to `user.sessions` by session ID) — a narrow `user.sessions` window will miss long-running sessions and produce false "orphans."

**Session creation delay:**
- The session aggregation service waits for ~30+ minutes of inactivity before closing a session and writing the `user.sessions` record.
- This means **recent events (last ~1 hour) will not yet have a matching `user.sessions` entry** — this is normal, not a data gap.
- When correlating `user.events` with `user.sessions`, exclude recent data (e.g., use `to: now() - 1h`) to avoid counting in-progress sessions as orphans.

**Zombie sessions (events without a `user.sessions` record):**
- Not every `dt.rum.session.id` in `user.events` will have a corresponding `user.sessions` record. The session aggregation service intentionally skips **zombie sessions** — sessions with no real user activity (zero navigations and zero user interactions).
- Zombie sessions contain only background, machine-driven activity (e.g., automatic XHR requests, heartbeats) with no page views or clicks. Serializing them would add no value to users.
- When correlating `user.events` with `user.sessions`, expect a large number of unmatched session IDs. This is **by design**, not a data gap. Filter to sessions with activity before diagnosing orphans:
```dql
  fetch user.events, from: now() - 2h, to: now() - 1h
  | filter isNotNull(dt.rum.session.id)
  | summarize navs = countIf(characteristics.has_navigation == true),
      interactions = countIf(characteristics.has_user_interaction == true),
      by: {dt.rum.session.id}
  | filter navs > 0 or interactions > 0
```

**Example — bounce rate and session quality:**
```dql
fetch user.sessions, from: now() - 24h
| filter dt.rum.user_type == "real_user"
| summarize
    total_sessions = count(),
    bounces = countIf(characteristics.is_bounce == true),
    zero_activity = countIf(toLong(navigation_count) == 0 and toLong(user_interaction_count) == 0),
    avg_duration_s = avg(toLong(duration)) / 1000000000
| fieldsAdd bounce_rate_pct = round((bounces * 100.0) / total_sessions, decimals: 1)
```

## Core Session Metrics

**Key Metrics:**

- `dt.frontend.session.active.estimated_count` - Active user sessions
- `dt.frontend.user.active.estimated_count` - Unique active users

**Key Fields (Event-Based):**

- `dt.rum.session.id` - Unique session identifier
- `dt.rum.instance.id` - Unique user/device instance
- `dt.rum.user_tag` - Custom user identifier
- `session_properties.__property_name__` - Custom session properties
- `event_properties.__property_name__` - Custom event properties

**Alerting Thresholds:**

- Critical: Active sessions dropping > 50%
- Track user growth trends for capacity planning

## Active User Session Monitoring

Track active user sessions by application:

```dql
timeseries active_sessions = countDistinct(dt.frontend.session.active.estimated_count),
          by: {frontend.name},
          from: now() - 4h
| sort active_sessions desc

```

**Use Case:** Monitor real-time user engagement and capacity planning.

## Unique Active User Tracking

Monitor unique active users:

```dql
timeseries unique_users = countDistinct(dt.frontend.user.active.estimated_count),
          active_sessions = countDistinct(dt.frontend.session.active.estimated_count),
          by: {frontend.name},
          from: now() - 2h

| fieldsAdd
    sessions_per_user = active_sessions[] / unique_users[],
    avg_unique_users = arrayAvg(unique_users)
| sort avg_unique_users desc

```

**Use Case:** Understand user engagement patterns and identify power users.

## Geographic User Distribution

Analyze user distribution across regions:

```dql
timeseries unique_users = countDistinct(dt.frontend.user.active.estimated_count),
          active_sessions = countDistinct(dt.frontend.session.active.estimated_count),
          by: {frontend.name, geo.country.iso_code},
          from: now() - 6h

| fieldsAdd
    avg_sessions_per_user = active_sessions[] / unique_users[],
    peak_unique_users = arrayMax(unique_users)
| filter arrayMax(unique_users) > 5
| sort peak_unique_users desc

```

**Use Case:** Identify key geographic markets and plan regional infrastructure investments.

## Device Type Usage Patterns

Compare user activity across device types:

```dql
timeseries unique_users = countDistinct(dt.frontend.user.active.estimated_count),
          active_sessions = countDistinct(dt.frontend.session.active.estimated_count),
          by: {frontend.name, device.type},
          from: now() - 4h

| fieldsAdd
    session_ratio = active_sessions[] / unique_users[],
    peak_unique_users = arrayMax(unique_users)
| sort device.type, peak_unique_users desc

```

**Use Case:** Optimize mobile-first or desktop-first strategies based on device usage.

## Browser Adoption Tracking

Track browser distribution among active users:

```dql
timeseries unique_users = countDistinct(dt.frontend.user.active.estimated_count),
          active_sessions = countDistinct(dt.frontend.session.active.estimated_count),
          by: {frontend.name, browser.name},
          from: now() - 24h,
          interval: 1h
| filter arrayMax(unique_users) > 1
| sort browser.name, timeframe desc

```

**Use Case:** Prioritize browser compatibility testing based on actual user distribution.

## Sessions with User Tags

Query tagged user sessions:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_user_tag == true
| summarize
    session_count = countDistinct(dt.rum.session.id),
    event_count = count(),
    by: {frontend.name, dt.rum.user_tag}
| sort session_count desc
| limit 50

```

**Use Case:** Analyze behavior of specific identified users.

## Sessions by Custom Property

Aggregate by session property (e.g., subscription tier):

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_session_properties == true
| summarize
    session_count = countDistinct(dt.rum.session.id),
    user_count = countDistinct(dt.rum.instance.id, precision: 9),
    by: {frontend.name}

```

**Use Case:** Segment users by custom business attributes.

## Session Duration Analysis

Analyze session lengths:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_page_summary == true or characteristics.has_view_summary == true
| summarize
    session_duration = sum(duration),
    by: {frontend.name, dt.rum.session.id}
| summarize
    avg_duration = avg(session_duration),
    p50_duration = percentile(session_duration, 50),
    p90_duration = percentile(session_duration, 90),
    by: {frontend.name}

```

**Use Case:** Understand user engagement depth.

## Session Journey Overview

Trace user journey through an app:

```dql
fetch user.events, from: now() - 2h
| filter dt.rum.session.id == "<session_id>"
| fields
    start_time,
    characteristics.classifier,
    view.name,
    page.url.path,
    interaction.name,
    error.type
| sort start_time asc

```

**Use Case:** Debug specific user session issues.

## New vs Returning Users

Analyze user retention patterns:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_navigation == true
| summarize
    sessions = countDistinct(dt.rum.session.id),
    by: {frontend.name, dt.rum.instance.id}
| summarize
    single_session_users = countIf(sessions == 1),
    returning_users = countIf(sessions > 1),
    by: {frontend.name}

```

**Use Case:** Measure user retention and engagement.

## User Interactions

Analyze user clicks, form inputs, scrolls, and other interactions for UX insights.

**Data Source:** `fetch user.events` with `characteristics.has_user_interaction`

**Key Fields:**

- `interaction.name` - Type: click, change, blur, scroll, touch, etc.
- `ui_element.name` - Element identifier (aria-label, title, name, etc.)
- `ui_element.custom_name` - Custom name via `data-dt-name` attribute
- `ui_element.tag_name` - HTML tag or mobile component type
- `ui_element.features` - Feature grouping via `data-dt-features`

### All User Interactions

Query all interaction types:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_user_interaction == true
| summarize
    interaction_count = count(),
    session_count = countDistinct(dt.rum.session.id),
    by: {frontend.name, interaction.name}
| sort interaction_count desc

```

### Click Analysis

Analyze button/link clicks:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_user_interaction == true
| filter interaction.name == "click"
| summarize
    click_count = count(),
    unique_users = countDistinct(dt.rum.instance.id, precision: 9),
    by: {frontend.name, ui_element.resolved_name, ui_element.tag_name}
| sort click_count desc
| limit 30

```

**Use Case:** Identify most-clicked UI elements.

### Feature Usage Analysis

Analyze custom feature areas:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_user_interaction == true
| filter isNotNull(ui_element.features)
| summarize
    interaction_count = count(),
    unique_users = countDistinct(dt.rum.instance.id, precision: 9),
    by: {ui_element.features}
| sort interaction_count desc

```

**Use Case:** Measure feature adoption using `data-dt-features`.

## Page & View Analysis

Analyze page summaries (web) and view summaries (mobile) for engagement metrics.

**Key Fields:**

- `page.url.path` / `view.name` - Page/view identifier
- `page.foreground_time` / `view.foreground_time` - Active time
- `page.background_time` / `view.background_time` - Hidden time
- `view.sequence_number` - View position in session
- `navigation.type` - How user arrived: `navigate`, `reload`, `back_forward`

### Page Views Overview

Query all page views (web):

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_page_summary == true
| summarize
    page_views = count(),
    unique_sessions = countDistinct(dt.rum.session.id),
    unique_users = countDistinct(dt.rum.instance.id, precision: 9),
    by: {frontend.name, page.url.path}
| sort page_views desc
| limit 30

```

**Use Case:** Identify most visited pages.

### Entry Pages

Analyze landing pages:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_page_summary == true
| filter view.sequence_number == 1
| summarize
    entry_count = count(),
    unique_sessions = countDistinct(dt.rum.session.id),
    by: {frontend.name, page.url.path}
| sort entry_count desc
| limit 20

```

**Use Case:** Optimize landing page performance.

### Views per Session

Analyze session depth:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_page_summary == true or characteristics.has_view_summary == true
| summarize max_sequence = max(view.sequence_number), by: {frontend.name, dt.rum.session.id}
| summarize
    sessions = count(),
    avg_views = avg(max_sequence),
    p50_views = percentile(max_sequence, 50),
    p90_views = percentile(max_sequence, 90),
    by: {frontend.name}

```

**Use Case:** Measure user journey depth.

