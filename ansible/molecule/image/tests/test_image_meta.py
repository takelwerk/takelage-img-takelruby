import os
import pytest
import takeltest

testinfra_hosts = [takeltest.hosts()[0]]


def test_image_meta_env_exists(image_meta_data):
    assert image_meta_data['Config']['Env'] is not None


@pytest.mark.parametrize('env, value', [(0, 'DEBIAN_FRONTEND=noninteractive'),
                                        (1, 'LANG=en_US.UTF-8'),
                                        (2, 'SUPATH='),
                                        (3, 'PATH='
                                            '/usr/local/sbin:'
                                            '/usr/local/bin:'
                                            '/usr/sbin:'
                                            '/usr/bin:'
                                            '/sbin:'
                                            '/bin')])
def test_image_meta_env_values(image_meta_data, env, value):
    assert value == image_meta_data['Config']['Env'][env]


def test_image_meta_cmd(testvars, image_meta_data):
    image = os.environ.get('TAKELAGE_PROJECT_IMG')
    if 'command' in testvars['project']['images'][image]:
        expected = testvars['project']['images'][image]['command']
    else:
        expected = '/usr/bin/tail -f /dev/null'
    assert expected.split(' ') == image_meta_data['Config']['Cmd']


def test_image_meta_work_dir(image_meta_data):
    assert '/root' == image_meta_data['Config']['WorkingDir']
