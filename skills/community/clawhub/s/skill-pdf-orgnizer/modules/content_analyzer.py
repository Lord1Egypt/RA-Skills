"""
Content Analyzer Module
Uses OpenAI GPT API or Kimi API to analyze PDF content and extract title and topic
"""

import json
import time
from openai import OpenAI
from typing import Dict, Optional, List


class ContentAnalyzer:
    """Analyzes PDF content using OpenAI GPT API or Kimi API"""

    # Standard topic categories
    STANDARD_TOPICS = [
        "Technology",
        "Finance",
        "Health",
        "Science",
        "Education",
        "Business",
        "Entertainment",
        "Politics",
        "Sports",
        "Other"
    ]

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", api_provider: str = "openai"):
        """
        Initialize content analyzer

        Args:
            api_key: API key (OpenAI or Kimi)
            model: Model to use (default: gpt-3.5-turbo for OpenAI, moonshot-v1-8k for Kimi)
            api_provider: API provider to use ("openai" or "kimi")
        """
        self.api_provider = api_provider
        self.model = model
        self.custom_topic_mappings = {}

        # Configure client based on provider
        if api_provider == "kimi":
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.moonshot.cn/v1"
            )
        else:  # OpenAI
            self.client = OpenAI(api_key=api_key)

    def set_custom_topic_mappings(self, mappings: Dict[str, str]):
        """
        Set custom topic mappings

        Args:
            mappings: Dictionary mapping specific topics to standard topics
        """
        self.custom_topic_mappings = mappings

    def analyze_content(
        self,
        text_content: str,
        metadata: Dict[str, str]
    ) -> Dict[str, any]:
        """
        Analyze PDF content to extract title, author, journal, and topic

        Args:
            text_content: Extracted text from PDF
            metadata: PDF metadata

        Returns:
            Dictionary with 'title', 'author', 'journal', 'topic', and 'subtopics'
        """
        # Use metadata title if available, otherwise analyze content
        if metadata.get('title'):
            title = metadata['title']
        else:
            title = self._extract_title(text_content)

        # Extract author from metadata if available, otherwise analyze
        author = metadata.get('author', '')
        if not author:
            author = self._extract_author(text_content)

        # Analyze topic
        topic_info = self._analyze_topic(text_content, metadata)

        # Extract journal information
        journal = self._extract_journal(text_content, metadata)

        return {
            'title': title,
            'author': author,
            'journal': journal,
            'topic': topic_info['topic'],
            'subtopics': topic_info['subtopics'],
            'confidence': topic_info.get('confidence', 0.0)
        }

    def _extract_title(self, text_content: str) -> str:
        """
        Extract title from content using GPT

        Args:
            text_content: Text from PDF

        Returns:
            Extracted title
        """
        prompt = f"""Extract the main document title from this content. Look for the paper title, which is typically found at the beginning of the document.
The title should be concise and describe the main topic of the paper.
Return ONLY the title, no additional text or explanations.

Content:
{text_content[:3000]}

Title:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts document titles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )

            title = response.choices[0].message.content.strip()
            # Clean up title
            title = title.replace('Title:', '').strip()
            title = title.replace('"', '').strip()

            return title if title else "Untitled"

        except Exception as e:
            print(f"Error extracting title: {str(e)}")
            return "Untitled"

    def _extract_author(self, text_content: str) -> str:
        """
        Extract author name from content using GPT

        Args:
            text_content: Text from PDF

        Returns:
            Extracted author name
        """
        prompt = f"""Extract the author name(s) from this document content.
If there are multiple authors, list the first author followed by "et al." for more than 3 authors.
Return only the author name(s), nothing else.

Content:
{text_content[:2000]}

Author:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts author names from documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )

            author = response.choices[0].message.content.strip()
            # Clean up author name
            author = author.replace('Author:', '').strip()
            author = author.replace('"', '').strip()

            return author if author else "Unknown_Author"

        except Exception as e:
            print(f"Error extracting author: {str(e)}")
            return "Unknown_Author"

    def _extract_journal(self, text_content: str, metadata: Dict[str, str]) -> str:
        """
        Extract journal name from content using GPT

        Args:
            text_content: Text from PDF
            metadata: PDF metadata

        Returns:
            Extracted journal name
        """
        # Check metadata first
        if metadata.get('journal'):
            return metadata['journal']

        prompt = f"""Extract the journal name, conference name, or publication venue from this document content.
If this is not from a journal/conference, return "Technical_Report" or "Preprint".
Return only the journal/conference name, nothing else.

Content:
{text_content[:2000]}

Journal/Conference:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts journal names from documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )

            journal = response.choices[0].message.content.strip()
            # Clean up journal name
            journal = journal.replace('Journal/Conference:', '').strip()
            journal = journal.replace('"', '').strip()

            return journal if journal else "Unknown_Venue"

        except Exception as e:
            print(f"Error extracting journal: {str(e)}")
            return "Unknown_Venue"

    def _analyze_topic(self, text_content: str, metadata: Dict[str, str]) -> Dict[str, any]:
        """
        Analyze the topic of the content using GPT

        Args:
            text_content: Text from PDF
            metadata: PDF metadata

        Returns:
            Dictionary with topic and subtopics
        """
        topics_list = ", ".join(self.STANDARD_TOPICS)

        system_message = f"""You are a document classifier. Your task is to analyze document content and classify it into one of these standard topics: {topics_list}

