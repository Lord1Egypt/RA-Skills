/**
 * Deep-dive sidebar reference — shadcn/ui's Sidebar component family.
 *
 * The Sidebar is one of shadcn's most complex components — this file
 * documents the full prop surface and the patterns that aren't obvious
 * from a first read of the docs: icon-collapse mode, the hover rail,
 * active-route styling, grouped nav with collapsible sections, and the
 * built-in mobile behavior (auto-switches to a Sheet overlay).
 *
 * Assumes: shadcn/ui `sidebar`, `avatar`, `dropdown-menu`, `collapsible`
 * added. `npx shadcn@latest add sidebar` installs the full family in one
 * command: SidebarProvider, Sidebar, SidebarHeader/Content/Footer,
 * SidebarGroup, SidebarMenu*, SidebarRail, SidebarTrigger, SidebarInset.
 */

"use client";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarRail,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  LayoutDashboard,
  Users,
  Settings,
  ChevronRight,
  FileText,
  BarChart3,
} from "lucide-react";
import { usePathname } from "next/navigation";

/**
 * KEY PROPS ON <Sidebar>:
 *
 * - `collapsible`: "offcanvas" (default — slides fully off-screen on
 *    toggle) | "icon" (collapses to an icon-only rail, most common for
 *    dashboards) | "none" (always expanded, no collapse behavior at all)
 * - `variant`: "sidebar" (default, flush) | "floating" (inset with margin
 *    and its own border/shadow) | "inset" (main content gets rounded
 *    corners and its own shadow, sidebar feels embedded)
 * - `side`: "left" | "right"
 *
 * `useSidebar()` hook exposes: state ("expanded" | "collapsed"), open,
 * setOpen, openMobile, setOpenMobile, isMobile, toggleSidebar — reach for
 * this when a component outside the Sidebar needs to react to its state.
 *
 * Mobile behavior is automatic: below the md breakpoint, the Sidebar
 * renders as a Sheet-based overlay instead of a fixed column — no extra
 * code needed, `isMobile` from useSidebar() is how you'd branch manually
 * if a component needs different behavior on mobile.
 *
 * Default keyboard shortcut: Cmd/Ctrl+B toggles the sidebar, wired
 * automatically by SidebarProvider.
 */

const NAV_ITEMS = [
  { label: "Overview", icon: LayoutDashboard, href: "/dashboard" },
  { label: "Team", icon: Users, href: "/dashboard/team" },
];

const REPORTS_ITEMS = [
  { label: "Analytics", icon: BarChart3, href: "/dashboard/reports/analytics" },
  { label: "Exports", icon: FileText, href: "/dashboard/reports/exports" },
];

export default function AppShellWithSidebar({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      {/* SidebarInset pairs with variant="inset" on <Sidebar> for the
          embedded-panel look; use a plain <main> if using the default
          "sidebar" variant instead. */}
      <SidebarInset>
        <header className="flex h-14 items-center gap-4 border-b border-border px-4">
          <SidebarTrigger />
          <span className="text-sm font-medium">Dashboard</span>
        </header>
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}

function AppSidebar() {
  const pathname = usePathname();

  return (
    <Sidebar collapsible="icon" variant="inset">
      <SidebarHeader className="px-3 py-4">
        <span className="font-display text-sm font-semibold group-data-[collapsible=icon]:hidden">
          Product
        </span>
      </SidebarHeader>

      <SidebarContent>
        {/* Flat group — always visible */}
        <SidebarGroup>
          <SidebarGroupLabel>Workspace</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {NAV_ITEMS.map((item) => (
                <SidebarMenuItem key={item.label}>
                  {/* isActive drives the active-route styling built into
                      SidebarMenuButton — compare against the real route,
                      don't hand-roll a className check */}
                  <SidebarMenuButton asChild isActive={pathname === item.href} tooltip={item.label}>
                    <a href={item.href}>
                      <item.icon />
                      <span>{item.label}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        {/* Collapsible group — for nav sections with several sub-items,
            wrap the group in <Collapsible> so it can fold shut */}
        <Collapsible defaultOpen className="group/collapsible">
          <SidebarGroup>
            <SidebarGroupLabel asChild>
              <CollapsibleTrigger className="flex w-full items-center">
                Reports
                <ChevronRight className="ml-auto size-4 transition-transform group-data-[state=open]/collapsible:rotate-90" />
              </CollapsibleTrigger>
            </SidebarGroupLabel>
            <CollapsibleContent>
              <SidebarGroupContent>
                <SidebarMenu>
                  {REPORTS_ITEMS.map((item) => (
                    <SidebarMenuItem key={item.label}>
                      <SidebarMenuButton asChild isActive={pathname === item.href} tooltip={item.label}>
                        <a href={item.href}>
                          <item.icon />
                          <span>{item.label}</span>
                        </a>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                </SidebarMenu>
              </SidebarGroupContent>
            </CollapsibleContent>
          </SidebarGroup>
        </Collapsible>
      </SidebarContent>

      <SidebarFooter className="p-3">
        <UserMenu />
      </SidebarFooter>

      {/* SidebarRail: a thin hover/drag strip at the sidebar's edge — lets
          users grab-toggle the sidebar even when collapsed to icon mode.
          Purely additive; safe to always include with collapsible="icon". */}
      <SidebarRail />
    </Sidebar>
  );
}

function UserMenu() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="flex w-full items-center gap-2 rounded-md p-2 text-left hover:bg-accent">
        <Avatar className="size-7 shrink-0">
          <AvatarFallback>JD</AvatarFallback>
        </Avatar>
        {/* group-data-[collapsible=icon]:hidden — the standard pattern for
            hiding text labels when the sidebar collapses to icon-only */}
        <div className="min-w-0 flex-1 group-data-[collapsible=icon]:hidden">
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
 * STYLING BY SIDEBAR STATE — common recipes:
 *
 * Hide an element only when collapsed to icons:
 *   className="group-data-[collapsible=icon]:hidden"
 *
 * Show an element only when collapsed to icons:
 *   className="hidden group-data-[collapsible=icon]:block"
 *
 * Style a menu button differently when active (built in via `isActive`
 * prop on SidebarMenuButton — don't hand-roll this with usePathname
 * string matching inside a className, use the prop so it also drives
 * aria-current correctly).
 */
