WPG - Wallpaper Generator
=========================

Generate blocked gradient wallpapers with Python.

### Installation

1. Set up virtualenv: `virtualenv -p python3 venv`
2. Install dependencies: `pip3 install -r requirements.txt`

### Usage

```bash
wpg.py [-h] -c COLOR [-e END_COLOR] [-b BLOCK_SIZE] width height
```

### Examples

```bash
wpg.py -c "#FF0000" -b 40 1920 1080
```

This will create a wallpaper (1920x1080), which displays the gradient from red to white. The step size will be approximately 40x40 pixels.

```bash
wpg.py -c "#0000FF" -e "#FF0000" 1600 900
```

This will create a wallpaper (1600x900), which displays the gradient from blue to red. The step size will be the GCD of width and height.
