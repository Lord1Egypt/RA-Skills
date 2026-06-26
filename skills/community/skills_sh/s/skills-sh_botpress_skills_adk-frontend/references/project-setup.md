# Frontend Project Setup

This guide walks you through setting up a React + TypeScript frontend application that connects to your ADK bot. The recommended stack is Vite, React 19, TanStack Router, TanStack Query, Zustand, and Tailwind CSS.

## Prerequisites

Before starting, ensure you have:

- **Node.js 18+** installed
- **pnpm** package manager installed (`npm install -g pnpm`)
- **Your bot deployed** to Botpress Cloud (`adk deploy`)
- **Personal Access Token (PAT)** from Botpress Cloud
  - Go to https://app.botpress.cloud
  - Navigate to Settings > Personal Access Tokens
  - Create a new token and save it securely
- **Bot and Workspace IDs** from your `agent.config.ts` file

## Step 1: Create Vite + React Project

Create a new Vite project with React and TypeScript:

```bash
# Create project
pnpm create vite@latest my-frontend -- --template react-ts

# Navigate to project
cd my-frontend

# Install base dependencies
pnpm install
```

## Step 2: Install Dependencies

### Core Dependencies

Install the essential packages:

```bash
pnpm add @botpress/client \
  @tanstack/react-query \
  @tanstack/react-router \
  zustand \
  react react-dom \
  zod
```

### UI Dependencies (Optional)

For a complete UI setup with Tailwind and Radix UI components:

```bash
pnpm add @tailwindcss/vite tailwindcss \
  @radix-ui/react-avatar @radix-ui/react-dialog \
  @radix-ui/react-dropdown-menu @radix-ui/react-icons \
  class-variance-authority clsx tailwind-merge \
  lucide-react
```

### Dev Dependencies

Install build tools and TypeScript configuration:

```bash
pnpm add -D @tanstack/router-plugin \
  @vitejs/plugin-react \
  babel-plugin-react-compiler \
  @types/node @types/react @types/react-dom \
  typescript
```

## Step 3: TypeScript Configuration

### Main TypeScript Config

Replace `tsconfig.json` with:

```json
{
  "files": [],
  "references": [{ "path": "./tsconfig.app.json" }, { "path": "./tsconfig.node.json" }]
}
```

### App TypeScript Config

Replace `tsconfig.app.json` with:

```json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "types": ["vite/client"],
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true,

    /* Path mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}
```

**Key features:**

- **Strict mode enabled** for type safety
- **Path alias `@/`** maps to `./src/` for clean imports
- **moduleResolution: bundler** for modern Vite bundling
- **React 19 JSX** with automatic runtime

## Step 4: Vite Configuration

Replace `vite.config.ts` with:

```typescript
import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tanstackRouter from '@tanstack/router-plugin/vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    // IMPORTANT: TanStack Router MUST come before React plugin
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
    }),
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler']],
      },
    }),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

**Important notes:**

- **Plugin order matters**: `@tanstack/router-plugin` must be registered before `@vitejs/plugin-react`
- **React Compiler**: Enables automatic optimizations for React 19
- **Path alias**: Enables `import { foo } from "@/lib/foo"` instead of relative paths
- **Auto code splitting**: TanStack Router automatically splits routes into separate chunks

## Step 5: Environment Variables

### Get Your Bot Configuration

Your bot's `agent.config.ts` file contains the required IDs. You can also find them in your deployed bot's dashboard.

### Create Environment File

Create `.env` in your project root:

```bash
# DO NOT COMMIT THIS FILE - Add .env to .gitignore
VITE_BOT_ID=your_bot_id
VITE_WORKSPACE_ID=your_workspace_id
```

### Create Configuration File

Create `src/config.ts`:

```typescript
export const botId = import.meta.env.VITE_BOT_ID as string
export const workspaceId = import.meta.env.VITE_WORKSPACE_ID as string

// Validate required config
if (!botId || !workspaceId) {
  throw new Error('Missing required environment variables. Please check your .env file.')
}
```

**Why a config file?**

- Centralized configuration makes it easier to update
- Type safety with TypeScript
- Runtime validation catches missing variables early
- Single source of truth for IDs across your app

## Step 6: Set Up React Query

Create `src/lib/query-client.ts`:

```typescript
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
})
```

**Configuration explained:**

- **retry: 1** - Retry failed queries once before giving up
- **staleTime: 5 minutes** - Cache data for 5 minutes before refetching
- **refetchOnWindowFocus: false** - Don't refetch when user returns to tab

## Step 7: First Connection Test

### Create a Test Service

Create `src/services/test.ts`:

```typescript
import { Client } from '@botpress/client'
import { botId, workspaceId } from '@/config'

