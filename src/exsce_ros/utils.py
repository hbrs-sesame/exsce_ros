import os
import yaml

import rospkg

from itertools import tee


def get_package_path(package, subfolder=""):
    rospack = rospkg.RosPack()
    pkg_path = os.path.join(rospack.get_path(package), subfolder)
    return pkg_path


def get_file_path(file_name, package="metamorphic_testing", subfolder="runs"):
    pkg_path = get_package_path(package, subfolder)
    file_path = os.path.join(pkg_path, file_name)
    return file_path


class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


def dump_yaml(dictionary):
    return yaml.dump(dictionary, default_flow_style=False, Dumper=Dumper)


def write_yaml_file(file_path, contents_as_dict):
    with open(file_path, "w") as yaml_file:
        yaml_file.write(dump_yaml(contents_as_dict))


def load_yaml(file_path):
    with open(file_path, "r") as yaml_file:
        file_contents = yaml.load(yaml_file, Loader=yaml.FullLoader)

    return file_contents


def save_prov_file(file_name_prefix, prov):
    prov_file_name = "{}.prov.json".format(file_name_prefix)
    file_path = get_file_path(prov_file_name)
    prov.serialize(file_path, indent=2)
    prov.plot("{}.svg".format(file_path))
    return file_path


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
