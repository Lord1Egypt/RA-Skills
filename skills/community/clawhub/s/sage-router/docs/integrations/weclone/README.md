# WeClone v14.3 Ollama bridge checkpoint

Sage Router provider: `weclone-cyber`  
Model: `weclone:v14.3`  
Umbrel tunnel endpoint: `http://[::1]:11435`  
Cyber bridge endpoint: `http://127.0.0.1:11435`  
Cyber adapter endpoint: `http://127.0.0.1:8003`

Runtime path:

1. Sage Router receives `model: "weclone"` or `model: "weclone-cyber/weclone:v14.3"`.
2. Provider `weclone-cyber` calls the Ollama-compatible bridge at `/api/chat`.
3. Bridge forwards to WeClone HTTP adapter `/infer`.
4. Adapter loads `/workspace/weclone_releases/v14_3_20260510/adapter`.

Verified smoke:

- `weclone`, `sage-router/weclone`, `weclone-cyber/weclone:v14.3`, and `weclone:v14.3` route to `weclone-cyber/weclone:v14.3`.
- Production candidate metrics: paraphrase `20/20`, stress `30/30`, refusal rows `7/7`, hallucinations `0`.

`Modelfile` is a checkpoint/documentation artifact. The active deployment is the HTTP bridge, not a native Ollama converted model.
