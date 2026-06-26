---
description: Setup production-grade Root and dynamic Main (Tab) Navigators
---

// turbo-all
# 🗺️ Navigation Setup (Root & Main)

Follow these steps to implement a reactive, configuration-driven navigation system with Auth/Verified/Guest gating.

## 🟢 Step 1: Definition
Verify the requirements:
1.  **Auth Gating**: Does the app require a different stack for authenticated vs. guest users?
2.  **Verification Flow**: Does the app have a multi-step user verification process (e.g., OTP, Profile completion)?
3.  **Dynamic Tabs**: Should the bottom tab bar be driven by the central `Config`?

## 🟡 Step 2: Optimization (Centralization)

### 1. `src/hooks/useAppStyle.ts` (Global Config)
Centralize common navigation options to ensure project-wide consistency and perfect RTL handling.
```typescript
const navigationOptions = {
    headerShown: false,
    contentStyle: { backgroundColor: colors.background },
    animation: isRTL ? 'slide_from_left' : 'slide_from_right' as any,
};
```

## 🟡 Step 3: Implementation (Root Navigator)

### 1. `src/navigation/RootNavigator.tsx` (The Gatekeeper)
Implement the `RootNavigator` stack using the centralized logic:
- **Centralized Options**: Consuming `navigationOptions` from `useAppStyle`.
- **Key-Based Remounting**: Use `key={isAuthenticated ? 'authed' : 'guest'}` on the navigator to clear state during transitions.

## 🟡 Step 4: Implementation (Main Navigator)

### 1. `src/navigation/MainNavigator.tsx` (Dynamic Tabs)
Implement the `MainNavigator` (usually a BottomTabNavigator):
- **Config Driven**: Map `config.navigation.bottomTabs` items to screen components.
- **Custom Tab Bar**: Integrate a `CustomTabBar` component for premium aesthetics.
- **Togglability**: Allow disabling the tab bar via `config.features.enableBottomNavbar`.

## 🔵 Step 5: Component Support

### 1. `src/components/CustomTabBar/`
Ensure a premium, animated tab bar is implemented using:
- **Reanimated**: For smooth active-tab indicator transitions.
- **Config Labels**: Fetching localized labels and icons from the central config.
- **Icon Mapping**: Converting generic icon names from the backend/config to `Ionicons` or `AppImage` sources.

## 🏁 Step 6: Verification
- [ ] Log out and verify the navigator resets correctly to the `Login` screen.
- [ ] Toggle a tab in `Config.ts` and verify it appears/disappears dynamically.
- [ ] Check RTL transitions for correct slide direction.
