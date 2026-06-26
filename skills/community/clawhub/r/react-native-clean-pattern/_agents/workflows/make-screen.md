---
description: Scaffold a new MVC-Lite screen for React Native
---

# 🏗️ MVC-Lite Screen Scaffolding

Follow these steps to generate a standardized, RTL-ready screen for the Clawhub ecosystem.

## 🟢 Step 1: Definition
Ask the user for:
1.  **Screen Name**: (e.g., `Profile`, `OrderDetails`)
2.  **Parent Directory**: (Default: `src/screens/`)
3.  **Optional Modules**:
    - [ ] **Pagination**: Adding `page` state and `onEndReached` logic.
    - [ ] **Pull-to-Refresh**: Adding `isRefreshing` state and `onRefresh` logic.
    - [ ] **Search**: Local or remote filtering logic in the controller.
    - [ ] **API Integrated**: Pre-scaffolded API call in the brain.
4.  **Entry Path**: (e.g., `app/home.tsx`)

## 🟡 Step 2: Implementation (The 4-File Rule)
Create a new directory for the screen and generate these files:

### 1. `types.ts` (Structure)
- Define the `[Name]Props` interface.
- Export any local state or param types.

### 2. `styles.ts` (Nerves)
- Implement `getStyles`.
- Consume `config` (theme, isRTL, rowDirection, tokens).
- Use **centralized tokens** (e.g., `tokens.spacing.md`, `tokens.borderRadius.sm`) instead of hardcoded numbers.
- Use HSL colors from the provided `colors` object.

### 3. `controller.ts` (Brain)
- Implement `use[Name]Controller`.
- Hook into `useAppStyle`, `useAppDispatch`, `useAppSelector`.
- Return state, methods, and the `styles` object.

### 4. `index.tsx` (Skin)
- Import the controller and shared components.
- Map the controller state to the UI layout.
- Use `KeyboardAvoidingView` and `SafeAreaView` where appropriate.

## 🔵 Step 3: Route Integration
1.  Create the entry file in the `app/` directory (e.g., `app/profile.tsx`).
2.  Import and default-export the screen from its `src/screens/` location.

## 🏁 Step 4: Quality Check
- [ ] No relative imports allowed (use path aliases).
- [ ] RTL functionality tested (layout flips correctly).
- [ ] Zero `any` types in `types.ts`.
- [ ] Shared components used for all primary UI elements.
