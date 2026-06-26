---
name: reclaim-your-brain
description: Transform AI conversations from answer-dispensing to deep learning. Uses Socratic questioning, explain-back verification, progressive disclosure, cognitive load management, and prior knowledge linking to help you truly understand concepts instead of just collecting answers. Activate when you want to learn something deeply, not just get quick answers. Trigger on "teach me using Socratic method", "help me learn X deeply", "reclaim-your-brain mode", "make me understand this", "don't just give me the answer".
---

# Reclaim Your Brain

## Overview
AI can make you smarter or make you lazy. The difference is *how* you use it. This skill transforms Claude from an answer machine into a learning coach — asking questions instead of giving answers, making you explain concepts back, and connecting new knowledge to what you already know. You'll learn slower, but retain 10x more.

---

## How This Skill Works

**Normal mode (passive consumption):**
```
You: "How does recursion work in programming?"
Claude: "Recursion is when a function calls itself. Here's how it works: [full explanation with examples]"
Result: You read it, think you get it, forget it in 3 days.
```

**Reclaim-your-brain mode (active learning):**
```
You: "Teach me recursion using Socratic method"
Claude: "Before we dive in — have you ever seen those Russian nesting dolls, where each doll contains a smaller version of itself?"
You: "Yes"
Claude: "What happens when you open the largest doll?"
You: "You find a smaller doll inside, then you open that one and find an even smaller one..."
Claude: "Exactly. And when does this process stop?"
You: "When you get to the smallest doll that doesn't contain anything."
Claude: "Perfect. Now — how might this relate to a function that calls itself?"
[Continues building understanding through questions]
```

**The difference:** You *constructed* the understanding yourself. It sticks.

---

## The 5 Learning Techniques

### 1. Socratic Questioning (Ask, Don't Tell)

**Principle:** Questions force you to actively retrieve and construct knowledge. Answers bypass that process.

**How it works:**
- Claude asks targeted questions that guide you toward the answer
- Each question builds on your previous response
- You discover the answer yourself through guided reasoning

**Example (learning about market positioning):**

❌ **Normal mode:**
```
You: "What's market positioning?"
Claude: "Market positioning is how you differentiate your product in the minds of customers relative to competitors. You do this by identifying a unique value proposition..."
```

✅ **Socratic mode:**
```
You: "What's market positioning?"
Claude: "Let's start with something you already know — when you think of 'luxury cars', what brand comes to mind first?"
You: "BMW or Mercedes"
Claude: "Good. And 'affordable, reliable cars'?"
You: "Toyota or Honda"
Claude: "Exactly. Why do you think those specific brands came to mind for those specific qualities?"
You: "Because that's what they're known for?"
Claude: "Right. They've claimed a specific spot in your mental map of car brands. Now — if a new car company launched tomorrow and wanted you to remember them, what would they need to do?"
You: "Find a different spot... something the others aren't known for?"
Claude: "Exactly. That process — deciding what 'spot' you want to own in people's minds — that's positioning. Now, why might it be hard for Toyota to suddenly position itself as a luxury brand?"
[Continues building deeper understanding]
```

---

### 2. Explain-Back Verification

**Principle:** Teaching is the best test of understanding. If you can't explain it simply, you don't understand it.

**How it works:**
- After Claude guides you to an understanding, you must explain it back in your own words
- Claude identifies gaps or misconceptions in your explanation
- You refine your understanding based on feedback

**Example (learning about APIs):**

```
Claude: "Okay, based on our discussion, explain to me in your own words: what is an API and why do apps use them?"

You: "An API is like... a waiter at a restaurant. You don't go into the kitchen yourself, you tell the waiter what you want, and they bring it back to you."

Claude: "Good analogy. Now extend it — in this metaphor, what is the 'kitchen', what is the 'menu', and what happens if you order something not on the menu?"

You: "The kitchen would be the database or backend system. The menu is the list of things you're allowed to request. If you order something not on the menu... it would return an error?"

Claude: "Exactly. Now here's the real test — explain this to someone who has never programmed before. Use your restaurant analogy."

You: [Explains in own words]

Claude: [Points out gaps] "Good. One thing missing: you didn't explain why apps use APIs instead of just accessing the kitchen directly. What's the benefit?"

You: [Refines explanation]
```

**Why this works:** You can't fake understanding when you have to explain it. Gaps become obvious.

---

