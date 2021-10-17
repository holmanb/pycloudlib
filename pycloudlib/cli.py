from argparse import ArgumentParser
from typing import Dict, Type

from pycloudlib.cloud import BaseCloud
from pycloudlib.azure.cloud import Azure
from pycloudlib.ec2.cloud import EC2
from pycloudlib.gce.cloud import GCE
from pycloudlib.lxd.cloud import LXDContainer, LXDVirtualMachine
from pycloudlib.oci.cloud import OCI
from pycloudlib.openstack.cloud import Openstack

CLOUDS = {
    'azure': Azure,
    'ec2': EC2,
    'gce': GCE,
    'lxd_container': LXDContainer,
    'lxd_vm': LXDVirtualMachine,
    'oci': OCI,
    'openstack': Openstack,
}  # type: Dict[str, Type[BaseCloud]]


def launch(cloud, name, image, instance_type, userdata):
    cloud_class = CLOUDS[cloud](tag=name)
    image_id = cloud_class.released_image(image)
    kwargs = {'image_id': image_id}
    if instance_type:
        kwargs['instance_type'] = instance_type
    if userdata:
        kwargs['user_data'] = userdata
    cloud_class.launch(**kwargs)


def main():
    parser = ArgumentParser(description='One CLI to rule them all')
    subparsers = parser.add_subparsers(help='sub-command')

    parser_launch = subparsers.add_parser(
        'launch',
        help='Launch a new instance'
    )

    parser_launch.add_argument('name')
    parser_launch.add_argument('--cloud', choices=CLOUDS.keys())
    parser_launch.add_argument('--image', required=True)
    parser_launch.add_argument('--instance_type')
    parser_launch.add_argument('--userdata')

    args = parser.parse_args()
    launch(
        args.cloud, args.name, args.image, args.instance_type, args.userdata
    )


if __name__ == '__main__':
    main()
