#!/usr/bin/env python3
"""
Generate animated PNG (APNG) of a driving car with transparent background.
Supports normal and rainy weather conditions.
"""

from PIL import Image, ImageDraw
import math
from datetime import datetime
import os

# Configuration
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 200
FRAME_COUNT = 20
FRAME_DURATION = 100  # milliseconds

def draw_car(draw, x, y, is_rainy=False, color=(50, 50, 50)):
    """Draw a sedan car profile (similar to Honda Prelude)."""
    
    # Car body dimensions
    car_width = 120
    car_height = 50
    
    # Main body
    draw.rectangle(
        [x, y + 15, x + car_width, y + 35],
        fill=color,
        outline=(0, 0, 0),
        width=2
    )
    
    # Cabin/roof section (sloped)
    points = [
        (x + 20, y + 15),
        (x + 40, y + 5),
        (x + 90, y + 5),
        (x + 110, y + 15)
    ]
    draw.polygon(points, fill=color, outline=(0, 0, 0))
    
    # Windows
    # Front window
    draw.rectangle(
        [x + 35, y + 8, x + 60, y + 14],
        fill=(100, 150, 200),
        outline=(0, 0, 0),
        width=1
    )
    
    # Back window
    draw.rectangle(
        [x + 65, y + 8, x + 105, y + 14],
        fill=(100, 150, 200),
        outline=(0, 0, 0),
        width=1
    )
    
    # Headlights (front)
    draw.ellipse(
        [x + 8, y + 20, x + 14, y + 26],
        fill=(255, 255, 200),
        outline=(0, 0, 0),
        width=1
    )
    draw.ellipse(
        [x + 8, y + 28, x + 14, y + 32],
        fill=(255, 100, 100),  # Tail light
        outline=(0, 0, 0),
        width=1
    )
    
    # Wheels
    wheel_radius = 8
    
    # Front wheel
    draw.ellipse(
        [x + 25 - wheel_radius, y + 38, x + 25 + wheel_radius, y + 54],
        fill=(40, 40, 40),
        outline=(0, 0, 0),
        width=2
    )
    # Wheel rim
    draw.ellipse(
        [x + 25 - 4, y + 42, x + 25 + 4, y + 50],
        outline=(150, 150, 150),
        width=1
    )
    
    # Rear wheel
    draw.ellipse(
        [x + 95 - wheel_radius, y + 38, x + 95 + wheel_radius, y + 54],
        fill=(40, 40, 40),
        outline=(0, 0, 0),
        width=2
    )
    # Wheel rim
    draw.ellipse(
        [x + 95 - 4, y + 42, x + 95 + 4, y + 50],
        outline=(150, 150, 150),
        width=1
    )
    
    # Add rain drops if rainy
    if is_rainy:
        # Add diagonal rain lines
        for i in range(5):
            offset = i * 25
            draw.line(
                [x + 10 + offset, y - 10, x + 5 + offset, y + 5],
                fill=(100, 150, 200),
                width=2
            )
            draw.line(
                [x + 20 + offset, y - 10, x + 15 + offset, y + 5],
                fill=(100, 150, 200),
                width=2
            )


def generate_animated_png(output_path, is_rainy=False):
    """Generate an animated PNG of a car driving."""
    
    frames = []
    
    for frame_num in range(FRAME_COUNT):
        # Create transparent background (RGBA)
        img = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate car position (moves left to right then right to left, oscillating)
        # Use sine wave for smooth back-and-forth motion
        progress = frame_num / FRAME_COUNT
        sin_value = math.sin(progress * math.pi)  # 0 to 1 to 0
        car_x = 50 + (sin_value * 250)  # Oscillates across 250 pixels
        
        # Draw car
        draw_car(draw, car_x, 50, is_rainy=is_rainy)
        
        # Add weather indicator text
        if is_rainy:
            text = "🌧️ RAINY"
            text_color = (100, 150, 200, 255)
        else:
            text = "☀️ NORMAL"
            text_color = (255, 200, 100, 255)
        
        draw.text((CANVAS_WIDTH - 130, 10), text, fill=text_color, font=None)
        
        frames.append(img)
    
    # Save as APNG
    # PIL's save() can export animated PNGs when given the right parameters
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0,  # Infinite loop
        optimize=False
    )
    
    print(f"✓ Generated {output_path}")


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
    print("Generating animated car PNGs...")
    generate_animated_png(
        os.path.join(images_dir, 'car-normal.png'),
        is_rainy=False
    )
    generate_animated_png(
        os.path.join(images_dir, 'car-rainy.png'),
        is_rainy=True
    )
    
    # Select which one to display
    select_and_copy_image()
    
    print("\n✅ Car animation generation complete!")
