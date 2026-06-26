import "./globals.css";
import type { Metadata } from "next";
import { Inter_Tight, JetBrains_Mono } from "next/font/google";

const interTight = Inter_Tight({
  subsets: ["latin"],
  variable: "--font-inter-tight",
  display: "swap",
});
const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
  display: "swap",
});

export const metadata: Metadata = {
  title: "x402 Watch",
  description:
    "Live tracker of x402 micropayments to The Graph on Base — agent counts, growth, and per-agent leaderboards.",
  metadataBase: new URL("https://graphadvocate.com"),
  openGraph: {
    title: "x402 Watch",
    description:
      "Live x402 micropayments on Base, with ERC-8004 agent attribution.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "x402 Watch",
    description: "Live x402 micropayments on Base.",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${interTight.variable} ${jetbrains.variable}`}>
      <body className="min-h-screen">
        <div className="mx-auto max-w-[1280px] px-6 py-8">{children}</div>
        <footer className="mx-auto max-w-[1280px] px-6 pb-8 pt-2 text-center">
          <div className="text-[13px] font-medium tracking-wide text-muted">
            Data powered by{" "}
            <a
              className="text-ink underline decoration-accent decoration-2 underline-offset-4 hover:text-accent"
              href="https://thegraph.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              The Graph
            </a>
          </div>
          <div className="mt-1 text-[11px] text-dim">
            refreshes once daily · run by{" "}
            <a className="text-muted hover:text-accent" href="https://graphadvocate.com" target="_blank" rel="noopener noreferrer">
              graphadvocate.eth
            </a>
          </div>
        </footer>
      </body>
    </html>
  );
}
