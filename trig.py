import win32api
import win32con
import numpy as np
from PIL import ImageGrab
import threading
import time
import asyncio
import pyautogui

# Global variables
running = False
current_mode = "auto"
available_modes = ["auto", "pistol", "marshal"]
mode_index = 0
h_press_timestamps = []  # Track timestamps of "H" key presses

# Configuration (Flexible color detection for purple color)
config = {
    "modes": {
        "auto": {
            "target_colors_rgb": [
                [173, 79, 181],  # Purple shade 1
                [147, 63, 153],  # Purple shade 2
                [200, 100, 210], # Purple shade 3
            ],
            "box_size": 10,  # Smaller detection box for better accuracy
            "color_tolerance": 25,  # Flexibility in detecting shades
        },
        "pistol": {
            "target_colors_rgb": [
                [165, 70, 175],
                [140, 60, 145],
                [185, 90, 200],
            ],
            "box_size": 10,  # Smaller detection box for more accuracy
            "color_tolerance": 30,  # Higher tolerance for variation
        },
        "marshal": {
            "target_colors_rgb": [
                [180, 85, 190],
                [155, 65, 160],
                [195, 95, 210],
            ],
            "box_size": 10,  # Smaller detection box for more precise targeting
            "color_tolerance": 20,  # Precise tolerance for marshal
        },
    }
}

def calculate_color_range(target_colors_rgb, tolerance):
    """
    Calculate the minimum and maximum RGB bounds based on the given colors and tolerance.
    """
    min_rgb = [255, 255, 255]
    max_rgb = [0, 0, 0]

    for color in target_colors_rgb:
        for i in range(3):  # Iterate over R, G, B
            min_rgb[i] = min(min_rgb[i], color[i])
            max_rgb[i] = max(max_rgb[i], color[i])

    # Apply tolerance to the ranges
    min_rgb = [max(0, val - tolerance) for val in min_rgb]
    max_rgb = [min(255, val + tolerance) for val in max_rgb]

    return min_rgb, max_rgb

def is_color_match(pixel, min_rgb, max_rgb):
    """
    Check if the pixel's RGB values fall within the calculated range.
    """
    r, g, b = pixel
    return (min_rgb[0] <= r <= max_rgb[0] and
            min_rgb[1] <= g <= max_rgb[1] and
            min_rgb[2] <= b <= max_rgb[2])

def capture_center_box(box_size):
    """
    Capture a smaller portion of the screen for precise detection.
    Slightly bigger box size than before.
    """
    screenshot = np.array(ImageGrab.grab())
    h, w, _ = screenshot.shape
    center_x, center_y = w // 2, h // 2
    half_box = box_size // 2
    top_left_x = max(0, center_x - half_box)
    top_left_y = max(0, center_y - half_box)
    bottom_right_x = min(w, center_x + half_box)
    bottom_right_y = min(h, center_y + half_box)
    return screenshot[top_left_y:bottom_right_y, top_left_x:bottom_right_x, :]

def press_h_key():
    global h_press_timestamps

    # Get the current timestamp
    current_time = time.time()

    # Remove timestamps older than 0.35 seconds
    h_press_timestamps = [t for t in h_press_timestamps if current_time - t <= 0.35]

    # If two presses occurred within the last 0.35 seconds, delay
    if len(h_press_timestamps) >= 2:
        print("Delay to account for recoil")
        time.sleep(0.35)
        h_press_timestamps.clear()

    pyautogui.press('h')  # Use pyautogui to simulate the H key press
    print("Pressed 'H'")

    # Add the current timestamp
    h_press_timestamps.append(current_time)

def is_movement_key_pressed():
    return (
        win32api.GetAsyncKeyState(ord('W')) < 0 or
        win32api.GetAsyncKeyState(ord('A')) < 0 or
        win32api.GetAsyncKeyState(ord('S')) < 0 or
        win32api.GetAsyncKeyState(ord('D')) < 0
    )

def toggle_script_state():
    global running
    if running:
        running = False
        print("Script paused")
    else:
        running = True
        print("Script started")

def switch_mode():
    global current_mode, mode_index
    mode_index = (mode_index + 1) % len(available_modes)
    current_mode = available_modes[mode_index]
    print(f"Switched to {current_mode} mode")

async def detect_target(min_rgb, max_rgb, box_size):
    """
    Function to detect the target color in a defined screen area.
    Slightly bigger box to allow better accuracy.
    """
    center_box = capture_center_box(box_size)
    color_found = False

    # Check every pixel in the detection area for better precision
    for y in range(0, center_box.shape[0]):  # Checking every pixel in the box
        for x in range(0, center_box.shape[1]):
            pixel = center_box[y, x]
            if is_color_match(pixel, min_rgb, max_rgb):
                color_found = True
                break
        if color_found:
            break

    return color_found

async def main_loop():
    # Precompute the color range for the current mode
    target_colors = config["modes"][current_mode]["target_colors_rgb"]
    tolerance = config["modes"][current_mode]["color_tolerance"]
    min_rgb, max_rgb = calculate_color_range(target_colors, tolerance)

    while True:
        # Toggle script state with 'P'
        if win32api.GetAsyncKeyState(ord('P')) < 0:
            toggle_script_state()
            await asyncio.sleep(0.1)

        # Switch mode with 'I'
        if win32api.GetAsyncKeyState(ord('I')) < 0:
            switch_mode()
            target_colors = config["modes"][current_mode]["target_colors_rgb"]
            tolerance = config["modes"][current_mode]["color_tolerance"]
            min_rgb, max_rgb = calculate_color_range(target_colors, tolerance)
            await asyncio.sleep(0.1)

        # If the script is running and no movement keys are pressed, check for target color
        if running and not is_movement_key_pressed():
            color_found = await detect_target(min_rgb, max_rgb, config["modes"][current_mode]["box_size"])

            if color_found:
                press_h_key()  # Press "H" key when the color is detected directly in the narrowed crosshair
                print("Target color detected! Pressing 'H'.")

        # Reduce the sleep time for faster detection
        await asyncio.sleep(0.001)  # Faster detection loop

if __name__ == "__main__":
    # Create and start the main loop in a separate thread
    main_thread = threading.Thread(target=lambda: asyncio.run(main_loop()), daemon=True)
    main_thread.start()

    try:
        # Keep the main thread running, allowing you to exit gracefully
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Exiting...")
