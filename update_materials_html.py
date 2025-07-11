import os
import re

MATERIALS_DIR = 'materials'
HTML_EXT = '.html'
START_MARK = '<!-- AUTO-GENERATED-START -->'
END_MARK = '<!-- AUTO-GENERATED-END -->'

# File extensions
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
TEXT_EXTS = {'.txt', '.md', '.html', '.rtf'}


def generate_list(folder, rel_folder):
    items = []
    # Insert Text.html contents directly if present
    text_html_path = os.path.join(folder, 'Text.html')
    if os.path.isfile(text_html_path):
        with open(text_html_path, 'r', encoding='utf-8') as f:
            text_html_content = f.read().strip()
        if text_html_content:
            items.append(text_html_content)
    # List other files (skip Text.html)
    for fname in sorted(os.listdir(folder)):
        if fname == 'Text.html':
            continue
        fpath = os.path.join(folder, fname)
        if os.path.isdir(fpath):
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext in IMAGE_EXTS:
            items.append(f'<li><img src="{rel_folder}/{fname}" alt="{fname}" style="max-width:300px;"></li>')
        elif ext in TEXT_EXTS:
            items.append(f'<li><a href="{rel_folder}/{fname}" target="_blank">{fname}</a></li>')
    if not items:
        return '<ul><li><em>No files yet.</em></li></ul>'
    # If any of the items is a <ul> (from Text.html), don't wrap again
    if any(item.strip().startswith('<ul>') for item in items):
        return '\n'.join(items)
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'


def update_html(html_path, new_content):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    pattern = re.compile(f'{START_MARK}.*?{END_MARK}', re.DOTALL)
    replacement = f'{START_MARK}\n{new_content}\n{END_MARK}'
    new_html, n = pattern.subn(replacement, html)
    if n == 0:
        print(f'Warning: Markers not found in {html_path}. Skipping.')
        return
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'Updated: {html_path}')


def main():
    for entry in os.listdir(MATERIALS_DIR):
        folder = os.path.join(MATERIALS_DIR, entry)
        if not os.path.isdir(folder):
            continue
        html_file = os.path.join(MATERIALS_DIR, entry + HTML_EXT)
        if not os.path.isfile(html_file):
            print(f'No HTML file for {entry}, skipping.')
            continue
        rel_folder = entry  # e.g., '000'
        new_content = generate_list(folder, rel_folder)
        update_html(html_file, new_content)

if __name__ == '__main__':
    main() 