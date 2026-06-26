const steps = [
  {
    icon: "\u{1FA99}",
    title: "Pick 20 Predictions",
    description:
      "Pay $1 USDC and choose heads or tails for 20 coin flips. Enter anytime — the game never stops.",
  },
  {
    icon: "\u{1F3B2}",
    title: "20 Coins Flip at Once",
    description:
      "Each round flips all 20 coins simultaneously. Your first 14 predictions must match — one wrong and you're out.",
  },
  {
    icon: "\u{1F3C6}",
    title: "Take the Jackpot",
    description:
      "Match all 14 and claim the entire pot. If nobody wins, the jackpot keeps growing from new entries.",
  },
];

export function HowItWorks() {
  return (
    <section className="border-t border-border bg-card/50">
      <div className="max-w-3xl mx-auto px-6 py-12">
        <h2 className="text-sm font-mono text-muted-foreground uppercase tracking-wider mb-8 text-center">
          How it works
        </h2>

        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((step, i) => (
            <div key={i} className="text-center">
              <div className="text-3xl mb-3">{step.icon}</div>
              <div className="text-sm font-bold text-foreground mb-2">
                {step.title}
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {step.description}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-10 p-4 rounded-lg bg-secondary/50 border border-border">
          <p className="text-xs text-muted-foreground text-center leading-relaxed">
            <span className="text-foreground font-medium">
              $1 could become $1M+.
            </span>{" "}
            The jackpot grows continuously until someone wins. No rounds that
            lock you out, no time limit, no cap. Fully on-chain, fully
            verifiable.
          </p>
        </div>
      </div>
    </section>
  );
}
