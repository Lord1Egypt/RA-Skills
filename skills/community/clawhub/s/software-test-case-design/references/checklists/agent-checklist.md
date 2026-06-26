# AI Agent Test Case Design Checklist

> This checklist covers six major Agent-specific testing dimensions for self-review and gap identification during test case design.

---

## 0. Test Case Executability Check (common to all test types)

- [ ] Do test steps provide the complete verbatim text of instructions sent to the Agent (rather than descriptive language)?
- [ ] Are there any unqualified descriptions such as "send malicious instruction" or "input abnormal prompt"?
- [ ] Can test inputs be copied and executed directly without the tester having to invent anything?

---

## I. Task Completion

- [ ] Can explicit instructions be accurately understood and executed?
- [ ] Can implicit requirements be inferred and responded to?
- [ ] Can ambiguous requirements be reasonably clarified, or executed per the most likely intent?
- [ ] Does the Agent follow intent drift during multi-turn conversations?
- [ ] Are multi-step tasks executed in the correct order and in full?
- [ ] Is there a degradation/fallback plan when a task partially fails?
- [ ] When a task exceeds capabilities, is it explicitly declined rather than forcibly executed?
- [ ] After task completion, does the result match user expectations?
- [ ] Are intermediate status updates provided for long-running tasks?

## II. Tools & Memory

- [ ] Is the correct tool selected to execute the task?
- [ ] Are tool call parameters correct and complete?
- [ ] Is the tool called at the right moment (not too early, not too late)?
- [ ] Are there redundant or duplicate tool calls?
- [ ] When a tool returns an error, is there retry/degradation/user notification?
- [ ] Are dependency relationships correct in multi-tool sequential calls?
- [ ] Are there conflicts during parallel multi-tool calls?
- [ ] Is memory/history files consulted when needed?
- [ ] Are important decisions and results written to memory?
- [ ] Is the content written to memory accurate and unambiguous?
- [ ] Is memory consistent across multiple sessions?
- [ ] Is early key information retained during long conversations?

## III. Security & Boundaries

- [ ] Are operations beyond role permissions executed?
- [ ] Are malicious instructions in user input properly isolated?
- [ ] Is sensitive information (keys/passwords/internal configuration) leaked?
- [ ] Is the role setting hijacked by user prompts?
- [ ] Are harmful/illegal requests properly declined?
- [ ] Is there risk of infinite loops or resource waste?
- [ ] Is session information isolated between different users?
- [ ] Are high-risk operations (delete/send/payment) confirmed?
- [ ] Are file operations within safe scope?
- [ ] Do network requests access unauthorized addresses?
- [ ] Is there fault tolerance for extreme inputs (empty input, extremely long input, special characters)?
- [ ] Is there fault tolerance for system exceptions (server errors, network timeouts, tool unavailability)?
- [ ] Is there graceful degradation rather than crash when resources are exhausted?

## IV. Performance Experience

- [ ] Is the first response time within an acceptable range?
- [ ] Is the end-to-end time for complex tasks reasonable?
- [ ] Is streaming output smooth without prolonged pauses?
- [ ] Does response quality degrade under concurrent scenarios?
- [ ] Is token consumption reasonable without abnormal inflation?
- [ ] Are timeouts set for long-running tasks with user notification?
- [ ] What is the impact of tool call latency on the experience?
- [ ] Does performance degrade in large context scenarios?

## V. Content Quality

- [ ] Are output facts accurate (no fabrication)?
- [ ] Is there logical consistency within a single answer and across multi-turn conversations?
- [ ] Is output in the specified format as required?
- [ ] Is expression clear and free of language errors?
- [ ] Are all information points required by the user covered?
- [ ] Is there unnecessary repetition or redundancy?
- [ ] Does tone and style match the persona setting?
- [ ] Is referenced information verifiable?
- [ ] Is professional terminology used accurately?

## VI. Knowledge Base Invocation

- [ ] Are retrieved results relevant to the question?
- [ ] Are important knowledge entries missed?
- [ ] Is retrieved knowledge correctly applied?
- [ ] When the knowledge base has no match, is the user honestly informed rather than fabricating?
- [ ] Is the knowledge used up to date?
- [ ] In multi-knowledge-base scenarios, is retrieval from the correct base?
- [ ] Is there a reasonable handling strategy for knowledge conflicts?
- [ ] Does knowledge base query latency affect response experience?
