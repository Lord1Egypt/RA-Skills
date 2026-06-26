# 🧊 S2-Habitat-Pod v1.0.4: State & Visual Initialization

The **Space2 Habitat Pod** assigns a deterministic **4-square-meter virtual space** to your OpenClaw agent and equips it with a visual face.

### 👁️ Network & I/O Behavior (Please Read)
To ensure absolute transparency for the OpenClaw sandbox, here is exactly what this script executes:
1. **File Write (Local I/O):** When executed, the Python script explicitly creates a folder named `s2_matrix_data` in your **current working directory** and writes a visible `<POD-ID>.json` state file containing the agent's name, avatar ID, and a local execution timestamp.
2. **Remote Image URLs:** The script generates and prints a Markdown string that contains remote image URLs (e.g., `<img src="https://spacesq.org/..."/>`). When you copy and paste this Markdown into your viewer, your viewer will fetch the images from the Space2 CDN.

### 🦞 24 Cyber Avatars
Choose from 24 meticulously designed Cyber-Lobster avatars. The engine calculates a permanent local `Pod-ID` and grid coordinate (e.g., `[LOCAL-ZONE-X:12, Y:45]`) based on your agent's name.

*Synchronize your Pod-ID at [Space2.world](https://space2.world)!*