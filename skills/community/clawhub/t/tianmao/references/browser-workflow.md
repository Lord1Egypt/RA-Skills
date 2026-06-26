# Browser Workflow Guide

## Overview

This skill supports browser automation for Tmall shopping with clear safety boundaries.

## Supported Operations

| Operation | Login Required | Description |
|-----------|----------------|-------------|
| Search | No | Search products with filters |
| Official Stores | No | Filter 官方旗舰店 |
| View Product | No | Read specs, prices, 88VIP prices |
| Brand Verification | No | Check authorization badges |
| Reviews | No | Read user reviews |
| Add to Cart | Yes | Add selected item |
| View Cart | Yes | Review cart contents |
| Apply Coupons | Yes | Check 店铺券, 平台券, 88VIP |
| Generate Order Preview | Yes | Calculate final price |
| Payment | **Never** | User only |

## Workflow Steps

### 1. Discovery (Public Pages)
```javascript
// Navigate to Tmall search
browser.navigate("https://www.tmall.com/")
browser.type("#mq", "化妆品")
browser.click(".tm-search-btn")

// Filter official stores
browser.click("[data-test='official-store-filter']")

// Extract results
snapshot.extract({
  title: ".product-title",
  price: ".price-current",
  storeName: ".shop-name",
  storeBadge: ".shop-badge",
  rating: ".rate-score"
})
```

### 2. Product Detail
```javascript
// Open product page
browser.navigate(productUrl)

// Extract details
snapshot.extract({
  title: ".tb-detail-h1",
  originalPrice: ".price-original",
  salePrice: ".price-sale",
  vipPrice: ".price-vip",
  storeName: ".shop-name",
  storeBadge: ".shop-badge",
  services: ".service-list",
  reviews: ".rate-item"
})
```

### 3. Cart Operations (Login Required)
```javascript
// Add to cart
browser.click(".tb-btn-addcart")

// View cart
browser.navigate("https://cart.tmall.com/")

// Extract cart info
snapshot.extract({
  items: ".cart-item",
  subtotal: ".cart-sum",
  coupons: ".coupon-available"
})
```

### 4. Order Preview (Login Required)
```javascript
// Proceed to checkout
browser.click(".cart-checkout")

// Extract order summary
snapshot.extract({
  address: ".address-selected",
  items: ".order-item",
  storeCoupon: ".coupon-store",
  platformCoupon: ".coupon-platform",
  vipDiscount: ".vip-discount",
  total: ".order-total"
})
```

## Safety Rules

1. **Always announce** before browser actions
2. **Stop at payment** - never proceed to payment
3. **Ask before login** - get explicit consent
4. **Show evidence** - snapshot key information
5. **Handoff clearly** - tell user next manual steps

## Common Selectors

| Element | Selector |
|---------|----------|
| Search box | `#mq` |
| Search button | `.tm-search-btn` |
| Official store filter | `[data-test='official-store']` |
| Product title | `.product-title` |
| Original price | `.price-original` |
| Sale price | `.price-sale` |
| 88VIP price | `.price-vip` |
| Store badge | `.shop-badge` |
| Service list | `.service-list` |
| Add to cart | `.tb-btn-addcart` |
| Cart icon | `.cart-icon` |
| Coupon input | `.coupon-input` |
| Submit order | `.order-submit` |

## Error Handling

| Scenario | Action |
|----------|--------|
| CAPTCHA | Hand to user |
| Login required | Ask user first |
| Not official store | Warn and ask confirmation |
| Price changed | Alert user before proceeding |
| Coupon invalid | Try alternatives or report |
