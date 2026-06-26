// components/SuspenseOnSearchParams.tsx
//
// A standard <Suspense> does NOT re-trigger its fallback on client-side
// navigation when only `searchParams` changes — the boundary is keyed on
// the route, not the query string. This wrapper re-keys the boundary on
// every searchParams change so the fallback shows during the new fetch.
//
// Use this on every page that has search or filter params.

"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, type ReactNode } from "react";

type Props = {
  fallback: ReactNode;
  children: ReactNode;
};

export default function SuspenseOnSearchParams({ fallback, children }: Props) {
  const searchParams = useSearchParams();
  return (
    <Suspense key={searchParams.toString()} fallback={fallback}>
      {children}
    </Suspense>
  );
}
