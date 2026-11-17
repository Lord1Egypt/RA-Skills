/**
 * Authenticated app shell structural reference — Tailwind v4 + shadcn/ui.
 *
 * Pattern: collapsible sidebar + sticky topbar + scrollable content region.
 * Adapt nav items, content, and empty/loading states to the real product —
 * this is scaffolding, not a finished screen.
 *
 * Assumes: shadcn/ui `sidebar`, `avatar`, `dropdown-menu`, `input`,
 * `skeleton`, `table` added, and the `useIsMobile` hook shadcn's sidebar
 * component generates alongside it.
 */

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { LayoutDashboard, Users, Settings, Search } from "lucide-react";

const NAV_ITEMS = [
  { label: "Overview", icon: LayoutDashboard, href: "/dashboard" },
  { label: "Team", icon: Users, href: "/dashboard/team" },
  { label: "Settings", icon: Settings, href: "/dashboard/settings" },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <Sidebar collapsible="icon">
        <SidebarHeader className="px-3 py-4">
          <span className="font-display text-sm font-semibold">Product</span>
        </SidebarHeader>
        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupLabel>Workspace</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {NAV_ITEMS.map((item) => (
                  <SidebarMenuItem key={item.label}>
                    <SidebarMenuButton asChild>
                      <a href={item.href}>
                        <item.icon className="size-4" aria-hidden="true" />
                        <span>{item.label}</span>
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
        <SidebarFooter className="p-3">
          <UserMenu />
        </SidebarFooter>
      </Sidebar>

      <div className="flex min-h-svh flex-1 flex-col">
        {/* Topbar */}
        <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b border-border bg-background px-4">
          <SidebarTrigger />
          <div className="relative max-w-sm flex-1">
            <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
            <Input placeholder="Search..." className="pl-9" aria-label="Search" />
          </div>
        </header>

        {/* Content region — consistent max-width and padding, not per-page arbitrary values */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="mx-auto max-w-6xl">{children}</div>
        </main>
      </div>
    </SidebarProvider>
  );
}

function UserMenu() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="flex w-full items-center gap-2 rounded-md p-2 text-left hover:bg-accent">
        <Avatar className="size-7">
          <AvatarFallback>JD</AvatarFallback>
        </Avatar>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium">Jane Doe</p>
          <p className="truncate text-xs text-muted-foreground">jane@company.com</p>
        </div>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="w-56">
        <DropdownMenuItem>Account settings</DropdownMenuItem>
        <DropdownMenuItem>Billing</DropdownMenuItem>
        <DropdownMenuItem>Sign out</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

/**
 * Example content-region pattern: loading, empty, and populated states
 * for a data table. Swap the table body for TanStack Table + shadcn's
 * `data-table` block when wiring real data — this shows the three
 * states that must all be designed, not just the happy path.
 */
export function DashboardTableStates({
  status,
}: {
  status: "loading" | "empty" | "populated";
}) {
  if (status === "loading") {
    return (
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full rounded-md" />
        ))}
      </div>
    );
  }

  if (status === "empty") {
    return (
      <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-border py-16 text-center">
        <p className="font-medium">No team members yet</p>
        <p className="mt-1 max-w-sm text-sm text-muted-foreground">
          Invite people to your workspace to see them listed here.
        </p>
      </div>
    );
  }

  return <p className="text-sm text-muted-foreground">Populated table goes here.</p>;
}
