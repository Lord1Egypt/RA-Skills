# Mini Program Test Points

> This file defines the test dimensions and strategy points that distinguish mini programs from other platforms.
> For the output format, see `references/examples/format-spec.md`; for the checklist, see `references/checklists/mini-program-checklist.md`.

---

## 1. Lifecycle

### Key focus points
- Differences in data loading between cold start and hot start
- Page state restoration when switching to the background and back to the foreground
- After a long time in the background, the mini program is destroyed by WeChat → must reload when reopened
- Page stack management: at most 10 levels of pages; new pages cannot be opened beyond that

### Common defects
- Data not refreshed after returning to the foreground, still showing old data
- Page stack overflow prevents navigation
- Global data lost when restoring after being destroyed in the background

---

## 2. Authorization Management

### Key focus points
- Privacy authorization: when processing users' personal information, the privacy protection guidelines must be shown first, and privacy-related APIs or components can be called only after the user agrees
- Privacy APIs not declared in the "Mini Program User Privacy Protection Guidelines" cannot be called
- Avatar and nickname: obtained via the avatar and nickname filling capability (button open-type="chooseAvatar", input type="nickname"); getUserProfile no longer returns the real avatar and nickname
- Phone number authorization flow (triggered by button open-type="getPhoneNumber")
- Authorization for system permissions such as location / camera / photo album
- Feature degradation and guidance after authorization is denied
- Persistence and expiration handling of authorization state

### Common defects
- Calling privacy APIs without agreement to the privacy guidelines, causing the calls to fail
- No prompt or a frozen feature after privacy authorization is denied
- Still using getUserProfile for avatar and nickname, getting only the default grey avatar and the nickname "WeChat User"
- Subsequent logic executed before the authorization pop-up is triggered
- No guidance after authorization is denied
- Authorization not re-obtained after expiration

---

## 3. Sharing

### Key focus points
- Sharing from the top-right menu vs an in-page button (onShareAppMessage vs onShareTimeline)
- Configuration of share card title / description / cover image / path
- Differences between sharing to friends and sharing to Moments
- Parameter passing and page routing when opened from a share card

### Common defects
- Share card cover image not configured, showing a default screenshot
- Share path parameters lost, opening a blank page
- Moments sharing not supported in some scenarios

---

## 4. Payment

### Key focus points
- WeChat Pay invocation flow and callback handling
- Order status after payment interruption (user cancels / network exception)
- Payment security: amount verification, prevention of duplicate payment
- iOS virtual payment restrictions (virtual goods may not be purchased within mini programs)

### Common defects
- Payment succeeded but the front end did not receive the callback, causing inconsistent status
- After the user cancels payment, the order still shows "Pending Payment"
- iOS virtual goods payments rejected in review

---

## 5. Mini Program Navigation

### Key focus points
- Navigating to other mini programs (the appid list must be configured)
- Data passing when returning from another mini program
- Opening H5 pages via the web-view component, and two-way communication between H5 and the mini program
- Usage restrictions of half-screen mini programs

### Common defects
- Navigation fails because the target mini program appid is not configured
- Communication between web-view and the mini program is lost
- Wrong navigation parameter format

---

## 6. Subscription Messages

> Mini program template messages have been retired; subscription messages are used instead.

### Key focus points
- Differences between one-time and long-term subscriptions (long-term subscriptions are only open to specific industry categories)
- Trigger timing and frequency limits of the subscription authorization pop-up
- Message template content configuration and parameter filling
- Fallback when the user turns off notifications

### Common defects
- Cannot push again after a one-time subscription is used up
- Message sending fails because template parameters are not filled
- Induced subscriptions rejected in review

---

## 7. Storage and Cache

### Key focus points
- The 10 MB limit of wx.setStorage / wx.setStorageSync
- Storage data persistence: whether it is retained after the mini program is updated
- Recovery behavior after cache clearing (manual by the user / automatic by the system)
- Performance issues with synchronous Storage writes (large data should be written in batches)
- Security of sensitive data storage (encrypt tokens; never store passwords in plain text)

### Common defects
- Writes silently fail after exceeding the 10 MB limit
- Blank page or data loss after cache clearing
- Stutter caused by synchronously writing large amounts of data
- Tokens stored unencrypted

---

## 8. Maps and Location

### Key focus points
- Map component performance: rendering many markers, smoothness of zooming
- Location accuracy: GPS vs WiFi vs cell towers; permissions affect accuracy
- Privacy compliance: location can only be obtained with user authorization
- Background location: mini programs do not support continuous background location
- Recall accuracy and performance of nearby POI search
- Loading of map layer overlays (traffic / satellite)

### Common defects
- Blank map or crash after location permission is denied
- Map stutters with many markers
- Large location deviation (inaccurate indoor WiFi positioning)
- POI search results not as expected

---

## 9. Platform Difference Adaptation

### Key focus points
- API differences between WeChat / Alipay / Baidu / Douyin mini programs
- Component compatibility (e.g., confirm-type of the input component)
- Login flow differences (wx.login vs my.getAuthCode)
- Review guideline differences (each platform has different content / feature requirements)

### Common defects
- Passes only on WeChat, with compatibility issues on other platforms
- Errors on other platforms caused by non-standard APIs
