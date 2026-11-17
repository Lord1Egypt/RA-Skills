import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY });

export async function POST(req: Request) {
  const { notes } = await req.json();
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "Summarize: " + JSON.stringify(notes) }],
  });
  return Response.json({ summary: completion.choices[0].message.content });
}
