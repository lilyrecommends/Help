import re
from bs4 import BeautifulSoup

# File paths
LOG2025 = 'LOG2025.html'
LOG_HTML = 'log.html'

# Extract and clean the table HTML from LOG2025.html
with open(LOG2025, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')
    table = soup.find('table')
    if not table:
        print('No table found in LOG2025.html!')
        exit(1)
    # Remove the first row (column headers like A, B, C...)
    rows = table.find_all('tr')
    if rows:
        rows[0].decompose()
    # Remove the first column (row headers like 1, 2, 3...)
    for row in table.find_all('tr'):
        first_cell = row.find(['th', 'td'])
        if first_cell:
            first_cell.decompose()
    new_table_html = str(table)

# Read log.html
with open(LOG_HTML, encoding='utf-8') as f:
    html = f.read()

# Find the 2025 table block
pattern = re.compile(r'(<button class="collapsible collapsed">2025[\s\S]+?<div class="scroll-table"[\s\S]+?<table[\s\S]+?</table>[\s\S]+?</div>[\s\S]+?</div>)', re.MULTILINE)
match = pattern.search(html)
if not match:
    print('Could not find 2025 table in log.html!')
    exit(1)
block = match.group(0)

# Replace the old table with the cleaned one from LOG2025.html
new_block = re.sub(r'<table[\s\S]+?</table>', new_table_html, block, count=1)

# Replace in the full HTML
new_html = html.replace(block, new_block)

with open(LOG_HTML, 'w', encoding='utf-8') as f:
    f.write(new_html)

print('2025 table in log.html replaced with cleaned table from LOG2025.html!') 