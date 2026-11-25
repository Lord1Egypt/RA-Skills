# Mobile Web Test Points

> This file defines the test dimensions and strategy points that distinguish mobile web (H5) from other platforms.
> For the output format, see `references/examples/format-spec.md`; for the checklist, see `references/checklists/mobile-web-checklist.md`.

---

## 1. Browser Compatibility

### Key focus points
- iOS Safari / Android Chrome / WeChat built-in browser / QQ Browser / UC Browser
- WebView container differences (WKWebView vs Android WebView)
- CSS feature compatibility (flexbox gap, aspect-ratio, etc.)
- JavaScript API compatibility (IntersectionObserver, ResizeObserver, etc.)
- Effect of private / incognito mode on Storage

### Common defects
- Date format parsing differences in iOS Safari (yyyy-MM-dd must be handled)
- Long-press QR code recognition in the WeChat built-in browser interferes with page interaction
- localStorage writes throw errors in private mode

---

## 2. Touch Interaction

### Key focus points
- Visual feedback for tap states (compatibility of the :active pseudo-class on mobile)
- Tap delay compatibility in older WebViews (touch-action / viewport configuration)
- Smoothness of swipe paging / carousels
- Pinch-zoom restrictions and page-level zoom control
- Gesture conflicts in nested scroll areas
- Momentum scrolling and rubber-band effect

### Common defects
- No visual feedback on tap, so the user is unsure whether it registered
- Page stutters when scrolling quickly
- Inner and outer scrolling conflicts in nested lists

---

## 3. Responsive Layout

### Key focus points
- Key breakpoints: 320px / 375px / 414px / 768px
- Whether media query breakpoints cover all target devices
- Safe area adaptation for notched / punch-hole screens (env(safe-area-inset-*))
- Landscape layout switching
- Content display differences between tall screens (19.5:9) and short screens (16:9)

### Common defects
- Text truncated or overlapping on small screens
- Layout broken in landscape
- Content hidden by the notch

---

## 4. Viewport Configuration

### Key focus points
- viewport meta configuration (width, initial-scale, viewport-fit)
- Viewport height changes when the virtual keyboard opens / closes (behavior of 100vh on mobile)
- Viewport recalculation on screen rotation
- Whether zoom restrictions (user-scalable, maximum-scale) take effect
- Viewport adaptation in split-screen mode

### Common defects
- 100vh includes the address bar height, causing wrong page height calculations
- Layout not recalculated after rotating the screen
- Page does not return to its original position after the keyboard closes

---

## 5. Keyboard and Input

### Key focus points
- Input box hidden by the keyboard after focusing
- Keyboard types triggered by different input types (number / tel / email / url)
- Chinese IME composition events (compositionstart / end)
- Form autofill, show / hide password toggle
- Maximum length restrictions and input format validation

### Common defects
- Input box hidden after the keyboard opens
- Multiple requests triggered while searching with a Chinese IME
- Full keyboard shown for a numeric input box

---

## 6. H5-Specific Features

### Key focus points
- Triggering and parameters of tel: / sms: / mailto: links
- Browser support and fallback for the Web Share API
- PWA: add to home screen, Service Worker offline cache
- Geolocation / camera access (requires HTTPS + user authorization)
- Scroll-through and scroll locking for pop-ups

### Common defects
- Background still scrolls when a pop-up is open (scroll-through)
- Wrong PWA manifest configuration causes add-to-home-screen to fail
- Geolocation API unavailable in HTTP environments

---

## 7. Third-Party Login and Payment

### Key focus points
- WeChat H5 authorized login (must be in the WeChat browser, uses OAuth 2.0)
- WeChat H5 payment (payment directory and domain must be configured)
- Alipay H5 payment flow
- Parameter passing and state restoration for authorization callback URLs
- Login state synchronization across multiple tabs

### Common defects
- WeChat login cannot be invoked outside the WeChat browser
- Wrong payment callback URL configuration causes payment to fail
- Login state not synchronized across tabs

---

## 8. WebView-Specific

### Key focus points
- JSBridge: two-way calls between H5 and the native app, handling of call failures
- Physical back button (Android): go back to the previous page or close the WebView
- Navigation bar: title synchronization, custom navigation bar
- Invoking native capabilities: camera, photo album, location, QR scanning
- Login state synchronization: passing the app login state to H5 (cookie / token sync)
- Loading progress bar and load-failure error page

### Common defects
- JSBridge called before injection completes, causing failure
- Android back button closes the whole WebView directly
- App is logged in but the H5 page shows not logged in

---

## 9. Network and Cache

### Key focus points
- Loading prompts and timeout handling on weak networks
- Offline prompt and automatic reconnection after network recovery
- Service Worker cache strategies: Cache First / Network First / Stale While Revalidate
- HTTP cache header configuration (Cache-Control / ETag / Last-Modified)
- Offline degradation: which features are available and which need a prompt
- Cache update mechanism: how users get the latest resources after a version update
- Pre-caching key resources (App Shell model)

### Common defects
- Endless loading without a timeout prompt on weak networks
- Wrong cache strategy causes users to always see the old version
- Blank page with no fallback prompt when offline
- Old resources not invalidated after a cache update
- Service Worker errors make the page permanently unable to load

---

## 10. Performance Experience

### Key focus points
- First-screen load time, FCP, LCP, and other core metrics (follow project requirements; when none exist, use the reference values in the checklist)
- Image compression and lazy loading
- Skeleton screen display
- Rendering smoothness for scrolling, animation, etc.
- Memory usage after staying on the page for a long time (whether it keeps growing)

### Common defects
- Long blank first screen
- Uncompressed images cause slow loading and heavy data usage
- Choppy scrolling in long lists

---

## 11. SEO and Sharing

### Key focus points
- WeChat share card: title / description / cover image (depends on JS-SDK or meta tags)
- Open Graph tag configuration
- Page title and meta description
- Passing URL parameters in share links

### Common defects
- WeChat share not using JS-SDK, so page content is scraped by default
- Share cover image not configured
- URL parameters lost when sharing