You must respond in valid JSON format with this structure:
{{
  "topic": "Primary topic (must be one of: {topics_list})",
  "subtopics": ["list of 2-4 relevant subtopics"],
  "confidence": 0.95
}}

Rules:
- The topic MUST be exactly one of the standard topics listed above
- Subtopics should be more specific categories
- Confidence should be between 0.0 and 1.0
- If unsure, classify as "Other"
"""

        user_message = f"""Classify this document into the most appropriate topic.

Document metadata:
- Title: {metadata.get('title', 'N/A')}
- Subject: {metadata.get('subject', 'N/A')}
- Page count: {metadata.get('page_count', 'N/A')}

Document content:
{text_content[:3000]}

Respond with valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=300
            )

            content = response.choices[0].message.content.strip()

            # Parse JSON response
            try:
                result = json.loads(content)

                # Validate topic is in standard list
                if result.get('topic') not in self.STANDARD_TOPICS:
                    # Try to match to a standard topic
                    result['topic'] = self._match_to_standard_topic(result.get('topic', 'Other'))

                # Apply custom mappings if configured
                topic = result.get('topic', 'Other')
                if topic in self.custom_topic_mappings:
                    result['topic'] = self.custom_topic_mappings[topic]

                return result

            except json.JSONDecodeError:
                # Fallback: try to extract topic from text
                return self._fallback_analysis(content)

        except Exception as e:
            print(f"Error analyzing topic: {str(e)}")
            return {
                'topic': 'Other',
                'subtopics': [],
                'confidence': 0.0
            }

    def _match_to_standard_topic(self, topic: str) -> str:
        """
        Match a topic to the closest standard topic

        Args:
            topic: Topic to match

        Returns:
            Closest standard topic
        """
        # Simple keyword matching
        topic_lower = topic.lower()

        keyword_mappings = {
            'technology': ['tech', 'computer', 'software', 'programming', 'ai', 'artificial intelligence',
                          'machine learning', 'digital', 'cyber', 'internet', 'app', 'data'],
            'finance': ['money', 'invest', 'bank', 'economic', 'market', 'stock', 'financial', 'budget',
                       'credit', 'debt', 'fund'],
            'health': ['health', 'medical', 'doctor', 'hospital', 'disease', 'wellness', 'fitness',
                      'nutrition', 'medicine', 'pharmaceutical'],
            'science': ['science', 'research', 'study', 'experiment', 'physics', 'chemistry', 'biology',
                       'scientific', 'lab'],
            'education': ['education', 'school', 'university', 'teaching', 'learning', 'academic',
                         'student', 'course', 'curriculum', 'classroom'],
            'business': ['business', 'company', 'corporate', 'enterprise', 'organization', 'management',
                        'startup', 'entrepreneur', 'workplace'],
            'entertainment': ['entertainment', 'movie', 'music', 'game', 'film', 'tv', 'television',
                            'celebrity', 'show', 'media'],
            'politics': ['politics', 'government', 'election', 'political', 'policy', 'democrat',
                        'republican', 'law', 'legislation'],
            'sports': ['sport', 'game', 'athlete', 'team', 'player', 'championship', 'tournament',
                     'football', 'basketball', 'soccer', 'tennis', 'baseball']
        }

        for standard_topic, keywords in keyword_mappings.items():
            if any(keyword in topic_lower for keyword in keywords):
                return standard_topic.capitalize()

        return 'Other'

    def _fallback_analysis(self, content: str) -> Dict[str, any]:
        """
        Fallback analysis when JSON parsing fails

        Args:
            content: Response content from GPT

        Returns:
            Best guess analysis
        """
        # Try to find the topic in the text
        for topic in self.STANDARD_TOPICS:
            if topic.lower() in content.lower():
                return {
                    'topic': topic,
                    'subtopics': [],
                    'confidence': 0.5
                }

        return {
            'topic': 'Other',
            'subtopics': [],
            'confidence': 0.0
        }

    def analyze_batch(
        self,
        items: List[tuple]
    ) -> List[Dict[str, any]]:
        """
        Analyze multiple PDFs with rate limiting

        Args:
            items: List of (text_content, metadata) tuples

        Returns:
            List of analysis results
        """
        results = []

        for i, (text_content, metadata) in enumerate(items):
            try:
                result = self.analyze_content(text_content, metadata)
                results.append(result)

                # Rate limiting: wait between requests
                if i < len(items) - 1:
                    time.sleep(0.5)

            except Exception as e:
                print(f"Error analyzing item {i}: {str(e)}")
                results.append({
                    'title': 'Error',
                    'topic': 'Other',
                    'subtopics': [],
                    'confidence': 0.0
                })

        return results
