import os
import time
import logging
from google import genai
from google.genai import types

from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an expert YouTube video summarizer.
Please analyze the provided video transcript or video audio and provide a detailed summary.

Your response MUST:
1. Be written in highly readable, well-structured Markdown.
2. Include both **English** and **Chinese** translations.
3. Contain the following sections:
   - **Key Takeaways (核心要点)**: 3 to 5 bullet points of the most important takeaways.
   - **Detailed Summary (详细总结)**: A comprehensive paragraph or list explaining the content in depth.
   - **Timestamps / Structure (内容结构)** (if applicable / inferable): High-level flow of the video.

Ensure your tone is objective and informative.
"""

def get_gemini_client():
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        raise ValueError("Please set your GEMINI_API_KEY in config.py")
    return genai.Client(api_key=GEMINI_API_KEY)

def summarize_text(text: str) -> str:
    """Summarizes a text transcript using Gemini 1.5 Flash."""
    client = get_gemini_client()
    
    prompt = f"Here is the transcript of a YouTube video:\n\n{text}\n\nPlease summarize it."
    
    logger.info("Sending text to Gemini 1.5 Flash for summarization...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
        )
    )
    return response.text

def summarize_audio(file_path: str) -> str:
    """Summarizes an audio file using Gemini API."""
    client = get_gemini_client()
    
    logger.info(f"Uploading audio file {file_path} to Gemini...")
    uploaded_file = client.files.upload(file=file_path)
    
    # Wait for file processing to complete
    logger.info(f"Waiting for audio file processing: {uploaded_file.name}")
    try:
        while True:
            file_info = client.files.get(name=uploaded_file.name)
            if file_info.state == 'ACTIVE':
                break
            elif file_info.state == 'FAILED':
                raise RuntimeError(f"File processing failed for {uploaded_file.name}")
            logger.info("Processing... sleeping 5 seconds.")
            time.sleep(5)
            
        logger.info("Audio ready. Sending prompt to Gemini...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                uploaded_file,
                "Please analyze this audio recording of a YouTube video and summarize it."
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
            )
        )
        return response.text
        
    finally:
        # Clean up file from Gemini storage
        try:
            logger.info(f"Deleting uploaded file {uploaded_file.name}")
            client.files.delete(name=uploaded_file.name)
        except Exception as e:
            logger.error(f"Failed to delete file from Gemini: {e}")

def summarize_content(content: dict) -> str:
    """
    Takes the output dictionary from extractor.py and routes it to
    the correct summarization method.
    """
    if not content or 'type' not in content:
        return "Error: No valid content provided."

    try:
        if content['type'] == 'text':
            return summarize_text(content['data'])
        elif content['type'] == 'audio':
            return summarize_audio(content['data'])
        else:
            return f"Error: Unknown content type {content['type']}"
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return f"Error during AI summarization: {e}"
