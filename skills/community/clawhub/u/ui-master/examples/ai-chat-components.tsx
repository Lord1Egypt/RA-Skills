/**
 * AI chat interface components — Tailwind v4 + shadcn/ui.
 *
 * Covers the pieces almost every AI agent/chat UI needs: message bubbles
 * (user vs. assistant), a typing/thinking indicator, streaming text with
 * a blinking cursor, markdown rendering inside a bubble (code blocks,
 * lists, links), and an auto-resizing prompt input with the standard
 * Enter-to-send / Shift+Enter-for-newline convention.
 *
 * Assumes: shadcn/ui `avatar`, `button`, `textarea`, `tooltip` added.
 * Markdown rendering assumes `react-markdown` + `remark-gfm` installed
 * (`npm install react-markdown remark-gfm`) — swap for any markdown
 * renderer, the styling wrapper is what matters here.
 */

"use client";

import { useEffect, useRef, useState } from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { ArrowUp, Square, Copy, Check, Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/* ------------------------------------------------------------------ */
/* Message bubble                                                      */
/* ------------------------------------------------------------------ */

type Role = "user" | "assistant";

interface ChatMessageProps {
  role: Role;
  content: string;
  isStreaming?: boolean;
}

export function ChatMessage({ role, content, isStreaming }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      <Avatar className="mt-0.5 size-7 shrink-0">
        <AvatarFallback className={isUser ? "bg-primary text-primary-foreground" : "bg-muted"}>
          {isUser ? "U" : <Sparkles className="size-3.5" />}
        </AvatarFallback>
      </Avatar>

      <div className={`flex max-w-[75%] flex-col gap-1 ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={
            isUser
              ? "rounded-2xl rounded-tr-sm bg-primary px-4 py-2.5 text-sm text-primary-foreground"
              : "rounded-2xl rounded-tl-sm bg-muted px-4 py-2.5 text-sm text-foreground"
          }
        >
          {isUser ? (
            // User messages: plain text, preserve line breaks, never
            // render as markdown (avoids user-controlled markdown/HTML
            // injection concerns and keeps rendering trivially cheap).
            <p className="whitespace-pre-wrap">{content}</p>
          ) : (
            <MarkdownContent content={content} />
          )}
          {isStreaming && <StreamingCursor />}
        </div>

        {!isUser && !isStreaming && content && <MessageActions content={content} />}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Streaming cursor + typing indicator                                 */
/* ------------------------------------------------------------------ */

function StreamingCursor() {
  return (
    <span
      className="ml-0.5 inline-block h-4 w-[2px] translate-y-0.5 animate-pulse bg-current align-middle motion-reduce:animate-none"
      aria-hidden="true"
    />
  );
}

/**
 * "Thinking" indicator shown before the first token arrives — distinct
 * from the streaming cursor, which appears once text is actively
 * rendering. Showing the right one at the right time is what makes a
 * chat UI feel responsive rather than frozen.
 */
export function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 rounded-2xl rounded-tl-sm bg-muted px-4 py-3">
      <span className="sr-only">Assistant is responding</span>
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="size-1.5 animate-bounce rounded-full bg-muted-foreground/60 motion-reduce:animate-none"
          style={{ animationDelay: `${i * 120}ms`, animationDuration: "900ms" }}
        />
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Markdown-in-bubble rendering                                        */
/* ------------------------------------------------------------------ */

function MarkdownContent({ content }: { content: string }) {
  return (
    <div
      className="
        prose prose-sm max-w-none dark:prose-invert
        prose-p:my-1.5 prose-p:leading-relaxed
        prose-headings:mb-2 prose-headings:mt-3 prose-headings:font-semibold
        prose-ul:my-1.5 prose-ol:my-1.5
        prose-li:my-0.5
        prose-a:text-primary prose-a:underline prose-a:underline-offset-2
        prose-strong:font-semibold
        prose-code:rounded prose-code:bg-black/10 prose-code:px-1 prose-code:py-0.5 prose-code:text-[0.85em] prose-code:before:content-none prose-code:after:content-none
        dark:prose-code:bg-white/10
      "
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Override <pre><code> to get a real code block with a copy
          // button — the default prose styling only handles inline code.
          pre: ({ children }) => <CodeBlock>{children}</CodeBlock>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

function CodeBlock({ children }: { children: React.ReactNode }) {
  const [copied, setCopied] = useState(false);
  const codeRef = useRef<HTMLPreElement>(null);

  async function handleCopy() {
    const text = codeRef.current?.textContent ?? "";
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="group relative my-2">
      <pre
        ref={codeRef}
        className="overflow-x-auto rounded-lg bg-neutral-950 p-3 text-xs text-neutral-100 dark:bg-black"
      >
        {children}
      </pre>
      <Button
        size="icon"
        variant="ghost"
        className="absolute right-2 top-2 size-7 opacity-0 transition-opacity group-hover:opacity-100"
        onClick={handleCopy}
        aria-label="Copy code"
      >
        {copied ? <Check className="size-3.5" /> : <Copy className="size-3.5" />}
      </Button>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Message actions (copy, regenerate — shown after streaming completes) */
/* ------------------------------------------------------------------ */

function MessageActions({ content }: { content: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="flex gap-1 px-1 opacity-0 transition-opacity group-hover:opacity-100 focus-within:opacity-100">
      <Button size="icon" variant="ghost" className="size-6" onClick={handleCopy} aria-label="Copy message">
        {copied ? <Check className="size-3" /> : <Copy className="size-3" />}
      </Button>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Auto-resizing prompt input                                          */
/* ------------------------------------------------------------------ */

interface PromptInputProps {
  onSubmit: (value: string) => void;
  isGenerating?: boolean;
  onStop?: () => void;
}

export function PromptInput({ onSubmit, isGenerating, onStop }: PromptInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize: reset height first so shrinking works, then grow to
  // scrollHeight, capped by max-height in the className (overflow then
  // takes over instead of growing forever).
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [value]);

  function handleSubmit() {
    const trimmed = value.trim();
    if (!trimmed || isGenerating) return;
    onSubmit(trimmed);
    setValue("");
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    // Enter sends; Shift+Enter inserts a newline — the standard chat
    // convention users expect from every major AI product.
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div className="flex items-end gap-2 rounded-2xl border border-input bg-background p-2 shadow-sm focus-within:ring-2 focus-within:ring-ring">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Message..."
        rows={1}
        className="max-h-[200px] flex-1 resize-none bg-transparent px-2 py-1.5 text-sm outline-none placeholder:text-muted-foreground"
        aria-label="Message input"
      />

      {isGenerating ? (
        <Button size="icon" variant="secondary" className="shrink-0 rounded-full" onClick={onStop} aria-label="Stop generating">
          <Square className="size-3.5 fill-current" />
        </Button>
      ) : (
        <Button
          size="icon"
          className="shrink-0 rounded-full"
          onClick={handleSubmit}
          disabled={!value.trim()}
          aria-label="Send message"
        >
          <ArrowUp className="size-4" />
        </Button>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Composed example                                                    */
/* ------------------------------------------------------------------ */

export function ChatExample() {
  return (
    <div className="mx-auto flex h-full max-w-2xl flex-col gap-6 p-4">
      <div className="flex-1 space-y-6 overflow-y-auto">
        <ChatMessage role="user" content="Explain what a two-tier memory system is." />
        <ChatMessage
          role="assistant"
          content={`A two-tier memory system typically separates:\n\n1. **Short-term memory** — recent conversation turns, kept in fast storage (e.g. SQLite).\n2. **Long-term memory** — semantic recall over the full history, kept in a vector store (e.g. Vectra).\n\n\`\`\`ts\nconst recent = await shortTermMemory.getLast(10);\nconst relevant = await vectorStore.search(query, { topK: 5 });\n\`\`\``}
        />
        <div className="flex gap-3">
          <Avatar className="mt-0.5 size-7 shrink-0">
            <AvatarFallback className="bg-muted">
              <Sparkles className="size-3.5" />
            </AvatarFallback>
          </Avatar>
          <TypingIndicator />
        </div>
      </div>

      <PromptInput onSubmit={(v) => console.log("send:", v)} />
    </div>
  );
}
