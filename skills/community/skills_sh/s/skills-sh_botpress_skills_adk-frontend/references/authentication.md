# Authentication with Botpress PATs

This guide demonstrates how to implement authentication in your ADK agent's frontend using **Personal Access Tokens (PATs)** and cookie-based storage, following production-tested patterns.

## What are Personal Access Tokens (PATs)?

Personal Access Tokens (PATs) are the primary authentication mechanism for Botpress Cloud APIs. They provide secure, user-scoped access to your workspace and bot resources.

### Generating PATs

1. Log in to [Botpress Cloud](https://app.botpress.cloud)
2. Navigate to your profile settings
3. Go to "Personal Access Tokens"
4. Click "Generate New Token"
5. Set an expiration date (optional)
6. Copy the token immediately (it won't be shown again)

### Token Scopes

PATs inherit permissions from the user who created them:

- Workspace-level operations (list bots, manage resources)
- Bot-level operations (send messages, query tables)
- User profile access via `client.getAccount()`

**Security Note:** Treat PATs like passwords. Never commit them to version control or expose them in client-side code.

## Storage Strategy: Cookies vs localStorage

This pattern uses **cookie-based storage** for PATs instead of localStorage:

### Why Cookies?

✅ **Automatic inclusion in requests** - Cookies are sent with every HTTP request
✅ **HttpOnly option** - Can be set server-side to prevent XSS attacks (if using SSR)
✅ **SameSite protection** - CSRF protection built-in
✅ **Expiration control** - Built-in expiration dates
✅ **Cross-tab synchronization** - Changes propagate across browser tabs

### Why Not localStorage?

❌ **Manual management** - Must explicitly include in API calls
❌ **No HttpOnly** - Always accessible to JavaScript (XSS risk)
❌ **No automatic expiration** - Must implement manually
❌ **Limited sync** - Changes don't propagate across tabs

### Security Considerations

```typescript
// ✅ GOOD - Secure cookie settings
document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`

// ⚠️  BETTER - Add Secure flag in production
document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax;Secure`

// 🔒 BEST - HttpOnly cookies (requires server-side rendering)
// Set via HTTP header: Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict
```

## Complete Auth Pattern

Here's a complete authentication system implementation. Let's walk through every part:

### 1. AuthContext Type Definition (Lines 8-15)

```typescript
interface AuthContextType {
  token: string | null
  isAuthenticated: boolean
  userProfile: (BaseTableRow & AgentTableRow) | null
  isLoadingProfile: boolean
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)
```

**What it provides:**

- `token` - The PAT itself
- `isAuthenticated` - Boolean flag for auth status
- `userProfile` - User data fetched from bot tables
- `isLoadingProfile` - Loading state for async profile fetch
- `login()` - Function to authenticate with a PAT
- `logout()` - Function to clear authentication

### 2. Cookie Helper Functions (Lines 22-38)

```typescript
const TOKEN_COOKIE_KEY = 'botpress_pat'

// Set cookie with 1-year expiration
function setCookie(name: string, value: string, days = 365) {
  const expires = new Date()
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000)
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`
}

// Retrieve cookie by name
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null
  }
  return null
}

