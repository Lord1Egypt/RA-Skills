# Mobile Web Testing Checklist

> The sections of this checklist correspond one-to-one with `references/platform/mobile-web.md` and are used for item-by-item self-checking after test case design.

## Browser Compatibility
- [ ] Latest iOS Safari works
- [ ] Mainstream iOS Safari versions are compatible
- [ ] Android Chrome works
- [ ] Mainstream Android Chrome versions are compatible
- [ ] WeChat built-in browser works
- [ ] QQ Browser works
- [ ] UC Browser works
- [ ] Quark Browser works
- [ ] Samsung Internet works
- [ ] Private / incognito mode works
- [ ] WebView (WKWebView / Android) compatibility
- [ ] JavaScript feature compatibility

## Touch Interaction
- [ ] Single tap responds normally
- [ ] Double-tap to zoom
- [ ] Long press triggers the context menu
- [ ] Swipe left / right to switch
- [ ] Swipe up / down to scroll
- [ ] Pinch to zoom
- [ ] Pull to refresh
- [ ] Load more on scroll
- [ ] Visual feedback on tap
- [ ] Touch disabling settings take effect
- [ ] No conflicts in nested scrolling
- [ ] Rubber-band effect works
- [ ] Smooth momentum scrolling
- [ ] Gesture conflicts handled correctly

## Responsive Layout
- [ ] 320px width works
- [ ] 375px width works
- [ ] 414px width works
- [ ] 768px (iPad) width works
- [ ] Tall screens (19.5:9) adapted
- [ ] Content not hidden by the notch
- [ ] Correct media query breakpoints
- [ ] Images adapt to width
- [ ] Font size adaptation
- [ ] Horizontal scrolling lists work
- [ ] Fixed-position elements work
- [ ] Correct landscape layout

## Viewport Configuration
- [ ] Viewport set correctly
- [ ] Safe area adaptation for notched screens
- [ ] Punch-hole screen adaptation
- [ ] Viewport recalculated on rotation
- [ ] Layout adjusts when the keyboard opens
- [ ] Layout restores when the keyboard closes
- [ ] Zoom restrictions take effect
- [ ] Split-screen mode adaptation

## Keyboard and Input
- [ ] Input focus works
- [ ] Smooth keyboard open animation
- [ ] Keyboard does not cover the input box
- [ ] Correct numeric / email keyboard types
- [ ] Chinese IME works
- [ ] Autocorrect works
- [ ] Show / hide password toggle
- [ ] Form autofill works
- [ ] Maximum length limit takes effect
- [ ] Input format regex validation

## H5-Specific Features
- [ ] tel: links make calls correctly
- [ ] sms: links send SMS correctly
- [ ] mailto: links open email correctly
- [ ] Map links open correctly
- [ ] Web Share API sharing works
- [ ] Add to home screen
- [ ] Splash screen displays correctly
- [ ] Full-screen mode works
- [ ] PWA offline features work
- [ ] Push notifications work

## Third-Party Login and Payment
- [ ] WeChat H5 login works
- [ ] Alipay H5 login works
- [ ] QQ H5 login works
- [ ] Weibo H5 login works
- [ ] WeChat H5 payment works
- [ ] Alipay H5 payment works
- [ ] Login state persists
- [ ] Multi-account switching works
- [ ] Authorization callback works
- [ ] Payment result query works

## WebView-Specific
- [ ] JSBridge calls work
- [ ] Camera invocation works
- [ ] Photo album invocation works
- [ ] Location invocation works
- [ ] QR scanning works
- [ ] Physical back button handled correctly
- [ ] Custom navigation bar works
- [ ] Loading progress bar displays correctly
- [ ] Error page displays correctly
- [ ] Pull to refresh works
- [ ] Sharing works
- [ ] Login state sync works

## Network and Cache
- [ ] WiFi network works
- [ ] 4G/5G network works
- [ ] Friendly prompts on weak networks
- [ ] Friendly prompts when offline
- [ ] Automatic reconnection after network recovery
- [ ] Service Worker offline cache
- [ ] LocalStorage works
- [ ] SessionStorage works
- [ ] Image lazy loading works
- [ ] Cache update strategy works

## Performance Experience
> Follow project requirements for metrics; when none exist, use these as reference values.

- [ ] First-screen load < 3 seconds
- [ ] FCP < 1.8 seconds
- [ ] LCP < 2.5 seconds
- [ ] Image compression optimized
- [ ] Code splitting takes effect
- [ ] No obvious rendering stutter
- [ ] No memory leaks
- [ ] Skeleton screen displays correctly
- [ ] CDN resources load correctly
- [ ] First-screen monitoring data is normal

## SEO and Sharing
- [ ] Complete meta tags
- [ ] Optimized page title
- [ ] Correct WeChat share card content
- [ ] Correct QQ share card content
- [ ] Correct Weibo share card content
- [ ] Complete OG tags
- [ ] Complete Twitter Card
- [ ] Correct structured data
- [ ] Share callback works
- [ ] Anti-blocking handling works
