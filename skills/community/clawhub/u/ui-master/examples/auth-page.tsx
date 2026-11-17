/**
 * Auth page structural reference — Tailwind v4 + shadcn/ui.
 *
 * Pattern: centered card, split-screen brand panel optional on desktop.
 * The loading and error states below are not optional extras — an auth
 * form demoed only in its empty, untouched state will visibly break the
 * first time a real user mistypes a password.
 *
 * Assumes: shadcn/ui `card`, `input`, `label`, `button`, `form` (React
 * Hook Form + Zod) added.
 */

"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AlertCircle, Loader2 } from "lucide-react";

export default function AuthPage() {
  const [status, setStatus] = useState<"idle" | "submitting" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("submitting");
    setErrorMessage(null);

    try {
      // await signIn(...)
      await new Promise((resolve) => setTimeout(resolve, 800));
      setStatus("idle");
    } catch {
      setStatus("error");
      // Specific and actionable, in the interface's voice — never a raw
      // stack trace or a bare "Error" string.
      setErrorMessage("Couldn't sign in — check your email and password and try again.");
    }
  }

  return (
    <div className="grid min-h-svh grid-cols-1 lg:grid-cols-2">
      {/* Brand panel — desktop only. On mobile this section is skipped
          entirely rather than stacked, keeping the form the sole focus. */}
      <div className="hidden flex-col justify-between bg-primary p-10 text-primary-foreground lg:flex">
        <span className="font-display text-lg font-semibold">Product</span>
        <blockquote className="max-w-md text-lg">
          Replace with a real customer quote or product statement — never
          filler text on a shipped screen.
        </blockquote>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center p-6">
        <Card className="w-full max-w-sm">
          <CardHeader>
            <h1 className="font-display text-2xl font-semibold">Welcome back</h1>
            <p className="text-sm text-muted-foreground">Sign in to your account to continue.</p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4" noValidate>
              {status === "error" && errorMessage && (
                <div
                  role="alert"
                  className="flex items-start gap-2 rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive"
                >
                  <AlertCircle className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
                  <span>{errorMessage}</span>
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  disabled={status === "submitting"}
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password">Password</Label>
                  <a href="#" className="text-sm text-muted-foreground hover:text-foreground">
                    Forgot password?
                  </a>
                </div>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  disabled={status === "submitting"}
                />
              </div>

              <Button type="submit" className="w-full" disabled={status === "submitting"}>
                {status === "submitting" ? (
                  <>
                    <Loader2 className="mr-2 size-4 animate-spin" aria-hidden="true" />
                    Signing in...
                  </>
                ) : (
                  "Sign in"
                )}
              </Button>
            </form>

            <p className="mt-6 text-center text-sm text-muted-foreground">
              Don't have an account?{" "}
              <a href="#" className="font-medium text-foreground hover:underline">
                Sign up
              </a>
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