// Delete cookie by setting expiration to past date
function deleteCookie(name: string) {
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`
}
```

**Key points:**

- Default 1-year expiration (PATs are long-lived)
- `SameSite=Lax` provides CSRF protection
- `path=/` makes cookie available to entire app
- Delete by setting expiration to 1970

### 3. AuthProvider Implementation (Lines 41-155)

The `AuthProvider` component manages authentication state and orchestrates the login flow. Let's break it down:

#### State Management (Lines 42-46)

```typescript
const [token, setToken] = useState<string | null>(null)
const [userProfile, setUserProfile] = useState<(BaseTableRow & AgentTableRow) | null>(null)
const [isLoading, setIsLoading] = useState(true)
const [isLoadingProfile, setIsLoadingProfile] = useState(false)
const posthog = usePostHog()
```

#### Load Token from Cookie on Mount (Lines 49-55)

```typescript
useEffect(() => {
  const storedToken = getCookie(TOKEN_COOKIE_KEY)
  if (storedToken) {
    setToken(storedToken)
  }
  setIsLoading(false)
}, [])
```

**What happens:**

1. On app startup, check for existing PAT in cookies
2. If found, restore authentication state
3. Stop showing loading spinner

#### Fetch User Profile When Token Available (Lines 58-122)

This is the most complex part - it handles profile fetching with automatic retry logic:

```typescript
useEffect(() => {
  if (!token) {
    setUserProfile(null)
    setIsLoadingProfile(false)
    return
  }

  const fetchUserProfile = async () => {
    setIsLoadingProfile(true)
    try {
      // Step 1: Get account info from Botpress API
      const client = getApiClient()
      const { account: user } = await client.getAccount({})

      if (!user.email) {
        throw new Error('User email not found in account data')
      }

      // Step 2: Fetch user profile from bot's admin table
      const result = await getMyUserProfile(user.email)
      setUserProfile(result)

      // Step 3: Clear reload flag on success
      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('auth_reload_attempted')
      }

      // Step 4: Identify user in PostHog analytics
      if (result) {
        posthog?.identify(result.id, {
          email: result.email,
          name: result.name,
        })
      }
    } catch (error) {
      console.error('Failed to fetch user profile:', error)

      // Retry logic: Reload page once on failure
      const hasReloaded = typeof window !== 'undefined' ? sessionStorage.getItem('auth_reload_attempted') : null

      if (!hasReloaded) {
        // First failure - try reloading
        console.log('Authentication failed, reloading page to reinitialize...')
        if (typeof window !== 'undefined') {
          sessionStorage.setItem('auth_reload_attempted', 'true')
          window.location.reload()
        }
      } else {
        // Second failure - logout
        console.error('Authentication failed after reload, logging out...')
        if (typeof window !== 'undefined') {
          sessionStorage.removeItem('auth_reload_attempted')
        }
        setToken(null)
        setUserProfile(null)
        deleteCookie(TOKEN_COOKIE_KEY)
      }
    } finally {
      setIsLoadingProfile(false)
    }
  }

  fetchUserProfile()
}, [token, posthog])
```

**What happens:**

1. When token changes, fetch user profile
2. First, get account info from Botpress API (`client.getAccount()`)
3. Use email to query bot's admin table for full profile
4. On success, store profile and identify user in analytics
5. On failure, attempt page reload once (handles stale client state)
6. On second failure, logout user

**Why the reload logic?**
Sometimes the Botpress client can get into a stale state. A page reload often fixes it. This pattern prevents users from getting stuck.

#### Login Function (Lines 124-127)

```typescript
const login = (newToken: string) => {
  setToken(newToken)
  setCookie(TOKEN_COOKIE_KEY, newToken)
}
```

**What happens:**

1. Update state with new token
2. Persist token to cookie
3. Triggers profile fetch via useEffect

#### Logout Function (Lines 129-134)

```typescript
const logout = () => {
  setToken(null)
  setUserProfile(null)
  deleteCookie(TOKEN_COOKIE_KEY)
  posthog?.reset()
}
```

**What happens:**

1. Clear token from state
2. Clear user profile
3. Delete cookie
4. Reset analytics session

#### Loading State (Lines 146-152)

```typescript
if (isLoading) {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
    </div>
  );
}
```

Shows a spinner while checking for stored token on mount.

### 4. useAuth Hook (Lines 161-167)

```typescript
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

Custom hook to access auth context with type safety.

### 5. getPat Export (Lines 157-159)

```typescript
export function getPat() {
  return getCookie(TOKEN_COOKIE_KEY)
}
```

Utility function to retrieve PAT from cookie outside React context.

## Fetching User Profile

The profile fetching strategy uses two data sources:

### 1. Botpress Account API

```typescript
const client = getApiClient()
const { account: user } = await client.getAccount({})
```

Returns basic account information:

- `id` - Botpress user ID
- `email` - User's email address
- `displayName` - Display name
- `emailVerified` - Whether email is verified
- `profilePicture` - Profile picture URL
- `createdAt` - Account creation date

### 2. Bot Table Query

```typescript
// From services/users.ts
export async function getMyUserProfile(email: string) {
  const client = getApiClient({ botId, workspaceId })
  const result = await client.findTableRows({
    table: 'AgentsTable',
    filter: { email },
    limit: 1,
  })
  if (!result.rows.length) {
    throw new Error(`User with email ${email} not found`)
  }
  return result.rows[0] as BaseTableRow & AgentTableRow
}
```

**What it does:**

1. Use email from account API as lookup key
2. Query bot's admin table for full profile
3. Return combined type with all user data

**Why two sources?**

- Botpress API provides authentication info
- Bot tables provide application-specific data (roles, preferences, metadata)

## Client Initialization

The API client is initialized with the PAT from cookies:

```typescript
// From stores/clientsStore.ts
import { getPat } from '../lib/auth'

const newClient = new APIClient({
  apiUrl: 'https://api.botpress.cloud',
  workspaceId: props?.workspaceId,
  token: getPat() ?? '',
  botId: props?.botId,
})
```

**Key points:**

- `token` is pulled from cookie via `getPat()`
- Client is scoped to specific workspace/bot
- Clients are cached in Zustand store by key

## Protecting Routes

This pattern uses TanStack Router's context system for route protection:

### 1. Define Router Context (router.tsx)

```typescript
interface RouterContext {
  auth?: {
    userProfile: (BaseTableRow & AgentTableRow) | null
    isAuthenticated: boolean
  }
}

export const router = createRouter({
  routeTree,
  context: {} as RouterContext,
})
```

### 2. Inject Auth Context (main.tsx)

```typescript
export function InnerApp() {
  const auth = useAuth();

  return (
    <RouterProvider
      router={router}
      context={{
        auth: {
          userProfile: auth.userProfile,
          isAuthenticated: auth.isAuthenticated
        }
      }}
    />
  );
}
```

### 3. Check Auth in Root Route (\_\_root.tsx)

```typescript
export const Route = createRootRoute({
  component: RootComponent,
  beforeLoad: ({ context }) => {
    // Pass through any existing context (like auth)
    return context;
  },
});

function RootComponent() {
  const { isAuthenticated } = useAuth();
  const routerState = useRouterState();
  const currentPath = routerState.location.pathname;
  const isAuthCallback = currentPath === "/auth/callback";

  // Allow callback route to render even when not authenticated
  if (!isAuthenticated && !isAuthCallback) {
    return <AuthScreen />;
  }

  // Auth callback route renders without sidebar
  if (isAuthCallback) {
    return <Outlet />;
  }

  // Render authenticated app with sidebar
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <Outlet />
      </SidebarInset>
    </SidebarProvider>
  );
}
```

**What happens:**

1. On every route change, check `isAuthenticated`
2. If not authenticated (and not on callback route), show auth screen
3. Auth callback route is special-cased to complete OAuth flow
4. Authenticated users see full app with sidebar

### 4. Route-Level Protection (Optional)

Individual routes can access auth context:

```typescript
export const Route = createFileRoute('/admin')({
  beforeLoad: ({ context }) => {
    if (!context.auth?.userProfile?.isAdmin) {
      throw redirect({ to: '/inbox' })
    }
  },
  component: AdminComponent,
})
```

## Login Flow

This pattern uses Botpress's OAuth-style CLI login flow:

### 1. Auth Screen (components/auth-screen.tsx)

```typescript
export function AuthScreen() {
  const handleAuthenticate = () => {
    // Redirect to Botpress auth with callback to our app
    const callbackUrl = `${window.location.origin}/auth/callback`;
    const authUrl = `https://app.botpress.cloud/cli-login?redirect=${encodeURIComponent(callbackUrl)}`;

    window.location.href = authUrl;
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 text-center">
        <h1 className="text-3xl font-bold">Welcome</h1>
        <p className="text-muted-foreground">Authenticate with Botpress to continue</p>
        <Button onClick={handleAuthenticate} size="lg" className="w-full">
          <LogIn className="mr-2 h-4 w-4" />
          Authenticate with Botpress
        </Button>
      </div>
    </div>
  );
}
```

### 2. OAuth Callback Route (routes/auth.callback.tsx)

```typescript
interface AuthCallbackSearch {
  pat?: string;
  token?: string;
}

