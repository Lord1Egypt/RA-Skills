# State Management with Zustand

This guide covers client-side state management in ADK frontend projects using Zustand, focused on ADK-specific patterns.

## When to Use Zustand vs TanStack Query

Understanding when to use each tool is critical for maintainable architecture:

**Use Zustand for:**

- **Global app state**: UI preferences, theme settings
- **Application logic state**: File uploads, form wizards, multi-step flows
- **Client-side only data**: User preferences, UI state that doesn't sync to server
- **Singleton management**: Botpress client instances, configuration

**Use TanStack Query for:**

- **Server state**: Data from bot actions, tables, knowledge bases
- **API responses**: Fetching, caching, and synchronizing server data
- **Background updates**: Automatic refetching, invalidation, polling
- **Request state**: Loading, error, and success states for API calls

**Clear separation of concerns:**

```typescript
// Zustand for client management
const client = useClientsStore((state) => state.getAPIClient())

// TanStack Query for server data
const { data } = useQuery({
  queryKey: ['tickets'],
  queryFn: () => listTickets({ state: 'open' }),
})
```

> **Note:** For the Botpress client store pattern (creating, caching, and managing client instances), see [Botpress Client](./botpress-client.md).

---

## Composer File Store Example (Real-World ADK Pattern)

This is a concrete example of Zustand managing file upload state — the kind of complex client-side logic that **should not** live in TanStack Query:

```typescript
import { create } from 'zustand'

const MAX_FILES = 10

export type FileType = 'image' | 'video' | 'audio' | 'file'

export type FileItem = {
  name: string
  type: FileType
  url?: string
  instance: File
  status: 'loading' | 'error' | 'uploaded'
}

type ComposerFileStore = {
  files: FileItem[]
  setFiles: (files: FileItem[]) => void
  upsertFile: (file: FileItem) => void
  deleteFile: (filename: string) => void
  addFile: (file: File, uploadFn?: (file: File) => Promise<string>) => void
}

export const useComposerFileStore = create<ComposerFileStore>((set, get) => ({
  files: [],

  setFiles: (files) => set({ files }),

  upsertFile: (incomingFile) =>
    set(({ files }) => {
      const fileExists = files.some((f) => f.name === incomingFile.name)
      const filesArr = fileExists
        ? files.map((file) => (file.name === incomingFile.name ? { ...file, ...incomingFile } : file))
        : [...files, { ...incomingFile }]
      return { files: filesArr }
    }),

  addFile: async (file, uploadFn) => {
    const hasReachedMaxFiles = get().files.length >= MAX_FILES
    if (hasReachedMaxFiles) return

    const fileName = file.name

    // Determine file type based on MIME type
    let fileType: FileType = 'file'
    if (file.type.startsWith('image/')) fileType = 'image'
    else if (file.type.startsWith('video/')) fileType = 'video'
    else if (file.type.startsWith('audio/')) fileType = 'audio'

    if (fileType === 'image' && uploadFn) {
      const previewUrl = URL.createObjectURL(file)

      // Add file with loading status
      get().upsertFile({
        name: fileName,
        type: fileType,
        url: previewUrl,
        instance: file,
        status: 'loading',
      })

      try {
        const uploadedUrl = await uploadFn(file)
        get().upsertFile({
          name: fileName,
          type: fileType,
          url: uploadedUrl,
          instance: file,
          status: 'uploaded',
        })
        URL.revokeObjectURL(previewUrl)
      } catch (error) {
        console.error('Failed to upload image:', error)
        get().upsertFile({
          name: fileName,
          type: fileType,
          url: previewUrl,
          instance: file,
          status: 'error',
        })
      }
    } else {
      const url = URL.createObjectURL(file)
      get().upsertFile({
        name: fileName,
        type: fileType,
        url,
        instance: file,
        status: 'uploaded',
      })
    }
  },

  deleteFile: (filename) =>
    set(({ files }) => {
      const file = files.find((f) => f.name === filename)
      if (file?.url) URL.revokeObjectURL(file.url)
      return { files: files.filter((file) => file.name !== filename) }
    }),
}))
```

**Key ADK patterns demonstrated:**

- **Optimistic UI**: Shows preview immediately, uploads in background
- **Status tracking**: loading → uploaded/error states
- **Resource cleanup**: Revokes object URLs to prevent memory leaks
- **Async actions**: Handles file uploads within store actions
- **Upsert pattern**: Updates existing files or adds new ones
- **Validation**: Enforces MAX_FILES limit

---

