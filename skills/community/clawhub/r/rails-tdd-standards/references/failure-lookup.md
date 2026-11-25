# System Spec Failures At A Glance

A symptom-to-cause lookup table for the failures covered in the sibling
references in this folder.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Element "not visible" but present | taller than headless viewport | raise `--window-size` |
| `undefined method 'sign_in'` in request spec | missing Devise integration helper | `config.include Devise::Test::IntegrationHelpers, type: :request` |
| `current_user` nil after signing in | used `login_as` in a Devise app | use `sign_in` |
| `ActionMailer::Base.deliveries` unchanged | `deliver_later` + `:test` adapter | `perform_enqueued_jobs` / `:inline` / `have_enqueued_job` |
| Spec passes but the feature is broken | `have_content` matched elsewhere | scope with `within_frame` / `within` |
| Form does nothing | `data-turbo="false"` + `data-turbo-frame` | pick one |
| Stimulus controller inert | not registered, not imported, or not attached | check the Stimulus registry file, the browser console, and the `data-controller` attribute |
| Page shows stale content | service worker cache | disable SW in test |
| All specs fail with a proxy error (Firefox) | Firefox ignoring `no_proxy` | `network.proxy.no_proxies_on` pref |
| Intermittent pass/fail on the same commit | driver/browser/version drift | pin versions, run 3x to classify |

---
