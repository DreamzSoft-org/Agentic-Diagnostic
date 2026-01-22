import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "xai-112CMNM2yYCcrCMSuBqxWMZaEkHWvlx45EnJWKbR9m6c8fw9Curhd5YlZqdHIvaB1y10wht6o3ge1IlH")

    # File upload settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {
        'images': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
        'documents': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'txt', 'rtf', 'md'],
        'medical': ['dcm', 'dicom']
    }

    # Supported medical image types
    MEDICAL_IMAGE_TYPES = [
        'X-Ray', 'CT Scan', 'MRI', 'Ultrasound',
        'PET Scan', 'Mammography', 'DICOM',
        'Endoscopy', 'Pathology Slides'
    ]

    # Report sections
    REPORT_SECTIONS = [
        'Patient Information',
        'Clinical Findings',
        'Laboratory Results',
        'Imaging Results',
        'Diagnosis',
        'Recommendations',
        'Follow-up Plan'
    ]

    # LLM Settings
    LLM_MODEL_PREFERENCES = {
        'primary': 'openai',  # Options: 'openai', 'groq'
        'fallback': 'groq'
    }

    # Default models
    DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
    DEFAULT_GROQ_MODEL = "mixtral-8x7b-32768"

settings = Settings()