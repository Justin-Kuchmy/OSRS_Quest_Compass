# Work In Progress

# OSRS Quest Compass 🧭
A CLI tool that tracks your Old School RuneScape skills and quest completions to suggest achievable quests you can work towards next.

---

## How It Works

1. **`parse.py`** reads your Excel spreadsheet containing your current stats and quest completions, then creates/updates a `quests.json` file.
2. **The main C++ program** reads `quests.json` and randomly suggests quests you are eligible to start or can realistically progress toward, based on your current skill levels and completed quests.

The tool will never suggest a quest if you don't meet its skill or quest prerequisites.

---

## Requirements

- Python 3.x
- A C++ compiler (e.g. `g++`, `clang++`, or MSVC)
- Your OSRS stats and quest completions in an Excel spreadsheet (`.xlsx`)

### Python dependencies

```bash
pip install pandas
```

---

## Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/OSRS_Quest_Compass.git
cd OSRS_Quest_Compass
```

### 2. Update your spreadsheet

Fill in your current skill levels and mark which quests you've completed in the Excel file.

### 3. Parse your data

```bash
python parse.py
```

This will generate or update `quests.json` with your current progress.

### 4. Compile the C++ program

```bash
g++ -o quest_compass main.cpp
```

### 5. Run it

```bash
./quest_compass
```

On Windows:

```bash
quest_compass.exe
```

The program will output a random suggestion for a quest you can work towards next.

---

## Platform Support

Works on **Windows**, **macOS**, and **Linux**.

---

## File Overview

| File | Description |
|---|---|
| `parse.py` | Reads the Excel spreadsheet and generates `quests.json` |
| `main.cpp` | Reads `quests.json` and outputs quest suggestions |
| `quests.json` | Auto-generated — do not edit manually |

---
