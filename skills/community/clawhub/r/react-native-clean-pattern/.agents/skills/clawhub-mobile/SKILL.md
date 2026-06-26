---
name: clawhub-mobile
description: Clawhub master skill for Expo/React Native. Production-grade patterns: MVC-Lite, RTL-First, Centralized Hook Styles, Zero-Any TS, and Sentry-Integrated Logging.
---

# 📱 Clawhub React Native (Expo) Master Skill

A unified, intelligent guide for building and maintaining high-performance mobile applications within the **Clawhub** ecosystem.

## 📥 Installation

### 1. Register the Skill:
Add this directory to your agent's skill path.

### 2. Environment Setup:
Ensure you have the following global dependencies installed:
```bash
npm install -g expo-cli eas-cli react-native-clean-pattern
```
OR

```bash
bun clawdhub install react-native-clean-pattern
```

## ⌨️ Usage

### To start a new project:
```bash
/provision-app
```

### To scaffold a new feature/screen:
```bash
/make-screen
```

### To scaffold a new component:
```bash
/make-component
```

### To setup API or Navigation infrastructure:
```bash
/setup-api
/setup-navigation
```

---

## 🚀 §0 — Execution & Workflow Standards

Follow these steps for any task in the Clawhub ecosystem:

1.  **STRATEGIZE**: Identify if the task is **Provisioning** (New App), **Expansion** (New Screen/Feature), or **Diagnosis** (Bug Fix).
2.  **AUDIT & CLEAN**: Before adding new code, check for **Duplicated Files** or redundant logic. Reuse existing `@shared` components or `@hooks`.
3.  **SCAFFOLD**: If expanding, always create the 4-file MVC-Lite structure.
4.  **STYLING**: Initialize `getStyles` using the `useAppStyle()` hook for RTL-compliance. Use HSL tokens from `@styles/common`.
5.  **INTEGRATE**: Connect UI logic to `controller.ts`, utilizing `@hooks/useRedux` and `@services/apiClient`.
6.  **SECURE & OPTIMIZE**: Ensure `mountedRef` is used in all async controllers to prevent **Memory Leaks**.
7.  **VERIFY**: Run `npx tsc --noEmit` and check RTL/LTR UI toggle.

---

## 🏗️ §1 — Project Architecture & Path Aliases

Standardized, strictly typed, and RTL-ready folder architecture. All files must be interconnected via aliases.

```text
.
├── app/                         # Expo Router (routes & layouts)
├── screens/                     # Feature-specific implementations (MVC-Lite)
├── components/                  # Distributed Atom/Molecule components
│   ├── [RegularComponent]/      # Regular/Feature components (e.g., DynamicIsland)
│   └── SharedComponent/         # Global blessed component library (@shared)
├── services/                    # Infrastructure (API, Auth, Firebase, Storage)
├── store/                       # State Management (Redux Power Slices)
├── hooks/                       # Custom logical hooks (@hooks)
├── helpers/                     # Shared pure logic & utilities (@helpers)
├── enums/                       # Global Constants & Types (@enums)
├── styles/                      # Design Token System (@styles)
├── i18n/                        # Localization assets (@i18n)
└── assets/                      # Media & Fonts (@assets)
```

### ⭐ Path Alias Enforcement
Never use relative paths (`../../`). Always use:
`@shared`, `@services`, `@hooks`, `@store`, `@helpers`, `@config`, `@styles`, `@enums`.

---

## §1.1 — Standardized Enums (`@enums`)

Use these enums to ensure zero `string-literal` errors across the app.

| Enum | Key Values |
|:---|:---|
| `AuthScreen` | `LOGIN`, `REGISTER`, `FORGOT_PASSWORD`, `OTP_VERIFY` |
| `ValidationRule` | `REQUIRED`, `EMAIL`, `MIN_LENGTH`, `MATCH` |
| `UserType` | `USER`, `VENDOR`, `ADMIN`, `DELIVERY_BOY` |
| `TokenKey` | `ACCESS_TOKEN`, `REFRESH_TOKEN`, `FCM_TOKEN` |

