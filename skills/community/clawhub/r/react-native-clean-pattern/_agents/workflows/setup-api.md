---
description: Setup production-grade API Client and Logger in a React Native project
---

// turbo-all
# 🌐 API & Logging Setup

Follow these steps to implement the standardized `ApiClient` and `Logger` with terminal/Sentry integration.

## 🟢 Step 1: Dependencies
Ensure the project has the following dependencies:
```bash
npm install axios i18next @sentry/react-native @react-native-async-storage/async-storage
```

## 🟡 Step 2: Implementation (The Standard Structure)

### 1. `src/helpers/logger.ts` (Unified Observability)
Create a logger that handles:
- **Redaction**: Sanitizing sensitive keys (`password`, `token`, `otp`).
- **Terminal (DEV)**: Rich formatting with icons and request durations.
- **Sentry (PROD)**: Automatic breadcrumbs and exception capturing.

### 2. `src/services/apiClient.ts` (The Engine)
Implement a singleton class supporting `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.
- **Headers**: Dynamic `Accept-Language` and `Authorization` bearer token.
- **Payloads**: Seamless support for `JSON` and `FormData`.
- **Advanced Features**:
    - **Pagination Helper**: Logic to handle `total`, `per_page`, and `current_page` keys.
    - **Retry Logic**: Configurable retries for network failures.
    - **Multipart Safety**: Automatic `Content-Type` elision for FormData.
- **Integrated Logging**: Every request/response/error must trigger the corresponding `logger` method.
- **Error Handling**: Flatten validation errors from the backend into a readable message.

## 🔵 Step 3: Registration
1.  Verify the base URL is defined in `src/config/index.ts`.
2.  Ensure `TokenStorage` (or `AsyncStorage`) is accessible for the bearer token.

## 🏁 Step 4: Verification
- [ ] Run a test GET request and check the console for the 🌐 icon.
- [ ] Verify that sensitive fields are marked as `***` in the logs.
- [ ] Trigger a fake error and verify it shows up in Sentry (if configured).
