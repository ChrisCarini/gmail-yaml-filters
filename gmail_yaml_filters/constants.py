from pathlib import Path

DEFAULT_CLIENT_SECRET_FILE = 'client_secret.json'
DEFAULT_CREDENTIAL_STORE = Path.home() / '.credentials' / 'gmail_yaml_filters.json'
DEFAULT_SCOPES = [
    'https://www.googleapis.com/auth/gmail.settings.basic',
    'https://www.googleapis.com/auth/gmail.labels',
]
