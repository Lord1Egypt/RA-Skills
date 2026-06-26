# Mobile App Platform-Specific Testing

> This document defines specialized testing dimensions and strategy highlights specific to mobile apps, distinct from other platforms.
> See `references/examples/format-spec.md` for output format and `references/checklists/mobile-app-checklist.md` for the checklist.

---

## I. Gesture Operations

### Focus Areas
- Touch target size ≥ 44×44px, especially for icon buttons and list swipe operation areas
- Gesture conflicts: swipe-to-page vs swipe-to-delete vs swipe-to-go-back
- Edge gestures: left-swipe-back (iOS), bottom-swipe-up (system gesture area) may be intercepted by the App
- Priority between multi-finger and single-finger gestures

### Common Defects
- Small touch targets causing mis-tapping
- Inner and outer gesture conflicts in nested scrolling
- Long-press triggering conflicting with scrolling

---

## II. Interruption Recovery

### Focus Areas
- System interruptions: incoming calls, SMS, alarms, low battery alerts, system update notifications
- Memory reclamation after backgrounding causing page reconstruction (more aggressive on Android)
- Mid-form-filling interruption → whether data is retained upon return
- Payment flow interruption → whether order status is consistent

### Common Defects
- White screen or crash after returning from interruption
- Form data loss
- Inconsistent payment status (user charged but order not updated)
- App killed by system after extended backgrounding, abnormal recovery

---

## III. Network Switching

### Focus Areas
- Handling of in-progress requests during WiFi ↔ 4G/5G switching
- User experience under weak network conditions (high latency/low bandwidth/high packet loss)
- Auto-reconnection after airplane mode/disconnection → recovery
- Degradation when network permission is disabled by the system

### Common Defects
- Requests hanging without response during network switching
- Infinite loading without timeout prompts under weak network
- Image/resource loading failure without placeholders after disconnection

---

## IV. Permission Management

### Focus Areas
- Must explain purpose when requesting permissions for the first time (mandatory on iOS, recommended on Android)
- Function degradation after denial: core paths must not break
- Guiding to settings page after "Don't ask again"
- State synchronization after permission revocation (turning off in system settings)
- iOS/Android permission mechanism differences

### Common Defects
- Crash or freeze after denial
- No guidance to settings page; user doesn't know how to restore
- Permission state not refreshed after returning from background

---

## V. Push Notifications

### Focus Areas
- Notification permission request timing (should ask after user understands the value)
- Notification tap navigation: different handling paths for cold start vs warm start
- Notification parameter passing and page routing
- iOS/Android notification mechanism differences

### Common Defects
- Tapping notification goes to home page instead of target page
- Notification parameters lost during cold start
- No prompt in-app when notification permission is off

---

## VI. Device Compatibility

### Focus Areas
- iOS/Android version differences (new API compatibility, deprecated API handling)
- Different manufacturer ROM differences (Xiaomi MIUI, Huawei EMUI, OPPO ColorOS, etc.)
- Notch/punch-hole/foldable/tall screen safe area adaptation
- Impact of system font size settings on layout

### Common Defects
- Content obscured by notch
- Layout broken after system font enlargement
- Abnormal layout after foldable screen unfolding/folding

---

## VII. Storage & Data

### Focus Areas
- Local storage solution selection: SharedPreferences / Keychain / SQLite / Room / CoreData
- Caching strategy: image caching, API data caching, cache expiration and cleanup
- Offline data: conflict handling for local cache → online synchronization
- Recovery behavior after cache clearing/data clearing
- Secure storage of sensitive data (Token encryption, prohibition of plaintext password storage)

### Common Defects
- Login state lost after cache clearing but UI still shows logged in
- Offline operation data overwritten during synchronization
- Unencrypted Token storage causing security risks
- No cache expiration policy causing stale data

---

## VIII. Updates & Versioning

### Focus Areas
- Trigger conditions and user guidance for mandatory vs optional updates
- Rollback mechanism for hot updates (React Native/Flutter, etc.)
- Compatibility handling for data structure inconsistencies between old and new versions
- Phased rollout: gradual release by percentage/region/user group
- Update package integrity verification (tamper prevention)
- Downgrade scenarios: data compatibility when user rolls back to old version

### Common Defects
- Mandatory update dialog can't be dismissed but download fails, user stuck
- Old data lost after new version database schema changes
- App crashes after hot update failure with no auto-rollback
- Local cache format incompatible after downgrade

---

## IX. Performance Experience

### Focus Areas
- Cold start/warm start time
- Scroll smoothness (lists, page transitions)
- Memory usage (especially long lists, image-heavy pages)
- Battery consumption (background location, push, etc.)

### Common Defects
- List scrolling stutter
- White screen during page transitions
- Persistent background battery drain

---

## X. Accessibility

### Focus Areas
- Screen reader compatibility (iOS VoiceOver / Android TalkBack)
- All images and icons have contentDescription or accessibilityLabel
- Impact of system font size adjustment on layout (iOS Accessibility → Larger Text)
- High contrast mode adaptation
- Touch target size ≥ 44×44dp
- Focus navigation order (focus movement in accessibility mode)
- Video/audio content has captions or text alternatives

### Common Defects
- Images/icons lack accessibility labels
- Text truncated or overlapping after system font enlargement
- Screen reader unable to correctly describe page structure
- Custom components not correctly identified by accessibility APIs
