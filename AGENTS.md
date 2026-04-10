# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

**Little Computer** — a Python tkinter desktop calculator application targeting Windows. Single-file app (`calculator.py`) with no external Python dependencies (tkinter is stdlib).

### Running the application

```bash
# On Linux, requires python3-tk package:
#   sudo apt-get install -y python3-tk
# If headless (no display), start Xvfb first:
#   Xvfb :99 -screen 0 1280x1024x24 &
#   export DISPLAY=:99
# On the Cloud Agent VM, the desktop display is DISPLAY=:1

python3 calculator.py
```

### Lint

```bash
ruff check calculator.py
```

No project-level ruff/pylint config exists; default ruff rules pass cleanly.

### Build (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --clean --noconfirm calculator.spec
# Output: dist/LittleComputer (Linux) or dist/LittleComputer.exe (Windows)
```

The `.spec` file and `installer.iss` (Inno Setup) target Windows. The GitHub Actions CI/CD workflow runs on `windows-latest` and is triggered by tag pushes (`v*`) or manual dispatch.

### Key caveats

- **No automated tests exist.** Validation is manual GUI interaction only.
- **Font rendering:** The app uses "Segoe UI" which is a Windows font. On Linux, tkinter falls back to a default font — this is cosmetic only.
- **`python3-tk`** must be installed as a system package on Ubuntu/Debian. It is NOT installable via pip.
- **Build artifacts** (`dist/`, `build/`, `Output/`) are not committed and should stay git-ignored.
