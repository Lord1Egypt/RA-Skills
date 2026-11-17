/**
 * Standalone header/navbar reference — Tailwind v4 + shadcn/ui.
 *
 * Covers: sticky + backdrop-blur on scroll, desktop nav, mobile Sheet-based
 * nav (correct focus trap / ARIA for free via Radix), and an optional
 * command-palette trigger (Cmd/Ctrl+K) — a common production pattern for
 * SaaS apps and docs sites.
 *
 * Assumes: shadcn/ui `button`, `sheet`, `command` added.
 */

"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetTitle,
} from "@/components/ui/sheet";
import {
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
} from "@/components/ui/command";
import { Menu, Search } from "lucide-react";

const NAV_LINKS = [
  { label: "Features", href: "#features" },
  { label: "Pricing", href: "#pricing" },
  { label: "Docs", href: "#docs" },
];

export default function Header() {
  const [commandOpen, setCommandOpen] = useState(false);

  // Cmd/Ctrl+K to open the command palette — standard SaaS convention
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setCommandOpen((open) => !open);
      }
    }
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-border bg-background/80 backdrop-blur-md backdrop-saturate-150">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <a href="/" className="font-display text-lg font-semibold">
            Product
          </a>

          <nav className="hidden items-center gap-8 text-sm text-muted-foreground md:flex" aria-label="Primary">
            {NAV_LINKS.map((link) => (
              <a key={link.href} href={link.href} className="transition-colors hover:text-foreground">
                {link.label}
              </a>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            {/* Search / command palette trigger */}
            <Button
              variant="outline"
              size="sm"
              className="hidden text-muted-foreground sm:inline-flex"
              onClick={() => setCommandOpen(true)}
            >
              <Search className="mr-2 size-4" aria-hidden="true" />
              Search
              <kbd className="ml-3 rounded border border-border bg-muted px-1.5 py-0.5 text-xs">⌘K</kbd>
            </Button>

            <Button variant="ghost" size="sm" className="hidden md:inline-flex">
              Sign in
            </Button>
            <Button size="sm" className="hidden md:inline-flex">
              Get started
            </Button>

            {/* Mobile nav — Sheet gets focus trap + ARIA for free via Radix */}
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden" aria-label="Open menu">
                  <Menu className="size-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-72">
                <SheetTitle className="sr-only">Navigation</SheetTitle>
                <nav className="mt-8 flex flex-col gap-1" aria-label="Mobile">
                  {NAV_LINKS.map((link) => (
                    <a
                      key={link.href}
                      href={link.href}
                      className="rounded-md px-3 py-2 text-sm hover:bg-accent"
                    >
                      {link.label}
                    </a>
                  ))}
                  <div className="mt-4 flex flex-col gap-2 border-t border-border pt-4">
                    <Button variant="outline">Sign in</Button>
                    <Button>Get started</Button>
                  </div>
                </nav>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </header>

      <CommandDialog open={commandOpen} onOpenChange={setCommandOpen}>
        <CommandInput placeholder="Type a command or search..." />
        <CommandList>
          <CommandEmpty>No results found.</CommandEmpty>
          <CommandGroup heading="Navigation">
            {NAV_LINKS.map((link) => (
              <CommandItem key={link.href} onSelect={() => setCommandOpen(false)}>
                {link.label}
              </CommandItem>
            ))}
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </>
  );
}