---

## §1.2 — Core Application Hooks (`@hooks`)

| Hook | Responsibility |
|:---|:---|
| `useAppDispatch` / `useAppSelector` | Strictly typed Redux access. |
| `useRTL` | Manages `I18nManager` force-flipping and app reloads. |
| `useAppStyle` | Dynamic UI pipe that merges base themes with remote config, resolves RTL directionality (rowDirection, textAlign), and provides centralized design tokens and localized font resolution. |
| `useAppConfig` | Reactive access to merged Local/Remote Config. |
| `useColorScheme` | Reactive system theme detection (Light/Dark mode). |
| `useNotifications` | Orchestrates FCM registration, Notifee channel management, and real-time state rehydration (Profile/Theme) upon receipt of push payloads. |

---

## 📦 §2 — Core Modules (The Gold Standards)

### 2.1 Configuration System (`@config`)
Environment-driven, strictly typed central config:
- **Environment**: Mapped to `.env` variables via `process.env`.
- **Typing**: Governed by the `AppConfig` interface.
- **Safety**: Includes fallbacks and platform-specific logic.

### 2.2 API Client (`@services/apiClient`)
Singleton wrapper with:
- **Auth**: Automatic Bearer token injection.
- **I18n**: Reactive `Accept-Language` headers.
- **Payloads**: Native support for `JSON` and `FormData`.
- **Logging**: Detailed request/response tracing with duration.

### 2.3 Auth Service (`@services/authService`)
Orchestrator for Login, Register, OTP, and Profile management with:
- **Multi-Method Support**: Native handling for `EMAIL_PASSWORD`, `EMAIL_OTP`, and `PHONE_OTP`.
- **UserType Injection**: Context-aware management of delivery, vendor, or customer states.
- **Redux Integration**: Synchronized state for OTP sending status and active auth methods.

### 2.4 Firebase Service (`@services/firebaseService`)
Platform-aware initialization for Expo Go and Development Builds.

### 2.5 Notification Service (`@services/notificationService`)
Management of paginated alert listing and "read" state synchronization.

### 2.6 Security Storage (`@services/tokenStorage`)
Encrypted or AsyncStorage persistence for tokens and user metadata.

### 2.7 Consolidated Logging (`@helpers/logger`)
Sensitized logging system with:
- **Redaction**: Automatic sanitization of sensitive fields (`password`, `token`, `authorization`, `otp`).
- **Tracing**: Structured `request()`, `response()`, and `error()` tracing with latency tracking.
- **Observability**: Seamless Sentry integration via `addBreadcrumb` and `captureException`.
- **Environment Aware**: Debug-only rich formatting (`__DEV__`) with terminal icons (🌐, ✅, ❌, 🔴, ℹ️, ⚠️).

### 2.8 Localization (`@i18n`)
RTL-First standard with:
- **Engine**: `i18next` with `compatibilityJSON: 'v3'` for React Native safe pluralization.
- **Persistence**: Mandatory `AsyncStorage` usage to remember language selection across reloads.
- **Hypdration**: `initializeI18n()` async boot sequence required in `_layout.tsx`.
- **RTL**: `I18nManager` force-flip with `expo-updates` reload (try/catch protected).
- **State Sync**: Must use a callback pattern for Redux synchronization; NEVER import `store` directly into the i18n instance.
- **Reload**: Integration with `expo-updates` for mandatory UI rehydration on direction change.
- **Sync**: `setupRTL()` boot helper to maintain state consistency.

### 2.9 Redux Toolkit Power Slices (`@store`)
Strictly typed state management with:
- **Hooks**: Mandatory use of `useAppDispatch` and `useAppSelector` for type-safe state access.
- **Pillars**: Auth (Session/User/AuthMethod), App (Theme/Language/RTL), and Notification (Alerts) slices.

---

## 🧩 §3 — Standard Component Library (@shared)

