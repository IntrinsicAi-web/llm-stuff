# MyLLM

LLM-from-scratch style experiments: tokenization, self-attention, and notebooks using PyTorch and tiktoken.

## Quick start (uv)

From the project root, run these in order:

```bash
# 1. Install uv (one time, if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install and pin Python 3.12 for this repo (Torch wheels are not available for cp313 on Intel macOS)
uv python install 3.12

# 3. Create .venv and install dependencies (use --no-install-project for notebook-only projects)
uv lock
uv sync --no-install-project

# 4. Activate the env and run the notebook
source .venv/bin/activate   # macOS/Linux
jupyter notebook book.ipynb
```

In Jupyter, choose the kernel that points to this project’s `.venv` so all dependencies are available.

---

## Setup with uv (full instructions)

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Dependencies are declared in `pyproject.toml` and locked in `uv.lock`.

### Prerequisites

- Python 3.10-3.12 on your system (`<3.13` because this repo pins `torch==2.2.2`)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed:

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # or: pip install uv
  ```

### One-time setup

From the project root:

```bash
# Install Python 3.12 if needed
uv python install 3.12

# Generate/update the lockfile from pyproject.toml
uv lock

# Create .venv and install all dependencies (without installing this project as a package)
uv sync --no-install-project
```

**Why `--no-install-project`?** This repo is notebook + scripts only (no `myllm` Python package directory). Using `--no-install-project` skips building/installing the project itself and avoids hatchling build errors. Dependencies (torch, tiktoken, notebook, matplotlib, etc.) are still installed into `.venv`.

### Running the notebook

**Option A — activate then run (recommended):**

```bash
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate   # Windows
jupyter notebook book.ipynb
# or: jupyter lab
```

**Option B — run via uv (no activate):**

```bash
uv run jupyter notebook book.ipynb
```

If Option B fails with a “Failed to build myllm” error, use Option A.

### Adding dependencies

```bash
# Add a package (updates pyproject.toml and uv.lock)
uv add <package>

# Then reinstall
uv sync --no-install-project
```

### After changing pyproject.toml by hand

```bash
uv lock
uv sync --no-install-project
```

### Dependencies (`pyproject.toml`)

| Package    | Version   | Purpose            |
|-----------|-----------|--------------------|
| matplotlib| ≥ 3.7.0   | Plotting           |
| notebook  | ≥ 7.1.0   | Jupyter notebook   |
| tiktoken  | ≥ 0.7.0   | Tokenizer (GPT-2)  |
| torch     | 2.2.2     | PyTorch (pinned for macOS compatibility) |

To export a `requirements.txt` from the lockfile:

```bash
uv export --no-hashes -o requirements.txt
```

## Project layout

- `book.ipynb` — main notebook (tokenization, embeddings, self-attention)
- `the-verdict.txt` — sample text (downloaded by notebook if missing)
- `pyproject.toml` — project metadata and dependencies
- `uv.lock` — locked dependency tree (commit this)

## Troubleshooting

- **`ModuleNotFoundError`** — Use the kernel that points to this project’s `.venv` (Kernel → Change kernel).
- **`RuntimeError: Numpy is not available`** — The plotting cell uses `.tolist()` to avoid this; if you see it elsewhere, ensure the kernel is the project `.venv` and run `uv sync --no-install-project`.
- **`Failed to build myllm`** — Use `uv sync --no-install-project` and run Jupyter after `source .venv/bin/activate` instead of `uv run jupyter`.
- **`torch ... doesn't have a wheel for cp313`** — This project now constrains Python to `<3.13`. Run `uv python install 3.12` and retry `uv sync --no-install-project`.
