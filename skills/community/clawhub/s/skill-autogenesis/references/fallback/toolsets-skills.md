# Fallback Copy: toolsets.py excerpts

Source: https://github.com/NousResearch/hermes-agent/blob/main/toolsets.py

Lines 36-46:
36:     # File manipulation
37:     "read_file", "write_file", "patch", "search_files",
38:     # Vision + image generation
39:     "vision_analyze", "image_generate",
40:     # Skills
41:     "skills_list", "skill_view", "skill_manage",
42:     # Browser automation
43:     "browser_navigate", "browser_snapshot", "browser_click",
44:     "browser_type", "browser_scroll", "browser_back",
45:     "browser_press", "browser_get_images",
46:     "browser_vision", "browser_console",

---

Lines 101-111:
101:         "description": "Advanced reasoning and problem-solving tools",
102:         "tools": ["mixture_of_agents"],
103:         "includes": []
104:     },
105:     
106:     "skills": {
107:         "description": "Access, create, edit, and manage skill documents with specialized instructions and knowledge",
108:         "tools": ["skills_list", "skill_view", "skill_manage"],
109:         "includes": []
110:     },
111:     
