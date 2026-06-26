"use client";

import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatWindow from "@/components/ChatWindow";
import { unlockSession } from "@/lib/api";

export default function ChatPage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = use(params);
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Detect Stripe redirect: sessionId will be a checkout session ID like cs_test_...
    if (sessionId.startsWith("cs_test_") || sessionId.startsWith("cs_")) {
      const realSessionId = localStorage.getItem("pending_unlock_session");
      if (realSessionId) {
        unlockSession(realSessionId).then(() => {
          localStorage.removeItem("pending_unlock_session");
          localStorage.setItem("just_unlocked", realSessionId);
          router.replace(`/chat/${realSessionId}`);
        });
      } else {
        // No session found — send to home
        router.replace("/");
      }
    } else {
      setReady(true);
    }
  }, [sessionId, router]);

  if (!ready) {
    return (
      <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
        <p className="text-zinc-500">Loading...</p>
      </div>
    );
  }

  return <ChatWindow sessionId={sessionId} />;
}
