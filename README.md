# llm-cohere

[![PyPI](https://img.shields.io/pypi/v/llm-cohere.svg)](https://pypi.org/project/llm-cohere/)
[![Changelog](https://img.shields.io/github/v/release/accudio/llm-cohere?include_prereleases&label=changelog)](https://github.com/accudio/llm-cohere/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/accudio/llm-cohere/blob/main/LICENSE)

Plugin for [LLM](https://llm.datasette.io/) adding support for [Cohere](https://cohere.com)'s Generater and Summarize models.

## Installation

Install this plugin in the same environment as LLM.
```bash
llm install llm-cohere
```
## Configuration

You will need an API key from Cohere. You can obtain one by creating an account and going to 'API Keys'.

You can set that as an environment variable called `COHERE_API_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set cohere
```
```
Enter key: <paste key here>
```

## Usage

This plugin adds two models. `cohere-generate` uses an input prompt and generates output based on it. `summarize` takes an input prompt and generates a summarised response.

```bash
llm -m cohere-generate "Seven great names for a pet lemur"
```
PaLM also supports system prompts:
```bash
echo "I like lemurs a lot" | llm -m cohere-generate --system "Translate to german"
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-cohere
python3 -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```