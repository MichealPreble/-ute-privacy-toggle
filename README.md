# Architect CLI

Generate production-ready build plans (PRDs) for AI coding assistants using a reusable system prompt.

## Prerequisites
- Python 3.9+
- `openai` Python package (`pip install openai`)
- `OPENAI_API_KEY` environment variable set

## Files
- `architect_prompt.txt` — the strict system prompt that drives the planner.
- `build_architect.py` — CLI that sends your idea and saves the plan to `BUILD_PLAN.md`.

## Usage
```bash
export OPENAI_API_KEY="your-key-here"
python build_architect.py "A tinder-style app for adopting shelter dogs"
# or run without arguments to be prompted for the idea
```

Open `BUILD_PLAN.md` and feed each step to your AI coding assistant sequentially for structured implementation.
