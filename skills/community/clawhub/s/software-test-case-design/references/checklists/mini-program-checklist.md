# Mini Program Testing Checklist

> The sections of this checklist correspond one-to-one with `references/platform/mini-program.md` and are used for item-by-item self-checking after test case design.

## Lifecycle
- [ ] Cold start
- [ ] Hot start
- [ ] Page onLoad
- [ ] Page onShow
- [ ] Page onReady
- [ ] Page onHide
- [ ] Page onUnload
- [ ] Switching to the background
- [ ] Returning to the foreground
- [ ] Destroyed after a long time in the background

## Authorization Management
- [ ] Privacy protection guidelines pop-up is triggered
- [ ] Agreeing to the privacy protection guidelines
- [ ] Rejecting the privacy protection guidelines
- [ ] Undeclared privacy APIs cannot be called
- [ ] Avatar and nickname filling
- [ ] Phone number authorization
- [ ] Location authorization
- [ ] Camera authorization
- [ ] Photo album authorization
- [ ] Bluetooth authorization
- [ ] Recording authorization
- [ ] Authorization granted
- [ ] Authorization denied
- [ ] Re-guidance after denial
- [ ] Enabling permissions on the settings page
- [ ] Authorization state persistence

## Sharing
- [ ] Sharing from the top-right menu
- [ ] Sharing via a share button
- [ ] Share title
- [ ] Share description
- [ ] Share cover image
- [ ] Share path
- [ ] Sharing to a friend
- [ ] Sharing to a group chat
- [ ] Sharing to Moments
- [ ] Share success callback
- [ ] Share failure handling
- [ ] Opening from a share card
- [ ] Share parameter passing
- [ ] Share opens the specified page

## Payment
- [ ] WeChat Pay
- [ ] Alipay
- [ ] Payment callback
- [ ] Payment success page
- [ ] Payment failure handling
- [ ] Order status sync
- [ ] Refund flow
- [ ] Payment security

## Mini Program Navigation
- [ ] Navigating to other mini programs
- [ ] Navigating with parameters
- [ ] Returning from another mini program
- [ ] Opening H5 via web-view
- [ ] H5 navigating to the mini program
- [ ] Opening the mini program from an app
- [ ] Opening an app from the mini program
- [ ] Navigation count limits
- [ ] Half-screen mini programs
- [ ] Mutual navigation between mini programs

## Subscription Messages
- [ ] Subscription message authorization
- [ ] Distinguishing one-time and long-term subscriptions
- [ ] Long-term subscriptions limited to specific categories
- [ ] Sending subscription messages
- [ ] Opening subscription messages
- [ ] Subscription count limits
- [ ] Revoking subscription permission
- [ ] Message push settings

## Storage and Cache
- [ ] Storage write
- [ ] Storage read
- [ ] Storage clear
- [ ] Capacity limit
- [ ] Cache update
- [ ] Cache cleanup
- [ ] Temporary file storage
- [ ] File system management

## Maps and Location
- [ ] Map component loading
- [ ] Rendering performance with many markers
- [ ] Zoom smoothness
- [ ] Location accuracy (GPS / WiFi / cell tower)
- [ ] Degradation after location permission is denied
- [ ] Nearby POI search accuracy
- [ ] Map layer (traffic / satellite) switching
- [ ] Background location restrictions

## Platform Difference Adaptation
- [ ] WeChat Mini Program APIs
- [ ] Alipay Mini Program APIs
- [ ] Baidu Smart Program APIs
- [ ] Douyin Mini Program APIs
- [ ] Component compatibility
- [ ] Style compatibility
- [ ] Login differences
- [ ] Payment differences
- [ ] Sharing differences
- [ ] Review guideline differences
