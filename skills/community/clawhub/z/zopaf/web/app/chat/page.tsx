"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { createSession } from "@/lib/api";

export default function NewChat() {
  const router = useRouter();

  useEffect(() => {
    createSession().then((sessionId) => {
      router.replace(`/chat/${sessionId}`);
    });
  }, [router]);

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
      <p className="text-zinc-500">Starting session...</p>
    </div>
  );
}
