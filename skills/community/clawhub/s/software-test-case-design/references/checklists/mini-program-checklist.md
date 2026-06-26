# Mini-Program Testing Checklist

## Lifecycle (10 items)
- [ ] Cold start
- [ ] Warm start
- [ ] Page onLoad
- [ ] Page onShow
- [ ] Page onReady
- [ ] Page onHide
- [ ] Page onUnload
- [ ] Switch to background
- [ ] Return to foreground
- [ ] Destruction after extended background

## Authorization Management (12 items)
- [ ] User info authorization
- [ ] Phone number authorization
- [ ] Location authorization
- [ ] Camera authorization
- [ ] Photo library authorization
- [ ] Bluetooth authorization
- [ ] Recording authorization
- [ ] Authorization granted
- [ ] Authorization denied
- [ ] Re-prompt after denial
- [ ] Enable permission via settings page
- [ ] Authorization state persistence

## Sharing Functionality (14 items)
- [ ] Share via top-right menu
- [ ] Share via share button
- [ ] Share title
- [ ] Share description
- [ ] Share cover image
- [ ] Share path
- [ ] Share to friend
- [ ] Share to group chat
- [ ] Share to Moments
- [ ] Share success callback
- [ ] Share failure handling
- [ ] Open from share card
- [ ] Share parameter passing
- [ ] Share opens specified page

## Platform Difference Adaptation (10 items)
- [ ] WeChat Mini-Program API
- [ ] Alipay Mini-Program API
- [ ] Baidu Mini-Program API
- [ ] Douyin Mini-Program API
- [ ] Component compatibility
- [ ] Style compatibility
- [ ] Login differences
- [ ] Payment differences
- [ ] Sharing differences
- [ ] Review guideline differences

## Subscription & Template Messages (8 items)
- [ ] Subscription message authorization
- [ ] Subscription message sending
- [ ] Subscription message open
- [ ] Template message sending
- [ ] Template message open
- [ ] Subscription count limit
- [ ] Subscription permission revocation
- [ ] Message push settings

## Mini-Program Navigation (10 items)
- [ ] Navigate to another mini-program
- [ ] Navigate with parameters
- [ ] Return from another mini-program
- [ ] web-view opens H5
- [ ] H5 navigates to mini-program
- [ ] Open mini-program from App
- [ ] Open App from mini-program
- [ ] Navigation count limit
- [ ] Half-screen mini-program
- [ ] Inter-mini-program navigation

## Local Storage (8 items)
- [ ] Storage write
- [ ] Storage read
- [ ] Storage clear
- [ ] Capacity limit
- [ ] Cache update
- [ ] Cache cleanup
- [ ] Temporary file storage
- [ ] File system management

## Map & Location (8 items)
- [ ] Map component loading
- [ ] Multi-marker rendering performance
- [ ] Region zoom smoothness
- [ ] Location accuracy (GPS/WiFi/cell tower)
- [ ] Degradation after location permission denial
- [ ] Nearby POI search accuracy
- [ ] Map layer (traffic/satellite) switching
- [ ] Background location restrictions

## Payment Functionality (8 items)
- [ ] WeChat Pay
- [ ] Alipay
- [ ] Payment callback
- [ ] Payment success page
- [ ] Payment failure handling
- [ ] Order status synchronization
- [ ] Refund flow
- [ ] Payment security

