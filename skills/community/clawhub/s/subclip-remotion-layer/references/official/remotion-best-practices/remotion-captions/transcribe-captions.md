# Transcription in Subclip

Read `$subclip-transcription` and use Subclip's selected transcription engine. Import source media into the project library, then transcribe through native tools and place captions in the native captions layer. Preserve the transcript, word timing, language, and source identity for editing.

Do not install Whisper/ONNX packages, download models from layer code, create Node scripts, ask for provider API keys, or decode/transcribe footage inside a Remotion component. Subclip owns inference, workers, model downloads, cancellation, and resource cleanup. For a visual intrinsic to a Remotion layer, pass existing caption data through serializable props and use the already installed `@remotion/captions` utilities.
