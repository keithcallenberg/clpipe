import json
import datetime
import os
from pkg_resources import resource_stream


class ConfigParser:

    def __init__(self):
        self.setup_default_config()

    def config_json_parser(self,json_path):
        with open(json_path, "r") as config_file:
            config = json.load(config_file)

        return config

    def config_updater(self, newConfig):

        if newConfig is None:
            None
        else:
            self.config = {**self.config, **newConfig}
            self.config['dateRan'] = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

    def config_json_dump(self, filepath):
        with open(filepath, 'w') as fp:
            json.dump(self.config, fp)

    def setup_default_config(self):
        self.config = json.load(resource_stream(__name__,'data/defaultConfig.json'))


