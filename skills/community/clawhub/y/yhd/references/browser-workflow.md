# Browser Workflow Guide

## Overview

This skill supports browser automation for YHD.com (1号店) shopping with clear safety boundaries.

## Supported Operations

| Operation | Login Required | Description |
|-----------|----------------|-------------|
| Search | No | Search products with filters |
| Flash Sales | No | Browse daily rotating deals |
| View Product | No | Read specs, prices, member prices |
| Compare Prices | No | Regular vs member pricing |
| Add to Cart | Yes | Add selected item |
| View Cart | Yes | Review cart contents |
| Apply Coupons | Yes | Check 免邮券, 满减 |
| Delivery Slots | Yes | View 2-hour windows |
| Generate Order Preview | Yes | Calculate final price |
| Payment | **Never** | User only |

## Workflow Steps

### 1. Discovery (Public Pages)
```javascript
// Navigate to search or flash sales
browser.navigate("https://www.yhd.com/")
browser.click("[data-test='flash-sale-tab']")

// Extract flash sale items
snapshot.extract({
  title: ".product-name",
  regularPrice: ".regular-price",
  memberPrice: ".member-price",
  countdown: ".flash-countdown",
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
  regularPrice: ".price-regular",
  memberPrice: ".price-member",
  origin: ".origin-info",
  grade: ".quality-grade",
  reviews: ".review-item"
})
```

### 3. Cart Operations (Login Required)
```javascript
// Add to cart
browser.click(".add-to-cart-btn")

// View cart
browser.navigate("https://cart.yhd.com/")

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
  address: ".delivery-address.selected",
  deliverySlots: ".time-slot-option",
  items: ".order-item",
  coupons: ".applied-coupon",
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
| Search box | `#searchInput` |
| Search button | `.search-btn` |
| Flash sale tab | `[data-test='flash-sale']` |
| Product title | `.product-name` |
| Regular price | `.price-regular` |
| Member price | `.price-member` |
| Add to cart | `.add-cart-btn` |
| Cart icon | `.cart-icon` |
| Coupon input | `.coupon-code` |
| Delivery slot | `.time-slot` |
| Submit order | `.submit-order-btn` |

## Error Handling

| Scenario | Action |
|----------|--------|
| CAPTCHA | Hand to user |
| Login required | Ask user first |
| Flash sale sold out | Report and suggest alternatives |
| Price changed | Alert user before proceeding |
| Coupon invalid | Try alternatives or report |
| Delivery slot full | Show next available |
