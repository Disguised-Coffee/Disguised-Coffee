#!/usr/bin/env python3
"""
Generate animated PNG (APNG) of a driving car with transparent background.
Supports normal and rainy weather conditions.
"""

from datetime import datetime
import os

def select_and_copy_image():
    """Select which car image to show based on current conditions."""
    
    # Paths
    normal_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'car-normal.png')
    rainy_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'car-rainy.png')
    current_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'car-current.png')
    
    # For now, alternate based on day of week
    # You can later replace this with actual weather API call
    day_of_week = datetime.now().weekday()
    is_rainy = day_of_week >= 5  # Saturday and Sunday are "rainy"
    
    source = rainy_path if is_rainy else normal_path
    
    # Copy to current image
    if os.path.exists(source):
        import shutil
        shutil.copy(source, current_path)
        weather = "RAINY" if is_rainy else "NORMAL"
        print(f"✓ Selected {weather} car image")
    else:
        print(f"⚠️ Source image not found: {source}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    images_dir = os.path.join(project_root, 'images')
    
    # Ensure images directory exists
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate both versions
    print("Switching cars...")

    # Select which one to display
    select_and_copy_image()
    
    print("\n✅ Car animation generation complete!")
