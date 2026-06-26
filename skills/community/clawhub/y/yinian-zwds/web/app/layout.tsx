import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "一念紫微斗数 | Yinian ZWDS",
  description: "AI驱动的紫微斗数深度解盘系统 · 三派合一",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🦞</text></svg>" />
      </head>
      <body>{children}</body>
    </html>
  );
}
