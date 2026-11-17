import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const app = initializeApp({
  apiKey: "demo-api-key",
  authDomain: "habits-demo.firebaseapp.com",
  projectId: "habits-demo",
});

export const db = getFirestore(app);
