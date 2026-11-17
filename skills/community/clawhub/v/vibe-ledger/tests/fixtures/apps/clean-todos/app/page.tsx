"use client";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function Todos() {
  const [todos, setTodos] = useState<any[]>([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    supabase.from("todos").select("*").then(({ data }) => setTodos(data ?? []));
  }, []);

  async function add() {
    await supabase.from("todos").insert({ title });
  }

  return (
    <main>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <button onClick={add}>添加</button>
      <ul>{todos.map((t) => <li key={t.id}>{t.title}</li>)}</ul>
    </main>
  );
}
