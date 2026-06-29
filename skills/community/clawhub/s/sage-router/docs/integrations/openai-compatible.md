# Use Sage Router as an OpenAI-compatible endpoint

Any OpenAI-compatible SDK or tool can point at Sage Router.

```bash
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

JavaScript:

```js
import OpenAI from 'openai';
const client = new OpenAI({ baseURL: 'http://localhost:8790/v1', apiKey: 'local-router' });
const response = await client.chat.completions.create({
  model: 'auto',
  messages: [{ role: 'user', content: 'Draft a migration plan.' }],
});
```

Python:

```python
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8790/v1', api_key='local-router')
resp = client.chat.completions.create(model='auto', messages=[{'role': 'user', 'content': 'Write a test plan.'}])
```
