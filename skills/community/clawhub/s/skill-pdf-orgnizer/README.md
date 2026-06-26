# PDF Organizer

An intelligent PDF organization tool that uses AI to automatically categorize and organize your PDF files into structured folders based on their topic.

## Features

- **AI-Powered Analysis**: Uses OpenAI's GPT to understand PDF content and extract titles and topics
- **Automatic Organization**: Creates topic-based folders (Technology, Finance, Health, Science, Education, Business, Entertainment, Politics, Sports, Other)
- **Subtopic Support**: Creates subfolders for more granular organization
- **Incremental Processing**: Only processes new or modified files
- **Dry Run Mode**: Preview changes without actually moving files
- **Batch Processing**: Efficiently process multiple PDFs at once
- **File Conflict Resolution**: Automatically handles filename conflicts
- **Detailed Logging**: Tracks all file movements for audit trail

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Open `config.json` and configure the following settings:

```json
{
  "openai_api_key": "your-actual-api-key-here",
  "input_folder": "./input_pdfs",
  "output_folder": "./organized_pdfs",
  "model": "gpt-3.5-turbo",
  "dry_run": false,
  "incremental": true,
  "max_chars": 10000,
  "custom_topics": {
    "Artificial Intelligence": "Technology",
    "Machine Learning": "Technology"
  }
}
```

### Configuration Options

- **openai_api_key**: Your OpenAI API key (required)
- **input_folder**: Folder containing PDFs to organize
- **output_folder**: Destination folder for organized PDFs
- **model**: GPT model to use (default: gpt-3.5-turbo)
- **dry_run**: Preview mode without moving files (true/false)
- **incremental**: Only process new/modified files (true/false)
- **max_chars**: Maximum characters to analyze from each PDF
- **custom_topics**: Custom topic mappings

## Usage

### Basic Usage

1. Place your PDF files in the `input_pdfs` folder (or your configured input folder)

2. Run the organizer:
```bash
python pdf_organizer.py
```

### Dry Run Mode

Preview the organization without actually moving files:
```bash
python pdf_organizer.py --dry-run
```

### Custom Configuration

Use a different configuration file:
```bash
python pdf_organizer.py --config my_config.json
```

## How It Works

1. **PDF Reading**: Extracts text content from each PDF file
2. **AI Analysis**: Sends the content to OpenAI's GPT to identify:
   - Document title
   - Primary topic
   - Subtopics
3. **Folder Organization**: Creates topic-based folders and subfolders as needed
4. **File Movement**: Moves PDFs to their appropriate folders with descriptive filenames

## Standard Topics

PDFs are automatically classified into one of these categories:

- Technology
- Finance
- Health
- Science
- Education
- Business
- Entertainment
- Politics
- Sports
- Other

## Project Structure

```
skill_PDF_orgnizer/
├── pdf_organizer.py          # Main entry point
├── requirements.txt          # Python dependencies
├── config.json              # Configuration file
├── modules/
│   ├── pdf_reader.py       # PDF text extraction
│   ├── content_analyzer.py  # OpenAI GPT integration
│   ├── folder_manager.py    # Folder creation and management
│   └── file_mover.py        # File operations
└── README.md                # This file
```

## Example Output

```
============================================================
PDF Organizer - Starting
============================================================

Found 5 PDF file(s) to process

[1/5] Processing: research_paper.pdf
  Title: Advances in Artificial Intelligence
  Topic: Technology
  Subtopics: Machine Learning, Deep Learning
  Destination: Technology/Machine_Learning

[2/5] Processing: financial_report.pdf
  Title: Q3 Financial Analysis
  Topic: Finance
  Subtopics: Investment, Budgeting
  Destination: Finance

============================================================
Processing Summary
============================================================

Total files: 5
Processed: 5
Failed: 0
Skipped: 0
Duration: 12.3 seconds

Topics found:
  Technology: 3 file(s)
  Finance: 2 file(s)

Files moved: 5
Failed moves: 0
```

## Troubleshooting

### API Key Error
Make sure your OpenAI API key is set correctly in `config.json`. Get your API key from https://platform.openai.com/api-keys

### PDF Reading Errors
Some PDFs may be corrupted or have complex structures that can't be read. These files will be skipped and reported in the summary.

### Rate Limiting
If you encounter rate limiting errors from OpenAI, consider:
- Using the `incremental` mode to process fewer files
- Increasing the delay between API calls in the code
- Using a paid OpenAI account for higher rate limits

## Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection (for AI analysis)

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues and enhancement requests!
