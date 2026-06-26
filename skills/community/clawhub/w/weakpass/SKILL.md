---
name: weakpass
slug: weakpass
version: 1.0.0
description: Search hashes through 25 billion leaked passwords using the Weakpass API (no API key required).
homepage: https://weakpass.com/
author: ibnaleem
repository: https://github.com/ibnaleem/weakpass-skill
license: GPL-3.0
changelog: "Initial release"
metadata: {"openclaw":{"requires":{"bins":["curl"]},"os":["linux","darwin","win32"]}}
---

# Weakpass

One primary service, no API keys needed.

## API References:

- https://weakpass.com/openapi.json
- https://weakpass.com/openapi.yaml
- https://weakpass.com/api

Use the API references when you're stuck. Try the json reference before trying others.

## Searching Hashes

Search supplied hash in the database. You do not need to specify exact hash type.

Required arg: hash

Hash must have size between 32 and 64 characters and contains only next chars - [A-Fa-f0-9]

JSON:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/search/12345678902dd833fc9db9d72e9483c5.json' -H 'accept: application/json'
# Output: { "type": "md5", "hash": "12345678902dd833fc9db9d72e9483c5", "pass": "4kgdjv1"}
```

Text/plain:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/search/12345678902dd833fc9db9d72e9483c5.txt' -H 'accept: text/plain'
# Output: md5;12345678902dd833fc9db9d72e9483c5;4kgdjv1
```

## Searching Ranges

Retrieve a list of hash-password pairs based on a specific prefix.

Required arg: hash prefix
Optional args:
- filter: ["hash", "pass"]
- type: ["md5", "ntlm", "sha1", "sha256"]

Hash prefix must have size between 6 and 64 characters and contains only next chars - [A-Fa-f0-9]

If the hash filter is selected, it will return only hashes in the range of the hash prefix

If the pass filter is selected, it will return only passwords in the range of the hash prefix

Get hash-password pairs with a hash prefix range in JSON:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.json' -H 'accept: application/json'
# Output: [{"hash": "f2df2a00138a4f18bb49a8f16bc51dbd","pass": "m6o6veja5y"},{"hash":"f2df2a003215c2063f56f4dccd4a94b6","pass": "viDushiBhaDana"},{...}]
```

Get hash-password pairs with a hash prefix range in text/plain:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.txt' -H 'accept: text/plain'
# Output: 
#         f2df2a00138a4f18bb49a8f16bc51dbd:m6o6veja5y
#         f2df2a003215c2063f56f4dccd4a94b6:viDushiBhaDana
#         f2df2a0063a32dc7e3c8ec9fb7a0328c:Carbel@
#         ...
```

Get hash-password pairs with a hash prefix range and a hash type in JSON:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.json?type=sha1' -H 'accept: application/json'
# Output: [{"hash": "f2df2a0059611f885f7c98eafcf70d9440f4166c","pass": "a`7^x"},{"hash":"f2df2a014638901607ec9570815bb9d25c0dccea","pass": "6984egon"},{...}]
```

Get hash-password pairs with a hash prefix range and a hash type in text/plain:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.txt?type=sha1' -H 'accept: text/plain'
# Output:
#         f2df2a0059611f885f7c98eafcf70d9440f4166c:a`7^x
#         f2df2a014638901607ec9570815bb9d25c0dccea:6984egon
#         f2df2a03cf01794e5171a94f7739fb9ccc060d2b:MelBay
#         ...
```

Get hashes with a hash prefix range and a filter for hashes in JSON:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.json?filter=hash' -H 'accept: application/json'
# Output: [{"hash": "f2df2a00138a4f18bb49a8f16bc51dbd"},{"hash": "f2df2a003215c2063f56f4dccd4a94b6"},{...}]
```

Get hashes with a hash prefix range and a filter for hashes in text/plain:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.txt?filter=hash' -H 'accept: text/plain'
# Output:
#         f2df2a00138a4f18bb49a8f16bc51dbd
#         f2df2a003215c2063f56f4dccd4a94b6
#         f2df2a0063a32dc7e3c8ec9fb7a0328c
#         ...
```

### Combining Filters and Types

You can combine filters and types together.

Get hashes with a hash prefix range, a filter for hashes, and a hash type in JSON:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.json?filter=hash&type=sha1' -H 'accept: application/json'
# Output: [{"hash": "f2df2a0059611f885f7c98eafcf70d9440f4166c"},{"hash": "f2df2a014638901607ec9570815bb9d25c0dccea"},{...}]
```

Get hashes with a hash prefix range, a filter for hashes, and a hash type in text/plain:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.txt?filter=hash&type=sha1' -H 'accept: text/plain'
# Output:
#         f2df2a0059611f885f7c98eafcf70d9440f4166c
#         f2df2a014638901607ec9570815bb9d25c0dccea
#         f2df2a03cf01794e5171a94f7739fb9ccc060d2b
#         ...
```

Get passwords with a hash prefix range, a filter for passwords, and a hash type in JSON:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.json?filter=pass&type=sha1' -H 'accept: application/json'
# Output: [{"pass": "a`7^x"},{"pass": "3"},{"pass":"MelBay"}. {"pass":"KORESSA3790"}, {...}]
```

Get passwords with a hash prefix range, a filter for passwords, and a hash type in text/plain:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/range/f2df2a.txt?filter=pass&type=sha1' -H 'accept: text/plain'
# Output:
#         a`7^x
#         6984egon
#         MelBay
#         ...
```

## Generating Wordlists

Generate wordlist for a certain words based on specific hashcat rules

Required args:

- word: the word to generate a wordlist on using the specified hashcat rules

- set: [
  "online.rule", "top_3000.rule", "top_1500.rule", "top_750.rule", "top_500.rule", "top_250.rule", 
  "nsa_64.rule", "numbers.rule", "numbers100.rule", "years_1900_2025.rule", "years.rule", "symbols.rule"
  ]

- type: ["txt", "json"]


Generate a wordlist of the word "myword" with a rule set "online.rule" using type "txt":
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/generate/myword?set=online.rule&type=txt' -H 'accept: text/plain'
# Output:
#         myword
#         Myword
#         MYWORD
#         ...
```

Generate a wordlist of the word "myword" with a rule set "top_3000.rule" using type "json":
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/generate/myword?set=top_3000.rule&type=json' -H 'accept: text/plain'
# Output: ["myword","yword","word","rd","ord","ywordm","wordmy","myword1","d","drowym",...]
```

Yes, even though the type is json, the header is still `'accept: text/plain'`.

## Getting Wordlists

Retrieve available wordlists on Weakpass or get wordlists data in chunks of specified size.

Getting available wordlists:
```bash
curl -X 'GET' 'https://weakpass.com/api/v1/wordlists' -H 'accept: application/json'
# Output: 
#         10_million_password_list_top_10000.txt
#         hashmob.net.small.found.txt
#         ignis-10K.txt
#         nsa64.rule
#         rockyou.txt
```

Getting wordlist/rule data in chunks

Required arg:

wordlist: ["10_million_password_list_top_10000.txt", "hashmob.net.small.found.txt", "ignis-10K.txt", "nsa64.rule", "rockyou.txt"]

```bash
curl -X 'GET' 'https://weakpass.com/api/v1/wordlists/10_million_password_list_top_10000.txt' -H 'accept: text/plain'
# Output: [file]
```