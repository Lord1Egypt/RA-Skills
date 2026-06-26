# Smallest AI — Voice Catalog (Lightning v3.1)

## English

| Voice ID   | Gender | Style                | Accent   | Best For                         |
|------------|--------|----------------------|----------|----------------------------------|
| sophia     | Female | Neutral, clear       | American | General use (default)            |
| robert     | Male   | Professional         | American | Professional, reports (default)  |
| zara       | Female | Conversational       | American | Casual, friendly                 |
| melody     | Female | Warm, expressive     | American | Storytelling, greetings          |
| stella     | Female | Expressive, warm     | American | Narration, reading               |
| edward     | Male   | Professional         | British  | Formal, authoritative            |
| brooke     | Female | Conversational       | American | Casual updates                   |

## Hindi / Bilingual

| Voice ID   | Gender | Style              | Accent     | Best For                       |
|------------|--------|--------------------|------------|--------------------------------|
| advika     | Female | Natural, clear     | Indian     | Hindi content, code-switching  |
| vivaan     | Male   | Conversational     | Indian     | Bilingual English/Hindi        |
| arjun      | Male   | Professional       | Indian     | English/Hindi bilingual        |
| aisha      | Female | Warm               | Indian     | Hindi content                  |

## Spanish

| Voice ID   | Gender | Style              | Accent        | Best For                    |
|------------|--------|--------------------|---------------|-----------------------------|
| camilla    | Female | Natural            | Mexican/Latin | Spanish content              |
| carlos     | Male   | Professional       | Mexican/Latin | Spanish content              |
| luis       | Male   | Conversational     | Mexican/Latin | Casual Spanish               |

## Tamil

| Voice ID   | Gender | Style              | Accent     | Best For                    |
|------------|--------|--------------------|------------|-----------------------------|
| anitha     | Female | Natural            | Tamil      | Tamil content                |
| raju       | Male   | Conversational     | Tamil      | Tamil content                |

80+ more voices available. Fetch the full list via API:
```bash
curl -s "https://api.smallest.ai/waves/v1/lightning-v3.1/get_voices" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" | python3 -m json.tool
```

## Voice Selection Tips

- **Default/neutral**: Use `sophia` when unsure
- **Male default**: Use `robert` for general male voice
- **Briefings & reports**: Use `robert` or `edward` for authoritative tone
- **Friendly updates**: Use `melody` or `zara` for warmth
- **Hindi content**: Use `advika` (female) or `vivaan` (male)
- **Spanish content**: Use `camilla` (female) or `carlos` (male)
- **Speed adjustment**: Professional content at 1.0x, casual at 1.1-1.3x

## Voice Cloning

Available on Basic plan ($5/mo) and above. Requires only 5 seconds of reference audio.

Create custom voices via the Smallest AI console:
https://waves.smallest.ai

## Sample Rate Guide

| Sample Rate | Quality     | File Size | Best For                          |
|-------------|-------------|-----------|-----------------------------------|
| 8000 Hz     | Phone       | Smallest  | IVR, telephony, voice bots        |
| 16000 Hz    | Standard    | Small     | Voice assistants, transcription    |
| 24000 Hz    | High        | Medium    | General use, voice notes (default) |
| 44100 Hz    | Studio      | Large     | Podcasts, audiobooks, production   |
