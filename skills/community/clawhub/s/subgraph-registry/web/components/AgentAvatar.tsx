import { walletGradient } from "@/lib/format";

export function AgentAvatar({ wallet, size = 28 }: { wallet: string; size?: number }) {
  const { from, to } = walletGradient(wallet);
  return (
    <span
      aria-hidden
      className="inline-block flex-shrink-0 rounded-full"
      style={{
        width: size,
        height: size,
        background: `linear-gradient(135deg, ${from}, ${to})`,
        boxShadow: "inset 0 0 0 1px rgba(255,255,255,0.06)",
      }}
    />
  );
}
