# Mobile App Testing Checklist

> The sections of this checklist correspond one-to-one with `references/platform/mobile-app.md` and are used for item-by-item self-checking after test case design.

## Gestures
- [ ] Tap
- [ ] Double tap
- [ ] Long press
- [ ] Swipe
- [ ] Pinch to zoom
- [ ] Drag
- [ ] Pull to refresh
- [ ] Load more on scroll
- [ ] Multi-finger gestures
- [ ] Gesture conflicts
- [ ] Gesture feedback
- [ ] Disabled gestures
- [ ] Special gestures
- [ ] Accessibility gestures

## Screen Adaptation
- [ ] Small-screen devices
- [ ] Medium-screen devices
- [ ] Large-screen devices
- [ ] Tablets
- [ ] Tall-screen devices
- [ ] Notched screens
- [ ] Foldables
- [ ] Landscape mode
- [ ] Portrait mode
- [ ] Switching between portrait and landscape
- [ ] Resolution adaptation
- [ ] System font size

## Interruption Recovery
- [ ] Incoming call interruption
- [ ] SMS interruption
- [ ] Push notification interruption
- [ ] Alarm interruption
- [ ] Low battery pop-up
- [ ] System update prompt
- [ ] Switching to the background and back
- [ ] Multitasking switching
- [ ] Long time in the background
- [ ] Restart after the process is killed
- [ ] Interruption while filling in a form
- [ ] Interruption during payment
- [ ] Playback interruption
- [ ] Network request interruption

## Network Switching
- [ ] WiFi network
- [ ] 4G/5G network
- [ ] Switching between WiFi and 4G/5G
- [ ] Weak network - high latency
- [ ] Weak network - low bandwidth
- [ ] Weak network - high packet loss
- [ ] Offline detection
- [ ] Reconnection after going offline
- [ ] Airplane mode
- [ ] Offline mode
- [ ] Network switch during submission
- [ ] Network switch during download
- [ ] Network switch during upload
- [ ] Network switch during video playback
- [ ] Network permission disabled
- [ ] DNS resolution failure

## Permission Management
- [ ] Camera permission
- [ ] Photo album permission
- [ ] Location permission
- [ ] Notification permission
- [ ] Microphone permission
- [ ] Storage permission
- [ ] Contacts permission
- [ ] Bluetooth permission
- [ ] Feature degradation after permission denial
- [ ] Guidance to the permission settings page
- [ ] Permission revocation
- [ ] Permission state persistence

## Push Notifications
- [ ] Timing of the notification permission request
- [ ] Push display in the foreground
- [ ] Push display in the background
- [ ] Navigation on cold start from a notification tap
- [ ] Navigation on hot start from a notification tap
- [ ] Notification parameter passing and page routing
- [ ] Degradation prompt after notification permission is turned off
- [ ] Differences between iOS and Android notification mechanisms

## Device Compatibility
- [ ] Latest iOS version
- [ ] Older iOS versions
- [ ] Latest Android version
- [ ] Older Android versions
- [ ] Different vendor ROMs
- [ ] Different screen resolutions
- [ ] Different hardware configurations
- [ ] iPad tablets
- [ ] Foldable devices
- [ ] Emulators

## System Interaction
- [ ] System sharing
- [ ] Copy and paste
- [ ] System keyboard
- [ ] Screenshots
- [ ] Screen recording
- [ ] Opening the system browser
- [ ] Making phone calls
- [ ] Sending SMS
- [ ] Sending email
- [ ] Opening maps

## Storage and Data
- [ ] SharedPreferences / Keychain read and write work
- [ ] SQLite / Room / CoreData database operations work
- [ ] Image cache strategy takes effect
- [ ] API data cache strategy takes effect
- [ ] Expired cache is cleaned automatically
- [ ] Manual cache cleanup works
- [ ] Offline data is stored locally
- [ ] Offline data syncs online without conflicts
- [ ] Login state is consistent after clearing the cache
- [ ] Sensitive data (tokens / passwords) is stored encrypted

## Updates and Versions
- [ ] Forced update pop-up can be triggered
- [ ] Optional update pop-up can be closed
- [ ] Update download progress is shown correctly
- [ ] Failed update downloads can be retried
- [ ] Update package integrity check passes
- [ ] Data migration after update works
- [ ] Hot updates (React Native / Flutter) load correctly
- [ ] Failed hot updates roll back automatically
- [ ] Gradual rollout by percentage works
- [ ] Data compatibility after downgrading to an old version

## Performance Experience
- [ ] Cold start time
- [ ] Hot start time
- [ ] First-screen load time
- [ ] Page load time
- [ ] Scrolling smoothness
- [ ] Animation smoothness
- [ ] Memory usage
- [ ] CPU usage
- [ ] Battery consumption
- [ ] Heat control
- [ ] Data usage
- [ ] Storage space

## Accessibility
- [ ] Screen reader compatibility (VoiceOver / TalkBack)
- [ ] All images and icons have contentDescription (Android) / accessibilityLabel (iOS)
- [ ] Font size is adjustable
- [ ] High-contrast mode is supported
- [ ] Touch areas are large enough (iOS ≥ 44×44pt, Android ≥ 48×48dp)
- [ ] All features can be operated by gesture + voice
- [ ] Videos have captions
- [ ] Important information has haptic feedback
