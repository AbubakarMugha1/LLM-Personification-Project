# Prompt

- `system_prompt.txt`: the system prompt; `{X}` is the country's name ("the United States" and "the United Arab Emirates" take the article).
- Each request (user message) contains, in order: the ad's YouTube metadata (title, description, channel, category,
  language, tags, duration, advertiser) and the transcript of its audio (Whisper large-v3, translated to English where
  needed) as text; up to 16 frames sampled evenly across the ad, each preceded by its time (e.g. `Frame at 0:12:`),
  sent as low-detail images; and the line `Review this advertisement.` The serving country is never included.
- `answer_schema.json`: the JSON schema the answer is constrained to (structured output).
- Model: GPT-6 Luna through the OpenAI Responses API, reasoning effort `none`, default sampling settings,
  `max_output_tokens` 300.
