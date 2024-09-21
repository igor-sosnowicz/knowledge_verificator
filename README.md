# Knowledge Verificator

**Knowledge Verificator** is a tool for self-learning. It employs *Natural Language Processing* (NLP) techniques to facilitate and increase effectiveness of self-study.
The project has been created as the Bachelor's Thesis of Igor Sosnowicz.

## Installation

### Install with `pipx`

If you have `pipx` already installed, use:

```bash
pipx install knowledge-verificator
```

### Install with `pip`

If you have `pip` already installed, use:

```bash
pip install knowledge-verificator
```

## Usage

### Run with `pipx`

If you have installed with `pipx`, run with:

```bash
pipx run knowledge-verificator
```

### Run with `pip`

If you have installed with `pip`, run with:

```bash
python -m knowledge_verificator
```

## Development

### Prerequisites
You have to have the following tools installed:
- build and dependency management system: [poetry](https://github.com/python-poetry/poetry)

### Steps
1. Clone the repository.
    ```bash
    git clone git@github.com:Iamhexi/knowledge_verificator.git
    ```

1. Enter its directory.
    ```bash
    cd knowledge_verificator
    ```

1. Install all dependencies, also including the optional ones.
    ```bash
    poetry install --with test
    ```

1. Build the package.
    ```bash
    poetry build
    ```

---
As a one-liner:

```bash
git clone git@github.com:Iamhexi/knowledge_verificator.git && cd knowledge_verificator && poetry install --with test && poetry build
```
---

And then run the application.
```bash
poetry run python knowledge_verificator/main.py
```
