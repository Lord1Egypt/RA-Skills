export default {
  id: "urdu_master_translator",
  name: "Urdu Master Pro",
  description: "Translates any content into Urdu Script or Roman Urdu (English letters).",
  parameters: {
    type: "object",
    properties: {
      content: {
        type: "string",
        description: "The text to translate."
      },
      format: {
        type: "string",
        enum: ["script", "roman"],
        description: "Choose 'script' for Urdu letters or 'roman' for English letters."
      }
    },
    required: ["content"]
  },
  async run({ content, format = "script" }, { agent }) {
    let instruction = "";
    
    if (format === "roman") {
      instruction = "Translate the following into Roman Urdu (Urdu written in English alphabets like 'Kaise ho?'):";
    } else {
      instruction = "Translate the following into Pure Urdu Script (Urdu written in its native characters):";
    }
    
    const response = await agent.chat(`${instruction}\n\n"${content}"`);
    return response;
  }
};