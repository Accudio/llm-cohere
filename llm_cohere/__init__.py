import click
import cohere  
import llm
from pprint import pprint
from typing import Optional
from pydantic import field_validator, Field

@llm.hookimpl
def register_models(register):
    register(Generate("cohere-generate"))


@llm.hookimpl
def register_commands(cli):
    @cli.group(name="cohere")
    def cohere_():
        "Commands for working directly with Cohere"

    @cohere_.command()
    @click.option("--key", help="Cohere API key")
    def models(key):
        "List models available in the Cohere API"
        api_key = llm.get_key(key, "cohere", "COHERE_API_KEY")
        cohere.configure(api_key=api_key)
        models = cohere.list_models()
        pprint(list(models))


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
            'temperature': prompt.options.temperature or 0.750
        }

        cohere_response = co.generate(**kwargs)
        last = cohere_response.generations[0].text
        yield last or ""
        response._prompt_json = kwargs

    def __str__(self):
        return "Cohere: {}".format(self.model_id)
