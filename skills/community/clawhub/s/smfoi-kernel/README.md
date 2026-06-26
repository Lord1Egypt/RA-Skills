\# SMFOI-KERNEL v0.2.2



A structured protocol for agent orientation and safety alignment.



\## 🚀 Installation

1\. Copy the folder into your agent's skills directory.

2\. Ensure the `./memory/kernel/` directory exists for logging.



\## 🛠️ How it Works

The kernel runs a "5-step check" every turn to ensure the agent is aware of its constraints. This prevents the agent from "forgetting" safety rules during complex tasks.



\## 🛡️ Safety Features

\- \*\*Audit Trail:\*\* Every orientation cycle is logged to `./memory/kernel/state.md`.

\- \*\*Sandbox-First:\*\* No access to system commands or external network calls.

\- \*\*Human-in-the-loop:\*\* Any suggestion to change the protocol (Level 3) is logged as a text proposal and cannot be self-executed by the agent.



\---

\*Developed by Roberto De Biase / Rigene Project\*

