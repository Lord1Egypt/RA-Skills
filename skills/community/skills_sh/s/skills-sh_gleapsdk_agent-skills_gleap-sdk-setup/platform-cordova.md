# Cordova SDK

## Installation

```
cordova plugin add cordova-plugin-gleap
```

Works for both Android and iOS.

## Initialization

In your `deviceready` handler:

```javascript
document.addEventListener('deviceready', function () {
    cordova.plugins.GleapPlugin.initialize("API_KEY");
}, false);
```

## Common API Usage

The Cordova SDK exposes methods via `cordova.plugins.GleapPlugin`.

### Identify Users

```javascript
cordova.plugins.GleapPlugin.identify("USER_ID", {
  name: "Franz",
  email: "franz@example.com",
  plan: "Pro plan",
  companyName: "ACME inc.",
  customData: {
    role: "admin",
  },
});
```

Clear identity on logout:
```javascript
cordova.plugins.GleapPlugin.clearIdentity();
```

### Track Events

```javascript
cordova.plugins.GleapPlugin.trackEvent("User signed in");

// With data:
cordova.plugins.GleapPlugin.trackEvent("Purchase completed", {
  amount: 49.99,
  currency: "USD",
});
```

### Custom Data

```javascript
cordova.plugins.GleapPlugin.attachCustomData({ environment: "staging" });
cordova.plugins.GleapPlugin.setCustomData("key", "value");
cordova.plugins.GleapPlugin.removeCustomData("key");
cordova.plugins.GleapPlugin.clearCustomData();
```

### Widget Control

```javascript
cordova.plugins.GleapPlugin.open();
cordova.plugins.GleapPlugin.close();
```
