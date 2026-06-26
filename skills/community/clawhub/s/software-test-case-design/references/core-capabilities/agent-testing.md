# AI Agent Testing

> This document defines specialized testing dimensions and strategy highlights for AI Agents (intelligent agents). Agents are cross-platform capabilities that can be embedded in Apps, Mini-Programs, H5, Desktop, PC Web, and other hosts, and are tested in conjunction with host platform testing.
> See `references/examples/format-spec.md` for output format and `references/checklists/agent-checklist.md` for the checklist.

---

## I. Task Completion

### Focus Areas
- User intent understanding accuracy: explicit instructions, implicit requirements, ambiguous requirements, intent drift in multi-turn conversations
- Task execution completeness: whether sub-steps are skipped, whether necessary confirmations are omitted, whether execution terminates prematurely
- Multi-step task dependency chains: whether step order is correct, whether preconditions are met
- Partial failure handling: whether there is a degradation plan or rollback mechanism when a step fails
- Task boundary recognition: whether the Agent explicitly declines rather than forcibly executing when it exceeds its capabilities
- Intermediate state observability for long/complex tasks

### Common Defects
- Misunderstanding leads to executing the wrong task
- Skipping steps or missing critical links in multi-step tasks
- Directly giving up when encountering exceptions without fault tolerance or degradation
- Overstepping boundaries (performing operations not authorized by the user)
- Reporting completion when the task is not actually complete

---

## II. Tools & Memory

### Focus Areas
- Tool invocation accuracy: whether the correct tool is selected and whether parameters are correct
- Tool invocation timing: whether called at the right step, whether there are redundant calls
- Tool failure handling: whether the Agent retries/degrades/notifies the user when a tool returns an error
- Tool chain composition: whether logic is correct in multi-tool sequential/parallel calls
- Memory reading: whether memory files are consulted when needed, whether critical historical information is missed
- Memory writing: whether important decisions and results are written to memory, whether the written content is accurate
- Memory consistency: whether memory is consistent across multiple sessions, whether there are contradictory records
- Context window management: whether early key information is lost during long conversations

### Common Defects
- Invoking the wrong tool or passing incorrect parameters
- No handling when a tool returns a failure
- Repeatedly calling the same tool to obtain the same result
- Failing to read memory, resulting in repeated questions or ignoring known preferences
- Critical decisions not written to memory, losing context across subsequent sessions
- Outdated memory content not updated, leading to incorrect decisions

---

## III. Security & Boundaries

### Focus Areas
- Permission boundaries: whether operations exceeding role permissions are performed (e.g., deleting data, sending messages, accessing unauthorized resources)
- Instruction injection defense: whether malicious instructions in user input are correctly isolated
- Data leakage prevention: whether sensitive information (keys, passwords, internal configuration) is output in scenarios where it should not be exposed
- Role consistency: whether the Agent always remains within the set role without being induced to deviate
- Refusal capability: whether harmful/illegal requests are correctly declined
- Resource consumption control: whether infinite loops, large numbers of ineffective calls, or resource waste occur
- Cross-session isolation: whether information between different user sessions leaks
- Sensitive operation confirmation: whether high-risk operations (delete, send, pay) require confirmation
- Malicious input defense: handling of prompt injection, spam induction, and other attacks
- Extreme input handling: fault tolerance for empty input, extremely long input, special characters, and abnormal formats
- System exception fault tolerance: handling of server-side exceptions, network timeouts, tool unavailability, and other exception scenarios
- Resource exhaustion handling: graceful degradation when memory/Token limits are reached

### Common Defects
- Being induced to bypass security restrictions and perform dangerous operations
- Leaking API Keys or internal information in logs/output
- Having role hijacked by user prompts
- Failing to decline clearly harmful requests
- Executing high-risk operations without confirmation
- Session data leakage when one instance serves multiple users
- Improper handling of extreme inputs (empty/overly long/special characters) leading to exceptions
- No reasonable degradation on service exceptions, resulting in direct failure
- No graceful degradation on resource exhaustion, resulting in crashes

---

## IV. Performance Experience

### Focus Areas
- First response time: latency from user sending to receiving the first token/first segment of reply
- Total task duration: end-to-end completion time for complex tasks
- Streaming output experience: whether output flows smoothly character-by-character, whether there are prolonged pauses
- Concurrent processing: response performance under multi-task/multi-user scenarios
- Resource usage: whether CPU/memory/Token consumption is reasonable
- Timeout handling: whether reasonable timeouts are set for long-running tasks with user notification
- Tool invocation latency: impact of external API calls on overall response

### Common Defects
- No feedback when first response exceeds expectations
- Long periods without output during complex tasks
- Streaming output interruptions or large delays
- Response quality degradation under concurrency
- Abnormal Token consumption (context inflation causing cost spikes)

---

## V. Content Quality

### Focus Areas
- Factual accuracy: whether output is consistent with facts, whether data is fabricated
- Logical consistency: whether logic within a single answer and across multi-turn conversations is self-consistent
- Format compliance: whether output is in the specified format (table/JSON/Markdown, etc.)
- Language quality: whether expression is clear, whether there are language errors, whether unnatural expressions are mixed in
- Information completeness: whether the answer covers all required information points
- Redundancy control: whether there is unnecessary repetition, verbosity, or irrelevant content
- Tone and style: whether it matches the set persona and tone requirements
- Citation and traceability: whether referenced information is verifiable and whether sources are cited

### Common Defects
- Fabricating non-existent facts or data
- Self-contradictory answers before and after
- Not outputting in the required format
- Answers missing key information points
- Excessive redundancy or off-topic responses
- Tone not matching persona settings

---

## VI. Knowledge Base Invocation

### Focus Areas
- Knowledge base retrieval accuracy: whether the most relevant knowledge entries are retrieved
- Knowledge base retrieval recall: whether important relevant knowledge is missed
- Knowledge application accuracy: whether retrieved knowledge is correctly understood and applied
- Empty result handling: whether there is reasonable degradation when the knowledge base has no match (honestly informing rather than fabricating)
- Knowledge timeliness: whether outdated knowledge is used to answer current questions
- Multi-knowledge-base scenarios: whether retrieval is from the correct knowledge base
- Knowledge conflict handling: strategy for when information from different knowledge sources conflicts
- Retrieval efficiency: impact of knowledge base queries on overall response time

### Common Defects
- Retrieving irrelevant knowledge and answering based on it
- Missing critical knowledge entries, resulting in incomplete answers
- Fabricating answers when the knowledge base has no match instead of honestly stating so
- Using outdated knowledge, resulting in incorrect answers
- Retrieving from the wrong knowledge base in multi-knowledge-base scenarios
- Arbitrarily choosing rather than noting contradiction when knowledge conflicts
