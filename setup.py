from setuptools import setup
import os

VERSION = "1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="llm-cohere",
    description="Plugin for LLM adding support for Cohere's Generate and Summarize models",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Alistair Shepherd",
    url="https://github.com/accudio/llm-cohere",
    project_urls={
        "Issues": "https://github.com/accudio/llm-cohere/issues",
        "CI": "https://github.com/accudio/llm-cohere/actions",
        "Changelog": "https://github.com/accudio/llm-cohere/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=["License :: OSI Approved :: Apache Software License"],
    version=VERSION,
    packages=["llm_cohere"],
    entry_points={"llm": ["llm_cohere = llm_cohere"]},
    install_requires=[
        "llm>=0.5",
        "cohere",
        "fastavro==1.8.2"
    ],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    python_requires=">=3.9",
)