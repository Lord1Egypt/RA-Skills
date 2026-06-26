# Browser Workflow Guide

## Overview

This skill supports browser automation for Vipshop (唯品会) shopping with clear safety boundaries.

## Supported Operations

| Operation | Login Required | Description |
|-----------|----------------|-------------|
| Search | No | Search products with filters |
| Flash Sales | No | Browse 限时特卖, 品牌特卖 |
| View Product | No | Read specs, prices, VIP prices |
| Inventory Check | No | Check size/color availability |
| Add to Cart | Yes | Add selected item |
| View Cart | Yes | Review cart contents |
| Apply Coupons | Yes | Check 优惠券, 超级VIP discounts |
| Generate Order Preview | Yes | Calculate final price |
| Payment | **Never** | User only |

## Workflow Steps

### 1. Discovery (Public Pages)
```javascript
// Navigate to Vipshop
browser.navigate("https://www.vip.com/")

// Go to flash sales
browser.click("[data-test='flash-sale']")

// Extract deals
snapshot.extract({
  title: ".product-name",
  brand: ".brand-name",
  originalPrice: ".price-original",
  salePrice: ".price-sale",
  vipPrice: ".price-vip",
  discount: ".discount-badge",
  stock: ".stock-indicator"
})
```

### 2. Product Detail
```javascript
// Open product page
browser.navigate(productUrl)

// Extract details
snapshot.extract({
  title: ".product-title",
  brand: ".brand-info",
  originalPrice: ".price-original",
  salePrice: ".price-sale",
  vipPrice: ".price-vip",
  sizes: ".size-options",
  colors: ".color-options",
  stockStatus: ".stock-status",
  saleCountdown: ".flash-countdown"
})
```

### 3. Cart Operations (Login Required)
```javascript
// Add to cart
browser.click(".add-cart-btn")

// View cart
browser.navigate("https://cart.vip.com/")

// Extract cart info
snapshot.extract({
  items: ".cart-item",
  subtotal: ".cart-subtotal",
  coupons: ".available-coupon"
})
```

### 4. Order Preview (Login Required)
```javascript
// Proceed to checkout
browser.click(".checkout-btn")

// Extract order summary
snapshot.extract({
  address: ".delivery-address",
  items: ".order-item",
  vipDiscount: ".vip-discount",
  couponDiscount: ".coupon-discount",
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
| Search box | `#J_search_input` |
| Search button | `.search-btn` |
| Flash sale tab | `[data-test='flash-sale']` |
| Product title | `.product-name` |
| Brand name | `.brand-name` |
| Original price | `.price-original` |
| Sale price | `.price-sale` |
| VIP price | `.price-vip` |
| Size options | `.size-options` |
| Color options | `.color-options` |
| Stock status | `.stock-status` |
| Add to cart | `.add-cart-btn` |
| Cart icon | `.cart-icon` |
| Coupon input | `.coupon-input` |
| Submit order | `.submit-order-btn` |

## Error Handling

| Scenario | Action |
|----------|--------|
| CAPTCHA | Hand to user |
| Login required | Ask user first |
| Out of stock | Report and suggest alternatives |
| Size unavailable | Check other sizes or items |
| Flash sale ended | Show current deals |
| Price changed | Alert user before proceeding |
| Coupon invalid | Try alternatives or report |
