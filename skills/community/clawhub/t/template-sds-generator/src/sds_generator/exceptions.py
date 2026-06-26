class SDSGeneratorError(Exception):
    """Base exception for the project."""


class InvalidInputCountError(SDSGeneratorError):
    """Raised when input file count is outside the supported range."""


class InvalidInputBundleError(SDSGeneratorError):
    """Raised when a role-aware input bundle is incomplete or inconsistent."""


class InvalidTemplateContractError(SDSGeneratorError):
    """Raised when a supplied template does not satisfy the formal contract."""


class UnsupportedFileTypeError(SDSGeneratorError):
    """Raised when an unsupported input type is supplied."""


class ParsingError(SDSGeneratorError):
    """Raised when parsing of an input document fails."""


class OCRUnavailableError(SDSGeneratorError):
    """Raised when OCR was requested but no OCR backend is available."""


class MostlyScannedPdfError(ParsingError):
    """Raised when a PDF appears scanned and OCR is disabled."""


class CriticalFieldFabricationError(SDSGeneratorError):
    """Raised when a critical field would need to be fabricated."""
