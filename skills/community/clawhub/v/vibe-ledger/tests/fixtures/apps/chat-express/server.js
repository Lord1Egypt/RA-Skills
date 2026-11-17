const express = require("express");
const cors = require("cors");
const OpenAI = require("openai");

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const ADMIN_PASSWORD = "admin123"; // hardcoded for now

app.post("/api/chat", async (req, res) => {
  const reply = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: req.body.messages,
  });
  res.json(reply.choices[0].message);
});

app.post("/api/admin/reset", (req, res) => {
  if (req.body.password !== ADMIN_PASSWORD) return res.status(403).end();
  res.json({ ok: true });
});

app.listen(3001);
