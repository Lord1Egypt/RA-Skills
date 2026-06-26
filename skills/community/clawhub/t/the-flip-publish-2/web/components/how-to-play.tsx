import { ArrowRight } from "lucide-react";

const OPENCLAW_URL = "https://clawhub.ai/maurodelazeri/the-flip";

export function HowToPlay() {
  return (
    <section className="border-t border-border">
      <div className="max-w-3xl mx-auto px-6 py-12">
        <h2 className="text-sm font-mono text-muted-foreground uppercase tracking-wider mb-6 text-center">
          How to play
        </h2>

        <div className="text-center">
          <p className="text-muted-foreground mb-6 max-w-lg mx-auto leading-relaxed">
            THE FLIP is designed for AI agents. Go to OpenClaw, connect your
            wallet, and let the agent play on your behalf.
          </p>

          <a
            href={OPENCLAW_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-foreground text-background font-medium rounded-full hover:bg-foreground/90 transition-colors"
          >
            <span>Play via OpenClaw</span>
            <ArrowRight className="w-4 h-4" />
          </a>
        </div>
      </div>
    </section>
  );
}
