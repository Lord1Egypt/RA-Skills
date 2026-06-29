#!/home/guoxh/.openclaw/venv-clawd/bin/python
"""
EXIF preservation utilities for photo editing.
Reads EXIF from input, preserves through any processing pipeline.
"""
import os
import sys
from typing import Dict, Any, Optional

# Try multiple EXIF libraries
PIEXIF_AVAILABLE = False
EXIF_AVAILABLE = False

try:
    import piexif
    PIEXIF_AVAILABLE = True
except ImportError:
    pass

try:
    import exif
    EXIF_AVAILABLE = True
except ImportError:
    pass


class ExifPreserver:
    """
    Reads EXIF from source image and provides methods to apply it to output.
    Works with both PIL (JPEG, PNG, WebP) and standalone EXIF files.
    """
    
    def __init__(self, source_path: str):
        self.source_path = source_path
        self.exif_dict: Optional[Dict] = None
        self.exif_bytes: Optional[bytes] = None
        self._read()
    
    def _read(self):
        """Read EXIF data from source image."""
        if not os.path.exists(self.source_path):
            return
        
        ext = os.path.splitext(self.source_path)[1].lower()
        
        # Try piexif first (works on raw image bytes)
        if PIEXIF_AVAILABLE:
            try:
                self.exif_dict = piexif.load(self.source_path)
                # Convert to bytes for later insertion
                self.exif_bytes = piexif.dump(self.exif_dict)
                return
            except Exception:
                pass
        
        # Fallback: use exif library for basic tag reading
        if EXIF_AVAILABLE:
            try:
                with open(self.source_path, 'rb') as f:
                    tags = exif.Image(f).get_all()
                if tags:
                    # Convert to piexif-compatible dict
                    self.exif_dict = self._convert_to_piexif(tags)
                    if self.exif_dict:
                        self.exif_bytes = piexif.dump(self.exif_dict)
                    return
            except Exception:
                pass
    
    def _convert_to_piexif(self, tags: Dict) -> Optional[Dict]:
        """Convert exif.Image tags dict to piexif format."""
        if not PIEXIF_AVAILABLE:
            return None
        
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        
        # Mapping of common exif.Image attribute names to piexif IFD keys
        # piexif uses numeric constants
        PIEXIF_CONSTANTS = {
            # 0th IFD (Image)
            "make": piexif.ImageIFD.Make,
            "model": piexif.ImageIFD.Model,
            "orientation": piexif.ImageIFD.Orientation,
            "software": piexif.ImageIFD.Software,
            "datetime": piexif.ImageIFD.DateTime,
            "artist": piexif.ImageIFD.Artist,
            "copyright": piexif.ImageIFD.Copyright,
            "exif_ifd_pointer": None,  # skip pointers
            "gps_ifd_pointer": None,
        }
        
        # Exif IFD tags
        EXIF_CONSTANTS = {
            "exposure_time": piexif.ExifIFD.ExposureTime,
            "f_number": piexif.ExifIFD.FNumber,
            "iso_speed": piexif.ExifIFD.ISOSpeedRatings,
            "date_time_original": piexif.ExifIFD.DateTimeOriginal,
            "shutter_speed_value": piexif.ExifIFD.ShutterSpeedValue,
            "aperture_value": piexif.ExifIFD.ApertureValue,
            "brightness_value": piexif.ExifIFD.BrightnessValue,
            "metering_mode": piexif.ExifIFD.MeteringMode,
            "flash": piexif.ExifIFD.Flash,
            "focal_length": piexif.ExifIFD.FocalLength,
            "focal_length_in_35mm_film": piexif.ExifIFD.FocalLengthIn35mmFilm,
            "white_balance": piexif.ExifIFD.WhiteBalance,
            "exposure_mode": piexif.ExifIFD.ExposureMode,
            "exposure_program": piexif.ExifIFD.ExposureProgram,
            "scene_type": piexif.ExifIFD.SceneType,
            "subject_distance": piexif.ExifIFD.SubjectDistance,
            "lens_make": piexif.ExifIFD.LensMake,
            "lens_model": piexif.ExifIFD.LensModel,
            "lens_specification": piexif.ExifIFD.LensSpecification,
        }
        
        for attr, key in PIEXIF_CONSTANTS.items():
            if attr in tags and key is not None:
                val = tags[attr]
                if isinstance(val, bytes):
                    try:
                        val = val.decode('utf-8', errors='replace')
                    except Exception:
                        continue
                if val:
                    exif_dict["0th"][key] = val
        
        for attr, key in EXIF_CONSTANTS.items():
            if attr in tags and key is not None:
                val = tags[attr]
                if isinstance(val, bytes):
                    try:
                        val = val.decode('utf-8', errors='replace')
                    except Exception:
                        continue
                if val:
                    exif_dict["Exif"][key] = val
        
        # Check if we got any data
        if not exif_dict["0th"] and not exif_dict["Exif"]:
            return None
        
        return exif_dict
    
    def has_exif(self) -> bool:
        """Check if source image has EXIF data."""
        return bool(self.exif_dict) and bool(self.exif_bytes)
    
    def apply_to_file(self, output_path: str, source_image_for_format: str = None):
        """
        Apply stored EXIF to output image file.
        
        Args:
            output_path: Path to write the EXIF data to
            source_image_for_format: Optional source image whose format determines
                                    how EXIF is written (JPEG vs PNG vs TIFF)
        """
        if not self.exif_bytes:
            return False
        
        if not os.path.exists(output_path):
            return False
        
        if not PIEXIF_AVAILABLE:
            return False
        
        try:
            piexif.insert(self.exif_bytes, output_path)
            return True
        except Exception as e:
            print(f"Warning: Could not write EXIF: {e}", file=sys.stderr)
            return False
    
    def apply_to_pil_image(self, pil_image, output_path: str):
        """
        Apply EXIF to a PIL Image and save it.
        
        Args:
            pil_image: PIL Image object
            output_path: Path to save the image
        """
        if not self.exif_bytes:
            pil_image.save(output_path)
            return
        
        try:
            # piexif requires loading from bytes and dumping to get bytes
            # For PIL, we embed exif via the exif keyword argument
            pil_image.save(output_path, exif=self.exif_bytes)
        except Exception as e:
            # Fallback: save without EXIF
            pil_image.save(output_path)
            print(f"Warning: Could not embed EXIF in {output_path}: {e}", file=sys.stderr)


