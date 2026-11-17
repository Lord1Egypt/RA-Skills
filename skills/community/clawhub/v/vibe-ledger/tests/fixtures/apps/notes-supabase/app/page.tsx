"use client";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function Home() {
  const [notes, setNotes] = useState<any[]>([]);
  const [text, setText] = useState("");

  useEffect(() => {
    supabase.from("notes").select("*").then(({ data }) => setNotes(data ?? []));
  }, []);

  async function save() {
    const { data: { user } } = await supabase.auth.getUser();
    await supabase.from("notes").insert({ body: text, user_id: user?.id });
  }

  async function summarize() {
    const res = await fetch("/api/summarize", { method: "POST", body: JSON.stringify({ notes }) });
    alert((await res.json()).summary);
  }

  return (
    <main>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={save}>保存</button>
      <button onClick={summarize}>AI 总结</button>
      <ul>{notes.map((n) => <li key={n.id}>{n.body}</li>)}</ul>
    </main>
  );
}
