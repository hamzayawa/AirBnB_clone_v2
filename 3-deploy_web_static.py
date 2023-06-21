#!/usr/bin/python3
"""creates and distributes an archive to web servers.
using the function deploy
"""

from datetime import datetime
from fabric.api import *
import os.path


env.hosts = ['101.188.67.134', '101.188.67.134']


def deploy():
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


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


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    archive_list = archive_path.split("/")
    archive_filename = archive_list[-1]
    filename_list = archive_filename.split(".")
    filename_noext = filename_list[0]
    result = put(archive_path, "/tmp/")
    if result.failed:
        return False
    result = run('mkdir -p /data/web_static/releases/{:}/'.format(
        filename_noext))
    if result.failed:
        return False
    result = run('tar -xzf /tmp/{:} -C /data/web_static/releases/{:}/'.format(
        archive_filename, filename_noext))
    if result.failed:
        return False
    result = run('rm /tmp/{:}'.format(archive_filename))
    if result.failed:
        return False
    result = run('mv /data/web_static/releases/{:}/web_static/* \
                 /data/web_static/releases/{:}/'.format(
                     filename_noext, filename_noext))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/releases/{:}/web_static".format(
        filename_noext))
    if result.failed:
        return False
    result = run('rm -rf /data/web_static/current')
    if result.failed:
        return False
    result = run(
        'ln -s /data/web_static/releases/{:}/ /data/web_static/current'.format(
            filename_noext))
    if result.failed:
        return False
    return True
