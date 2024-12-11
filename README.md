

1. Create a Virtual Environment
Open a command prompt or terminal window.

Navigate to the folder where your code is saved. You can do this with the cd command. For example:

bash
Copy code
cd C:\Users\dylan\Desktop\triggy
Create a new virtual environment (if you haven't already). Replace venv with your preferred environment name if needed.

bash
Copy code
python -m venv venv
This will create a virtual environment named venv in your project folder.

2. Activate the Virtual Environment
Windows:

bash
Copy code
venv\Scripts\activate
Mac/Linux:

bash
Copy code
source venv/bin/activate
When the virtual environment is activated, you'll see (venv) at the beginning of the command line prompt.

3. Install the Required Libraries
Now, we need to install all the necessary libraries (such as win32api, pyautogui, Pillow, and numpy).

Run the following command to install the required libraries:

bash
Copy code
pip install pyautogui pillow numpy pywin32
pyautogui: For simulating key presses like 'H'.
pillow: For taking screenshots and image processing.
numpy: For array manipulation (which is used for handling screenshots).
pywin32: For interacting with Windows-specific functions like simulating key presses and getting keyboard state.
4. Run Your Code
After installing all the libraries, you're ready to run your script. Simply execute the following command:

bash
Copy code
python trig.py
This will start your Python script, and it should work as expected.

5. Deactivate the Virtual Environment (when done)
When you're finished working with your virtual environment, you can deactivate it by running:

bash
Copy code
deactivate
This will return you to the global Python environment.

Summary
Create a virtual environment:
bash
Copy code
python -m venv venv
Activate the virtual environment:
bash
Copy code
venv\Scripts\activate  # For Windows
Install the required libraries:
bash
Copy code
pip install pyautogui pillow numpy pywin32
Run the script:
bash
Copy code
python trig.py
Deactivate the virtual environment when done:
bash
Copy code
deactivate
