[features]
multi_agent = true
enable_fanout = true

[agents]
max_threads = 6
max_depth = 1

[agents.<agent_id>]
config_file = "./agents/<agent_id>.toml"
