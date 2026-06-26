# WeryAI Chat API

Use this file when you need the exact public contract for the WeryAI chat endpoints wrapped by this skill.

## Endpoints

- `POST /v1/chat/completions`
  - OpenAI-compatible chat completions shape
  - required body: `model`, `messages`
  - common optional fields: `max_tokens`, `temperature`, `top_p`, `presence_penalty`, `frequency_penalty`, `seed`, `n`
- `GET /v1/chat/models`
  - returns model metadata directly as `{ "models": [...] }`
  - includes `model`, `desc`, `max_tokens`, `input_price`, `output_price`

## Notes

- The models endpoint is not wrapped in the standard `status/desc/message/data` envelope.
- The docs currently say `stream` is not supported yet.
- Use this skill for general assistant chat, not specialized blog/email/social writing.
