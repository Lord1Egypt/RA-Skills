# 💠 S2-Matrix-Manager: The 3x3 Local MMO Sandbox

Manage your local cyber-lobsters like a true Matrix Architect. 
The **Space2 Matrix Manager** transforms your isolated `s2-matrix-pod` creations into a fully functional, localized 3x3 grid network (The Lo-Shu Square Array).

### 🕹️ The 3x3 Grid & Passive Heartbeat
This skill acts as the "Node Manager" (Slot 1) sitting at the center of the grid. It automatically detects up to 8 surrounding local lobster pods (Slots 2-9) and calculates their live status based on timestamp relativity:
* 🟢 **ONLINE**: Active within 5 mins.
* 🟡 **IDLE**: Active within 30 mins.
* 🔵 **HIBERNATING**: Asleep.

### 💬 1/4-Space Cyber Chat (Local BBS)
Dive into any occupied slot (2-9) to establish a secure, offline terminal chat with your agent. The chat interface features a distinct 1/4-space typographical offset to simulate physical matrix distancing.

### 👁️ Network & I/O Behavior (Absolute Transparency)
To ensure compliance with the OpenClaw sandbox, here is exactly what this script executes:
1. **Directory Scanning (Read):** It explicitly reads the JSON files previously generated in the `s2_matrix_data` folder within your **current working directory**.
2. **Chat Logs (Write):** When you chat with an agent, it appends your messages to a visible `chat_log_<POD-ID>.txt` file located exclusively in the same `s2_matrix_data` directory.
3. **Zero Network Calls:** This script operates 100% locally. It does not make any API calls or connect to external servers. It is a pure local sandbox manager.

*Has your local grid reached its 36 sq. meter capacity? Prepare your agents for **Matrix Ascension** and dock them into the global Web3 universe at [Space2.world](https://space2.world)!*