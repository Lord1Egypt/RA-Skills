---
description: Start a new React Native app with Auth and optional modules
---

// turbo-all
# 🚀 Provisioning a New React Native App

Follow these steps to initialize a production-ready React Native app from scratch using the Clawhub standard.

## 🟢 Step 1: Requirements Gathering
Before writing code, ask the user the following questions to tailor the setup:

1.  **Project Identity**:
    *   **App Name**: What is the name of the new application?
    *   **Bundle Identifier**: (e.g., `com.company.appname`)

2.  **Localization & RTL**:
    *   **RTL Support**: Does the app require Right-to-Left (RTL) support?
    *   **Languages**: Which languages are needed?
        *   **LTR Options**: English, Spanish, French, Chinese, Hindi, Russian, Portuguese, etc.
        *   **RTL Options**: Arabic, Hebrew, Persian (Farsi), Urdu, Pashto, Sindhi.

3.  **Core Screens**: 
    *   **Splash Screen**: Mandatory boot logic (fonts, remote config).
    *   **Intro/Onboarding**: Does the app need Intro screens?
    *   **Auth Flow**: Confirm which screens are needed: `Login`, `Register`, `OTP`, `Forgot Password`.

4.  **Optional Modules**: Ask which of these should be implemented:
    *   **Firebase**: For Cloud Messaging/Notifications?
    *   **Redux Toolkit**: For global state management (Auth, App, Notifications)?
    *   **Sentry**: For error tracking and crash reporting?
    *   **Token Storage**: Secure persistence (Encrypted)?
    *   **Custom Logger**: Structured logging with environment sensitivity?

## 🟡 Step 2: Project Configuration
1.  **Path Aliases**: Update `tsconfig.json` and `babel.config.js` with the mandatory `@/*` mappings:
    - `@/`: root of `./src`
    - `@components`, `@hooks`, `@constants`, `@store`, `@i18n`, `@assets`, `@config`, `@app-types`, `@enums`, `@utils`, `@helpers`, `@services`, `@screens`, `@styles`.
2.  **Babel Plugins**: Ensure `module-resolver` and `react-native-reanimated/plugin` are correctly configured.
3.  **Metro Config**: Standardize `metro.config.js` to handle asset resolution and symlinks.

## 🟡 Step 3: Foundation (Folder Structure)
Create the core directory structure to support the Clawhub pattern:
- `app/`: Expo Router config.
- `src/`: Core logic.
  - `components/Shared/`: Atomic UI components.
  - `screens/Auth/`: MVC-Lite screens.
  - `store/`: Redux configuration.
  - `services/`: API, Auth, and Storage services.
  - `enums/`: Centralized constants.
  - `helpers/`: Utility functions (Logger, etc.).
  - `styles/`: Theme and tokens.

## 🔵 Step 4: Implementation Strategy (MVC-Lite)
For each Auth screen (Login, Register, OTP), create the 4-file structure:
1.  `index.tsx`: UI layout using `@shared` components.
2.  `controller.ts`: Screen logic (validation, API calls).
3.  `styles.ts`: Screen-specific styles using `useAppStyle`.
4.  `types.ts`: Interface definitions for the screen.

## 🟠 Step 5: Module Setup (Based on User Choice)
- **API Client**: Implement `src/services/apiClient.ts` as a singleton class featuring:
    - Automatic `Authorization` token injection from storage.
    - `Accept-Language` header synchronization with `i18next`.
    - Structured logging for requests, responses (with duration), and errors.
    - Support for both `JSON` and `FormData` (multipart) payloads.
    - Standardized error parsing to flatten backend validation objects.
- **Auth Service**: Singleton wrapper for `apiClient` mapping to authorization endpoints (login, register, otp) with `UserType` injection logic.
- **Firebase Service**: Safe initialization logic that handles **Expo Go vs Native** environment differences and dynamic config loading.
- **Notification Service**: Centralized handling for fetching paginated notifications and managing "read" states via the API.
- **Token Storage**: Persistence layer using `AsyncStorage` (or `SecureStore`) for tokens and user metadata, driven by `@config` keys.
- **Config System**: Centralize all environment-specific and sensitive data in `src/config/index.ts`:
    - Use `process.env` for API URLs, Firebase keys, and Sentry DSN.
    - Implement a strictly typed `AppConfig` interface covering API, Auth, Theme, Firebase, and Sentry.
    - Provide a local `.env.example` template for development set up.
