# PDF Organizer Skill

## Description
AI-powered PDF organization tool that automatically categorizes and organizes PDF files by topic using GPT analysis.

## Features
- **AI-Powered Content Analysis**: Uses OpenAI/Kimi API to extract titles, authors, and journal names
- **Automatic Topic Classification**: Classifies PDFs into 10 standard categories (Technology, Finance, Health, Science, Education, Business, Entertainment, Politics, Sports, Other)
- **Smart File Naming**: Renames files in `Title_Author_Journal.pdf` format using only underscores
- **Hierarchical Organization**: Creates topic-based folders with subtopic subfolders
- **Batch Processing**: Efficiently processes multiple PDFs at once
- **Incremental Mode**: Only processes new/modified files
- **Error Handling**: Gracefully handles corrupted PDFs and API failures
- **Detailed Logging**: Tracks all operations with comprehensive statistics

## Requirements
- Python 3.8+
- OpenAI API key or Kimi API key
- PDF files to organize

## Usage
1. Configure API key in `config.json`
2. Place PDF files in `input_pdfs/` folder
3. Run: `python pdf_organizer.py`
4. Organized files appear in `organized_pdfs/` folder

## Project Structure
```
pdf_organizer.py          # Main entry point
modules/
  ├── pdf_reader.py       # PDF text extraction
  ├── content_analyzer.py  # OpenAI/Kimi API integration
  ├── folder_manager.py    # Folder creation and management
  └── file_mover.py        # File operations
config.json              # Configuration file
requirements.txt          # Python dependencies
README.md                # Documentation
setup.py                # Setup/initialization script
```

## Configuration Options
- `openai_api_key`: Your API key (required)
- `input_folder`: Folder containing PDFs to organize
- `output_folder`: Destination folder for organized PDFs
- `model`: GPT model to use (gpt-3.5-turbo or moonshot-v1-8k)
- `api_provider`: API provider ("openai" or "kimi")
- `dry_run`: Preview mode without moving files (true/false)
- `incremental`: Only process new/modified files (true/false)
- `max_chars`: Maximum characters to analyze from each PDF
- `custom_topics`: Custom topic mappings

## Example Output
Organized files are named: `Title_Author_Journal.pdf`
Example: `Visual_SLAM_What_Are_the_Current_Trends_and_What_to_Expect_Ali_Tourani,_Hriday_Bavle,_Jose_Luis_Sanchez-Lopez,_and_Holger_Voos_Sensors.pdf`
