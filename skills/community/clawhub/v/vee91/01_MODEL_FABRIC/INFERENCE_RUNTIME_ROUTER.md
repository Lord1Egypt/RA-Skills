# Inference Runtime Router

Treat inference engines as interchangeable execution backends. Candidate families include llama.cpp for portability/edge use and vLLM/SGLang for higher-concurrency serving, subject to current hardware and workload tests.

Select by measured workload, not reputation. Benchmark batch size, context length, KV-cache behavior, latency, memory pressure, and failure rate.
