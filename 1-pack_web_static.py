#!/usr/bin/python3
from datetime import datetime
from fabric.api import local

def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now()
    dt_string = now.strftime("web_static_%Y%m%d%H%m%S")
    output_file = "versions/{:}.tgz".format(dt_string)
    local("mkdir -p versions")
    result = local("tar -cvzf {:} web_static".format(output_file))
    if result.failed:
        return None
    return output_file
