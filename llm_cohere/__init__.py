import click
import cohere
import llm
from pprint import pprint
from typing import Optional
from pydantic import field_validator, Field

@llm.hookimpl
def register_models(register):
    register(Generate("cohere-generate"))
    register(Summarize("cohere-summarize"))


@llm.hookimpl
def register_commands(cli):
    @cli.group(name="cohere")
    def cohere_():
        "Commands for working directly with Cohere"


class Generate(llm.Model):
    needs_key = "cohere"
    key_env_var = "COHERE_API_KEY"

    def __init__(self, model_id):
        self.model_id = model_id

    class Options(llm.Options):
        max_tokens: Optional[int] = Field(
            description="Number of tokens to generate",
            default=None
        )
        temperature: Optional[float] = Field(
            description="The randomness aspect of which tokens the model picks for output",
            default=None
        )

        @field_validator("max_tokens")
        def validate_max_tokens(cls, max_tokens):
            if max_tokens is None:
                return None
            if not 2 <= max_tokens <= 4000:
                raise ValueError("max_tokens must be between 2 and 4000")
            return max_tokens

        @field_validator("temperature")
        def validate_temperature(cls, temperature):
            if temperature is None:
                return None
            if not 0 <= temperature <= 2:
                raise ValueError("temperature must be between 0 and 2")
            return temperature


    def execute(self, prompt, stream, response, conversation):
        co = cohere.Client(api_key=self.get_key())

        kwargs = {
            'model': 'command',
            'prompt': prompt.prompt,
            'max_tokens': prompt.options.max_tokens or 200,
            'temperature': prompt.options.temperature or 0.75
        }

        if prompt.system:
            kwargs['prompt'] = prompt.system + ': ' + prompt.prompt

        cohere_response = co.generate(**kwargs)
        last = cohere_response.generations[0].text
        yield last or ""
        response._prompt_json = kwargs

    def __str__(self):
        return "Cohere: {}".format(self.model_id)


class Summarize(llm.Model):
    needs_key = "cohere"
    key_env_var = "COHERE_API_KEY"

    def __init__(self, model_id):
        self.model_id = model_id

    class Options(llm.Options):
        length: Optional[str] = Field(
            description="Indicates the approximate length of the summary. One of `short`, `medium`, `long`, or `auto` (default). If `auto` is selected, the best option will be picked based on the input text.",
            default="auto"
        )
        format: Optional[str] = Field(
            description="Indicates the style in which the summary will be delivered - in a free form paragraph or in bullet points. One of `paragraph`, `bullets`, or `auto` (default). If `auto` is selected, the best option will be picked based on the input text.",
            default="auto"
        )
        model: Optional[str] = Field(
            description="The ID of the model to generate the summary with. Currently available models are `summarize-medium` and `summarize-xlarge` (default). Smaller models are faster, while larger models will perform better",
            default="summarize-xlarge"
        )
        extractiveness: Optional[str] = Field(
            description="Controls how close to the original text the summary is. One of `low`, `medium`, `high`, or `auto` (default). High extractiveness summaries will lean towards reusing sentences verbatim, while low extractiveness summaries will tend to paraphrase more. If `auto` is selected, the best option will be picked based on the input text.",
            default="auto"
        )
        temperature: Optional[float] = Field(
            description="Controls the randomness of the output. Ranges from 0 to 5, defaults to 0.75. Lower values tend to generate more 'predictable' output, while higher values tend to generate more 'creative' output. The sweet spot is typically between 0 and 1.",
            default=0.75
        )
        additional_command: Optional[str] = Field(
            description="A free-form instruction for modifying how the summaries get generated. Should complete the sentence 'Generate a summary _'. Eg. 'focusing on the next steps' or 'written by Yoda'",
            default=None
        )

        @field_validator("length")
        def validate_length(cls, length):
            options = ['short', 'medium', 'long', 'auto']
            if length not in options:
                raise ValueError("length must be one of `short`, `medium`, `long` or `auto`.")
            return length
        @field_validator("format")
        def validate_format(cls, format):
            options = ['paragraph', 'bullets', 'auto']
            if format not in options:
                raise ValueError("format must be one of `paragraph`, `bullets`, or `auto`.")
            return format
        @field_validator("model")
        def validate_model(cls, model):
            options = ['summarize-medium', 'summarize-xlarge']
            if model not in options:
                raise ValueError("model must be one of `summarize-medium` or `summarize-xlarge`.")
            return model
        @field_validator("extractiveness")
        def validate_extractiveness(cls, extractiveness):
            options = ['low', 'medium', 'high', 'auto']
            if extractiveness not in options:
                raise ValueError("extractiveness must be one of `low`, `medium`, `high`, or `auto`.")
            return extractiveness
        @field_validator("temperature")
        def validate_temperature(cls, temperature):
            if temperature is None:
                return None
            if not 0 <= temperature <= 5:
                raise ValueError("temperature must be between 0 and 5")
            return temperature


    def execute(self, prompt, stream, response, conversation):
        co = cohere.Client(api_key=self.get_key())

        kwargs = {
            'text': prompt.prompt,
            'length': prompt.options.length or 'auto',
            'format': prompt.options.format or 'auto',
            'extractiveness': prompt.options.extractiveness or 'auto',
            'temperature': prompt.options.temperature or 0.75,
        }

        if prompt.options.additional_command:
            kwargs['additional_command'] = prompt.options.additional_command

        cohere_response = co.summarize(**kwargs)
        last = cohere_response.summary
        yield last or ""
        response._prompt_json = kwargs

    def __str__(self):
        return "Cohere: {}".format(self.model_id)