export const Route = createFileRoute("/auth/callback")({
  component: AuthCallbackComponent,
  validateSearch: (search: Record<string, unknown>): AuthCallbackSearch => {
    return {
      pat: (search.pat as string) || undefined,
      token: (search.token as string) || undefined,
    };
  },
});

function AuthCallbackComponent() {
  const { login } = useAuth();
  const { pat, token } = Route.useSearch();

  useEffect(() => {
    const receivedToken = pat || token;

    if (receivedToken) {
      login(receivedToken);
    }
  }, [pat, token, login]);

  // Redirect to inbox after login
  return <Navigate to="/inbox" search={{ filter: "my-inbox", unread: false }} />;
}
```

### Complete Flow Diagram

```
User clicks "Authenticate"
  ↓
Redirect to https://app.botpress.cloud/cli-login?redirect=...
  ↓
User logs in / authorizes
  ↓
Botpress redirects back: /auth/callback?pat=bp_pat_...
  ↓
Callback route extracts PAT from URL params
  ↓
Call login(receivedToken)
  ↓
AuthProvider stores PAT in cookie + state
  ↓
useEffect triggers profile fetch
  ↓
Navigate to /inbox
  ↓
User is authenticated!
```

**Security notes:**

- PAT is passed in URL query parameter (brief exposure)
- Immediately stored in cookie and removed from URL via navigation
- Cookie has `SameSite=Lax` protection
- Consider using POST request to callback endpoint for extra security

## Logout Flow

```typescript
const { logout } = useAuth()

