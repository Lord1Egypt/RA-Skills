"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import PaywallCard from "./PaywallCard";
import { sendMessage, getSessionHistory } from "@/lib/api";

interface Message {
  role: "user" | "coach";
  content: string;
  gated?: boolean;
}

interface ChatWindowProps {
  sessionId: string;
}

export default function ChatWindow({ sessionId }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "coach",
      content:
        "Hey — I'm your negotiation coach. Tell me what you're negotiating. What kind of deal is it, who are the parties, and what's on the table so far?",
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isGated, setIsGated] = useState(false);
  const [restored, setRestored] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Restore session after payment redirect
  useEffect(() => {
    const justUnlocked = localStorage.getItem("just_unlocked");
    if (justUnlocked === sessionId) {
      localStorage.removeItem("just_unlocked");

      // Fetch chat history from backend and restore it
      getSessionHistory(sessionId).then((history) => {
        if (history.messages.length > 0) {
          setMessages([
            {
              role: "coach",
              content:
                "Hey — I'm your negotiation coach. Tell me what you're negotiating. What kind of deal is it, who are the parties, and what's on the table so far?",
            },
            ...history.messages,
          ]);
          setRestored(true);

          // Now auto-request the strategy since they paid
          setIsLoading(true);
          sendMessage(sessionId, "Show me my personalized counteroffers and strategy.")
            .then((result) => {
              setMessages((prev) => [
                ...prev,
                { role: "coach", content: result.response },
              ]);
            })
            .catch(() => {
              setMessages((prev) => [
                ...prev,
                {
                  role: "coach",
                  content: "Welcome back! You're unlocked. Ask me anything about your negotiation strategy.",
                },
              ]);
            })
            .finally(() => setIsLoading(false));
        } else {
          // Session was lost (server redeployed) — show a message
          setMessages([
            {
              role: "coach",
              content:
                "Welcome back! It looks like your session was reset (we're still in prototype mode). " +
                "Your payment went through — just start a new conversation and I'll get you to your strategy faster this time.",
            },
          ]);
        }
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSend = async (text: string) => {
    const userMessage: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const result = await sendMessage(sessionId, text);
      const coachMessage: Message = {
        role: "coach",
        content: result.response,
        gated: result.gated,
      };
      setMessages((prev) => [...prev, coachMessage]);
      if (result.gated) {
        setIsGated(true);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "coach",
          content:
            "Sorry, I hit an error. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-zinc-950">
      {/* Header */}
      <div className="border-b border-zinc-800 px-6 py-4">
        <h1 className="text-lg font-semibold text-zinc-100">
          Negotiation Coach
        </h1>
        <p className="text-xs text-zinc-500 mt-0.5">
          Your AI negotiation advisor
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto">
          {messages.map((msg, i) => (
            <MessageBubble key={i} role={msg.role} content={msg.content} />
          ))}

          {isGated && <PaywallCard sessionId={sessionId} />}

          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="bg-zinc-900 border border-zinc-800 rounded-2xl px-5 py-3.5">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:0ms]" />
                  <div className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:150ms]" />
                  <div className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading || isGated} />
    </div>
  );
}
