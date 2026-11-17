// components/use-task.ts
'use client';

import { useEffect, useState } from 'react';

export type TaskState = {
  status?: string;
  done?: boolean;
  ok?: boolean;
  files?: string[];
  text?: string | null;
  cost?: number | null;
  error?: string;
};

/** Polls /api/tasks/[token] every 3 seconds until the task ends. */
export function useTask(token: string | null): TaskState | null {
  const [state, setState] = useState<TaskState | null>(null);

  useEffect(() => {
    if (!token) return;
    let stopped = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const poll = async () => {
      try {
        const response = await fetch(`/api/tasks/${token}`, { cache: 'no-store' });
        const next = (await response.json()) as TaskState;
        if (stopped) return;
        setState(next);
        if (!next.done && !next.error) timer = setTimeout(poll, 3000);
      } catch {
        if (!stopped) timer = setTimeout(poll, 5000);
      }
    };
    void poll();
    return () => {
      stopped = true;
      clearTimeout(timer);
    };
  }, [token]);

  return state;
}
