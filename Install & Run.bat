@echo off

:: Step 1: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Step 2: Clear pip cache to remove installed packages
echo Clearing pip cache...
pip cache purge

:: Step 3: Run the Python script
echo Running HookTool.py...
python HookTool.py

:: End of batch file
echo Batch process complete.
pause