const handleLogout = () => {
  logout()
  // User is automatically redirected to AuthScreen by RootComponent
}
```

**What happens:**

1. Call `logout()` from auth context
2. Token cleared from state
3. Profile cleared from state
4. Cookie deleted
5. Analytics session reset
6. Root component detects `!isAuthenticated` and shows AuthScreen

## Integration with PostHog (Optional)

You can include optional PostHog analytics integration:

### 1. Wrap App with PostHogProvider (main.tsx)

```typescript
import { PostHogProvider } from "posthog-js/react";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <PostHogProvider
      apiKey={posthogApiKey}
      options={{
        api_host: posthogApiHost,
        defaults: "2025-05-24",
        capture_exceptions: true,
        debug: false,
      }}
    >
      <AuthProvider>
        <App />
      </AuthProvider>
    </PostHogProvider>
  </StrictMode>
);
```

### 2. Identify User After Login (auth.tsx)

```typescript
// Inside fetchUserProfile() success block
if (result) {
  posthog?.identify(result.id, {
    email: result.email,
    name: result.name,
  })
}
```

### 3. Reset on Logout (auth.tsx)

```typescript
const logout = () => {
  setToken(null)
  setUserProfile(null)
  deleteCookie(TOKEN_COOKIE_KEY)
  posthog?.reset() // Clear user identity
}
```

### 4. Track Events Throughout App

```typescript
import { usePostHog } from "posthog-js/react";

function MyComponent() {
  const posthog = usePostHog();

  const handleAction = () => {
    posthog?.capture("action_performed", {
      actionType: "send_message",
      ticketId: "123"
    });
  };

  return <button onClick={handleAction}>Send</button>;
}
```

## Best Practices

### 1. Secure Cookie Settings

```typescript
// Development
document.cookie = `token=${value};path=/;SameSite=Lax`

// Production (HTTPS only)
document.cookie = `token=${value};path=/;SameSite=Strict;Secure`
```

**Key settings:**

- `Secure` - Only send over HTTPS (production)
- `SameSite=Strict` - Strongest CSRF protection (may break OAuth flows)
- `SameSite=Lax` - Balance of security and compatibility (recommended)
- `HttpOnly` - Prevents JavaScript access (requires server-side implementation)

### 2. PAT Rotation Strategy

```typescript
// Check token expiration on app load
useEffect(() => {
  if (token) {
    const checkTokenValidity = async () => {
      try {
        await client.getAccount({})
      } catch (error) {
        // Token invalid/expired - logout
        logout()
      }
    }
    checkTokenValidity()
  }
}, [])
```

### 3. Error Handling

```typescript
try {
  const result = await client.findTableRows({...});
} catch (error) {
  if (error.code === 401 || error.code === 403) {
    // Token expired or invalid
    logout();
    throw new Error("Session expired. Please log in again.");
  }
  throw error;
}
```

### 4. Loading States

```typescript
const { isLoadingProfile, isAuthenticated } = useAuth();

if (!isAuthenticated) {
  return <AuthScreen />;
}

if (isLoadingProfile) {
  return <LoadingSpinner />;
}

return <App />;
```

Always show loading states during async operations to prevent UI flashing.

### 5. Environment Variables

```typescript
// ❌ NEVER commit PATs
const DEFAULT_TOKEN = 'bp_pat_abc123...' // WRONG!

// ✅ Use environment variables
const DEFAULT_TOKEN = import.meta.env.VITE_BOTPRESS_PAT

