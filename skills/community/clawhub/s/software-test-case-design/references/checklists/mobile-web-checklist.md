# Mobile Web Testing Checklist

## Browser Compatibility (12 items)
- [ ] iOS Safari latest version works correctly
- [ ] iOS Safari mainstream version compatible
- [ ] Android Chrome works correctly
- [ ] Android Chrome mainstream version compatible
- [ ] WeChat built-in browser works correctly
- [ ] QQ Browser works correctly
- [ ] UC Browser works correctly
- [ ] Quark Browser works correctly
- [ ] Samsung Internet works correctly
- [ ] Private/Incognito mode works correctly
- [ ] WebView (WKWebView/Android) compatible
- [ ] JavaScript feature compatibility

## Touch Interaction (14 items)
- [ ] Single tap responds correctly
- [ ] Double-tap zoom functionality
- [ ] Long-press triggers context menu
- [ ] Left-right swipe to switch
- [ ] Up-down swipe to scroll
- [ ] Pinch-to-zoom functionality
- [ ] Pull-to-refresh functionality
- [ ] Pull-up to load more
- [ ] Tap state visual feedback
- [ ] Touch disable setting takes effect
- [ ] Nested scrolling has no conflicts
- [ ] Rubber band effect works correctly
- [ ] Inertial scrolling is smooth
- [ ] Gesture conflict handling is correct

## Responsive Layout (12 items)
- [ ] 320px width works correctly
- [ ] 375px width works correctly
- [ ] 414px width works correctly
- [ ] 768px (iPad) width works correctly
- [ ] Tall screen (19.5:9) adaptation
- [ ] Notch screen content is not obstructed
- [ ] Media query breakpoints are correct
- [ ] Image widths are responsive
- [ ] Font sizes adapt correctly
- [ ] Horizontal scrolling lists work correctly
- [ ] Fixed-position elements work correctly
- [ ] Landscape layout is correct

## Viewport Configuration (8 items)
- [ ] viewport setting is correct
- [ ] Notch screen safe area adaptation
- [ ] Punch-hole screen adaptation
- [ ] Viewport recalculation on screen rotation
- [ ] Keyboard popup layout adjustment
- [ ] Keyboard dismissal layout restoration
- [ ] Zoom restriction takes effect
- [ ] Split-screen mode adaptation

## Keyboard & Input (10 items)
- [ ] Input field focus works correctly
- [ ] Keyboard popup animation is smooth
- [ ] Keyboard does not obscure input fields
- [ ] Number/email keyboard types are correct
- [ ] Chinese input method works correctly
- [ ] Auto-correction works correctly
- [ ] Password show/hide toggle works
- [ ] Form autofill works correctly
- [ ] Maximum length restriction takes effect
- [ ] Input format regex validation

## H5-Specific Features (10 items)
- [ ] tel: link dials phone correctly
- [ ] sms: link sends SMS correctly
- [ ] mailto: link opens email correctly
- [ ] Map links open correctly
- [ ] Web Share API sharing works correctly
- [ ] Add to Home Screen functionality
- [ ] Splash screen displays correctly
- [ ] Fullscreen mode works correctly
- [ ] PWA offline functionality works correctly
- [ ] Notification push functionality works correctly

## Third-Party Login & Payment (10 items)
- [ ] WeChat H5 login works correctly
- [ ] Alipay H5 login works correctly
- [ ] QQ H5 login works correctly
- [ ] Weibo H5 login works correctly
- [ ] WeChat H5 payment works correctly
- [ ] Alipay H5 payment works correctly
- [ ] Login state persistence works correctly
- [ ] Multi-account switching works correctly
- [ ] Authorization callback works correctly
- [ ] Payment result query works correctly

## WebView-Specific (12 items)
- [ ] JSBridge calls work correctly
- [ ] Camera invocation works correctly
- [ ] Photo library invocation works correctly
- [ ] Location invocation works correctly
- [ ] QR code scanning works correctly
- [ ] Physical back button handling is correct
- [ ] Navigation bar customization works correctly
- [ ] Loading progress bar displays correctly
- [ ] Error page displays correctly
- [ ] Pull-to-refresh works correctly
- [ ] Sharing functionality works correctly
- [ ] Login state synchronization works correctly

## Network & Cache (10 items)
- [ ] WiFi network works correctly
- [ ] 4G/5G network works correctly
- [ ] Weak network environment has friendly prompts
- [ ] Offline prompts are friendly
- [ ] Auto-reconnect on network recovery
- [ ] Service Worker offline caching
- [ ] LocalStorage works correctly
- [ ] SessionStorage works correctly
- [ ] Image lazy loading works correctly
- [ ] Cache update strategy works correctly

## Performance Optimization (10 items)
- [ ] First-screen load < 3 seconds
- [ ] FCP time < 1.8 seconds
- [ ] LCP time < 2.5 seconds
- [ ] Image compression optimization
- [ ] Code splitting takes effect
- [ ] No noticeable rendering stutter
- [ ] No memory leaks
- [ ] Skeleton screen displays correctly
- [ ] CDN resource loading works correctly
- [ ] First-screen monitoring data is correct

## SEO & Sharing (10 items)
- [ ] Meta tags are complete
- [ ] Page title optimization
- [ ] WeChat share card content is correct
- [ ] QQ share card content is correct
- [ ] Weibo share card content is correct
- [ ] OG tags are complete
- [ ] Twitter Cards are complete
- [ ] Structured data is correct
- [ ] Share callback works correctly
- [ ] Anti-blocking handling works correctly
