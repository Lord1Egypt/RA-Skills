---
description: Scaffold a new shared component for React Native
---

// turbo-all
# 🧩 Component Scaffolding

Follow these steps to generate a standardized, reusable component for the `@shared` library.

## 🟢 Step 1: Definition
Ask the user for:
1.  **Component Type**:
    - **Shared**: (Target: `src/components/SharedComponent/`) - Global, "blessed" components, usually prefixed with `App`.
    - **Regular**: (Target: `src/components/`) - Feature-specific or general application components.
    - **Local**: (Target: `src/screens/[ScreenName]/local-components/`) - Bound to specific features.
2.  **Component Name**: (e.g., `AppCard`, `Tag`, `Banner`)
3.  **Complexity**: Is it a simple UI atom or a complex molecule with its own controller?

## 🟡 Step 2: Implementation (The Standard Structure)
Create a new directory in the **Target Directory** and generate:

### 1. `types.ts` (Structure)
- Define the `[Name]Props` interface.
- **Mandatory Prop Standards**: Every shared component MUST support these if applicable:
    - `containerStyle?: ViewStyle`: For external layout positioning.
    - `style?: TextStyle | ViewStyle`: For overriding internal element styles.
    - `disabled?: boolean`: To handle interaction states.
    - `testID?: string`: For automated testing identification.
    - `children?: React.ReactNode`: If the component acts as a wrapper.
- Ensure all style props are optional and correctly typed using absolute path aliases.

### 2. `styles.ts` (Nerves)
- Implement `getStyles` consuming `colors`, `tokens`, and RTL config.
- Use **centralized spacing and radius tokens** instead of hardcoded values.

### 3. `index.tsx` (The Component)
- Wrap the component in `React.memo` for performance.
- Use `useAppStyle` to resolve colors and styles if needed.
- Merge user-provided `style` and `containerStyle` props correctly.

### 4. `controller.ts` (Brain)
- Standard requirement for all Clawhub components. 
- Defines the `use[Name]Controller` hook providing styles and interaction logic to the UI skin.

## 🔵 Step 3: Registration
1.  **If Shared**, add the new component to `src/components/SharedComponent/index.ts`.
2.  **If Regular**, add to `src/components/index.ts`.
3.  **Ensure it is exported** with a clear, prefixed name if it is shared (e.g., `AppButton`).

## 🏁 Step 4: Quality Check
- [ ] Component is memoized (`React.memo`).
- [ ] Props allow for style overrides.
- [ ] RTL/LTR directionality is respected.
- [ ] Accessibility props (`accessibilityLabel`, etc.) are included where appropriate.