// ⚠️  Even better - no defaults, force user to authenticate
// Don't provide any default token in production
```

## Security Considerations

### 1. HTTPS in Production

**Always use HTTPS** when handling PATs. HTTP transmits tokens in plain text.

```typescript
// Enforce HTTPS in production
if (import.meta.env.PROD && window.location.protocol !== 'https:') {
  window.location.href = window.location.href.replace('http:', 'https:')
}
```

### 2. Token Expiration Handling

Implement automatic logout when tokens expire:

```typescript
// Wrap API calls with error handling (Client has no event emitter)
async function safeApiCall<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn()
  } catch (error: any) {
    if (error.status === 401) {
      logout()
      window.location.href = '/'
    }
    throw error
  }
}
```

### 3. Never Log PATs

```typescript
// ❌ WRONG
console.log('User token:', token)

// ✅ CORRECT
console.log('User authenticated:', !!token)
```

### 4. CORS Configuration

Ensure your API allows requests from your frontend domain:

```typescript
// Backend CORS configuration
app.use(
  cors({
    origin: process.env.ALLOWED_ORIGINS.split(','),
    credentials: true, // Required for cookies
  })
)
```

### 5. Rate Limiting

Implement rate limiting on authentication endpoints:

```typescript
// Example with express-rate-limit
import rateLimit from 'express-rate-limit'

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
})

app.post('/auth/login', authLimiter, handleLogin)
```

### 6. Session Timeout

Implement automatic logout after inactivity:

```typescript
let inactivityTimer: NodeJS.Timeout

const resetInactivityTimer = () => {
  clearTimeout(inactivityTimer)
  inactivityTimer = setTimeout(
    () => {
      logout()
      alert('Session expired due to inactivity')
    },
    30 * 60 * 1000
  ) // 30 minutes
}

// Reset timer on user activity
useEffect(() => {
  window.addEventListener('mousemove', resetInactivityTimer)
  window.addEventListener('keypress', resetInactivityTimer)

  return () => {
    window.removeEventListener('mousemove', resetInactivityTimer)
    window.removeEventListener('keypress', resetInactivityTimer)
    clearTimeout(inactivityTimer)
  }
}, [])
```

## Complete Implementation Checklist

- [ ] **Cookie helpers** - setCookie, getCookie, deleteCookie functions
- [ ] **AuthContext** - Define interface with token, profile, login, logout
- [ ] **AuthProvider** - Implement with useState, useEffect for token persistence
- [ ] **Load from cookie** - Check for existing PAT on mount
- [ ] **Fetch profile** - Query Botpress API and bot tables on token change
- [ ] **Retry logic** - Handle transient failures with reload strategy
- [ ] **Login function** - Store token in state + cookie
- [ ] **Logout function** - Clear token, profile, cookie
- [ ] **useAuth hook** - Export custom hook with type safety
- [ ] **Client initialization** - Pass PAT to Botpress client
- [ ] **Router context** - Inject auth into TanStack Router
- [ ] **Route protection** - Check isAuthenticated in root route
- [ ] **Auth screen** - UI for unauthenticated users
- [ ] **OAuth callback** - Handle PAT from URL params
- [ ] **Loading states** - Show spinners during async operations
- [ ] **Error handling** - Handle expired tokens, network errors
- [ ] **Analytics** - Integrate PostHog (optional)
- [ ] **Security** - HTTPS, Secure cookies, no logging of tokens
- [ ] **Production config** - Environment variables, rate limiting

## Related Documentation

- [Frontend Project Setup](./project-setup.md) - Initial React + Vite setup
- [Botpress Client](./botpress-client.md) - Using @botpress/client API
- [Data Fetching](./data-fetching.md) - TanStack Query patterns
- [State Management](./state-management.md) - Zustand for global state
- [Tables](../tables.md) - Querying bot tables for user data

## Reference Implementation

**Recommended file structure:**

- Auth provider: `packages/frontend/src/lib/auth.tsx`
- Client store: `packages/frontend/src/stores/clientsStore.ts`
- User services: `packages/frontend/src/services/users.ts`
- Router setup: `packages/frontend/src/router.tsx`
- Root route: `packages/frontend/src/routes/__root.tsx`
- Auth screen: `packages/frontend/src/components/auth-screen.tsx`
- Callback route: `packages/frontend/src/routes/auth.callback.tsx`
- Main entry: `packages/frontend/src/main.tsx`