| Component | Purpose | Key Props |
|:---|:---|:---|
| `AppText` | Typography with RTL font scaling. | `variant`, `weight`, `align` |
| `Button` | Themed touchable with loading states. | `title`, `loading`, `icon`, `variant` |
| `AppHeader` | RTL-aware screen header with back/actions. | `title`, `showBackButton`, `rightComp` |
| `AppInput` | Validated text input with icons. | `label`, `error`, `icon`, `secure` |
| `PriceTag` | Currency-aware formatted price display. | `price`, `originalPrice`, `discount` |
| `AppLoader` | Lottie-powered full-screen or inline loading. | `visible`, `variant`, `message` |
| `AppModal` | Standardized bottom-sheet or center popup. | `visible`, `onClose`, `title` |

---

## 🛠️ §4 — Standard Feature Modules

Implemented as isolated folders under `screens/` following MVC-Lite:
1.  **Auth Flow**: Sign In, Sign Up, OTP, Password Recovery.
2.  **Catalog**: Product List (FlashList optimized), Category Browse.
3.  **Cart & Checkout**: Multi-step checkout, Order Summary, Payments.
4.  **Profile**: User Details, Address Management, Order History.

---

## 📚 §5 — Approved Dependency Matrix

*   **Core**: `expo@~55.0.5`, `react@19.2.0`, `react-native@0.83.2`.
*   **Navigation**: `@react-navigation/native`, `@react-navigation/native-stack`, `@react-navigation/bottom-tabs`. 
    *   **Standards**: Dynamic configuration-driven Bottom Tabs and Auth/Guest gating with Navigator-level `key` remounting.
*   **State & Logic**: `@reduxjs/toolkit@^2.11.2`, `react-redux@^9.2.0`.
*   **Networking & Auth**: `@react-native-firebase/app`, `@react-native-firebase/messaging`.
*   **Persistence**: `@react-native-async-storage/async-storage@^2.2.0`.
*   **Internationalization**: `i18next@^25.8.16`, `react-i18next@^16.5.6`, `expo-localization`.
*   **UI & Visuals**: `lottie-react-native@~7.3.4`, `react-native-reanimated@4.2.1`, `react-native-render-html`.
*   **Maps & Location**: `react-native-maps`, `react-native-maps-directions`, `expo-location`.
*   **Typography**: `@expo-google-fonts/cairo`, `@expo-google-fonts/outfit`, `@expo-google-fonts/roboto`.
*   **Observability**: `@sentry/react-native@~7.11.0`.
*   **Native Features**: `@notifee/react-native`, `expo-image-picker`, `expo-document-picker`.

---

## 🧱 §6 — Expansion Pattern (MVC-Lite)

Every new screen, feature, OR shared component MUST consist of exactly 4 files:

1.  **`index.tsx` (Skin)**: Pure JSX. Connects to `controller.ts`.
2.  **`controller.ts` (Brain)**: logic hook, utilizes `@hooks/useRedux`.
3.  **`styles.ts` (Nerves)**: Function-based styles consuming `useAppStyle`.
4.  **`types.ts` (Structure)**: Interface definitions. Zero `any`.

---

## 🛡️ §7 — Defensive Coding & Security

