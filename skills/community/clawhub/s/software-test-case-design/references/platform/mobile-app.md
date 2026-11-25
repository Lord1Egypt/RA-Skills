# Mobile App Test Points

> This file defines the test dimensions and strategy points that distinguish mobile apps from other platforms.
> For the output format, see `references/examples/format-spec.md`; for the checklist, see `references/checklists/mobile-app-checklist.md`.

---

## 1. Gestures

### Key focus points
- Touch targets: iOS ≥ 44×44pt, Android ≥ 48×48dp, especially icon buttons and swipe-action areas in lists
- Gesture conflicts: swipe to page vs swipe to delete vs swipe to go back
- Edge gestures: swipe back from the left edge (iOS) and swipe up from the bottom (system gesture area) may be intercepted by the app
- Priority between multi-finger and single-finger gestures

### Common defects
- Small touch areas cause mis-taps
- Inner and outer gesture conflicts in nested scrolling
- Long press conflicts with scrolling

---

## 2. Screen Adaptation

### Key focus points
- Layout on small / medium / large phones and tablets
- Safe area adaptation for notched / punch-hole / tall screens
- Layout and state retention when unfolding / folding a foldable
- Portrait / landscape modes and orientation switching
- Effect of the system font size setting on layout

### Common defects
- Content hidden by the notch
- Layout broken after enlarging the system font
- Abnormal layout after unfolding / folding a foldable
- Page state lost after switching orientation

---

## 3. Interruption Recovery

### Key focus points
- System interruptions such as incoming calls / SMS / alarms / low battery pop-ups / system update prompts
- Page recreation caused by memory reclamation in the background (more aggressive on Android)
- Interrupted while filling in a form → whether data is retained after returning
- Payment flow interrupted → whether the order status is consistent

### Common defects
- Blank screen or crash after returning from an interruption
- Form data lost
- Inconsistent payment status (user charged but order not updated)
- App killed by the system after a long time in the background, with abnormal recovery

---

## 4. Network Switching

### Key focus points
- Handling of in-flight requests when switching between WiFi and 4G/5G
- User experience on weak networks (high latency / low bandwidth / high packet loss)
- Airplane mode / offline → automatic reconnection after recovery
- Degradation when network permission is disabled by the system

### Common defects
- Requests hang without response when the network switches
- Endless loading without a timeout prompt on weak networks
- No placeholder when images / resources fail to load after going offline

---

## 5. Permission Management

### Key focus points
- Explain the purpose when first requesting a permission (mandatory on iOS, recommended on Android)
- Feature degradation after denial: the core path must not break
- Guide users to the settings page after "Don't ask again"
- State synchronization after a permission is revoked (turned off in system settings)
- Differences between iOS and Android permission mechanisms

### Common defects
- Crash or freeze after denial
- No guidance to the settings page, so users do not know how to restore it
- Permission state not refreshed after returning from the background

---

## 6. Push Notifications

### Key focus points
- Timing of the notification permission request (request after the user understands the value)
- Navigation when tapping a notification: different handling paths for cold start vs hot start
- Notification parameter passing and page routing
- Differences between iOS and Android notification mechanisms

### Common defects
- Tapping a notification opens the home page instead of the target page
- Notification parameters lost on cold start
- No prompt in the app after notification permission is turned off

---

## 7. Device Compatibility

### Key focus points
- Differences between iOS / Android versions (new API compatibility, handling of deprecated APIs)
- Differences between vendor ROMs (Xiaomi MIUI, Huawei EMUI, OPPO ColorOS, etc.)
- Feature availability on different hardware (low-memory, low-performance devices)
- Differences between emulators and real devices

### Common defects
- Crashes when calling new APIs on old OS versions
- App killed in the background or push not received on specific vendor ROMs
- Stutter or crashes on low-end devices

---

## 8. System Interaction

### Key focus points
- Invoking the system share sheet; correctness of the shared content / link
- Copy and paste: across apps, format retention
- Compatibility with the system keyboard and third-party input methods
- Screenshots / screen recording: anti-capture protection on sensitive pages (payment, password)
- Launching external apps: system browser, phone, SMS, email, maps

### Common defects
- Shared content or link missing or wrongly formatted
- Input issues with third-party input methods
- No prompt when launching an external app fails
- No anti-capture protection on payment / password pages

---

## 9. Storage and Data

### Key focus points
- Choice of local storage: SharedPreferences / Keychain / SQLite / Room / CoreData
- Cache strategy: image cache, API data cache, cache expiration and cleanup
- Offline data: conflict handling when syncing local cache → online
- Recovery behavior after clearing cache / clearing data
- Security of sensitive data storage (encrypted token storage; never store passwords in plain text)

### Common defects
- After clearing cache, the login session is lost but the UI still shows logged in
- Offline changes overwritten during sync
- Tokens stored unencrypted, creating security risks
- No cache expiration policy, leading to stale data

---

## 10. Updates and Versions

### Key focus points
- Trigger conditions and user guidance for forced vs optional updates
- Rollback mechanism for hot updates (React Native / Flutter, etc.)
- Compatibility handling when data structures differ between old and new versions
- Gradual rollout: release progressively by percentage / region / user group
- Update package integrity verification (tamper protection)
- Downgrade scenario: data compatibility after the user rolls back to an old version

### Common defects
- The forced update pop-up cannot be closed but the download fails, leaving the user stuck
- Old data lost after a database schema change in the new version
- App crashes after a failed hot update and cannot roll back automatically
- Local cache format incompatible after downgrading

---

## 11. Performance Experience

### Key focus points
- Cold / hot start time
- Scrolling smoothness (lists, page transitions)
- Memory usage (especially long lists and image-heavy pages)
- Battery consumption (background location, push, etc.)

### Common defects
- Choppy list scrolling
- Blank screen during page transitions
- Continuous battery drain in the background

---

## 12. Accessibility

### Key focus points
- Screen reader compatibility (iOS VoiceOver / Android TalkBack)
- All images and icons have a contentDescription or accessibilityLabel
- Effect of system font size on layout (iOS Accessibility → Larger Text)
- High-contrast mode adaptation
- Touch target size: iOS ≥ 44×44pt, Android ≥ 48×48dp
- Focus navigation order (focus movement in accessibility mode)
- Captions or text alternatives for video / audio content

### Common defects
- Images / icons missing accessibility labels
- Text truncated or overlapping after enlarging the system font
- Screen readers cannot correctly describe the page structure
- Custom components not correctly recognized by accessibility APIs