// For testing — in production, use the client store pattern from botpress-client.md
function getTestClient(pat: string) {
  return new Client({
    apiUrl: 'https://api.botpress.cloud',
    workspaceId,
    token: pat,
    botId,
  })
}

export async function testBotConnection(pat: string) {
  const client = getTestClient(pat)

  try {
    const result = await client.callAction({
      type: 'listTables',
      input: {},
    })

    console.log('Bot connection successful!', result)
    return result
  } catch (error) {
    console.error('Bot connection failed:', error)
    throw error
  }
}
```

> **Note:** For production client management (caching, Zustand store), see [Botpress Client](./botpress-client.md). The `createAdkClient` function from `.adk/client.ts` is another option for a fully typed client.

### Update Main App

Replace `src/main.tsx` with:

```typescript
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/query-client";
import "./index.css";

function App() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Bot Connection Test</h1>
      <button
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        onClick={async () => {
          const { testBotConnection } = await import("./services/test");
          await testBotConnection("YOUR_PAT_HERE");
        }}
      >
        Test Connection
      </button>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>
);
```

### Run the Test

```bash
pnpm dev
```

Open http://localhost:5173 and click "Test Connection". Check the browser console for:

```
Bot connection successful! { output: { ... } }
```

## Step 8: Project Structure

Your project should now have this structure:

```
my-frontend/
├── src/
│   ├── config.ts                 # Bot IDs and configuration
│   ├── lib/
│   │   └── query-client.ts      # React Query config
│   ├── services/
│   │   └── test.ts              # Connection test
│   ├── main.tsx                 # App entry point
│   └── index.css                # Global styles
├── .env                         # Environment variables (DO NOT COMMIT)
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript config
├── tsconfig.app.json           # App TypeScript config
└── package.json                # Dependencies
```

## Troubleshooting

### Type Errors with Path Aliases

**Problem:** TypeScript doesn't recognize `@/` imports.

**Solution:**

1. Verify `tsconfig.app.json` has the `paths` configuration
2. Restart TypeScript server in your editor (VS Code: Cmd+Shift+P → "Restart TypeScript Server")
3. Ensure `vite.config.ts` has the matching alias configuration

### Connection Fails with 401 Unauthorized

**Problem:** API calls return 401 errors.

**Solutions:**

1. **Check your PAT is valid**: Go to https://app.botpress.cloud → Settings → Personal Access Tokens
2. **Create a new token** if needed
3. **Ensure PAT has access** to the correct workspace

### Connection Fails with CORS Error

**Problem:** Browser blocks requests with CORS policy errors.

**Solution:** This usually means:

- Your bot is not deployed (`adk deploy` first)
- Using wrong workspace/bot IDs (verify against your bot config)
- API URL is incorrect (should be `https://api.botpress.cloud`)

### TanStack Router Build Errors

**Problem:** Build fails with router-related errors.

**Solution:**

- Ensure `@tanstack/router-plugin` comes **before** `@vitejs/plugin-react` in `vite.config.ts`
- Clear build cache: `rm -rf node_modules/.vite && pnpm dev`

### React 19 Peer Dependency Warnings

**Problem:** pnpm shows peer dependency warnings for React 19.

**Solution:** This is expected during React 19's rollout. Add to `package.json`:

```json
{
  "pnpm": {
    "overrides": {
      "react": "^19.0.0",
      "react-dom": "^19.0.0"
    }
  }
}
```

### Module Not Found: Can't resolve '@/...'

**Problem:** Vite can't resolve path aliases.

**Solution:**

1. Install types for Node.js: `pnpm add -D @types/node`
2. Verify `vite.config.ts` imports `path` correctly
3. Restart dev server: `Ctrl+C` then `pnpm dev`

## Next Steps

Now that your project is set up and connected to your bot:

1. **Set up the client store**: See [Botpress Client](./botpress-client.md) for the Zustand-based client management pattern
2. **Generate types**: See [Type Generation](./type-generation.md) for end-to-end type safety
3. **Build your service layer**: See [Service Layer](./service-layer.md) for wrapping actions/tables
4. **Add authentication**: See [Authentication](./authentication.md) for PAT-based auth flow

## Production Checklist

Before deploying to production:

- [ ] Environment variables properly configured
- [ ] PAT stored securely (not in code)
- [ ] Proper authentication flow implemented
- [ ] Error handling for API calls
- [ ] Loading states for async operations
- [ ] HTTPS enabled for production domain
- [ ] Build process tested (`pnpm build`)
- [ ] Bundle size optimized

---

## See Also

- **[Botpress Client](./botpress-client.md)** - Client store pattern and usage
- **[Type Generation](./type-generation.md)** - Setting up generated types
- **[Authentication](./authentication.md)** - PAT-based auth flow
- **[Recommended Stack](./recommended-stack.md)** - Full tech stack details