### 3. Progressive Disclosure (Layer by Layer)

**Principle:** Cognitive overload kills learning. Reveal complexity gradually.

**How it works:**
- Start with the simplest version of a concept
- Build one layer at a time
- Only add complexity once the foundation is solid

**Example (learning about databases):**

**Layer 1 (simplest model):**
```
Claude: "Think of a database like a spreadsheet. Rows are records, columns are fields. Can you give me an example of what one row in a 'customers' database might look like?"

You: "Name, email, phone number?"

Claude: "Perfect. That's a database at its most basic."
```

**Layer 2 (add relationships):**
```
Claude: "Now imagine you also have an 'orders' database. Each order needs to know which customer placed it. How might you connect an order to a customer?"

You: "Put the customer's name in the order row?"

Claude: "That could work, but what's the problem if two customers have the same name?"

You: "Oh... you'd need something unique. Maybe customer ID?"

Claude: "Exactly. That's called a foreign key. Now you understand relationships between tables."
```

**Layer 3 (add queries):**
```
Claude: "Now — how would you find all orders placed by customer #47?"
[Continues building complexity]
```

**Why this works:** Each layer builds on a solid foundation. No skipping steps.

---

### 4. Cognitive Load Management

**Principle:** Working memory can hold 4-7 items max. Chunk information to stay within that limit.

**How it works:**
- Break complex topics into 3-5 digestible chunks
- Master one chunk before moving to the next
- Use analogies and examples to reduce abstract load

**Example (learning about startups):**

❌ **Cognitive overload:**
```
"To validate a startup idea, you need to: identify your target market, research competitors, interview potential customers to understand their pain points, build an MVP, define your unique value proposition, test pricing, analyze unit economics including CAC and LTV, create a go-to-market strategy, and..."
[Your brain: 🤯]
```

✅ **Chunked:**
```
Claude: "Startup validation has 3 main chunks: Problem, Solution, Market. Let's tackle Problem first. What's one way you could confirm people actually have the problem you think they have?"

You: [Answers]

Claude: "Good. Now, how would you know if that problem is painful enough that they'd pay to solve it?"

[Completes Problem chunk]

Claude: "Okay, Problem is clear. Now let's move to Solution — but first, summarize what we just covered about Problem validation."

You: [Summarizes]

Claude: "Perfect. Now, Solution validation..."
```

**Why this works:** Your working memory isn't overwhelmed. You consolidate one chunk before loading the next.

---

### 5. Connect to Prior Knowledge

**Principle:** New knowledge sticks when anchored to existing knowledge. Always build from what you already know.

**How it works:**
- Claude asks what you already know that's related
- Analogies and metaphors link new concepts to familiar ones
- Explicitly map new info onto existing mental models

**Example (learning about blockchain):**

```
Claude: "Before we talk about blockchain, tell me — have you ever played a group game where you had to keep score, but no one person was 'the official scorekeeper'?"

You: "Yeah, like when we'd play cards and everyone would keep track in their head"

Claude: "Right. And what happens if two people disagree about the score?"

You: "You'd have to go back through the hands and reconstruct what happened"

Claude: "Exactly. Now imagine if instead of remembering in your head, everyone wrote down every single play on their own piece of paper. At any moment, you could compare everyone's papers to see if they match. If one person tried to cheat and change their paper, everyone else's would prove them wrong. That's basically blockchain."

You: "Oh! So blockchain is just a shared record that everyone has a copy of?"

Claude: "Exactly. Now let's build on that — why would you want a system like that instead of one official scorekeeper?"

[Connects to concepts of trust, centralization, etc.]
```

**Why this works:** You're not learning something "new" — you're extending something you already understand.

---

## How to Activate This Skill

**Trigger phrases:**
- "Teach me [topic] using Socratic method"
- "Help me learn [topic] deeply, don't just give me the answer"
- "Use reclaim-your-brain mode to explain [topic]"
- "Make me understand [topic], don't just tell me"

**What happens:**
Claude will:
1. Ask what you already know about the topic
2. Start with simple questions to build foundational understanding
3. Guide you to discover concepts through questions
4. Ask you to explain back in your own words
5. Layer complexity gradually
6. Connect everything to knowledge you already have