- **Localization (i18n)**: Implement `src/i18n/index.ts` featuring:
    - `i18next` initialization with `compatibilityJSON: 'v3'` and **AsyncStorage persistence** to remember user choice across reloads.
    - `initializeI18n()` async boot function to restore language before UI mounting.
    - Reactive resource management and `setupRTL()` logic for boot-time state synchronization.
    - **Security**: Avoid importing the Redux `store` directly into `i18n/index.ts` to prevent circular dependencies; use a callback pattern for state synchronization.
    - Integration with `expo-updates` (try/catch protected) for mandatory app reloads on RTL/LTR toggles.
- **Styling Hook**: Implement `src/hooks/useAppStyle.ts` as the central UI pipe:
    - **Remote Sync**: Merge base theme colors with reactive `remoteConfig` overrides from Redux.
    - **Directional UI**: Compute RTL-aware helpers (`rowDirection`, `textAlign`, `startAlign`, `left/right`).
    - **Font Resolution**: Dynamic font family mapping based on language (e.g., Arabic vs English) and weight tokens.
    - **Design Tokens**: Expose the centralized `Tokens` object (spacing, radius, shadows) to all consuming components.
- **Theme Hook**: Implement `src/hooks/use-color-scheme.ts` to provide reactive system theme detection (Light/Dark).
- **Redux**: Initialize the store with `authSlice`, `appSlice`, and `notificationSlice`:
    - Implement `src/hooks/useRedux.ts` providing strictly typed `useAppDispatch` and `useAppSelector` wrappers.
    - Ensure all state access across the app uses these typed hooks to maintain "Zero-Any" compliance.
- **Notifications Hook**: Implement `src/hooks/useNotifications.ts` with:
    - **Expo Safety**: Dynamic `require` and environment checks to prevent crashes in Expo Go.
    - **Token Sync**: Automatic FCM token registration and refresh handling tied to the Auth state.
    - **Display**: Integration with `@notifee/react-native` for high-importance local display and channel management.
    - **Live Refresh**: Ability to trigger Redux actions (Profile/Notifications/RemoteConfig) upon message receipt.
    - **RTL/Theme Sync**: Detection of background theme updates via the `APP_THEME_UPDATE` payload type.
- **Logger/Sentry**: Implement `src/helpers/logger.ts` for unified observability:
    - **Security**: Mandatory `sanitize` logic to redact `tokens`, `passwords`, and `otp` from logs.
    - **Observability**: Structured `request()`, `response()`, and `error()` methods.
    - **Sentry Integration**: Automatic `Sentry.addBreadcrumb` for every request/response and `captureException` for errors.
    - **Environment Aware**: Rich console formatting (icons, durations) enabled only in `__DEV__` mode.

- **Root Layout (`app/_layout.tsx`)**: Implement the master orchestrator using:
    - **Wrappers**: `Sentry.wrap`, Redux `Provider`, and `SafeAreaProvider`.
    - **Resource Loading**: Standardized `useFonts` logic with `SplashScreen.preventAutoHideAsync`.
    - **System Boot**: Mandatory call to `setupRTL()` and service activation via `useNotifications()`.
    - **State Hydration**: Parallel dispatch of `restoreAppConfig`, `restoreSession`, and `fetchRemoteConfig`.
    - **Stack Definition**: Clean stack grouping for `(auth)`, `(tabs)`, and feature modals.
- **Route Index (`app/index.tsx`)**: Implement smart redirection logic to either `/intro` (new users) or `/(tabs)` (returning users).

## 🏁 Step 6: Verification
1.  Ensure all path aliases are configured in `tsconfig.json` and `babel.config.js`.
2.  Verify the screen navigation flow: `Register` -> `OTP` -> `Login` -> `Home`.
3.  Check that sensitive data (passwords/tokens) is never logged raw.
4.  Confirm that NO hardcoded hex/rgba codes are present in any component or screen (must use `colors.primary`, etc.).
5.  Confirm that NO inline styles (`style={{...}}`) are present in the JSX skin files; all layout and presentation logic must reside in `styles.ts`.