## Using Stores in Components

### Selecting Specific State Slices

```typescript
// Only re-renders when files array changes
function FileList() {
  const files = useComposerFileStore((state) => state.files);
  return <ul>{files.map(/* ... */)}</ul>;
}

// Only re-renders when specific derived value changes
function UploadedFileCount() {
  const uploadedCount = useComposerFileStore((state) =>
    state.files.filter((f) => f.status === "uploaded").length
  );
  return <span>{uploadedCount} uploaded</span>;
}
```

### Multiple Values with Shallow

```typescript
import { shallow } from 'zustand/shallow'

function FileUploader() {
  const { files, addFile, deleteFile } = useComposerFileStore(
    (state) => ({
      files: state.files,
      addFile: state.addFile,
      deleteFile: state.deleteFile,
    }),
    shallow
  )
  // ...
}
```

### Accessing Store Outside React

```typescript
export const getComposerFiles = () => useComposerFileStore.getState().files

// Use in non-React code
function handleExternalEvent() {
  const currentFiles = getComposerFiles()
  console.log('Current files:', currentFiles)
}
```

---

## Persist State When Needed

For persisting state to localStorage:

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type PreferencesStore = {
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void
}

export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'user-preferences', // localStorage key
    }
  )
)
```

---

## Best Practices

### 1. Keep Stores Focused

```typescript
// Good — focused stores
const useAuthStore = create(...);  // Auth state only
const useUIStore = create(...);    // UI preferences only
const useFileStore = create(...);  // File management only

// Bad — kitchen sink store
const useAppStore = create(...);   // Everything mixed together
```

### 2. Use Selectors for Derived State

```typescript
// Good — compute in selector
const hasFiles = useComposerFileStore((state) => state.files.length > 0)

// Bad — compute in render
const files = useComposerFileStore((state) => state.files)
const hasFiles = files.length > 0 // Re-computes on every render
```

### 3. Separate Concerns (Server vs App State)

```typescript
// Good — clear separation
const client = useClientsStore((state) => state.getAPIClient());
const { data: tickets } = useQuery({
  queryKey: ["tickets"],
  queryFn: () => listTickets({ state: "open" }),
});

// Bad — mixing server state in Zustand
const useTicketsStore = create((set) => ({
  tickets: [],
  fetchTickets: async () => {
    const data = await client.findTableRows({...});
    set({ tickets: data });
  },
}));
```

### 4. Clean Up Resources

```typescript
deleteFile: (filename) =>
  set(({ files }) => {
    const file = files.find((f) => f.name === filename);
    if (file?.url) URL.revokeObjectURL(file.url);
    return { files: files.filter((f) => f.name !== filename) };
  }),
```

---

## When NOT to Use Zustand

### Server Data — Use TanStack Query

```typescript
// Wrong — don't manage server data in Zustand
const useMessagesStore = create((set) => ({
  messages: [],
  loading: false,
  fetchMessages: async () => {
    set({ loading: true });
    const data = await client.findTableRows({...});
    set({ messages: data, loading: false });
  },
}));

// Correct — use TanStack Query
const { data: messages, isLoading } = useQuery({
  queryKey: ["messages", ticketId],
  queryFn: () => listMessages(ticketId),
});
```

### Form State — Use Local useState or React Hook Form

```typescript
// Correct — use local state for forms
function ContactForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  return (
    <form>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
    </form>
  );
}
```

### Temporary UI State — Use useState

```typescript
// Correct — use local state for component-scoped UI
function MyComponent() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsModalOpen(true)}>Open</button>
      <Modal open={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </>
  );
}
```

---

## Summary

**Use Zustand for:**

- Client instance management (see [Botpress Client](./botpress-client.md))
- Global app state (theme, preferences, user settings)
- Complex UI state that needs to be shared (file uploads, multi-step wizards)

**Don't use Zustand for:**

- Server state (use TanStack Query)
- Form state (use useState or React Hook Form)
- Temporary component state (use useState)
- Data that should be fetched from APIs (use TanStack Query)

**Remember:** Zustand is for **application state**, TanStack Query is for **server state**. Keep them separate.

---

## See Also

- **[Botpress Client](./botpress-client.md)** — Client store pattern with Zustand
- **[Data Fetching](./data-fetching.md)** — TanStack Query for server state
- **[Real-Time Updates](./realtime-updates.md)** — Polling and optimistic patterns
- **[Calling Actions](./calling-actions.md)** — Using mutations with actions
- **[Overview](./overview.md)** — Architecture context
