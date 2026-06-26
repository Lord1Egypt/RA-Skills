"use client";

interface MessageBubbleProps {
  role: "user" | "coach";
  content: string;
}

function formatCoachMessage(text: string): string {
  // Convert **bold** to <strong>
  let html = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Convert *italic* to <em>
  html = html.replace(/\*(.*?)\*/g, "<em>$1</em>");
  // Convert newlines to <br>
  html = html.replace(/\n/g, "<br />");
  return html;
}

export default function MessageBubble({ role, content }: MessageBubbleProps) {
  const isCoach = role === "coach";

  return (
    <div className={`flex ${isCoach ? "justify-start" : "justify-end"} mb-4`}>
      <div
        className={`max-w-[85%] md:max-w-[70%] rounded-2xl px-5 py-3.5 text-sm leading-relaxed ${
          isCoach
            ? "bg-zinc-900 text-zinc-100 border border-zinc-800"
            : "bg-white text-black"
        }`}
      >
        {isCoach ? (
          <div
            dangerouslySetInnerHTML={{
              __html: formatCoachMessage(content),
            }}
          />
        ) : (
          <p className="whitespace-pre-wrap">{content}</p>
        )}
      </div>
    </div>
  );
}