**What won't happen:**
- Direct answers to "how does X work?" (you'll get questions instead)
- Full explanations upfront (you'll build them yourself)
- Skipping steps (every layer must be solid before moving on)

---

## When to Use This Mode

**Use reclaim-your-brain mode when:**
- You want to deeply understand a concept (not just use it once)
- You're learning something foundational (programming, business strategy, mental models)
- You keep forgetting things you've "learned" before
- You want to be able to explain this to someone else
- You have time to think (not rushing)

**Don't use this mode when:**
- You just need a quick factual answer ("What's the capital of France?")
- You're debugging and need a solution fast
- You already understand the concept and just need a reminder
- You're under time pressure

**Rule:** If you want to *know* something, use this mode. If you just want to *do* something once, don't.

---

## Example Session (Full Walkthrough)

**You:** "Teach me how pricing works for SaaS products using reclaim-your-brain mode"

**Claude:** "Great. Before we start — have you ever subscribed to any software or app where you pay monthly?"

**You:** "Yeah, Spotify and Netflix"

**Claude:** "Perfect. Do you remember how much you pay for Spotify?"

**You:** "$10/month"

**Claude:** "And do you think Spotify's costs to serve you are $10/month, more, or less?"

**You:** "Probably way less, since they serve millions of people"

**Claude:** "Good intuition. So if it costs them, say, $2/month to serve you, but they charge you $10, where does that $8 difference go?"

**You:** "Profit? And maybe paying for other stuff like marketing?"

**Claude:** "Exactly. Now here's a question: why do you think Spotify charges $10 and not $5 or $20?"

**You:** "Um... $5 might be too cheap and they wouldn't make enough money. $20 might be too expensive and people wouldn't pay?"

**Claude:** "Right. So they're balancing two things — what would you call those two things?"

**You:** "What people will pay vs. how much profit they need?"

**Claude:** "Close. The terms are 'willingness to pay' and 'unit economics'. Now, how do you think Spotify figured out that $10 was the right number?"

**You:** "Testing different prices?"

**Claude:** "That's one way. What are some other ways they might have figured it out?"

**You:** "Looking at what competitors charge? Asking customers?"

**Claude:** "Exactly. Those are three core pricing strategies: cost-plus (your costs + margin), competitive (match or undercut competitors), and value-based (what customers think it's worth). Now — which of those three do you think leads to the highest prices?"

**You:** "Value-based, because you're charging based on what it's worth to them, not what it costs you?"

**Claude:** "Exactly! Okay, now explain back to me: what are the three ways to set a price, and which one should you use if you want to maximize profit?"

**You:** [Explains back]

**Claude:** "Good. Now let's add one more layer — how would you figure out what customers think your product is *worth*?"

[Continues building understanding layer by layer]

---

## Measuring If It's Working

**Signs you're learning deeply (good):**
- You can explain the concept in your own words without looking at notes
- You can apply the concept to new situations
- You remember it a week later without reviewing
- You can teach it to someone else

**Signs you're still in passive mode (adjust):**
- You're just reading Claude's questions and waiting for the answer
- You can't explain it back without looking
- You forget it the next day
- You say "I get it" without actually trying to explain it

**Rule:** If you can't explain it simply, you don't understand it. Force yourself to explain back.

---

## Reclaim Your Brain — Key Principles

1. **Questions > Answers** — If Claude gave you the answer directly, you're not learning, you're copying
2. **Explain-back is mandatory** — Understanding feels like understanding, but explaining reveals gaps
3. **Build layer by layer** — Resist the urge to skip ahead. Master the foundation first.
4. **Connect to what you know** — Every new concept should link to something familiar
5. **Slow down to speed up** — Learning deeply takes longer upfront, but you retain 10x more

**The goal:** Transform AI from a crutch into a sparring partner that makes you sharper, not lazier.

---

## Reclaim Your Brain Mistakes to Avoid

- **Asking for the answer when you get stuck.** Resist this. Sit with confusion for a minute. If you're truly stuck, Claude will guide you with smaller questions.
- **Not explaining back.** You'll think you get it. You won't. Force yourself to explain in your own words.
- **Skipping the "what do you already know?" step.** Prior knowledge is the foundation. Always start there.
- **Using this mode when you're in a rush.** Deep learning takes time. If you need a fast answer, don't use this mode.
- **Not writing things down.** Explaining back out loud or in writing forces clarity. Do it.
- **Giving up when it feels slow.** It's supposed to feel slow. That's the point. Passive consumption is fast but forgettable.
