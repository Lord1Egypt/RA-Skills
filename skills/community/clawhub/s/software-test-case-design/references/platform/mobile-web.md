# Mobile Web Platform-Specific Testing

> This document defines specialized testing dimensions and strategy highlights specific to Mobile Web (H5), distinct from other platforms.
> See `references/examples/format-spec.md` for output format and `references/checklists/mobile-web-checklist.md` for the checklist.

---

## I. Responsive Layout

### Focus Areas
- Key breakpoint adaptation: 320px / 375px / 414px / 768px
- Whether media query breakpoints cover all target devices
- Notch/punch-hole screen safe area adaptation (env(safe-area-inset-*))
- Landscape layout switching
- Content display differences between tall screens (19.5:9) and short screens (16:9)

### Common Defects
- Text truncation or overlap on small screens
- Layout broken in landscape mode
- Content obscured by notch

---

## II. Touch Interaction

### Focus Areas
- Tap-state visual feedback (:active pseudo-class compatibility on mobile)
- 300ms tap delay and touch-action handling
- Smoothness of swipe-to-page/carousel
- Pinch-to-zoom restrictions and page-level zoom control
- Gesture conflicts in nested scroll areas
- Inertial scrolling and rubber band effect

### Common Defects
- No visual feedback on tap; user unsure if it registered
- Page stutter during fast swiping
- Inner/outer scroll conflicts in nested lists

---

## III. Browser Compatibility

### Focus Areas
- iOS Safari / Android Chrome / WeChat built-in browser / QQ Browser / UC Browser
- WebView container differences (WKWebView vs Android WebView)
- CSS feature compatibility (flexbox gap, aspect-ratio, etc.)
- JavaScript API compatibility (IntersectionObserver, ResizeObserver, etc.)
- Impact of private/incognito mode on Storage

### Common Defects
- iOS Safari date format parsing differences (requires yyyy-MM-dd compatibility)
- WeChat built-in browser long-press QR code recognition interfering with page interaction
- localStorage write errors in private mode

---

## IV. Viewport & Input

### Focus Areas
- viewport meta configuration (width, initial-scale, viewport-fit)
- Layout adjustment when virtual keyboard appears (100vh behavior on mobile)
- Input field obscured by keyboard when focused
- Keyboard types triggered by different input types (number/tel/email/url)
- Chinese input method composition events (compositionstart/end)

### Common Defects
- Input field obscured after keyboard appears
- 100vh including address bar height causing page height calculation errors
- Multiple requests triggered during Chinese input method search

---

## V. Third-Party Login & Payment

### Focus Areas
- WeChat H5 authorized login (must be in WeChat browser, uses OAuth2.0)
- WeChat H5 payment (must configure payment directory and domain)
- Alipay H5 payment flow
- Parameter passing and state restoration in authorization callback URLs
- Login state synchronization across multiple tabs

### Common Defects
- Cannot invoke WeChat login outside WeChat browser
- Payment callback URL misconfiguration causing payment failure
- Login state not synchronized across tabs

---

## VI. H5-Specific Features

### Focus Areas
- tel:/sms:/mailto: link triggering and parameters
- Web Share API browser support and degradation
- PWA: Add to Home Screen, Service Worker offline caching
- Geolocation/camera invocation (requires HTTPS + user authorization)
- Scroll penetration and modal locking

### Common Defects
- Background still scrollable when modal is open (scroll penetration)
- PWA manifest misconfiguration causing Add to Home Screen failure
- Geolocation API unavailable under HTTP

---

## VII. Cache & Offline

### Focus Areas
- Service Worker caching strategies: Cache First / Network First / Stale While Revalidate
- HTTP cache header configuration (Cache-Control / ETag / Last-Modified)
- Offline access degradation: which features are available, which require prompts
- Cache update mechanism: how users get the latest resources after version update
- Pre-caching critical resources (App Shell pattern)

### Common Defects
- Incorrect caching strategy causing users to always see old version
- White screen with no degradation prompt when offline
- Old resources not invalidated after cache update
- Service Worker anomaly causing permanent page load failure

---

## VIII. SEO & Sharing

### Focus Areas
- WeChat share card: title/description/cover image (relies on JS-SDK or meta tags)
- Open Graph tag configuration
- Page title and meta description
- URL parameter passing in share links

### Common Defects
- WeChat share not calling JS-SDK, resulting in default page content scraping
- Share cover image not configured
- URL parameters lost in sharing
