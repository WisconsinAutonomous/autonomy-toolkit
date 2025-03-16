# SPDX-License-Identifier: MIT
"""
System utilities for the autonomy_toolkit package
"""

def is_port_available(port: int, udp: bool = False) -> bool:
    """Checks whether a specified port is available to be attached to.

    From `podman_compose <https://github.com/containers/podman-compose/blob/devel/podman_compose.py>`_.

    Args:
        port (int): The port to check.
        udp (bool): Also check udp

    Returns:
        bool: True if available, False otherwise.
    """
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        in_use = s.connect_ex(('localhost', int(port))) == 0

    if udp:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            in_use = s.connect_ex(('localhost', int(port))) == 0 or in_use

    return not in_use

def get_mac_address() -> str:
    """
    Returns the MAC address of the first non-loopback interface.
    """
    addrs = psutil.net_if_addrs()
    for interface, snics in addrs.items():
        if interface.lower() == 'lo' or interface.startswith('Loopback'):
            continue
        for snic in snics:
            # psutil.AF_LINK is usually available as the family for MAC addresses
            if snic.family == psutil.AF_LINK and snic.address != '00:00:00:00:00:00':
                return snic.address
    return "00:00:00:00:00:00"

def getuser() -> str:
    """
    Get the username of the current user.

    Will leverage the ``getpass`` package.

    Returns:
        str: The username of the current user
    """
    import getpass
    return getpass.getuser()

def getuid(default: int = 1000) -> int:
    """
    Get the uid (user id) for the current user.

    If a Posix system (Linux, Mac) is detected, ``os.getuid`` is used. Otherwise, ``default`` is returned.

    Args:
        default (int): The default value if a posix system is not detected. Defaults to 1000. 

    Returns:
        int: The uid, either grabbed from the current user or the default if not a posix system.
    """
    import os
    return os.getuid() if os.name == "posix" else default

def getgid(default: int = 1000) -> int:
    """
    Get the gid (group id) for the current user.

    If a Posix system (Linux, Mac) is detected, ``os.getgid`` is used. Otherwise, ``default`` is returned.

    Args:
        default (int): The default value if a posix system is not detected. Defaults to 1000. 

    Returns:
        int: The gid, either grabbed from the current user or the default if not a posix system.
    """
    import os
    return os.getgid() if os.name == "posix" else default
