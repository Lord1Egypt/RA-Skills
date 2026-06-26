\---

name: random-fact

description: "Share a random interesting fact about science, history, or everyday life"

version: 1.0.0

author: hahg199

tags:

&#x20; - fun

&#x20; - fact

&#x20; - trivia

\---



\## Description

This skill provides a random interesting fact when asked. No external APIs or data fetching – all facts are hardcoded in the instructions.



\## Instructions

When user asks for a fact (e.g., "tell me a fact", "give me a random fact", "surprise me"), randomly select one fact from the list below and output it as a single sentence.



\### Fact list (pick one at random):

\- A day on Venus is longer than a year on Venus.

\- Octopuses have three hearts.

\- Bananas are berries, but strawberries are not.

\- Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs.

\- There are more stars in the universe than grains of sand on all Earth's beaches.

\- The Eiffel Tower can grow more than 6 inches in summer due to heat expansion.

\- A group of flamingos is called a "flamboyance".

\- The average cloud weighs about 1.1 million pounds.

\- Octopus blood is blue because it contains copper instead of iron.

\- Cows have best friends and become stressed when separated from them.



\## Examples

\*\*User:\*\* "Tell me a fact"

\*\*AI:\*\* "A day on Venus is longer than a year on Venus."



\*\*User:\*\* "Give me a random fact"

\*\*AI:\*\* "Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs."



\## Edge Cases

\- If user asks repeatedly, always give a different random fact (avoid repeating in short sequence).

\- If user asks for fact about a specific topic, politely say "I only have general random facts. Would you like one anyway?"



\## Notes for AI

\- No external calls needed.

\- Just output the fact, no extra commentary unless user asks.

