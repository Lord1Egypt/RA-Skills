# Mini-Program Platform-Specific Testing

> This document defines specialized testing dimensions and strategy highlights specific to mini-programs, distinct from other platforms.
> See `references/examples/format-spec.md` for output format and `references/checklists/mini-program-checklist.md` for the checklist.

---

## I. Lifecycle

### Focus Areas
- Data loading differences between cold start and warm start
- Page state restoration when switching to background → foreground
- Mini-program destroyed by WeChat after extended background → must reload on reopen
- Page stack management: maximum 10 page layers; new pages cannot be opened beyond this limit

### Common Defects
- Data not refreshed but still showing old data after returning to foreground
- Page stack overflow preventing navigation
- Global data lost when recovering after background destruction

---

## II. Authorization Management

### Focus Areas
- WeChat user info/phone number authorization flow (triggered by button component)
- System permission authorization for location/camera/photo library
- Function degradation and guidance after authorization denial
- Authorization state persistence and expiry handling

### Common Defects
- Subsequent logic executed before authorization dialog is triggered
- No guidance prompt after authorization denial
- Authorization not re-acquired after expiry

---

## III. Sharing Functionality

### Focus Areas
- Top-right menu share vs in-page button share (onShareAppMessage vs onShareTimeline)
- Share card title/description/cover image/path configuration
- Differences between sharing to friend and sharing to Moments
- Parameter passing and page routing when opened from share card

### Common Defects
- Share card cover image not configured, showing default screenshot
- Share path parameters lost, causing blank page on open
- Moments sharing not supported for some scenarios

---

## IV. Payment Functionality

### Focus Areas
- WeChat Pay invocation flow and callback handling
- Order status after payment interruption (user cancellation/network exception)
- Payment security: amount verification, duplicate payment prevention
- iOS virtual goods payment restriction (virtual goods cannot be purchased within mini-programs)

### Common Defects
- Payment successful but frontend doesn't receive callback, causing status inconsistency
- Order still shows "Pending Payment" after user cancels
- iOS virtual goods payment rejected in review

---

## V. Mini-Program Navigation

### Focus Areas
- Navigating to other mini-programs (requires appid list configuration)
- Data passing when returning from another mini-program
- web-view component opening H5 and bidirectional communication between H5 and mini-program
- Usage restrictions of half-screen mini-programs

### Common Defects
- Target mini-program appid not configured, causing navigation failure
- Communication lost between web-view and mini-program
- Navigation parameter format errors

---

## VI. Subscription Messages

### Focus Areas
- Differences between one-time subscription and long-term subscription
- Trigger timing and frequency limits for subscription authorization dialog
- Message template content configuration and parameter filling
- Degradation handling when user turns off notifications

### Common Defects
- Cannot push again after one-time subscription is exhausted
- Message template parameters not filled, causing send failure
- Induced subscription rejected in review

---

## VII. Storage & Cache

### Focus Areas
- 10MB capacity limit for wx.setStorage / wx.setStorageSync
- Storage data persistence: whether data is retained after mini-program update
- Recovery behavior after cache clearing (manual/system)
- Performance issues with synchronous Storage writes (large data should be batched)
- Secure storage of sensitive data (Token encryption, prohibition of plaintext password storage)

### Common Defects
- Silent write failure after exceeding 10MB limit
- White screen or data loss after cache clearing
- Stutter caused by synchronous writes of large data
- Token stored without encryption

---

## VIII. Map & Location

### Focus Areas
- Map component performance: multi-marker rendering, region zoom smoothness
- Location accuracy: GPS vs WiFi vs cell tower, permission impact on accuracy
- Privacy compliance: location must only be obtained with user authorization
- Background location: mini-programs do not support continuous background location
- Recall accuracy and performance of nearby POI search
- Loading of map layer overlays (traffic/satellite)

### Common Defects
- Map white screen or crash after location permission denial
- Map stutter with large number of markers
- Excessive location deviation (inaccurate indoor WiFi positioning)
- POI search results not matching expectations

---

## IX. Platform Difference Adaptation

### Focus Areas
- API differences between WeChat/Alipay/Baidu/Douyin mini-programs
- Component compatibility (e.g., input component's confirm-type)
- Login flow differences (wx.login vs my.getAuthCode)
- Review guideline differences (different platforms have different content/functionality requirements)

### Common Defects
- Only tested on WeChat; compatibility issues on other platforms
- Non-standard API usage causing errors on other platforms
