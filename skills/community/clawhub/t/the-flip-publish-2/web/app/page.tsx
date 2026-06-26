import { LiveIndicator } from "@/components/live-indicator";
import { JackpotDisplay } from "@/components/jackpot-display";
import { StatsDisplay } from "@/components/stats-display";
import { HowItWorks } from "@/components/how-it-works";
import { HowToPlay } from "@/components/how-to-play";
import { TicketLookup } from "@/components/ticket-lookup";
import { Footer } from "@/components/footer";
import { FlippingCoin } from "@/components/flipping-coin";

export default function Home() {
  return (
    <main className="min-h-screen bg-background flex flex-col relative overflow-hidden selection:bg-foreground selection:text-background">
      <LiveIndicator />

      {/* Hero section */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-16">
        {/* Coin animation */}
        <div className="mb-6">
          <FlippingCoin />
        </div>

        {/* Label */}
        <div className="mb-3 flex items-center gap-3">
          <span className="text-xs font-mono text-muted-foreground uppercase tracking-[0.3em]">
            Jackpot
          </span>
        </div>

        <JackpotDisplay />
        <StatsDisplay />
      </div>

      <HowItWorks />
      <TicketLookup />
      <HowToPlay />
      <Footer />
    </main>
  );
}