*   **Memory Safety**: Always use `isMounted` ref in controllers. Abort all API calls in `useEffect` cleanup.
*   **Zero Duplication**: Shared logic must stay in `@hooks` or `@helpers`. Don't copy-paste styles; use `@styles/common`. **Hard Requirement**: All sizes, spacing, and colors must be consumed via `useAppStyle().tokens` and `useAppStyle().colors`.
*   **Zero Hardcoding**: Using literal hex codes (`#FFFFFF`) or RGBA strings in UI components is FORBIDDEN. All UI colors must be resolved from the `colors` object provided by the central styling hook.
*   **Zero Inline Styles**: Using the `style={{ ... }}` prop in JSX is FORBIDDEN for layout and presentation. All styles MUST be defined in the accompanying `styles.ts` file and resolve via the screen/component controller to ensure theme and RTL reactivity.
*   **Branding Sync**: Primary theme colors MUST be defined in `src/config/index.ts` and consumed via `@constants/Colors.ts` to support white-labeling and remote branding.
*   **RTL Enforcement**: Use `rowDirection` and `textAlign` from `useAppStyle`.
*   **Sanitization**: Never log raw bodies containing `password` or `token`.
*   **Absolute Paths**: All imports MUST use standardized aliases. Relative paths (`../../`) are forbidden. 
    *   **Standard Aliases**: `@/`, `@components`, `@hooks`, `@constants`, `@store`, `@i18n`, `@assets`, `@config`, `@app-types`, `@enums`, `@utils`, `@helpers`, `@services`, `@screens`, `@styles`.

---

## ✅ §8 — Verification Checklist

1.  [ ] `npx tsc --noEmit` passes with zero errors.
2.  [ ] i18n RTL/LTR layout flip verified.
3.  [ ] No hardcoded colors/spacing outside of `@styles/common`.
4.  [ ] No relative paths found in imports.
5.  [ ] Async logic verified for `mountedRef` safety.

---

## 🏗️ §9 — Provisioning Guide (Training)

When starting a **NEW** application, you must follow this interactive training flow to ensure architectural integrity without merely copy-pasting old classes.

### 1. The Inquiry Phase
You **MUST** ask the user for authorization to implement:
- **Project Identity**: Targeted app name and bundle identifier.
- **Localization**: RTL support needs and target languages (LTR: EN, ES, FR, etc. | RTL: AR, HE, FA, etc.).
- **Core Screens**: 
    - `app/_layout.tsx`: Master orchestrator (Sentry, Redux, RTL, Hydration).
    - `app/(auth)`: Auth flow group (Login, Register, OTP).
    - `app/(tabs)`: Main application navigation.
- **Core Auth**: Login, Register, OTP, and Forgot Password recovery screens.
- **State Architecture**: Redux Toolkit (Auth/App/Notify slices).
- **Native Bridges**: Firebase Messaging and Notifee.
- **Observation Layer**: Sentry integration and Custom Logger.
- **Persistence**: Encrypted Token Storage.

### 2. The Structural Blueprint
Instead of copying files, generate fresh implementations based on these patterns:
- **Auth (MVC-Lite)**: Each screen (`Login`, `Register`, `OTP`) gets its own `Skin`, `Brain`, `Nerves`, and `Structure`.
- **Services**: Freshly authored `apiClient.ts` and `authService.ts`.
- **Global Store**: A clean Redux initialization with strictly typed slices.

### 3. The Activation Loop
1.  **Initialize**: Generate the `package.json`, `tsconfig.json`, and `app.json`.
2.  **Install**: Run `npm install` or `bun install` to pull the **Approved Dependency Matrix**.
3.  **Environment**: Create the `.env` file from the `.env.example` template.
4.  **Launch**: Execute `npx expo start` to verify the baseline.

## ⌨️ §10 — Workflow & Slash Command Reference

Use these commands to automate common development tasks within the Clawhub ecosystem:

| Command | Purpose | When to Use |
| :--- | :--- | :--- |
| `/provision-app` | **Initialize Project** | Starting a new app from scratch. |
| `/setup-api` | **API & Observability** | Adding a production-grade `apiClient.ts` and `logger.ts`. |
| `/setup-navigation` | **Router Setup** | Scaffolding Root (Auth) and Main (Dynamic Tab) navigators. |
| `/make-screen` | **Feature Scaffolding** | Creating a new screen using the 4-file MVC-Lite pattern. |
| `/make-component` | **UI Scaffolding** | Creating a new **Shared**, **Regular**, or **Local** component. |

---

## 🔗 Author & Links

- **GitHub**: [yahongie2014](https://github.com/yahongie2014)
- **Website**: [coder79.me](https://coder79.me)
