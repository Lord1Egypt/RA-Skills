# Mobile App Testing Checklist

## Gesture Operations (15 items)
- [ ] Tap operation testing
- [ ] Double-tap operation testing
- [ ] Long-press operation testing
- [ ] Swipe operation testing
- [ ] Pinch-to-zoom operation testing
- [ ] Drag operation testing
- [ ] Pull-to-refresh testing
- [ ] Pull-up-to-load-more testing
- [ ] Multi-finger gesture testing
- [ ] Gesture conflict testing
- [ ] Gesture feedback testing
- [ ] Gesture disabling testing
- [ ] Special gesture testing
- [ ] Accessibility gesture testing
- [ ] Gaming gesture testing

## Screen Adaptation (12 items)
- [ ] Small screen device testing
- [ ] Medium screen device testing
- [ ] Large screen device testing
- [ ] Tablet device testing
- [ ] Tall screen device testing
- [ ] Notch screen testing
- [ ] Foldable screen testing
- [ ] Landscape mode testing
- [ ] Portrait mode testing
- [ ] Portrait-landscape rotation testing
- [ ] Resolution adaptation testing
- [ ] System font size testing

## Interruption Recovery (14 items)
- [ ] Incoming call interruption testing
- [ ] SMS interruption testing
- [ ] Push notification interruption testing
- [ ] Alarm interruption testing
- [ ] Low battery alert testing
- [ ] System update notification testing
- [ ] Background-and-return testing
- [ ] Multi-task switching testing
- [ ] Extended background time testing
- [ ] Process-killed restart testing
- [ ] Form-filling interruption testing
- [ ] Payment flow interruption testing
- [ ] Playback interruption testing
- [ ] Network request interruption testing

## Network Switching (16 items)
- [ ] WiFi network testing
- [ ] 4G/5G network testing
- [ ] WiFi ↔ 4G/5G switching testing
- [ ] Weak network - high latency testing
- [ ] Weak network - low bandwidth testing
- [ ] Weak network - high packet loss testing
- [ ] Network disconnection detection testing
- [ ] Reconnection after disconnection testing
- [ ] Airplane mode testing
- [ ] Offline mode testing
- [ ] Network switch during submission testing
- [ ] Network switch during download testing
- [ ] Network switch during upload testing
- [ ] Network switch during video playback testing
- [ ] Network permission disabled testing
- [ ] DNS resolution failure testing

## Device Compatibility (10 items)
- [ ] Latest iOS version testing
- [ ] Older iOS version testing
- [ ] Latest Android version testing
- [ ] Older Android version testing
- [ ] Different manufacturer ROM testing
- [ ] Different screen resolution testing
- [ ] Different hardware configuration testing
- [ ] iPad tablet testing
- [ ] Foldable device testing
- [ ] Emulator testing

## Permission Management (12 items)
- [ ] Camera permission testing
- [ ] Photo library permission testing
- [ ] Location permission testing
- [ ] Notification permission testing
- [ ] Microphone permission testing
- [ ] Storage permission testing
- [ ] Contacts permission testing
- [ ] Bluetooth permission testing
- [ ] Function degradation after permission denial testing
- [ ] Permission settings page guidance testing
- [ ] Permission revocation testing
- [ ] Permission state persistence testing

## Push Notifications (8 items)
- [ ] Notification permission request timing
- [ ] Foreground push display
- [ ] Background push display
- [ ] Cold start navigation via notification tap
- [ ] Warm start navigation via notification tap
- [ ] Notification parameter passing and page routing
- [ ] Degradation prompt when notification permission is off
- [ ] iOS/Android notification mechanism differences

## System Interaction (10 items)
- [ ] System sharing testing
- [ ] Copy-paste testing
- [ ] System keyboard testing
- [ ] Screenshot functionality testing
- [ ] Screen recording functionality testing
- [ ] System browser open testing
- [ ] Phone call testing
- [ ] SMS sending testing
- [ ] Email sending testing
- [ ] Map open testing

## Performance Experience (12 items)
- [ ] Cold start time testing
- [ ] Warm start time testing
- [ ] First-screen load time testing
- [ ] Page load time testing
- [ ] Scroll smoothness testing
- [ ] Animation smoothness testing
- [ ] Memory usage testing
- [ ] CPU usage testing
- [ ] Battery consumption testing
- [ ] Thermal control testing
- [ ] Data usage testing
- [ ] Storage space testing

## Accessibility (8 items)
- [ ] Screen reader compatibility (VoiceOver/TalkBack)
- [ ] All images have alt text or descriptions
- [ ] Font size is adjustable
- [ ] High contrast mode supported
- [ ] Touch targets are large enough (≥ 44×44px)
- [ ] All functions operable by gesture + voice
- [ ] Videos have captions
- [ ] Important information has haptic feedback

## Storage & Data (10 items)
- [ ] SharedPreferences/Keychain read/write works correctly
- [ ] SQLite/Room/CoreData database operations work correctly
- [ ] Image caching strategy takes effect
- [ ] API data caching strategy takes effect
- [ ] Cache expiration auto-cleanup works
- [ ] Manual cache clearing works correctly
- [ ] Offline data local storage works correctly
- [ ] Offline-to-online sync has no conflicts
- [ ] Login state remains consistent after cache clearing
- [ ] Sensitive data (Token/password) is stored encrypted

## Updates & Versioning (10 items)
- [ ] Mandatory update dialog triggers correctly
- [ ] Optional update dialog can be dismissed
- [ ] Update download progress displays correctly
- [ ] Update download failure can retry
- [ ] Update package integrity verification passes
- [ ] Data migration after update works correctly
- [ ] Hot update (React Native/Flutter) loads correctly
- [ ] Hot update failure auto-rollback works
- [ ] Phased rollout scales correctly by percentage
- [ ] Downgrade to old version has data compatibility
