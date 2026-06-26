"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { unlockSession } from "@/lib/api";

export default function UnlockSuccess() {
  const router = useRouter();
  const [status, setStatus] = useState("Unlocking your strategy...");

  useEffect(() => {
    const sessionId = localStorage.getItem("pending_unlock_session");
    if (!sessionId) {
      setStatus("No session found. Please try again.");
      return;
    }

    unlockSession(sessionId)
      .then(() => {
        localStorage.removeItem("pending_unlock_session");
        localStorage.setItem("just_unlocked", sessionId);
        router.replace(`/chat/${sessionId}`);
      })
      .catch(() => {
        setStatus("Something went wrong. Please contact support.");
      });
  }, [router]);

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
      <p className="text-zinc-400">{status}</p>
    </div>
  );
}
