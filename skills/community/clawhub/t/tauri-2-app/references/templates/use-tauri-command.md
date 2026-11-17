# `src/hooks/useTauriCommand.ts`

Generic hook that wraps `invoke()` with `data` / `isLoading` / `error` / `execute`. Every per-domain hook (`useSettings`, `useRecording`, …) composes this. **Components never call `invoke()` directly.**

```ts
import { invoke } from "@tauri-apps/api/core";
import { useCallback, useEffect, useState } from "react";
import { isTauriReady } from "../tauriReady";

export interface UseCommandOptions<T> {
  command: string;
  args?: Record<string, unknown>;
  onSuccess?: (data: T) => void;
  onError?: (error: string) => void;
}

export interface CommandState<T> {
  data: T | null;
  isLoading: boolean;
  error: string | null;
  execute: (args?: Record<string, unknown>) => Promise<T>;
}

export function useTauriCommand<T = unknown>(
  options: UseCommandOptions<T>,
): CommandState<T> {
  const { command, args: defaultArgs, onSuccess, onError } = options;
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (args?: Record<string, unknown>) => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await invoke<T>(command, args || defaultArgs);
        setData(result);
        onSuccess?.(result);
        return result;
      } catch (err) {
        const errorMsg = String(err);
        setError(errorMsg);
        onError?.(errorMsg);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [command, defaultArgs, onSuccess, onError],
  );

  return { data, isLoading, error, execute };
}

export interface UseLoadOptions<T> extends UseCommandOptions<T> {
  loadOnMount?: boolean;
  defaultValue?: T;
}

export interface LoadState<T> {
  data: T;
  isLoading: boolean;
  error: string | null;
  execute: (args?: Record<string, unknown>) => Promise<T>;
  reload: () => Promise<T>;
}

export function useTauriLoad<T = unknown>(
  options: UseLoadOptions<T>,
): LoadState<T> {
  const { loadOnMount = true, defaultValue, ...commandOptions } = options;
  const { data, isLoading, error, execute } = useTauriCommand<T>(commandOptions);

  const reload = useCallback(() => execute(), [execute]);

  useEffect(() => {
    if (!loadOnMount) return;
    if (!isTauriReady()) return;
    execute().catch(() => {
      /* error already captured */
    });
  }, [loadOnMount, execute]);

  return {
    data: (data ?? defaultValue) as T,
    isLoading,
    error,
    execute,
    reload,
  };
}

export interface UseMutationOptions<T> extends UseCommandOptions<T> {
  onMutate?: () => void | Promise<void>;
}

export interface MutationState<T> {
  isMutating: boolean;
  error: string | null;
  execute: (args?: Record<string, unknown>) => Promise<T>;
  resetError: () => void;
}

export function useTauriMutation<T = unknown>(
  options: UseMutationOptions<T>,
): MutationState<T> {
  const { command, args: defaultArgs, onSuccess, onError, onMutate } = options;
  const [isMutating, setIsMutating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (args?: Record<string, unknown>) => {
      if (!isTauriReady()) {
        return Promise.reject(new Error("Tauri not ready"));
      }
      setIsMutating(true);
      setError(null);
      try {
        await onMutate?.();
        const result = await invoke<T>(command, args || defaultArgs);
        onSuccess?.(result);
        return result;
      } catch (err) {
        const errorMsg = String(err);
        setError(errorMsg);
        onError?.(errorMsg);
        throw err;
      } finally {
        setIsMutating(false);
      }
    },
    [command, defaultArgs, onMutate, onSuccess, onError],
  );

  const resetError = useCallback(() => setError(null), []);

  return { isMutating, error, execute, resetError };
}
```

## Per-domain hook example

```ts
// src/hooks/useSettings.ts
import type { Settings } from "../types";
import { useTauriLoad, useTauriMutation } from "./useTauriCommand";

const DEFAULT_SETTINGS: Settings = { /* sensible defaults */ };

export function useSettings() {
  return useTauriLoad<Settings>({
    command: "get_settings",
    defaultValue: DEFAULT_SETTINGS,
  });
}

export function useSaveSettings() {
  return useTauriMutation<void>({ command: "save_settings_command" });
}
```

## Component usage

```tsx
function SettingsPage() {
  const { data: settings, isLoading, error, reload } = useSettings();
  const { execute: saveSettings, isMutating } = useSaveSettings();

  if (isLoading) return <Spinner />;
  if (error) return <ErrorBanner error={error} onRetry={reload} />;

  return (
    <Form
      initialValues={settings}
      onSubmit={async (values) => {
        await saveSettings({ settings: values });
        await reload();
      }}
    />
  );
}
```

## Why this shape

- **One place to add cross-cutting concerns** — retry, exponential backoff, telemetry, error toasts, request-id headers — all change one file.
- **Type safety** — `T` flows through `invoke<T>`. The hook user gets `data: T | null`, not `data: any`.
- **Three flavors** —
  - `useTauriCommand`: imperative; component triggers it.
  - `useTauriLoad`: auto-fires on mount; for "get me this data".
  - `useTauriMutation`: imperative; explicitly skips auto-fire; for write paths.
- **`isTauriReady()` guard** — In Tauri 2 the IPC bridge is ready before React mounts, but the guard makes the code safe to preview via plain `vite dev` for static UI iteration.
- **No `invoke()` in components** — Refactoring command names, adding logging, fixing race conditions all happen in one file. Without this discipline, every component reinvents loading/error state slightly differently.
