import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    """Returns a sorted list of encyclopedia entry names."""
    _, filenames = default_storage.listdir("entries")
    return sorted(
        re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")
    )

def save_entry(title, content):
    """Saves an encyclopedia entry in Markdown format.
       If the entry exists, it replaces the old content.
    """
    filename = f"entries/{title}.md"
    
    # Encode content in UTF-8 before saving
    encoded_content = content.encode("utf-8")

    if default_storage.exists(filename):
        default_storage.delete(filename)

    default_storage.save(filename, ContentFile(encoded_content))

def get_entry(title):
    """Retrieves an encyclopedia entry by its title."""
    filename = f"entries/{title}.md"
    try:
        with default_storage.open(filename, "rb") as f:  # Open as binary
            content = f.read()
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                return "Error: This entry contains non-UTF-8 characters!"
    except FileNotFoundError:
        return None  # Returns None if entry doesn't exist
