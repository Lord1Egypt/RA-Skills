"use client";

const STRIPE_PAYMENT_LINK = "https://buy.stripe.com/9B6fZgdMX1lZ8QJ0xCdEs00";

interface PaywallCardProps {
  sessionId: string;
}

export default function PaywallCard({ sessionId }: PaywallCardProps) {
  const handleCheckout = () => {
    // Store sessionId so we can unlock after payment redirect
    localStorage.setItem("pending_unlock_session", sessionId);
    window.location.href = STRIPE_PAYMENT_LINK;
  };

  return (
    <div className="flex justify-start mb-4">
      <div className="max-w-md w-full rounded-2xl border border-zinc-700 bg-gradient-to-b from-zinc-800 to-zinc-900 p-6">
        <h3 className="text-lg font-semibold text-zinc-100 mb-2">
          Your strategy is ready
        </h3>
        <p className="text-sm text-zinc-400 mb-4">
          I&apos;ve built a model of your negotiation and generated personalized
          counteroffers. Unlock to see:
        </p>
        <ul className="text-sm text-zinc-400 mb-6 space-y-2">
          <li className="flex items-start gap-2">
            <span className="text-green-400 mt-0.5">&#10003;</span>
            Smart counteroffers tailored to your priorities
          </li>
          <li className="flex items-start gap-2">
            <span className="text-green-400 mt-0.5">&#10003;</span>
            Analysis of what you gain and what you trade
          </li>
          <li className="flex items-start gap-2">
            <span className="text-green-400 mt-0.5">&#10003;</span>
            Strategy to reveal the other side&apos;s priorities
          </li>
        </ul>
        <button
          onClick={handleCheckout}
          className="w-full rounded-full bg-white text-black px-6 py-3 text-sm font-semibold hover:bg-zinc-200 transition-colors"
        >
          Unlock your strategy — $9
        </button>
        <p className="text-xs text-zinc-600 text-center mt-3">
          One-time payment. No subscription.
        </p>
      </div>
    </div>
  );
}
