import os
import json
import mimetypes
import base64
from PIL import Image
from io import BytesIO
import subprocess
import sys


def install_bs4():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])


try:
    from bs4 import BeautifulSoup
except:
    install_bs4()
    from bs4 import BeautifulSoup

from bs4 import BeautifulSoup


def is_hidden(path):
    return os.path.basename(path).startswith('.')


def is_hidden_directory(path):
    directories = path.split(os.sep)
    for directory in directories:
        first = 1
        if first and directory in ['.', '..']:
            continue
        if directory.startswith('.'):
            # print(f"{directory} is a hidden directory.")
            return True
        first = 0
    return False


def get_metadata(path):
    file_name = os.path.basename(path)
    file_extension = os.path.splitext(path)[1]
    last_update = os.path.getmtime(path)
    mime_type, _ = mimetypes.guess_type(path)
    metadata = {
        "url": f"{path}",
        "tags": [
            last_update,
            mime_type,
            file_extension
        ],
        'description': f"last_update: {last_update}, 'mime_type': {mime_type}, 'extension': {file_extension}",
    }

    # exit()
    # Check if file is an image
    if not mime_type:
        print(mime_type)
        print(os.path.isfile(path))
        print(path)
        print(file_name)
        if os.path.isfile(path) and not file_name.startswith('.') and not is_hidden_directory(path):
            with open(path, 'r') as file:
                content = file.read()
                body_text = (content[:275] + '..')
                # metadata['description'] = ' '.join(body_text.split()[:20])
                metadata['description'] = body_text
        else:
            return None
    elif mime_type and 'image' in mime_type:
        # Open, resize and convert the image to base64
        with Image.open(path) as img:
            img.thumbnail((64, 64))
            buffered = BytesIO()
            img.save(buffered, format=img.format)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            metadata['icon_64px_base64'] = f"data:image/png;base64,{img_str}"
    elif os.path.isfile(
            path) and 'text' in mime_type and not 'image' in mime_type and not 'audio' in mime_type and not 'video' in mime_type:
        with open(path, 'r') as file:
            content = file.read()
            if file_extension == '.html':
                soup = BeautifulSoup(content, 'html.parser')
                body_text = (soup.text[:275] + '..')
            else:
                body_text = (content[:275] + '..')

            # metadata['description'] = ' '.join(body_text.split()[:20])
            metadata['description'] = body_text

    return metadata


def save_to_jsonl(files_data, jsonl_file_path):
    with open(jsonl_file_path, 'w') as outfile:
        for entry in files_data:
            json.dump(entry, outfile)
            outfile.write('\n')


def get_files_data(directory_path):
    files_data = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            path = os.path.join(root, file)
            file_data = get_metadata(path)
            if file_data:
                files_data.append(file_data)
    return files_data


def main(directory_path, jsonl_file_path):
    files_data = get_files_data(directory_path)
    save_to_jsonl(files_data, jsonl_file_path)


directory_path = '../'  # replace this with your directory path
jsonl_file_path = 'data.jsonl'  # output jsonl file
main(directory_path, jsonl_file_path)

# pip install beautifulsoup4
