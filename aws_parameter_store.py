from functools import partial
from io import FileIO

import click
from ssm_parameter_store import EC2ParameterStore


@click.command()
@click.argument("prefix", type=click.STRING)
@click.argument("output", type=click.File("w"))
def main(prefix, output):
    """Simple program that greets NAME for a total of COUNT times."""
    secrets = retrieve_aws_ssm_as_dict(key_prefix=prefix)
    print_dict_as_env(secrets, output=output)


def retrieve_aws_ssm_as_dict(key_prefix) -> dict:
    store = EC2ParameterStore()
    return store.get_parameters_by_path(
        path=key_prefix,
        decrypt=True,
        recursive=True,
        strip_path=True,
    )


def print_dict_as_env(dict_data: dict, output: FileIO):
    out = partial(print, file=output)
    for key, value in dict_data.items():
        upper_key = key.upper()
        out(f"{upper_key}={value}")


if __name__ == "__main__":
    main()

