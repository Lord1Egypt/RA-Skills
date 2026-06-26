"""TTS backend registry."""
import os
import sys


BACKENDS = {
    'azure': {
        'module': '.azure',
        'env': ['AZURE_SPEECH_KEY'],
        'import': ('azure.cognitiveservices.speech', 'azure-cognitiveservices-speech',
                    'pip install azure-cognitiveservices-speech'),
        'max_chars': 400,
    },
    'cosyvoice': {
        'module': '.cosyvoice',
        'env': ['DASHSCOPE_API_KEY'],
        'import': ('dashscope', 'dashscope', 'pip install dashscope'),
        'max_chars': 400,
    },
    'edge': {
        'module': '.edge',
        'env': [],
        'import': ('edge_tts', 'edge-tts', 'pip install edge-tts'),
        'max_chars': 400,
    },
    'doubao': {
        'module': '.doubao',
        'env': ['VOLCENGINE_APPID', 'VOLCENGINE_ACCESS_TOKEN'],
        'import': ('requests', 'requests', 'pip install requests'),
        'max_chars': 280,
    },
    'elevenlabs': {
        'module': '.elevenlabs',
        'env': ['ELEVENLABS_API_KEY'],
        'import': ('requests', 'requests', 'pip install requests'),
        'max_chars': 400,
    },
    'openai': {
        'module': '.openai_tts',
        'env': ['OPENAI_API_KEY'],
        'import': ('requests', 'requests', 'pip install requests'),
        'max_chars': 400,
    },
    'google': {
        'module': '.google_tts',
        'env': ['GOOGLE_TTS_API_KEY'],
        'import': ('requests', 'requests', 'pip install requests'),
        'max_chars': 400,
    },
}


def init_backend(name):
    """Validate dependencies and env vars for a backend. Returns config dict."""
    if name not in BACKENDS:
        print(f"Error: Unknown backend '{name}'. Use: {', '.join(BACKENDS.keys())}", file=sys.stderr)
        sys.exit(1)

    info = BACKENDS[name]

    # Check Python module
    mod_name, pkg_name, install_cmd = info['import']
    try:
        __import__(mod_name)
    except ImportError:
        print(f"Error: '{pkg_name}' not installed. Run: {install_cmd}", file=sys.stderr)
        sys.exit(1)

    # Check env vars
    for var in info['env']:
        if not os.environ.get(var):
            print(f"Error: {var} not set", file=sys.stderr)
            sys.exit(1)

    return _build_config(name)


def get_synthesize_func(name):
    """Import and return the synthesize function for a backend."""
    from importlib import import_module
    mod = import_module(BACKENDS[name]['module'], package='tts.backends')
    return mod.synthesize


def get_max_chars(name):
    """Return max chunk size for a backend."""
    return BACKENDS[name]['max_chars']


def _build_config(name):
    """Build backend-specific config dict from environment variables."""
    config = {}
    if name == 'azure':
        config['key'] = os.environ['AZURE_SPEECH_KEY']
        config['region'] = os.environ.get('AZURE_SPEECH_REGION', 'eastasia')
        config['voice'] = os.environ.get('AZURE_TTS_VOICE', 'zh-CN-XiaoxiaoMultilingualNeural')
    elif name == 'edge':
        config['voice'] = os.environ.get('EDGE_TTS_VOICE', 'zh-CN-XiaoxiaoNeural')
    elif name == 'doubao':
        config['appid'] = os.environ['VOLCENGINE_APPID']
        config['token'] = os.environ['VOLCENGINE_ACCESS_TOKEN']
        config['cluster'] = os.environ.get('VOLCENGINE_CLUSTER', 'volcano_tts')
        config['voice'] = os.environ.get('VOLCENGINE_VOICE_TYPE', 'BV001_streaming')
        config['endpoint'] = os.environ.get('VOLCENGINE_TTS_ENDPOINT', 'https://openspeech.bytedance.com/api/v1/tts')
    elif name == 'elevenlabs':
        config['key'] = os.environ['ELEVENLABS_API_KEY']
        config['voice'] = os.environ.get('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
        config['model'] = os.environ.get('ELEVENLABS_MODEL', 'eleven_multilingual_v2')
    elif name == 'openai':
        config['key'] = os.environ['OPENAI_API_KEY']
        config['voice'] = os.environ.get('OPENAI_TTS_VOICE', 'alloy')
        config['model'] = os.environ.get('OPENAI_TTS_MODEL', 'tts-1-hd')
    elif name == 'google':
        config['key'] = os.environ['GOOGLE_TTS_API_KEY']
        config['voice'] = os.environ.get('GOOGLE_TTS_VOICE', 'en-US-Neural2-F')
        config['language'] = os.environ.get('GOOGLE_TTS_LANGUAGE', 'en-US')
    return config
