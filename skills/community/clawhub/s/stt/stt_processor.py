#!/usr/bin/env python3
"""
Speech-to-Text Processor using OpenAI Whisper

This script monitors the media/inbound folder for audio files and transcribes them
using OpenAI Whisper. It supports various audio formats and provides structured
output for integration with the OpenClaw system.
"""

import os
import sys
import json
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
import shutil

try:
    import whisper
    import torch
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install dependencies: pip install openai-whisper torch")
    sys.exit(1)


class STTProcessor:
    """Speech-to-Text processor using OpenAI Whisper"""
    
    def __init__(self, 
                 model_name: str = "base",
                 media_dir: str = None,
                 output_dir: str = None,
                 language: str = None):
        """
        Initialize the STT processor
        
        Args:
            model_name: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
            media_dir: Path to media directory containing inbound folder
            output_dir: Path to output directory for transcriptions
            language: Language code for transcription (None for auto-detect)
        """
        self.model_name = model_name
        self.language = language
        
        # Set up directories
        if media_dir:
            self.media_dir = Path(media_dir)
        else:
            # Default to media folder at same level as workspace
            workspace_dir = Path(__file__).parent.parent.parent
            self.media_dir = workspace_dir.parent / "media"
        
        self.inbound_dir = self.media_dir / "inbound"
        
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent / "output"
        
        self.processed_dir = self.output_dir / "processed"
        self.failed_dir = self.output_dir / "failed"
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        self.failed_dir.mkdir(exist_ok=True)
        
        # Supported audio formats
        self.supported_formats = {'.ogg', '.wav', '.mp3', '.m4a', '.flac', '.aac', '.opus'}
        
        # Initialize model (lazy loading)
        self._model = None
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.output_dir / "stt_processor.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_model(self):
        """Lazy load the Whisper model"""
        if self._model is None:
            self.logger.info(f"Loading Whisper model: {self.model_name}")
            try:
                self._model = whisper.load_model(self.model_name)
                self.logger.info("Model loaded successfully")
            except Exception as e:
                self.logger.error(f"Failed to load model: {e}")
                raise
        return self._model
    
    def get_audio_files(self) -> List[Path]:
        """Get list of audio files to process from inbound directory"""
        if not self.inbound_dir.exists():
            self.logger.warning(f"Inbound directory does not exist: {self.inbound_dir}")
            return []
        
        audio_files = []
        for file_path in self.inbound_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                audio_files.append(file_path)
        
        return sorted(audio_files, key=lambda x: x.stat().st_mtime)
    
    def transcribe_audio(self, audio_path: Path) -> Dict:
        """
        Transcribe an audio file using Whisper
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing transcription results
        """
        model = self._load_model()
        
        try:
            self.logger.info(f"Transcribing: {audio_path.name}")
            start_time = time.time()
            
            # Transcribe the audio
            result = model.transcribe(
                str(audio_path),
                language=self.language,
                verbose=False
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Prepare structured output
            transcription = {
                'file_info': {
                    'filename': audio_path.name,
                    'file_path': str(audio_path),
                    'file_size': audio_path.stat().st_size,
                    'file_modified': audio_path.stat().st_mtime
                },
                'processing_info': {
                    'model': self.model_name,
                    'language': result.get('language', 'unknown'),
                    'processing_time_seconds': round(processing_time, 2),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                },
                'transcription': {
                    'text': result.get('text', '').strip(),
                    'segments': []
                }
            }
            
            # Add detailed segments if available
            for segment in result.get('segments', []):
                transcription['transcription']['segments'].append({
                    'start': segment.get('start', 0),
                    'end': segment.get('end', 0),
                    'text': segment.get('text', '').strip()
                })
            
            self.logger.info(f"Transcription completed in {processing_time:.2f}s")
            return transcription
            
        except Exception as e:
            self.logger.error(f"Failed to transcribe {audio_path.name}: {e}")
            return {
                'file_info': {
                    'filename': audio_path.name,
                    'file_path': str(audio_path)
                },
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
    
    def save_transcription(self, transcription: Dict, original_file: Path) -> Path:
        """Save transcription to JSON file"""
        output_filename = f"{original_file.stem}_transcription.json"
        output_path = self.output_dir / output_filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transcription, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Transcription saved: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to save transcription: {e}")
            raise
    
    def move_processed_file(self, audio_file: Path, success: bool = True) -> Optional[Path]:
        """Move processed audio file to appropriate directory"""
        try:
            target_dir = self.processed_dir if success else self.failed_dir
            target_path = target_dir / audio_file.name
            
            # Handle filename conflicts
            counter = 1
            while target_path.exists():
                stem = audio_file.stem
                suffix = audio_file.suffix
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            shutil.move(str(audio_file), str(target_path))
            self.logger.info(f"Moved {audio_file.name} to {target_dir.name}")
            return target_path
            
        except Exception as e:
            self.logger.error(f"Failed to move file {audio_file.name}: {e}")
            return None
    
    def process_single_file(self, audio_file: Path) -> bool:
        """Process a single audio file"""
        try:
            # Transcribe the audio
            transcription = self.transcribe_audio(audio_file)
            
            # Save transcription
            self.save_transcription(transcription, audio_file)
            
            # Check if transcription was successful
            success = 'error' not in transcription
            
            # Move the processed file
            self.move_processed_file(audio_file, success)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error processing {audio_file.name}: {e}")
            self.move_processed_file(audio_file, False)
            return False
    
    def process_all_files(self) -> Tuple[int, int]:
        """
        Process all audio files in the inbound directory
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        audio_files = self.get_audio_files()
        
        if not audio_files:
            self.logger.info("No audio files found to process")
            return 0, 0
        
        self.logger.info(f"Found {len(audio_files)} audio files to process")
        
        successful = 0
        failed = 0
        
        for audio_file in audio_files:
            if self.process_single_file(audio_file):
                successful += 1
            else:
                failed += 1
        
        self.logger.info(f"Processing complete: {successful} successful, {failed} failed")
        return successful, failed
    
    def watch_directory(self, check_interval: int = 10):
        """
        Watch the inbound directory for new files and process them
        
        Args:
            check_interval: Time in seconds between directory checks
        """
        self.logger.info(f"Starting directory watch mode (checking every {check_interval}s)")
        self.logger.info(f"Watching: {self.inbound_dir}")
        
        processed_files = set()
        
        try:
            while True:
                audio_files = self.get_audio_files()
                new_files = [f for f in audio_files if f not in processed_files]
                
                if new_files:
                    self.logger.info(f"Found {len(new_files)} new files")
                    for audio_file in new_files:
                        if self.process_single_file(audio_file):
                            processed_files.add(audio_file)
                        else:
                            # Keep track of failed files too to avoid reprocessing
                            processed_files.add(audio_file)
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Directory watch stopped by user")
        except Exception as e:
            self.logger.error(f"Error in directory watch: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Speech-to-Text Processor using OpenAI Whisper")
    parser.add_argument('--model', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--language', help='Language code for transcription (auto-detect if not specified)')
    parser.add_argument('--media-dir', help='Path to media directory (default: ../../../media)')
    parser.add_argument('--output-dir', help='Path to output directory (default: ./output)')
    parser.add_argument('--watch', action='store_true', help='Watch directory for new files')
    parser.add_argument('--interval', type=int, default=10, help='Check interval for watch mode (default: 10s)')
    parser.add_argument('--file', help='Process a specific audio file')
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = STTProcessor(
        model_name=args.model,
        media_dir=args.media_dir,
        output_dir=args.output_dir,
        language=args.language
    )
    
    if args.file:
        # Process specific file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return 1
        
        success = processor.process_single_file(file_path)
        return 0 if success else 1
    
    elif args.watch:
        # Watch directory mode
        processor.watch_directory(args.interval)
        return 0
    
    else:
        # Process all files in inbound directory
        successful, failed = processor.process_all_files()
        return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())