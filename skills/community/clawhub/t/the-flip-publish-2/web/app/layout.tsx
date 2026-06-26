import React from "react";
import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import { Providers } from "@/components/providers";
import "./globals.css";

const _geist = Geist({ subsets: ["latin"] });
const _geistMono = Geist_Mono({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "THE FLIP",
  description:
    "$1 USDC. Pick 20. 20 coins flip at once. Match 14 to win the jackpot.",
  generator: "v0.app",
  openGraph: {
    title: "THE FLIP",
    description:
      "$1 USDC. Pick 20. 20 coins flip at once. Match 14 to win the jackpot.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "THE FLIP",
    description:
      "$1 USDC. Pick 20. 20 coins flip at once. Match 14 to win the jackpot.",
  },
  icons: {
    icon: [
      {
        url: "/icon-light-32x32.png",
        media: "(prefers-color-scheme: light)",
      },
      {
        url: "/icon-dark-32x32.png",
        media: "(prefers-color-scheme: dark)",
      },
      {
        url: "/icon.svg",
        type: "image/svg+xml",
      },
    ],
    apple: "/apple-icon.png",
  },
};

export const viewport: Viewport = {
  themeColor: "#000000",
  colorScheme: "dark",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <Providers>{children}</Providers>
        <Analytics />
      </body>
    </html>
  );
}
