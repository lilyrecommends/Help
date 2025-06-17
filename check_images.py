#!/usr/bin/env python3
import os
import re
from pathlib import Path

def check_images_in_html(html_file):
    """Check which images referenced in HTML file don't exist"""
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image src attributes
    img_pattern = r'<img\s+src="([^"]+)"'
    image_refs = re.findall(img_pattern, content)
    
    missing_images = []
    existing_images = []
    
    print(f"Checking {len(image_refs)} image references...")
    print("-" * 50)
    
    for img_path in image_refs:
        # Convert relative path to absolute path
        full_path = Path(img_path)
        
        if full_path.exists():
            existing_images.append(img_path)
            print(f"✅ EXISTS: {img_path}")
        else:
            missing_images.append(img_path)
            print(f"❌ MISSING: {img_path}")
    
    print("-" * 50)
    print(f"Summary:")
    print(f"  Existing images: {len(existing_images)}")
    print(f"  Missing images: {len(missing_images)}")
    
    if missing_images:
        print(f"\nMissing images:")
        for img in missing_images:
            print(f"  - {img}")
        
        # Ask if user wants to remove them
        response = input(f"\nWould you like to remove the {len(missing_images)} missing image references from the HTML? (y/n): ")
        
        if response.lower() == 'y':
            remove_missing_images(html_file, missing_images)
    else:
        print("\n🎉 All images exist!")

def remove_missing_images(html_file, missing_images):
    """Remove missing image references from HTML file"""
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    backup_file = html_file + '.backup'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created backup: {backup_file}")
    
    # Remove each missing image's div
    for img_path in missing_images:
        # Pattern to match the entire gallery-thumb div containing this image
        pattern = r'<div class="gallery-thumb"><img src="' + re.escape(img_path) + r'"[^>]*></div>\s*'
        content = re.sub(pattern, '', content)
    
    # Write the cleaned content back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Removed {len(missing_images)} missing image references from {html_file}")
    print(f"   Backup saved as {backup_file}")

if __name__ == "__main__":
    html_file = "look.html"
    
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found!")
        exit(1)
    
    check_images_in_html(html_file) 