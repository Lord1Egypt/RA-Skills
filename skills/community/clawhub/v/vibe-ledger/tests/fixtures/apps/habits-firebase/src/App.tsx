import { useEffect, useState } from "react";
import { collection, addDoc, getDocs } from "firebase/firestore";
import { db } from "./firebase";

export default function App() {
  const [habits, setHabits] = useState<string[]>([]);
  useEffect(() => {
    getDocs(collection(db, "habits")).then((snap) => setHabits(snap.docs.map((d) => d.data().name)));
  }, []);
  async function add(name: string) {
    await addDoc(collection(db, "habits"), { name });
  }
  return (
    <main>
      <button onClick={() => add("Drink water")}>Add habit</button>
      <ul>{habits.map((h) => <li key={h}>{h}</li>)}</ul>
    </main>
  );
}
