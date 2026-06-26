---
name: React
detect:
  files: ["src/App.tsx", "src/App.jsx", "src/App.js"]
  dependencies: ["react", "react-dom", "react-native", "@react-native-community"]
  keywords: ["React", "React Native"]
---

## attack-surface-frontend

**`dangerouslySetInnerHTML` Audit:**
1. Grep for every instance of `dangerouslySetInnerHTML` in the codebase
   - For EACH instance: trace the `__html` value to its source — is it user-controlled or from external data?
   - Is the HTML sanitized before injection? (e.g., DOMPurify, sanitize-html)
   - Can an attacker influence the HTML content through any upstream data source?

**JSX Auto-Escaping Bypass Patterns:**
2. JSX auto-escapes string values in `{}` expressions, but these patterns bypass it:
   - Passing raw HTML strings through `dangerouslySetInnerHTML` (obvious)
   - Creating React elements with `React.createElement()` where props come from user input
   - Using `ref` callbacks that manipulate DOM directly: `ref={(el) => el.innerHTML = userData}`
   - Template literals in `style` attributes: `style={{background: `url(${userInput})`}}` (CSS injection)
   - `href` attributes with `javascript:` protocol: `<a href={userInput}>` where input is `javascript:alert(1)`

**React Context Sensitive Data Leaks:**
3. Are there React contexts that store sensitive data? (Grep for `createContext`, `useContext`)
   - Can a nested component access context data it shouldn't see?
   - Is sensitive data (tokens, PII, encryption keys) stored in context that's accessible to third-party components?
   - Are context values logged or serialized in error boundaries?

**`useEffect` and Data Fetching Races:**
4. Are there `useEffect` hooks that fetch data without cleanup/abort controllers?
   - Can a race condition between rapid component mounts/unmounts cause stale or wrong data to be displayed?
   - If fetch results update auth state, can a race cause an auth bypass? (stale token displayed after logout)

**Third-Party Component XSS:**
5. Are there third-party React components that render user-controlled data?
   - Rich text editors (Quill, TipTap, Slate): do they sanitize output?
   - Markdown renderers (react-markdown, marked): are they configured to disallow raw HTML?
   - Data table/grid components: do they render cell content as HTML?
   - Chart libraries: can label/tooltip content include unsanitized HTML?

**State Management Security:**
6. If using Redux, Zustand, MobX, or similar:
   - Is sensitive data (tokens, keys) stored in global state that appears in browser dev tools?
   - Are Redux DevTools disabled in production? (Grep for `__REDUX_DEVTOOLS_EXTENSION__`, `devtools` middleware)
   - Can browser extensions read/modify the global state?

**Error Boundary Information Leaks:**
7. Do error boundaries (`componentDidCatch`, `ErrorBoundary`) expose stack traces or internal data in production?
   - Are error details sent to client-visible UI or only to logging services?
   - Can a crafted input trigger an error that reveals internal component structure?
