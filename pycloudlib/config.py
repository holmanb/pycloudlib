"""Deal with configuration"""
import os

import toml

CONFIG_PATH = os.path.expanduser('~/.config/pycloudlib.toml')


class Config(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            raise KeyError(
                "{} must be defined in {} to make this call".format(
                    key, CONFIG_PATH
                )
            ) from None


def parse_config(config_path=CONFIG_PATH):
    return toml.load(config_path, _dict=Config)


def choose_config(config, key, priority):
    """Choose configuration value to use.

    When a value is passed into the API, it should take priority. If the
    values wasn't passed, try to use the value in the configration file.
    """
    if priority:
        return priority
    return config.get(key, None)