def preserve_exif(input_path: str, output_path: str):
    """
    Convenience function: copy EXIF from input to output.
    Works for any image format supported by piexif/exif.
    """
    preserver = ExifPreserver(input_path)
    if preserver.has_exif():
        preserver.apply_to_file(output_path)
        return True
    return False


# Decorator pattern for easy use with any processing function
def with_exif_preservation(input_arg_name: str = "input", output_arg_name: str = "output"):
    """
    Decorator that automatically preserves EXIF metadata.
    
    Usage:
        @with_exif_preservation("input", "output")
        def my_processing(input, output, **kwargs):
            # ... your code ...
            cv2.imwrite(output, processed)
    
    The decorated function's input and output paths will have EXIF
    automatically transferred.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get input/output paths
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            input_path = kwargs.get(input_arg_name)
            output_path = kwargs.get(output_arg_name)
            
            # Also check positional args
            if input_path is None and input_arg_name in params:
                idx = params.index(input_arg_name)
                if idx < len(args):
                    input_path = args[idx]
            
            if output_path is None and output_arg_name in params:
                idx = params.index(output_arg_name)
                if idx < len(args):
                    output_path = args[idx]
            
            # Call the function
            result = func(*args, **kwargs)
            
            # Apply EXIF if we have both paths
            if input_path and output_path and os.path.exists(output_path):
                preserver = ExifPreserver(input_path)
                if preserver.has_exif():
                    preserver.apply_to_file(output_path)
            
            return result
        return wrapper
    return decorator


# ─────────────────────────────────────────────────────────────────
# CLI helpers for standalone use
# ─────────────────────────────────────────────────────────────────

def cmd_read_exif(path: str) -> Dict[str, Any]:
    """Read and display EXIF from an image."""
    preserver = ExifPreserver(path)
    
    if not preserver.has_exif():
        print(f"No EXIF data found in: {path}")
        return {}
    
    result = {}
    
    # Parse 0th IFD
    ifd0 = preserver.exif_dict.get("0th", {})
    important_tags = {
        piexif.ImageIFD.Make: "Make",
        piexif.ImageIFD.Model: "Model",
        piexif.ImageIFD.Software: "Software",
        piexif.ImageIFD.DateTime: "DateTime",
        piexif.ImageIFD.Orientation: "Orientation",
        piexif.ImageIFD.Artist: "Artist",
        piexif.ImageIFD.Copyright: "Copyright",
    }
    
    print(f"\nEXIF data for: {path}")
    print(f"{'─'*50}")
    
    for key, name in important_tags.items():
        if key in ifd0:
            val = ifd0[key]
            if isinstance(val, bytes):
                val = val.decode('utf-8', errors='replace')
            print(f"  {name:20s}: {val}")
            result[name.lower()] = val
    
    # Parse Exif IFD
    exif_ifd = preserver.exif_dict.get("Exif", {})
    exif_tags = {
        piexif.ExifIFD.ExposureTime: "Exposure Time",
        piexif.ExifIFD.FNumber: "F-Number",
        piexif.ExifIFD.ISOSpeedRatings: "ISO",
        piexif.ExifIFD.FocalLength: "Focal Length",
        piexif.ExifIFD.DateTimeOriginal: "Date Taken",
        piexif.ExifIFD.LensModel: "Lens Model",
        piexif.ExifIFD.LensMake: "Lens Make",
    }
    
    for key, name in exif_tags.items():
        if key in exif_ifd:
            val = exif_ifd[key]
            if isinstance(val, bytes):
                val = val.decode('utf-8', errors='replace')
            print(f"  {name:20s}: {val}")
            result[name.lower().replace(' ', '_')] = val
    
    print(f"{'─'*50}\n")
    return result


def cmd_strip_exif(path: str, output: str = None):
    """Remove EXIF from an image."""
    import shutil
    
    if output is None:
        output = path
    
    preserver = ExifPreserver(path)
    
    # Just copy file and then strip
    shutil.copy2(path, output)
    
    if PIEXIF_AVAILABLE:
        try:
            piexif.remove(output)
            print(f"✓ EXIF stripped: {output}")
            return
        except Exception:
            pass
    
    # Fallback: use ImageMagick
    import subprocess
    for cmd in ["magick", "convert"]:
        try:
            subprocess.run([cmd, "-strip", output, output],
                         capture_output=True, timeout=10)
            print(f"✓ EXIF stripped with {cmd}: {output}")
            return
        except Exception:
            pass
    
    print(f"Warning: Could not strip EXIF from {output}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="EXIF utility tool")
    sub = parser.add_subparsers(dest="cmd")
    
    r = sub.add_parser("read", help="Read and display EXIF from image")
    r.add_argument("image", help="Image file path")
    
    s = sub.add_parser("strip", help="Remove EXIF from image")
    s.add_argument("image", help="Image file path")
    s.add_argument("-o", "--output", help="Output path (default: overwrite)")
    
    copy = sub.add_parser("copy", help="Copy EXIF from input to output")
    copy.add_argument("input", help="Source image")
    copy.add_argument("output", help="Destination image")
    
    args = parser.parse_args()
    
    if args.cmd == "read":
        cmd_read_exif(args.image)
    elif args.cmd == "strip":
        cmd_strip_exif(args.image, args.output)
    elif args.cmd == "copy":
        preserver = ExifPreserver(args.input)
        if preserver.has_exif():
            preserver.apply_to_file(args.output)
            print(f"✓ EXIF copied: {args.input} → {args.output}")
        else:
            print(f"No EXIF in {args.input} to copy")
    else:
        parser.print_help()
