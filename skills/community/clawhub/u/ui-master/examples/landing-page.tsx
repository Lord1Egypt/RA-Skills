/**
 * Landing page structural reference — Tailwind v4 + shadcn/ui.
 *
 * This is a STRUCTURAL pattern, not a template to paste verbatim.
 * Replace copy, imagery, and the hero's signature visual with something
 * specific to the actual product brief before shipping — see the
 * frontend-design skill for aesthetic direction if a distinctive
 * art-direction pass is needed on top of this structure.
 *
 * Assumes: shadcn/ui initialized, `button`, `card`, `badge` added.
 * Assumes: design tokens (bg-background, text-foreground, bg-primary, etc.)
 * already wired per references/design-tokens.md.
 */

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check } from "lucide-react";

const FEATURES = [
  { title: "Feature one", description: "One concrete sentence about the real capability, not marketing fluff." },
  { title: "Feature two", description: "State what changes for the user, in their language, not the system's." },
  { title: "Feature three", description: "Specific beats clever — say exactly what this does." },
];

const PRICING_TIERS = [
  { name: "Starter", price: "$0", features: ["Core feature", "Up to 3 projects", "Community support"] },
  { name: "Pro", price: "$29", features: ["Everything in Starter", "Unlimited projects", "Priority support"], highlighted: true },
  { name: "Enterprise", price: "Custom", features: ["Everything in Pro", "SSO / SAML", "Dedicated support"] },
];

export default function LandingPage() {
  return (
    <div className="min-h-svh bg-background text-foreground">
      {/* Nav */}
      <header className="sticky top-0 z-40 border-b border-border bg-background/80 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <span className="font-display text-lg font-semibold">Product</span>
          <nav className="hidden items-center gap-8 text-sm text-muted-foreground md:flex">
            <a href="#features" className="hover:text-foreground">Features</a>
            <a href="#pricing" className="hover:text-foreground">Pricing</a>
            <a href="#" className="hover:text-foreground">Docs</a>
          </nav>
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm">Sign in</Button>
            <Button size="sm">Get started</Button>
          </div>
        </div>
      </header>

      {/* Hero — the thesis of the page: one clear headline + proof, not a template stat block by default */}
      <section className="mx-auto max-w-6xl px-6 py-24 text-center">
        <Badge variant="secondary" className="mb-6">New — v2.0 is live</Badge>
        <h1 className="mx-auto max-w-3xl font-display text-4xl font-semibold tracking-tight sm:text-5xl">
          Replace the headline with the one true claim this product makes
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-lg text-muted-foreground">
          One sentence explaining what the product does and who it's for. No filler adjectives.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Button size="lg">Get started free</Button>
          <Button size="lg" variant="outline">View demo</Button>
        </div>
      </section>

      {/* Social proof */}
      <section className="border-y border-border bg-muted/30 py-10">
        <div className="mx-auto max-w-6xl px-6">
          <p className="text-center text-sm text-muted-foreground">Trusted by teams at</p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-x-12 gap-y-4 opacity-60 grayscale">
            {/* logo placeholders — swap for real customer logos */}
            {["Acme", "Globex", "Initech", "Umbrella", "Soylent"].map((name) => (
              <span key={name} className="text-sm font-medium">{name}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Feature grid */}
      <section id="features" className="mx-auto max-w-6xl px-6 py-24">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="font-display text-3xl font-semibold tracking-tight">What it does, plainly</h2>
          <p className="mt-4 text-muted-foreground">
            Each card should state a real capability. Cut anything that's decoration rather than information.
          </p>
        </div>
        <div className="mt-16 grid grid-cols-1 gap-6 sm:grid-cols-3">
          {FEATURES.map((f) => (
            <Card key={f.title} className="p-6">
              <h3 className="font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{f.description}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="mx-auto max-w-6xl px-6 py-24">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="font-display text-3xl font-semibold tracking-tight">Simple pricing</h2>
        </div>
        <div className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-3">
          {PRICING_TIERS.map((tier) => (
            <Card
              key={tier.name}
              className={`p-6 ${tier.highlighted ? "border-primary shadow-lg" : ""}`}
            >
              <h3 className="font-semibold">{tier.name}</h3>
              <p className="mt-2 font-display text-3xl font-semibold">{tier.price}</p>
              <ul className="mt-6 space-y-3 text-sm">
                {tier.features.map((feat) => (
                  <li key={feat} className="flex items-center gap-2">
                    <Check className="size-4 text-primary" aria-hidden="true" />
                    {feat}
                  </li>
                ))}
              </ul>
              <Button className="mt-6 w-full" variant={tier.highlighted ? "default" : "outline"}>
                Choose {tier.name}
              </Button>
            </Card>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="border-t border-border bg-muted/30 py-24 text-center">
        <h2 className="font-display text-3xl font-semibold tracking-tight">Ready to start?</h2>
        <div className="mt-8">
          <Button size="lg">Get started free</Button>
        </div>
      </section>

      {/* Footer — real link groups, not a single row of icons */}
      <footer className="border-t border-border py-12">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-8 px-6 text-sm sm:grid-cols-4">
          <div>
            <p className="font-medium">Product</p>
            <ul className="mt-3 space-y-2 text-muted-foreground">
              <li><a href="#features" className="hover:text-foreground">Features</a></li>
              <li><a href="#pricing" className="hover:text-foreground">Pricing</a></li>
            </ul>
          </div>
          <div>
            <p className="font-medium">Company</p>
            <ul className="mt-3 space-y-2 text-muted-foreground">
              <li><a href="#" className="hover:text-foreground">About</a></li>
              <li><a href="#" className="hover:text-foreground">Careers</a></li>
            </ul>
          </div>
          <div>
            <p className="font-medium">Resources</p>
            <ul className="mt-3 space-y-2 text-muted-foreground">
              <li><a href="#" className="hover:text-foreground">Docs</a></li>
              <li><a href="#" className="hover:text-foreground">Support</a></li>
            </ul>
          </div>
          <div>
            <p className="font-medium">Legal</p>
            <ul className="mt-3 space-y-2 text-muted-foreground">
              <li><a href="#" className="hover:text-foreground">Privacy</a></li>
              <li><a href="#" className="hover:text-foreground">Terms</a></li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  );
}
