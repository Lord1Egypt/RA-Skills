# Skill Security Notes

The standalone skill:

- resolves an API key from documented env/config paths
- calls the diarize REST API with `curl`
- uses `jq` for JSON parsing

It does not modify host networking, install proxies, or execute privileged commands.
