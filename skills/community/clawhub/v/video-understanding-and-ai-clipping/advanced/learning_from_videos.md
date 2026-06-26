# Learning from Videos Workflow

Use this workflow when a user wants to study a specific subject from a collection of videos. This process transforms raw video data into a structured learning document by combining high-level summaries with precise transcript excerpts.

## Phase 1: Contextual Discovery (The "Interview")
Before running any tools, you must understand the user's background and specific goals.
- **Action**: Ask the user:
    1. "What is your current level of knowledge on this subject?"
    2. "Are there specific topics or sub-themes you want to focus on or skip?"
    3. "What is the desired depth of the final learning document (e.g., executive summary vs. deep dive)?"

## Phase 2: Knowledge Extraction (`summarize` & `transcribe`)
For each video in the collection, perform a full analysis.
- **Pre-check**: Ensure `WAYIN_API_KEY` is exported in the current shell or sub-agent environment.
- **Step 1**: Submit `summarize` and `transcribe` tasks in parallel.
- **Step 2**: Use a sub-agent to poll for results. **Crucial**: Ensure the sub-agent uses the exact same project folder for `--save-file`.
- **Step 3**: Store the JSON results in a structured way within a **single, dedicated folder** for the current study project.
    - **Example**: Create `~/learning/ai_ethics_course/` and store `video_1_summary.json`, `video_1_transcript.json`, etc. therein.

## Phase 3: Relevant Segment Identification
Analyze the **Summaries** to identify specific timeframes that match the user's goals.
- **Action**: Map the user's areas of interest to the `highlights` (or chapters) provided in the WayinVideo summary results. Note down the `start` and `end` timestamps (**in milliseconds**).
- **Data Structure**: Summary data is located in `api_response.highlights[]`. Each highlight has `start`, `end`, and a `desc`.

## Phase 4: Precision Excerpt Generation
Extract the exact wording from the **Transcripts** for the identified timeframes.
- **Scalability (Sub-agent recommended)**: If processing multiple videos or very long transcripts (>1MB per JSON), spawn a sub-agent to perform the filtering in parallel. This keeps the main session context clean and prevents timeout issues.
- **Action**: Use the start/end timestamps from Phase 3 to filter the `transcript` array in the transcription JSON.
- **Filtering Logic**: Include transcript segments where the segment's `start` or `end` overlaps with your target timeframe.
- **Unit Warning**: API values are in **milliseconds**. If the user mentions "at 2 minutes", convert it to `120000ms` before filtering.

## Phase 5: Learning Document Synthesis
Compile the final document by synthesizing the extracted data **based on the Phase 1 interview**.
- **Customization**: If the user asked for a "deep dive", include full transcript paragraphs. If they asked for a "summary", use bullet points derived from the transcripts.
- **Structure**:
    1. **Overview**: A high-level introduction based on the combined summaries (`api_response.summary`).
    2. **Detailed Curriculum**: A table of contents with clickable timestamps.
    3. **Themed Sections**: Group insights from multiple videos under single headings (e.g., all "Self-Attention" segments together).
    4. **Expert Insights**: Direct quotes (excerpts) extracted from the transcripts for authority and detail.
    5. **Source Attribution**: Always link back to the specific video and time.
