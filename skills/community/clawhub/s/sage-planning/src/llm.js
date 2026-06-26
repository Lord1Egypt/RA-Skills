const fs = require('fs');
const path = require('path');

// Simple LLM Client for Gemini API
// Supports: google/gemini-3-pro-preview (if available), gemini-1.5-pro, gemini-pro

class LLMClient {
  constructor(apiKey) {
    this.apiKey = apiKey || process.env.GEMINI_API_KEY;
    if (!this.apiKey) {
      throw new Error("Missing GEMINI_API_KEY");
    }
    this.baseUrl = "https://generativelanguage.googleapis.com/v1beta/models";
    this.model = process.env.GEMINI_MODEL || "gemini-3-pro-preview"; // Use 3 Pro Preview if available
  }

  async generate(prompt, systemInstruction = "") {
    const url = `${this.baseUrl}/${this.model}:generateContent?key=${this.apiKey}`;
    
    const payload = {
      contents: [
        {
          role: "user",
          parts: [{ text: prompt }]
        }
      ],
      generationConfig: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 8192,
      }
    };

    if (systemInstruction) {
      // Gemini v1beta supports system_instruction at root
      // Format: { role: "system" | "user", parts: [...] }
      payload.system_instruction = {
        parts: [{ text: systemInstruction }]
      };
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`LLM API Error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      
      if (data.candidates && data.candidates.length > 0 && data.candidates[0].content) {
        return data.candidates[0].content.parts[0].text;
      } else {
        throw new Error("No content generated");
      }
    } catch (error) {
      console.error("LLM Generation Failed:", error);
      throw error;
    }
  }
}

module.exports = LLMClient;
